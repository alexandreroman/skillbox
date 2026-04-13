# Observability

## Spring Boot Actuator

Expose only the endpoints that are needed and
serve them on a separate management port so they
stay off the public network.

### Separate management port

```yaml
management:
  server:
    port: ${MANAGEMENT_PORT:8081}
```

Actuator endpoints serve operational data
(health checks, metrics, thread dumps) that
must never be reachable from the public network.
Binding them to a dedicated port lets network
policies and ingress rules block external access
without touching the application routes.

### Minimal endpoint exposure

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, metrics
```

By default Spring Boot exposes only `health`.
Explicitly listing `health, metrics` keeps the
surface small while enabling the two endpoints
every production service needs. Add more only
when a concrete use case requires them.

### Health probes

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
        add-additional-paths: true
```

`probes.enabled: true` activates the liveness
and readiness health groups. `add-additional-paths:
true` publishes them at `/livez` and `/readyz` on
the management port. These paths are used by
container orchestrators (Kubernetes liveness /
readiness probes) and Docker health checks
(`HEALTHCHECK` instruction) alike, providing a
consistent way to monitor application health
regardless of the deployment target.

### Metric tags

```yaml
management:
  metrics:
    tags:
      service.name: ${spring.application.name}
      service.instance.id: ${random.uuid}
```

These tags are attached to every metric emitted
by the application. `service.name` enables
per-service filtering in dashboards, while
`service.instance.id` (a random UUID generated
at startup) distinguishes individual replicas.
Together they make it possible to drill down
from a service-level overview to a single
instance without additional instrumentation.

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
Structured logs are preferred because they are
easier to ingest by log aggregation systems and
easier to parse and reason about for AI coding
agents.

In source code, declare the logger as a
`private static final` field named `LOGGER`:

```java
private static final Logger LOGGER =
    LoggerFactory.getLogger(OrderService.class);
```

Use SLF4J structured logging with key-value pairs
instead of string interpolation:

```java
LOGGER.atInfo()
    .setMessage("Order processed")
    .addKeyValue("orderId", orderId)
    .addKeyValue("amount", amount)
    .log();
```

This produces machine-parseable fields in the
structured output, rather than burying values in
free-text messages.

## OpenTelemetry Starter (Spring Boot 4.0+)

Use the dedicated starter instead of manually
wiring Micrometer bridges. It covers both tracing
and metrics export in OTLP format, giving a
unified OTel pipeline.

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
