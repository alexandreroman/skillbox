# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog][keepachangelog], and this
project adheres to [Semantic Versioning][semver].

[keepachangelog]: https://keepachangelog.com/en/1.1.0/
[semver]: https://semver.org/spec/v2.0.0.html

## [0.7.0] - 2026-11-12

### Added

- A "Dependency Injection — uber-go/fx" reference to the
  `project-rules` Go section, recommending fx for projects with a
  large volume of components: the threshold for adopting it over
  hand wiring, per-package `fx.Module` layout, `slog` event
  logging, and a `fx.ValidateApp` guard against runtime wiring
  errors.
- A "Generic Methods (Go 1.27+)" section to the `project-rules` Go
  modern-syntax reference: type parameters on concrete methods,
  when to prefer a method over a package-level generic function,
  method expressions, and the standing ban on generic interface
  methods.
- A Python section in `project-rules`: `uv` for environments and
  dependencies, `ruff` for lint and format, `pytest` for tests,
  `watchfiles` for generic reload, and per-framework hot reload,
  with `fastapi dev` kept for FastAPI even when its CLI must be
  added first. The conventions now live with the rules, not in
  the scaffold.
- A "latest stable version" rule under "Always applies" in
  `project-rules`: new dependencies and tools are pinned to the
  latest stable release instead of a remembered version.
- An integration mode in `init-project` for adopting an existing
  repository: it adds the missing conventions without regenerating
  files that already exist, and seeds the project memory with a
  summary of the project that the user confirms.
- Safeguards in `init-project`: it stops before scaffolding when
  the project memory cannot be written, always asks for the Go
  module owner instead of guessing it, never checks the Claude
  Code version, and asks closed questions as multiple choice.
- Tests for `check_tables.py` in `tests/`, covering every case
  fixed below.

### Changed

- Update the `README.md` skill lists to match the current skills
  and add a section on `AGENTS.md`, the shared instruction file.
- Make `init-project` the only user-invocable skill.
  `project-memory` and `write-readme` are now model-only: the
  agent loads them when needed, so they no longer clutter the
  slash-command list.
- Move the Makefile rule and its template from `init-project` to
  `project-rules`, so the rule applies to any project and not only
  to new ones. Go projects now build on Make and Task is dropped;
  Air is run through `go tool` rather than a separate install.
- Move the Compose/Temporal rule and the `compose.temporal.yaml`
  template from `init-project` to `project-rules`, for the same
  reason.
- Prefer Vite and Nuxt in the Node rules, and fix the pnpm-only
  guidance so that no `npm` or `npx` command is suggested.
- Slim down the `init-project` scaffolds (Go, Java, Node, Python):
  conventions already stated in `project-rules` are no longer
  repeated, which removes the risk of the two copies drifting.
  This covers the `golangci` `gosimple` linter, `go install`, the
  `.air.toml` file, `npm init` and `npx`, and the ECS logging
  block.
- Rename the `init-project` instruction template from
  `CLAUDE.md` to `AGENTS.md`. It imports the memory index with
  `@.claude/project-memory/MEMORY.md`, so the memory loads on
  startup.
- State each `project-memory` rule once (the conflict rule and
  the English rule were repeated) and add a rule for subagents:
  on a conflict or a duplicate they write nothing and report it
  to the caller, since they cannot reach the user.
- Restrict `code-reviewer` to read and search tools, with the
  skills it needs preloaded. Alignment checks are done by reading
  the files rather than by running a script, and a missing or
  diverging Makefile is reported as a minor finding.
- Have the agents return open questions to the caller instead of
  asking the user directly. `code-writer` adds a Makefile only
  when asked; when editing one, it adds the missing standard
  targets and keeps the project's own.
- Slim down `init-project` itself (491 to 345 lines): the
  Makefile and Compose phases point to the rules, rules already
  stated by a phase are no longer repeated, the plan is one rule
  instead of task lists, and the integration mode moves to
  `references/integration.md`, loaded only in that mode.
- Narrow the `gh` permissions in `.claude/settings.json` to
  read-only commands and `gh pr create`.
- Rename this repository's `CLAUDE.md` to `AGENTS.md`.
- Trim what every session loads: each rule is now stated once
  across `write-readme`, `project-memory`, `project-rules`,
  `init-project` and the Compose and container references, and
  the `project-rules` and `project-memory` descriptions are
  shorter. `project-rules` no longer repeats per-stack key rules
  that its references already state, and `write-readme` gains
  explicit "Use when" triggers.
