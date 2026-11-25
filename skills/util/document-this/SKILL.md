---
name: document-this
description: Synthesizes a discussion or supplied material into a durable markdown document that a human or agent can understand later without the original conversation. Use when the user wants to document, crystallize, write up, or preserve an idea, proposal, plan, concept, development approach, software architecture, feature design, or other subject, including Magic the Gathering deck ideas.
---

# Document This

Turn the current discussion and relevant supplied material into a durable document that a human or agent can understand later without the original conversation. Preserve what the idea means, the reasoning behind consequential choices, and what remains tentative. A brainstorm is one possible source; the subject need not be software or a finished design.

## Synthesis Rules

**Preserve what future understanding requires.** Include the purpose, key concepts, relevant details, constraints, and intended use. Retain rationale and implementation detail when they explain the subject or enable someone to use the document. Define unfamiliar terms and avoid references such as "the approach above" that depend on the conversation.

**Preserve decision status.** Distinguish settled decisions, proposals, assumptions, and open questions. Apply "final position wins" only to actual revisions or agreements. The latest suggestion, including an agent recommendation, is not automatically a decision. Preserve unresolved contradictions without silently choosing a side.

**Keep consequential reasoning.** Retain the reasons and tradeoffs behind important choices. Omit conversational history and abandoned branches unless they explain a tradeoff or help a future reader avoid reopening a settled issue.

**Synthesize without filling gaps.** Organize and clarify the material without inventing decisions, facts, or missing design details. Ask only when an ambiguity prevents a faithful write-up; otherwise record the uncertainty. Do not turn documentation into a new research, design, or planning exercise unless requested.

**Keep length proportional.** Make the document as short as possible while preserving what someone needs to understand and use it. A concept sketch and a substantial architecture warrant different lengths. Use lists, tables, or diagrams when they clarify relationships; omit empty sections.

**Reference durable artifacts.** When specifications, plans, ADRs, issues, commits, diffs, or other artifacts already capture a detail, link to them by path or URL instead of duplicating their contents. Include enough context to make this document understandable, then point to supporting detail. Use supplied or verified references; do not invent paths or imply that unread material was verified. If the discussion changes an existing documented decision, identify the change and its status explicitly rather than appearing to agree with the older artifact. Do not modify supporting artifacts unless requested.

**Redact sensitive information.** Omit or replace API keys, passwords, access tokens, private keys, personal data, and other sensitive information in both inline drafts and saved documents. Preserve the relevant concept without exposing the value—for example, describe storing a credential without recording it. Check examples and reference URLs for sensitive values as well.

## Adapt the Structure

Use a descriptive title and a brief explanation of what the document describes. Organize the essential details for the subject, retaining consequential reasoning and clearly identifying anything tentative or unresolved. These are useful foundations, not mandatory headings.

Choose sections that suit the material. For example:

- **Proposal or concept:** intended outcome, core idea, constraints, tradeoffs, and open questions.
- **Development approach or plan:** goal, approach, sequence, dependencies, and known uncertainties. Include ownership or milestones only when established.
- **Software architecture:** components, responsibilities, interactions, constraints, decisions, and tradeoffs.
- **Feature design:** key concepts, user flows, behaviors, rules, and unresolved choices.
- **Magic the Gathering deck idea:** format and constraints if established, strategy, card roles and interactions, weaknesses, and candidate choices. Do not invent a complete decklist or treat unverified legality or interactions as settled facts.

Adapt freely to other subjects. Do not force every document into one of these examples or introduce sections simply to complete a template.

## Workflow

1. **Gather and synthesize.** Read the relevant available conversation and supplied material. Consult supporting artifacts selectively when they inform the write-up. Identify the current concept, consequential reasoning, decision status, unresolved questions, useful references, and sensitive information to redact.

2. **Write and review.** Choose a structure suited to the subject and intended reader. Check that someone reading it later can understand it without the original conversation, that tentative ideas remain tentative, that references support the associated text, and that sensitive values are absent.

3. **Save.** Use a destination already supplied or clearly established by the project. When the destination is known, write the markdown file directly without requiring a separate draft approval. Create a missing destination directory as needed. If the destination remains unclear, show the draft and ask where to save it. If the user requests only an inline document, provide that without requiring a file. When updating an existing document, preserve unrelated content and incorporate the requested changes.

4. **Finish.** Confirm where the document was saved with a link, or deliver the requested inline document. Do not initiate implementation or other next steps unless requested.
