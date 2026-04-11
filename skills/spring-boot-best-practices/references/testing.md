# Testing

Goal: reliable, fast, maintainable test suite with
appropriate use of Spring Boot test slicing.

## Dependencies

Ensure the following are present:

- `spring-boot-starter-test` (included by default)
- `spring-boot-testcontainers` +
  `testcontainers` (if the project uses a database
  or message broker — ask the user)

## Unit tests

- Test services and domain logic **without** Spring
  context (`@ExtendWith(MockitoExtension.class)`).
- Mock external dependencies with Mockito.
- Naming convention:
  `MethodName_StateUnderTest_ExpectedBehavior`
  or descriptive `@DisplayName`.

## Slice tests

Use the narrowest test slice available:

| Slice | Annotation    |
|-------|---------------|
| Web   | `@WebMvcTest` |
| JPA   | `@DataJpaTest`|
| JSON  | `@JsonTest`   |

Avoid `@SpringBootTest` unless testing full
integration.

**Important:** Spring Boot 4.x reorganized test
slice packages. Before writing imports, check
the project's actual Spring Boot version and
verify the correct package (e.g. `@WebMvcTest`
moved from
`o.s.boot.test.autoconfigure.web.servlet` to
`o.s.boot.webmvc.test.autoconfigure`).

## Integration tests with Testcontainers

If the user opted in, set up a reusable container
configuration:

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

Reference the configuration in integration tests
with `@Import(ContainersConfig.class)`.

## Checklist

- [ ] Unit tests for services and domain logic
      (no Spring context)
- [ ] Slice tests for controllers (`@WebMvcTest`)
      and repositories (`@DataJpaTest`)
- [ ] `@SpringBootTest` only for full integration
- [ ] Testcontainers for external dependencies
      (if applicable)
