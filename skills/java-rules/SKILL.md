---
name: java-rules
description: >-
  Java coding rules: best practices, code
  conventions, and design preferences (up to
  Java 25). Covers language features, concurrency,
  API patterns, and code style. Use this skill to
  influence how Java code is written, reviewed,
  or refactored.
allowed-tools: Read
---

# Java Rules

Best practices, code conventions, and design
preferences for modern Java projects. Apply these
rules when writing, reviewing, or refactoring Java
code.
Focuses on Java 21–25 additions and common pitfalls.

## Process

### Step 1 — Scan the project

Before making any change, scan the project to
understand its current state:

- Read `pom.xml` or `build.gradle` for the Java
  source/target version and dependencies.
- Identify the main package structure under
  `src/main/java/`.
- Look for patterns that could benefit from
  modernization.

### Step 2 — Apply all domains

Apply each domain one at a time, in order. For each
domain, read the matching reference file and follow
its instructions. Present proposed changes to the
user and get confirmation before moving to the next.

1. [code-style.md](references/code-style.md)
2. [modern-syntax.md](references/modern-syntax.md)
3. [collections-streams.md](references/collections-streams.md)
4. [concurrency.md](references/concurrency.md)

## Rules

- **Respond in the user's language** when
  communicating with the user.
- **All generated code must be in English.**
- **Do not rewrite working code** just to match a
  convention — only change what provides concrete
  value.
- **Present changes before applying** — show the
  user what you plan to do and get confirmation.
- **Check the project's Java version** before
  suggesting features. Do not suggest features
  that require a higher Java version than the
  project targets.
- **Prefer standard APIs** over third-party
  libraries when the JDK provides an equivalent.
