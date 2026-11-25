# Skills

Shared skills for Claude Code, Codex, and Gemini CLI.

## Structure

```
skills/
  development/       # coding, debugging, architecture
  engineering/       # project setup and conversational work-item tracking
  brainstorming/     # idea exploration, refinement, and development
  personal/          # personal productivity
  util/              # documentation and skill creation
scripts/
  install.sh         # one-time setup per machine
  update.sh          # pull latest + install and clean up repository links
```

## Bootstrap a new machine

```bash
git clone https://github.com/erik-saltwell/skills.git
cd skills
./scripts/install.sh
```

The installer links skills into `~/.claude/skills` and `~/.agents/skills`
(shared by Codex and Gemini CLI, avoiding duplicate discovery). Selecting either
Codex or Gemini installs to their shared location. It preserves existing files, directories, and symlinks
owned outside this repository. The source grouping is flattened at installation,
so skill names must be unique across groups.

Install just one group or agent:

```bash
./scripts/install.sh --category engineering
./scripts/install.sh --agent codex --category engineering
```

Set `SKILLS_INSTALL_ROOT` to a separate directory to smoke-check installation
without touching your personal skill directories.

Installation locations follow the official [Claude Code](https://code.claude.com/docs/en/skills),
[Codex](https://learn.chatgpt.com/docs/build-skills), and
[Gemini CLI](https://geminicli.com/docs/cli/skills/) documentation.

## Engineering workflow

- `setup-project`: creates `.work-items/workflow.md`, an empty root `WORK-ITEMS.md`,
  and `.agent_context.md` for your project-specific instructions. `CLAUDE.md` and
  `GEMINI.md` import `.agent_context.md` every turn; all three agent files point
  to the workflow for work-item activity. `AGENTS.md` directs Codex to read the
  context before starting work. Repeat setup preserves existing context, workflow customizations,
  and work items.
- `setup-workitem`: creates an item folder and a `registered` master-list entry,
  without creating `item.md`, an intent, or placeholders.
- `load-workitem`: selects an item as the conversation's focus and reads its saved
  documentation into context; asks which item to load when none is specified.
- `list-open-workitems`: lists all items whose status is not `complete`, including
  registration-only items, with their current statuses and folder links.
- `define-rubric` (optional): develops distinct qualitative quality dimensions and
  concise descriptions of what each values, without scores or anchor points. Once approved, the
  rubric is saved in the item's `intent.md` (created if needed). Without one,
  `workshop` derives its own qualitative rubric.
- `update-workitem`: saves rubrics/evaluations/ideas/intents/phased plans/progress,
  manages current-activity statuses, and lists or resumes work. Existing skills
  such as `workshop`, `flesh-out`, and `document-this` remain useful for the discussion.

In a new project's AI conversation, ask `Use setup-project here`. After exploring
an idea, ask `Use update-workitem to save this idea`. You can clear context and
resume by item name. Start with `Use setup-workitem to register CSV export`, then
optionally define its quality rubric using `define-rubric`. Claude Code also supports
`/setup-project` and `/update-workitem save intent`; use the skill picker or plain
language in other clients.

The installed project workflow defines these statuses:
`registered`, `captured`, `ideating`, `fleshing-out`, `planning`, `implementing`, `complete`.
Saving preserves the current status; starting a stage updates it. All records live
under `.work-items/`, and the root table includes open and completed items with
repo-relative folder paths as both link labels and targets. Planning and
implementation use appropriate verification without creating or expanding unit tests.

## Textual MCP server

[`servers/textual-mcp/`](servers/textual-mcp/) contains a standalone MCP server for
driving Textual applications, inspecting runtime state, capturing SVG/PNG documentation
evidence, and replaying scenarios. Its README includes installation, client configuration,
and a complete demo workflow.

## Update

```bash
./scripts/update.sh
```

## Adding a skill

1. Create a directory under `skills/<category>/<skill-name>/`
2. Add a `SKILL.md` with the skill instructions
3. Run `./scripts/install.sh` (or it will be picked up on next `update.sh`)
4. Commit and push
