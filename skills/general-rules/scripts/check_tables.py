#!/usr/bin/env python3
"""Check that every Markdown table has vertically
aligned columns. Exit code 0 = all aligned,
1 = misalignment found."""

import sys


def check(path: str) -> bool:
    with open(path) as f:
        lines = f.readlines()

    in_table = False
    tables: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []

    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")
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
            [len(c) for c in row.split("|")[1:-1]]
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


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        print("usage: check_tables.py FILE ...")
        sys.exit(2)
    all_ok = all(check(p) for p in paths)
    if all_ok:
        print("All tables aligned.")
    sys.exit(0 if all_ok else 1)
