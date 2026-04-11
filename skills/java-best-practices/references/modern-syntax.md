# Modern Syntax

Goal: leverage modern Java language features to
reduce boilerplate, improve readability, and
increase type safety.

## Records (Java 16+)

Replace plain data-carrier classes (POJOs with only
fields, constructor, getters, `equals`, `hashCode`,
`toString`) with records:

```java
// Before
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    // equals, hashCode, toString...
}

// After
public record Point(int x, int y) {}
```

**When NOT to convert:** classes with mutable state,
inheritance hierarchies, or JPA entities (which
require a no-arg constructor and mutable fields).

## Sealed Classes (Java 17+)

Use `sealed` to restrict type hierarchies where the
set of subtypes is known and fixed:

```java
public sealed interface Shape
        permits Circle, Rectangle, Triangle {}

public record Circle(double radius)
        implements Shape {}
public record Rectangle(double w, double h)
        implements Shape {}
public record Triangle(double a, double b,
        double c) implements Shape {}
```

Sealed hierarchies enable exhaustive pattern matching
in `switch` without a `default` branch.

## Pattern Matching for switch (Java 21+)

Replace chains of `instanceof` checks with pattern
matching in `switch`:

```java
// Before
if (shape instanceof Circle c) {
    return Math.PI * c.radius() * c.radius();
} else if (shape instanceof Rectangle r) {
    return r.w() * r.h();
} else {
    throw new IllegalArgumentException();
}

// After
return switch (shape) {
    case Circle c ->
        Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.w() * r.h();
    case Triangle t -> computeTriangleArea(t);
};
```

Use **record patterns** to destructure nested
records directly:

```java
case Circle(var radius) ->
    Math.PI * radius * radius;
```

## Text Blocks (Java 15+)

Replace concatenated multi-line strings with text
blocks:

```java
// Before
String json = "{\n"
    + "  \"name\": \"Alice\",\n"
    + "  \"age\": 30\n"
    + "}";

// After
String json = """
        {
          "name": "Alice",
          "age": 30
        }
        """;
```

## Switch Expressions (Java 14+)

Replace `switch` statements with `switch`
expressions when a value is being computed:

```java
String label = switch (status) {
    case ACTIVE -> "Active";
    case INACTIVE -> "Inactive";
    case PENDING -> "Pending";
};
```

## Unnamed Variables (Java 22+)

Use `_` for variables that are intentionally unused:

```java
try {
    return Integer.parseInt(s);
} catch (NumberFormatException _) {
    return defaultValue;
}

map.forEach((_, value) -> process(value));
```

## Flexible Constructor Bodies (Java 25+)

Use pre-construction statements to validate
arguments before calling `super()` or `this()`:

```java
public class PositiveRange extends Range {
    public PositiveRange(int lo, int hi) {
        if (lo < 0 || hi < 0)
            throw new IllegalArgumentException(
                "Values must be positive");
        super(lo, hi);
    }
}
```

## Checklist

- [ ] Data-carrier classes converted to records
      where appropriate
- [ ] Sealed hierarchies for closed type sets
- [ ] Pattern matching in `switch` instead of
      `instanceof` chains
- [ ] Text blocks for multi-line strings
- [ ] Switch expressions for value-producing
      switches
- [ ] `_` for intentionally unused variables
