---
name: init-project
description: >-
  Use when starting a new project, bootstrapping an
  empty repository, adding a new module to an existing
  project, or adopting skillbox in an existing
  repository ("adopt skillbox", "set up Claude Code in
  this repo"). Interactively gathers the objective and
  name, then generates or completes the files so Claude
  Code has proper context from day one.
---

# Initialize Project

Bootstrap a new project or module by gathering
requirements from the user, then generating
foundational files.

## Modes

This skill operates in one of three modes, determined
during the requirements phase:

| Mode            | Scope                                      |
| --------------- | ------------------------------------------ |
| **Project**     | Top-level repository — full scaffold       |
| **Module**      | Sub-directory inside existing project      |
| **Integration** | Existing repository adopting skillbox      |

A **base directory** can optionally be specified in
either mode. When provided, the base replaces the
generic scaffolding references and is used as a
template for the new project or module.

## Plan

After gathering requirements (phase 1), create a
tracked plan so the user can follow progress: one task
per phase from 2 to 6, in order, with phase 5 split into
its three steps (README, LICENSE, AGENTS.md). Module
mode skips the phases marked "project only", which
leaves context, scaffold, and review. Integration mode
uses the plan in
[references/integration.md](references/integration.md).

Mark each task `in_progress` when you start it and
`completed` when you finish it.

## Process

### Phase 1 — Gather requirements

This phase runs **before** the plan is created.

#### 1a — Understand the objective

Ask the user to describe the objective in a few
sentences:

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
directory already contains an `AGENTS.md` (or
`CLAUDE.md`) or a parent project manifest, this is
likely a module. Ask the user to confirm. If the user
explicitly says they want to create a module,
component, or sub-project, treat it as a module.

**Detecting integration mode:** if the current
directory is an existing project (sources present) and
the user does not ask for a new module, offer
integration mode and ask for confirmation. In that
mode, skip 1b and 1c, then follow "Integration mode"
below instead of phases 2 to 6.

Do NOT proceed until you have a clear answer.

#### 1b — Choose a name

Propose 3-5 short, memorable names based on the
objective. Names should be:

- Lowercase, kebab-case (e.g. `data-forge`)
- Easy to type and remember
- Evocative of the purpose

For modules, the name will be used as the directory
name inside the existing project.

Ask the user to pick one or suggest their own.
Do NOT proceed until a name is confirmed.

#### 1c — Choose a license (project only)

**Skip this step for modules.**

Ask the user which license to use. Suggest:

- **Apache-2.0** (default)
- **MIT**

The user may also specify a different license.
If the user has no preference, use Apache-2.0.

#### 1d — Create the plan

Now that requirements are clear, create the plan
described in the Plan section above for the detected
mode.

### Phase 2 — Establish project context

This phase runs **before a single project file is
written**. Its purpose is to make the project's own
instructions — `AGENTS.md`, the project memory, and the
project rules — active for the rest of *this* session.
Nothing here may be deferred to a session restart: the
instruction file is loaded at startup only, so the skill
must load and apply it itself.

#### 2a — Bootstrap AGENTS.md

**Project mode.** Read the template at
[assets/AGENTS.md](assets/AGENTS.md) and write
`./AGENTS.md` now, filling it with what phase 1 already
established: the project name, a one-sentence
description, and the tech stack when it is known.

- Copy the **Agents**, **Memory**, and **Conventions**
  sections as-is — they never depend on the scaffold.
  The **Memory** section imports the memory index
  (`@.claude/project-memory/MEMORY.md`).
- Omit **Build & run** and **Modules** for now; phase
  5c fills them in once the scaffold exists.
- Check for an existing `AGENTS.md` (or `CLAUDE.md`)
  first and ask the user before overwriting.
- Do **not** generate a `CLAUDE.md`: its presence makes
  Claude Code ignore `AGENTS.md`. Only for Claude Code
  older than 2.1.277, which does not read `AGENTS.md`,
  add a one-line `CLAUDE.md` containing `@AGENTS.md`.

**Module mode.** Do not write an instruction file. Read
the parent project's `AGENTS.md` (or `CLAUDE.md`) instead,
plus any closer one between the repository root and the
module directory.

#### 2b — Adopt AGENTS.md immediately

Read back the `AGENTS.md` that now governs the project
and treat its content as **active instructions for the
remainder of this session**, exactly as if it had been
loaded at startup. In particular, from phase 3 onwards:

- Delegate every source-file write, edit, or refactor
  to the **code-writer** agent — never edit source
  files yourself. The skill writes only `AGENTS.md`,
  `LICENSE`, `Makefile`, and `compose.yaml`; the
  README goes to **write-readme**.
- Apply the conventions it states: line-length limits
  and Markdown formatting.

#### 2c — Open the project memory

Invoke the **project-memory** skill and follow its own
format and trigger rules. Do not invent a storage
layout.

- **Project mode** — it creates
  `.claude/project-memory/` and its `MEMORY.md`. Save
  the founding decisions from phase 1: the objective
  and target audience, the chosen name, the license,
  the tech stack and why it was picked, and any
  constraint the user stated. These are exactly the
  decisions that would otherwise be lost between
  sessions.
- **Module mode** — read the existing `MEMORY.md`
  before scaffolding so the module follows past
  decisions, then save the module's objective and
  where it sits in the project.

#### 2d — Load the project rules

Invoke the **project-rules** skill. Detect the stack
from the phase 1 answers in
project mode — the manifests do not exist yet — or
from the parent project's manifests in module mode.
Read the General section plus every section matching
the language and framework, then apply those rules to
everything generated from phase 3 onwards.

### Phase 3 — Scaffold

Per the `AGENTS.md` adopted in phase 2b, the
**code-writer** agent writes every source file created
in this phase. Hand it the objective, the chosen name,
the stack, and the layout decided below; it loads the
project rules and the project memory on its own.

#### When a base was provided

The base takes precedence: do not mix it with the
scaffolding references below. Read its manifests,
source layout, and code patterns, copy its structure
into the new location, then:

- **Keep** its build configuration, shared
  dependencies, and structural conventions.
- **Adapt** packages, namespaces, and identifiers to
  the chosen name, and replace business logic,
  endpoints, and routes with starter code for the new
  objective.
- **Replace** base-specific tests with placeholder
  tests.

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

### Phase 4 — Generate developer tooling (project only)

**Skip this entire phase for modules.** A module inherits
the parent project's tooling.

#### 4a — Generate the Makefile

Apply the project-rules rules in `references/general/makefile.md`
(see [project-rules](../project-rules/SKILL.md)), starting
from the template
[../project-rules/assets/Makefile](../project-rules/assets/Makefile).
Write `./Makefile` at the project root, filling every
`{{placeholder}}` for the detected tech stack.

#### 4b — Configure Compose infrastructure

If the app depends on infrastructure services (databases,
brokers, Temporal, object storage, ...), apply the
project-rules rules in `references/general/compose.md` and
create `compose.yaml` at the project root. For Temporal,
start from
[compose.temporal.yaml](../project-rules/assets/compose.temporal.yaml).
List the service names in the Makefile's
`{{infra-services}}`. Skip this step when the app has no
such dependencies.

### Phase 5 — Generate documentation (project only)

**Skip this entire phase for modules.**

#### 5a — Generate README.md

Before generating files, check for an existing
`README.md` — ask the user before overwriting.

Delegate README generation to the **write-readme**
skill. It scans the scaffolded project, gathers any
missing context from the user, and produces a polished
README.

Do NOT generate README.md manually — let write-readme
handle it entirely.

#### 5b — Generate LICENSE

Write `./LICENSE` with the full text of the license
chosen in phase 1. Use the current year and the
user's name (from git config) for the copyright
notice.

Reference:
https://choosealicense.com/licenses/

#### 5c — Finalize AGENTS.md

`AGENTS.md` already exists from phase 2a. Fill in the
`{{placeholder}}` sections that were left out because
the scaffold did not exist yet:

- **Tech stack** — confirm or correct it against what
  was actually generated.
- **Build & run** — the essential commands, taken from
  the generated `Makefile`.
- **Modules** — one bullet per module or top-level
  directory.

Keep the file **short and essential** (~40-60 lines
max). Remove any section whose placeholder still has
nothing useful to say. The **Agents** section (with
code-writer and code-reviewer) and the **Memory**
section (with the memory index import) are mandatory —
never remove them.

Reference:
https://code.claude.com/docs/en/best-practices

### Phase 6 — Review and confirm

Show all generated files to the user for review.
Ask if anything needs adjustment before finalizing.

## Integration mode

For an existing repository adopting skillbox. Read
[references/integration.md](references/integration.md)
and follow it: it adds only what is missing and never
rewrites existing content, so a second run changes
nothing.

## Rules

- **English only for generated files** — all content
  in README.md and AGENTS.md must be in English,
  regardless of the user's language.
- **Concise** — prefer references over inline
  documentation. Do not duplicate information between
  README.md and AGENTS.md; AGENTS.md should reference
  README.md rather than repeat it.
- **README.md reference is mandatory** in AGENTS.md —
  always link to README.md.
- **No secrets or paths** — do not include absolute
  paths, credentials, or environment-specific values.
