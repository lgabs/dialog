build-api:
	docker compose build api

build-db:
	docker compose build db

evals:
	docker run --rm --name dialog-evals \
	-p 8081:8081 \
	--env-file .env \
	-v "./src:/app" \
	-v "./data:/app/data" \
	-v "./etc:/app/etc" \
	--network=dialog_default \
	dialog-api \
	/app/etc/run_evals.sh