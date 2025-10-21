# FastAPI Project

I develop the following project based
on [FastAPI Beyond CRUD](https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P&si=rl-08ktaRjcm2aIQ)
course.
The course focuses on FastAPI development concepts that go beyond the basic CRUD operations:
JWT authentication, Email notification, Middleware implementation.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [Contributing](#contributing)
7. [DB schema](#DB-schema-for-the-application)

## Getting Started

Follow the instructions below to set up and run your FastAPI project.

### Prerequisites

Ensure you have the following installed:

- Python >= 3.12
- PostgreSQL
- Redis

### Project Setup via pipenv

1. Clone the project repository:
    ```bash
    git clone https://github.com/AliakseiTarasenka/fastapi-docker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd fastapi-docker/
    ```

3. Install the required dependencies:
   This will create a virtual environment if it doesn’t exist yet
   and install all dependencies from your Pipfile/Pipfile.lock
    ```bash
    pipenv install
    ```
4. Activate a virtual environment:
    ```bash
    pipenv shell
    ```

5. Set up environment variables by copying the example configuration:
    ```bash
    cp .env.example .env
    ```

6. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```
   For DB with tables already created manually:
    ```bash
    pipenv run alembic stamp head
    ```
7. Start running the application:
    ```bash
    pipenv run uvicorn main:app --reload
    ```

It will be available on the address:

http://127.0.0.1:8000/docs

## Running the Application

Start the application:

```bash
fastapi dev main.py
```

Alternatively, you can run the application using Docker:

```bash
docker compose up -d
```

## Running Tests

Run the tests using this command

```bash
pytest
```

## Contributing

I welcome contributions to improve the documentation! You can
contribute [here](https://github.com/jod35/fastapi-beyond-crud-docs).

## DB schema for the application

https://dbdiagram.io/d/68e68028d2b621e422e49c03