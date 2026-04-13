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
