# Define Rubric

`define-rubric` helps a user define what makes a particular idea or work item excellent. It produces independent qualitative dimensions with concise descriptions of what each values. Later assessment uses subjective judgments explained in ordinary language to guide refinement, especially during brainstorming.

## Agreed design

The assistant proposes a small set of dimensions based on the user's intended effect and priorities, explains what each values, and refines them through a focused conversation. The user controls which definitions are kept.

Check that dimensions describe distinct qualities: can an outcome be strong on one and weak on another? If not, clarify or merge them. Keep descriptions specific enough to guide useful judgment without defining performance levels.

Do not define numerical scores, rating scales, or anchor points. This includes verbal anchors and mandatory labels such as weak, adequate, and strong. Numerical precision and calibration added conceptual overhead without helping guide the brainstorming sessions this rubric is mainly intended to support.

Use a contrasting example only when it clarifies ambiguity or a meaningful tradeoff. There is no required calibration phase. Such examples clarify the dimensions rather than assess the current idea.

## Scope

The output contains dimension names and descriptions, plus useful context where needed. It has no scores, anchors, weights, required quality targets, or pass/fail thresholds. Actual assessment, selecting refinement priorities, and recommending improvements belong to later work.

Subjective judgment is expected. Explain assessments with reasons, relevant evidence, and uncertainty rather than manufacturing precision. Separate behavioral acceptance conditions from quality dimensions.

`workshop` uses these qualitative dimensions throughout refinement. Without an approved rubric, it derives its own working dimensions. Each round describes how the current idea fares, what changed, and the likely benefits and tradeoffs of the next proposal. Older numerical rubrics can supply dimension names and meanings, but their scales and anchors are not used for new assessments; historical records remain intact.

## Workflow integration

Rubric definition is optional and is not a workflow stage. Invoking it does not change an item's status. Once the user approves the complete rubric for saving, it is saved as the `Quality rubric` section of the item's `intent.md`, creating that document if needed. Saving preserves existing status; creating the first record for a registered item uses `captured`. Explicitly requested partial saves are marked as unapproved drafts.

A standalone discussion can define a rubric without creating a work item. Saving does not start assessment or later stages.

See [the skill](../skills/engineering/define-rubric/SKILL.md) for operating instructions and [the project workflow template](../skills/engineering/setup-project/assets/workflow.md) for record conventions.
