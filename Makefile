build-api:
	docker compose build api

build-db:
	docker compose build db

db:
	docker compose up db

dialog:
	docker compose up dialog

evals:
	docker compose --profile evals up evals
	docker compose down