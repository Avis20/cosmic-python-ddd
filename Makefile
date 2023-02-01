.DEFAULT_GOAL := help


.PHONY: up
up: ## Up all services locally with docker-compose
	touch .docker.env
	docker-compose up --build --no-log-prefix


.PHONY: uninstall
uninstall: ## Complete remove containers and named volumes
	docker-compose down --remove-orphans --volumes


.PHONY: clean-python
clean-python: ## Remove pycache
	bash -c 'find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf'


.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
