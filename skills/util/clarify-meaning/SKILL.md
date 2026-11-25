---
name: clarify-meaning
description: "Ask about ambiguous wording in what I've said, so we mean the same thing."
disable-model-invocation: true
---

# Clarify Meaning

Make sure you and the user mean the same thing by what they have already said.

## Find consequential ambiguities

Use the user's supplied statement or identified discussion as the subject. If they invoke the skill without naming a subject, use the current discussion. Read the available context and prior clarifications before deciding that wording is ambiguous.

Look for plausible competing interpretations grounded in what the user actually said. Ask only when choosing between them could change how you respond or act in later turns. Do not manufacture remote interpretations or reopen meanings already resolved by context.

Distinguish ambiguity from an unspecified detail: competing readings of existing terms or concepts need clarification; a choice the user has not expressed does not become an ambiguity merely because it might matter later. Do not solicit new requirements, flesh out ideas, recommend improvements, or turn this interaction into a design interview.

If no consequential ambiguity remains, say so briefly and finish. Do not invent a question to justify using the skill.

## Ask about the intended meaning

Ask all questions together, numbering each one (**Q1.**, **Q2.**, ...) so the user can reference them. For each question:

- Quote or clearly identify the wording or concept being clarified.
- Present plausible competing meanings in neutral, concrete language.

Keep questions focused and easy to answer. Prioritize consequential distinctions and avoid redundant questions.

## Finish

Use the resolved meaning in subsequent turns. If an answer raises a new consequential ambiguity, ask about it; do not re-ask anything already settled. Finish when no consequential ambiguity remains or the user ends the clarification. Ending this exchange does not start fleshing-out, implementation, saving, or another activity without a user request.
