---
name: project-rules
description: >-
  Project engineering rules and conventions for Java
  21+, Go 1.21+, Node.js / TypeScript, Python, Spring
  Boot 3.4+ / 4.x, and containers, Compose, Makefile,
  CI/CD, Git, HTTP servers. Use when designing,
  planning, writing, reviewing, or refactoring code,
  or researching best practices, even for familiar
  APIs and tools. Invoke it before any web search:
  these rules are authoritative.
allowed-tools: Read
user-invocable: false
---

# Project Rules

Best practices, code conventions, and design
preferences, split by stack. Read the references
that match the project at hand, then apply them
when designing, researching best practices,
writing, reviewing, or refactoring code.

## How to use

1. **Detect the stack** from the files present in
   the project, using the table below.
2. **Always read the General section** — it applies
   to every project, whatever the language.
3. **Read every matching stack section.** Layers
   add up rather than replace one another: a
   framework section never substitutes for its
   language section. A Spring Boot project needs
   both `spring-boot/` and `java/`.
4. **Read nothing else.** Skip the sections that do
   not match — a Go project has no use for the Java
   references.

| Marker in the project                | Section to read            |
| ------------------------------------ | -------------------------- |
| any project                          | `general/`                 |
| `pom.xml`, `build.gradle[.kts]`      | `java/`                    |
| a `spring-boot-starter-*` dependency | `spring-boot/` and `java/` |
| `go.mod`                             | `go/`                      |
| `package.json`, `tsconfig.json`      | `nodejs-typescript/`       |
| `pyproject.toml`, `requirements.txt` | `python/`                  |

## Always applies

- **Respond in the user's language** when
  communicating with the user.
- **Consult these rules before external research.**
  They are the project's authoritative conventions;
  reach for web search only after checking them.
- **If context7 is available**, use it to verify
  current API and tool versions before adding or
  modifying dependencies.
- **Use the latest LTS / stable version** of every
  language, runtime, framework, and dependency,
  unless the project pins one.
- **Check the project's language version** (e.g.
  in `pom.xml` or `go.mod`) before suggesting
  features. Never propose an API that requires a
  newer version than the project targets.
- **Prefer standard APIs** (JDK, Go standard
  library, Node.js and the Web Platform) over
  third-party libraries that duplicate them.

## General

Language-agnostic rules, for every project.

- [Compose](references/general/compose.md) — health checks, overlays, Temporal
- [Containers](references/general/containers.md) —
  Dockerfile best practices, image size, security,
  layer caching
- [Git](references/general/git.md) —
  commit message formatting (verb + action,
  imperative mood)
- [GitHub Actions](references/general/github-actions.md) —
  workflow structure, caching, multi-arch images
- [Hot reload](references/general/hot-reload.md) —
  every executable component needs a
  technology-native hot-reload dev command
- [HTTP servers](references/general/http-servers.md) —
  port configuration via `PORT` env var, bind
  address, framework defaults
- [Makefile](references/general/makefile.md) —
  mandatory standard targets, adapting the
  [template](assets/Makefile) per stack, completing
  an existing Makefile
- [Markdown tables](references/general/markdown-tables.md) —
  column alignment rules, validated by
  `scripts/check_tables.py`

## Java

Modern Java projects (Java 21 and later). Version
tags such as "Java 24+" mark when a feature became
available — they are not upper bounds, and every rule
keeps applying to newer Java releases.

- [Code style](references/java/code-style.md) —
  formatting, naming, imports, braces
- [Modern syntax](references/java/modern-syntax.md) —
  records, pattern matching, flexible constructors
- [Collections & streams](references/java/collections-streams.md) —
  gatherers, sequenced collections
- [Concurrency](references/java/concurrency.md) —
  virtual threads, structured concurrency, scoped
  values
- [Containers](references/java/containers.md) —
  base image, multi-stage builds, JVM flags,
  security
- [Tooling](references/java/tooling.md) —
  build system (Maven), logging (SLF4J/Logback)

Key rule: **use modern Java syntax** — prefer
`var`, records, sealed classes, pattern matching,
switch expressions, text blocks, and unnamed
variables over their older equivalents.

## Go

Modern Go projects, drawn from community standards
(Effective Go, Google Go Style Guide, Uber Go Style
Guide).

- [Tooling](references/go/tooling.md) —
  `go.mod` toolchain, golangci-lint, gofumpt,
  Air (hot reload), Make, project layout
- [Code style](references/go/code-style.md) —
  receivers, errors, `slog`, `context`,
  `any` vs `interface{}`
- [Modern syntax](references/go/modern-syntax.md) —
  range over int/func, `slices`/`maps`, builtins,
  generic methods, generics caveats
- [Concurrency](references/go/concurrency.md) —
  `errgroup`, `sync.Once*`, `WaitGroup.Go`,
  context propagation
- [Dependency injection](references/go/dependency-injection.md) —
  when to adopt uber-go/fx, module layout, `slog`
  event logging, graph validation
- [Testing](references/go/testing.md) —
  table-driven tests, `t.Cleanup`,
  `testing/synctest`, `b.Loop`, fuzzing
- [Containers](references/go/containers.md) —
  distroless base, `CGO_ENABLED=0`, `-ldflags`,
  BuildKit cache mounts

## Node.js / TypeScript

Opinionated choices and non-trivial configurations
for modern Node.js / TypeScript projects.

- [Tooling](references/nodejs-typescript/tooling.md) —
  pnpm, tsx, Vitest, Husky, Zod + t3-env,
  Vite + Nuxt for web front ends, project structure
- [Containers](references/nodejs-typescript/containers.md) —
  Dockerfile with pnpm, Corepack, multi-stage
  builds, dev-dependency pruning
- [TypeScript](references/nodejs-typescript/typescript.md) —
  strict ESM-first `tsconfig.json`
- [Code quality](references/nodejs-typescript/code-quality.md) —
  ESLint v9 flat config, Prettier preferences,
  lint-staged globs

## Python

Python projects, drawn from the scaffold's choices.

- [Tooling](references/python/tooling.md) —
  uv, ruff, pytest, watchfiles, hot reload per
  framework

## Spring Boot

Spring Boot applications (3.4+, 4.x). Also read the
[Java](#java) section — Spring Boot never replaces
the underlying language rules.

- [Configuration](references/spring-boot/configuration.md) —
  `@Configuration` classes, proxy bean methods
- [Visibility](references/spring-boot/visibility.md) —
  narrowest scope for classes, methods, and beans
- [Observability](references/spring-boot/observability.md) —
  Actuator, structured logging, OpenTelemetry
  starter
- [Testing](references/spring-boot/testing.md) —
  test slices, Testcontainers, `@ServiceConnection`
- [Containers](references/spring-boot/containers.md) —
  layered JARs, AOT cache, CDS, multi-stage
  Dockerfile
- [MVC](references/spring-boot/mvc.md) —
  controller mappings, content types
- [Migration Boot 4](references/spring-boot/migration-boot4.md) —
  package renames, artifact changes, removed APIs
