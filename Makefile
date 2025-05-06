all:
	docker compose down -v
	docker compose up --build -d postgres
	sleep 5  # Give the database time to initialize
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f
