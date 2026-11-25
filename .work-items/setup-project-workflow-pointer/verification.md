# Setup-project verification

Executed `python3 /home/eriksalt/proj/skills/skills/engineering/setup-project/scripts/setup_project.py <project>` against `/tmp/setup-project-pointer-3jpvhvki/fresh` and `/tmp/setup-project-pointer-3jpvhvki/legacy-project-copy`. The legacy fixture copies this repository's old setup and adds prefix/suffix instructions around each managed block.

Fresh setup and migration succeeded. Repeat setup on both directories made no changes. Prefix and suffix bytes outside the markers are unchanged in all three legacy instruction files. Existing context, workflow, index, and all copied work-item files are byte-for-byte unchanged. Fresh context contains only its heading; the fresh workflow matches the revised template.

All five other engineering work-item skills already explicitly read `.work-items/workflow.md`: `define-rubric`, `setup-workitem`, `update-workitem`, `list-open-workitems`, and `load-workitem`. No changes to those skills were needed.

## Fresh setup

Helper output:

```text
Wrote .work-items/workflow.md
Wrote WORK-ITEMS.md
Wrote .agent_context.md
Wrote AGENTS.md
Wrote CLAUDE.md
Wrote GEMINI.md
```

### CLAUDE.md

```markdown
<!-- engineering-workflow:start -->
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow `.work-items/workflow.md`.
@.agent_context.md
<!-- engineering-workflow:end -->
```

### GEMINI.md

```markdown
<!-- engineering-workflow:start -->
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow `.work-items/workflow.md`.
@.agent_context.md
<!-- engineering-workflow:end -->
```

### AGENTS.md

```markdown
<!-- engineering-workflow:start -->
Before starting work, read and follow [.agent_context.md](.agent_context.md).
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow [.work-items/workflow.md](.work-items/workflow.md).
Resolve both paths relative to this file.
<!-- engineering-workflow:end -->
```

### .agent_context.md

```markdown
# Project context
```

## Old-block project copy migration

Helper output:

```text
Wrote AGENTS.md
Wrote CLAUDE.md
Wrote GEMINI.md
```

### CLAUDE.md

```markdown
# Existing project instructions

Keep this prefix.

<!-- engineering-workflow:start -->
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow `.work-items/workflow.md`.
@.agent_context.md
<!-- engineering-workflow:end -->

## Existing agent notes

Keep this suffix.
```

### GEMINI.md

```markdown
# Existing project instructions

Keep this prefix.

<!-- engineering-workflow:start -->
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow `.work-items/workflow.md`.
@.agent_context.md
<!-- engineering-workflow:end -->

## Existing agent notes

Keep this suffix.
```

### AGENTS.md

```markdown
# Existing project instructions

Keep this prefix.

<!-- engineering-workflow:start -->
Before starting work, read and follow [.agent_context.md](.agent_context.md).
Work items: before registering, saving, listing, resuming, or changing the status of a work item, or planning or implementing tracked work, read and follow [.work-items/workflow.md](.work-items/workflow.md).
Resolve both paths relative to this file.
<!-- engineering-workflow:end -->

## Existing agent notes

Keep this suffix.
```

### .agent_context.md

```markdown
# Project context

Add project-specific context and instructions here.
```
