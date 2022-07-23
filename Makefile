DEFAULT_GOAL := help

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[35m  %-25s\033[0m %s\n", $$1, $$2}'

lint-all:	black

black: ## Format code using black
	@echo "--- Performing black reformatting ---"
	black . --check

pylama:	## Perform python linting using pylama
	@echo "--- Performing pylama linting ---"
	pylama .

yamllint:	## Perform YAML linting using yamllint
	@echo "--- Performing yamllint linting ---"
	yamllint .