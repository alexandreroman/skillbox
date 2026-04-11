---
name: spring-boot-best-practices
description: >-
  Apply best practices to a Java / Spring Boot
  application. Covers observability, configuration,
  REST API design, and testing. Use when working on
  an existing Spring Boot project to audit or improve
  its structure.
allowed-tools: Read
---

# Java / Spring Boot Best Practices

Audit and improve a Java / Spring Boot application
by applying best practices across four domains:
observability, configuration, REST API, and testing.

## Process

### Step 1 — Identify the scope

Use AskUserQuestion to ask the user which domains
to apply. Present the four domains and let the user
pick one or more:

- **Observability** — structured logging, health
  checks, metrics, distributed tracing
- **Configuration** — externalization, profiles,
  secrets management
- **REST API** — controller structure, validation,
  error handling, OpenAPI
- **Testing** — unit tests, slice tests,
  Testcontainers

If the user already specified a domain when invoking
the skill, skip this step.

### Step 2 — Scan the project

Before making any change, scan the project to
understand its current state:

- Read `pom.xml` or `build.gradle` for dependencies.
- Identify the main package structure under
  `src/main/java/`.
- Read `application.yaml` /
  `application.properties`.
- Check for existing tests under `src/test/java/`.

### Step 3 — Apply selected domains

For each selected domain, read **only** the matching
reference file and follow its instructions:

- [observability.md](references/observability.md)
- [configuration.md](references/configuration.md)
- [rest-api.md](references/rest-api.md)
- [testing.md](references/testing.md)

Apply one domain at a time. Present proposed changes
to the user and get confirmation before moving to
the next domain.

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
