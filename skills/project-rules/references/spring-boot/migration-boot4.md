# Migration Spring Boot 3 to 4

Spring Boot 4 is built on Spring Framework 7 and
raises the Jakarta EE baseline to version 11. This
reference lists the package renames, artifact changes,
and removed APIs that affect migration.

## Baselines

Spring Boot 4 requires at minimum:

| Dependency      | Minimum version             |
| --------------- | --------------------------- |
| Java            | 17 (JDK 25 recommended)     |
| Jakarta EE      | 11                          |
| Servlet         | 6.1 (Tomcat 11, Jetty 12)   |
| JPA             | 3.2 (Hibernate ORM 7.1+)    |
| Bean Validation | 3.1 (Hibernate Val. 9.0+)   |
| Kotlin          | 2.2+                        |
| Gradle          | 8.14+ or 9                  |
| GraalVM         | 25+                         |
| JUnit           | 6                           |

## Starter renames

Old starters still resolve but are deprecated. Use
the new names in new projects and during migration.
Names below omit the `spring-boot-starter-` prefix.

| Deprecated starter            | Replacement                            |
| ----------------------------- | -------------------------------------- |
| `aop`                         | `aspectj`                              |
| `web`                         | `webmvc`                               |
| `web-services`                | `webservices`                          |
| `oauth2-authorization-server` | `security-oauth2-authorization-server` |
| `oauth2-client`               | `security-oauth2-client`               |
| `oauth2-resource-server`      | `security-oauth2-resource-server`      |

## New starters

Technologies that previously relied on transitive
auto-configuration now require an explicit starter
(prefix `spring-boot-starter-` omitted).

| Technology             | Starter                |
| ---------------------- | ---------------------- |
| Flyway                 | `flyway`               |
| Liquibase              | `liquibase`            |
| OpenTelemetry          | `opentelemetry`        |
| Zipkin                 | `zipkin`               |
| Micrometer Metrics     | `micrometer-metrics`   |
| Jackson                | `jackson`              |
| Kotlin Serialization   | `kotlin-serialization` |
| Spring Batch (JDBC)    | `batch-jdbc`           |
| Spring Batch (no JDBC) | `batch`                |
| Tomcat WAR runtime     | `tomcat-runtime`       |
| Security test          | `security-test`        |

Compatibility starters `spring-boot-starter-classic`
and `spring-boot-starter-test-classic` restore the
Boot 3.x auto-configuration surface for a smoother
transitional period.

## Jackson 3

Jackson 3 changes both the Maven groupId and the Java
package root. The package root moves from
`com.fasterxml.jackson` to `tools.jackson`, and the
groupIds follow:

| Old groupId                        | New groupId                |
| ---------------------------------- | -------------------------- |
| `com.fasterxml.jackson.core`       | `tools.jackson.core`       |
| `com.fasterxml.jackson.dataformat` | `tools.jackson.dataformat` |
| `com.fasterxml.jackson.datatype`   | `tools.jackson.datatype`   |
| `com.fasterxml.jackson.module`     | `tools.jackson.module`     |

Exception: `jackson-annotations` keeps its original
groupId `com.fasterxml.jackson.core` and its original
Java package `com.fasterxml.jackson.annotation`.

The deprecated module `spring-boot-jackson2` provides
Jackson 2 compatibility during transition.

## Annotation and class renames

### Spring Boot

| Old                                  | New                                   |
| ------------------------------------ | ------------------------------------- |
| `@JsonComponent`                     | `@JacksonComponent`                   |
| `@JsonMixin`                         | `@JacksonMixin`                       |
| `JsonObjectSerializer`               | `ObjectValueSerializer`               |
| `JsonValueDeserializer`              | `ObjectValueDeserializer`             |
| `@MockBean`                          | `@MockitoBean` (Spring Framework)     |
| `@SpyBean`                           | `@MockitoSpyBean` (Spring Framework)  |
| `ConditionalOnEnabledTracing`        | `ConditionalOnEnabledTracingExport`   |
| `StreamBuilderFactoryBeanCustomizer` | `StreamsBuilderFactoryBeanConfigurer` |

Renames too long for the table:

- `Jackson2ObjectMapperBuilderCustomizer` →
  `JsonMapperBuilderCustomizer`
