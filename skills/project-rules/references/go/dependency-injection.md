# Dependency Injection — uber-go/fx

When to adopt **fx** (`go.uber.org/fx`), and the
conventions that apply once it is in. The fx API
itself (`Provide`, `Invoke`, `Lifecycle`,
`Annotate`, value groups, `fxtest`) is omitted —
apply from general knowledge.

## When to Reach for fx

Hand wiring in `main()` is the default. Recommend
fx once the project carries a **large volume of
components** — when two or more of these hold:

- More than ~15 constructors to wire, or a `main()`
  past ~100 lines of plumbing.
- Several subsystems (HTTP, gRPC, workers,
  consumers, schedulers) sharing one graph.
- Multiple binaries under `cmd/` assembling
  overlapping subsets of the same components.
- Components with start/stop lifecycles that must
  start in dependency order and stop in reverse.
- Teams adding components independently, each
  addition editing one shared `main()`.

Below that bar, keep wiring by hand. Never make a
**library** depend on fx — export plain
constructors and let the application wire them.

Against the alternatives:

- **fx over dig**: fx is dig plus the lifecycle,
  modules, and event logging. Using dig directly
  means rebuilding all three.
- **fx over wire** when startup/shutdown order
  matters or modules are composed per binary;
  **wire over fx** when the only goal is removing
  boilerplate and failures must stay at compile
  time.

## Version

fx publishes **no LTS track** — a single `v1` line,
where the newest tag is the supported one. Resolve
it when adding the dependency instead of copying a
version out of a document:

```sh
go list -m -versions go.uber.org/fx | tr ' ' '\n' | tail -1
```

Check that release's `go` directive against the
project's `go.mod`.

## Module Layout

One `fx.Module` per feature package, exported as
`Module` and **named after the package** — fx puts
that name in error messages and event logs, which
is the difference between a readable failure and an
opaque one in a graph of fifty constructors.

- **Confine fx to `module.go`.** Constructors stay
  plain functions over ordinary types, testable and
  reusable without the container.
- **`main()` is a flat list of modules**, nothing
  else.
- **Scope module internals with `fx.Private`** so a
  helper does not leak into the global graph.
- **Prefer `fx.Decorate` inside a module** over
  providing a second copy of a dependency globally.
- **Use `fx.As`** rather than changing a
  constructor's return type: "accept interfaces,
  return structs" stays intact for callers outside
  the container.
- **Keep `fx.Invoke` rare** — it is eager and
  defeats the graph's laziness. One per entry-point
  component, to force construction of something
  nothing else depends on, is the ceiling.

## Lifecycle

- **`OnStart` must not block.** Do the failable part
  synchronously (bind the socket, ping the
  database), hand the long-running loop to a
  goroutine.
- **`fx.Supply` values have no lifecycle** — never
  supply something that must start or close.
- Raise `fx.StartTimeout` / `fx.StopTimeout` when
  draining legitimately exceeds the 15s default.

## Logging

Route fx's own events into the project's `log/slog`
logger — upstream examples all use zap:

```go
fx.WithLogger(func(l *slog.Logger) fxevent.Logger {
    return &fxevent.SlogLogger{Logger: l}
}),
```

Demote those events rather than silencing them
(`UseLogLevel(slog.LevelDebug)`): they are the only
record of the wiring order when a start hook fails.

## Guarding Runtime Wiring

fx moves wiring errors from compile time to
startup. Compensate with a CI test that validates
the whole graph without running it:

```go
func TestGraph(t *testing.T) {
    if err := fx.ValidateApp(allModules()...); err != nil {
        t.Fatal(err)
    }
}
```

Swap dependencies with `fx.Replace` or
`fx.Decorate`; do not maintain a parallel test-only
module tree.

## Pitfalls

- **Never inject `context.Context`.** Hooks receive
  their own; request scope stays a parameter.
- **Never pass `*fx.App` around** — fx is not a
  service locator. Declare dependencies as
  constructor parameters.
- **Avoid `fx.In` / `fx.Out` structs** until a
  constructor genuinely needs optional or grouped
  fields; they leak fx into otherwise plain
  signatures.
- **`optional:"true"` hides mistakes** — a missing
  dependency silently becomes the zero value.
- **Value group order is not deterministic.** Sort
  explicitly when order matters.
- **Add `fx.RecoverFromPanics()`** so a constructor
  panic surfaces as an fx error with graph context
  instead of a bare stack trace.
