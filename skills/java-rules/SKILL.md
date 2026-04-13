---
name: java-rules
description: >-
  Java coding rules: best practices, code
  conventions, formatting, and design preferences
  (up to Java 25). Covers code style, language
  features, concurrency, and API patterns. Use
  this skill to influence how Java code is written,
  reviewed, or refactored.
allowed-tools: Read
---

# Java Rules

Best practices, code conventions, and design
preferences for modern Java projects (Java 21–25).
Read the relevant references to apply these rules
when writing, reviewing, or refactoring Java code.

## Domains

- [Code style](references/code-style.md) —
  formatting, naming, imports, braces
- [Modern syntax](references/modern-syntax.md) —
  records, pattern matching, flexible constructors
- [Collections & streams](references/collections-streams.md) —
  gatherers, sequenced collections
- [Concurrency](references/concurrency.md) —
  virtual threads, structured concurrency, scoped
  values
- [Containers](references/containers.md) —
  base image, multi-stage builds, JVM flags,
  security
- [Tooling](references/tooling.md) —
  build system (Maven), logging (SLF4J/Logback)

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **Check the project's Java version** before
  suggesting features. Do not suggest features
  that require a higher Java version than the
  project targets.
- **Prefer standard APIs** over third-party
  libraries when the JDK provides an equivalent.
- **Use Maven and SLF4J/Logback** — see
  [Tooling](references/tooling.md) for details.
