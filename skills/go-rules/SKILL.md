---
name: go-rules
description: >-
  Go coding rules: best practices, code
  conventions, modern syntax, concurrency, and
  tooling preferences (Go 1.21+). Use this skill
  to influence how Go code is written, reviewed,
  or refactored.
allowed-tools: Read
---

# Go Rules

Best practices and conventions for modern Go
projects, drawn from community standards
(Effective Go, Google Go Style Guide, Uber Go
Style Guide). Read the relevant references to
apply these rules when writing, reviewing, or
refactoring Go code.

## Domains

- [Tooling](references/tooling.md) —
  `go.mod` toolchain, golangci-lint, gofumpt,
  Air (hot reload), Task, project layout
- [Code style](references/code-style.md) —
  receivers, errors, `slog`, `context`,
  `any` vs `interface{}`
- [Modern syntax](references/modern-syntax.md) —
  range over int/func, `slices`/`maps`, builtins,
  generics caveats
- [Concurrency](references/concurrency.md) —
  `errgroup`, `sync.Once*`, `WaitGroup.Go`,
  context propagation
- [Testing](references/testing.md) —
  table-driven tests, `t.Cleanup`, `testing/synctest`,
  `b.Loop`, fuzzing
- [Containers](references/containers.md) —
  distroless base, `CGO_ENABLED=0`, `-ldflags`,
  BuildKit cache mounts

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **Check the project's Go version** in `go.mod`
  before suggesting features. Do not propose APIs
  that require a newer Go toolchain than the
  project targets.
- **Prefer the standard library** over third-party
  packages when `slices`, `maps`, `cmp`,
  `log/slog`, `net/http`, or `context` already
  cover the use case.
- **Use `any` over `interface{}`** in new code
  (Go 1.18+ alias).
- **Wrap errors with `%w`** in `fmt.Errorf` and
  compare via `errors.Is` / `errors.As` — never
  `==` or string matching.
- **If context7 is available**, use it to verify
  current API and tool versions before adding or
  modifying dependencies.
