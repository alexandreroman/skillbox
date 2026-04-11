# Collections & Streams

Goal: use modern collection APIs and Stream
enhancements for cleaner, more expressive code.

## Immutable Collection Factories (Java 9+)

Replace verbose collection initialization with
factory methods:

```java
// Before
List<String> list = Collections.unmodifiableList(
    Arrays.asList("a", "b", "c"));
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);
Map<String, Integer> umap =
    Collections.unmodifiableMap(map);

// After
List<String> list = List.of("a", "b", "c");
Map<String, Integer> map = Map.of("a", 1, "b", 2);
```

**Important:** `List.of()`, `Set.of()`, and
`Map.of()` return unmodifiable collections that
do not allow `null` elements.

## toList() on Streams (Java 16+)

Replace `.collect(Collectors.toList())` with
`.toList()`:

```java
// Before
var names = people.stream()
    .map(Person::name)
    .collect(Collectors.toList());

// After
var names = people.stream()
    .map(Person::name)
    .toList();
```

**Note:** `.toList()` returns an unmodifiable list.
If a mutable list is needed, keep using
`.collect(Collectors.toCollection(ArrayList::new))`.

## Sequenced Collections (Java 21+)

Use the `SequencedCollection`, `SequencedSet`, and
`SequencedMap` interfaces when order matters:

```java
// Access first/last elements uniformly
SequencedCollection<String> seq = ...;
String first = seq.getFirst();
String last = seq.getLast();

// Reverse view
SequencedCollection<String> reversed =
    seq.reversed();
```

Prefer `SequencedCollection` over `List` in method
signatures when only ordered access (not indexing)
is needed.

## Stream Gatherers (Java 24+)

Use `Stream.gather()` with built-in gatherers for
operations that were previously awkward:

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

Prefer built-in gatherers (`windowFixed`,
`windowSliding`, `fold`, `scan`,
`mapConcurrent`) over hand-rolled stateful
stream operations.

## mapMulti (Java 16+)

Use `mapMulti` as a lighter alternative to
`flatMap` when producing zero or few elements
per input:

```java
// Before
orders.stream()
    .flatMap(o -> o.items().stream())
    .toList();

// After (avoids intermediate stream creation)
orders.stream()
    .<Item>mapMulti((order, downstream) -> {
        for (var item : order.items()) {
            downstream.accept(item);
        }
    })
    .toList();
```

Use `mapMulti` when the mapping logic is
imperative or conditional. Prefer `flatMap` when
the mapping is a simple method reference.

## Checklist

- [ ] `List.of()` / `Set.of()` / `Map.of()` for
      immutable collection literals
- [ ] `.toList()` instead of
      `.collect(Collectors.toList())`
- [ ] `SequencedCollection` where order matters
      but indexing is not needed
- [ ] Stream gatherers for windowing, batching,
      and stateful operations
