---
name: general-rules
description: >-
  Language-agnostic engineering rules: best
  practices and conventions that apply to any
  project. Covers containers, CI/CD, Git and
  commit conventions, security, and operational
  concerns. Consult this skill when designing,
  planning, or researching best practices for
  infrastructure and cross-cutting concerns — even
  for familiar tools — and when writing or reviewing
  such code. Invoke it before external web search;
  these rules are the project's authoritative
  conventions.
allowed-tools: Read
---

# General Rules

Language-agnostic best practices and conventions
that apply to any project. Read the relevant
references to apply these rules when designing,
researching best practices, writing, reviewing, or
refactoring code.

## Domains

- [Compose](references/compose.md) —
  Docker Compose health checks, dependencies,
  restart policy, read-only volumes, multi-file
  overlays (dev overlay vs. auto-merged
  `compose.override.yaml`), and host-port overrides
  with `!override`
- [Containers](references/containers.md) —
  Dockerfile best practices, image size, security,
  layer caching
- [Git](references/git.md) —
  commit message formatting (verb + action,
  imperative mood)
- [Hot Reload](references/hot-reload.md) —
  every executable component needs a
  technology-native hot-reload dev command
- [GitHub Actions](references/github-actions.md) —
  workflow structure, caching, multi-arch images
- [HTTP Servers](references/http-servers.md) —
  port configuration via `PORT` env var, bind
  address, framework defaults
- [Markdown Tables](references/markdown-tables.md) —
  column alignment rules and validation script

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **Consult these rules before external research.**
  They are the project's authoritative conventions;
  reach for web search only after checking them.
- **If context7 is available**, use it to verify
  current API and tool versions before adding or
  modifying dependencies.
