# REST API

Goal: consistent, well-structured REST controllers
with proper error handling, validation, and
documentation.

## Controller structure

- One `@RestController` per resource or bounded
  context.
- Use `@RequestMapping("/api/v1/resource")` at the
  class level.
- Keep controller methods thin — delegate business
  logic to a service layer.

## Input validation

Add `spring-boot-starter-validation` if missing.

- Annotate request bodies with `@Valid`.
- Use Jakarta Bean Validation annotations
  (`@NotBlank`, `@Size`, `@Email`, etc.) on DTOs.
- Never validate manually what the framework can
  validate declaratively.

## Error handling

Only create a `@RestControllerAdvice` if the project
actually throws exceptions that need mapping (e.g.
`MethodArgumentNotValidException` from `@Valid`,
`NoSuchElementException`, or custom exceptions).
Do not create one preemptively.

When needed, handle:

- `MethodArgumentNotValidException` → 400 with
  field-level error details.
- `NoSuchElementException` or custom not-found
  exceptions → 404.
- Unhandled exceptions → 500 with a generic message
  (no stack trace in the response body).

Use RFC 9457 Problem Details (`ProblemDetail`)
as the error response format:

```java
@ExceptionHandler(NoSuchElementException.class)
ProblemDetail handleNotFound(
        NoSuchElementException ex) {
    ProblemDetail pd =
        ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND,
            ex.getMessage());
    pd.setTitle("Resource not found");
    return pd;
}
```

## Documentation

If OpenAPI documentation is desired (ask the user),
add `springdoc-openapi-starter-webmvc-ui` and
ensure controllers use `@Operation` and `@Tag`
annotations.
