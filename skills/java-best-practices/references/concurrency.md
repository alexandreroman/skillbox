# Concurrency

Goal: leverage virtual threads and modern
concurrency primitives for simpler, more scalable
concurrent code.

## Virtual Threads (Java 21+)

Virtual threads are lightweight threads managed
by the JVM. Use them for I/O-bound tasks instead
of platform thread pools.

### Creating virtual threads

```java
// One-off task
Thread.startVirtualThread(() -> handleRequest());

// Executor for task submission
try (var executor =
        Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> fetchFromDb());
    executor.submit(() -> callExternalApi());
}
```

### When to use virtual threads

- **Use for:** I/O-bound workloads (HTTP calls,
  database queries, file I/O, message consumers).
- **Avoid for:** CPU-bound computation — virtual
  threads do not add parallelism beyond available
  cores.

### Migration guidelines

- Replace `Executors.newFixedThreadPool(n)` with
  `Executors.newVirtualThreadPerTaskExecutor()`
  for I/O-bound work.
- Remove manual thread-pool sizing — virtual
  threads scale automatically.
- Avoid `synchronized` blocks that guard I/O
  operations — they pin virtual threads to platform
  threads. Use `ReentrantLock` instead:

```java
// Before (pins virtual thread)
synchronized (lock) {
    connection.query(...);
}

// After
private final ReentrantLock lock =
    new ReentrantLock();

lock.lock();
try {
    connection.query(...);
} finally {
    lock.unlock();
}
```

- Avoid thread-local variables in virtual-thread
  contexts — they consume memory per virtual thread.
  Consider scoped values instead.

## Structured Concurrency (Preview)

Structured concurrency ensures that concurrent
subtasks are managed as a unit: if one fails, the
others are cancelled.

**Note:** Structured concurrency is a preview
feature. Check the project's compiler flags before
suggesting it. Only propose it if the user
explicitly opts in to preview features.

```java
try (var scope =
        StructuredTaskScope.open()) {
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

Scoped values are an immutable, virtual-thread
friendly alternative to `ThreadLocal`.

**Note:** Scoped values are a preview feature.
Same guidance as structured concurrency — only
suggest if the user opts in.

```java
private static final ScopedValue<User> CURRENT_USER =
    ScopedValue.newInstance();

ScopedValue.runWhere(CURRENT_USER, user, () -> {
    // CURRENT_USER.get() available in this scope
    // and all tasks forked from it
    processRequest();
});
```

**When to migrate from ThreadLocal:**

- The value is set once and read many times
  (immutable per scope).
- The code runs on virtual threads where
  `ThreadLocal` is wasteful.
- The value should be inherited by child tasks
  in structured concurrency.

## Checklist

- [ ] Virtual threads for I/O-bound executors
- [ ] No `synchronized` blocks guarding I/O
      (use `ReentrantLock`)
- [ ] No unnecessary thread-pool sizing for
      I/O workloads
- [ ] Structured concurrency for fan-out patterns
      (if preview features are enabled)
- [ ] Scoped values instead of `ThreadLocal`
      (if preview features are enabled)
