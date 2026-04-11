# Configuration

Goal: externalized, environment-agnostic
configuration with sensible defaults.

## Rules

1. **Never hard-code** connection strings, ports,
   credentials, or feature flags in Java source.
   Use `application.yaml` properties with
   `${ENV_VAR:default}` syntax.

2. **Use profiles sparingly.** Profiles should only
   toggle infrastructure concerns (e.g. `dev` vs
   `prod` datasource). Business logic must not
   depend on the active profile.

3. **Group properties** with
   `@ConfigurationProperties` instead of scattered
   `@Value` annotations. Add
   `spring-boot-configuration-processor` to
   `pom.xml` for metadata generation:

   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>
           spring-boot-configuration-processor
       </artifactId>
       <optional>true</optional>
   </dependency>
   ```

4. **Server port**: bind via environment variable
   with a default:

   ```yaml
   server:
     port: ${PORT:8080}
   ```

5. **Secrets**: never commit secrets. Use
   environment variables or a secret manager.
   If a `application-*.yaml` file contains
   passwords or tokens, flag it to the user.

## Checklist

- [ ] No hard-coded values in Java source for
      anything environment-specific
- [ ] `@ConfigurationProperties` for grouped config
- [ ] `${ENV_VAR:default}` pattern for all ports
      and external URLs
- [ ] No secrets in tracked files
