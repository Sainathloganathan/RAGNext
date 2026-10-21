# 🚀 Cloud Commanders Python SDK

Official Python client library for connecting to Cloud Commanders & Version-Aware RAG services.

---

## 📦 Installation

Install in editable mode directly in your environment:

```bash
pip install -e .
```

---

## ⚡ Quickstart

```python
from cloud_commanders import CloudCommandersClient

client = CloudCommandersClient(
    base_url="http://127.0.0.1:8000",
    api_key="cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo",
)

# 1. Health check
health = client.health()
print(f"Status: {health.status}")

# 2. Version-Aware RAG query
response = client.query("What is the remote work security policy allowance?")
print(response.answer)

for citation in response.citations:
    print(f"[{citation.document_title} v{citation.version_number}, p.{citation.page}]: {citation.text}")
```

---

## 🛠️ Key Capabilities

| Namespace | Methods | Description |
|-----------|---------|-------------|
| `client.health()` / `client.ping()` | `health()`, `ping()` | Inspect server health, status, and authentication state. |
| `client.query(...)` / `client.chat` | `query(question, ...)` | Execute natural language queries with version resolution and citations. |
| `client.documents` | `list()`, `get(id)`, `upload(...)`, `delete(id)` | Ingest and inspect documents and version trees. |
| `client.versions` | `list_by_document(id)`, `update_status(...)`, `delete(id)` | Manage document version statuses (`Active`, `Superseded`, `Draft`). |
| `client.commands` | `execute(command, ...)`, `get_status(id)` | Orchestrate remote commands and tasks. |
| `client.get()`, `post()`, `delete()` | Standard HTTP methods | Low-level authenticated REST requests with automatic retries. |

---

## 🛡️ Error Handling

The client maps standard HTTP status codes to explicit exceptions:

```python
from cloud_commanders import (
    CloudCommandersClient,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    ServerError,
    ConnectionError,
)

try:
    client = CloudCommandersClient(
        base_url="http://127.0.0.1:8000",
        api_key="cc_live_...",
    )
    client.health()
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
except ConnectionError as e:
    print(f"Unable to reach server: {e}")
```

---

## 💻 CLI Usage

The package provides a built-in command line interface:

```bash
# Check health
python -m cloud_commanders health

# Ask a question to RAG engine
python -m cloud_commanders query "What is the policy?"

# List documents
python -m cloud_commanders documents
```
