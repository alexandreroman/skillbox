# API Design

Goal: design clear, safe, and maintainable public
APIs by leveraging modern Java idioms.

## Optional (Java 8+, refined over time)

Use `Optional` as a return type to signal that a
value may be absent. Never use it as a field type,
method parameter, or collection element.

```java
// Good — return type signals possible absence
public Optional<User> findById(Long id) {
    return Optional.ofNullable(userMap.get(id));
}

// Bad — do not use as a parameter
public void process(Optional<String> name) { ... }
```

### Optional best practices

- **Never call `.get()` without checking presence.**
  Prefer `.orElse()`, `.orElseGet()`,
  `.orElseThrow()`, or `.ifPresent()`.
- **Use `.map()` / `.flatMap()`** to chain
  transformations instead of `if (opt.isPresent())`.
- **Use `.stream()`** (Java 9+) to integrate with
  Stream pipelines:

```java
users.stream()
    .map(this::findAddress)
    .flatMap(Optional::stream)
    .toList();
```

## Nullability Discipline

Even without `Optional`, make nullability explicit:

1. **Document contracts** — annotate parameters and
   return types with `@Nullable` / `@NonNull`
   (from `jakarta.annotation`,
   `org.jspecify.annotations`, or
   `org.springframework.lang`).
2. **Fail fast** — use `Objects.requireNonNull()`
   at public API boundaries:

```java
public UserService(UserRepository repo) {
    this.repo = Objects.requireNonNull(repo,
        "repo must not be null");
}
```

3. **Prefer empty collections over null** — return
   `List.of()` or `Map.of()` instead of `null` for
   collection-typed methods.

## Immutability

Favor immutable data structures to reduce bugs
and simplify reasoning:

- Use **records** for value objects.
- Return **unmodifiable collections** from public
  methods (`List.of()`, `List.copyOf()`,
  `.toList()`).
- Make fields `final` wherever possible.
- Use **defensive copies** when accepting mutable
  collections:

```java
public record Team(String name,
        List<String> members) {
    public Team {
        members = List.copyOf(members);
    }
}
```

## Sealed Interfaces for APIs

Use sealed interfaces to define closed sets of
types in public APIs. This enables exhaustive
handling by consumers and makes the API contract
explicit:

```java
public sealed interface Result<T>
        permits Success, Failure {
    record Success<T>(T value)
            implements Result<T> {}
    record Failure<T>(String error)
            implements Result<T> {}
}
```

Consumers can pattern-match exhaustively:

```java
return switch (result) {
    case Success<String>(var v) -> process(v);
    case Failure<String>(var e) -> handleError(e);
};
```

## Encapsulation with Modules (Java 9+)

If the project uses the Java module system, ensure
proper encapsulation:

- Export only public API packages in
  `module-info.java`.
- Use `requires` for explicit dependencies.
- Do not use `--add-opens` or `--add-exports` as a
  workaround for encapsulation violations — fix the
  underlying dependency instead.

If the project does not use modules, do not force
migration. Suggest it only for library projects
or large applications with clear module boundaries.

## Checklist

- [ ] `Optional` only as return type, never as
      field or parameter
- [ ] No bare `.get()` on `Optional` — use
      `.orElseThrow()` or alternatives
- [ ] Nullability annotations on public API
      boundaries
- [ ] `Objects.requireNonNull()` for non-null
      parameters
- [ ] Empty collections instead of `null`
- [ ] Records for value objects, unmodifiable
      collections from public methods
- [ ] Sealed interfaces for closed type
      hierarchies in APIs
