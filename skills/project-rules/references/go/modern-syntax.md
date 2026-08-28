# Modern Syntax

Recent language features that are easy to
overlook. Well-known features (generics syntax,
short variable declarations, defer) are omitted —
apply from general knowledge.

## Loop Variable Per-Iteration Scope (Go 1.22+)

Since Go 1.22, the loop variable is **scoped per
iteration**, fixing the long-standing closure
capture footgun:

```go
// Go 1.22+ — each goroutine sees its own v
for _, v := range items {
    go func() { process(v) }()
}
```

Before 1.22 this required `v := v` shadowing.
**Check the module's `go` directive** before
relying on the new behavior — the change is gated
on `go 1.22` in `go.mod`, even if the toolchain
is newer.

## Range over Integer (Go 1.22+)

```go
for i := range 10 {
    fmt.Println(i)   // 0, 1, ..., 9
}
```

Prefer over `for i := 0; i < 10; i++` when the
counter is the only loop state.

## Range over Function — Iterators (Go 1.23+)

User-defined iterators are functions of type
`iter.Seq[V]` or `iter.Seq2[K, V]` ranged with
`for`:

```go
import "iter"

func Lines(r io.Reader) iter.Seq[string] {
    return func(yield func(string) bool) {
        s := bufio.NewScanner(r)
        for s.Scan() {
            if !yield(s.Text()) {
                return    // consumer broke out
            }
        }
    }
}

for line := range Lines(file) {
    fmt.Println(line)
}
```

Rules:

- Prefer iterators over returning a slice when
  the sequence is large, lazy, or infinite.
- The `yield` callback returns `false` when the
  consumer breaks early — **always check it**
  and return cleanly.
- `slices.All`, `slices.Values`, `maps.All`,
  `maps.Keys`, and `maps.Values` now return
  iterators (their signatures changed in 1.23 —
  check call sites when bumping the module
  version).

## slices and maps Packages (Go 1.21+)

The standard library now ships generic helpers —
prefer them over hand-rolled loops and
third-party packages (`golang.org/x/exp/slices`
is deprecated):

```go
import (
    "slices"
    "maps"
)

slices.Contains(xs, target)
slices.Sort(xs)
slices.SortFunc(xs, func(a, b X) int { ... })
slices.BinarySearch(sorted, key)
slices.Reverse(xs)

maps.Keys(m)        // returns iter.Seq (1.23+)
maps.Clone(m)
maps.Equal(m1, m2)
```

`slices.SortFunc` takes a **three-way
comparator** returning `-1 / 0 / +1`, not the
`less` function used by `sort.Slice`. Use
`cmp.Compare(a, b)` to build one.

## Built-in min, max, clear (Go 1.21+)

```go
n := min(a, b, c)
m := max(x, y)
clear(s)          // zeroes a slice / empties a map
```

No import required. `clear` on a map deletes all
entries; on a slice it zeroes elements without
changing length.

## Generic Type Aliases (Go 1.24+)

```go
type Set[T comparable] = map[T]struct{}
```

Useful for compatibility shims and renaming
generic types without forcing call-site changes.

## Generic Methods (Go 1.27+)

Since Go 1.27, concrete (non-interface) methods can
declare their own type parameters, between the
method name and the parameter list:

```go
type List[E any] struct {
    elem E
    next *List[E]
}

// R belongs to the method, independent of the
// receiver's E.
func (List[E]) Map[R any](f func(E) R) List[R] {
    /* ... */
}
```

Before 1.27, the result type had to be lifted into
a package-level generic function:

```go
// Go 1.18 workaround
func MapList[E, R any](l List[E], f func(E) R) List[R] { /* ... */ }
```

Rules:

- Prefer a method when the operation belongs to one
  type and only the **result** type varies. Keep a
  package-level generic function when the operation
  spans several types.
- Chained calls then read left to right —
  `NewList(0, 2, 4).Map(add(2)).Map(divideBy(2))`
  instead of nesting `MapList(MapList(...), ...)`.
- A method expression recovers the function form
  when it reads better: `f := List[int].Map[int]`.
- Like every generic construct, a generic method
  must be instantiated — explicitly or by
  inference — before it is called or converted to a
  function value.

**Interface methods still cannot declare type
parameters**, and this is deliberate — the compiler
would have to instantiate the method for every type
argument a separate package might use:

```go
type I interface {
    M[P any]()    // invalid in Go 1.27
}
```

A generic method therefore never helps satisfy an
interface: `func (T) M[P any]()` does not make `T`
implement `interface{ M() }`, even though
`T.M[int]` has a matching signature. When a type
must satisfy an interface, keep the method
non-generic — a thin non-generic method delegating
to a generic one is the usual way out.

See [Generic Methods](https://go.dev/blog/generic-methods)
on the Go blog.

## Generics — Use Sparingly

- Reach for generics only when the alternative
  is **`any` plus type assertions** or **code
  duplication across several concrete types**.
- Do **not** generify single-use container code,
  CRUD repositories, or "just in case" helpers —
  compile times grow, errors get noisier, and
  the standard library style prefers concrete
  types.
- The same restraint applies to generic methods:
  add one to remove duplication, not to make an
  API look fluent.
- Constraints live in `cmp.Ordered`,
  `comparable`, and `~T` underlying-type
  approximations — most projects do not need a
  `constraints` package.

## Zero Values Are Useful

Many standard types are designed so that the
zero value is immediately usable. Lean on this
instead of constructors:

```go
var b strings.Builder       // ready to use
var wg sync.WaitGroup       // ready to use
var m sync.Mutex            // ready to use
var buf bytes.Buffer        // ready to use
```

Design your own types the same way when
possible — it eliminates a class of
"forgot to call New" bugs.
