# Python

1. Run `uv init --no-readme --name {{project-name}}`,
   with the name chosen in phase 1b. This creates
   `pyproject.toml` and a `.python-version` file; the
   README comes from phase 5a.

2. If the user wants a web framework (FastAPI, Flask,
   Django) or any other dependency, add it with
   `uv add <package>`. To remove a dependency, use
   `uv remove <package>`.

3. Add the dev dependencies and the hot-reload command
   described in
   [Python tooling](../../project-rules/references/python/tooling.md).
