# Containers

Language-agnostic best practices for building
production container images. Language-specific
sections (e.g., `java/containers.md`,
`spring-boot/containers.md`) extend these rules
with their own additions.

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
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY src/ ./src/
```

## BuildKit cache mounts

`--mount=type=cache` persists dependency and build
caches across image builds (package-manager
downloads, compiler caches). Each language's
`containers.md` gives the concrete mount targets.

- **Always set an explicit `id`** on each cache
  mount, and reuse the same `id` across every `RUN`
  that mounts it. Beyond sharing the volume, an
  `id`-less mount can misbehave under podman/buildah:
  at best you get silent cache misses, and for Go it
  breaks `go build` module resolution outright
  (`no required module provides package …` even
  though `go mod download` populated the cache).

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
  (e.g., `node:26-alpine`), not `:latest`, to
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
Under Linux, PID 1 gets **no default signal
actions**: `SIGINT` and `SIGTERM` are ignored unless
the process installs a handler, so `Ctrl+C` and
`docker stop` have no effect. PID 1 must also reap
orphaned child processes (zombies).

**Use a lightweight init** such as
[`tini`](https://github.com/krallin/tini) as the
`ENTRYPOINT` when the process does not handle
signals or reap children itself (e.g. Node.js, a
shell script). It forwards signals and reaps
zombies:

```dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/index.js"]
```

A process that handles `SIGTERM` and spawns no
children (a Go binary, the JVM) runs directly as
PID 1, with no init. Prefer an in-image init over
`docker run --init` so the behaviour is portable
across orchestrators.

## Health checks

Expose a health endpoint in the application and
declare a `HEALTHCHECK` instruction or Kubernetes
liveness/readiness probes so the orchestrator can
detect unhealthy containers.
