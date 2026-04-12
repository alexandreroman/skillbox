# Observability

Well-known features (SLF4J logging, actuator
endpoints, health probes) are omitted — apply from
general knowledge.

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

Configure sampling in `application.yaml`:

```yaml
management:
  tracing:
    sampling:
      probability: 1.0
```

## Checklist

- [ ] Structured logging via
      `logging.structured.format.console` instead
      of custom JSON layouts
- [ ] `spring-boot-starter-opentelemetry` instead
      of manual Micrometer/OTel wiring
