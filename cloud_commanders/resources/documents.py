"""
Document management resource for Cloud Commanders SDK.
"""

import os
from typing import Any, Dict, List, Optional, Union, BinaryIO
from .base import BaseResource
from ..models import DocumentResponse, VersionResponse


class DocumentsResource(BaseResource):
    """Resource for uploading, listing, inspecting, and deleting documents."""

    def list(self) -> List[DocumentResponse]:
        """List all documents."""
        res = self._get("/api/documents")
        data = res.json()
        doc_list = data.get("documents", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        return [DocumentResponse.from_dict(d) for d in doc_list]

    def get(self, document_id: str) -> Dict[str, Any]:
        """Get document details along with its version lineage."""
        res = self._get(f"/api/documents/{document_id}")
        data = res.json()
        if isinstance(data, dict):
            doc = DocumentResponse.from_dict(data.get("document", {}))
            versions = [
                VersionResponse.from_dict(v)
                for v in data.get("versions", [])
            ]
            return {"document": doc, "versions": versions, "raw": data}
        return {"raw": data}

    def upload(
        self,
        file_path_or_buffer: Union[str, BinaryIO],
        title: Optional[str] = None,
        category: str = "General",
        version_number: str = "1.0",
        status: str = "Active",
        effective_date: Optional[str] = None,
        department: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload and ingest a document file (PDF, DOCX, TXT, etc.).
        """
        data: Dict[str, Any] = {
            "category": category,
            "versionNumber": version_number,
            "status": status,
        }
        if title:
            data["title"] = title
        if effective_date:
            data["effectiveDate"] = effective_date
        if department:
            data["department"] = department

        files: Dict[str, Any] = {}
        close_file = False

        if isinstance(file_path_or_buffer, str):
            if not os.path.exists(file_path_or_buffer):
                raise FileNotFoundError(f"File not found: {file_path_or_buffer}")
            fname = filename or os.path.basename(file_path_or_buffer)
            fobj = open(file_path_or_buffer, "rb")
            files["file"] = (fname, fobj)
            close_file = True
        else:
            fname = filename or "document.txt"
            files["file"] = (fname, file_path_or_buffer)

        try:
            res = self._post("/api/documents/upload", data=data, files=files)
            return res.json()
        finally:
            if close_file:
                fobj.close()

    def delete(self, document_id: str) -> Dict[str, Any]:
        """Delete a document and all associated version embeddings."""
        res = self._delete(f"/api/documents/{document_id}")
        return res.json()
