# Python

## Variables

| Variable | Source |
|---|---|
| `project-name` | Step 2 |
| `short-description` | Step 1 |

## Steps

1. Create a `pyproject.toml` with the project
   metadata using the standard format:

```toml
[project]
name = "{{project-name}}"
version = "0.1.0"
description = "{{short-description}}"
requires-python = ">=3.13"
dependencies = []
```

2. If the user wants a web framework (FastAPI, Flask,
   Django), add it to `dependencies` and scaffold
   the conventional directory structure.