- `HttpMessageConverters` →
  `ClientHttpMessageConvertersCustomizer` /
  `ServerHttpMessageConvertersCustomizer`
- `ScheduledTasksObservabilityAutoConfiguration` →
  `ScheduledTasksObservationAutoConfiguration`
- `RestClientBuilderCustomizer` (Elasticsearch) →
  `Rest5ClientBuilderCustomizer`
- `RabbitRetryTemplateCustomizer` →
  `RabbitTemplateRetrySettingsCustomizer` /
  `RabbitListenerRetrySettingsCustomizer`

### Spring Framework 7

| Old                    | New                                   |
| ---------------------- | ------------------------------------- |
| `o.s.lang.Nullable`    | `org.jspecify.annotations.Nullable`   |
| `o.s.lang.NonNull`     | JSpecify `@NonNullByDefault` (module) |
| `o.s.orm.hibernate5.*` | `o.s.orm.jpa.hibernate.*`             |

(`o.s` = `org.springframework`)

## Package reorganizations (Spring Boot 4)

Boot 4 modularizes packages under
`org.springframework.boot.<technology>`.

With `o.s` = `org.springframework`:

- `o.s.boot.BootstrapRegistry` →
  `o.s.boot.bootstrap.BootstrapRegistry`
- `o.s.boot.env.EnvironmentPostProcessor` →
  `o.s.boot.EnvironmentPostProcessor`
- `o.s.boot.autoconfigure.domain.EntityScan` →
  `o.s.boot.persistence.autoconfigure.EntityScan`
- `o.s.boot.test.autoconfigure.properties.PropertyMapping` →
  `o.s.boot.test.context.PropertyMapping`
- `o.s.boot.test.web.client.TestRestTemplate` →
  `o.s.boot.resttestclient.TestRestTemplate`

## javax to jakarta

Spring Framework 7 removes support for the legacy
`javax.*` annotations. All code must use the
`jakarta.*` equivalents:

| Old                              | New                                |
| -------------------------------- | ---------------------------------- |
| `javax.annotation.Resource`      | `jakarta.annotation.Resource`      |
| `javax.annotation.PostConstruct` | `jakarta.annotation.PostConstruct` |
| `javax.annotation.PreDestroy`    | `jakarta.annotation.PreDestroy`    |
| `javax.inject.Inject`            | `jakarta.inject.Inject`            |
| `javax.inject.Named`             | `jakarta.inject.Named`             |

## Hibernate artifacts

| Old artifactId          | New                   |
| ----------------------- | --------------------- |
| `hibernate-jpamodelgen` | `hibernate-processor` |
| `hibernate-proxool`     | Removed               |
| `hibernate-vibur`       | Removed               |

## Elasticsearch artifacts

The low-level REST client artifacts are removed:

- `org.elasticsearch.client:elasticsearch-rest-client`
- `org.elasticsearch.client:elasticsearch-rest-client-sniffer`

Replace both with `co.elastic.clients:elasticsearch-java`.

## Other removals

| Removed                          | Alternative                              |
| -------------------------------- | ---------------------------------------- |
| `o.s:spring-jcl`                 | `commons-logging:commons-logging:1.3.0+` |
| Spring Retry dependency mgmt.    | `o.s.core.retry` (built-in)              |
| Spring Auth Server dep. mgmt.    | Now part of Spring Security 7            |
| Undertow (lacks Servlet 6.1)     | Tomcat or Jetty                          |
| Pulsar Reactive auto-config      | Removed                                  |
| Spring Session Hazelcast support | Maintained by Hazelcast                  |
| Spring Session MongoDB support   | Maintained by MongoDB                    |
| Spock test integration           | Removed (Spock lacks Groovy 5 support)   |
| Wavefront metrics export         | Removed (end-of-life)                    |
| SignalFx metrics export          | Removed (deprecated in Micrometer 1.15)  |
| `ListenableFuture`               | `CompletableFuture`                      |
| OkHttp3 client support           | Removed                                  |
| `webjars-locator-core`           | `webjars-locator-lite`                   |
| `Jackson2ObjectMapperBuilder`    | `JsonMapper.builder()`                   |
| Executable jar launch scripts    | Removed                                  |
