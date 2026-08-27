# Concurrency

Patterns and APIs that are easy to miss.
Well-known basics (goroutines, channels,
`select`) are omitted — apply from general
knowledge.

## errgroup

Use `golang.org/x/sync/errgroup` to fan out
goroutines with first-error short-circuit and
context cancellation:

```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(ctx)
g.SetLimit(8)    // bounded parallelism

for _, item := range items {
    g.Go(func() error {
        return process(ctx, item)
    })
}
if err := g.Wait(); err != nil {
    return err
}
```

- `WithContext` cancels `ctx` as soon as any
  goroutine returns an error — propagate `ctx`
  into the called code so they observe it.
- `SetLimit(n)` bounds concurrency without
  manual semaphores.

## sync.WaitGroup.Go (Go 1.25+)

`sync.WaitGroup` gained a `Go` method that wraps
`Add(1)` + `go func()` + `Done()`:

```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Go(func() {
        process(item)
    })
}
wg.Wait()
```

Prefer over the manual `Add`/`defer Done` pattern
in Go 1.25+ — it eliminates the classic bug of
forgetting `Done` on a panic path.

## sync.Once* (Go 1.21+)

For lazy one-shot initialization, prefer the
typed wrappers over a hand-rolled `sync.Once`
with a package-level variable:

```go
var loadConfig = sync.OnceValue(func() *Config {
    return mustReadConfig()
})

// Caller
cfg := loadConfig()
```

- `sync.OnceFunc(f)` — runs `f` once, no return
  value.
- `sync.OnceValue(f)` — single return value,
  cached.
- `sync.OnceValues(f)` — `(T, error)` pair,
  cached.

If `f` panics, **the panic is re-thrown on every
subsequent call** — design accordingly.

## Context Propagation

- **Always pass `ctx` down**; never let a
  goroutine outlive its request without an
  explicit detach.
- For background work that must outlive a
  request, derive a new context explicitly:

```go
bgCtx := context.WithoutCancel(parentCtx)  // Go 1.21+
go cleanup(bgCtx)
```

  `context.WithoutCancel` retains values but
  drops cancellation — use it instead of
  `context.Background()` when you still want
  trace IDs and request-scoped values.

- `context.AfterFunc(ctx, f)` (Go 1.21+) runs
  `f` exactly once when `ctx` is cancelled. Use
  for cleanup tied to a context's lifetime.

## Channels

- **Direction in signatures**: declare the
  narrowest channel direction at the API
  boundary so misuse is a compile error:

```go
func produce(out chan<- Event) { ... }
func consume(in <-chan Event)  { ... }
```

- **Close from the sender only**, never the
  receiver. Closing a closed channel panics.
- **Unbuffered channels are synchronization
  points**, not "fast queues". Use buffers only
  when you have a concrete reason (decoupling
  throughput from latency, fan-in batching).
- **Do not use `time.After` in long-lived
  `select` loops** — it leaks timers until they
  fire. Use `time.NewTimer` and `timer.Reset`
  with explicit `Stop`.

## Goroutine Hygiene

- **Every `go` is a leak risk**. Before
  starting one, answer: how does it stop? Who
  waits for it? What context cancels it?
- **No mutex copies**. `govet` catches most
  cases; the rule is: any struct containing a
  `sync.Mutex` (or `sync.WaitGroup`,
  `sync.Cond`, etc.) must be passed by pointer.
- **Map access is not concurrency-safe**, even
  for reads-while-write. Use `sync.Map` for
  read-mostly caches with stable keys; a plain
  `map` plus `sync.RWMutex` otherwise.
  `sync.Map` is **not** a faster `map` —
  benchmark before adopting.

## GOMAXPROCS in Containers (Go 1.25+)

Since Go 1.25, the runtime reads cgroup CPU
limits and sets `GOMAXPROCS` accordingly inside
containers — the `automaxprocs` workaround is
no longer needed. On older toolchains, still use
`go.uber.org/automaxprocs` to avoid the runtime
defaulting to host-wide CPU count.
