"""
Version management resource for Cloud Commanders SDK.
"""

from typing import Any, Dict, List, Optional
from .base import BaseResource
from ..models import VersionResponse


class VersionsResource(BaseResource):
    """Resource for managing document versions, status transitions, and comparisons."""

    def list_by_document(self, document_id: str) -> List[VersionResponse]:
        """List all versions associated with a document ID."""
        res = self._get(f"/api/documents/{document_id}/versions")
        data = res.json()
        raw_versions = data.get("versions", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        return [VersionResponse.from_dict(v) for v in raw_versions]

    def update_status(
        self,
        version_id: str,
        status: str,
        supersede_previous: bool = False,
    ) -> Dict[str, Any]:
        """
        Update the lifecycle status of a specific document version.
        Allowed statuses: 'Draft', 'Active', 'Superseded', 'Expired', 'Archived'.
        """
        payload = {
            "status": status,
            "supersedePrevious": supersede_previous,
        }
        res = self._patch(f"/api/versions/{version_id}/status", json=payload)
        return res.json()

    def delete(self, version_id: str) -> Dict[str, Any]:
        """Delete a single version and its vector embeddings."""
        res = self._delete(f"/api/versions/{version_id}")
        return res.json()
