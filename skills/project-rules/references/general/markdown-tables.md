# Markdown Tables

## Formatting rules

- Pad every cell with spaces so that each `|` in a
  column lines up vertically across all rows.
- Use `-` runs in the separator row that match the
  column width exactly.
- Keep one leading and one trailing space inside
  each cell (`| value |`, not `|value|`).

## Validation script

After writing or editing a Markdown file that
contains tables, run `scripts/check_tables.py` to
detect misaligned columns. Fix any reported lines
before considering the task complete.

```bash
python3 scripts/check_tables.py path/to/file.md
```

Pass multiple files to check them all in one run.
