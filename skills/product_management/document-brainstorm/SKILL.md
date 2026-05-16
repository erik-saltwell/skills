---
name: document-brainstorm
description: Synthesizes a brainstorm conversation into a concise, human-readable domain-level markdown document. Captures entities, flows, behaviors, and unresolved tensions from the conversation. Use when the user wants to crystallize, document, or summarize a brainstorm session into a feature doc. Triggered by phrases like "crystallize this", "document this brainstorm", "write this up", or "turn this into a doc".
---

# Document Brainstorm

## Overview

To take a brainstorm conversation — with all its branches, revisions, and tangents — and synthesize it into a clean, domain-level markdown document that a human can read to understand how a feature or product works conceptually.

The output lives between a PRD (business level: why) and a technical design doc (technical level: how). It answers *what*: the entities, flows, behaviors, and rules that define the feature at the domain level.

## Synthesis Rules

**Final position wins.** When the conversation revises or contradicts itself, use the settled position. Drop earlier branches silently unless the contradiction was explicitly named but not resolved.

**Named tensions become Open Questions.** If the conversation surfaced a real ambiguity but did not close it, preserve it in the Open Questions section rather than silently picking a side.

**Domain language only.** Strip business justification (why we're building it) and implementation details (how it's built). Keep entities, flows, behaviors, and rules.

**Concise over complete.** The document should be readable in under 5 minutes. If a section would become a wall of text, summarize and use bullets.

## Output Template

Use this as a starting point. Deviate freely when the content doesn't fit — add sections, merge sections, or drop sections that have nothing to say.

```markdown
# [Feature Name]

## Overview
One paragraph. The core idea and what it does at the domain level. No business rationale, no implementation details.

## Key Concepts
The entities and terms the reader must understand to follow the rest of the document. Define them briefly. If the brainstorm used inconsistent terminology, pick the canonical term here.

## Flows
How things move through the system. User journeys, state transitions, sequences of events. Use numbered steps or sub-sections for distinct flows.

## Behaviors & Rules
Constraints, edge cases, and notable invariants. What the system does (and doesn't do) in specific situations.

## Open Questions
Tensions or ambiguities that the brainstorm named but did not resolve. One bullet per question. Omit this section entirely if there are none.
```

## Workflow

1. **Synthesize** — Read the full conversation. Identify the final settled position on each design decision. Note any explicitly unresolved tensions.

2. **Draft** — Write the document using the template above as a guide. Adapt the structure to fit the content. Show the draft inline in the conversation.

3. **Save** — After showing the draft, ask the user where to save the file. Use their answer to write the markdown file to disk.

   Suggested prompt: *"Where should I save this? (e.g., `docs/feature-name.md`)"*

   If the user suggests a path in a directory that doesn't exist, create it.

4. **Done** — Confirm the file was saved. Do not iterate further unless the user requests changes.
