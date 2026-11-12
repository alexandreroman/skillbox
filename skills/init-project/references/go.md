# Go

## Variables

| Variable       | Source                                 |
|----------------|----------------------------------------|
| `owner`        | Asked in step 1                        |
| `project-name` | Step 2                                 |

## Steps

1. Ask the user for the module owner (GitHub username
   or organization), even when a default seems
   obvious. Propose one from the repository's remote
   or `git config` if available, but never derive it
   from an unrelated URL such as a plugin's
   repository.

2. Run `go mod init github.com/{{owner}}/{{project-name}}`

3. Set up linting, formatting and hot reload as
   described in
   [Go tooling](../../project-rules/references/go/tooling.md).
