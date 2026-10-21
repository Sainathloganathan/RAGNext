"""
Core Client implementation for Cloud Commanders SDK.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    import urllib.parse
    HAS_REQUESTS = False

from .exceptions import (
    AuthenticationError,
    CloudCommandersError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .models import ApiResponse, HealthResponse, QueryResponse
from .resources.chat import ChatResource
from .resources.commands import CommandsResource
from .resources.documents import DocumentsResource
from .resources.health import HealthResource
from .resources.versions import VersionsResource

logger = logging.getLogger("cloud_commanders")


class CloudCommandersClient:
    """
    Main client interface for Cloud Commanders and Version-Aware RAG services.

    Example:
        from cloud_commanders import CloudCommandersClient

        client = CloudCommandersClient(
            base_url="http://127.0.0.1:8000",
            api_key="cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo",
        )

        # Quick Health Check
        health = client.health()

        # Natural Language Version-Aware RAG Query
        res = client.query("What is the remote work security policy?")
        print(res.answer)
    """

    DEFAULT_BASE_URL = "http://127.0.0.1:8000"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
    ):
        """
        Initialize the Cloud Commanders Client.

        Args:
            base_url: Base URL of the API (defaults to http://127.0.0.1:8000 or env CLOUD_COMMANDERS_BASE_URL).
            api_key: Secret or live API key (e.g. cc_live_... or env CLOUD_COMMANDERS_API_KEY).
            timeout: Request timeout in seconds (default: 30.0).
            max_retries: Number of retry attempts on network or transient server errors (default: 3).
            headers: Optional additional HTTP headers.
            verify_ssl: Whether to verify SSL certificates (default: True).
        """
        self.base_url = (
            base_url
            or os.environ.get("CLOUD_COMMANDERS_BASE_URL")
            or self.DEFAULT_BASE_URL
        ).rstrip("/")

        self.api_key = (
            api_key
            or os.environ.get("CLOUD_COMMANDERS_API_KEY")
            or ""
        )

        self.timeout = float(timeout)
        self.max_retries = int(max_retries)
        self.verify_ssl = verify_ssl

        # Default headers
        self._default_headers = {
            "Accept": "application/json",
            "User-Agent": "CloudCommanders-Python-SDK/1.0.0",
        }
        if self.api_key:
            self._default_headers["Authorization"] = f"Bearer {self.api_key}"
            self._default_headers["X-API-Key"] = self.api_key

        if headers:
            self._default_headers.update(headers)

        # HTTP Session setup
        if HAS_REQUESTS:
            self._session = requests.Session()
            self._session.headers.update(self._default_headers)
        else:
            self._session = None

        # Resource sub-interfaces
        self.health_resource = HealthResource(self)
        self.chat = ChatResource(self)
        self.documents = DocumentsResource(self)
        self.versions = VersionsResource(self)
        self.commands = CommandsResource(self)

    # --------------------------------------------------------------------------
    # High-level Convenience Methods
    # --------------------------------------------------------------------------

    def health(self) -> HealthResponse:
        """Check API service health."""
        return self.health_resource.check()

    def ping(self) -> bool:
        """Check if server is responding and healthy."""
        return self.health_resource.ping()

    def query(
        self,
        question: str,
        document_id: Optional[str] = None,
        category: Optional[str] = None,
        status_filter: Optional[str] = None,
        **kwargs: Any,
    ) -> QueryResponse:
        """
        Execute a Version-Aware RAG query.

        Args:
            question: Question string.
            document_id: Optional ID of document to query.
            category: Optional document category filter.
            status_filter: Optional status filter ('Active', 'Superseded', etc.).

        Returns:
            QueryResponse with answer, citations, and version eligibility.
        """
        return self.chat.query(
            question=question,
            document_id=document_id,
            category=category,
            status_filter=status_filter,
            **kwargs,
        )

    # --------------------------------------------------------------------------
    # Core HTTP Request Engine
    # --------------------------------------------------------------------------

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        """
        Execute an HTTP request against the API server with error mapping and retries.
        """
        url = self._build_url(endpoint)
        req_timeout = timeout if timeout is not None else self.timeout

        merged_headers = dict(self._default_headers)
        if headers:
            merged_headers.update(headers)

        attempts = 0
        last_exception: Optional[Exception] = None

        while attempts <= self.max_retries:
            attempts += 1
            try:
                if HAS_REQUESTS:
                    resp = self._session.request(
                        method=method.upper(),
                        url=url,
                        params=params,
                        json=json,
                        data=data,
                        files=files,
                        headers=merged_headers,
                        timeout=req_timeout,
                        verify=self.verify_ssl,
                    )
                    status_code = resp.status_code
                    resp_headers = dict(resp.headers)
                    raw_text = resp.text

                    try:
                        parsed_data = resp.json()
                    except Exception:
                        parsed_data = raw_text

                else:
                    status_code, resp_headers, raw_text, parsed_data = self._urllib_request(
                        method=method.upper(),
                        url=url,
                        params=params,
                        json_payload=json,
                        data=data,
                        headers=merged_headers,
                        timeout=req_timeout,
                    )

                # Check status and raise appropriate exception
                self._handle_response_status(status_code, parsed_data, raw_text)

                return ApiResponse(
                    status_code=status_code,
                    data=parsed_data,
                    headers=resp_headers,
                    raw_text=raw_text,
                )

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) if HAS_REQUESTS else (urllib.error.URLError, TimeoutError) as e:
                last_exception = ConnectionError(
                    f"Failed to connect to Cloud Commanders server at '{url}': {e}"
                )
                if attempts <= self.max_retries:
                    backoff = 0.5 * (2 ** (attempts - 1))
                    time.sleep(backoff)
                    continue
                raise last_exception

            except RateLimitError as e:
                if attempts <= self.max_retries:
                    time.sleep(1.0 * attempts)
                    continue
                raise e

            except ServerError as e:
                if attempts <= self.max_retries:
                    backoff = 0.5 * (2 ** (attempts - 1))
                    time.sleep(backoff)
                    continue
                raise e

        if last_exception:
            raise last_exception
        raise CloudCommandersError(f"Request failed after {attempts} attempts")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        """Send a GET request."""
        return self.request("GET", endpoint, params=params, headers=headers, timeout=timeout)

    def post(
        self,
        endpoint: str,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        """Send a POST request."""
        return self.request(
            "POST",
            endpoint,
            params=params,
            json=json,
            data=data,
            files=files,
            headers=headers,
            timeout=timeout,
        )

    def put(
        self,
        endpoint: str,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        """Send a PUT request."""
        return self.request("PUT", endpoint, json=json, headers=headers, timeout=timeout)

    def patch(
        self,
        endpoint: str,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        """Send a PATCH request."""
        return self.request("PATCH", endpoint, json=json, headers=headers, timeout=timeout)

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        """Send a DELETE request."""
        return self.request("DELETE", endpoint, params=params, headers=headers, timeout=timeout)

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        clean_endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{clean_endpoint}"

    def _handle_response_status(self, status_code: int, data: Any, raw_text: str) -> None:
        if 200 <= status_code < 300:
            return

        err_msg = ""
        if isinstance(data, dict):
            err_msg = data.get("error") or data.get("message") or data.get("detail") or ""
        if not err_msg:
            err_msg = raw_text or f"HTTP {status_code} Error"

        if status_code in (401, 403):
            raise AuthenticationError(
                f"Authentication failed: {err_msg}",
                status_code=status_code,
                response_body=data,
            )
        elif status_code == 404:
            raise NotFoundError(
                f"Resource not found: {err_msg}",
                status_code=status_code,
                response_body=data,
            )
        elif status_code in (400, 422):
            raise ValidationError(
                f"Validation error: {err_msg}",
                status_code=status_code,
                response_body=data,
            )
        elif status_code == 429:
            raise RateLimitError(
                f"Rate limit exceeded: {err_msg}",
                status_code=status_code,
                response_body=data,
            )
        elif 500 <= status_code < 600:
            raise ServerError(
                f"Server error: {err_msg}",
                status_code=status_code,
                response_body=data,
            )
        else:
            raise CloudCommandersError(
                f"Request failed: {err_msg}",
                status_code=status_code,
                response_body=data,
            )

    def _urllib_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
    ) -> Tuple[int, Dict[str, str], str, Any]:
        req_headers = dict(headers or {})

        if params:
            query_str = urllib.parse.urlencode(params)
            url = f"{url}?{query_str}" if "?" not in url else f"{url}&{query_str}"

        body_bytes = None
        if json_payload is not None:
            body_bytes = json.dumps(json_payload).encode("utf-8")
            req_headers["Content-Type"] = "application/json"
        elif data is not None:
            if isinstance(data, str):
                body_bytes = data.encode("utf-8")
            elif isinstance(data, bytes):
                body_bytes = data
            elif isinstance(data, dict):
                body_bytes = urllib.parse.urlencode(data).encode("utf-8")
                req_headers["Content-Type"] = "application/x-www-form-urlencoded"

        req = urllib.request.Request(url, data=body_bytes, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                status_code = response.status
                resp_headers = dict(response.headers)
                raw_text = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            status_code = e.code
            resp_headers = dict(e.headers)
            raw_text = e.read().decode("utf-8", errors="replace")

        try:
            parsed_data = json.loads(raw_text)
        except Exception:
            parsed_data = raw_text

        return status_code, resp_headers, raw_text, parsed_data

    # --------------------------------------------------------------------------
    # Context Manager & Lifecycle
    # --------------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP session."""
        if HAS_REQUESTS and self._session:
            self._session.close()

    def __enter__(self) -> "CloudCommandersClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        masked_key = (
            f"{self.api_key[:6]}...{self.api_key[-4:]}"
            if len(self.api_key) > 10
            else ("***" if self.api_key else "None")
        )
        return (
            f"CloudCommandersClient(base_url='{self.base_url}', "
            f"api_key='{masked_key}')"
        )
