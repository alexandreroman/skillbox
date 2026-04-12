# Memory Guidelines

## What NOT to save

- Code patterns, architecture, file paths, or
  project structure — derivable from the current
  project state.
- Git history or who-changed-what — use
  `git log`.
- Debugging solutions — the fix is in the code.
- Anything already in CLAUDE.md files.
- Ephemeral task details or current conversation
  context.
- Personal user data (role, preferences,
  identity) — these belong in `~/.claude/`
  (user-level), not in a shared project
  repository.

## When to access memories

- When memories seem relevant, or the user
  references prior-conversation work.
- You MUST access memory when the user
  explicitly asks.
- If the user says to *ignore* memory, do not
  use it.
- Verify stale memories against current state
  before acting on them.

## Before recommending from memory

- If the memory names a file path: check it
  exists.
- If the memory names a function or flag: grep
  for it.
- If the user is about to act on your
  recommendation, verify first.

## Memory vs other persistence

- Use a **plan** (not memory) for implementation
  alignment within a conversation.
- Use **tasks** (not memory) for tracking current
  conversation progress.
- This memory is project-scope and shared via
  version control — tailor memories to this
  project.
