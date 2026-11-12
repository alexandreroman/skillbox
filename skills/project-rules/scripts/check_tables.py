#!/usr/bin/env python3
"""Check that every Markdown table has vertically
aligned columns. Exit code 0 = all aligned,
1 = misalignment found."""

import re
import sys

FENCE = re.compile(r"^ *(?:(?:[-*+]|\d+[.)]) +)?(`{3,}|~{3,})(.*)$")
SEP = re.compile(r"(?<!\\)\|")


def check(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{path}: file not found", file=sys.stderr)
        return False
    except (OSError, UnicodeDecodeError) as e:
        print(f"{path}: cannot read file ({e.__class__.__name__})", file=sys.stderr)
        return False

    in_table = False
    tables: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []

    fence = ""
    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")
        m = FENCE.match(stripped)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = ""
            continue
        if m:
            fence = m.group(1)
            if in_table:
                tables.append(current)
                in_table = False
                current = []
            continue
        stripped = stripped.lstrip()
        if stripped.startswith("|"):
            if not in_table:
                in_table = True
                current = []
            current.append((i + 1, stripped))
        else:
            if in_table:
                tables.append(current)
                in_table = False
                current = []
    if in_table:
        tables.append(current)

    ok = True
    for table in tables:
        widths = [
            [len(c) for c in SEP.split(row)[1:-1]]
            for _, row in table
        ]
        ref = widths[0]
        for j, w in enumerate(widths):
            if w != ref:
                ok = False
                lineno = table[j][0]
                print(
                    f"{path}:{lineno}: "
                    f"col widths {w} "
                    f"(expected {ref})"
                )
    return ok


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_tables.py FILE ...")
        return 2
    results = [check(p) for p in argv]
    if all(results):
        print("All tables aligned.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
