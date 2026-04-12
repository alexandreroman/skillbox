# Go

## Variables

| Variable       | Source                                 |
|----------------|----------------------------------------|
| `owner`        | Ask the user or read from `git config` |
| `project-name` | Step 2                                 |

## Steps

1. Use AskUserQuestion to confirm the module owner
   if it cannot be inferred from `git config`
   (e.g. GitHub username or organization).

2. Run `go mod init github.com/{{owner}}/{{project-name}}`
