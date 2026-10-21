"""
Exceptions for Cloud Commanders SDK.
"""

from typing import Optional, Any


class CloudCommandersError(Exception):
    """Base exception for all Cloud Commanders SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(CloudCommandersError):
    """Raised when authentication fails (HTTP 401 or 403)."""
    pass


class NotFoundError(CloudCommandersError):
    """Raised when a requested resource is not found (HTTP 404)."""
    pass


class ValidationError(CloudCommandersError):
    """Raised when request payload or parameters fail validation (HTTP 400 or 422)."""
    pass


class RateLimitError(CloudCommandersError):
    """Raised when rate limits are exceeded (HTTP 429)."""
    pass


class ServerError(CloudCommandersError):
    """Raised when the remote server returns a 5xx internal error."""
    pass


class ConnectionError(CloudCommandersError):
    """Raised when network connection or transport fails."""
    pass
