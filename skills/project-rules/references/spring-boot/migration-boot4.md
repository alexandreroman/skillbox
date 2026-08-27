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

| Deprecated starter                                | Replacement                                                |
| ------------------------------------------------- | ---------------------------------------------------------- |
| `spring-boot-starter-aop`                         | `spring-boot-starter-aspectj`                              |
| `spring-boot-starter-web`                         | `spring-boot-starter-webmvc`                               |
| `spring-boot-starter-web-services`                | `spring-boot-starter-webservices`                          |
| `spring-boot-starter-oauth2-authorization-server` | `spring-boot-starter-security-oauth2-authorization-server` |
| `spring-boot-starter-oauth2-client`               | `spring-boot-starter-security-oauth2-client`               |
| `spring-boot-starter-oauth2-resource-server`      | `spring-boot-starter-security-oauth2-resource-server`      |

## New starters

Technologies that previously relied on transitive
auto-configuration now require an explicit starter.

| Technology             | Starter                                    |
| ---------------------- | ------------------------------------------ |
| Flyway                 | `spring-boot-starter-flyway`               |
| Liquibase              | `spring-boot-starter-liquibase`            |
| OpenTelemetry          | `spring-boot-starter-opentelemetry`        |
| Zipkin                 | `spring-boot-starter-zipkin`               |
| Micrometer Metrics     | `spring-boot-starter-micrometer-metrics`   |
| Jackson                | `spring-boot-starter-jackson`              |
| Kotlin Serialization   | `spring-boot-starter-kotlin-serialization` |
| Spring Batch (JDBC)    | `spring-boot-starter-batch-jdbc`           |
| Spring Batch (no JDBC) | `spring-boot-starter-batch`                |
| Tomcat WAR runtime     | `spring-boot-starter-tomcat-runtime`       |
| Security test          | `spring-boot-starter-security-test`        |

Compatibility starters `spring-boot-starter-classic`
and `spring-boot-starter-test-classic` restore the
Boot 3.x auto-configuration surface for a smoother
transitional period.

## Jackson 3

Jackson 3 changes both the Maven groupId and the Java
package root.

| Scope        | Old                                | New                        |
| ------------ | ---------------------------------- | -------------------------- |
| GroupId      | `com.fasterxml.jackson.core`       | `tools.jackson.core`       |
| GroupId      | `com.fasterxml.jackson.dataformat` | `tools.jackson.dataformat` |
| GroupId      | `com.fasterxml.jackson.datatype`   | `tools.jackson.datatype`   |
| GroupId      | `com.fasterxml.jackson.module`     | `tools.jackson.module`     |
| Java package | `com.fasterxml.jackson`            | `tools.jackson`            |

Exception: `jackson-annotations` keeps its original
groupId `com.fasterxml.jackson.core` and its original
Java package `com.fasterxml.jackson.annotation`.

The deprecated module `spring-boot-jackson2` provides
Jackson 2 compatibility during transition.

## Annotation and class renames

### Spring Boot

| Old                                                | New                                                                               |
| -------------------------------------------------- | --------------------------------------------------------------------------------- |
| `@JsonComponent`                                   | `@JacksonComponent`                                                               |
| `@JsonMixin`                                       | `@JacksonMixin`                                                                   |
| `JsonObjectSerializer`                             | `ObjectValueSerializer`                                                           |
| `JsonValueDeserializer`                            | `ObjectValueDeserializer`                                                         |
| `Jackson2ObjectMapperBuilderCustomizer`            | `JsonMapperBuilderCustomizer`                                                     |
| `HttpMessageConverters`                            | `ClientHttpMessageConvertersCustomizer` / `ServerHttpMessageConvertersCustomizer` |
| `@MockBean`                                        | `@MockitoBean` (Spring Framework)                                                 |
| `@SpyBean`                                         | `@MockitoSpyBean` (Spring Framework)                                              |
| `ConditionalOnEnabledTracing`                      | `ConditionalOnEnabledTracingExport`                                               |
| `ScheduledTasksObservabilityAutoConfiguration`     | `ScheduledTasksObservationAutoConfiguration`                                      |
| `RestClientBuilderCustomizer` (Elasticsearch)      | `Rest5ClientBuilderCustomizer`                                                    |
| `RabbitRetryTemplateCustomizer`                    | `RabbitTemplateRetrySettingsCustomizer` / `RabbitListenerRetrySettingsCustomizer` |
| `StreamBuilderFactoryBeanCustomizer`               | `StreamsBuilderFactoryBeanConfigurer`                                             |

