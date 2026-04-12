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
preferences for Spring Boot applications (3.4+,
4.x). Read the relevant references to apply these
rules when writing, reviewing, or refactoring
Spring Boot code.

## Domains

- [Observability](references/observability.md) —
  Actuator, structured logging, OpenTelemetry starter
- [Testing](references/testing.md) —
  test slices, Testcontainers, @ServiceConnection

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **If context7 is available**, use it to verify
  current Spring Boot API and dependency versions
  before adding or modifying dependencies.
