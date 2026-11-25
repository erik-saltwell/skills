#!/usr/bin/env python3
"""Install the workflow and agent references without replacing project content."""

import argparse
from pathlib import Path


START = "<!-- engineering-workflow:start -->"
END = "<!-- engineering-workflow:end -->"
IMPORT_BLOCK = f"""{START}
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow `.work-items/workflow.md`.
@.agent_context.md
{END}"""
CODEX_BLOCK = f"""{START}
Before starting work, read and follow [.agent_context.md](.agent_context.md).
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow [.work-items/workflow.md](.work-items/workflow.md).
Resolve both paths relative to this file.
{END}"""
CONTEXT = "# Project context\n"
INDEX = "# Work items\n\n| Name | Status | Folder |\n|---|---|---|\n"


def setup(project: Path) -> None:
    if not project.is_dir():
        raise ValueError(f"Project directory does not exist: {project}")
    template = Path(__file__).resolve().parents[1] / "assets" / "workflow.md"
    writes = {}
    defaults = {
        project / ".work-items" / "workflow.md": template.read_text(),
        project / "WORK-ITEMS.md": INDEX,
        project / ".agent_context.md": CONTEXT,
    }
    for path, content in defaults.items():
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Expected a regular project file: {path}")
        if not path.exists():
            writes[path] = content
    if (project / ".work-items").is_symlink():
        raise ValueError(".work-items must be a project directory, not a symlink")
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        block = CODEX_BLOCK if name == "AGENTS.md" else IMPORT_BLOCK
        path = project / name
        if path.is_symlink():
            # Let the agent inspect shared instructions instead of writing through them.
            raise ValueError(f"Inspect the existing instruction symlink before editing: {path}")
        old = path.read_text() if path.exists() else ""
        if START in old or END in old:
            if old.count(START) != 1 or old.count(END) != 1:
                raise ValueError(f"Ambiguous workflow markers in {path}")
            start, end = old.index(START), old.index(END)
            if end < start:
                raise ValueError(f"Reversed workflow markers in {path}")
            new = old[:start] + block + old[end + len(END):]
        else:
            separator = "" if not old else ("\n" if old.endswith("\n") else "\n\n")
            new = old + separator + block + "\n"
        if new != old:
            writes[path] = new
    # Validate all inputs before writing any files.
    for path, content in writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Wrote {path.relative_to(project)}")
    if not writes:
        print("Workflow already set up; no changes needed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Existing target project directory")
    args = parser.parse_args()
    try:
        setup(args.project.resolve())
    except (OSError, ValueError) as error:
        parser.exit(1, f"Setup stopped: {error}\n")


if __name__ == "__main__":
    main()
