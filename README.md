# skillbox

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
plugin providing reusable skills and agents for everyday
software engineering tasks.

Skills enforce coding conventions, scaffold new projects,
and generate documentation. Agents handle code writing and
code review with opinionated best-practice defaults.

## Installation

Add the `cc-plugins` marketplace, then install skillbox:

```bash
/plugin marketplace add alexandreroman/cc-plugins
/plugin install skillbox@cc-plugins
```

## Skills

### User-invocable

Shown in the slash menu. Run them from the Claude Code
prompt.

| Skill          | Description                             |
| -------------- | --------------------------------------- |
| `init-project` | Bootstrap a new project or add a module |

### Model-only

Hidden from the slash menu. Claude uses them when the
task calls for them.

| Skill            | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `project-rules`  | Coding rules for Java, Go, Node.js, Spring Boot, infra |
| `project-memory` | Persist project decisions, deadlines, and team context |
| `write-readme`   | Generate a README.md for an existing project           |

## Agents

| Agent           | Description                                 |
| --------------- | ------------------------------------------- |
| `code-writer`   | Writes and refactors code, simplicity first |
| `code-reviewer` | Read-only review of code, docs, and memory  |

## Usage

Skills and agents are namespaced under `skillbox:`.

Invoke a skill from the Claude Code prompt:

```text
/skillbox:init-project
```

> [!TIP]
> **Getting started with a new project** — Run
> `/skillbox:init-project` first when bootstrapping
> a new repository. It generates an `AGENTS.md` that
> configures the `code-writer` and `code-reviewer`
> agents and wires up project memory so that
> decisions, deadlines, and team context persist
> across conversations — and it applies them from the
> very first generated file, with no session restart.

## Agent instructions

Generated projects get an `AGENTS.md` file and no
`CLAUDE.md`. Claude Code (v2.1.277 and later) reads
`AGENTS.md` natively, but it ignores `AGENTS.md` when
the project has a `CLAUDE.md` or a `CLAUDE.local.md`.

For older versions, or when a `CLAUDE.md` is already
present, add a one-line `CLAUDE.md` that contains
`@AGENTS.md`.

Docs: <https://code.claude.com/docs/en/memory#agents-md>

## Project structure

```text
.claude-plugin/plugin.json   Plugin manifest
skills/                      One folder per skill (SKILL.md)
agents/                      One file per agent (.md)
```

## License

[Apache-2.0](LICENSE)
