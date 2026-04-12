# Docker Compose

Best practices for writing production-grade
`compose.yaml` files.

## Health checks

Every application service **must** declare a
`healthcheck` block. Use the following defaults
unless the service has specific requirements:

```yaml
healthcheck:
  test: ["CMD-SHELL", "<probe command>"]
  interval: 10s
  timeout: 10s
  retries: 3
```

Choose the probe command based on the service:

- **HTTP endpoint available** — use
  `curl -sf http://localhost:<port>/<path>`.
- **gRPC / CLI tool available** — use the
  service's own CLI
  (e.g., `temporal operator cluster health`).
- **TCP-only** — use
  `nc -z localhost <port>` or an equivalent.

Infrastructure services that pull a public image
(Prometheus, Grafana, etc.) may omit the
healthcheck when no simple probe command exists,
but prefer adding one when possible.

## Service dependencies

Never use a bare `depends_on`:

```yaml
# bad
depends_on:
  - database
```

Always require the dependency to be healthy:

```yaml
# good
depends_on:
  database:
    condition: service_healthy
```

This guarantees ordered startup and avoids race
conditions where a service starts before its
dependency is ready.

## Restart policy

Application services — those with a `build:` key —
**must** set `restart: on-failure` so that Compose
restarts them after a crash without creating an
infinite restart loop on misconfiguration.

Infrastructure services using public images
typically rely on their own defaults and do not
need an explicit restart policy.

## Volumes

Mount configuration files in **read-only** mode
to prevent the container from accidentally
modifying them:

```yaml
volumes:
  - ./config/app.yaml:/etc/app/config.yaml:ro
```

Reserve writable mounts for directories where the
service must persist data (databases, caches, logs).
