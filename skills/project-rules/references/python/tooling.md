# Tooling

Tool choices for Python projects.

## Project Management — uv

Use **uv** for the project, the virtual environment and
dependencies:

- `uv add <package>` / `uv add --dev <package>` to add
- `uv remove <package>` to remove
- Dev dependencies for a new project: `uv add --dev ruff
  pytest watchfiles` (add `watchfiles` only when hot
  reload needs it)
- `uv sync` to install
- `uv run <command>` to run anything inside the
  environment

## Lint and Format — ruff

Use **ruff** for both: `uv run ruff check .` and
`uv run ruff format .`.

## Testing — pytest

Use **pytest**: `uv run pytest`.

## Hot Reload

Run every command through `uv run`. Pick the mechanism
by framework:

| Framework     | Command                                  |
| ------------- | ---------------------------------------- |
| FastAPI       | `fastapi dev`                            |
| Flask         | `flask run --debug`                      |
| Django        | `manage.py runserver`                    |
| Other ASGI    | `uvicorn --reload`                       |
| Anything else | `watchfiles` (add with `uv add --dev`)   |
