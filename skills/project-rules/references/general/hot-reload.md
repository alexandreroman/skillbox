# Hot Reload

Every executable component of a project must ship
with a hot-reload mechanism for local development.
"Executable component" means anything you start and
keep running: an HTTP server, a worker, a CLI daemon,
a frontend dev server, a background job processor.

## Why

A code-generation tool — a coding assistant such as
Claude Code — iterates by making a change and
immediately observing its effect. Without hot reload,
every edit needs a manual stop/rebuild/restart cycle,
which breaks the feedback loop and slows the
assistant (and humans) down. Hot reload keeps the
running component in sync with the source so changes
take effect automatically.

## Rules

- **Provide a watch/reload dev command** for each
  executable component (for example a `dev` script,
  Makefile target, or Compose service) that rebuilds
  and restarts — or live-patches — on source change.
- **Use the idiomatic mechanism for the technology**
  rather than a custom file-watching shell loop.
- **Keep reload scoped to development.** Never enable
  auto-restart tooling or dev-only reloaders in
  production images or builds.
- **Make it the default entry point** for working on
  the component, so a coding assistant can start it
  and rely on changes being picked up.

## Idiomatic mechanisms

| Technology         | Hot-reload mechanism                     |
| ------------------ | ---------------------------------------- |
| Go                 | `air` (or `wgo`) watch + rebuild         |
| Java / Spring Boot | Spring Boot DevTools automatic restart   |
| Node.js / TS       | `tsx watch` or `nodemon`                 |
| Vite / Nuxt        | built-in HMR via the dev server          |
| Python (ASGI)      | `uvicorn --reload`                       |
| Python (Flask)     | debug mode reloader (`flask run --debug`)|

For other stacks, pick the community-standard watcher
or the framework's built-in reload feature.
