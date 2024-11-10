################################################################################
# VARIABLES                                                                    #
################################################################################

NEO4J_USERNAME ?= neo4j
NEO4J_PASSWORD ?= supersecret
OLLAMA_MODELS ?= llama3.2 llama3.1:8b gemma2:9b

################################################################################
# COMMANDS                                                                     #
################################################################################

.PHONY: install
## Prepare example project (movies, model, app)
install: install-graphs install-models install-app

.PHONY: install-graphs
## Load the graph databases
install-graphs:
	docker compose ps --format "{{.Service}} {{.State}}" | \
		grep 'knowledge-graph running' || \
		docker compose up -d knowledge-graph
	./wait-for-it.sh localhost:7474 --strict -- wget --spider --no-verbose localhost:7474/

	docker compose exec knowledge-graph cypher-shell \
		--username "$(NEO4J_USERNAME)" \
		--password "$(NEO4J_PASSWORD)" \
		"CREATE DATABASE movies;"

	docker compose exec knowledge-graph cypher-shell \
		--username "$(NEO4J_USERNAME)" \
		--password "$(NEO4J_PASSWORD)" \
		--database 'movies' \
		--file '/opt/scripts/movies.cypher'

	docker compose exec knowledge-graph cypher-shell \
		--username "$(NEO4J_USERNAME)" \
		--password "$(NEO4J_PASSWORD)" \
		"CREATE DATABASE starwars;"

	docker compose exec knowledge-graph cypher-shell \
		--username "$(NEO4J_USERNAME)" \
		--password "$(NEO4J_PASSWORD)" \
		--database 'starwars' \
		--file '/opt/scripts/star-wars.cypher'

.PHONY: install-models
## Preload Ollama models
install-models:
	docker compose ps --format "{{.Service}} {{.State}}" | \
		grep 'ollama running' || \
		docker compose up -d ollama
	./wait-for-it.sh localhost:11434 --strict -- wget --spider --no-verbose localhost:11434/

	for model in $(OLLAMA_MODELS); do \
		docker compose exec ollama ollama pull "$$model"; \
	done

.PHONY: install-app
## Generate wheel and build Docker image
install-app:
	cd ..; hatch run example:deploy
	docker compose build

################################################################################
# Self Documenting Commands                                                    #
################################################################################

.DEFAULT_GOAL := show-help

# Inspired by
# <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && \
		echo '--no-init --raw-control-chars')
