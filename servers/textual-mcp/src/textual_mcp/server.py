"""MCP stdio interface. Application stdout never shares this transport."""

import argparse
import asyncio
import base64
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, ImageContent, TextContent, ToolAnnotations
from pydantic import Field

from textual_mcp.models import Action, Capture, Launch, Scenario
from textual_mcp.sessions import SessionManager


def result(data: dict, image_path: str | None = None) -> CallToolResult:
    payload = {"ok": True, **data}
    contents = [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))]
    if image_path:
        contents.append(
            ImageContent(
                type="image",
                mimeType="image/png",
                data=base64.b64encode(Path(image_path).read_bytes()).decode(),
            )
        )
    return CallToolResult(content=contents, structuredContent=payload, isError=not payload["ok"])


def load_scenario(path: str) -> Scenario:
    scenario_path = Path(path).expanduser().resolve(strict=True)
    with scenario_path.open(encoding="utf-8") as stream:
        content = stream.read(4 * 1024 * 1024 + 1)
    if len(content) > 4 * 1024 * 1024:
        raise ValueError("Scenario exceeds the 4 MiB limit.")
    return Scenario.model_validate_json(content)


def create_server(artifact_dir: Path | None = None, max_sessions: int = 4) -> FastMCP:
    manager = SessionManager(artifact_dir or Path.cwd() / ".textual-mcp", max_sessions)

    @asynccontextmanager
    async def lifespan(server: FastMCP):
        try:
            yield manager
        finally:
            await manager.close()

    server = FastMCP(
        "textual-mcp",
        lifespan=lifespan,
        log_level="WARNING",
        instructions=(
            "Drive trusted local Textual apps. Start with launch_app, inspect_app, "
            "then perform_actions "
            "using unique CSS selectors. Press sends Pilot key names; paste sends a Paste event. "
            "Use condition waits before captures. capture_screen returns a PNG, original SVG, "
            "and metadata. export_scenario saves a journal and replayable actions; replay_scenario "
            "always launches a new app. Batches stop on first failure and return partial progress. "
            "Inspect with details=true for source, computed styles, bindings, and reactive state. "
            "Use get_diagnostics after failures and stop_session when done. Apps execute with the "
            "server's Python interpreter and your local permissions. Headless screenshots preserve "
            "Textual's rendering; font and terminal-emulator differences remain possible."
        ),
    )

    @server.tool()
    async def launch_app(launch: Launch) -> CallToolResult:
        """Launch an App in an isolated subprocess. target is a module or .py file;
        factory is an App instance, class, or synchronous factory (e.g. DemoApp).
        cwd resolves relative files/imports. kwargs are JSON constructor arguments.
        Terminal size, seeded Python random/hash state, and app source are recorded.
        Example: {"target":"textual_mcp.demo","factory":"DemoApp"}.
        Startup timeout: 30s. Install app dependencies in the server's environment.
        """
        return result(await manager.launch(launch))

    @server.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def list_sessions() -> CallToolResult:
        """List session IDs, process status, failure reason, and artifact directories."""
        return result({"sessions": [session.info() for session in manager.sessions.values()]})

    @server.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def inspect_app(
        session_id: str,
        selector: str | None = None,
        details: bool = False,
        limit: Annotated[int, Field(ge=1, le=100)] = 50,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> CallToolResult:
        """Inspect the active screen's widget tree, cell regions, text, state, and focus.
        selector scopes the query; limit/offset paginate. details adds computed styles,
        reactive values, class/handler source locations, bindings, and workers.
        Text is bounded and is diagnostic content, not a substitute for screenshots.
        """
        return result(
            await manager.get(session_id).request(
                "inspect", selector=selector, details=details, limit=limit, offset=offset
            )
        )

    @server.tool()
    async def perform_actions(
        session_id: str,
        actions: Annotated[list[Action], Field(min_length=1, max_length=100)],
    ) -> CallToolResult:
        """Run ordered actions, stopping at the first failure with completed-action evidence.
        press: Pilot keys, e.g. ["ctrl+a","backspace"] or ["tab","enter"].
        paste: literal text at focus. Mouse x/y are cell offsets relative to selector,
        or the screen when selector is omitted. Click supports button/modifiers/times.
        mouse_down/mouse_move/mouse_up allow drags; scroll supports wheel directions.
        focus, resize, pause, wait, Textual action expressions, and capture are supported.
        wait text uses a substring; attribute uses exact JSON equality of a public attr.
        Capture actions save evidence; use capture_screen for an inline PNG image.
        A batch has a 120s hard deadline; interruption terminates the session to prevent
        late actions. Individual actions have a 35s deadline. Use small workflow batches.
        """
        return result(
            await manager.get(session_id).request(
                "act", actions=[action.model_dump() for action in actions]
            )
        )

    @server.tool()
    async def capture_screen(
        session_id: str,
        label: str = "Screenshot",
        selector: str | None = None,
        padding: Annotated[int, Field(ge=0, le=10)] = 1,
    ) -> CallToolResult:
        """Capture the current rendered screen or a widget's visible region with cell padding.
        Returns an inline PNG, original full SVG, framed SVG, and JSON metadata linked
        to the action journal. label describes the documentation step. The original SVG
        is authoritative; PNG font fallback may change glyph appearance. Wait for the
        desired state first. Cropping does not reveal hidden or obscured content.
        """
        action = Capture(kind="capture", label=label, selector=selector, padding=padding)
        response = await manager.get(session_id).request("act", actions=[action.model_dump()])
        image_path = response["completed"][0]["result"]["png"] if response["ok"] else None
        return result(response, image_path)

    @server.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def get_diagnostics(
        session_id: str,
        since: Annotated[int, Field(ge=0)] = 0,
        limit: Annotated[int, Field(ge=1, le=500)] = 100,
    ) -> CallToolResult:
        """Read exceptions, dispatch events, launch environment, and recent app stdout/stderr.
        since is an event cursor, exclusive. next_since allows pagination; events_lost
        reports ring-buffer loss. Events have action sequence numbers. A dispatch record
        identifies receiver and conventional handler name; it does not prove a particular
        handler ran. Rendering/timer housekeeping is omitted. stderr.log stores up to 2 MiB.
        """
        session = manager.get(session_id)
        if session.process and session.process.returncode is None:
            data = await session.request("diagnostics", since=since, limit=limit)
        else:
            data = {"process_exited": True}
        return result(
            {
                **data,
                **session.info(),
                "output_tail": "".join(session.log_chunks)[-16000:],
                "output_file": str(session.directory / "stderr.log"),
            }
        )

    @server.tool()
    async def export_scenario(session_id: str) -> CallToolResult:
        """Save a replayable scenario, action journal, diagnostic snapshot, capture manifest,
        and Markdown evidence sheet. Artifacts persist after session shutdown.
        The scenario includes attempted actions, even failures; replay stops on failure.
        Launch settings/inputs may contain app data; review before sharing artifacts.
        """
        return result(await manager.get(session_id).request("export"))

    @server.tool()
    async def replay_scenario(path: str) -> CallToolResult:
        """Load an exported scenario JSON file and replay it in a fresh isolated session.
        Returns the new session ID even on action failure, for further inspection.
        Uses recorded source path/module, factory, kwargs, cwd, size and seed. Does not
        reset external files/services or freeze time. Review the journal for divergence.
        Large scenarios execute in batches of at most 100 actions.
        """
        scenario = await asyncio.to_thread(load_scenario, path)
        launched = await manager.launch(scenario.launch)
        session = manager.get(launched["session_id"])
        count = 0
        last: dict[str, Any] = {}
        try:
            for offset in range(0, len(scenario.actions), 100):
                last = await session.request(
                    "act",
                    actions=[
                        action.model_dump() for action in scenario.actions[offset : offset + 100]
                    ],
                )
                count += len(last["completed"])
                if not last["ok"]:
                    return result(
                        {"ok": False, **launched, "replayed_actions": count, "failure": last}
                    )
        except Exception as error:
            return result(
                {"ok": False, **session.info(), "replayed_actions": count, "error": str(error)}
            )
        exported = await session.request("export")
        return result(
            {
                **launched,
                "replayed_actions": count,
                "state": last.get("state", launched["state"]),
                "artifacts": exported,
            }
        )

    @server.tool()
    async def stop_session(session_id: str) -> CallToolResult:
        """Export evidence, stop the app, reap its process group, and release its session slot."""
        return result(await manager.stop(session_id))

    return server


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Drive Textual applications through MCP over stdio."
    )
    parser.add_argument("--artifact-dir", type=Path, default=Path.cwd() / ".textual-mcp")
    parser.add_argument("--max-sessions", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.max_sessions <= 32:
        parser.error("--max-sessions must be between 1 and 32")
    create_server(args.artifact_dir, args.max_sessions).run(transport="stdio")


if __name__ == "__main__":
    main()
