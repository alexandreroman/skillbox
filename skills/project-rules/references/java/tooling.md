# Tooling

Build system and logging preferences for Java
projects.

## Build System

- **Maven** is the preferred build system.
- Use **Maven Wrapper** (`mvnw`) to invoke
  Maven — never a globally installed `mvn`.
- Follow Maven-standard directory layout:
  `src/main/java`, `src/test/java`,
  `src/main/resources`, etc.
- Stick to `pom.xml` conventions — do not
  introduce Gradle or other build tools unless
  the project already uses them.

## Dependency Versions

To find the latest stable version of a Maven
dependency, fetch its `maven-metadata.xml`
file from Maven Central:

```text
https://repo1.maven.org/maven2/{groupIdPath}/{artifactId}/maven-metadata.xml
```

Build `{groupIdPath}` by replacing `.` with `/`
in the `groupId` (e.g. `org.springframework.boot`
→ `org/springframework/boot`).

Read `<release>` for the latest stable release,
or `<latest>` for the most recent version
(which may include snapshots or release
candidates).

**Do not use** the Maven Central `solrsearch`
API (`https://search.maven.org/solrsearch/`) to
look up versions — it is unreliable and often
returns outdated results.

## Logging

- **SLF4J with Logback** is the preferred
  logging stack.
- Use the `org.slf4j.Logger` /
  `org.slf4j.LoggerFactory` API:

```java
private static final Logger LOGGER =
        LoggerFactory.getLogger(MyClass.class);
```

- Never use `System.out.println`,
  `System.err.println`, or `java.util.logging`
  for application logging.
- **Prefer structured logging** — use key-value
  pairs so log entries are machine-parseable:

```java
// Bad — unstructured, hard to parse
LOGGER.info("Processing order " + orderId);

// Better — parameterized but unstructured
LOGGER.info("Processing order {}", orderId);

// Best — structured key-value pairs
LOGGER.atInfo()
        .setMessage("Processing order")
        .addKeyValue("orderId", orderId)
        .log();
```
