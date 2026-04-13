---
name: init-project
description: >-
  Use when starting a new project, bootstrapping an
  empty repository, or adding a new module to an
  existing project. Interactively gathers the objective
  and name, then generates the appropriate files so
  Claude Code has proper context from day one.
allowed-tools: Read, Skill, TaskCreate, TaskUpdate
---

# Initialize Project

Bootstrap a new project or module by gathering
requirements from the user, then generating
foundational files.

## Modes

This skill operates in one of two modes, determined
during the requirements phase:

| Mode        | Scope                                  |
| ----------- | -------------------------------------- |
| **Project** | Top-level repository — full scaffold   |
| **Module**  | Sub-directory inside existing project  |

A **base directory** can optionally be specified in
either mode. When provided, the base replaces the
generic scaffolding references and is used as a
template for the new project or module.

## Plan

After gathering requirements (phase 1), create a
plan using TaskCreate so the user can track progress.
Adapt the plan to the detected mode:

### Project-mode plan

Create the following tasks in order:

1. Scaffold project
2. Apply best practices
3. Generate README.md
4. Generate CLAUDE.md
5. Generate LICENSE
6. Review and confirm

### Module-mode plan

Create the following tasks in order:

1. Scaffold module
2. Apply best practices
3. Review and confirm

Use TaskUpdate to mark each task `in_progress` when
you start it and `completed` when you finish it.

## Process

### Phase 1 — Gather requirements

This phase runs **before** the plan is created.

#### 1a — Understand the objective

Use AskUserQuestion to ask the user to describe the
objective in a few sentences:

- What problem does it solve?
- Who is the target audience?
- Any known technical constraints (language,
  framework, platform)?
- Is this a **standalone project** (top-level
  repository) or a **module** within an existing
  project?
- Should it be based on an **existing module or
  directory** in the codebase? If so, which one?

**Detecting module mode:** if the current working
directory already contains a `CLAUDE.md` or a parent
project manifest, this is likely a module. Ask the
user to confirm. If the user explicitly says they
want to create a module, component, or sub-project,
treat it as a module.

Do NOT proceed until you have a clear answer.

#### 1b — Choose a name

Propose 3-5 short, memorable names based on the
objective. Names should be:

- Lowercase, kebab-case (e.g. `data-forge`)
- Easy to type and remember
- Evocative of the purpose

For modules, the name will be used as the directory
name inside the existing project.

Use AskUserQuestion to ask the user to pick one or
suggest their own.
Do NOT proceed until a name is confirmed.

#### 1c — Choose a license (project only)

**Skip this step for modules.**

Use AskUserQuestion to ask the user which license
to use. Suggest:

- **Apache-2.0** (default)
- **MIT**

The user may also specify a different license.
If the user has no preference, use Apache-2.0.

#### 1d — Create the plan

Now that requirements are clear, create the tasks
listed in the Plan section above (project-mode or
module-mode) using TaskCreate.

### Phase 2 — Scaffold

Mark the scaffold task `in_progress`.

#### When a base was provided

1. Read the base directory's structure (manifest
   files, source layout, configuration).
2. Identify the **tech stack**, **build setup**,
   **dependency list**, and **code patterns**
   (naming conventions, directory layout, shared
   utilities, framework idioms).
3. Note what should be **kept as-is** (build config,
   shared dependencies, structural conventions) vs.
   what should be **adapted** (module-specific names,
   business logic, endpoints, routes).
4. Copy the base directory structure into the new
   location, then adapt it:
   - Rename packages, namespaces, and identifiers
     to match the chosen name.
   - Replace business logic with starter code that
     matches the new objective.
   - Keep build configuration, shared dependencies,
     and structural conventions from the base.
   - Remove base-specific tests and replace with
     placeholder tests for the new module.

#### When no base was provided

If the tech stack matches one of the scaffolding
references, follow its instructions. If no reference
matches, skip scaffolding.

Pick the matching file from
[references/](references/):

- [java-spring-boot.md](references/java-spring-boot.md)
- [nodejs-typescript.md](references/nodejs-typescript.md)
- [python.md](references/python.md)
- [go.md](references/go.md)

Read **only** the matching file and apply its
instructions.

#### Entry point

After scaffolding (with or without a base), generate
the application entry point (e.g. main class,
`main.py`, `main.go`, etc.) with working starter
code that matches the objective and tech stack.

Mark the scaffold task `completed`.

### Phase 3 — Apply best practices

Mark the best-practices task `in_progress`.

Before generating any source file, check which
coding-rules skills are available in the current
session (they appear in the system-reminder skill
list). Invoke each applicable skill so its rules
are loaded, then apply them to all generated source
code. At a minimum, apply any language-agnostic
rules skill and any skill matching the project's
language or framework.

Mark the best-practices task `completed`.

### Phase 4 — Generate documentation (project only)

**Skip this entire phase for modules.**

#### 4a — Generate README.md

Mark the README task `in_progress`.

Before generating files, check for an existing
`README.md` — ask the user before overwriting.

Delegate README generation to the **write-readme**
skill by invoking it with the Skill tool. The skill
will scan the scaffolded project, gather any missing
context from the user, and produce a polished README.

Do NOT generate README.md manually — let write-readme
handle it entirely.

Mark the README task `completed`.

#### 4b — Generate CLAUDE.md

Mark the CLAUDE.md task `in_progress`.

Read the template at
[assets/CLAUDE.md](assets/CLAUDE.md).
Write `./CLAUDE.md` by filling in each
`{{placeholder}}` with project-specific content.
Keep the file **short and essential** (~40-60 lines
max). Remove any section whose placeholder has
nothing useful to say. The **Agents section is
mandatory** — never remove it.

Reference:
https://code.claude.com/docs/en/best-practices

Mark the CLAUDE.md task `completed`.

#### 4c — Generate LICENSE

Mark the LICENSE task `in_progress`.

Write `./LICENSE` with the full text of the license
chosen in phase 1. Use the current year and the
user's name (from git config) for the copyright
notice.

Reference:
https://choosealicense.com/licenses/

Mark the LICENSE task `completed`.

### Phase 5 — Review and confirm

Mark the review task `in_progress`.

Show all generated files to the user for review.
Ask if anything needs adjustment before finalizing.

Mark the review task `completed`.

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
- **Sequential phases** — complete each phase before
  moving to the next. Do not generate files before
  the user has confirmed the objective and name.
- **Module mode** — when creating a module, skip
  phases marked "project only". Only scaffold the
  code and apply best practices. The module inherits
  the parent project's documentation and
  configuration.
- **Base mode** — when an existing directory is
  used as a base, preserve its conventions
  (build config, dependencies, directory layout)
  and adapt only names and business logic.
  Do not mix scaffolding references with a base —
  the base takes precedence.
