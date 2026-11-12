# Containers

Node.js / TypeScript additions to the
language-agnostic container rules defined in
`general/containers.md`.

## Install pnpm with npm

Node.js 25+ no longer bundles Corepack: install
pnpm with npm. By default, pnpm then switches to
the version pinned in the `packageManager` field
of `package.json`.
Copy the manifests before installing dependencies
so a code-only change does not invalidate the
install layer.

```dockerfile
RUN npm install -g pnpm
COPY package.json pnpm-lock.yaml ./
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
FROM node:26-alpine AS builder
WORKDIR /app

RUN npm install -g pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm prune --prod --ignore-scripts

# — runtime stage —
FROM node:26-alpine
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
