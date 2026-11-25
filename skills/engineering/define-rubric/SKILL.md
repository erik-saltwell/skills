---
name: define-rubric
description: Collaboratively define an optional qualitative quality rubric for an idea or work item by refining distinct dimensions and describing what each values, without scores or anchors. Use when the user wants to define or revise how quality will be judged. An approved rubric is saved in the item's intent.md. Actual assessment and refinement recommendations belong to later work.
---

# Define Rubric

Help the user define the qualities that matter for this particular idea. Produce independent qualitative dimensions, each with a short description of the quality it values. Assessments will be subjective judgments explained in ordinary language; do not define numerical scores, rating scales, or anchor points. The user controls which definitions are kept. Do not evaluate the current idea, recommend refinements to it, or produce an aggregate score, weights, required targets, or pass/fail thresholds.

## Start from context

Use the supplied idea and discussion. Read relevant available material selectively before asking questions it can answer. If the subject is unclear, ask what the user wants to define a rubric for.

For an identified project work item, read applicable instructions, `.work-items/workflow.md`, `WORK-ITEMS.md`, and existing item documents, including any rubric already in `intent.md`. Rubric definition is optional and is not a workflow stage: invocation does not change the item's status. Preserve the item's folder, unrelated content, and prior decisions. A registration-only row is valid; create no records until an approved rubric or explicitly requested draft is saved. If project conventions are missing, use `setup-project` when available within the tracked-work request. Do not overwrite customized conventions.

For standalone rubric design, keep the discussion conversational until saving is requested. Do not create a work item merely because a workspace is available. If the user explicitly requests a new tracked item, use `setup-workitem` for registration first, then begin this skill's activity.

## Establish dimensions first

Propose a small, manageable set of dimensions grounded in the user's intended effect and priorities. Explain what each rewards. Avoid a generic checklist imposed on every idea. Focus each turn on the most consequential refinement and ask one question at a time, giving a recommendation and a concise reason.

Let the user add, remove, merge, or reshape dimensions and their descriptions. Carry accepted changes forward; exploration or silence does not establish agreement. Keep uncertain definitions tentative.

Check for overlap using a concrete distinction: can an outcome be strong on one dimension and weak on another? If not, propose clarifying or merging them. Distinctness matters more than reaching a prescribed dimension count.

Do not require every dimension to imply an actionable repair, prescribe an improvement strategy, or start refining the underlying idea. Those activities belong to future work.

## Clarify only where useful

Keep descriptions concise and specific to the subject. They should explain what matters, without prescribing levels of performance or defining what counts as weak, adequate, or strong. Do not replace numerical anchors with verbal anchors or require fixed rating labels.

Use a contrasting example only when it would clarify an ambiguous dimension or meaningful tradeoff. Ask whether the dimension captures what the user cares about, then revise its description if needed. Do not require a separate calibration exercise for every rubric. These examples clarify the dimensions; they are not an assessment of the current idea or a choice of its next refinement priority.

## Save a usable rubric

When the rubric seems settled, present it in full and ask the user whether to approve it and save it into `intent.md`. General agreement with individual definitions is not approval of the whole rubric. When the user approves it, save it for an identified work item as a `Quality rubric` section of the item's `intent.md`, creating `intent.md` if it does not exist. Use `update-workitem` when available or follow the local workflow directly. A newly created `intent.md` contains only a brief statement of the intended outcome and the rubric; do not invent scope or behavior to fill it out. Preserve all other intent content when adding or replacing the section. Saving preserves an existing status; if it creates the first record for a registered item, use `captured`. It does not start fleshing-out, ideation, planning, or implementation. Do not save a rubric the user has not approved; a request to pause and save records the partial draft in the same section, clearly marked as an unapproved draft with explicit open decisions, instead of inventing agreement.

The rubric section should stand alone and contain:

- The subject and intended effect being judged.
- Each dimension's name and a concise description of what it values.
- Useful context or tradeoffs when they clarify interpretation, without performance levels or anchors.
- Any unresolved definitions, clearly distinguished from settled content.

Keep dimensions independently assessable in words. Do not add scores, rating scales, anchors, weights, thresholds, targets, actual assessments, or refinement recommendations. Save future evaluations separately from the rubric definition.

When revising an existing rubric, preserve the reason for consequential changes and enough information to distinguish prior definitions used by existing evaluations. Preserve historical evaluations and distinguish assessments made against earlier dimension definitions. When replacing an older numerical rubric, retain useful dimension meanings without carrying forward its scales or anchors, and leave historical scores as historical records.

Verify the saved intent, item status, links, and index agree. Briefly report the saved path and any unresolved definitions, then stop. In a standalone conversation, present the agreed rubric inline unless a file destination is established. Do not automatically launch assessment or further work.
