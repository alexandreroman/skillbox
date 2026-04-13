# Containers

Node.js / TypeScript additions to the
language-agnostic container rules defined in
`general-rules`.

## Activate pnpm via Corepack

Enable the exact pnpm version declared in
`package.json`:

```dockerfile
RUN corepack enable && corepack prepare
```

## Layer caching

Copy dependency manifests **before** source
code so that a code-only change does not
invalidate the install layer:

```dockerfile
COPY package.json pnpm-lock.yaml .npmrc ./
RUN pnpm install --frozen-lockfile
```

## Strip dev dependencies

Use `--ignore-scripts` when pruning — lifecycle
scripts such as `prepare` (Husky) will fail
after their own package has been removed:

```dockerfile
RUN pnpm prune --prod --ignore-scripts
```

## Multi-stage example

```dockerfile
# — builder stage —
FROM node:24-alpine AS builder
WORKDIR /app

RUN corepack enable && corepack prepare

COPY package.json pnpm-lock.yaml .npmrc ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm prune --prod --ignore-scripts

# — runtime stage —
FROM node:24-alpine
WORKDIR /app

RUN addgroup --system app \
 && adduser --system --ingroup app app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER app:app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```
