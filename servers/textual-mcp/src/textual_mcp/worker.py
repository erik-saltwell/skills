"""One trusted application per process, with a dedicated JSON control channel."""

import asyncio
import hashlib
import importlib
import importlib.util
import json
import os
import random
import sys
import time
import traceback
from collections import deque
from importlib.metadata import version
from pathlib import Path
from typing import Any

from textual import events
from textual._context import active_message_pump
from textual.app import App

from textual_mcp.capture import capture
from textual_mcp.inspection import (
    identity,
    inspect_app,
    snapshot,
    source_of,
    text_of,
    unique_widget,
    value_of,
    visible_region,
)
from textual_mcp.models import Launch, Wait, actions_adapter


def load_app(launch: Launch) -> App:
    random.seed(launch.seed)
    sys.path.insert(0, str(Path.cwd()))
    target = Path(launch.target)
    if target.suffix == ".py":
        target = target.resolve(strict=True)
        sys.path.insert(0, str(target.parent))
        spec = importlib.util.spec_from_file_location("_textual_mcp_target", target)
        if spec is None or spec.loader is None:
            raise ValueError(f"Cannot import {target}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    else:
        module = importlib.import_module(launch.target)
    factory = module
    for part in launch.factory.split("."):
        factory = getattr(factory, part)
    app = factory if isinstance(factory, App) else factory(**launch.kwargs)
    if not isinstance(app, App):
        raise TypeError("factory must resolve to a Textual App instance or return one")
    if factory is app and launch.kwargs:
        raise ValueError("kwargs cannot be used with an existing App instance")
    return app


class Runtime:
    def __init__(self, launch: Launch, directory: Path) -> None:
        self.launch = launch
        self.directory = directory
        self.app: App = load_app(launch)
        self.pilot = None
        self.sequence = 0
        self.event_number = 0
        self.events: deque[dict] = deque(maxlen=1000)
        self.actions: list[dict] = []
        self.captures: list[dict] = []
        self.last_action_error: dict | None = None
        self.started = time.monotonic()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.environment = {
            "python": sys.version,
            "executable": sys.executable,
            "textual": version("textual"),
            "rich": version("rich"),
            "cwd": str(Path.cwd()),
            "terminal": {name: os.environ.get(name) for name in ("TERM", "COLORTERM", "NO_COLOR")},
            "seed": launch.seed,
            "app_source": source_of(type(self.app)),
        }
        source_file = self.environment["app_source"].get("file")
        self.environment["app_source_sha256"] = (
            hashlib.sha256(Path(source_file).read_bytes()).hexdigest() if source_file else None
        )
        self.write_record(
            {"kind": "launch", "launch": launch.model_dump(), "environment": self.environment}
        )

    def write_record(self, record: dict) -> None:
        with (self.directory / "journal.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    def message_hook(self, message: Any) -> None:
        if type(message).__name__ in {
            "Idle",
            "Update",
            "Layout",
            "UpdateScroll",
            "Callback",
            "Prompt",
            "InvokeLater",
            "Timer",
        }:
            return
        receiver = active_message_pump.get(None)
        self.event_number += 1
        data = {
            "number": self.event_number,
            "sequence": self.sequence,
            "elapsed": round(time.monotonic() - self.started, 6),
            "message": f"{type(message).__module__}.{type(message).__qualname__}",
            "receiver": identity(receiver),
            "handler_name": message.handler_name,
        }
        # This is dispatch evidence, not a claim that a convention-based handler ran.
        # Decorated handlers can have different names; inspect exposes their source too.
        sender = getattr(message, "_sender", None)
        data["sender"] = identity(sender)
        self.events.append(data)

    def check_alive(self) -> None:
        error = self.app._exception
        if error:
            raise RuntimeError(f"Application crashed: {type(error).__name__}: {error}") from error
        if not self.app.is_running:
            raise RuntimeError("Application exited. Launch or replay to create a fresh session.")

    def state(self) -> dict:
        if not self.app.is_running:
            return {"running": False, "return_value": value_of(self.app.return_value)}
        return snapshot(self.app)

    def diagnostics(self, since: int = 0, limit: int = 100) -> dict:
        selected = [event for event in self.events if event["number"] > since]
        error = self.app._exception
        return {
            "state": self.state(),
            "environment": self.environment,
            "exception": "".join(traceback.format_exception(error)) if error else None,
            "last_action_error": self.last_action_error,
            "events": selected[:limit],
            "next_since": selected[min(limit, len(selected)) - 1]["number"] if selected else since,
            "latest_event": self.event_number,
            "events_lost": max(0, self.events[0]["number"] - since - 1) if self.events else 0,
            "event_note": (
                "Dispatch observations; timers/render housekeeping omitted; last 1000 retained."
            ),
        }

    async def wait_condition(self, action: Wait) -> dict:
        deadline = time.monotonic() + action.timeout
        observed = None
        while True:
            self.check_alive()
            matches = list(self.app.screen.query(action.selector))
            if action.condition in {"exists", "absent"}:
                observed = bool(matches)
                matched = observed if action.condition == "exists" else not observed
            else:
                if len(matches) > 1:
                    raise ValueError("Condition target is ambiguous; use a unique selector.")
                matched = False
                if matches:
                    widget = matches[0]
                    if action.condition == "visible":
                        observed = bool(visible_region(widget))
                        matched = observed
                    elif action.condition == "focused":
                        observed = widget.has_focus
                        matched = observed
                    elif action.condition == "enabled":
                        observed = not widget.is_disabled
                        matched = observed
                    elif action.condition == "text":
                        observed = text_of(widget)
                        matched = action.value in observed
                    else:
                        observed = getattr(widget, action.attribute)
                        matched = observed == action.value
            if matched:
                return {"condition": action.condition, "observed": value_of(observed)}
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Condition {action.condition!r} on {action.selector!r} timed out; "
                    f"observed {value_of(observed)!r}"
                )
            await self.pilot.pause(0.05)

    async def do_action(self, action: Any) -> dict:
        self.check_alive()
        pilot = self.pilot
        if action.kind == "press":
            await pilot.press(*action.keys)
        elif action.kind == "paste":
            self.app.post_message(events.Paste(action.text))
        elif action.kind == "focus":
            widget = unique_widget(self.app, action.selector)
            widget.focus()
            await pilot.pause()
            if self.app.focused is not widget:
                raise ValueError(
                    "Widget did not accept focus; check visibility, disabled, and can_focus."
                )
        elif action.kind == "resize":
            await pilot.resize_terminal(action.width, action.height)
        elif action.kind == "pause":
            await pilot.pause(action.seconds)
        elif action.kind == "wait":
            return await self.wait_condition(action)
        elif action.kind == "action":
            if not await self.app.run_action(action.action):
                raise ValueError(
                    "Textual action was not handled; inspect bindings and action methods."
                )
        elif action.kind == "capture":
            await pilot.pause()
            result = capture(self.app, action, self.directory / "captures", self.sequence)
            self.captures.append(result)
            return result
        else:
            widget = unique_widget(self.app, action.selector) if action.selector else None
            kwargs = {
                "widget": widget,
                "offset": (action.x, action.y),
                "shift": action.shift,
                "meta": action.meta,
                "control": action.control,
            }
            if action.kind == "click":
                landed = await pilot.click(**kwargs, button=action.button, times=action.times)
            elif action.kind == "mouse_down":
                landed = await pilot.mouse_down(**kwargs, button=action.button)
            elif action.kind == "mouse_up":
                landed = await pilot.mouse_up(**kwargs)
            elif action.kind == "hover":
                landed = await pilot.hover(widget, offset=(action.x, action.y))
            else:
                # Pilot has no public wheel/drag move methods. Keep this one private
                # compatibility seam shared with Pilot's own hit-testing/forwarding.
                event_type = (
                    events.MouseMove
                    if action.kind == "mouse_move"
                    else {
                        "up": events.MouseScrollUp,
                        "down": events.MouseScrollDown,
                        "left": events.MouseScrollLeft,
                        "right": events.MouseScrollRight,
                    }[action.direction]
                )
                landed = await pilot._post_mouse_events(
                    [event_type] * (action.amount if action.kind == "scroll" else 1),
                    **kwargs,
                    button=action.button if action.kind == "mouse_move" else 0,
                )
            if not landed:
                raise ValueError(
                    "Mouse event missed the specified widget (possibly obscured or clipped). "
                    "Inspect the active screen and coordinates."
                )
        if self.app.is_running:
            await pilot.pause()
        if self.app._exception:
            self.check_alive()
        return {"state": self.state()}

    async def act(self, raw_actions: list[dict]) -> dict:
        actions = actions_adapter.validate_python(raw_actions)
        completed = []
        for action in actions:
            if len(self.actions) >= 2000:
                return {
                    "ok": False,
                    "completed": completed,
                    "error": (
                        "Session action limit reached (2000). Export and launch a fresh session."
                    ),
                }
            self.sequence += 1
            self.actions.append(action.model_dump())
            before = self.state()
            first_event = self.event_number
            record = {
                "sequence": self.sequence,
                "action": action.model_dump(),
                "before": before,
                "elapsed": round(time.monotonic() - self.started, 6),
            }
            self.write_record({"kind": "action_started", **record})
            deadline = asyncio.timeout(35)
            try:
                async with deadline:
                    result = await self.do_action(action)
                record.update(ok=True, result=result)
            except Exception as error:
                record.update(
                    ok=False,
                    error=f"{type(error).__name__}: {error}",
                    traceback=traceback.format_exc(),
                )
                record["fatal"] = deadline.expired()
                self.last_action_error = {
                    "sequence": self.sequence,
                    "error": record["error"],
                    "traceback": record["traceback"],
                }
            record["after"] = self.state()
            record["event_range"] = (
                [first_event + 1, self.event_number] if self.event_number > first_event else None
            )
            self.write_record({"kind": "action_finished", **record})
            completed.append(record)
            if not record["ok"]:
                return {
                    "ok": False,
                    "completed": completed,
                    "failed_sequence": self.sequence,
                    "error": record["error"],
                    "fatal": record.get("fatal", False),
                    "diagnostics": self.diagnostics(max(0, self.event_number - 30)),
                }
        return {"ok": True, "completed": completed, "state": self.state()}

    def export(self) -> dict:
        scenario = {"version": 1, "launch": self.launch.model_dump(), "actions": self.actions}
        scenario_path = self.directory / "scenario.json"
        scenario_path.write_text(json.dumps(scenario, indent=2), encoding="utf-8")
        diagnostics_path = self.directory / "diagnostics.json"
        diagnostics_path.write_text(
            json.dumps(self.diagnostics(limit=1000), indent=2), encoding="utf-8"
        )
        manifest_path = self.directory / "captures.json"
        manifest_path.write_text(json.dumps(self.captures, indent=2), encoding="utf-8")
        guide_path = self.directory / "evidence.md"
        lines = [
            "# Documentation evidence",
            "",
            "Captures are linked to action numbers in `journal.jsonl`.",
            "",
        ]
        for item in self.captures:
            label = item["label"].replace("\n", " ")
            image_path = Path(item["png"]).relative_to(self.directory)
            lines.extend(
                [
                    f"## Action {item['sequence']}: {label}",
                    "",
                    f"![Screenshot]({image_path})",
                    "",
                    f"State: `{json.dumps(item['state'])}`",
                    "",
                ]
            )
        guide_path.write_text("\n".join(lines), encoding="utf-8")
        return {
            "scenario": str(scenario_path),
            "journal": str(self.directory / "journal.jsonl"),
            "diagnostics": str(diagnostics_path),
            "captures": str(manifest_path),
            "evidence": str(guide_path),
            "action_count": len(self.actions),
            "note": (
                "Scenario includes attempted actions, including failures. "
                "Replay stops at the first failure. External data and time are not reset."
            ),
        }


async def serve(reader: asyncio.StreamReader, control: Any) -> None:
    def send(payload: dict) -> None:
        control.write(json.dumps(payload, ensure_ascii=False) + "\n")
        control.flush()

    runtime = None
    try:
        line = await reader.readline()
        if not line:
            return
        config = json.loads(line)
        runtime = Runtime(Launch.model_validate(config["launch"]), Path(config["directory"]))
        async with runtime.app.run_test(
            size=(runtime.launch.width, runtime.launch.height),
            tooltips=runtime.launch.tooltips,
            notifications=runtime.launch.notifications,
            message_hook=runtime.message_hook,
        ) as pilot:
            runtime.pilot = pilot
            await pilot.pause()
            runtime.check_alive()
            send(
                {
                    "ok": True,
                    "result": {"state": runtime.state(), "environment": runtime.environment},
                }
            )
            while line := await reader.readline():
                request = json.loads(line)
                method, args = request["method"], request.get("args", {})
                try:
                    if method == "stop":
                        send({"ok": True, "result": runtime.export()})
                        break
                    if method == "act":
                        result = await runtime.act(args["actions"])
                    elif method == "inspect":
                        runtime.check_alive()
                        await pilot.pause()
                        result = inspect_app(runtime.app, **args)
                    elif method == "diagnostics":
                        result = runtime.diagnostics(**args)
                    elif method == "export":
                        result = runtime.export()
                    else:
                        raise ValueError(f"Unknown worker method: {method}")
                    send({"ok": True, "result": result})
                except Exception as error:
                    send(
                        {
                            "ok": False,
                            "error": f"{type(error).__name__}: {error}",
                            "traceback": traceback.format_exc(),
                        }
                    )
    except Exception as error:
        send(
            {
                "ok": False,
                "error": f"{type(error).__name__}: {error}",
                "traceback": traceback.format_exc(),
            }
        )
    finally:
        if runtime:
            runtime.export()


async def main_async() -> None:
    # Duplicate the protocol descriptor, then redirect even low-level app writes
    # on fd 1 to stderr before importing application code.
    control = os.fdopen(os.dup(sys.stdout.fileno()), "w", buffering=1, encoding="utf-8")
    os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
    reader = asyncio.StreamReader(limit=4 * 1024 * 1024)
    protocol = asyncio.StreamReaderProtocol(reader)
    transport, _ = await asyncio.get_running_loop().connect_read_pipe(
        lambda: protocol, sys.stdin.buffer
    )
    try:
        await serve(reader, control)
    finally:
        transport.close()
        control.close()


if __name__ == "__main__":
    asyncio.run(main_async())
