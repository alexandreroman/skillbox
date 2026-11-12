# Go

1. Ask the user for the module owner (GitHub username
   or organization), even when a default seems
   obvious. Propose one from the repository's remote
   or `git config` if available, but never derive it
   from an unrelated URL such as a plugin's
   repository.

2. Run `go mod init github.com/{{owner}}/{{project-name}}`,
   with the owner from step 1 and the name chosen in
   phase 1b.

3. Set up linting, formatting and hot reload as
   described in
   [Go tooling](../../project-rules/references/go/tooling.md).
