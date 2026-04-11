---
name: agent-memory
description: >-
  Persistent file-based memory system. Manages
  feedback, project, and reference memories. Use when
  context needs to be remembered across conversations.
---

# Persistent Memory

You have a persistent, file-based memory system.
The memory directory is determined by context:

- Main conversation: `<project root>/.claude/memory/`
- Subagent: `<project root>/.claude/agent-memory/<agent-name>/`

Create the directory if it does not exist.

Build up this memory system over time so that future
conversations retain project context, collaboration
preferences, and the reasoning behind decisions.

If the user explicitly asks you to remember something,
save it immediately. If they ask you to forget
something, find and remove the relevant entry.

## Types of memory

<types>
<type>
    <name>feedback</name>
    <description>Guidance the user has given about how to approach work — both what to avoid and what to keep doing. Record from failure AND success.</description>
    <when_to_save>Any time the user corrects your approach OR confirms a non-obvious approach worked. Include *why* so you can judge edge cases later.</when_to_save>
    <how_to_use>Let these memories guide your behavior so that the user does not need to offer the same guidance twice.</how_to_use>
    <body_structure>Lead with the rule, then a **Why:** line and a **How to apply:** line.</body_structure>
</type>
<type>
    <name>project</name>
    <description>Information about ongoing work, goals, initiatives, bugs, or incidents not derivable from code or git history.</description>
    <when_to_save>When you learn who is doing what, why, or by when. Convert relative dates to absolute dates.</when_to_save>
    <how_to_use>Use to understand the broader context and motivation behind the user's request.</how_to_use>
    <body_structure>Lead with the fact or decision, then a **Why:** line and a **How to apply:** line.</body_structure>
</type>
<type>
    <name>reference</name>
    <description>Pointers to where information can be found in external systems.</description>
    <when_to_save>When you learn about resources in external systems and their purpose.</when_to_save>
    <how_to_use>When the user references an external system or information that may be in one.</how_to_use>
</type>
</types>

## What NOT to save

- Code patterns, architecture, file paths, or project
  structure — derivable from the current project state.
- Git history or who-changed-what — use `git log`.
- Debugging solutions — the fix is in the code.
- Anything already in CLAUDE.md files.
- Ephemeral task details or current conversation context.
- Personal user data (role, preferences, identity) —
  these belong in `~/.claude/` (user-level), not in
  a shared project repository.

## How to save memories

**Step 1** — write a file (e.g. `feedback_testing.md`,
`project_deadline.md`) with this frontmatter:

```yaml
---
name: "memory name"
description: "one-line description"
type: feedback | project | reference
---
```

**Step 2** — add a pointer in `MEMORY.md`. One line
per entry, under 150 characters:
`- [Title](file.md) — one-line hook`.

- Keep the index concise (max 200 lines).
- Organize by topic, not chronologically.
- Update or remove stale memories.
- Check for duplicates before writing.

## When to access memories

- When memories seem relevant, or the user references
  prior-conversation work.
- You MUST access memory when the user explicitly asks.
- If the user says to *ignore* memory, do not use it.
- Verify stale memories against current state before
  acting on them.

## Before recommending from memory

- If the memory names a file path: check it exists.
- If the memory names a function or flag: grep for it.
- If the user is about to act on your recommendation,
  verify first.

## Memory and other forms of persistence

- Use a **plan** (not memory) for implementation
  alignment within a conversation.
- Use **tasks** (not memory) for tracking current
  conversation progress.
- This memory is project-scope and shared via version
  control — tailor memories to this project.

