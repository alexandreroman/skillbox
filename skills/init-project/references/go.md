# Go

## Variables

| Variable       | Source                                 |
|----------------|----------------------------------------|
| `owner`        | Ask the user or read from `git config` |
| `project-name` | Step 2                                 |

## Steps

1. Ask the user to confirm the module owner
   if it cannot be inferred from `git config`
   (e.g. GitHub username or organization).

2. Run `go mod init github.com/{{owner}}/{{project-name}}`

3. Generate the `Makefile` following
   [the Makefile rule](../../project-rules/references/general/makefile.md),
   adapted to the chosen framework and project type
   (replace `{{project-name}}` with the name chosen in
   Step 2).

4. Set up linting, formatting and hot reload as
   described in
   [Go tooling](../../project-rules/references/go/tooling.md).
