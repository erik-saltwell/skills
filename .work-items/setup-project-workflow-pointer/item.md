---
name: "Setup project workflow pointer"
status: complete
---

# Setup project workflow pointer

Replace setup-project's always-loaded workflow import with a conditional work-item pointer while keeping project context loaded every turn. Use writing-for-agents as the writing standard. Preserve content outside managed blocks and existing project context during repeat setup, and create new context files with just their heading.

Update the bundled verification policy to the user-supplied wording, align skill documentation, and inspect all engineering work-item skills for workflow reads. Verify fresh setup and migration against a project copy and show the generated instruction and context files. Leave changes uncommitted; do not push.

## Completed

Updated setup-project's managed block constants to load project context and reach the workflow through the user-specified pointer. New context files contain only `# Project context`. Existing marker replacement already supported migration and was retained. Updated the bundled verification policy exactly as requested, steps 3 and 6 of the skill, and the README's description of the setup contract.

All five other engineering skills that act on work items already direct the agent to read the project workflow; no additions were needed. Loaded writing-for-agents and its mechanics reference before editing.

## Verification

[Full generated files and execution evidence](verification.md) show fresh setup and migration from a copy of this repository's old managed blocks. Both runs succeeded; repeat setup made no changes. Prefix and suffix bytes outside all three managed blocks stayed unchanged. Existing context, workflow, index, and work-item files were preserved byte-for-byte. Fresh context has only its heading and fresh workflow matches the revised template. Python source compilation passed. No unit tests were added.

The repository's own agent entry files and existing context were left in place; this change targets the setup skill and generated projects. No actual agent session was launched. Changes remain uncommitted; no push was performed.
