---
name: spring-boot-rules
description: >-
  Spring Boot coding rules: best practices, code
  conventions, and architecture preferences
  (3.4+, 4.x). Covers configuration, structure,
  and design patterns. Use this skill to influence
  how Spring Boot code is written, reviewed, or
  refactored.
allowed-tools: Read
---

# Spring Boot Rules

Best practices, code conventions, and architecture
preferences for Spring Boot applications. Apply
these rules when writing, reviewing, or refactoring
Spring Boot code. Focuses on recent additions and
pitfalls — well-known practices (externalized
config, `@Valid`, `@RestControllerAdvice`,
`ProblemDetail`, slice tests, Mockito) are omitted.

## Process

### Step 1 — Scan the project

Before making any change, scan the project to
understand its current state:

- Read `pom.xml` or `build.gradle` for dependencies
  and Spring Boot version.
- Identify the main package structure under
  `src/main/java/`.
- Read `application.yaml` /
  `application.properties`.
- Check for existing tests under `src/test/java/`.

### Step 2 — Apply all domains

Apply each domain one at a time, in order. For each
domain, read the matching reference file and follow
its instructions. Present proposed changes to the
user and get confirmation before moving to the next.

1. [observability.md](references/observability.md)
2. [testing.md](references/testing.md)

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **All generated code must be in English.**
- **Do not rewrite working code** just to match a
  convention — only change what provides concrete
  value.
- **Present changes before applying** — show the
  user what you plan to do and get confirmation.
- **Use context7** to verify current Spring Boot
  API and dependency versions before adding or
  modifying dependencies.
