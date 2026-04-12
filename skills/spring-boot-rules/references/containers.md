# Containers

Rules for building optimized container images
from Spring Boot applications.

## Layered JARs

Spring Boot supports layered JARs that split the
fat JAR into distinct layers for better Docker
image caching. Always use this approach when
writing a `Dockerfile`.

The jarmode `extract` command splits the fat JAR
into directories that map to Docker layers. The
resulting layout is also compatible with CDS and
AOT cache optimizations.

## AOT Cache (Java 24+)

On Java 24 and later, the AOT (Ahead-of-Time)
cache replaces CDS. A training run during the
Docker build produces an `.aot` file that
dramatically improves startup time and reduces
memory footprint.

| Flag                                | Purpose             |
| ----------------------------------- | ------------------- |
| `-XX:AOTCacheOutput=app.aot`        | Generate the cache  |
| `-XX:AOTCache=app.aot`              | Use the cache       |
| `-Dspring.context.exit=onRefresh`   | Exit after training |

## CDS (Java < 24)

On Java versions prior to 24, use Class Data
Sharing (CDS) instead. A training run generates a
`.jsa` archive that is reused at startup.

| Flag                                       | Purpose              |
| ------------------------------------------ | -------------------- |
| `-XX:ArchiveClassesAtExit=application.jsa` | Generate the archive |
| `-XX:SharedArchiveFile=application.jsa`    | Use the archive      |
| `-Dspring.context.exit=onRefresh`          | Exit after training  |

## Complete Dockerfile example

The example below combines layered extraction with
AOT cache (Java 25). Replace the AOT flags with
the CDS flags above if targeting Java < 24.

```dockerfile
# Stage 1 — extract layers from the fat JAR
FROM eclipse-temurin:25-jre AS extract
WORKDIR /build
COPY target/*.jar app.jar
RUN java -Djarmode=tools -jar app.jar \
      extract --layers --destination extracted

# Stage 2 — training run to build AOT cache
FROM eclipse-temurin:25-jre AS train
WORKDIR /app
COPY --from=extract /build/extracted/dependencies/ ./
COPY --from=extract /build/extracted/spring-boot-loader/ ./
COPY --from=extract /build/extracted/snapshot-dependencies/ ./
COPY --from=extract /build/extracted/application/ ./
RUN java -XX:AOTCacheOutput=app.aot \
      -Dspring.context.exit=onRefresh \
      -jar application.jar

# Stage 3 — runtime image
FROM eclipse-temurin:25-jre
WORKDIR /app
COPY --from=train /app/ ./
ENTRYPOINT ["java", "-XX:AOTCache=app.aot", \
            "-jar", "application.jar"]
```

Each `COPY` instruction in the extract stage
creates a separate Docker layer. Dependencies
change rarely, so they stay cached across builds;
only the `application/` layer is rebuilt on code
changes.

## General guidelines

- **Multi-stage builds** — always use a multi-stage
  `Dockerfile` to keep the runtime image small.
- **JRE, not JDK** — base the runtime stage on a
  JRE image (e.g., `eclipse-temurin:25-jre`).
- **Non-root user** — create a dedicated `app` user
  and group, and run the application as `app:app`
  in production images.
- **Health check** — expose the Actuator health
  endpoint and declare a `HEALTHCHECK` instruction
  or Kubernetes liveness/readiness probes.
