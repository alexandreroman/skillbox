# Configuration Classes

## Disable proxy bean methods

Always annotate configuration classes with
`@Configuration(proxyBeanMethods = false)`:

```java
@Configuration(proxyBeanMethods = false)
public class MyAppConfiguration {

    @Bean
    MyService myService(MyRepository repository) {
        return new MyService(repository);
    }
}
```

By default, `proxyBeanMethods` is `true` and
Spring creates a CGLIB subclass of every
`@Configuration` class so that inter-`@Bean`
method calls return the existing singleton
instead of creating a new instance. This proxy
has a cost: extra memory for the generated
subclass, slower startup, and incompatibility
with GraalVM native images.

Setting `proxyBeanMethods = false` switches the
class to _lite mode_: Spring registers the
`@Bean` methods but does not subclass the
configuration. This is the approach used by
Spring Boot's own auto-configurations.

The only scenario where `proxyBeanMethods = true`
is needed is when one `@Bean` method calls another
`@Bean` method directly and expects the singleton
back. Prefer constructor injection (as shown
above) to avoid that pattern entirely.

## Record-based configuration properties

When a component needs two or more external
properties, group them in a Java record annotated
with `@ConfigurationProperties` instead of
injecting individual `@Value` fields:

```java
@ConfigurationProperties(prefix = "app.billing")
public record BillingProperties(
    String currency,
    int maxRetries
) {
}
```

Enable the record in the configuration class:

```java
@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(BillingProperties.class)
public class BillingConfiguration {

    @Bean
    BillingService billingService(
            BillingProperties props) {
        return new BillingService(
            props.currency(), props.maxRetries());
    }
}
```

Records are a good fit because they are immutable,
need no boilerplate (no getters, `toString`,
`equals`), and make the property group explicit in
the constructor signature. For a single property,
`@Value` remains acceptable.
