# Makefile for argus-agent (monorepo root)

# ─── Development ──────────────────────────────────────────────────────────────

.PHONY: dev
dev: sync-deps ## Start backend + frontend concurrently
	@echo "Starting argus-agent dev environment..."
	$(MAKE) -j2 dev-backend dev-frontend

.PHONY: dev-backend
dev-backend: ## Start backend dev server (port 8000)
	cd backend && $(MAKE) dev

.PHONY: dev-frontend
dev-frontend: ## Start frontend dev server (port 5173)
	cd frontend && $(MAKE) dev

.PHONY: sync-deps
sync-deps: ## Sync backend + frontend dependencies
	cd backend && $(MAKE) install-dev
	cd frontend && $(MAKE) install

.PHONY: install
install: sync-deps ## Install all dependencies

# ─── Help ─────────────────────────────────────────────────────────────────────

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
