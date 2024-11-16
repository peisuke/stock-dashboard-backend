# Makefile for the Backend Project

# Variables
ENV_FILE := .env
DOCKER_COMPOSE_FILE := docker-compose.yml

# Load environment variables
env:
	@export $(shell sed 's/=.*//' $(ENV_FILE))

# Install dependencies using Poetry
install:
	poetry install

# Run FastAPI server locally
run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run Docker Compose for local development
compose-up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d

# Stop Docker Compose
compose-down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Run tests using pytest
test:
	poetry run pytest tests/

# Linting using flake8
lint:
	poetry run flake8 app/

# Format code using black
format:
	poetry run black app/

# Clean up Docker resources
clean:
	docker system prune -f

dev-setup: install compose-up

