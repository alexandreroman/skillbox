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
