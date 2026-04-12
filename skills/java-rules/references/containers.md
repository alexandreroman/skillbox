# Containers

Rules for building optimized container images
for Java applications.

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

## Multi-stage builds

Always use a multi-stage `Dockerfile` to keep the
runtime image small. Build in one stage, copy only
the artifacts needed at runtime into the final
stage.

```dockerfile
# Stage 1 — build
FROM eclipse-temurin:25-jdk AS build
WORKDIR /build
COPY . .
RUN ./mvnw -B package -DskipTests

# Stage 2 — runtime
FROM eclipse-temurin:25-jre
WORKDIR /app
COPY --from=build /build/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Security

- **Non-root user** — create a dedicated `app` user
  and group, and run the application as `app:app`.

```dockerfile
RUN addgroup --system app \
 && adduser --system --ingroup app app
USER app:app
```

- **No secrets in the image** — pass credentials
  via environment variables or mounted secrets at
  runtime, never bake them into layers.

## JVM flags for containers

The JVM detects container CPU and memory limits
since Java 10. Useful flags to set explicitly:

| Flag                               | Purpose                          |
| ---------------------------------- | -------------------------------- |
| `-XX:MaxRAMPercentage=75.0`        | Heap as a percentage of the      |
|                                    | container memory limit           |
| `-XX:+UseZGC`                      | Low-latency garbage collector    |
| `-XX:+ExitOnOutOfMemoryError`      | Let the orchestrator restart the |
|                                    | container on OOM                 |
| `-XX:+UseContainerSupport`         | Enabled by default; ensure it is |
|                                    | not disabled                     |

## Health checks

Expose a health endpoint (e.g., Spring Actuator,
MicroProfile Health) and declare a `HEALTHCHECK`
instruction or Kubernetes liveness/readiness
probes so the orchestrator can detect unhealthy
containers.

## `.dockerignore`

Always include a `.dockerignore` to exclude build
artifacts, IDE files, and version-control metadata
from the build context:

```text
.git
.idea
*.iml
target/
build/
.gradle/
```
