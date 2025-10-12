# ARG PYTHON_VERSION=3.12
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS base

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

# Copy dependency files
COPY pyproject.toml uv.lock* .env* ./

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
CMD ["uv", "run", "-m","src.openai_sdk_resume_assistant.resume_agent"]

# # Expose the port that the application listens on.
# EXPOSE 8000

# # Run the application.
# CMD gunicorn '.venv.Lib.site-packages.fastapi.middleware.wsgi' --bind=0.0.0.0:8000