- Document the `tests/` folder and its command in `README.md` and
  `AGENTS.md`, mention Python in the skill list, and note in
  `AGENTS.md` that `user-invocable` is the one Claude Code field
  allowed beyond the Agent Skills spec.

### Removed

- The `infra-logs` and `app-logs` targets from the `init-project`
  Makefile template. Following container logs is a one-off
  troubleshooting step, not a task worth a dedicated target;
  `infra-logs` is also dropped from `DEV_TARGETS`.
- The generated `CLAUDE.md` from `init-project`: `AGENTS.md` is
  the single instruction file.
- Task as the Go task runner; Go projects use Make.
- `project-memory/references/guidelines.md`, whose remaining
  rules moved into the skill itself; the stale "Variables" tables
  of the `init-project` stack references; the `.npmrc` block that
  only restated pnpm defaults; and the default `skills` path in
  `plugin.json`.

### Fixed

- `check_tables.py` now reports every misaligned file instead of
  stopping at the first, ignores tables inside fenced code
  blocks, checks indented tables, handles escaped pipes (`\|`)
  inside cells, and reports a missing file as an error rather
  than crashing.
- Fit the Spring Boot reference tables (Boot 4 migration, test
  slice packages, visibility) within the 80-column limit:
  common prefixes are stated once, and renames too long for a
  two-column table are listed instead.
- Container examples that did not build or did not do what they
  claimed: the Java Dockerfile now copies the Maven Wrapper, and
  the Spring Boot runtime image copies each extracted layer
  separately so dependency layers stay cached.
- Compose health checks no longer require a shell and `curl`,
  which distroless images lack, and an init process (tini) is
  required only where the process does not handle signals.
- The Makefile rule now says to drop the `infra-up` prerequisite
  of `dev` along with the Infra section, and never to leave the
  infrastructure service list empty.
- Contradictions in the rules: the golangci-lint example no longer
  lists linters already in the `standard` set, Node.js hot reload
  is stated once, the Java line-wrapping rule matches its example,
  and the last `npm` commands become `pnpm` ones.
- `init-project` no longer generates the Makefile twice (once per
  stack reference, once in phase 4a) and no longer asks twice
  before overwriting a README.
- Image and action versions follow the latest-stable rule: the
  Temporal dev server is pinned to `1.10.0` instead of `:latest`,
  Node.js images use `node:26-alpine` and install pnpm with npm
  (Node.js 25+ no longer ships Corepack), and the GitHub Actions
  examples use `checkout@v7` and `build-push-action@v7`.
- `project-memory` sends a project's workflow preferences to the
  project memory, in line with the generated `AGENTS.md`, and its
  `allowed-tools` field is space-separated, as the Agent Skills
  spec requires.

## [0.6.0] - 2026-08-27

### Changed

- Front-load project context in `init-project`. A new
  "Establish project context" phase runs right after the
  requirements interview and before any file is scaffolded: it
  writes a bootstrap `CLAUDE.md`, reads it back and adopts it as
  active instructions for the current session, opens the project
  memory through `project-memory` and records the founding
  decisions (objective, name, license, stack), then loads
  `project-rules` for the detected stack. Scaffolding is
  delegated to the `code-writer` agent from then on. `CLAUDE.md`
  is finalized at the end with the build commands and module
  list. Restarting the session is no longer needed for the
  project's own rules and memory to apply.
- Broaden the `code-reviewer` agent's default scope: it now
  reviews documentation and the project memory alongside the
  code, unless the user asks for a narrower perimeter. Stale,
  contradicted, or redundant memory entries are reported as
  findings; the agent stays read-only and never edits them.
- Make simplification and dead-code removal first-class review
  criteria for `code-reviewer`. It hunts for needless complexity
  (single-use abstractions, duplicated logic, speculative
  generality) and for dead code (unused symbols, unreachable
  branches, obsolete flags, unused dependencies), recommending
  deletion over refactoring and refactoring over addition.
- Drop the Java 25 upper bound from `project-rules`: the Java
  rules now target Java 21 and later, with version tags read as
  the release that introduced a feature rather than a maximum.
  `init-project` picks the most recent Java release offered by
  Spring Initializr instead of hardcoding 25.
- Stop naming agent-harness tools in skill and agent content.
  Skills now state the intent — ask the user, invoke a skill,
  delegate to an agent, track the plan — and leave the tool
  choice to the coding agent.

### Removed

- The stale `allowed-tools` lists on `init-project` and
  `write-readme`. Both orchestrate a full bootstrap — asking,
  reading, writing, delegating, tracking — and neither list
  covered what the skill actually does.

## [0.5.0] - 2026-08-27

