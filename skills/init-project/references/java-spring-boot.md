# Java / Spring Boot

Use [Spring Initializr](https://start.spring.io) to
generate the project skeleton.

## Steps

1. Ask the user for the `groupId` (e.g. `com.example`)
   and `packageName`, and confirm the dependency list.
   Always include `devtools`. Suggest additional
   dependencies based on the project objective (e.g.
   `web`, `data-jpa`). Propose a default `packageName`
   built from `{{groupId}}.{{project-name}}` with `-`
   and `_` stripped (e.g. `com.example.myapp`). The
   user may override it.

2. Call the Spring Initializr API, with the name chosen
   in phase 1b and a one-sentence description of the
   objective from phase 1a:

   ```text
   https://start.spring.io/starter.zip
     ?type=maven-project
     &language=java
     &javaVersion={{java-version}}
     &packaging=jar
     &groupId={{groupId}}
     &artifactId={{project-name}}
     &name={{project-name}}
     &description={{short-description}}
     &packageName={{packageName}}
     &dependencies={{comma-separated dependency ids}}
     &configurationFileFormat=yaml
   ```

   `{{java-version}}` is the latest LTS release that
   Spring Initializr offers, unless the user requests
   another version.

3. Save the response to `starter.zip` and extract it
   into the project directory.

4. Configure logging as described in
   [Spring Boot observability](../../project-rules/references/spring-boot/observability.md).

5. Clean up `pom.xml`: remove the `<url>`,
   `<licenses>`, `<developers>`, and `<scm>`
   sections if present.

6. Rename the generated `*Application.java` class
   and its file to `Application.java`. Update the
   class name inside the file accordingly.

Reference:
https://docs.spring.io/initializr/docs/current/reference/html/
