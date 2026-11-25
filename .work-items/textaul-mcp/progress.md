# Textual MCP implementation outcome

Completed 2026-09-15. The user requested reading the existing quality rubric and implementing the server. The standalone package is [servers/textual-mcp](../../servers/textual-mcp/); [its README](../../servers/textual-mcp/README.md) contains installation, MCP client configuration, action semantics, architecture, and limitations. No client configuration was changed and no commit or publication was performed.

## Delivered

- Nine stdio MCP tools: launch, list sessions, inspect, perform actions, capture, diagnostics, export, replay, and stop.
- Isolated App/Pilot subprocesses, per-session serialization, bounded requests/output, startup and action deadlines, cancellation cleanup, and crash recovery from flushed action-start records.
- Keyboard input, paste, focus, clicks/modifiers, pointer sequences, wheel events, resizing, condition waits, app-specific Textual actions, and batched captures.
- Widget regions/clipping, text, reactive attributes, own and inherited disabled state, computed CSS, class/decorated-handler source locations, bindings, workers, dispatch observations, app output, and control/application tracebacks.
- Original SVGs, framed SVG/PNG files, labels, cell geometry, state metadata, hashes, an action journal, replayable scenarios, and a Markdown documentation evidence sheet.
- An interactive demo, package metadata/entry point, dependency lockfile, and a locally installed `.venv` using Python 3.12.3. From `servers/textual-mcp`, run `uv sync --locked`; use `.venv/bin/textual-mcp` as the client command.

The implementation follows [rubric version 1](rubric.md) without changing its dimensions or anchors. [Evaluations](evaluations.md) distinguish evidence-based engineering judgments from unassessed areas.

## Verification performed

Linux; Python 3.14.3 in the initial development environment and Python 3.12.3 in the project and wheel-install environments. Textual 8.2.8, Rich 15.0.0, MCP SDK 1.30.0, CairoSVG 2.9.1, Ruff 0.16.7.

| Check | Actual outcome |
|---|---|
| Real MCP `ClientSession` over stdio | Initialized and discovered all nine tools; exercised lifecycle, inspection, actions, captures, diagnostics, export, and replay |
| Demo workflow | Entered a name, clicked Greet, waited for the result, captured full and cropped screens, opened/closed a modal, and resized to 80×24 |
| Replay comparison | All 13 actions reproduced in a fresh subprocess; resulting greeting matched; all four corresponding SVG capture hashes matched exactly |
| Visual inspection | Opened full-screen, cropped-result, and modal PNGs; verified readable text, colors, border geometry, and framing after fixing Cairo font fallback |
| Widget diagnostics | Verified geometry, computed styles, class/source references, decorated handler references, reactive values, and password-value redaction |
| Interaction coverage | Keyboard editing and exact attribute waits, custom-widget pointer down/move/up, wheel delivery, and actual demo-container scrolling passed |
| Error behavior | Invalid schema bounds, ambiguous selectors, hidden capture targets, condition timeout, and partial-batch failure behaved as documented; later batch actions were not executed |
| App failures and isolation | Constructor failure, direct action traceback, fatal event-handler traceback, and `os._exit(7)` checked; a second session remained usable; abrupt exit recovered its scenario from the journal |
| Output isolation | Both Python print output and low-level fd 1 writes during app import were kept out of MCP stdout and available in diagnostics |
| Lifecycle | Session limit enforced; normal app quit, stop, and client-context cleanup exercised |
| Cancellation | Cancelled a queued 10-second pause; app process was reaped, subsequent paste never started, and scenario recovery retained the attempted action |
| Hard deadline | Blocked an app event loop with a synchronous sleep; shortened the direct supervisor deadline to 0.3 seconds for verification; process was killed and reaped |
| Built package | Built sdist and wheel; installed wheel in a clean Python 3.12 environment and exercised stdio tools, form interaction, capture, scrolling, replay, and cleanup |
| Final scoped fix | Checked inherited disabled state and enabled-condition timeout directly on Python 3.12; rebuilt artifacts after that two-line behavior correction |
| Static checks | Ruff check and format check passed; `git diff --check` passed |

Actual packaging/check commands included:

```sh
uv sync --project servers/textual-mcp --python /usr/bin/python3
uv build servers/textual-mcp --out-dir /tmp/textual-mcp-dist
/tmp/textual-mcp-dev/bin/ruff check servers/textual-mcp
/tmp/textual-mcp-dev/bin/ruff format --check servers/textual-mcp
git diff --check
```

Behavior checks were direct Python execution against the official MCP client and temporary fixture apps; no unit-test tooling or automated suite was added. Temporary evidence lives under `/tmp/textual-mcp-check2/`, `/tmp/textual-mcp-failure-check/`, `/tmp/textual-mcp-supervision/`, and `/tmp/textual-mcp-wheel-evidence/` while this machine retains it. These temporary files are not needed to install or run the server. The included demo and README describe how to reproduce the main workflow.

## Remaining limits

- PNG uses local DejaVu Sans Mono/fallback fonts. A header symbol had a missing-glyph box; complex Unicode shaping and emulator-specific cursor/font behavior remain unverified. Original SVG output is retained for every capture.
- Verification covers the demo and purpose-built fixtures, not a user-supplied production app or an exhaustive terminal/widget matrix. Linux/Python 3.12 and 3.14 were exercised; Python 3.11, macOS, and Windows were not.
- Dispatch observations are not a complete handler-execution or causal trace. Event history and logs are bounded; diagnostic state is intentionally scoped.
- Replay does not reset external data, freeze time, seed every library, or snapshot the whole source tree. Application factories can provide fixtures. Source file/hash and dependency versions help explain differences.
- Textual private compatibility seams and Rich's SVG geometry are documented; upgrades need verification. Dependency ranges and the lockfile constrain the current implementation.

No required implementation step remains. Future work should start with a real target app and its observed gaps rather than assuming the rubric's highest anchors have been achieved.
