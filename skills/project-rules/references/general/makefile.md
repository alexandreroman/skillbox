# Makefile

Every project (not module) has a `Makefile` at its root as
the single, self-documenting entry point for common developer
tasks, whatever the stack, Go included. Modules inherit the
parent project's Makefile.

Build it from the template at
[../../assets/Makefile](../../assets/Makefile).

## Standard targets

| Target       | Meaning                                          |
| ------------ | ------------------------------------------------ |
| `help`       | List the targets; the default goal               |
| `dev`        | Run the app locally with hot reload, infra first |
| `infra-up`   | Start local infrastructure services              |
| `infra-down` | Stop local infrastructure services               |
| `app-up`     | Bring up the full stack in containers            |
| `app-down`   | Tear down the full stack                         |
| `test`       | Run the test suite                               |
| `check`      | Run tests and static checks                      |
| `build`      | Build the production artifact                    |

The `app-*` targets exist only when the project has a
compose file (see [compose.md](compose.md)); the `infra-*`
targets only when that file defines infrastructure
services.

## Adapt the template

Replace each `{{placeholder}}` with commands for the stack:

- `{{dev-command}}`: run the app locally with hot reload
  (e.g. `go tool air`, `pnpm dev`, `./mvnw spring-boot:run`;
  Python commands are in [../python/tooling.md](../python/tooling.md)).
  This is the headline `dev` target developers run day to
  day. It is wrapped in `trap 'kill 0' EXIT INT TERM` so
  Ctrl-C reaps the whole process group and leaves no
  orphans. Replace just the command; keep the surrounding
  `trap`, `&` and `wait`. When `dev` runs several processes,
  background each as `( cmd; kill 0 ) &` before the final
  `wait` so a crash of one tears down the rest.
- `{{compose}}`: the compose command (`docker compose` or
  `podman compose`), used by `app-up` / `app-down` and by
  `infra-up` / `infra-down`. Remove the **Stack** section
  if the project has no compose file.
- `{{infra-services}}`: the infrastructure services the app
  needs while running locally (e.g. `postgres redis`),
  never the app's own service; `dev` brings them up first.
  Never leave it empty: `up -d` with no service starts
  every service, the app container included. Without
  infrastructure services, remove the **Infra** section,
  the `infra-up` prerequisite of `dev` and the "Start
  infra, then" part of its description.
- `{{test-command}}`, `{{lint-command}}`, `{{build-command}}`:
  the stack's test, lint and build commands.
- `{{dev-targets}}`: extra target names that should load
  `.env.local` (empty if none).

Per-stack notes:

- **Go**: `go test -race -shuffle=on ./...` for tests,
  `golangci-lint run` for lint, `CGO_ENABLED=0 go build
  -trimpath -ldflags="-s -w"` for the build. Add `GOOS` /
  `GOARCH` variables only when cross-compiling. Add a
  `format` target only if the project wants one.
- **Python**: wrap the commands in `uv run`; add `install`
  (`uv sync`) when useful; lint and format with `ruff`.
- **Node.js / TypeScript**: thin wrappers around pnpm
  scripts; extras such as `typecheck`, `test-watch` and
  `coverage` are welcome.
- **Java / Spring Boot**: wrap the Maven or Gradle wrapper.

Extra project targets are fine; keep them in the same style.

## Conventions

- Keep `help` as the default goal so a bare `make` lists
  targets instead of running them.
- Keep the self-documenting convention: `##@` for section
  headers and `## description` after each target.
- Declare every non-file target `.PHONY`.
- Remove sections that do not apply rather than leaving
  empty or placeholder recipes.

## Existing Makefile

When a project already has a `Makefile`, do not replace it:

- Add each missing standard target, adapted from the
  template, in the same style as the file.
- Keep the project's own targets and recipes untouched.
- Do not rename or reorder existing targets.
