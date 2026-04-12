---
name: general-rules
description: >-
  Language-agnostic engineering rules: best
  practices and conventions that apply to any
  project. Covers containers, CI/CD, security,
  and operational concerns. Use this skill to
  influence how infrastructure and cross-cutting
  code is written or reviewed.
allowed-tools: Read
---

# General Rules

Language-agnostic best practices and conventions
that apply to any project. Read the relevant
references to apply these rules when writing,
reviewing, or refactoring code.

## Domains

- [Containers](references/containers.md) —
  Dockerfile best practices, image size, security,
  layer caching
- [GitHub Actions](references/github-actions.md) —
  workflow structure, caching, multi-arch images

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **If context7 is available**, use it to verify
  current API and tool versions before adding or
  modifying dependencies.
