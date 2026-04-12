---
name: write-readme
description: >-
  Generate a high-quality README.md for an existing
  project targeting GitHub publication. Analyzes the
  codebase, gathers missing context from the user,
  and produces a polished README following best
  practices.
allowed-tools: Read, Skill
---

# Generate README

Create or rewrite a project's README.md for GitHub
publication. Analyzes existing code, manifests, and
configuration to produce a comprehensive, well-
structured README.

## Process

### Step 1 — Scan the project

Read the following (skip any that do not exist):

- **Directory structure** — list top-level files and
  directories to understand project layout.
- **Project manifest** — `package.json`,
  `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`,
  `build.gradle`, `Gemfile`, or equivalent. Extract
  name, description, version, dependencies, scripts.
- **CI configuration** — `.github/workflows/`,
  `Makefile`, `Justfile`, `Dockerfile`,
  `docker-compose.yml`. Note build, test, and deploy
  commands.
- **Existing README.md** — note current structure and
  content for reference.
- **CLAUDE.md** — extract project description, tech
  stack, conventions.
- **LICENSE** — identify the license type.
- **CONTRIBUTING.md** — note if it exists.
- **Source code entry points** — main files, index
  files, or entry points to understand what the
  project does.

Compile a mental summary of:

- Project name and purpose
- Tech stack (language, framework, key dependencies)
- Build and run commands
- Test commands
- Key features or modules
- License type
- Whether the project is a library, CLI tool, web app,
  API, plugin, or other

### Step 2 — Check for existing README

If `README.md` already exists, use AskUserQuestion to
show its current state and ask:

> A README.md already exists. Do you want me to
> rewrite it from scratch, or update specific
> sections?

Do NOT overwrite without confirmation.

### Step 3 — Gather missing context

If any of the following are unclear after Step 1,
use AskUserQuestion to ask the user. Skip questions
whose answers are already obvious from the codebase.

- **Project purpose** — What does this project do in
  one or two sentences?
- **Target audience** — Who is it for (developers,
  end users, ops teams)?
- **Key features** — What are the main highlights
  worth calling out?
- **Prerequisites** — Any non-obvious requirements
  (specific runtime versions, external services, API
  keys)?
- **Badges** — Should the README include badges
  (CI status, license, version, coverage)?
  Suggest based on what CI and manifests reveal.
- **Screenshots or diagrams** — Does the user want
  to include any visuals?
- **Architecture diagram** — For non-trivial
  projects, propose including a Mermaid diagram
  showing the high-level architecture or component
  interactions.
- **Modules** — For multi-module projects (e.g.
  monorepos, multi-module Maven/Gradle builds,
  workspaces), list each module with a one-line
  description of its role.

Batch related questions into a single prompt to avoid
excessive back-and-forth.

### Step 4 — Generate README.md

Read the reference guide at
[references/guide.md](references/guide.md).

Read the template at
[references/template.md](references/template.md).

Generate `./README.md` by filling in each
`{{placeholder}}` with project-specific content:

- **Remove sections** that do not apply (e.g. no
  Configuration section if the project has none).
- **Adapt code examples** to the actual project
  commands and API.
- **Use fenced code blocks** with the correct
  language tag for all commands and code snippets.
- **Use relative links** for repo resources
  (e.g. `./docs/`, `./CONTRIBUTING.md`).
- **Add badges only if justified** — do not add
  aspirational badges for CI that does not exist.
- **Keep it concise** — prefer short paragraphs and
  bullet lists over walls of text.
- **Architecture diagram** — for non-trivial
  projects, include a Mermaid diagram showing
  high-level components and their interactions.
  Prefer Mermaid over ASCII art for GitHub
  rendering. Keep diagrams simple — 5 to 10 nodes
  maximum.
- **Module descriptions** — for multi-module
  projects, include a table or bullet list
  describing each module's purpose. Place this in
  the Architecture section.

### Step 5 — Review and refine

Present the generated README to the user. Use
AskUserQuestion to ask:

> Here is the generated README. Would you like to
> adjust anything — add sections, change wording,
> reorder content, or remove parts?

Apply requested changes. Repeat until the user is
satisfied.

## Rules

- **English only for generated files** — the README
  must be written in English, regardless of the
  user's language.
- **Respond in the user's language** when
  communicating with the user.
- **Do not fabricate** — only document what actually
  exists in the project. Do not invent features,
  commands, or configuration that you have not
  confirmed.
- **No secrets or absolute paths** — do not include
  credentials, tokens, or machine-specific paths.
- **Sequential steps** — complete each step before
  moving to the next.
- **Maintainable over comprehensive** — a shorter
  README that stays accurate beats a long one that
  rots. Prefer linking to external docs over
  duplicating them.
- **Line length** — keep Markdown lines to 80 columns
  max. Code blocks may extend to 120 columns.
