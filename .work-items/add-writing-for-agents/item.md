---
name: "Add writing-for-agents"
status: complete
---

# Add writing-for-agents

Provide retro's missing `writing-for-agents` dependency by importing Matt Pocock's three upstream skill files unchanged into `skills/development/writing-for-agents/` and installing it for Claude Code using the repository's symlink installer.

Preserve upstream MIT attribution, record the source commit in the skill's [source note](../../skills/development/writing-for-agents/SOURCE.md), and verify file equality, the frontmatter name, reference resolution, and installation. Leave retro unchanged; do not commit or push.

## Completed

Imported `SKILL.md`, `SKILL-MECHANICS.md`, and `agents/openai.yaml` unchanged from the default branch (`main`) of https://github.com/mattpocock/skills at commit `49dd158d1076134a641b33efb035946536778336`. Included the unchanged upstream root MIT `LICENSE` with Matt Pocock's copyright notice and a separate `SOURCE.md` for provenance. Kept the skill in `development` beside retro; retro and wait-what have this folder layout but no existing license or attribution note.

Installed with `./scripts/install.sh --agent claude --category development`. The installer created `/home/eriksalt/.claude/skills/writing-for-agents` as a symlink to this repository's skill folder.

## Verification

- Re-fetched all three requested files and `LICENSE` at the pinned commit: local bytes and Git blob hashes match upstream.
- Frontmatter `name` is exactly `writing-for-agents`.
- Both Markdown references to `SKILL-MECHANICS.md` resolve in the source and installed folders.
- Installed symlink resolves to the intended folder; installed `SKILL.md` and `agents/openai.yaml` exist.
- `git diff HEAD -- skills/development/retro skills/development/wait-what` is empty.
- No Claude Code runtime invocation was performed; installation was verified on disk.

No remaining implementation work. Changes are left uncommitted for review; no push was performed.
