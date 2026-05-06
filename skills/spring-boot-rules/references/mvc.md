# MVC Controllers

## Use MediaType constants for MIME types

Always use `MediaType` constants instead of
hard-coded strings in controller mapping
annotations:

```java
// Bad — magic string, easy to mistype
@PostMapping(
    value = "/bookings/start",
    produces = "text/plain")

// Good — compile-time checked constant
@PostMapping(
    value = "/bookings/start",
    produces = MediaType.TEXT_PLAIN_VALUE)
```

The `org.springframework.http.MediaType` class
exposes `*_VALUE` string constants for every
common MIME type (`APPLICATION_JSON_VALUE`,
`TEXT_PLAIN_VALUE`, `APPLICATION_PDF_VALUE`, etc.).
Using them avoids typos that the compiler cannot
catch and makes the content type searchable across
the codebase with a single symbol lookup.

The same rule applies to `consumes`, `produces`,
and any other annotation attribute that accepts a
MIME type string.

## Use `ProblemDetail` in exception handlers

When handling exceptions in a controller, return
an `org.springframework.http.ProblemDetail` (RFC
7807) rather than a custom error DTO or a bare
`ResponseEntity<String>`:

```java
// Bad — ad-hoc error shape, no standard contract
@ExceptionHandler(BookingNotFoundException.class)
public ResponseEntity<Map<String, String>> handle(
        BookingNotFoundException e) {
    return ResponseEntity.status(404)
        .body(Map.of("error", e.getMessage()));
}

// Good — standard problem+json response
@ExceptionHandler(BookingNotFoundException.class)
public ProblemDetail handle(
        BookingNotFoundException e) {
    var pd = ProblemDetail.forStatusAndDetail(
        HttpStatus.NOT_FOUND, e.getMessage());
    pd.setTitle("Booking not found");
    return pd;
}
```

`ProblemDetail` is serialized as
`application/problem+json`, gives clients a
predictable error envelope (`type`, `title`,
`status`, `detail`, `instance`), and supports
extension fields via `setProperty(...)`.

## Declare `@ExceptionHandler` at the controller level

Prefer per-controller `@ExceptionHandler` methods
over a global `@ControllerAdvice` / `@RestControllerAdvice`:

```java
// Preferred — handler scoped to this controller
@RestController
@RequestMapping("/bookings")
class BookingController {

    @ExceptionHandler(BookingNotFoundException.class)
    ProblemDetail handle(BookingNotFoundException e) {
        return ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, e.getMessage());
    }
}
```

Keeping the handler next to the controller it
serves makes the error contract explicit, easier
to read, and avoids surprising cross-controller
coupling. Reserve `@ControllerAdvice` for
genuinely cross-cutting concerns (e.g. a final
catch-all for unhandled exceptions).
