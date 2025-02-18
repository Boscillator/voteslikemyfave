# Use the official Python base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for Poetry and other tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Copy the rest of the application code
COPY . /app

# Set the default command to run the application
CMD ["python", "-m", "scraper"]
