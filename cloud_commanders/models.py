"""
Data models and response types for Cloud Commanders SDK.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class ApiResponse:
    """Generic wrapper for HTTP API responses."""

    def __init__(
        self,
        status_code: int,
        data: Any,
        headers: Optional[Dict[str, str]] = None,
        raw_text: str = "",
    ):
        self.status_code = status_code
        self.data = data
        self.headers = headers or {}
        self.raw_text = raw_text

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    def json(self) -> Any:
        return self.data

    def __getitem__(self, item: str) -> Any:
        if isinstance(self.data, dict):
            return self.data[item]
        raise TypeError(f"Response data is {type(self.data).__name__}, not dict")

    def get(self, item: str, default: Any = None) -> Any:
        if isinstance(self.data, dict):
            return self.data.get(item, default)
        return default

    def __contains__(self, item: str) -> bool:
        if isinstance(self.data, dict):
            return item in self.data
        return False

    def __repr__(self) -> str:
        return f"<ApiResponse status_code={self.status_code} data={self.data!r}>"


@dataclass
class Citation:
    """Citation supporting a generated RAG answer."""
    version_id: Optional[str] = None
    version_number: Optional[str] = None
    document_title: Optional[str] = None
    page: Optional[int] = None
    chunk_id: Optional[str] = None
    score: Optional[float] = None
    text: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Citation":
        return cls(
            version_id=data.get("versionId") or data.get("version_id"),
            version_number=data.get("versionNumber") or data.get("version_number"),
            document_title=data.get("documentTitle") or data.get("document_title"),
            page=data.get("page"),
            chunk_id=data.get("chunkId") or data.get("chunk_id"),
            score=data.get("score"),
            text=data.get("text") or data.get("content"),
        )


@dataclass
class QueryResponse:
    """Response returned from a RAG Query."""
    query: str
    answer: str
    intent: Optional[str] = None
    confidence: Optional[str] = None
    citations: List[Citation] = field(default_factory=list)
    eligible_versions: List[Dict[str, Any]] = field(default_factory=list)
    latency_ms: Optional[float] = None
    conflict_warning: Optional[str] = None
    status_note: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueryResponse":
        result = data.get("result", {}) if isinstance(data.get("result"), dict) else data
        raw_citations = result.get("citations", []) or data.get("citations", [])
        citations = [
            Citation.from_dict(c) if isinstance(c, dict) else Citation(text=str(c))
            for c in raw_citations
        ]

        return cls(
            query=data.get("query", ""),
            answer=result.get("answer") or data.get("answer") or result.get("content") or "",
            intent=data.get("intent") or result.get("intent"),
            confidence=result.get("confidence") or data.get("confidence"),
            citations=citations,
            eligible_versions=data.get("eligibleVersions") or data.get("eligible_versions") or [],
            latency_ms=data.get("latencyMs") or data.get("latency_ms"),
            conflict_warning=result.get("conflictWarning") or data.get("conflictWarning"),
            status_note=result.get("statusNote") or data.get("statusNote"),
            raw=data,
        )


@dataclass
class HealthResponse:
    """Response from health check endpoint."""
    status: str
    version: Optional[str] = None
    product: Optional[str] = None
    team: Optional[str] = None
    database: Optional[str] = None
    vector_store: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HealthResponse":
        return cls(
            status=data.get("status", "unknown"),
            version=data.get("version"),
            product=data.get("product"),
            team=data.get("team"),
            database=data.get("database"),
            vector_store=data.get("vectorStore") or data.get("vector_store"),
            raw=data,
        )


@dataclass
class DocumentResponse:
    """Document metadata representation."""
    id: str
    title: str
    category: Optional[str] = None
    department: Optional[str] = None
    versions_count: int = 0
    active_version: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentResponse":
        return cls(
            id=str(data.get("id", "")),
            title=data.get("title") or data.get("name") or "",
            category=data.get("category"),
            department=data.get("department"),
            versions_count=data.get("versionsCount", 0),
            active_version=data.get("activeVersion") or data.get("active_version"),
            raw=data,
        )


@dataclass
class VersionResponse:
    """Document Version representation."""
    id: str
    document_id: str
    version_number: str
    status: str
    file_path: Optional[str] = None
    chunk_count: int = 0
    effective_date: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VersionResponse":
        return cls(
            id=str(data.get("id", "")),
            document_id=str(data.get("documentId") or data.get("document_id", "")),
            version_number=str(data.get("versionNumber") or data.get("version_number", "")),
            status=str(data.get("status", "draft")),
            file_path=data.get("filePath") or data.get("file_path"),
            chunk_count=data.get("chunkCount") or data.get("chunk_count", 0),
            effective_date=data.get("effectiveDate") or data.get("effective_date"),
            raw=data,
        )
