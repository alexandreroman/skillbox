# Concurrency

Well-known features (virtual thread creation,
`newVirtualThreadPerTaskExecutor()`) are omitted —
apply from general knowledge.

## Virtual Thread Pinning (Java 21+)

`synchronized` blocks **pin** virtual threads to
platform threads, defeating their scalability.
Replace with `ReentrantLock` when guarding I/O:

```java
// Bad — pins virtual thread
synchronized (lock) {
    connection.query(...);
}

// Good
private final ReentrantLock lock =
    new ReentrantLock();

lock.lock();
try {
    connection.query(...);
} finally {
    lock.unlock();
}
```

Also avoid `ThreadLocal` in virtual-thread
contexts — it consumes memory per virtual thread.
Use scoped values instead.

## Structured Concurrency (Preview)

Manages concurrent subtasks as a unit — if one
fails, siblings are cancelled. Only propose if the
project opts in to preview features.

```java
try (var scope = StructuredTaskScope.open()) {
    Subtask<String> user =
        scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> orders =
        scope.fork(() -> fetchOrders(id));

    scope.join();

    return new UserProfile(
        user.get(), orders.get());
}
```

## Scoped Values (Preview)

Immutable, virtual-thread-friendly alternative to
`ThreadLocal`. Only propose if the project opts in
to preview features.

```java
private static final ScopedValue<User> CURRENT_USER =
    ScopedValue.newInstance();

ScopedValue.runWhere(CURRENT_USER, user, () -> {
    processRequest();
});
```

Migrate from `ThreadLocal` when the value is set
once per scope, code runs on virtual threads, or
the value should be inherited by child tasks in
structured concurrency.
