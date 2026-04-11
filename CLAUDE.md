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
