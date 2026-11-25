# Textual MCP

A local MCP server for driving Python Textual apps: inspect runtime state and source
locations, exercise workflows, capture screens, and replay recorded scenarios.

## Install and run

Requires Python 3.11+ and a system Cairo library for PNG rendering (on Debian/Ubuntu,
`sudo apt install libcairo2 fonts-dejavu-core`; on macOS, `brew install cairo`).
Install DejaVu Sans Mono for consistent PNG glyphs. Linux is the verified platform.

From this directory:

```bash
uv sync --locked
.venv/bin/textual-mcp --artifact-dir ./captures
```

The lockfile pins the verified dependencies. Alternatively, install the package with
`pip install .` in an existing environment. The command speaks MCP over stdio and waits
for a client. To try the example app in
a terminal, run `.venv/bin/python -m textual_mcp.demo`.

Use your MCP client's server configuration, with absolute paths:

```json
{
  "mcpServers": {
    "textual": {
      "command": "/absolute/path/to/textual-mcp/.venv/bin/textual-mcp",
      "args": ["--artifact-dir", "/absolute/path/to/captures"]
    }
  }
}
```

Install the target app and its dependencies into this **same Python environment**.
Each app runs in a separate process using the server's Python interpreter. Importing
and running apps executes trusted local Python with your permissions; this is process
isolation, not a sandbox. App output is diverted away from the MCP transport, including
low-level writes to stdout. No client configuration is changed by installation.

## A complete workflow

Call `launch_app`:

```json
{"launch":{"target":"textual_mcp.demo","factory":"DemoApp","width":100,"height":30}}
```

Use the returned `session_id` in `inspect_app`. For an application you own, `target`
can instead be `/project/app.py` or `my_package.app`; `factory` is the name of an App
class, synchronous factory, or existing App instance. File imports do not execute the
`if __name__ == "__main__"` block. Use an importable module for package-relative imports.
Set `cwd` for relative resource paths and `kwargs` for constructor arguments.

Call `perform_actions`:

```json
{
  "session_id": "<returned ID>",
  "actions": [
    {"kind":"focus","selector":"#name"},
    {"kind":"paste","text":"Ada"},
    {"kind":"click","selector":"#greet","x":3,"y":1},
    {"kind":"wait","selector":"#result","condition":"text","value":"Hello, Ada."},
    {"kind":"capture","label":"Your greeting appears below the form"}
  ]
}
```

Call `capture_screen` for an inline PNG image. To frame just the result, supply
`selector: "#result"`, `padding: 1`, and a meaningful `label`. Call `export_scenario`
to get paths to the scenario JSON, journal, capture manifest, and Markdown evidence
sheet. Pass the scenario path to `replay_scenario` to reproduce the workflow in a
new session. Finish with `stop_session` for each session.

## Tools

| Tool | Purpose |
|---|---|
| `launch_app` | Import, construct, and run an app at a known terminal size |
| `list_sessions` | Find session IDs, process status, and evidence directories |
| `inspect_app` | Paginated widget tree, text, geometry, state, and focus |
| `perform_actions` | Validated ordered actions, stopping on the first failure |
| `capture_screen` | Inline PNG plus SVG and metadata files |
| `get_diagnostics` | Exceptions, dispatch events, output, and environment |
| `export_scenario` | Save replay inputs and documentation evidence |
| `replay_scenario` | Run saved actions in a fresh session |
| `stop_session` | Export evidence and clean up the app process |

Use `inspect_app(details=true, selector="#widget")` for computed CSS, reactive
attributes, source file/line references, handler locations, active bindings, and workers.
The default view is smaller; `offset` and `limit` paginate widget results. Use unique
CSS IDs in your app to make interaction targets easy to describe.

### Actions

| `kind` | Fields and behavior |
|---|---|
| `press` | `keys`: Textual Pilot key names; e.g. `["tab", "enter"]`, `["ctrl+a", "backspace"]` |
| `paste` | `text`: a literal Paste event delivered through the app to focus |
| `click` | `selector`, cell offsets `x`/`y`, `button` (1 left, 2 middle, 3 right), `times` (1–3), modifiers |
| `hover` | `selector`, `x`/`y` |
| `mouse_down`, `mouse_move`, `mouse_up` | Cell offsets and modifiers, allowing custom pointer sequences and drags |
| `scroll` | `selector`, `x`/`y`, `direction` (up/down/left/right), `amount` |
| `focus` | `selector`: focus a widget; fail if it does not accept focus |
| `resize` | `width`/`height` in terminal cells |
| `pause` | `seconds` (0–10); a fixed delay |
| `wait` | `selector`, `condition`, optional `value`/`attribute`, `timeout` (up to 30s) |
| `action` | `action`: a Textual action expression, such as `app.help` |
| `capture` | `label`, optional crop `selector` and cell `padding` |

Mouse offsets are relative to the target widget, or to the screen if no selector is
given. `(0,0)` is the top-left cell, which may be a border. Targets must already be
visible: scroll first. A missed target produces an error even if another widget received
the event; this is recorded as a potentially state-changing failed action.

