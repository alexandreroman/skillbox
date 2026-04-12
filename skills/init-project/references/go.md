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

3. Generate a `Makefile` with development-oriented
   targets. Adapt the targets to the chosen framework
   and project type. Use the following template as a
   starting point:

   ```makefile
   .DEFAULT_GOAL := help

   BINARY := {{project-name}}

   ##@ Development

   .PHONY: run
   run: ## Run the application
   	go run .

   .PHONY: dev
   dev: ## Run with hot-reload (requires Air)
   	air

   .PHONY: build
   build: ## Build the binary
   	go build -o $(BINARY) .

   ##@ Quality

   .PHONY: test
   test: ## Run tests
   	go test ./...

   .PHONY: lint
   lint: ## Run linter (requires golangci-lint)
   	golangci-lint run ./...

   .PHONY: format
   format: ## Format code
   	gofmt -w .
   	goimports -w .

   .PHONY: vet
   vet: ## Run static analysis
   	go vet ./...

   .PHONY: check
   check: vet lint test ## Run all checks

   ##@ Helpers

   .PHONY: tidy
   tidy: ## Tidy and verify module dependencies
   	go mod tidy
   	go mod verify

   .PHONY: help
   help: ## Show this help
   	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' \
   		$(MAKEFILE_LIST) | \
   		awk 'BEGIN {FS = ":.*?## "}; \
   		{printf "\033[36m%-15s\033[0m %s\n", \
   		$$1, $$2}'
   ```

   Adapt the template to the project:

   - **`{{project-name}}`**: replace with the actual
     project name chosen in Step 2.
   - **`run` target**: if the project uses a web
     framework (Gin, Echo, Chi, Fiber), keep `go run .`;
     for CLI tools, keep the same.
   - **`build` target**: for multi-platform builds,
     add `GOOS` and `GOARCH` variables if relevant.
   - **`lint` target**: relies on
     [golangci-lint](https://golangci-lint.run/).
     Also generate a `.golangci.yml` configuration
     file enabling these linters at a minimum:
     `errcheck`, `govet`, `staticcheck`, `unused`,
     `gosimple`, `ineffassign`.
   - **`format` target**: uses `gofmt` (included in
     Go) and `goimports` (from `golang.org/x/tools`).
     Run `go install golang.org/x/tools/cmd/goimports@latest`
     to make it available.
   - **`dev` target**: uses
     [Air](https://github.com/air-verse/air) for
     hot-reload during development. Install with
     `go install github.com/air-verse/air@latest`.
     Also generate a `.air.toml` configuration file
     setting `cmd = "go build -o ./tmp/{{project-name}} ."`
     and `bin = "./tmp/{{project-name}}"`.
   - **`test` target**: always include; Go has
     built-in testing support.
