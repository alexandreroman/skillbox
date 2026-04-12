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
RUN npm ci --production
COPY src/ ./src/
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
  (e.g., `node:22-alpine`), not `:latest`, to
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

## Health checks

Expose a health endpoint in the application and
declare a `HEALTHCHECK` instruction or Kubernetes
liveness/readiness probes so the orchestrator can
detect unhealthy containers.
