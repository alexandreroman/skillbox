# Docker Compose

Best practices for writing production-grade
`compose.yaml` files.

## Filename

Always name the Compose file `compose.yaml`.
Do not use `docker-compose.yml` or
`docker-compose.yaml` — those are legacy names
predating the Compose Specification. Modern
Docker tooling discovers `compose.yaml` by
default, so prefer it everywhere: new projects,
generated examples, documentation snippets, and
references in CI workflows or READMEs.

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

## Multiple Compose files

`docker compose` supports layering overlays on top
of the base `compose.yaml`. Two naming rules drive
completely different behaviour, so choose the name
deliberately:

- **`compose.override.yaml`** is **auto-merged**.
  A plain `docker compose up` reads it on top of
  `compose.yaml` with no `-f` flag. Reserve it for
  machine-specific or ephemeral changes that should
  apply by default (e.g. remapping published host
  ports — see below).
- **Any other name** (e.g. `compose.dev.yaml`) is
  **not** auto-merged. It must be passed explicitly:

  ```bash
  docker compose -f compose.yaml -f compose.dev.yaml up
  ```

  Use a named overlay for an **opt-in** mode so it
  stays off the default path: `docker compose up`
  keeps running the base stack untouched.

Later files win, and mappings are deep-merged.
Sequences (`ports`, `command`, `entrypoint`, …) are
**appended** by default — see the `!override` tag
below to replace them instead.

## Single entry point (reverse proxy)

Prefer publishing a **single** host port and
routing everything behind a reverse proxy
(Caddy, nginx, Traefik, an Ingress — the choice is
yours). Internal services then use `expose` instead
of `ports`, so only the proxy is reachable from the
host and there is one URL to remember. This is a
convention, not a hard rule: a single-service stack
needs no proxy.

The pattern composes with the dev overlay below:
keep the proxy **containerised in both modes** and,
in dev, have it route to the host-side process via
`host.docker.internal` instead of the in-network
service name — so the published entry point stays
identical whether a given service runs in a
container or on the host.

## Dev overlay (hot-reload inner loop)

For a fast inner loop, keep the full containerised
stack in `compose.yaml` (run it as-is for an
integration/prod-like run) and add a named
`compose.dev.yaml` overlay that runs the service
under active development **on the host** with
hot reload, while its dependencies stay in
containers. Name it `compose.dev.yaml` (not
`compose.override.yaml`) so the container-only path
stays the default and the dev route is explicit.

When a containerised service must reach a process
running on the host (e.g. the container-side gateway
proxying to a host-side API), dial the special DNS
name `host.docker.internal` and declare it on the
container:

```yaml
services:
  gateway:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      API_UPSTREAM: "host.docker.internal:${API_PORT:-8020}"
```

`host.docker.internal` resolves natively on macOS
and Windows (Docker Desktop); the
`host.docker.internal:host-gateway` entry makes it
resolve on Linux too.

## Overriding published ports

To run several checkouts or Git worktrees of the
same project at once, remap the **published host
ports** so parallel instances never collide. Emit a
`compose.override.yaml` that offsets every published
port from a per-instance base port. Because it is
auto-merged, `docker compose` picks it up with no
extra flag.

Use the `!override` tag to **replace** a sequence
instead of appending to it:

```yaml
services:
  gateway:
    ports: !override
      - "18080:8080"
```

Without `!override`, Compose appends: both the base
`8080:8080` and the remapped `18080:8080` would be
published. `!override` replaces the whole list so
only the remapped port binds.

Treat the override file as the **source of truth**
for what is actually published: when it exists, read
the effective host ports back from it (in scripts,
Makefiles, or banners) rather than assuming the
defaults, so tooling never diverges from what Docker
actually binds.
