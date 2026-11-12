---
name: write-readme
description: >-
  Generate or update the README.md of an existing project for GitHub
  publication, from its codebase and the user's answers. Use when the user
  asks to write, create, regenerate, or improve a README, or when another
  skill delegates README generation. For a brand-new repository, start with
  init-project, which delegates the README here once the project exists.
user-invocable: false
---

# Generate README

Create or rewrite a project's README.md for GitHub
publication from its code, manifests, and
configuration.

When bootstrapping a brand-new repository, run the
**init-project** skill first, unless it is already
running: it scaffolds the project, then delegates the
README to this skill.

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
  `compose.yaml`. Note build, test, and deploy
  commands.
- **Existing README.md** — note current structure and
  content for reference.
- **Instruction file** — read `AGENTS.md`; if it does
  not exist, read `CLAUDE.md`. Extract project
  description, tech stack, conventions.
- **LICENSE** — identify the license type.
- **CONTRIBUTING.md** — note if it exists.
- **Source code entry points** — main files, index
  files, or entry points to understand what the
  project does.

From these, work out the project's name and purpose,
tech stack, build, run, and test commands, key
features or modules, license, and kind (library, CLI
tool, web app, API, plugin, or other).

### Step 2 — Check for existing README

If `README.md` already exists, show its current state
and ask the user:

> A README.md already exists. Do you want me to
> rewrite it from scratch, or update specific
> sections?

Do NOT overwrite without confirmation.

### Step 3 — Gather missing context

If any of the following are unclear after Step 1,
ask the user. Skip questions whose answers are
already obvious from the codebase.

- **Project purpose** — What does this project do in
  one or two sentences?
- **Target audience** — Who is it for (developers,
  end users, ops teams)?
- **Key features** — What are the main highlights
  worth calling out?
- **Prerequisites** — Any non-obvious requirements
  (specific runtime versions, external services, API
  keys)?
- **Badges** — Which badges to include? Suggest
  those that CI and manifests support.
- **Visuals** — Any screenshots or diagrams? For
  non-trivial projects, propose a Mermaid
  architecture diagram.

Batch related questions into a single prompt to avoid
excessive back-and-forth.

### Step 4 — Generate README.md

Read the guide at [references/guide.md](references/guide.md)
and the template at [assets/README.md](assets/README.md).

Generate `./README.md` by filling in each
`{{placeholder}}` with project-specific content.
Remove sections that do not apply (e.g. no
Configuration section if the project has none) and
adapt code examples to the actual project commands
and API.

### Step 5 — Review and refine

Present the generated README to the user and ask:

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
- **No secrets or absolute paths** — no credentials,
  tokens, or machine-specific paths, even as
  examples: use placeholders like `your-api-key`.
- **Sequential steps** — complete each step before
  moving to the next.
- **Maintainable over comprehensive** — a shorter
  README that stays accurate beats a long one that
  rots. Prefer linking to external docs over
  duplicating them.
