# GitHub Actions

Best practices for CI/CD workflows with GitHub
Actions.

## Workflow structure

- **Trigger on `push` and `pull_request`** to the
  main branch. Run the full build on PRs; restrict
  publishing to pushes on `main`.
- **Separate build, publish, and merge jobs** so
  each concern is isolated and can fail
  independently.
- **Use a strategy matrix** to fan out across
  modules, platforms, or language versions without
  duplicating job definitions.

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

## Permissions

Apply the **principle of least privilege**: declare
only the permissions the workflow actually needs.

```yaml
permissions:
  contents: read
  packages: write
```

## Caching

- **Cache dependency downloads** using the built-in
  `cache` option of setup actions
  (e.g., `actions/setup-java` with `cache: maven`).
- **Cache Docker layers** with GitHub Actions cache
  backend (`type=gha`) to speed up image builds.

```yaml
cache-from: type=gha,scope=${{ matrix.module }}-${{ matrix.platform }}
cache-to: type=gha,scope=${{ matrix.module }}-${{ matrix.platform }},mode=max
```

## Multi-architecture container images

Build images for both `linux/amd64` and
`linux/arm64` by running each architecture on its
**native runner** (faster than QEMU emulation).

1. **Build per platform** — use a matrix with
   native runners (`ubuntu-24.04` for amd64,
   `ubuntu-24.04-arm` for arm64) and push each
   image by digest.
2. **Upload digests as artifacts** — each platform
   job exports its digest so the merge job can
   collect them.
3. **Merge into a manifest list** — a final job
   downloads all digests and creates a multi-arch
   manifest with `docker buildx imagetools create`.

```yaml
strategy:
  matrix:
    runner: [ubuntu-24.04, ubuntu-24.04-arm]
    include:
      - runner: ubuntu-24.04
        platform: linux/amd64
      - runner: ubuntu-24.04-arm
        platform: linux/arm64
```

### Push by digest

Push each platform image by digest so the tag is
only created once during the merge step:

```yaml
- name: Build and push by digest
  uses: docker/build-push-action@v6
  with:
    context: .
    platforms: ${{ matrix.platform }}
    outputs: >-
      type=image,
      name=ghcr.io/${{ github.repository_owner }}/${{ env.IMAGE }},
      push-by-digest=true,
      name-canonical=true,
      push=true
    cache-from: type=gha,scope=${{ matrix.platform }}
    cache-to: type=gha,scope=${{ matrix.platform }},mode=max
```

### Merge manifests

```yaml
- name: Create manifest list and push
  run: |
    docker buildx imagetools create \
      -t ghcr.io/<owner>/<image>:latest \
      -t ghcr.io/<owner>/<image>:${{ github.sha }} \
      $(printf 'ghcr.io/<owner>/<image>@sha256:%s ' *)
```

## Image tagging

- Tag with the **git SHA** for traceability.
- Optionally add a **`latest`** tag on the main
  branch for convenience.
- Use `docker/metadata-action` to compute tags
  and labels automatically.

## General tips

- **Pin actions to a major version**
  (e.g., `actions/checkout@v4`) — avoid `@main`
  or `@latest`.
- **Use `if:` guards** to skip expensive jobs on
  PRs (e.g., publish only on push to `main`).
- **Keep secrets out of logs** — never echo tokens;
  use `docker/login-action` for registry auth.
- **Set short artifact retention** (`retention-days:
  1`) for intermediate artifacts like digests that
  are only needed between jobs.
