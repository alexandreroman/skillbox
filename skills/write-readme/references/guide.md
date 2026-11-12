# README Guide

A README must answer in seconds: **what** the
project does, **why** the reader should care, and
**how** to get started. Everything else is
supporting detail. The template sets the section
order; this guide adds what its placeholders do not
say.

## Writing style

- **Concise** — short paragraphs, bullet lists,
  tables. Break up a section longer than a
  screenful or move it to a separate doc.
- **Scannable** — use headings, bold text, and code
  formatting as visual anchors.
- **Action-oriented** — start instructions with
  verbs: "Install", "Run", "Configure".
- **Present tense** — "The server starts on port
  8080", not "will start".
- **Second person** — address the reader as "you".
- **No jargon without context** — define acronyms
  on first use or link to explanations.

## Sections

### Description

Do not repeat the project name in the description.

```markdown
# dataforge

Transforms messy CSV exports into clean, typed
datasets ready for analysis. Built for data
engineers who are tired of writing one-off
cleaning scripts.
```

### Badges

Place badges on a single line directly below the
description. Include only badges backed by real,
working infrastructure:

| Badge type   | When to include              |
| ------------ | ---------------------------- |
| CI status    | Working GitHub Actions or CI |
| License      | LICENSE file exists          |
| Version      | Published to a registry      |
| Coverage     | Coverage reporting is set up |
| Docker image | Image is published           |

```markdown
[![Build](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main)][ci]
[![License](https://img.shields.io/github/license/OWNER/REPO)](LICENSE)

[ci]: https://github.com/OWNER/REPO/actions
```

### Features

Describe outcomes, not implementation details.

### Usage

- Show real commands and realistic output.
- For libraries, show a minimal import-and-use
  snippet; for CLI tools, the most common
  invocation; for web apps, how to access the UI.

### Architecture

Include only when the structure is not obvious from
the directory layout.

- **Diagram** — Mermaid, which GitHub renders
  natively; prefer it over ASCII art. Keep it to 5 to 10
  nodes showing components, not implementation
  details, with short labels. Pick the type:
  `graph TD` for components and flows,
  `sequenceDiagram` for request flows, `C4Context`
  for system context.
- **Modules** — for monorepos, workspaces, or
  multi-module builds (Maven, Gradle, npm
  workspaces, Go modules), fill the modules table
  after the diagram: one row per module, core first
  then dependents, one-sentence descriptions.

### License

If the project has no LICENSE file, point out to the
user that an unlicensed repository is legally
ambiguous and suggest adding one.

## Formatting

- Blank line before and after every heading and
  every list.
- Fenced code blocks with a language tag (`bash`,
  `python`, `json`, ...); never indented blocks.
- Relative links for repo resources
  (`./docs/setup.md`), absolute URLs for external
  ones.
- Alt text on every image: `![Alt text](path.png)`.
- Tables: pad cells so every `|` lines up
  vertically, with separator dashes matching each
  column width.
- Markdown lines 80 columns max; code inside fenced
  blocks may extend to 120 columns.
