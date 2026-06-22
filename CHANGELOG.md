# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog][keepachangelog], and this
project adheres to [Semantic Versioning][semver].

[keepachangelog]: https://keepachangelog.com/en/1.1.0/
[semver]: https://semver.org/spec/v2.0.0.html

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

[0.4.2]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.2
[0.4.1]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.1
[0.4.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.4.0
[0.3.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.3.0
[0.2.1]: https://github.com/alexandreroman/skillbox/releases/tag/v0.2.1
[0.2.0]: https://github.com/alexandreroman/skillbox/releases/tag/v0.2.0
