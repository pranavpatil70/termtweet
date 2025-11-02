.PHONY: help install test build publish clean setup dev-setup

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package locally
	pip install -e .

setup: ## Run the interactive setup
	termtweet --setup

test: ## Run tests
	python -m pytest

build: ## Build the package
	python -m build

check: ## Check the built package
	python -m twine check dist/*

publish-test: ## Publish to Test PyPI
	python -m twine upload --repository testpypi dist/*

publish: ## Publish to PyPI
	python -m twine upload dist/*

clean: ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .coverage

dev-setup: ## Setup development environment
	pip install -r requirements.txt
	pip install pytest pytest-cov twine build

lint: ## Run linting
	python -m flake8 termtweet/ --count --select=E9,F63,F7,F82 --show-source --statistics
	python -m flake8 termtweet/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Format code with black
	python -m black termtweet/

check-format: ## Check code formatting
	python -m black --check termtweet/

release: clean build check ## Build and check package for release

# Default target
.DEFAULT_GOAL := help