# Python

## Variables

| Variable            | Source |
|---------------------|--------|
| `project-name`      | Step 2 |
| `short-description` | Step 1 |

## Steps

1. Run `uv init --name {{project-name}}` to bootstrap
   the project. This creates `pyproject.toml`, a
   `README.md` stub, and a `.python-version` file.

2. If the user wants a web framework (FastAPI, Flask,
   Django) or any other dependency, add it with
   `uv add <package>`. To remove a dependency, use
   `uv remove <package>`.

3. Generate the `Makefile` following
   [the Makefile rule](../../project-rules/references/general/makefile.md),
   adapted to the chosen framework and dependencies
   (`{{module_name}}` is the `project-name` converted
   to snake_case).

4. Add the dev dependencies and the hot-reload command
   described in
   [Python tooling](../../project-rules/references/python/tooling.md).
