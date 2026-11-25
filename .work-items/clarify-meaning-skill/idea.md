# Clarify-meaning skill: accepted workshop direction

Create an explicitly invoked skill that helps the user and LLM understand each other by resolving plausible ambiguities in what the user has already said. Focus only on competing meanings whose resolution could change the LLM's responses or actions in later prompts, turns, or messages.

## Settled boundaries

- Run only when the user invokes the skill, rather than checking every message automatically.
- Clarify existing meaning. Do not flesh out unspecified details, expand the idea, or turn clarification into a design interview.
- Respect context and prior clarifications when identifying plausible interpretations.

## Accepted workshop improvements

1. **Ground each question and explain its consequence.** Connect the question to a phrase the user used, present plausible competing interpretations, and briefly explain how the difference could affect a later response. This makes the reason for asking visible and helps filter out speculative ambiguities and requests for missing details. The tradeoff is slightly longer questions.
2. **Reflect the resolved meaning.** After the user answers, briefly restate the understood meaning, including any consequential boundary. This lets the user catch a misunderstanding before it influences later responses. Keep the reflection brief because it can feel repetitive for simple answers.
3. **Leave interpretations open.** Suggested meanings are possibilities, not an exhaustive choice. Allow the user to answer both, neither, or explain another meaning. This avoids forcing their intent into the LLM's assumptions. Use natural phrasing rather than repeatedly listing every possible answer type.

For illustration, a question could ask whether “save this” means preserving exact wording or summarizing decisions, explaining that the answer changes what would be written to the file. A reflection could then state the meaning established by the user's answer. Examples illustrate the approach; they do not establish the user's intent in a real interaction.

## Workshop endpoint and continuation

The user accepted all three improvements and agreed to finish the workshop. No tentative workshop proposals remain. The agent recommended stopping because further rules appeared likely to add complexity without a substantial benefit before trying the skill.

The [approved quality rubric](intent.md#quality-rubric) remains unchanged. The [workshop assessment](evaluations.md) describes apparent potential, not demonstrated performance. Actual question quality remains unverified because the skill has not been built or tried. No implementation plan or implementation choices were established.

## Later revision

After reviewing the implemented skill, the user removed improvements 1–3 and the illustrative example because they did not earn their place in the skill. The settled boundaries remain. See the [revision review](evaluations.md#revision-review--2026-10-14).
