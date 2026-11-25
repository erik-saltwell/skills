# Clarify-meaning skill

When explicitly invoked, clarify ambiguities in what the user has said that could affect the LLM's responses or actions in later turns, so the user and LLM share an understanding of the intended meaning.

## Quality rubric

This rubric judges how well the clarify-meaning skill establishes shared understanding of the user's existing statements. The skill runs only when invoked.

- **Interpretive fidelity:** Identifies plausible meanings grounded in the user's words and context, respecting prior clarifications.
- **Future relevance:** Focuses on ambiguities that could change the LLM's responses or actions in later turns.
- **Question clarity:** Makes competing meanings easy to understand and answer without steering the user's choice.
- **Conversational economy:** Keeps questions focused and avoids redundant clarification.
- **Clarification focus:** Establishes shared understanding of what the user already said, without fleshing out unspecified details or expanding the idea.
