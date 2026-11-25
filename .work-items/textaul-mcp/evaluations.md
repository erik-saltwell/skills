# Textual MCP quality assessment

## 2026-09-15 — implementation 0.1.0

Evaluated against [rubric version 1](rubric.md), accepted 2026-09-15. These are provisional engineering judgments based on [the recorded verification](progress.md), not a numerical benchmark or user acceptance. No aggregate, weights, or required threshold is applied.

Work version: `servers/textual-mcp/`, package 0.1.0. Implementation fingerprint: `958aac256f489bbf51db1d73e4cd4aba7cddcc78c456457c3e9497283c03b593`. This is SHA-256 over sorted `pyproject.toml`, `uv.lock`, and `src/**/*.py` paths relative to the package, with each path, NUL byte, file bytes, and NUL byte concatenated in order. It identifies the working implementation without implying a commit was created.

| Dimension | Score / 10 | Evidence and limit |
|---|---:|---|
| Diagnostic insight | 7 | Widget/reactive state, computed CSS, class and decorated-handler source locations, output, app/control tracebacks, and action-linked dispatch events narrowed observed failures. There is no full handler execution trace or broad difficult-failure validation. |
| Visual fidelity | 7 | Original Textual SVG preserved; size, crop geometry, full-screen and modal states verified; PNG font/grid correction visibly improved borders and spacing. Some glyph fallback remains visible, and no independent real-terminal comparison or Unicode matrix was performed. |
| Interaction coverage | 8 | Form input, keyboard editing, focus, clicks, modal navigation, pointer down/move/up, custom wheel handling, actual scrolling, resize, waits, and app-specific action calls exercised. Coverage across a real application's custom controls remains unassessed. |
| Repeatability | 8 | Fresh subprocess replay reproduced a 13-action workflow with four identical SVG hashes. Journals associate actions with before/after state and event ranges; interrupted actions are recoverable. External data, clocks, and additional random generators remain app responsibilities. |
| Documentation evidence | 8 | Readable full and cropped screenshots have labels, terminal dimensions, focus/screen state, hashes, action numbers, a capture manifest, and a Markdown evidence sheet. No end-user guide or long production workflow was reviewed. |
| Agent usability | 8 | Nine discoverable tools, discriminated action schemas, bounded/paginated inspection, inline PNG output, partial-failure records, diagnostics cursors, and fresh-session replay worked through a real MCP client. No independent agent study was performed; large detailed batches can still produce substantial output. |

### Unassessed areas

Production target applications; broad Unicode/emoji rendering; exact terminal-emulator appearance; cross-platform behavior; many app worker/concurrency patterns; extended stress or endurance workloads; and independent operator/editor experience. These gaps are not assigned zero scores.

### Refinement priorities

Validate against the user's actual app first. The strongest current opportunities are a browser/font-controlled rasterization path for difficult glyphs and richer app-specific diagnostic observations for complex failures. Those are future improvements, not claims that the accepted rubric or requested implementation scope has changed.
