# Testing

Standard-library testing conventions and recent
additions. Well-known basics (`testing.T`,
`t.Errorf`, `_test.go` suffix) are omitted.

## Standard Library First

- Use the standard `testing` package. `testify`
  is widespread but discouraged in new code —
  its DSL (`assert.Equal`, `require.NoError`)
  drifts from idiomatic Go, hides intent in
  diffs, and slows test compile times.
- Compare with `reflect.DeepEqual` or
  `go-cmp/cmp` (the only third-party testing
  dep worth adopting) for structured diffs:

```go
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("mismatch (-want +got):\n%s", diff)
}
```

## Table-Driven Tests

```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        in      string
        want    Token
        wantErr bool
    }{
        {"empty", "",       Token{},       true},
        {"int",   "42",     IntToken(42),  false},
        {"float", "3.14",   FloatToken(3), false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got, err := Parse(tt.in)
            if (err != nil) != tt.wantErr {
                t.Fatalf("err = %v, wantErr %v", err, tt.wantErr)
            }
            if diff := cmp.Diff(tt.want, got); diff != "" {
                t.Errorf("Parse() mismatch (-want +got):\n%s", diff)
            }
        })
    }
}
```

- **Use `t.Run`** to get one failure line per
  case and selective execution via
  `go test -run TestParse/float`.
- **Call `t.Parallel()` inside subtests** when
  cases are independent; combine with `-shuffle=on`
  in CI to catch order dependencies.
- The pre-Go-1.22 `tt := tt` capture is no
  longer needed (loop variable per-iteration
  scope).

## t.Cleanup over defer

`t.Cleanup` runs in LIFO order after the test
**and any subtests** finish — `defer` only
covers the function where it appears. Prefer
`Cleanup` in helpers that set up resources:

```go
func newTestDB(t *testing.T) *DB {
    t.Helper()
    db, err := openTempDB()
    if err != nil {
        t.Fatal(err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

Always pair setup helpers with `t.Helper()` so
failure lines point at the caller, not the
helper.

## testing/synctest (Go 1.24+)

`testing/synctest` runs concurrent code on a
**fake clock** with deterministic scheduling —
the cure for flaky timer/goroutine tests. Wrap
the section under test in `synctest.Test`:

```go
import "testing/synctest"

func TestTimeout(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        ctx, cancel := context.WithTimeout(t.Context(), time.Second)
        defer cancel()

        synctest.Wait()        // settle goroutines
        time.Sleep(2 * time.Second)
        if ctx.Err() == nil {
            t.Fatal("expected timeout")
        }
    })
}
```

- Inside the bubble, `time.Now` and
  `time.Sleep` advance virtually — tests run in
  milliseconds even for hour-long timeouts.
- `synctest.Wait()` blocks until every goroutine
  in the bubble is idle, deterministically
  resolving "wait for the background work to
  catch up" without sleeps.

## Benchmarks — b.Loop (Go 1.24+)

The classic `for i := 0; i < b.N; i++` pattern
is replaced by `b.Loop()`, which prevents the
compiler from optimizing the body away and
auto-resets the timer after setup:

```go
func BenchmarkParse(b *testing.B) {
    data := loadFixture(b)
    for b.Loop() {
        _, _ = Parse(data)
    }
}
```

Old `b.N` loops still work — only convert when
editing the benchmark.

## Fuzzing

Built-in since Go 1.18. Name fuzz targets
`FuzzXxx` and seed with `f.Add`:

```go
func FuzzParse(f *testing.F) {
    f.Add("42")
    f.Add("3.14")
    f.Fuzz(func(t *testing.T, in string) {
        _, _ = Parse(in)   // must not panic
    })
}

// go test -fuzz=FuzzParse -fuzztime=30s
```

Crashes are saved under `testdata/fuzz/...` —
**commit them** so the seed corpus regresses on
the next run.

## CI Flags

Run tests with:

```sh
go test -race -shuffle=on -count=1 ./...
```

- `-race` catches data races; tolerate the ~2×
  slowdown.
- `-shuffle=on` randomizes test order.
- `-count=1` disables the test cache (useful
  when running against a real DB / external
  service).
