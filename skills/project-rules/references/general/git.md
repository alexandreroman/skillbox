# Git

Language-agnostic conventions for working with Git.

## Commit messages

- **Start with a verb describing an action** — the
  subject line states what the commit does, in the
  imperative mood (e.g. `Add`, `Fix`, `Remove`,
  `Refactor`, `Bump`). Read it as "this commit will
  <subject>".
- **Prefer a verb + action over a noun or status** —
  write `Fix race condition in worker pool`, not
  `Race condition fix` or `worker bug`.
- **Keep the subject concise** — aim for 50 characters
  or fewer, no trailing period, capitalized first word.
- **Explain the why in the body**, not the what — the
  diff already shows what changed. Wrap the body at 72
  columns and separate it from the subject with a blank
  line.

| Prefer                          | Avoid                  |
| ------------------------------- | ---------------------- |
| `Add retry logic to client`     | `retry logic`          |
| `Fix null check in parser`      | `parser bug`           |
| `Remove unused import`          | `cleanup`              |
| `Bump version to 1.2.0`         | `version`              |
