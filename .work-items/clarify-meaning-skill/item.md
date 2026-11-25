---
name: "Clarify-meaning skill: identify ambiguous wording and ask questions to understand intended meaning"
status: complete
---

# Clarify-meaning skill

Create a skill that runs only when invoked and asks about plausible ambiguities in the user's statements that could change the LLM's responses or actions in later turns. Its purpose is shared understanding, without fleshing out unspecified details or expanding the idea.

The [accepted workshop direction](idea.md) records the settled boundaries and three accepted improvements: grounded questions with consequences, brief reflections of resolved meaning, and open interpretation choices. The user agreed to finish the workshop.

The approved [quality rubric](intent.md#quality-rubric) remains unchanged. The [workshop assessment](evaluations.md) records judgments of the unbuilt idea's potential and verification limits.

Implemented [clarify-meaning/SKILL.md](../../skills/util/clarify-meaning/SKILL.md) with the accepted boundaries. After review, the user removed the three workshop improvements and the example as not earning their place; questions are now asked together and numbered. Implicit invocation is disabled by `disable-model-invocation: true` (Claude Code) and `agents/openai.yaml` (Codex).

Verification: skill validation passed, the invocation policy parsed correctly, and the name is unique across categories. Manual instruction review and scenario walkthroughs covered the approved rubric; results and limitations are recorded in [evaluations.md](evaluations.md#implementation-review--2026-10-14), with the revised version assessed in the [revision review](evaluations.md#revision-review--2026-10-14). The revised skill passed `quick_validate.py`. Actual model adherence has not been verified in a live trial. Implementation is complete and ready for user review.
