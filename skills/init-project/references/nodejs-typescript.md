# Node.js / TypeScript

Run the appropriate scaffolding command:

- **Plain Node.js**: `npm init -y`
- **Next.js**: `npx create-next-app@latest . --ts`
- **Vite + React**:
  `npm create vite@latest . -- --template react-ts`
- **Vite + Nuxt**: `npx nuxi@latest init .`

Preferred option: **Vite + Nuxt**.
Use AskUserQuestion to confirm the framework choice
if not explicitly stated.

## Makefile

After scaffolding, generate a `Makefile` — thin
wrapper around pnpm scripts with a composite
`check` target:

```makefile
.DEFAULT_GOAL := help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev: ## Start dev server with hot reload
	pnpm dev

build: ## Compile TypeScript
	pnpm build

start: ## Run compiled app
	pnpm start

test: ## Run tests
	pnpm test

test-watch: ## Run tests in watch mode
	pnpm test:watch

coverage: ## Run tests with coverage
	pnpm test:coverage

typecheck: ## Type-check without emitting
	pnpm typecheck

lint: ## Run linter
	pnpm lint

lint-fix: ## Run linter with auto-fix
	pnpm lint:fix

format: ## Format all files
	pnpm format

format-check: ## Check formatting
	pnpm format:check

check: typecheck lint format-check test ## Run all checks (CI)

clean: ## Remove build artifacts
	pnpm clean
```

Adapt targets when using a framework (Nuxt,
Next.js) — remove `build`/`start` if the
framework provides its own.
