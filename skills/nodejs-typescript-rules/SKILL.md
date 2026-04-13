---
name: nodejs-typescript-rules
description: >-
  Node.js / TypeScript coding rules: tooling choices,
  TypeScript strict config, ESLint v9 flat config,
  Prettier preferences. Use this skill to influence
  how Node.js / TypeScript code is written, reviewed,
  or refactored.
allowed-tools: Read
---

# Node.js / TypeScript Rules

Opinionated choices and non-trivial configurations
for modern Node.js / TypeScript projects. Read the
relevant references to apply these rules when
writing, reviewing, or refactoring code.

## Domains

- [Tooling](references/tooling.md) —
  pnpm, tsx, Vitest, Husky, Zod + t3-env,
  project structure
- [Containers](references/containers.md) —
  Dockerfile with pnpm, Corepack, multi-stage
  builds, dev-dependency pruning
- [TypeScript](references/typescript.md) —
  strict ESM-first tsconfig.json
- [Code quality](references/code-quality.md) —
  ESLint v9 flat config, Prettier preferences,
  lint-staged globs

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **Prefer standard APIs** over third-party
  libraries when Node.js or the Web Platform
  provides an equivalent.
- **Use pnpm** — see
  [Tooling](references/tooling.md) for details.
- **If context7 is available**, use it to verify
  current API and tool versions before adding or
  modifying dependencies.
