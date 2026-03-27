# Makefile for argus-agents backend

# ─── Variables ───────────────────────────────────────────────────────────────
PYTHON := python
PYTEST_ARGS := -v --tb=short
COVERAGE_MIN := 80

# ─── Test Targets ─────────────────────────────────────────────────────────────

.PHONY: test
test: ## Run all tests
	$(PYTHON) -m pytest $(PYTEST_ARGS) tests/

.PHONY: test-unit
test-unit: ## Run unit tests only
	$(PYTHON) -m pytest $(PYTEST_ARGS) -m unit tests/

.PHONY: test-integration
test-integration: ## Run integration tests only
	$(PYTHON) -m pytest $(PYTEST_ARGS) -m integration tests/

.PHONY: test-cov
test-cov: ## Run all tests with coverage (minimum 80%)
	$(PYTHON) -m pytest $(PYTEST_ARGS) --cov=app --cov=tests \
		--cov-fail-under=$(COVERAGE_MIN) tests/

.PHONY: test-cov-report
test-cov-report: ## Run all tests with detailed coverage report
	$(PYTHON) -m pytest $(PYTEST_ARGS) --cov=app --cov=tests \
		--cov-report=term-missing:skip-covered \
		--cov-report=html:htmlcov tests/
	@echo "Coverage report generated at htmlcov/index.html"

.PHONY: test-cov-open
test-cov-open: test-cov-report ## Run coverage and open report in browser
	@open htmlcov/index.html 2>/dev/null || echo "Open htmlcov/index.html manually"

# ─── Development Helpers ──────────────────────────────────────────────────────

.PHONY: install-dev
install-dev: ## Install dev dependencies (including test tooling)
	uv sync --dev

.PHONY: check-deps
check-deps: ## Check that test dependencies are installed
	@$(PYTHON) -c "import pytest; import pytest_asyncio; import httpx" 2>/dev/null \
		|| (echo "Missing test dependencies. Run: make install-dev")

.PHONY: fmt
fmt: ## Format code (ruff)
	ruff format app/ tests/
	ruff check --fix app/ tests/

.PHONY: lint
lint: ## Lint code
	ruff check app/ tests/

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
