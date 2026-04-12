---
name: project-memory
description: >-
  PROACTIVE — invoke this skill automatically,
  without being asked, whenever the conversation
  reveals project decisions, deadlines, team
  context, external references, workflow
  preferences, or corrective feedback that should
  persist across conversations. Also invoke when
  the user says "remember", "don't forget",
  "keep track of", "note that", or asks to recall
  something previously saved. Do not wait for an
  explicit request — if the information is worth
  remembering, invoke this skill immediately.
allowed-tools: Read, Write, Edit, Glob
---

# Project Memory

Persistent, file-based memory system. Memory
directory depends on context:

- Main conversation:
  `<project root>/.claude/memory/`
- Subagent:
  `<project root>/.claude/agent-memory/<agent-name>/`

Create the directory if it does not exist.

## When to save — trigger checklist

Save a memory whenever:

- The user explicitly asks ("remember this",
  "note that", "keep track of").
- The user shares a **decision** and its
  rationale.
- The user mentions a **deadline**, milestone,
  or schedule constraint.
- The user describes **team context**: who owns
  what, who to ask, org changes.
- The user corrects your approach or confirms
  a non-obvious approach worked.
- The user points to an **external resource**
  (URL, dashboard, issue tracker, chat channel).
- The user shares **workflow preferences**
  that should carry across conversations.

To forget: find and remove the relevant entry.

## How to save

**Step 1** — Read `references/memory-types.md`
(next to this SKILL.md) to pick the right type
and body structure.

**Step 2** — Write a file (e.g.
`feedback_testing.md`, `project_deadline.md`)
with this frontmatter:

```yaml
---
name: "memory name (in English)"
description: "one-line description (in English)"
type: feedback | project | reference
---
```

Write all memory content in English, regardless
of the conversation language.

**Step 3** — Add a pointer in `MEMORY.md`.
One line per entry, under 150 characters:
`- [Title](file.md) — one-line hook`.
Keep the index concise (max 200 lines).
Check for duplicates before writing.

## Before saving or recalling

Read `references/guidelines.md` (next to this
SKILL.md) to check exclusion rules, access
rules, and persistence boundaries.
