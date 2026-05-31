PYTHON := uv run

SOURCE_DIR := src
CODE := $(SOURCE_DIR)
TESTS := tests

.PHONY: dev
dev:
	uv sync --all-groups --all-extras --all-packages
	$(PYTHON) pre-commit install
	@echo Development environment ready!

.PHONY: format
format:
	$(PYTHON) ruff format $(CODE)
	$(PYTHON) ruff check --show-fixes --fix $(CODE)
	@echo Code formatting complete!

.PHONY: type
type:
	$(PYTHON) mypy $(CODE)
	@echo Type checking complete!

.PHONY: test
test:
	$(PYTHON) pytest $(TESTS)
	@echo Tests complete!

.PHONY: all
all: format type test
