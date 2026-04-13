# Containers

Language-agnostic best practices for building
production container images. Language-specific
skills (e.g., `java-rules`, `spring-boot-rules`)
extend these rules with their own additions.

## Image size

- **Use minimal base images** — prefer Alpine,
  distroless, or slim variants over full OS images.
- **Multi-stage builds** — compile and package in a
  builder stage, copy only the runtime artifacts
  into the final stage.
- **Remove caches and temp files** in the same
  `RUN` layer that creates them so they do not
  bloat the image.

```dockerfile
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*
```

## Layer caching

- **Order instructions from least to most
  frequently changing** — OS packages first,
  dependency install next, application code last.
- **Copy dependency manifests before source code**
  so that a source-only change does not invalidate
  the dependency-install layer.

```dockerfile
COPY package.json package-lock.json ./
RUN npm ci
COPY src/ ./src/
```

When using **corepack** (Node.js), the manifest
must be present before `corepack prepare` runs —
it reads the `packageManager` field from
`package.json`:

```dockerfile
COPY package.json pnpm-lock.yaml .npmrc ./
RUN corepack enable && corepack prepare
RUN pnpm install --frozen-lockfile
```

## Security

- **Non-root user** — create a dedicated `app` user
  and group, and run the application as `app:app`.

```dockerfile
RUN addgroup --system app \
 && adduser --system --ingroup app app
USER app:app
```

- **No secrets in the image** — pass credentials
  via environment variables or mounted secrets at
  runtime, never bake them into layers.
- **Pin image tags** — use a specific version tag
  (e.g., `node:24-alpine`), not `:latest`, to
  ensure reproducible builds.
- **Scan images** — integrate a vulnerability
  scanner (Trivy, Grype, Snyk) into the CI
  pipeline.

## `.dockerignore`

Always include a `.dockerignore` to keep the
build context small and avoid leaking sensitive
files:

```text
.git
.env
*.md
```

Add language-specific exclusions (e.g., `node_modules/`,
`target/`, `__pycache__/`) as needed.

## Signal handling (PID 1)

A container's entry-point process runs as PID 1.
Under Linux, PID 1 does **not** receive default
signal handlers — `SIGINT` and `SIGTERM` are
silently ignored unless the process explicitly
handles them. This means `Ctrl+C` and
`docker stop` have no effect.

**Use a lightweight init** such as
[`tini`](https://github.com/krallin/tini) as the
`ENTRYPOINT`. It forwards signals to child
processes and reaps zombies:

```dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/index.js"]
```

Alternatively, pass `--init` to `docker run`, but
an in-image init is preferred so the behaviour is
portable across orchestrators.

## Health checks

Expose a health endpoint in the application and
declare a `HEALTHCHECK` instruction or Kubernetes
liveness/readiness probes so the orchestrator can
detect unhealthy containers.
