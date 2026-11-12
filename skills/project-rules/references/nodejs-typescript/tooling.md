# Tooling

Tool choices and non-obvious configuration for
Node.js / TypeScript projects.

## Package Manager — pnpm

Use **pnpm** as the package manager.

## Web Framework — Vite + Nuxt

Preferred option for web front ends: **Vite + Nuxt**.
Confirm the framework choice when the request
does not state it.

## Dev Runner — tsx

Hot reload uses Node's built-in `--watch`, with
`--env-file` and `--import tsx/esm`:

```json
"dev": "node --watch --env-file=.env --import tsx/esm src/index.ts"
```

## Testing — Vitest

Use **Vitest** with `@vitest/coverage-v8`.
Enable `globals: true` in config.

## Environment — Zod + t3-env

Use **@t3-oss/env-core** with **Zod** for typed,
validated environment variables (`src/env.ts`).

## Git Hooks — Husky + lint-staged

- **pre-commit**: `pnpm exec lint-staged`
- **pre-push**: `pnpm typecheck`

## Project Structure

```text
src/
  features/       # feature-based modules
  shared/         # shared utilities
  types/          # global types
```
