---
name: list-open-workitems
description: List all open work items in a project, including registration-only items, with their names, current statuses, and folder links. Use when the user asks to list or show open work items.
---

# List Open Workitems

Show the project's open work items without starting work or modifying tracking records.

1. Resolve the project from the request or workspace, normally its Git root. Read applicable project instructions, `.agent_context.md`, `.work-items/workflow.md`, and `WORK-ITEMS.md` when present. Use the local workflow's conventions.
2. Read existing `.work-items/*/item.md` records as well as the index. An item's record is authoritative for its name and current status when present; a registration-only index row is authoritative until a record exists. Include records missing from the index and retain registration-only items even when their empty folders are absent after checkout. Deduplicate by item folder.
3. List every item whose status is not `complete`, including `registered` items. Present a concise Markdown table with `Name`, `Status`, and `Folder` columns, sorted by folder slug, with clickable folder links. If there are no open items, say so plainly.
4. Briefly report any index/record disagreement, invalid metadata, unreadable record, or non-registered index row missing its record. Preserve uncertain items in the report with their recorded information and explain the uncertainty rather than silently omitting them or inventing a status. If an unreadable source prevents a complete listing, disclose that limitation.

If tracking is not set up, report that fact without creating a workflow. If records exist without an index, list the available open records and mention the missing index. Listing does not load all stage documents, select a current item, resume activity, change status, or repair files. Do not prompt the user to choose an item unless their request also asks to begin work and the target is ambiguous.
