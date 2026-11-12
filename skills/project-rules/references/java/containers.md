# Containers

Java-specific additions for container images. All
general container rules apply (image size, layer
caching, security, `.dockerignore`) — this file
only covers what Java adds on top.

## Base image

- Use a **JRE image**, not a JDK — the runtime
  image should not contain compilers or build tools.
- Prefer **Eclipse Temurin** official images
  (e.g., `eclipse-temurin:25-jre`).
- Pin the **major version** in the tag to avoid
  unexpected upgrades
  (e.g., `eclipse-temurin:25-jre`, not `:latest`).
- Prefer **`-jre` Alpine variants** when the
  application has no native dependency that requires
  glibc (e.g., `eclipse-temurin:25-jre-alpine`).

## Multi-stage build example

```dockerfile
# Stage 1 — build
FROM eclipse-temurin:25-jdk AS build
WORKDIR /build
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN --mount=type=cache,id=maven,target=/root/.m2 \
    ./mvnw -B dependency:go-offline -q
COPY src ./src
RUN --mount=type=cache,id=maven,target=/root/.m2 \
    ./mvnw -B package -DskipTests -q

# Stage 2 — runtime
FROM eclipse-temurin:25-jre
WORKDIR /app
RUN addgroup --system app \
 && adduser --system --ingroup app app
COPY --from=build --chown=app:app \
     /build/target/*.jar app.jar
USER app:app
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Build cache

The example mounts Maven's local repository
(`/root/.m2`) as a BuildKit cache and fetches
dependencies before copying the source. In a
project that already uses Gradle, mount
`/root/.gradle` and run `./gradlew` instead.

## JVM flags for containers

The JVM detects container CPU and memory limits
since Java 10. Useful flags to set explicitly:

| Flag                          | Purpose                        |
| ----------------------------- | ------------------------------ |
| `-XX:MaxRAMPercentage=75.0`   | Heap as a percentage of the    |
|                               | container memory limit         |
| `-XX:+UseZGC`                 | Low-latency garbage collector  |
| `-XX:+ExitOnOutOfMemoryError` | Let the orchestrator restart   |
|                               | the container on OOM           |
| `-XX:+UseContainerSupport`    | Enabled by default; ensure it  |
|                               | is not disabled                |

## `.dockerignore` additions

Add Java-specific exclusions alongside the general
entries:

```text
.idea
*.iml
target/
build/
.gradle/
```
