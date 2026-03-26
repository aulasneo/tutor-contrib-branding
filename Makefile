.DEFAULT_GOAL := help
.PHONY: docs

PYTHON ?= python3
SRC_DIRS = ./tutorbranding
BLACK_OPTS = --exclude templates ${SRC_DIRS}

clean: ## Remove build artifacts
	rm -rf build dist *.egg-info

upgrade: ## Compile requirements from requirements.in
	pip-compile

requirements: ## Install requirements from requirements.txt
	$(PYTHON) -m pip install --upgrade -r requirements.txt
	$(PYTHON) -m pip install -e .

build: clean ## Build the package
	$(PYTHON) -m build

dist: ## Upload package to PyPI
	twine upload dist/*

# Warning: These checks are not necessarily run on every PR.
test: test-lint test-types test-format test-dist test-tutor ## Run some static checks.

test-format: ## Run code formatting tests
	black --check --diff $(BLACK_OPTS)

test-lint: ## Run code linting tests
	pylint --errors-only --enable=unused-import,unused-argument --ignore=templates --ignore=docs/_ext ${SRC_DIRS}

test-types: ## Run type checks.
	mypy --exclude=templates --ignore-missing-imports --implicit-reexport --strict ${SRC_DIRS}

test-dist: build ## Check the distribution files
	twine check dist/*

test-tutor:
	export TUTOR_ROOT=$$(pwd) && tutor config save
	tutor plugins enable branding

format: ## Format code automatically
	black $(BLACK_OPTS)

isort: ##  Sort imports. This target is not mandatory because the output may be incompatible with black formatting. Provided for convenience purposes.
	isort --skip=templates ${SRC_DIRS}

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
