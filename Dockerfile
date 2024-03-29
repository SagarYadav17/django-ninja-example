# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /poetry
COPY pyproject.toml poetry.lock* /poetry/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Switch back to the app directory
WORKDIR /app

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD uvicorn config.asgi:application --host 0.0.0.0 --port 8000
