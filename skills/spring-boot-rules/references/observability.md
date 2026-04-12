# Observability

## Spring Boot Actuator

Expose only the endpoints that are needed and
serve them on a separate management port so they
stay off the public network.

Reference configuration in `application.yaml`:

```yaml
management:
  server:
    port: ${MANAGEMENT_PORT:8081}
  endpoints:
    web:
      exposure:
        include: health, metrics
  endpoint:
    health:
      probes:
        enabled: true
        add-additional-paths: true
  metrics:
    tags:
      service.name: ${spring.application.name}
      service.instance.id: ${random.uuid}
```

Key points:

- **Separate management port** — keeps actuator
  endpoints off the main server port, simplifying
  network policies and avoiding accidental exposure.
- **Minimal exposure** — only `health` and `metrics`
  are exposed; add more only when explicitly needed.
- **Health probes** — `probes.enabled: true` with
  `add-additional-paths: true` exposes `/livez`
  and `/readyz` endpoints.
- **Metric tags** — `service.name` and
  `service.instance.id` are attached to every
  metric, enabling per-service and per-instance
  filtering in dashboards.

## Structured Logging (Spring Boot 3.4+)

Spring Boot 3.4 added native structured logging.
Configure ECS-format output in `application.yaml`
without any extra dependency:

```yaml
logging:
  structured:
    format:
      console: ecs
```

This replaces custom Logback/Log4j2 JSON layouts.
Structured logs are preferred because they are easier
to ingest by log aggregation systems and easier to
parse and reason about for AI coding agents.

In source code, use SLF4J structured logging with
key-value pairs instead of string interpolation:

```java
logger.atInfo()
    .setMessage("Order processed")
    .addKeyValue("orderId", orderId)
    .addKeyValue("amount", amount)
    .log();
```

This produces machine-parseable fields in the
structured output, rather than burying values in
free-text messages.

## OpenTelemetry Starter (Spring Boot 4.0+)

Use the dedicated starter instead of manually wiring
Micrometer bridges. It covers both tracing and
metrics export in OTLP format, giving a unified
OTel pipeline.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>
        spring-boot-starter-opentelemetry
    </artifactId>
</dependency>
```

Tracing is enabled by default with the starter.
Create a `dev` profile in `application-dev.yaml`
to capture all traces during development:

```yaml
management:
  tracing:
    sampling:
      probability: 1.0
```

In production the default sampling probability
(0.1) applies, keeping trace volume manageable.
Set `probability: 1.0` only under the `dev`
profile.
