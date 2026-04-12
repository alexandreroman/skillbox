---
name: spring-boot-best-practices
description: >-
  Apply best practices to a Java / Spring Boot
  application. Covers recent Spring Boot features
  and pitfalls that are easy to miss (3.4+, 4.x).
  Use when working on an existing Spring Boot
  project to audit or improve its structure.
allowed-tools: Read
---

# Java / Spring Boot Best Practices

Audit and improve a Java / Spring Boot application.
Focuses on recent Spring Boot additions and common
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
