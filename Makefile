.PHONY: help run dev docker-build docker-up docker-down ingest setup test lint clean

help:
	@echo "WhatsApp AI Assistant - Common Commands"
	@echo ""
	@echo "  make run           Run locally with Flask dev server"
	@echo "  make dev           Same as run (alias)"
	@echo "  make docker-build  Build the Docker image"
	@echo "  make docker-up     Start with docker-compose"
	@echo "  make docker-down   Stop docker-compose"
	@echo "  make ingest        Ingest documents from uploads/"
	@echo "  make setup         Setup Pinecone index"
	@echo "  make test          Run pytest"
	@echo "  make clean         Remove __pycache__ and .pyc files"

run dev:
	FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=5000

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

ingest:
	python ingest_docs.py

setup:
	python setup_pinecone.py

test:
	pytest -v

lint:
	@echo "Consider installing ruff: pip install ruff"
	-ruff check . || true

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	echo "Cleaned Python cache files."
