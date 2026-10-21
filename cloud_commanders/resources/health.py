"""
Health check resource for Cloud Commanders SDK.
"""

from .base import BaseResource
from ..models import HealthResponse
from ..exceptions import NotFoundError


class HealthResource(BaseResource):
    """Resource for checking server and subsystem health."""

    def check(self) -> HealthResponse:
        """
        Check API health status.
        Tries `/api/health` first, falls back to `/health` or `/`.
        """
        try:
            res = self._get("/api/health")
        except NotFoundError:
            try:
                res = self._get("/health")
            except NotFoundError:
                res = self._get("/")

        data = res.json() if isinstance(res.json(), dict) else {"status": "ok", "raw": res.json()}
        return HealthResponse.from_dict(data)

    def ping(self) -> bool:
        """Return True if the remote server responds successfully."""
        try:
            health = self.check()
            return health.status.lower() in ("healthy", "ok", "ready", "running")
        except Exception:
            return False
