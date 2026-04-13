# Containers

Node.js / TypeScript additions to the
language-agnostic container rules defined in
`general-rules`.

## Activate pnpm via Corepack

Copy `package.json` **before** running
`corepack prepare` — it reads the
`packageManager` field and fails without it.
This also enables layer caching: a code-only
change does not invalidate the install layer.

```dockerfile
COPY package.json pnpm-lock.yaml .npmrc ./
RUN corepack enable && corepack prepare
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

COPY package.json pnpm-lock.yaml .npmrc ./
RUN corepack enable && corepack prepare
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm prune --prod --ignore-scripts

# — runtime stage —
FROM node:24-alpine
WORKDIR /app

RUN apk add --no-cache tini \
 && addgroup --system app \
 && adduser --system --ingroup app app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER app:app
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/index.js"]
```
