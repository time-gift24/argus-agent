# Makefile for argus-agents frontend

# ─── Variables ───────────────────────────────────────────────────────────────
PORT       := 5173
API_TARGET := http://localhost:8000

# ─── Development ──────────────────────────────────────────────────────────────

.PHONY: dev
dev: ## Start dev server (proxy to local backend, port 5173)
	npx vite --port $(PORT) --open

.PHONY: dev-remote
dev-remote: ## Start dev server proxying to remote API (set API_TARGET)
	npx vite --port $(PORT) --open --mode development

# ─── Production ───────────────────────────────────────────────────────────────

.PHONY: build
build: ## Build for production
	npx vite build

.PHONY: preview
preview: build ## Build and preview production bundle
	npx vite preview --port $(PORT) --open

# ─── Dependencies ─────────────────────────────────────────────────────────────

.PHONY: install
install: ## Install dependencies
	npm install

.PHONY: clean
clean: ## Remove node_modules and build output
	rm -rf node_modules dist

# ─── Help ─────────────────────────────────────────────────────────────────────

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
