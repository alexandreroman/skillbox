# Modern Syntax

Well-known features (records, sealed classes, pattern
matching, text blocks, switch expressions, unnamed
variables) are omitted — apply from general knowledge.

## Flexible Constructor Bodies (Java 25+)

Pre-construction statements allow validating
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

## Record Caveats

Favor records everywhere possible. The only
exceptions where records cannot be used:

- **JPA entities** — they require a no-arg
  constructor and mutable fields.
- **Classes that must extend another class** —
  records implicitly extend `java.lang.Record`.

## Record Patterns in switch (Java 21+)

Destructure nested records directly in `switch`
cases — easy to overlook:

```java
case Circle(var radius) ->
    Math.PI * radius * radius;
```

## Checklist

- [ ] Flexible constructor bodies where `super()`
      validation was previously impossible
- [ ] Records used wherever possible
- [ ] No JPA entities converted to records
