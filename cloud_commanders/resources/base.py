"""
Base resource class for Cloud Commanders API resources.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..client import CloudCommandersClient
    from ..models import ApiResponse


class BaseResource:
    """Base class for API resource namespaces."""

    def __init__(self, client: "CloudCommandersClient"):
        self._client = client

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "ApiResponse":
        return self._client.get(endpoint, params=params, headers=headers)

    def _post(
        self,
        endpoint: str,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "ApiResponse":
        return self._client.post(
            endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )

    def _put(
        self,
        endpoint: str,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "ApiResponse":
        return self._client.put(endpoint, json=json, headers=headers)

    def _patch(
        self,
        endpoint: str,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "ApiResponse":
        return self._client.patch(endpoint, json=json, headers=headers)

    def _delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "ApiResponse":
        return self._client.delete(endpoint, params=params, headers=headers)