Wait conditions: `exists`, `absent`, `visible`, `focused`, `enabled`, `text` (substring of
bounded rendered content), and `attribute` (exact equality with a public attribute).
Use an attribute wait for content beyond the first 30 widget lines. A condition wait
is preferable to guessing a delay. Regular actions wait for Textual's message queue;
this does not imply network calls, animations, or background workers have finished.
Programmatic focus and Textual actions are integration controls, not physical input.

For application-specific workflows, add an `action_*` method and invoke it through
`action`, or expose a public reactive attribute for inspection and condition waits.

## Evidence and fidelity

Each session gets a unique directory containing:

- `journal.jsonl`: launch environment, action-start records, results/errors, before/after
  screen and focus state, and event ranges. Starts are flushed before actions execute.
- `stderr.log`: combined application stdout/stderr, bounded to 2 MiB.
- `captures/`: original full SVG, framed SVG, PNG, hashes, and JSON metadata for each capture.
- On export/stop: `scenario.json`, `diagnostics.json`, `captures.json`, and `evidence.md`.

SVG comes directly from Textual's compositor through `App.export_screenshot`, preserving
rendered layout, styling, wrapping, overlays, and clipping at the recorded terminal size.
The original full SVG is kept even for cropped captures. Crops use the widget's clipped
screen region; overlapping content remains visible as rendered. Captures do not expose
content hidden behind another screen or outside the viewport.

PNG is rendered by CairoSVG with explicit glyph positions because Cairo ignores SVG
`textLength`. The original SVG uses Rich's Fira Code/monospace font declarations; Cairo
requests DejaVu Sans Mono from the locally available fonts. Emoji, complex shaping,
combining sequences, terminal
fonts, cursor blinking, and emulator-specific effects can differ. Inspect captures for
those cases before using them in published documentation. This is faithful Textual
headless rendering, not a screenshot of a specific terminal emulator.

The child receives `TERM=xterm-256color`, `COLORTERM=truecolor`, and no `NO_COLOR`, so
the MCP host's redirected-output settings do not silently remove app colors.
Tooltips and notifications are enabled by default and can be disabled in `launch`.

## Repeatability and failures

Replay records source target, factory, constructor arguments, cwd, terminal dimensions,
and seeds Python's `random` and hash behavior before app import. It creates a fresh app;
it does not roll back files/databases, pin dependencies, seed NumPy, freeze clocks, or
control remote services. Use fixtures in your App factory for those dependencies.
The journal records package versions, app source location, and the App class's source
file hash for comparing runs. The hash does not cover every imported module or CSS file.

Scenarios include **attempted** actions, including failed ones. Replay stops at the first
failure and returns its session ID. Inspect the journal to distinguish an app failure
from an invalid control request. Editing a scenario is supported: keep `version: 1`,
the `launch` object, and validated `actions`. Source edits are loaded on fresh launch.

Successful calls and action-batch failures expose structured results, with MCP `isError`
set for failures. Schema validation and launch errors use the SDK's standard error text.
Schemas reject unknown fields and invalid bounds before execution. Batches have at
most 100 actions and a 120s hard deadline; each action has a 35s deadline. Startup and
inspection have 30s deadlines. An interrupted transport request terminates that app
session to prevent later actions from running unexpectedly. Artifacts already written
survive; `export_scenario` can recover attempted actions from the journal after an abrupt
exit or forced termination. Control requests are limited to 4 MiB. At most 2,000 actions
are recorded per session. Four concurrent sessions are
allowed by default (`--max-sessions` changes this). Stop failed sessions to free slots.

Diagnostics include the most recent control-action traceback separately from a fatal
application exception. They retain the last 1,000 non-housekeeping message dispatches, with a cursor
and explicit count of events lost before the requested cursor. Dispatch observations
do not establish which decorated handler ran or prove causation. Timers/rendering
housekeeping are omitted. Password input values are redacted from widget inspection;
other runtime data, pasted inputs, app logs, and screenshots may contain app data.

Compatibility is bounded to Textual 8.2.8–8.x, Rich 15.x, and MCP Python SDK 1.30–1.x.
Private seams are limited to exception state, reactive metadata, message receiver/sender
context, and Pilot's mouse-event helper for wheel and drag motion. Check those seams
when upgrading Textual. On POSIX, cleanup reaps the dedicated app process group;
on Windows, only the direct app process is terminated.

## Architecture and verification

`server.py` defines MCP tools; `sessions.py` supervises subprocesses and transport;
`worker.py` owns each App/Pilot context and action journal; `inspection.py` produces
bounded observations; `capture.py` writes visual evidence; `models.py` shares validated
schemas. `demo.py` is an interactive example with a form, modal, switch, and scrolling.

Verification uses real MCP stdio sessions, the demo, and temporary failure apps, plus
build/lint checks. The repository workflow excludes adding a unit-test suite. See the
work item's progress and evaluation documents for the actual checks and limitations.

API references: [Textual testing/Pilot](https://textual.textualize.io/guide/testing/),
[Pilot API](https://textual.textualize.io/api/pilot/), and the
[official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).
