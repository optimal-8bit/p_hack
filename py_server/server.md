# py_server Backend Guide (Mongo + JWT + Google OAuth)

This backend uses FastAPI with a modular structure, MongoDB for storage, JWT for auth, and Google OAuth token login support.

## Architecture

```text
py_server/
  app/
    main.py                    # FastAPI app + startup/shutdown lifecycle
    api/
      router.py                # Central module router registration
    core/
      config.py                # Environment settings
      database.py              # MongoDB connection and indexes
      security.py              # JWT + password hash helpers
      dependencies.py          # Shared auth dependency (get_current_user)
    modules/
      health/
        routes.py
        controller.py
        service.py
        schemas.py
      auth/
        routes.py
        controller.py
        service.py
        schemas.py
      users/
        routes.py
        controller.py
        service.py
        schemas.py
      items/
        routes.py
        controller.py
        service.py
        schemas.py
      ai/
        functions.py          # reusable helper functions for LLM calls
        schemas.py
        providers/
          base.py
          factory.py
          google_ai_studio.py
          openrouter.py
          ollama.py
      cloudinary/
        functions.py          # reusable helper functions for file upload/delete
      google_workspace/
        functions.py          # SMTP email + Google Calendar/Meet helper functions
      rag/
        functions.py          # index + query helpers for full RAG flow
        chunking.py
        embeddings.py
        vector_store.py
        retrieval.py
        generation.py
        cache.py
        retry.py
        schemas.py
  tests/
  requirements.txt
  .env
  .env.example
```

## Layer Rules (Important)

1. routes.py
   - HTTP contract only: path, method, request/response model.
   - Calls controller functions.

2. controller.py
   - Route orchestration, API-specific validation and HTTP errors.
   - Calls service functions.

3. service.py
   - Business logic + MongoDB reads/writes.
   - No FastAPI router objects.

4. schemas.py
   - Pydantic request/response models.

5. app/api/router.py
   - The only shared file for module registration.

This split keeps features isolated and reduces merge conflicts.

## AI Helper Module (No Routes)

The AI module is intentionally route-free. It exposes one function to be called inside any controller/service:

- `call_llm` and `call_llm_with_fallback` from `app/modules/ai/functions.py`

Example usage from any controller:

```python
from app.modules.ai.functions import call_llm
from app.modules.ai.schemas import AIMessage


async def summarize_text_controller(text: str):
  result = await call_llm(
    provider="openrouter",
    messages=[
      AIMessage(role="system", content="You are a concise assistant."),
      AIMessage(role="user", content=f"Summarize: {text}"),
    ],
    model="openai/gpt-4o-mini",
  )
  return {"summary": result.content, "provider": result.provider_used}
```

There is no default provider. Caller explicitly passes provider and model.

## Cloudinary Helper Module (No Routes)

The Cloudinary module is route-free and can be used by any controller or service.

- `upload_file_bytes` from `app/modules/cloudinary/functions.py`
- `upload_file_path` from `app/modules/cloudinary/functions.py`
- `delete_asset` from `app/modules/cloudinary/functions.py`

Example usage from a controller:

```python
from app.modules.cloudinary.functions import upload_file_bytes


async def upload_receipt_controller(file_bytes: bytes, filename: str):
  result = upload_file_bytes(
    file_bytes=file_bytes,
    filename=filename,
    folder="receipts",
    resource_type="auto",
  )
  return {
    "public_id": result.get("public_id"),
    "url": result.get("secure_url"),
    "resource_type": result.get("resource_type"),
  }
```

## Google Workspace Helpers (No Routes)

This module provides helper functions for SMTP email and Google Calendar/Meet scheduling:

- `send_email_smtp` from `app/modules/google_workspace/functions.py`
- `create_calendar_event` from `app/modules/google_workspace/functions.py`
- `schedule_google_meet` from `app/modules/google_workspace/functions.py`

Example: send email

```python
from app.modules.google_workspace.functions import send_email_smtp


def notify_user_controller(email: str):
  return send_email_smtp(
    to_emails=email,
    subject="Welcome",
    body_text="Welcome to pHack",
  )
```

Example: create calendar event

```python
from app.modules.google_workspace.functions import create_calendar_event


def create_event_controller():
  return create_calendar_event(
    summary="Product Demo",
    start_iso="2026-04-15T10:00:00",
    end_iso="2026-04-15T10:30:00",
    timezone="Asia/Kolkata",
    attendees=["user@example.com"],
  )
```

Example: schedule Google Meet

```python
from app.modules.google_workspace.functions import schedule_google_meet


def schedule_meet_controller():
  return schedule_google_meet(
    summary="Client Sync",
    start_iso="2026-04-15T11:00:00",
    end_iso="2026-04-15T11:45:00",
    timezone="Asia/Kolkata",
    attendees=["a@example.com", "b@example.com"],
  )
```

