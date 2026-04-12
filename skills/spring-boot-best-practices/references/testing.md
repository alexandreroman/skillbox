# Testing

Well-known features (Mockito unit tests, slice test
annotations, `@SpringBootTest` avoidance) are
omitted — apply from general knowledge.

## Spring Boot 4.x Test Slice Packages

Spring Boot 4.x reorganized test slice packages.
Before writing imports, check the project's actual
Spring Boot version:

| Annotation     | 3.x package                               | 4.x package                          |
|----------------|-------------------------------------------|--------------------------------------|
| `@WebMvcTest`  | `o.s.boot.test.autoconfigure.web.servlet` | `o.s.boot.webmvc.test.autoconfigure` |
| `@DataJpaTest` | `o.s.boot.test.autoconfigure.orm.jpa`     | `o.s.boot.jpa.test.autoconfigure`    |
| `@JsonTest`    | `o.s.boot.test.autoconfigure.json`        | `o.s.boot.jackson.test.autoconfigure`|

Always verify the correct package against the
project's Spring Boot version before suggesting
imports.

## Testcontainers with @ServiceConnection

Use `@ServiceConnection` (Spring Boot 3.1+) instead
of `@DynamicPropertySource` for Testcontainers — it
auto-configures the connection properties:

```java
@TestConfiguration(proxyBeanMethods = false)
class ContainersConfig {

    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>(
            "postgres:17");
    }
}
```

Reference with `@Import(ContainersConfig.class)` in
integration tests.

**Key points:**

- `proxyBeanMethods = false` avoids CGLIB proxying
  overhead in test configs.
- `@ServiceConnection` replaces manual property
  wiring — no need for `registry.add(...)` calls.
