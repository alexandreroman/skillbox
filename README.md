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

| Skill            | Description                                                                      |
| ---------------- | -------------------------------------------------------------------------------- |
| `project-rules`  | Coding rules for Java, Go, Node.js / TypeScript, Spring Boot, and infrastructure |
| `project-memory` | Persist project decisions, deadlines, and team context across conversations      |

## Agents

| Agent            | Description                                                             |
| ---------------- | ----------------------------------------------------------------------- |
| `code-writer`    | Writes, modifies, and refactors source code with simplicity-first style |
| `code-reviewer`  | Read-only code review producing a severity-ranked findings report       |

## Usage

Skills and agents are namespaced under `skillbox:`.

Invoke a skill from the Claude Code prompt:

```text
/skillbox:init-project
/skillbox:write-readme
```

> [!TIP]
> **Getting started with a new project** — Run
> `/skillbox:init-project` first when bootstrapping
> a new repository. It generates a `CLAUDE.md` that
> configures the `code-writer` and `code-reviewer`
> agents and wires up project memory so that
> decisions, deadlines, and team context persist
> across conversations.

## Project structure

```text
.claude-plugin/plugin.json   Plugin manifest
skills/                      One folder per skill (SKILL.md)
agents/                      One file per agent (.md)
```

## License

[Apache-2.0](LICENSE)
