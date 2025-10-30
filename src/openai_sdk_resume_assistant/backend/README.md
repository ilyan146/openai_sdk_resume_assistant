## Backend Architecture
```
backend/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py                    # FastAPI app entry point
│       ├── config.py                  # Settings and environment variables
│       ├── dependencies.py            # Shared dependencies (auth, DB, etc.)
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── endpoints/
│       │       │   ├── __init__.py
│       │       │   ├── chat.py        # Chat endpoints
│       │       │   ├── health.py      # Health check
│       │       │   └── webhooks.py    # Webhook handlers
│       │       └── router.py          # API router aggregation
│       │
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base_agent.py
│       │   ├── rag_agent.py
│       │   └── resume_agent.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── requests.py            # Pydantic request models
│       │   └── responses.py           # Pydantic response models
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── chat_service.py        # Business logic
│       │   ├── vector_service.py
│       │   └── azure_client.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── logging.py             # Logging configuration
│       │   ├── middleware.py          # Custom middleware
│       │   └── exceptions.py          # Custom exceptions
│       │
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   └── test_agents/
│
├── docker/
│   ├── Dockerfile
│   └── Dockerfile.dev
│
├── compose.yaml
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
### 📁 Directory Structure Explained

#### `src/app/`
Core application code following FastAPI best practices.

- **`main.py`** - Application entry point, ASGI app initialization
- **`config.py`** - Environment-based configuration using Pydantic Settings
- **`dependencies.py`** - Reusable dependency injection functions

#### `api/v1/`
Versioned API layer for backward compatibility.

- **`endpoints/`** - Individual route modules (chat, health, webhooks)
- **`router.py`** - Aggregates all endpoint routers

#### `agents/`
AI agent implementations and orchestration logic.

- **`base_agent.py`** - Abstract base class for agents
- **`rag_agent.py`** - Retrieval-Augmented Generation agent
- **`resume_agent.py`** - Resume-specific agent

#### `models/`
Pydantic schemas for request/response validation.

- **`requests.py`** - Input validation models
- **`responses.py`** - Output serialization models

#### `services/`
Business logic layer, independent of HTTP transport.

- **`chat_service.py`** - Core chat orchestration
- **`vector_service.py`** - Vector DB operations
- **`azure_client.py`** - Azure OpenAI integration

#### `core/`
Cross-cutting concerns and infrastructure.

- **`logging.py`** - Structured logging setup
- **`middleware.py`** - Custom middleware (timing, auth, etc.)
- **`exceptions.py`** - Custom exception classes and handlers

#### `utils/`
Shared helper functions and utilities.

#### `tests/`
Test suite mirroring the application structure.

- **`conftest.py`** - Pytest fixtures and configuration
- **`test_api/`** - API endpoint tests
- **`test_agents/`** - Agent unit tests

### 🚀 Key Design Principles

1. **Separation of Concerns** - Clear boundaries between API, business logic, and data layers
2. **Dependency Injection** - FastAPI's native DI for loose coupling
3. **Type Safety** - Pydantic models enforce contracts at runtime
4. **Testability** - Services isolated from HTTP layer for easy testing
5. **Scalability** - Versioned APIs and modular structure support growth
6. **Observability** - Centralized logging and middleware for monitoring

### 🔧 Development Workflow

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Build Docker image
docker build -t backend:latest -f docker/Dockerfile .

# Start with Docker Compose
docker compose up
```