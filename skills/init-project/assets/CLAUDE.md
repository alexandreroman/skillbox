# {{project-name}}

{{One-sentence description of what the project does.}}

See [README.md](README.md) for full documentation.

## Tech stack

{{Language, framework, key dependencies — bullet list,
no versions unless a specific version constraint
matters. Omit if not yet decided.}}

## Build & run

{{Essential commands only: install, build, test, run.
Use a fenced code block. Omit if not yet applicable.}}

## Modules

{{Brief description of each module or top-level
directory and its responsibility — bullet list.
Omit if the project has no modular structure.}}

## Agents

Use the following agents (from the
[skillbox](https://github.com/alexandreroman/skillbox)
plugin) for all code tasks:

- **code-writer** — for ANY task that writes,
  modifies, or refactors code. No exceptions.
- **code-reviewer** — for read-only code review
  before merging or when investigating issues.

## Memory

At the start of every conversation, read
`.claude/project-memory/MEMORY.md` to load
project context from previous conversations.

Use the **project-memory** skill (from the
[skillbox](https://github.com/alexandreroman/skillbox)
plugin) proactively — without being asked — whenever
the conversation reveals project decisions, deadlines,
team context, external references, workflow preferences,
or corrective feedback worth persisting across
conversations.

**Important:** Always use the **project-memory**
skill to persist information. Never use the built-in
auto-memory system (`~/.claude/projects/.../memory/`)
for project decisions or context — it is local and
not shared with the team.

## Conventions

- Line length limits for readability:
  - Text / Markdown: 80 columns max
  - Code: 120 columns max
- Follow standard Markdown conventions: blank line
  before and after headings, blank line before and
  after lists, fenced code blocks with a language tag
- Always use the latest LTS or stable version of
  languages, frameworks, and libraries. Check the
  official documentation or use available tools
  (e.g. context7) to verify current versions before
  choosing a dependency.

{{Additional project-specific rules not obvious from
the code. Keep to 3-5 bullets max. Omit if nothing
non-obvious to say.}}
