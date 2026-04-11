# Java / Spring Boot

Use [Spring Initializr](https://start.spring.io) to
generate the project skeleton.

## Variables

| Variable | Source |
|---|---|
| `groupId` | Ask the user (e.g. `com.example`) |
| `packageName` | Ask the user — default: `{{groupId}}.{{project-name stripped of - and _}}` |
| `project-name` | Step 2 |
| `short-description` | Step 1 |
| `dependencies` | Ask the user — suggest based on the project objective |

## Steps

1. Use AskUserQuestion to collect the `groupId`,
   `packageName`, and confirm the dependency list
   with the user.
   Always include `actuator` and `devtools`.
   Suggest additional dependencies based on the
   project objective (e.g. `web`, `data-jpa`).
   Propose a default `packageName` built from
   `{{groupId}}.{{project-name}}` with `-` and `_`
   stripped (e.g. `com.example.myapp`). The user
   may override it.

2. Use WebFetch to call the Spring Initializr API:

```text
https://start.spring.io/starter.zip
  ?type=maven-project
  &language=java
  &javaVersion=25
  &packaging=jar
  &groupId={{groupId}}
  &artifactId={{project-name}}
  &name={{project-name}}
  &description={{short-description}}
  &packageName={{packageName}}
  &dependencies={{comma-separated dependency ids}}
  &configurationFileFormat=yaml
```

Use Java 25 by default. The user may request a
different version.

3. Save the response to `starter.zip` and extract it
   into the project directory.
4. Add the following default configuration to the
   generated `application.yaml`:

```yaml
server:
  port: ${PORT:8080}

logging:
  structured:
    format:
      console: ecs

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
5. Clean up `pom.xml`: remove the `<url>`,
   `<licenses>`, `<developers>`, and `<scm>`
   sections if present.
6. Rename the generated `*Application.java` class
   and its file to `Application.java`. Update the
   class name inside the file accordingly.

Reference:
https://docs.spring.io/initializr/docs/current/reference/html/
