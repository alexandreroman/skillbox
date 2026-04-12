# Code Style

Formatting rules to enforce when writing or
modifying Java code. Apply these to new and changed
code only — do not reformat untouched code.

## Indentation & Whitespace

- **4 spaces per indent level, never tabs.**
- No trailing whitespace on any line.
- Exactly one blank line between methods.
- No more than one consecutive blank line anywhere.
- One statement per line — never chain multiple
  statements with `;` on the same line.

## Braces

Use K&R style (opening brace on the same line):

```java
if (condition) {
    doSomething();
} else {
    doOther();
}
```

Always use braces, even for single-line bodies:

```java
// Bad
if (done) return;

// Good
if (done) {
    return;
}
```

## Line Length

- **120 characters max** per line.
- When wrapping, break **after** an operator or
  comma, and indent the continuation by 8 spaces
  (double indent):

```java
var result = someObject
        .firstOperation()
        .secondOperation(
                longArgument1,
                longArgument2);
```

## Imports

- No wildcard imports (`import java.util.*`).
- Group in this order, separated by a blank line:
  1. `java.*`
  2. `javax.*`
  3. Third-party (`com.*`, `org.*`, etc.)
  4. Project packages
- Remove unused imports.

## Naming

| Element          | Convention              | Example                  |
| ---------------- | ----------------------- | ------------------------ |
| Class / Record   | `UpperCamelCase`        | `OrderService`           |
| Method / Field   | `lowerCamelCase`        | `findByName`             |
| Constant         | `UPPER_SNAKE_CASE`      | `MAX_RETRY_COUNT`        |
| Package          | all lowercase, no `_`   | `com.acme.billing`       |
| Type parameter   | single uppercase letter | `T`, `E`, `K`, `V`      |
| Local variable   | `lowerCamelCase`        | `itemCount`              |
| Boolean accessor | `is` / `has` prefix     | `isEmpty`, `hasChildren` |

- Avoid abbreviations except universally accepted
  ones (`id`, `url`, `http`).
- Use `var` for local variables when the type is
  obvious from the right-hand side.

## Miscellaneous

- Use `final` on local variables only when it aids
  clarity (e.g., in lambdas or complex methods) —
  do not add it mechanically everywhere.
- Prefer `List.of()` / `Map.of()` for immutable
  literals over `Collections.unmodifiable*`.
- Use `Optional` as a return type, never as a field
  or method parameter.
- Annotate `@Override` on every overriding method.
- Place annotations on their own line, above the
  declaration they annotate.
