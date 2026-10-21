"""
Chat and RAG Query resource for Cloud Commanders SDK.
"""

from typing import Any, Dict, Optional
from .base import BaseResource
from ..models import QueryResponse
from ..exceptions import NotFoundError


class ChatResource(BaseResource):
    """Resource for executing RAG queries with version filtering and citations."""

    def query(
        self,
        question: str,
        document_id: Optional[str] = None,
        category: Optional[str] = None,
        status_filter: Optional[str] = None,
        conversation_id: Optional[str] = None,
        **extra: Any,
    ) -> QueryResponse:
        """
        Execute a version-aware RAG query against the knowledge repository.

        Args:
            question: Natural language question to ask.
            document_id: Optional target document ID to restrict search.
            category: Optional category filter (e.g., 'HR', 'Security').
            status_filter: Optional status filter ('active', 'superseded', 'draft').
            conversation_id: Optional session or conversation ID for context.
            **extra: Additional custom query parameters.

        Returns:
            QueryResponse object with synthesized answer and citations.
        """
        payload: Dict[str, Any] = {
            "question": question,
            **extra,
        }
        if document_id is not None:
            payload["documentId"] = document_id
        if category is not None:
            payload["category"] = category
        if status_filter is not None:
            payload["statusFilter"] = status_filter
        if conversation_id is not None:
            payload["conversationId"] = conversation_id

        # Attempt standard RAGNext /api/chat or /chat
        try:
            res = self._post("/api/chat", json=payload)
        except NotFoundError:
            res = self._post("/chat", json=payload)

        data = res.json()
        if not isinstance(data, dict):
            data = {"answer": str(data), "query": question}
        return QueryResponse.from_dict(data)
