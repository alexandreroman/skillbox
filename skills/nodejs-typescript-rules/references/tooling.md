# Tooling

Tool choices and non-obvious configuration for
Node.js / TypeScript projects.

## Package Manager — pnpm

`.npmrc`:

```ini
shamefully-hoist=false
strict-peer-dependencies=false
```

## Dev Runner — tsx

Use `--env-file` with `--import` for development:

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

- **pre-commit**: `npx lint-staged`
- **pre-push**: `pnpm typecheck`

## Docker — pnpm + corepack

When using corepack in a Dockerfile, **copy
`package.json` before running `corepack prepare`**
— it reads the `packageManager` field from
`package.json` and fails without it.

```dockerfile
COPY package.json pnpm-lock.yaml .npmrc ./
RUN corepack enable && corepack prepare
RUN pnpm install --frozen-lockfile
```

When pruning dev dependencies in a Docker build
stage, always use `--ignore-scripts` to prevent
lifecycle hooks (e.g., Husky `prepare`) from
failing after their own packages are removed:

```dockerfile
RUN pnpm prune --prod --ignore-scripts
```

## Project Structure

```text
src/
  features/       # feature-based modules
  shared/         # shared utilities
  types/          # global types
```
