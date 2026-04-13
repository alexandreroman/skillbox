# skillbox

A Claude Code plugin serving as a repository for
reusable skills and agents.

## Structure

```text
.claude-plugin/plugin.json   # Plugin manifest
skills/                      # One folder per skill
agents/                      # One .md file per agent
```

## Conventions

- Skills live in `skills/<skill-name>/SKILL.md`
- Agents live in `agents/<agent-name>.md`
- Use kebab-case for naming
- Skills and agents are namespaced under
  `skillbox:` (e.g. `/skillbox:my-skill`)
- All generated text and code must be in English
- Line length limits for readability:
  - Text / Markdown: 80 columns max
  - Code: 120 columns max
- Use worktrees for non-trivial changes
- Follow standard Markdown conventions: blank line
  before and after headings, blank line before and
  after lists, fenced code blocks with a language tag
- Format Markdown tables with aligned columns:
  pad cells with spaces so that every `|` in a
  column lines up vertically, and use `-` runs
  matching each column width in the separator row
- After editing a Markdown table, run
  `python3 skills/general-rules/scripts/check_tables.py <file>`
  and fix any reported misalignment before
  considering the change done
- Skills must follow the Agent Skills spec:
  https://agentskills.io/specification
