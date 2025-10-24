ARG PYTHON_VERSION=3.12
# FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS base
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm AS base


# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# # Create a non-privileged user that the app will run under.
# # See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

    
# # Change ownership of the app directory to appuser
# RUN chown -R appuser:appuser /app

# Install Node.js and npm for MCP servers
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock* .env* ./
# COPY pyproject.toml .env* ./

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy the source code into the container.
COPY ./src ./src

# Switch to the non-privileged user to run the application.
# USER appuser

# Set Python path to include .src directory
ENV PYTHONPATH=/app/src

# Run the application as a module
CMD ["uv", "run", "src/openai_sdk_resume_assistant/RAG/rag_agent.py"]

# # Expose the port that the application listens on.
# EXPOSE 8000

# # Run the application.
# CMD gunicorn '.venv.Lib.site-packages.fastapi.middleware.wsgi' --bind=0.0.0.0:8000
