# Developer task runner. Run `make` (or `make help`) to
# list the available targets.

.DEFAULT_GOAL := help

# Canonical environment, loaded for every target.
# A missing .env file is not an error.
ifneq (,$(wildcard .env))
include .env
export
endif

# Local overrides, loaded only for dev/test targets so that
# deploy/release targets see the canonical .env values only.
# Sequential include means later assignments win.
DEV_TARGETS := dev test check infra-up infra-down infra-logs {{dev-targets}}
GOALS := $(or $(MAKECMDGOALS),$(.DEFAULT_GOAL))
ifneq (,$(filter $(DEV_TARGETS),$(GOALS)))
ifneq (,$(wildcard .env.local))
include .env.local
export
endif
endif

##@ Infra

.PHONY: infra-up
infra-up: ## Start local infrastructure services (databases, brokers, ...)
	{{compose}} up -d {{infra-services}}

.PHONY: infra-down
infra-down: ## Stop local infrastructure services
	{{compose}} stop {{infra-services}}

.PHONY: infra-logs
infra-logs: ## Follow logs from infrastructure services
	{{compose}} logs -f {{infra-services}}

##@ Develop

.PHONY: dev
dev: infra-up ## Start infra, then run the app locally with hot reload
	# Trap reaps the whole process group (kill 0) on exit or signal, so no
	# orphaned processes survive Ctrl-C or a child crash. For multiple dev
	# processes, background each as `( cmd; kill 0 ) &` before the wait.
	@trap 'kill 0' EXIT INT TERM; \
		{{dev-command}} & \
		wait

##@ Stack

.PHONY: app-up
app-up: ## Bring up the full stack in containers (build + start)
	{{compose}} up -d --build

.PHONY: app-down
app-down: ## Tear down the full stack (removes containers and network)
	{{compose}} down

.PHONY: app-logs
app-logs: ## Follow logs from every stack container
	{{compose}} logs -f

##@ Quality

.PHONY: test
test: ## Run the test suite
	{{test-command}}

.PHONY: check
check: test ## Run tests and static checks
	{{lint-command}}

##@ Build

.PHONY: build
build: ## Build the production artifact
	{{build-command}}

##@ Helpers

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(firstword $(MAKEFILE_LIST))
