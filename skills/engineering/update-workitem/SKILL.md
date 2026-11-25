---
name: update-workitem
description: Save, list, resume, or update project work items using .work-items/workflow.md and WORK-ITEMS.md. Use when the user asks to save a rubric, qualitative evaluation, idea, intent, plan, or progress, change status, or inspect tracked work. Route registration-only requests to setup-workitem; separate skills handle rubric definition and design discussion.
---

# Update Workitem

Turn the user's conversation into durable work-item documents and keep the master list accurate. Choose paths and Markdown structure from the project workflow; the user does not need to specify them. This skill handles tracking and handoffs, while existing skills or the conversation handle ideation, intent, planning, and implementation.

## Load the project conventions

Resolve the project from the request or workspace, normally its Git root. Read applicable project instructions and `.work-items/workflow.md`, then `WORK-ITEMS.md` and the selected item's existing `item.md` and relevant artifacts. The local workflow is the source of truth for canonical statuses, artifact content, transitions, and verification. Do not carry assumptions from another project's customized workflow into this one.

If the workflow is missing and the user requests a mutation, use the installed `setup-project` skill to establish it as part of that request, preserving existing files. No additional setup approval is needed. If that skill is unavailable, explain the missing dependency without inventing a competing convention. A list-only request should report that tracking is not set up rather than creating files.

## Interpret the requested action

Invocation syntax is illustrative; accept equivalent natural language and the host's skill invocation syntax.

| Request | Action |
|---|---|
| `capture an item for CSV export` | Use `setup-workitem` to register its folder and index row only; do not create item documents |
| `save rubric` | Save an approved qualitative rubric as the `Quality rubric` section of `intent.md`, creating it if needed; do not invent dimensions or add scores, rating scales, or anchors |
| `save evaluation` | Save supplied per-dimension qualitative judgments and evidence in `evaluations.md`, identifying the evaluated version and rubric used |
| `save idea` | Synthesize the discussion into the item's `idea.md` |
| `save intent` | Save the agreed intent and unresolved details in `intent.md` |
| `save plan` | Save phased implementation steps and verification in `plan.md` |
| `save progress` | Update the resume note, implementation checkboxes, and `progress.md` as needed |
| `start planning CSV export` | Set the identified item's current activity from the explicit request and load its handoff |
| `resume CSV export` | Load the saved context and continue its current activity without advancing status |
| `complete CSV export` | Record completion and its known outcome and verification limitations |
| `show open work` / `show all work` | Present the corresponding items without starting or modifying them |
| `refresh the work-items table` | Reconcile item records while retaining authoritative registration-only rows |

Infer the item and artifact from the current conversation where unambiguous. Check for an existing matching item before creating one. Choose a descriptive slug automatically; never overwrite a different item on a naming collision. If multiple items or artifact types remain plausible, ask one concise question to identify the target. A bare invocation with useful conversation context normally means save the current work; with no context, show open items and ask what to update.

Registration-only requests end after folder/index setup and bypass artifact saving below. If `setup-workitem` is unavailable, follow the local workflow's folder-only registration rules directly. For a registered item without `item.md`, read its name and status from the index. Resuming registration reports that the item is registered and ready for whichever stage the user chooses; it does not create documents or start work. A rubric is optional and never a stage; use an approved rubric in `intent.md` when available, and never prompt for or start rubric definition because one is missing.

## Save and synchronize

1. Read before editing. Preserve existing decisions, unrelated document content, and other items' records. Resolve any conflict between saved material and the conversation using explicit user decisions, not the latest agent suggestion.
2. Use the workflow's artifact guidance. If `document-this` is available, use it for synthesis with the destination already resolved; otherwise synthesize directly. Preserve rationale, constraints, decision status, open questions, and enough context to resume without the chat. Do not create empty prerequisite documents or turn a save request into another design exercise.
3. Create or update `item.md` and the requested artifact. Create the first record only on a substantive save or explicit active-stage start, never registration or listing. Saving alone preserves an existing active status; first-time saves and saves from `registered` reflect the activity actually underway, while substantive capture-for-later uses `captured`. Reconcile any explicit stage start that was missed. Do not advance to the next stage merely because a document was saved. Preserve any `Quality rubric` section when saving intent, and link evaluations to it; changes to quality dimensions or their descriptions require user direction or agreement. Save reported qualitative judgments and evidence without manufacturing an assessment. Preserve historical numerical evaluations as historical records; do not turn them into new qualitative judgments without an assessment.
4. Synchronize the root index using the workflow's rules. Include all items, including completed ones, exactly once. Folder link labels and targets must both be repo-relative folder paths. `item.md` is authoritative where present; registration-only rows remain authoritative until a record exists and must survive rebuilding. Preserve inconsistent records or unmatched rows for resolution rather than silently deleting their information.
5. Check the affected frontmatter, canonical status, saved document and index agreement, and link destinations. Report the saved artifact and current status briefly. If a partial write failed, state what succeeded and repair the index from the saved records where possible.

Stage starts, resumption, and completion follow the same record/index consistency rules. Resuming should use only the relevant saved documents, then continue the requested activity; listing should stay read-only. Never infer implementation, deployment, or a new stage from a documentation request. Do not create or expand unit tests when planning or implementing under this workflow.
