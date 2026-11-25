---
name: load-workitem
description: Select a specified project work item as the focus of the conversation and load its saved documentation into context. Use when the user wants to load an item before working on it; ask which item if none is specified.
---

# Load Workitem

We are going to work on the specified work item. Establish it as this conversation's focus and read its saved documentation before proceeding.

1. Resolve the project from the request or workspace, normally its Git root. Read applicable project instructions, `.agent_context.md`, `.work-items/workflow.md`, and `WORK-ITEMS.md` when present. Follow the project's actual conventions.
2. Identify the item from the supplied name, slug, or folder path, checking the index and existing item records. If no item is specified, ask which work item the user wants to work on; show available names when helpful. If the supplied identifier matches multiple items or no existing item, ask one focused question rather than choosing arbitrarily or creating an item.
3. Read the selected item's `item.md` when present and all its saved documentation, including `idea.md`, `intent.md`, `evaluations.md`, `plan.md`, `progress.md`, and additional documents in its folder and subfolders. Read the contents into context, not just filenames or summaries. Follow relevant document references needed to understand the work. Split large documents into readable chunks so tool-output truncation does not silently omit content. If a document cannot be read, disclose the gap; do not claim it was loaded.
4. Use these records as the handoff: understand the intended outcome, settled decisions, constraints, approved quality rubric if any, unresolved questions, recorded progress, and next action. Distinguish superseded material from current decisions and flag material contradictions without inventing a resolution. When implementation is requested, verify the current code rather than treating saved progress as proof.
5. Briefly confirm the selected item, its current status, what documentation was loaded, and where the saved handoff says to continue. Proceed with any additional activity the user requested, following the project workflow. Loading alone does not start implementation or advance a stage.

For a registration-only item, use its index row and report that no documentation has been saved yet. Missing documents do not require backfilling or rubric definition. Loading is read-only: do not create documents, change status, update the index, or write a global current-item file merely to establish conversational context. If tracking conventions are missing, read the supplied item's existing documentation where possible and explain the missing context without automatically setting up a workflow.