### Spring Framework 7

| Old                                    | New                                       |
| -------------------------------------- | ----------------------------------------- |
| `org.springframework.lang.Nullable`    | `org.jspecify.annotations.Nullable`       |
| `org.springframework.lang.NonNull`     | JSpecify `@NonNullByDefault` (module)     |
| `org.springframework.orm.hibernate5.*` | `org.springframework.orm.jpa.hibernate.*` |

## Package reorganizations (Spring Boot 4)

Boot 4 modularizes packages under
`org.springframework.boot.<technology>`.

| Old                                                       | New                                                |
| --------------------------------------------------------- | -------------------------------------------------- |
| `o.s.boot.BootstrapRegistry`                              | `o.s.boot.bootstrap.BootstrapRegistry`             |
| `o.s.boot.env.EnvironmentPostProcessor`                   | `o.s.boot.EnvironmentPostProcessor`                |
| `o.s.boot.autoconfigure.domain.EntityScan`                | `o.s.boot.persistence.autoconfigure.EntityScan`    |
| `o.s.boot.test.autoconfigure.properties.PropertyMapping`  | `o.s.boot.test.context.PropertyMapping`            |
| `o.s.boot.test.web.client.TestRestTemplate`               | `o.s.boot.resttestclient.TestRestTemplate`         |

(`o.s` = `org.springframework`)

## javax to jakarta

Spring Framework 7 removes support for the legacy
`javax.*` annotations. All code must use the
`jakarta.*` equivalents:

| Old                                | New                                  |
| ---------------------------------- | ------------------------------------ |
| `javax.annotation.Resource`        | `jakarta.annotation.Resource`        |
| `javax.annotation.PostConstruct`   | `jakarta.annotation.PostConstruct`   |
| `javax.annotation.PreDestroy`      | `jakarta.annotation.PreDestroy`      |
| `javax.inject.Inject`              | `jakarta.inject.Inject`              |
| `javax.inject.Named`               | `jakarta.inject.Named`               |

## Hibernate artifacts

| Old artifactId          | New                   |
| ----------------------- | --------------------- |
| `hibernate-jpamodelgen` | `hibernate-processor` |
| `hibernate-proxool`     | Removed               |
| `hibernate-vibur`       | Removed               |

## Elasticsearch artifacts

The low-level REST client artifacts are removed:

| Removed artifact                                             | Replacement                             |
| ------------------------------------------------------------ | --------------------------------------- |
| `org.elasticsearch.client:elasticsearch-rest-client`         | `co.elastic.clients:elasticsearch-java` |
| `org.elasticsearch.client:elasticsearch-rest-client-sniffer` | `co.elastic.clients:elasticsearch-java` |

## Other removals

| Removed                                | Alternative                                                  |
| -------------------------------------- | ------------------------------------------------------------ |
| `org.springframework:spring-jcl`       | `commons-logging:commons-logging:1.3.0+`                     |
| Spring Retry dependency management     | `org.springframework.core.retry` (built-in)                  |
| Spring Auth Server dep. mgmt.          | Now part of Spring Security 7                                |
| Undertow server support                | Tomcat or Jetty (incompatible with Servlet 6.1)              |
| Pulsar Reactive auto-configuration     | Removed                                                      |
| Spring Session Hazelcast support       | Maintained by Hazelcast                                      |
| Spring Session MongoDB support         | Maintained by MongoDB                                        |
| Spock test integration                 | Removed (Spock incompatible with Groovy 5)                   |
| Wavefront metrics export               | Removed (end-of-life)                                        |
| SignalFx metrics export                | Removed (deprecated in Micrometer 1.15)                      |
| `ListenableFuture`                     | `CompletableFuture`                                          |
| OkHttp3 client support                 | Removed                                                      |
| `webjars-locator-core`                 | `webjars-locator-lite`                                       |
| `Jackson2ObjectMapperBuilder`          | `JsonMapper.builder()`                                       |
| Embedded executable uber-jar scripts   | Removed                                                      |
