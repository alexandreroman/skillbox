# Observability

Goal: structured logging, health checks, metrics,
and distributed tracing.

## Dependencies

Ensure the following starters are present:

- `spring-boot-starter-actuator`

## Structured logging

Configure ECS-format structured logging in
`application.yaml`:

```yaml
logging:
  structured:
    format:
      console: ecs
```

Replace raw `System.out.println` or
`e.printStackTrace()` calls with SLF4J logger usage:

```java
private static final Logger LOGGER =
    LoggerFactory.getLogger(MyClass.class);
```

## Actuator

Expose health and metrics on a separate management
port:

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
  metrics:
    tags:
      service.name: ${spring.application.name}
      service.instance.id: ${random.uuid}
```

## Tracing (optional)

If the user needs distributed tracing, add
`spring-boot-starter-opentelemetry` and configure
sampling in `application.yaml`:

```yaml
management:
  tracing:
    sampling:
      probability: 1.0
```