## RAG Helpers (No Routes)

This module provides a complete route-free RAG pipeline with clear abstraction:

- chunking and indexing: app/modules/rag/chunking.py and app/modules/rag/functions.py
- embeddings with fallback: app/modules/rag/embeddings.py
- Neo4j vector storage and search: app/modules/rag/vector_store.py
- retrieval and context building: app/modules/rag/retrieval.py
- grounded answer generation: app/modules/rag/generation.py
- retry and cache: app/modules/rag/retry.py and app/modules/rag/cache.py

Primary embedding provider is Google AI Studio with fallback to OpenRouter and Ollama using RAG_EMBEDDING_PROVIDER_ORDER.

Example: index a document

```python
from app.modules.rag.functions import index_document


async def index_doc_controller(document_id: str, text: str):
  return await index_document(
    document_id=document_id,
    content=text,
    metadata={"source": "upload"},
  )
```

Example: answer a query with retrieved context

```python
from app.modules.rag.functions import answer_query


async def ask_controller(query: str):
  result = await answer_query(query)
  return {
    "answer": result.answer,
    "provider": result.provider_used,
    "chunks": [chunk.model_dump() for chunk in result.chunks],
  }
```

## Environment Variables

Copy and edit env file:

```bash
cp .env.example .env
```

Required values:

```env
APP_NAME=pHack API
APP_ENV=dev
API_PREFIX=/api/v1

MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=phack

JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

GOOGLE_CLIENT_ID=your-google-oauth-client-id.apps.googleusercontent.com

AI_REQUEST_TIMEOUT_SECONDS=90
AI_TEMPERATURE=0.2
AI_MAX_TOKENS=512

OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini

GOOGLE_AI_STUDIO_API_KEY=
GOOGLE_AI_STUDIO_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GOOGLE_AI_STUDIO_MODEL=gemini-1.5-flash

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_SECURE=true

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_USE_TLS=true
SMTP_USE_SSL=false

GOOGLE_SERVICE_ACCOUNT_FILE=
GOOGLE_WORKSPACE_DELEGATED_USER=
GOOGLE_CALENDAR_ID=primary

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
NEO4J_DATABASE=neo4j

RAG_CHUNK_LABEL=RagChunk
RAG_VECTOR_INDEX_NAME=rag_chunk_embedding
RAG_CHUNK_SIZE=900
RAG_CHUNK_OVERLAP=120
RAG_TOP_K=5
RAG_CACHE_TTL_SECONDS=300
RAG_RETRY_ATTEMPTS=3
RAG_RETRY_BASE_DELAY_SECONDS=0.5

RAG_EMBEDDING_PROVIDER_ORDER=google_ai_studio,openrouter,ollama
RAG_GOOGLE_EMBEDDING_MODEL=text-embedding-004
RAG_OPENROUTER_EMBEDDING_MODEL=openai/text-embedding-3-small
RAG_OLLAMA_EMBEDDING_MODEL=nomic-embed-text

RAG_GENERATION_PROVIDER_ORDER=google_ai_studio,openrouter,ollama
RAG_GENERATION_TEMPERATURE=0.2
RAG_GENERATION_MAX_TOKENS=512
```

## Run Backend

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## MongoDB Notes

- App connects to MongoDB at startup and closes on shutdown.
- A unique index on users.email is created automatically.
- Users and items store Mongo ObjectId in DB and expose string id in API responses.

## Auth System

### JWT Local Auth Endpoints

- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me (Bearer token required)

Register/Login returns:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "name": "...",
    "email": "...",
    "auth_provider": "local"
  }
}
```

### Google OAuth (Token Login)

Endpoint:

- POST /api/v1/auth/google

Request body:

```json
{
  "id_token": "<google-id-token-from-client>"
}
```

Flow:

1. Frontend gets Google id_token via Google Sign-In.
2. Frontend sends id_token to backend endpoint.
3. Backend verifies token with GOOGLE_CLIENT_ID.
4. Backend upserts user in MongoDB and returns JWT.

## Existing Resource Modules

- users: MongoDB CRUD endpoints at /api/v1/users
- items: MongoDB CRUD endpoints at /api/v1/items
- health: /api/v1/health includes Mongo connectivity state

## Add New Module (Team Standard)

For module orders:

1. Create app/modules/orders with:
   - routes.py
   - controller.py
   - service.py
   - schemas.py
   - __init__.py
2. Keep route -> controller -> service direction only.
3. Register router in app/api/router.py.
4. Avoid editing other modules unless needed.

## Team Workflow For Fewer Conflicts

1. One branch per module/feature.
2. Keep PRs small and scoped to your module.
3. Coordinate changes to app/api/router.py (single shared file).
4. Keep shared logic in app/core only.
5. Follow naming consistency across all modules.
