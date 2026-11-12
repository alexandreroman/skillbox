# Python

## Variables

| Variable            | Source |
|---------------------|--------|
| `project-name`      | Step 2 |
| `short-description` | Step 1 |

## Steps

1. Run `uv init --no-readme --name {{project-name}}` to
   bootstrap the project. This creates `pyproject.toml`
   and a `.python-version` file; the README comes from
   phase 5a.

2. If the user wants a web framework (FastAPI, Flask,
   Django) or any other dependency, add it with
   `uv add <package>`. To remove a dependency, use
   `uv remove <package>`.

3. Add the dev dependencies and the hot-reload command
   described in
   [Python tooling](../../project-rules/references/python/tooling.md).
