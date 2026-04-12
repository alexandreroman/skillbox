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

3. Generate a `Makefile` with development-oriented
   targets. Adapt the targets to the chosen framework
   and dependencies. Use the following template as a
   starting point:

   ```makefile
   .DEFAULT_GOAL := help

   ##@ Development

   .PHONY: run
   run: ## Run the application
   	uv run python -m {{module_name}}

   .PHONY: dev
   dev: ## Run with auto-reload on file changes
   	uv run -- watchfiles \
   		'python -m {{module_name}}' src/

   .PHONY: install
   install: ## Install dependencies
   	uv sync

   ##@ Quality

   .PHONY: lint
   lint: ## Run linter
   	uv run ruff check .

   .PHONY: format
   format: ## Format code
   	uv run ruff format .

   .PHONY: test
   test: ## Run tests
   	uv run pytest

   ##@ Helpers

   .PHONY: help
   help: ## Show this help
   	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' \
   		$(MAKEFILE_LIST) | \
   		awk 'BEGIN {FS = ":.*?## "}; \
   		{printf "\033[36m%-15s\033[0m %s\n", \
   		$$1, $$2}'
   ```

   Adapt the template to the project:

   - **`{{module_name}}`**: replace with the Python
     module name (the `project-name` converted to
     snake_case).
   - **`dev` target**: if the project uses FastAPI,
     replace with
     `uv run -- fastapi dev src/{{module_name}}/main.py`;
     if it uses Flask, replace with
     `uv run -- flask --app {{module_name}} run --reload`;
     if it uses Django, replace with
     `uv run -- python manage.py runserver`;
     otherwise keep `watchfiles` and add it as
     a dev dependency with `uv add --dev watchfiles`.
   - **`test` target**: only include if the project
     is expected to have tests; add `pytest` as a
     dev dependency with `uv add --dev pytest`.
   - **`lint` / `format` targets**: add `ruff` as a
     dev dependency with `uv add --dev ruff`.
