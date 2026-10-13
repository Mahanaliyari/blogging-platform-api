# Blogging Platform API

A RESTful backend for a blogging platform built with **Python**, **FastAPI**, and **PostgreSQL**. The project includes JWT-based authentication, ownership-based authorisation, database migrations, integration tests, and a Docker-based development environment.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## Features

- RESTful API endpoints for blog content
- JWT-based authentication using OAuth2 bearer tokens
- Password hashing and ownership-based authorisation
- Request and response validation with Pydantic
- Relational database access using SQLAlchemy ORM
- Version-controlled database schema migrations with Alembic
- Automated integration tests with `pytest`
- Interactive API documentation through Swagger UI and ReDoc
- Docker Compose setup for running the API and PostgreSQL locally

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.12 |
| API framework | FastAPI |
| ASGI server | Uvicorn |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation and settings | Pydantic, Pydantic Settings |
| Authentication | OAuth2 bearer tokens, JWT |
| Testing | pytest, FastAPI TestClient |
| Containers | Docker, Docker Compose |

## Project Structure

```text
blogging-platform-api/
├── alembic/             # Database migration scripts
├── app/                 # Application source code
├── tests/               # Integration tests
├── alembic.ini          # Alembic configuration
├── compose.yaml         # API and PostgreSQL services
├── Dockerfile           # API container image
└── requirements.txt     # Application dependencies
```

## Getting Started

### Prerequisites

For the Docker-based setup, install:

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine with the Docker Compose plugin

For a local setup without Docker, you will also need Python 3.12 and a running PostgreSQL instance.

### 1. Clone the repository

```bash
git clone https://github.com/Mahanaliyari/blogging-platform-api.git
cd blogging-platform-api
```

### 2. Configure environment variables

Create the environment files expected by the project. Keep credentials out of version control and use strong, unique values for secrets.

The root `.env` file is used by Docker Compose for the PostgreSQL service and database connection configuration. For example:

```env
POSTGRES_USER=bloguser
POSTGRES_PASSWORD=replace-with-a-local-password
POSTGRES_DB=blogdb
SQLALCHEMY_DATABASE_URL=postgresql+psycopg://bloguser:replace-with-a-local-password@db:5432/blogdb
```

The hostname `db` must match the PostgreSQL service name in `compose.yaml`. Ensure the database URL uses the PostgreSQL driver installed by the project.

Create `app/.env` for the application settings required by the codebase. Set the authentication and other settings expected by the application's Pydantic Settings configuration. Do not use example secrets in a real deployment.

### 3. Start the application with Docker

```bash
docker compose up --build
```

In a second terminal, apply the database migrations:

```bash
docker compose exec api alembic upgrade head
```

The API should then be available at:

- **API Base URL:** [https://141.147.118.245](https://141.147.118.245)
- **Swagger UI:** [Interactive API documentation](https://141.147.118.245/docs)
- **ReDoc:** [API reference documentation](https://141.147.118.245/redoc)

To stop the containers, run:

```bash
docker compose down
```

To also remove the PostgreSQL data volume, run `docker compose down -v`. This permanently deletes the data stored in that volume.

## Running Locally Without Docker

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application environment variables and ensure PostgreSQL is running.

4. Apply the database migrations:

   ```bash
   alembic upgrade head
   ```

5. Start the development server:

   ```bash
   uvicorn app.main:app --reload
   ```


## Database Migrations

Alembic manages database schema changes.

Apply all pending migrations:

```bash
alembic upgrade head
```

Generate a migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

Roll back the most recent migration:

```bash
alembic downgrade -1
```

When running the application through Docker Compose, run these commands inside the API container by prefixing them with `docker compose exec api`.

## Testing

The project includes an integration test suite covering authentication, CRUD operations, authorisation, and error handling.

Run the tests from the project root:

```bash
pytest
```

The tests use FastAPI's `TestClient` and a separate PostgreSQL test database. Configure the test database independently from any development or production database before running the suite.

## Deployment

The API has also been deployed to an Ubuntu Linux virtual machine using `systemd` and Nginx, with HTTPS and environment-based configuration.

## Author

**Mahan Aliyari**  
[GitHub](https://github.com/Mahanaliyari)
