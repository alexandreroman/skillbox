# HTTP Servers

Language-agnostic best practices for HTTP server
configuration. Language-specific skills extend
these rules with their own additions.

## Port configuration

- **Read the port from the `PORT` environment
  variable** — this is the standard mechanism used
  by container orchestrators, PaaS platforms, and
  local tooling to assign a listen port at runtime.
- **Provide a sensible default** when `PORT` is not
  set. Use the convention of the framework or
  language:

| Framework / Language | Default port |
| -------------------- | ------------ |
| Spring Boot          | `8080`       |
| Express / Fastify    | `3000`       |
| Go `net/http`        | `8080`       |
| Flask / FastAPI      | `8000`       |
| Rust Actix / Axum    | `8080`       |

- **Never hard-code the port** — always read from
  the environment so the same image or binary works
  in any deployment context.
- **Bind to `0.0.0.0`** (all interfaces), not
  `127.0.0.1`, so the server is reachable inside a
  container or pod.
