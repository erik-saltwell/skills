---
name: setup-workitem
description: Register a project work item by creating its folder and adding it to WORK-ITEMS.md. Use when the user wants to set up, register, or capture a new item for later. Creates no item.md, intent, or other item documents.
---

# Setup Workitem

Create only the work-item folder and its master-list entry. Registration does not begin rubric definition, ideation, or implementation.

1. Resolve the project from the request or workspace, normally its Git root. Read applicable instructions, `.work-items/workflow.md`, and `WORK-ITEMS.md`. If the workflow is missing, use `setup-project` within this request. If unavailable, explain the missing dependency rather than inventing conventions.
2. Infer a descriptive name from the request or conversation. Ask one focused question if the item cannot be identified. Check the index and existing item folders and records for a match; reuse an existing item without resetting its status. Resolve genuinely different items with a meaningful slug suffix.
3. Create `.work-items/<slug>/` and add one `registered` row using the workflow's name, status, and repo-relative folder-link conventions. Preserve every other row and unrelated index content. Re-read before writing when concurrent edits are possible.
4. Verify the folder exists and the index contains exactly one matching entry. Report the folder and registration status briefly. Repair a partial registration where possible and disclose any remaining inconsistency.

Do not create `item.md`, `intent.md`, placeholders, or any other files inside the folder. Do not start an interview or define or score quality dimensions. Rubric definition is optional and happens only if the user invokes a rubric skill. Git does not preserve empty directories; the registered index entry reserves the path, and later work recreates the folder if needed.

Use project conventions when customized. If they conflict with folder-only registration, explain the conflict rather than silently generating documents. Registration stores the item's name and location, not a full conversation; a request to save substantive content belongs to `update-workitem`.
