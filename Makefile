build-api:
	docker compose build api

build-db:
	docker compose build db

evals:
	docker run --rm --name dialog-evals \
	-p 8081:8081 \
	--env-file .env \
	-v "./src:/app/src" \
	-v "./data:/data" \
	--network=dialog_default \
	dialog \
	/app/src/scripts/run_evals.sh