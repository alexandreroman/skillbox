# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog][keepachangelog], and this
project adheres to [Semantic Versioning][semver].

[keepachangelog]: https://keepachangelog.com/en/1.1.0/
[semver]: https://semver.org/spec/v2.0.0.html

## [Unreleased]

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
- Stop naming agent-harness tools in skill and agent content.
  Skills now state the intent — ask the user, invoke a skill,
  delegate to an agent, track the plan — and leave the tool
  choice to the coding agent.

### Removed

- The stale `allowed-tools` lists on `init-project` and
  `write-readme`. Both orchestrate a full bootstrap — asking,
  reading, writing, delegating, tracking — and neither list
  covered what the skill actually does.

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
