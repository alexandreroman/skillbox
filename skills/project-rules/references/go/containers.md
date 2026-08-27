# Containers

Go-specific additions for container images. All
general container rules apply (image size, layer
caching, security, `.dockerignore`) — this file
only covers what Go adds on top.

## Base Image — Distroless or scratch

A static Go binary needs nothing in the runtime
image. Prefer in order:

1. **`gcr.io/distroless/static-debian12:nonroot`**
   — minimal, includes CA certs, timezone data,
   `/etc/passwd`. The `nonroot` variant runs as
   UID 65532.
2. **`scratch`** — zero bytes; bring your own
   CA bundle and `/etc/passwd` if needed.
3. **`alpine`** — only when the binary depends
   on glibc-style features that musl provides,
   or you genuinely need a shell for debugging.

Avoid `golang:<ver>` as a runtime image — it
contains the whole toolchain (~1 GB).

## Build Flags

Always build the runtime binary with:

```sh
CGO_ENABLED=0 \
go build \
    -trimpath \
    -ldflags="-s -w" \
    -o /out/app ./cmd/app
```

- `CGO_ENABLED=0` — produces a pure-Go static
  binary that runs on `scratch`/`distroless/static`
  without glibc.
- `-trimpath` — removes build host paths from
  the binary, improving reproducibility and
  shrinking size.
- `-ldflags="-s -w"` — strips the symbol table
  and DWARF debug info (typically saves 20–30%).
  Do **not** strip if you ship to a profiler
  that needs symbols.

Embed build metadata via `-ldflags="-X"`:

```sh
-ldflags="-s -w -X main.version=${VERSION} -X main.commit=${COMMIT}"
```

The target variables must be **package-level
strings** in the named package — `-X` does not
work on constants.

## BuildKit Cache Mounts

Persist both Go module downloads and the build
cache across image builds:

```dockerfile
RUN --mount=type=cache,id=gomod,target=/go/pkg/mod \
    --mount=type=cache,id=gobuild,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" \
        -o /out/app ./cmd/app
```

- `/go/pkg/mod` — module download cache
  (populated by `go mod download`).
- `/root/.cache/go-build` — compiled package
  cache; massive impact on incremental builds.
- Use **the same `id`** across all `RUN`
  instructions that need each cache so they
  share the same volume.
- **Always set an explicit `id`** — it is not
  only about sharing. Under podman/buildah an
  `id`-less `type=cache` mount on `/go/pkg/mod`
  breaks `go build` module resolution: the build
  fails with `no required module provides
  package …` even though `go mod download`
  populated the cache and `go list -m all`
  resolves the module. A stable `id` (e.g.
  `id=gomod`) avoids it.

## Multi-Stage Build Example

```dockerfile
# syntax=docker/dockerfile:1.7

# — build stage —
FROM golang:1.25-alpine AS build
WORKDIR /src

COPY go.mod go.sum ./
RUN --mount=type=cache,id=gomod,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,id=gomod,target=/go/pkg/mod \
    --mount=type=cache,id=gobuild,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build \
        -trimpath -ldflags="-s -w" \
        -o /out/app ./cmd/app

# — runtime stage —
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

Notes:

- Copy `go.sum` and `go.mod` first, run `go mod
  download`, **then** copy source. This keeps
  the module-fetch layer cached across code-only
  changes (the cache mount layers on top of
  this, not in place of it).
- The runtime stage is a few MB total (binary +
  base image) and runs as non-root by default.

## .dockerignore Additions

Add Go-specific exclusions alongside the general
entries:

```text
bin/
tmp/             # Air's default rebuild dir
dist/
*.test
*.out            # coverage / profile output
.air.toml        # dev-only config
```

`tmp/` and `.air.toml` exist to make sure your
production image never contains Air's hot-reload
artifacts if someone runs `docker build` after
`air`.
