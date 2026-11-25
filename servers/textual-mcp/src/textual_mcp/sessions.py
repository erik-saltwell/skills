"""Process supervision, bounded transport, and deterministic cleanup."""

import asyncio
import json
import os
import signal
import sys
import uuid
from collections import deque
from pathlib import Path
from typing import Any

from textual_mcp.models import Launch


class Session:
    def __init__(self, session_id: str, launch: Launch, directory: Path) -> None:
        self.id = session_id
        self.launch = launch
        self.directory = directory
        self.process: asyncio.subprocess.Process | None = None
        self.lock = asyncio.Lock()
        self.log_chunks: deque[str] = deque(maxlen=16)
        self.log_task: asyncio.Task | None = None
        self.failure: str | None = None

    async def start(self) -> dict:
        env = os.environ.copy()
        env.pop("NO_COLOR", None)
        env.update(
            TERM="xterm-256color", COLORTERM="truecolor", PYTHONHASHSEED=str(self.launch.seed)
        )
        self.directory.mkdir(parents=True, exist_ok=True)
        self.process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-u",
            "-m",
            "textual_mcp.worker",
            cwd=self.launch.cwd,
            env=env,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=8 * 1024 * 1024,
            start_new_session=os.name == "posix",
        )
        self.log_task = asyncio.create_task(self.drain_logs())
        async with self.lock:
            return await self.exchange(
                {"launch": self.launch.model_dump(), "directory": str(self.directory)}, 30
            )

    async def drain_logs(self) -> None:
        written = 0
        with (self.directory / "stderr.log").open("wb") as stream:
            while chunk := await self.process.stderr.read(4096):
                self.log_chunks.append(chunk.decode("utf-8", errors="replace"))
                # Always drain the pipe; bound stored logs to 2 MiB per session.
                if written < 2 * 1024 * 1024:
                    stream.write(chunk)
                    stream.flush()
                    written += len(chunk)
                elif written == 2 * 1024 * 1024 or written < 2 * 1024 * 1024 + 4096:
                    stream.write(b"\n[stored log truncated at 2 MiB; pipe still drained]\n")
                    written = 2 * 1024 * 1024 + 4096

    def info(self) -> dict:
        return {
            "session_id": self.id,
            "target": self.launch.target,
            "factory": self.launch.factory,
            "process_running": bool(self.process and self.process.returncode is None),
            "failure": self.failure,
            "artifact_dir": str(self.directory),
        }

    async def exchange(self, payload: dict, budget_seconds: float) -> dict:
        encoded = (json.dumps(payload) + "\n").encode()
        if len(encoded) > 4 * 1024 * 1024:
            raise ValueError("Control request exceeds 4 MiB. Split the action batch or input.")
        try:
            async with asyncio.timeout(budget_seconds):
                if not self.process or self.process.returncode is not None:
                    raise RuntimeError(
                        "Application process is not running. Launch or replay a fresh session."
                    )
                self.process.stdin.write(encoded)
                await self.process.stdin.drain()
                line = await self.process.stdout.readline()
                if not line:
                    await self.process.wait()
                    raise RuntimeError(
                        f"Application process exited with code {self.process.returncode}."
                    )
                response = json.loads(line)
                if not response.get("ok"):
                    raise ValueError(
                        response.get("error", "Unknown worker error")
                        + "\n"
                        + response.get("traceback", "")
                    )
                return response["result"]
        except (
            TimeoutError,
            asyncio.CancelledError,
            BrokenPipeError,
            ConnectionResetError,
            json.JSONDecodeError,
        ) as error:
            self.failure = (
                f"{type(error).__name__}: control request interrupted; "
                "session terminated to prevent late actions."
            )
            await asyncio.shield(self.terminate())
            if isinstance(error, asyncio.CancelledError):
                raise
            raise RuntimeError(f"{self.failure} Evidence: {self.directory}") from error

    async def request(self, method: str, **args: Any) -> dict:
        async with self.lock:
            if method == "export" and self.process and self.process.returncode is not None:
                return await asyncio.to_thread(self.recover_scenario)
            result = await self.exchange(
                {"method": method, "args": args}, 120 if method == "act" else 30
            )
            if result.get("fatal"):
                self.failure = result["error"]
                await self.terminate()
            return result

    def recover_scenario(self) -> dict:
        """Recover replay inputs from flushed action starts after forced termination."""
        journal = self.directory / "journal.jsonl"
        actions = []
        if journal.exists():
            for line in journal.read_text(encoding="utf-8").splitlines():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue  # A process can die during the final append.
                if record.get("kind") == "action_started":
                    actions.append(record["action"])
        path = self.directory / "scenario.json"
        path.write_text(
            json.dumps(
                {"version": 1, "launch": self.launch.model_dump(), "actions": actions}, indent=2
            ),
            encoding="utf-8",
        )
        return {
            "scenario": str(path),
            "journal": str(journal),
            "action_count": len(actions),
            "artifact_dir": str(self.directory),
            "recovered": True,
            "note": "Recovered from action starts. The last action may have completed only partly.",
        }

    async def terminate(self) -> None:
        if self.process:
            # Kill the dedicated group even if the app process has already exited;
            # it may have left descendants holding stdout or stderr open.
            if os.name == "posix":
                try:
                    os.killpg(self.process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            elif self.process.returncode is None:
                self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), 2)
            except TimeoutError:
                pass
            if os.name == "posix":
                try:
                    os.killpg(self.process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            elif self.process.returncode is None:
                self.process.kill()
            await self.process.wait()
            if self.log_task:
                try:
                    await asyncio.wait_for(self.log_task, 2)
                except TimeoutError:
                    self.log_task.cancel()

    async def stop(self) -> dict:
        async with self.lock:
            result = {"artifact_dir": str(self.directory)}
            try:
                if self.process and self.process.returncode is None:
                    result.update(await self.exchange({"method": "stop"}, 5))
                    try:
                        await asyncio.wait_for(self.process.wait(), 2)
                    except TimeoutError:
                        result["shutdown_note"] = "Application required forced cleanup."
            except Exception as error:
                result["shutdown_note"] = str(error)
            finally:
                await self.terminate()
            if "scenario" not in result:
                result.update(await asyncio.to_thread(self.recover_scenario))
            return {"session_id": self.id, "stopped": True, **result}


class SessionManager:
    def __init__(self, root: Path, maximum: int = 4) -> None:
        self.root = root.expanduser().resolve()
        self.maximum = maximum
        self.sessions: dict[str, Session] = {}
        self.lock = asyncio.Lock()

    @staticmethod
    def resolve_launch(launch: Launch) -> Launch:
        cwd = Path(launch.cwd or Path.cwd()).expanduser().resolve(strict=True)
        if not cwd.is_dir():
            raise ValueError("cwd must be a directory")
        target = launch.target
        if target.endswith(".py"):
            path = Path(target).expanduser()
            target = str((cwd / path).resolve(strict=True))
        return launch.model_copy(update={"cwd": str(cwd), "target": target})

    async def launch(self, launch: Launch) -> dict:
        launch = await asyncio.to_thread(self.resolve_launch, launch)
        async with self.lock:
            if len(self.sessions) >= self.maximum:
                raise ValueError(
                    f"Session limit ({self.maximum}) reached. "
                    "Stop a session before launching another."
                )
            session_id = uuid.uuid4().hex[:12]
            session = Session(session_id, launch, self.root / session_id)
            self.sessions[session_id] = session
        try:
            result = await session.start()
        except BaseException as error:
            await asyncio.shield(session.terminate())
            self.sessions.pop(session_id, None)
            if isinstance(error, asyncio.CancelledError):
                raise
            logs = "".join(session.log_chunks)[-6000:]
            raise ValueError(
                f"Launch failed: {error}\n{logs}\nEvidence: {session.directory}"
            ) from error
        return {**session.info(), **result}

    def get(self, session_id: str) -> Session:
        try:
            return self.sessions[session_id]
        except KeyError:
            raise ValueError(
                f"Unknown session {session_id!r}. Use list_sessions or launch_app."
            ) from None

    async def stop(self, session_id: str) -> dict:
        session = self.get(session_id)
        result = await session.stop()
        self.sessions.pop(session_id, None)
        return result

    async def close(self) -> None:
        await asyncio.gather(
            *(session.stop() for session in list(self.sessions.values())), return_exceptions=True
        )
        self.sessions.clear()
