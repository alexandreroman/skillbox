# Integration mode

For an existing repository adopting skillbox. Everything
here is **additive and idempotent**: add only what is
missing, never rewrite, reorder, or overwrite existing
content, so a second run changes nothing. Phases named
below are those of the init-project skill.

## Plan

Create the following tasks in order:

1. Choose the instruction file
2. Add the missing sections
3. Open the project memory
4. Offer the missing files
5. Review and confirm

## Choose the instruction file

Look for `AGENTS.md` and `CLAUDE.md` at the root.

| Found            | Write to    | Then                            |
| ---------------- | ----------- | ------------------------------- |
| `AGENTS.md` only | `AGENTS.md` | Nothing else                    |
| Neither          | `AGENTS.md` | Create it from the template     |
| `CLAUDE.md` only | `CLAUDE.md` | Offer to move it to `AGENTS.md` |
| Both             | `AGENTS.md` | Ensure `CLAUDE.md` imports it   |

- **Move offer** — ask whether to rename `CLAUDE.md`
  to `AGENTS.md` with `git mv`. Move nothing without an
  explicit yes; on no or silence, leave it in place.
- **Both exist** — make sure `CLAUDE.md` contains the
  line `@AGENTS.md`; append it only when missing and
  leave the rest of the file as it is.
- A missing `AGENTS.md` is created from
  [assets/AGENTS.md](../assets/AGENTS.md), as in
  phase 2a.

## Add the missing sections

Compare the target file's headings with the **Agents**
and **Memory** sections of the template. Append each
section whose heading is missing, copied as in phase 2a.
Leave every existing section untouched, even when it
differs from the template. Then read the file back and
adopt it as in phase 2b.

## Open the project memory

Invoke **project-memory** as in phase 2c: it creates
`.claude/project-memory/MEMORY.md` only when missing.

When the memory holds no project context yet, draft a
short summary from the code and the instruction file:
the objective, the target audience, the tech stack, and
any visible constraint. Show it to the user in one
question and ask them to confirm or correct it. Record
only what they confirm, plus the decisions they made
during this run; record nothing inferred that they did
not confirm. Skip this when the memory already covers
the project.

## Offer the missing files

For each piece below that is missing, ask separately
and create it only when the user accepts. Never
overwrite an existing file.

- **Makefile** — per the project-rules rules in
  `references/general/makefile.md`, as in phase 4a.
- **README.md** — delegate to **write-readme**, as in
  phase 5a.
- **LICENSE** — ask which license, then write it as in
  phase 5b.

Finish with phase 6: show what changed and ask whether
anything needs adjusting.
