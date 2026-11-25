# textaul-mcp quality rubric

Version 1, completed 2026-09-15. The user accepted all six dimensions, their numerical anchors, and the contrasting-outcomes calibration below. This replaces the earlier dimensions-only draft. No actual evaluation scores have been assigned.

## Subject and intended use

textaul-mcp is an MCP server for driving Python applications built with Textual. The user has access to the applications' source code and can edit it. The intended operator is an AI agent supporting these primary use cases:

1. Debugging.
2. Visual styling and diagnostics.
3. Testing.
4. Generating end-user documentation with screenshots.

Operating on unmodified applications is not a primary requirement. Integration effort is not included as a quality dimension in this rubric.

## Scoring conventions

Use independent per-dimension scores on the workflow's shared 0–10 scale, where higher means stronger quality. Intermediate values require supporting reasoning. No aggregate score, weights, required targets, or pass/fail thresholds are defined. Actual evaluations and refinement recommendations belong to later work and are not part of this document.

Use the accepted anchors below to interpret numerical levels. Missing assessments are unassessed, not zero.

## Accepted dimensions

| Dimension | Quality being judged |
|---|---|
| Diagnostic insight | How well the server helps an agent explain unexpected behavior and identify relevant causes, connecting observed symptoms to application code or runtime state rather than only reporting symptoms. |
| Visual fidelity | How accurately the server conveys the full rendered appearance a person would see in the terminal, including layout, spacing, colors, styling, wrapping, clipping, widget visibility, and focus. Trustworthy visual representation is especially important for documentation screenshots. |
| Interaction coverage | How fully an agent can reach and exercise the application states and workflows needed for debugging, testing, and documentation. |
| Repeatability | How consistently scenarios can be reproduced and actions connected to their resulting application state. |
| Documentation evidence | How well captures and associated context support accurate end-user instructions: screenshots are readable, appropriately framed, and associated with the relevant action or state. |
| Agent usability | How understandable and efficient the inspection and control tools are for an AI agent, including tool discovery, context burden, and interaction overhead. |

## Dimension boundaries

Visual fidelity concerns whether the appearance is represented accurately. Documentation evidence concerns whether that representation is useful in an end-user guide. An accurate screenshot of the wrong moment can be faithful but poor documentation evidence.

Diagnostic insight concerns explaining behavior; visual fidelity concerns seeing it accurately. Interaction coverage concerns which workflows can be exercised; repeatability concerns how consistently those workflows can be reproduced.

## Accepted scoring anchors

### Diagnostic insight

| Score | Anchor |
|---|---|
| 0 | Provides no usable evidence for investigating unexpected behavior. |
| 2 | Exposes the visible symptom, but little context for explaining it. |
| 5 | Exposes relevant state and events, allowing the agent to narrow down plausible causes, though substantial investigation remains. |
| 8 | Lets the agent connect the symptom to relevant runtime state and application code, with enough evidence to distinguish likely causes. |
| 10 | Supports tracing difficult failures across interactions, state changes, and code, with evidence sufficient to verify a causal explanation and identify remaining uncertainty. |

Judge the evidence made available by the server; the agent can perform the reasoning. A 10 does not require the server to diagnose bugs itself.

### Visual fidelity

| Score | Anchor |
|---|---|
| 0 | Provides no usable representation of the rendered app. |
| 2 | Conveys some content or structure, but omits or distorts major visual details. |
| 5 | Represents the main layout and styling, but discrepancies limit confidence in judging wrapping, spacing, colors, clipping, or focus. |
| 8 | Faithfully captures the rendered appearance at a known terminal size, with only minor discrepancies that rarely affect visual diagnosis or documentation. |
| 10 | Consistently preserves visually meaningful details across relevant app states and terminal sizes, allowing trustworthy inspection and documentation without needing a separate visual check. |

Judge accuracy here; screenshot selection and framing belong to documentation evidence.

### Interaction coverage

| Score | Anchor |
|---|---|
| 0 | Cannot interact with the app. |
| 2 | Supports a few basic actions, leaving most relevant workflows inaccessible. |
| 5 | Supports common workflows, but meaningful gaps prevent exercising some controls, navigation paths, or application states. |
| 8 | Supports nearly all interactions needed for debugging, visual inspection, testing, and documentation; occasional cases require manual intervention. |
| 10 | Supports the full range of interactions needed across the intended apps, including custom controls and complex input sequences, without manual intervention. |

Judge coverage across the intended apps, not every possible Textual app. Source access makes app-specific integration acceptable. Reliability of executing these interactions is judged separately.

### Repeatability

| Score | Anchor |
|---|---|
| 0 | Cannot meaningfully reproduce an interaction sequence or establish what happened. |
| 2 | Repeating the same actions often produces unexplained differences, requiring substantial manual reconstruction. |
| 5 | Common scenarios can be repeated from a known starting state, but failures or divergent outcomes remain difficult to reconstruct. |
| 8 | Scenarios reproduce consistently under equivalent starting conditions, with enough action and state evidence to investigate divergences. |
| 10 | Even complex scenarios can be reproduced consistently, with starting conditions, actions, and resulting states traceable enough to distinguish application variation from control failures. |

Reward reproducible investigation without requiring the application itself to behave deterministically. No separate requirement for background activity or delayed updates is added.

### Documentation evidence

| Score | Anchor |
|---|---|
| 0 | Produces no usable screenshots or supporting context for documentation. |
| 2 | Produces captures, but their relevance or connection to user actions is unclear. |
| 5 | Provides readable screenshots of common workflows, but substantial manual work is needed to select, frame, and connect them to instructions. |
| 8 | Provides appropriately framed screenshots of relevant states, clearly associated with the actions and steps they illustrate, requiring little manual preparation. |
| 10 | Provides a coherent sequence of documentation-ready screenshots and supporting context across the intended workflows, making steps and outcomes clear with minimal editorial work. |

The server supplies evidence useful for explaining a task; it need not write the guide itself.

### Agent usability

| Score | Anchor |
|---|---|
| 0 | Tools and responses are too unclear or inconsistent for meaningful use. |
| 2 | Basic tasks require extensive guessing, repeated trial and error, or human guidance. |
| 5 | Common tasks are understandable, but awkward tool semantics, excessive output, or unclear errors create substantial overhead. |
| 8 | Tools are discoverable and consistent; responses provide relevant context, and errors explain how to recover. Most tasks require little avoidable overhead. |
| 10 | Even complex tasks remain straightforward to orchestrate, with precise tool semantics, appropriately scoped responses, and clear recovery paths that minimize unnecessary calls and context consumption. |

Judge ease of using the available capabilities. Broad interaction coverage does not by itself imply good agent usability.

## Accepted calibration comparison

The user confirmed the following hypothetical comparison matches their intended judgments:

- **Server A:** Faithful, well-framed screenshots with clear links to documentation steps, but basic diagnostic state and an interface requiring many cumbersome calls.
- **Server B:** Rich diagnostic evidence, repeatable interactions, and efficient tools, but screenshots that lose styling details and require manual preparation for documentation.

The rubric favors A on visual fidelity and documentation evidence, and B on diagnostic insight, repeatability, and agent usability. Interaction coverage could be equal. Neither receives an overall score. These are calibration examples, not evaluations of textaul-mcp.
