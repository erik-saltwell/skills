# Textual MCP implementation

Implement the server requested on 2026-09-15 against [rubric version 1](rubric.md). There was no prior implementation or saved design. Repository instructions and the existing work-item documents were inspected. Keep the standalone Python package in `servers/textual-mcp/` alongside the repository's skills.

## Design

Use the official MCP Python SDK over stdio. Each application runs in its own Python subprocess, driven through Textual's headless `App.run_test` / Pilot API. This isolates application imports, output, failures, and working directories. Accept a source file or importable module plus an App factory and JSON constructor arguments. The same Python environment must contain the server and app dependencies.

Expose session lifecycle, bounded widget/state/source inspection, diagnostics, batched actions with condition waits, faithful SVG plus PNG captures, and export/replay of scenarios. Record launch conditions, ordered actions, results, and screenshot metadata. Headless rendering does not establish pixel equivalence to every terminal emulator; preserve original SVG and document rasterization/font limits. Loading an application executes trusted local Python code.

## Steps and verification

- [x] Package and isolated session lifecycle, including timeout/crash/cleanup behavior. Supports agent usability and repeatability. Verified installation and real stdio MCP initialization/tool discovery.
- [x] Widget diagnostics and interactions: keyboard, paste, mouse, scroll, focus, resize, conditions, and batches with partial failure evidence. Supports diagnostic insight, coverage, repeatability, and usability. Exercised the demo and temporary fixture apps through the MCP client.
- [x] SVG/PNG screenshots with framing and evidence, action journal and fresh-session scenario replay. Supports visual fidelity, documentation evidence, and repeatability. Visually inspected generated images and compared replay outcomes.
- [x] Usage documentation, demo, quality assessment, and completion tracking. Build/lint and behavior-level lifecycle, isolation, failures, captures, and replay passed. No unit tests or automated test suite were added, per project workflow.

## Resolved choices and limits

Verified Textual 8.2.8, Rich 15.0.0, and MCP SDK 1.30.0 APIs against installed source and official documentation. Dependencies are locked. The parent enforces hard deadlines and reaps the app process group; action starts remain recoverable if a worker dies. CairoSVG PNG rendering explicitly positions glyphs and requests DejaVu Sans Mono; original SVGs are preserved. The server clears inherited NO_COLOR for its true-color app environment.

No intended real-world application was supplied; verification used the included demo and temporary fixture apps. External data, network services, and application randomness cannot be made deterministic by the server alone. See [progress.md](progress.md) for actual checks and [evaluations.md](evaluations.md) for the rubric assessment and remaining limits.
