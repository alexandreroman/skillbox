# Visibility Scope

## Prefer the narrowest visibility scope

Choose the most restrictive access modifier that
still allows the code to work. Spring Boot can
discover and inject components that are
**package-private** — there is no need to make
everything `public` by default:

```java
@Service
class OrderService {

    private final OrderRepository repository;

    OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    List<Order> findRecent() {
        return repository.findRecent();
    }
}
```

Guidelines:

| Element                | Default scope         | Make `public` only when…             |
| ---------------------- | --------------------- | ------------------------------------ |
| Stereotype components  | package-private class | exposed in another module's API      |
| `@Configuration`       | package-private class | referenced by `@Import` from outside |
| `@Bean` methods        | package-private       | called from another package          |
| Controllers            | package-private class | needed by code outside the package   |
| Helper methods         | `private`             | reused across the package            |

Keeping classes and methods package-private:

- **Reduces the public API surface** — less code to
  maintain and fewer accidental couplings.
- **Makes refactoring safer** — the compiler catches
  every caller inside the package; there are none
  outside.
- **Signals intent** — a `public` class is a
  deliberate contract; a package-private class is an
  implementation detail.

> Spring uses reflection to instantiate beans, so
> `public` is never required for dependency
> injection, component scanning, or proxy creation.
