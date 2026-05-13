# Tooling

Tool choices and non-obvious configuration for
modern Go projects.

## go.mod Toolchain Directive

Since Go 1.21, pin the toolchain explicitly so
collaborators and CI use the same Go version,
independent of what is installed locally:

```text
module github.com/acme/billing

go 1.24

toolchain go1.25.3
```

- `go` declares the **minimum language version**
  the module requires.
- `toolchain` declares the **specific toolchain**
  used to build it; Go downloads it on demand.
- Bump `toolchain` independently from `go` — most
  upgrades only need the toolchain line.

## Formatting — gofumpt

Use **gofumpt** instead of `gofmt`. It is a strict
superset: every gofumpt-formatted file is also
gofmt-formatted, but gofumpt enforces additional
rules (no empty blocks, consistent composite
literals, no leading/trailing blank lines in
blocks). Run via `golangci-lint` or directly:

```sh
go run mvdan.cc/gofumpt@latest -l -w .
```

Also run **goimports** (or `golangci-lint`'s
`goimports` linter) to manage import groups —
`gofmt`/`gofumpt` do not.

## Linting — golangci-lint v2

`golangci-lint` v2 (released 2025) introduced a
new config schema. Use a top-level `version: "2"`
field; pre-v2 configs are not auto-migrated:

```yaml
version: "2"
linters:
  default: standard
  enable:
    - errcheck
    - govet
    - ineffassign
    - staticcheck
    - revive
    - gosec
    - bodyclose
    - errorlint
    - gocritic
formatters:
  enable:
    - gofumpt
    - goimports
```

- `revive` replaces the long-deprecated `golint`.
- `errorlint` enforces `%w` wrapping and
  `errors.Is/As` checks.
- `staticcheck` is part of the default set since
  v2 — do not list it under `enable` redundantly.

## Hot Reload — Air

Use **Air** (`github.com/air-verse/air`) to
rebuild and restart the binary on file changes
during development — Go has no built-in watch
mode. Install once, then run from the project
root:

```sh
go install github.com/air-verse/air@latest
air init   # generates .air.toml
air
```

Useful `.air.toml` tweaks:

```toml
[build]
  cmd = "go build -o ./tmp/main ./cmd/server"
  bin = "./tmp/main"
  include_ext = ["go", "tmpl", "html", "sql"]
  exclude_dir = ["assets", "tmp", "vendor", "testdata"]
  delay = 200                # ms debounce
  kill_delay = "500ms"       # give the server time to drain
  send_interrupt = true      # SIGINT, not SIGKILL

[log]
  main_only = false
```

Rules:

- **Send SIGINT, not SIGKILL** (`send_interrupt =
  true`) so the server's graceful shutdown runs.
- **Exclude generated and vendored directories**
  to avoid restart loops.
- Air is a **dev-only tool** — never bake it into
  the production image.

Alternatives: `reflex`, `gow`, `wgo`. Air is the
de-facto community standard.

## Task Runner — Task

Prefer **Task** (`taskfile.dev`) over `make` for
new Go projects: cross-platform, YAML-based, no
tab/space pitfalls. A `Taskfile.yml` skeleton:

```yaml
version: "3"
tasks:
  dev:
    cmds: ["air"]
  lint:
    cmds: ["golangci-lint run"]
  test:
    cmds: ["go test -race -shuffle=on ./..."]
  build:
    cmds:
      - >-
        CGO_ENABLED=0 go build
        -trimpath
        -ldflags="-s -w"
        -o ./bin/app ./cmd/app
```

## Project Layout

Follow the **community-converged** layout, not
the unofficial `golang-standards/project-layout`
repository (which is not endorsed by the Go team
and is widely considered overkill for most
services):

```text
.
├── cmd/<binary>/main.go   # one dir per binary
├── internal/              # non-importable code
│   ├── <feature>/...
│   └── ...
├── <pkg>/                 # importable packages
├── go.mod
└── go.sum
```

- **`internal/`** is enforced by the Go toolchain
  — packages inside cannot be imported from
  outside the module root. Default to placing
  code here.
- **`pkg/`** has no special meaning; only use it
  if you genuinely publish reusable libraries.
- **No `src/`** — Go does not use it.

## Module Workspaces — go work

For repos with multiple modules that develop in
lockstep, use `go work` (Go 1.18+) instead of
`replace` directives in each `go.mod`:

```sh
go work init ./api ./worker ./shared
```

Commit `go.work` for monorepos; **do not commit**
`go.work` when contributors should pick their
own workspace setup — add it to `.gitignore`
instead.
