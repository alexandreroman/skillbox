# Containers

Rules for building optimized container images
from Spring Boot applications.

## Layered JARs

Spring Boot supports layered JARs that split the
fat JAR into distinct layers for better Docker
image caching. Always use this approach when
writing a `Dockerfile` or configuring a build.

### Dockerfile with layered extraction

```dockerfile
# Stage 1 — extract layers from the fat JAR
FROM eclipse-temurin:25-jre AS extract
WORKDIR /build
COPY target/*.jar app.jar
RUN java -Djarmode=tools -jar app.jar \
      extract --layers --destination extracted

# Stage 2 — assemble the runtime image
FROM eclipse-temurin:25-jre
WORKDIR /app
COPY --from=extract /build/extracted/dependencies/ ./
COPY --from=extract /build/extracted/spring-boot-loader/ ./
COPY --from=extract /build/extracted/snapshot-dependencies/ ./
COPY --from=extract /build/extracted/application/ ./
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Each `COPY` instruction creates a separate Docker
layer. Dependencies change rarely, so they stay
cached across builds; only the `application/` layer
is rebuilt on code changes.

## General guidelines

- **Multi-stage builds** — always use a multi-stage
  `Dockerfile` to keep the runtime image small.
- **JRE, not JDK** — base the runtime stage on a
  JRE image (e.g., `eclipse-temurin:25-jre`).
- **Non-root user** — run the application as a
  non-root user in production images.
- **Health check** — expose the Actuator health
  endpoint and declare a `HEALTHCHECK` instruction
  or Kubernetes liveness/readiness probes.
