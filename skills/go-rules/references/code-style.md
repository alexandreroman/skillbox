# Code Style

Conventions that diverge from or sharpen the
defaults shown in *A Tour of Go*. Well-known
rules (`gofmt` indentation, exported = capital,
short variable names) are omitted.

## Receivers

- Use a **short, consistent abbreviation** of the
  type name across all methods of the same type
  — never `this`, `self`, or `me`:

```go
// Bad
func (this *OrderService) Find(...) {}

// Good
func (s *OrderService) Find(...) {}
```

- Choose **value vs pointer** consistently per
  type. Mixing receiver kinds on the same type
  is a `govet` warning and a common source of
  subtle bugs (interface satisfaction differs
  between `T` and `*T`).
- Use pointer receivers when the method mutates
  state, the type embeds a `sync.Mutex`, or the
  struct is large (>~64 bytes).

## Error Handling

- **Wrap with `%w`** and unwrap via `errors.Is`
  / `errors.As`:

```go
if err := repo.Save(o); err != nil {
    return fmt.Errorf("save order %s: %w", o.ID, err)
}

// Caller side
if errors.Is(err, ErrNotFound) { ... }
```

- **Sentinel errors** are exported variables
  named `Err...`:

```go
var ErrNotFound = errors.New("order: not found")
```

- **Typed errors** implement `error` and are
  matched with `errors.As`. Use them when the
  caller needs structured data (HTTP status,
  field name) — not just identity.
- **Never compare with `==`** on errors that may
  be wrapped. Never match on `err.Error()` —
  message text is not a stable API.
- **Do not panic** across package boundaries.
  Reserve `panic` for programmer errors that
  signal a bug (impossible state), and recover
  only at well-defined boundaries (HTTP
  middleware, goroutine top frames).

## Structured Logging — log/slog

Use the standard library's `log/slog` (Go 1.21+)
— not `log`, `zap`, or `logrus` for new code.
Configure JSON output for production and a text
handler for local development:

```go
var logger *slog.Logger

func init() {
    h := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    })
    logger = slog.New(h)
    slog.SetDefault(logger)
}

slog.Info("processing order",
    "order_id", orderID,
    "customer_id", customerID,
)
```

- Use **lower_snake_case** for log keys
  (industry-wide convention for log aggregators).
- Pass `slog.Attr` for typed values when the
  key is reused: `slog.String("order_id", id)`.
- Propagate a logger via `context` only when it
  carries request-scoped fields; otherwise use
  `slog.Default()`.

## Context

- **First parameter, always named `ctx`**:

```go
func (s *OrderService) Find(ctx context.Context, id string) (*Order, error)
```

- **Never store `context.Context` in a struct**.
  It is request-scoped, not lifetime-scoped.
  Exception: types whose entire purpose is to
  represent a cancellable scope (rare).
- **Do not pass `nil` context**. Use
  `context.TODO()` when a caller has none yet
  and `context.Background()` at process entry
  points.
- **Use typed keys** for `context.WithValue`:

```go
type ctxKey struct{ name string }
var userKey = ctxKey{"user"}

ctx = context.WithValue(ctx, userKey, user)
```

  Never use a bare string as the key — collisions
  across packages are silent.

## any vs interface{}

`any` (Go 1.18+) is an alias for `interface{}`.
Use `any` in **all new code**, including
function signatures, type parameters, and map
values. Touch existing `interface{}` usage only
when you are already editing the surrounding
lines.

## Naming

| Element            | Convention            | Example          |
| ------------------ | --------------------- | ---------------- |
| Package            | short, lowercase, no  | `billing`,       |
|                    | `_` or `camelCase`    | `httputil`       |
| Exported type      | `UpperCamelCase`      | `OrderService`   |
| Unexported type    | `lowerCamelCase`      | `orderRepo`      |
| Acronyms           | preserve case as a    | `userID`,        |
|                    | unit                  | `parseURL`,      |
|                    |                       | `HTTPHandler`    |
| Interface (single  | verb + `er`           | `Reader`,        |
| method)            |                       | `Stringer`       |
| Test function      | `TestXxx(t *testing.  | `TestParse_Empty`|
|                    | T)`                   |                  |

- **Acronyms keep their case as a unit** — write
  `userID`, not `userId`; `parseURL`, not
  `parseUrl`; `HTTPHandler`, not `HttpHandler`.
- **Avoid stuttering**: in package `user`, call
  the type `User`, not `UserUser`; the
  constructor `New`, not `NewUser` (unless the
  package exposes several types).
- **Package names are not plural**: `user`, not
  `users`; `order`, not `orders`.

## Miscellaneous

- **No `init()` functions** unless strictly
  necessary (CLI flag registration, codec
  registration). Prefer explicit construction.
- **Return early**; do not nest `if/else`
  ladders. Happy-path stays at the leftmost
  indent.
- **Group related declarations** in `var ( ... )`
  / `const ( ... )` blocks rather than one
  declaration per line.
- **Do not name return values** for
  documentation; only name them when you need
  naked returns or `defer` mutation. Named
  returns in long functions are a common source
  of shadowing bugs.
- **Use `iota` for enums**; pair with a
  generated `String()` method via `stringer`
  (`go:generate stringer -type=State`).
