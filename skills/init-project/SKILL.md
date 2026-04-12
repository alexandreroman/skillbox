---
name: init-project
description: >-
  Use when starting a new project or bootstrapping an
  empty repository. Interactively gathers the project
  objective and name, then generates README.md and
  CLAUDE.md so Claude Code has proper context from
  day one.
allowed-tools: Read, Skill
---

# Initialize Project

Bootstrap a new project by gathering requirements
from the user, then generating foundational files.

## Process

### Step 1 — Understand the objective

Use AskUserQuestion to ask the user to describe the
project objective in a few sentences:

- What problem does it solve?
- Who is the target audience?
- Any known technical constraints (language,
  framework, platform)?

Do NOT proceed until you have a clear answer.

### Step 2 — Choose a project name

Propose 3-5 short, memorable project names based on
the objective. Names should be:

- Lowercase, kebab-case (e.g. `data-forge`)
- Easy to type and remember
- Evocative of the project's purpose

Use AskUserQuestion to ask the user to pick one or
suggest their own.
Do NOT proceed until a name is confirmed.

### Step 3 — Choose a license

Use AskUserQuestion to ask the user which license
to use. Suggest:

- **Apache-2.0** (default)
- **MIT**

The user may also specify a different license.
If the user has no preference, use Apache-2.0.

### Step 4 — Scaffold the project

If the tech stack chosen in step 1 matches one of the
scaffolding references, follow its instructions
**before** generating any documentation files.
If no reference matches, skip this step.

Pick the matching file from
[references/](references/):

- [java-spring-boot.md](references/java-spring-boot.md)
- [nodejs-typescript.md](references/nodejs-typescript.md)
- [python.md](references/python.md)
- [go.md](references/go.md)
- [rust.md](references/rust.md)

Read **only** the matching file and apply its
instructions.

### Step 5 — Scan existing state

Before generating files, check for:

- Existing `README.md` or `CLAUDE.md` — ask the user
  before overwriting.
- Project manifest (`package.json`, `pyproject.toml`,
  `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`,
  `Gemfile`, or equivalent) — extract tech stack info.
- CI configuration (`.github/workflows/`, `Makefile`,
  `Justfile`) — note build commands.

### Step 6 — Generate README.md

Read the template at
[assets/README.md](assets/README.md).
Write `./README.md` by
filling in each `{{placeholder}}` with project-
specific content. Remove any section whose
placeholder has nothing useful to say.

Reference:
https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

### Step 7 — Generate CLAUDE.md

Read the template at
[assets/CLAUDE.md](assets/CLAUDE.md).
Write `./CLAUDE.md` by
filling in each `{{placeholder}}` with project-
specific content. Keep the file **short and
essential** (~40-60 lines max). Remove any section
whose placeholder has nothing useful to say.
The **Agents section is mandatory** — never remove it.

Reference:
https://code.claude.com/docs/en/best-practices

### Step 8 — Generate LICENSE

Write `./LICENSE` with the full text of the license
chosen in step 3. Use the current year and the
user's name (from git config) for the copyright
notice.

Reference:
https://choosealicense.com/licenses/

### Step 9 — Present and confirm

Show all generated files to the user for review.
Ask if anything needs adjustment before finalizing.

## Rules

- **English only for generated files** — all content
  in README.md and CLAUDE.md must be in English,
  regardless of the user's language.
- **Respond in the user's language** when
  communicating with the user.
- **Concise** — prefer references over inline
  documentation. Do not duplicate information between
  README.md and CLAUDE.md; CLAUDE.md should reference
  README.md rather than repeat it.
- **Agents section is mandatory** in CLAUDE.md —
  always include code-writer and code-reviewer.
- **README.md reference is mandatory** in CLAUDE.md —
  always link to README.md.
- **No secrets or paths** — do not include absolute
  paths, credentials, or environment-specific values.
- **Sequential steps** — complete each step before
  moving to the next. Do not generate files before
  the user has confirmed the objective and name.
