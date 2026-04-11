---
name: java-best-practices
description: >-
  Apply modern Java best practices (up to Java 25)
  to an existing project. Covers modern syntax,
  collections & streams, concurrency, and API design.
  Use when working on a Java project to audit or
  modernize its codebase.
allowed-tools: Read
---

# Modern Java Best Practices

Audit and modernize a Java project by applying
best practices across four domains, leveraging
features available up to Java 25.

## Process

### Step 1 — Identify the scope

Use AskUserQuestion to ask the user which domains
to apply. Present the four domains and let the user
pick one or more:

- **Modern syntax** — records, sealed classes,
  pattern matching, text blocks, switch expressions,
  unnamed variables
- **Collections & Streams** — sequenced collections,
  Stream gatherers, modern collection factories
- **Concurrency** — virtual threads, structured
  concurrency, scoped values
- **API design** — Optional, immutability,
  nullability, encapsulation

If the user already specified a domain when invoking
the skill, skip this step.

### Step 2 — Scan the project

Before making any change, scan the project to
understand its current state:

- Read `pom.xml` or `build.gradle` for the Java
  source/target version and dependencies.
- Identify the main package structure under
  `src/main/java/`.
- Look for patterns that could benefit from
  modernization (e.g. verbose POJOs, manual null
  checks, synchronized blocks, old collection
  idioms).

### Step 3 — Apply selected domains

For each selected domain, read **only** the matching
reference file and follow its instructions:

- [modern-syntax.md](references/modern-syntax.md)
- [collections-streams.md](references/collections-streams.md)
- [concurrency.md](references/concurrency.md)
- [api-design.md](references/api-design.md)

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
- **Check the project's Java version** before
  suggesting features. Do not suggest features
  that require a higher Java version than the
  project targets.
- **Prefer standard APIs** over third-party
  libraries when the JDK provides an equivalent.