### Changed

- Merge the five convention skills (`general-rules`, `go-rules`,
  `java-rules`, `nodejs-typescript-rules`, `spring-boot-rules`)
  into a single `project-rules` skill. Its `SKILL.md` carries a
  stack-detection table and routes to `references/<stack>/`, so a
  project reads the General section plus only the sections that
  match its language and framework. The reference files
  themselves are unchanged.
- Point the `code-writer` and `code-reviewer` agents and the
  `init-project` skill at `project-rules` instead of enumerating
  the per-language skills.
- Make `project-memory` the single authority on memory. The
  `code-writer` and `code-reviewer` agents no longer decide for
  themselves what to persist or how to store it; they recall and
  save only through the skill, following its own trigger rules.

### Removed

- The `general-rules`, `go-rules`, `java-rules`,
  `nodejs-typescript-rules`, and `spring-boot-rules` skills.
  Their references now live under
  `skills/project-rules/references/`, and
  `check_tables.py` under `skills/project-rules/scripts/`.
- The per-agent memory directory
  `<project root>/.claude/agent-memory/<agent-name>/`. The main
  conversation and subagents now share
  `<project root>/.claude/project-memory/`.

## [0.4.5] - 2026-07-27

### Changed

- Mark the convention skills (`general-rules`, `go-rules`,
  `java-rules`, `nodejs-typescript-rules`, `spring-boot-rules`)
  as `user-invocable: false`. They carry coding rules rather
  than actions, so they no longer appear as slash commands;
  Claude still loads them automatically when relevant.

## [0.4.4] - 2026-07-21

### Added

- Document Compose multi-file overlays in `general-rules`: a dev
  overlay for the hot-reload inner loop, an auto-merged
  `compose.override.yaml` for host-port remapping via `!override`,
  and a tool-agnostic single-entry-point reverse-proxy note.

## [0.4.3] - 2026-07-13

### Changed

- Require an explicit `id` on every BuildKit cache mount. An
  `id`-less `--mount=type=cache` misbehaves under podman/buildah
  (silent cache misses, and for Go a hard `go build` module
  resolution failure). Documented in `general-rules` and
  `go-rules`.

## [0.4.2] - 2026-06-22

### Changed

- Trigger rules skills at design and research time, not only when
  writing code.

## [0.4.1] - 2026-06-10

### Changed

- Require a hot-reload dev command for executable components.
- Wrap the `init-project` dev target in a trap to avoid orphan
  processes.
- Clarify and promote the `reference` memory type in `project-memory`.
- Require present-tense facts in project memory entries.

## [0.4.0] - 2026-06-04

### Added

- Add documentation review to the `code-reviewer` agent scope.
- Add a Temporal Compose service rule to `init-project`.
- Add commit message conventions to `general-rules`.
- Generate a `Makefile` when scaffolding projects.

### Changed

- Make agent memory generic instead of per-agent.
- Emphasize readable over clever code in `code-writer`.
- Make `code-reviewer` validate Markdown table alignment.

### Fixed

- Fix a misaligned table in the `write-readme` guide.

### Removed

- Remove the stale `java-best-practices` worktree and ignore
  worktrees.

## [0.3.0] - 2026-05-14

### Added

- Add the `go-rules` skill with Go 1.21+ best practices.

## [0.2.1] - 2026-05-06

### Changed

- Document BuildKit cache mounts for Maven and Gradle.

### Removed

- Remove worktree isolation from agents.
- Remove the compound shell commands rule from the `init-project`
  template.

## [0.2.0] - 2026-05-05

### Added

- Initial release of the skillbox plugin.
- `init-project` skill for interactive project scaffolding with
  README, `CLAUDE.md`, and license generation.
- `write-readme` skill for generating GitHub-ready README files.
- `general-rules` skill covering containers, CI/CD, security, and
  operations.
- `java-rules` and `spring-boot-rules` skills for modern Java and
  Spring Boot.
- `nodejs-typescript-rules` skill with Vite + Nuxt scaffolding.
- `project-memory` skill to persist decisions, deadlines, and team
  context.
- `code-writer` and `code-reviewer` agents with opinionated
  best-practice defaults.

[0.7.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.7.0
[0.6.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.6.0
[0.5.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.5.0
[0.4.5]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.5
[0.4.4]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.4
[0.4.3]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.3
[0.4.2]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.2
[0.4.1]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.1
[0.4.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.0
[0.3.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.3.0
[0.2.1]: https://github.com/alexandreroman/skillbox/releases/tag/v0.2.1
[0.2.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.2.0
