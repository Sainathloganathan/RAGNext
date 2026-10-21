"""
Cloud Commanders Python SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Official Python client library for Cloud Commanders and Version-Aware RAG services.

Usage:
    from cloud_commanders import CloudCommandersClient

    client = CloudCommandersClient(
        base_url="http://127.0.0.1:8000",
        api_key="cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo",
    )

    # Health Check
    health = client.health()

    # Query RAG Engine
    answer = client.query("What is the remote work policy allowance?")
"""

from .client import CloudCommandersClient
from .exceptions import (
    CloudCommandersError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    ServerError,
    ConnectionError,
)
from .models import (
    ApiResponse,
    HealthResponse,
    QueryResponse,
    DocumentResponse,
    VersionResponse,
    Citation,
)

__version__ = "1.0.0"
__all__ = [
    "CloudCommandersClient",
    "CloudCommandersError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
    "ConnectionError",
    "ApiResponse",
    "HealthResponse",
    "QueryResponse",
    "DocumentResponse",
    "VersionResponse",
    "Citation",
]
