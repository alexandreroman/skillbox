# Collections & Streams

Well-known features (`List.of()`, `.toList()`,
`mapMulti`) are omitted — apply from general
knowledge.

## Stream Gatherers (Java 24+)

`Stream.gather()` with built-in gatherers replaces
hand-rolled stateful stream operations:

```java
import java.util.stream.Gatherers;

// Sliding windows
list.stream()
    .gather(Gatherers.windowSliding(3))
    .forEach(window -> process(window));

// Fixed-size groups
list.stream()
    .gather(Gatherers.windowFixed(10))
    .forEach(batch -> sendBatch(batch));

// Fold (stateful reduction with early termination)
var result = stream
    .gather(Gatherers.fold(
        () -> initialState,
        (state, element) -> combine(state, element)))
    .findFirst()
    .orElse(defaultState);
```

Built-in gatherers: `windowFixed`, `windowSliding`,
`fold`, `scan`, `mapConcurrent`.

## Sequenced Collections (Java 21+)

Prefer `SequencedCollection` over `List` in method
signatures when only ordered access (not indexing)
is needed. Provides `getFirst()`, `getLast()`, and
`reversed()`.

## Checklist

- [ ] Stream gatherers for windowing, batching,
      and stateful operations
- [ ] `SequencedCollection` in signatures where
      only ordered access is needed
