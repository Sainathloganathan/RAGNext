"""
Commands and Task orchestration resource for Cloud Commanders SDK.
"""

from typing import Any, Dict, List, Optional
from .base import BaseResource
from ..exceptions import NotFoundError


class CommandsResource(BaseResource):
    """Resource for executing remote commands, orchestrations, and benchmark tasks."""

    def execute(
        self,
        command: str,
        params: Optional[Dict[str, Any]] = None,
        async_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute an action or command on the Cloud Commanders engine.
        """
        payload = {
            "command": command,
            "params": params or {},
            "async": async_run,
        }
        try:
            res = self._post("/api/commands/execute", json=payload)
        except NotFoundError:
            res = self._post("/commands", json=payload)
        return res.json()

    def get_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of an ongoing or completed task."""
        try:
            res = self._get(f"/api/commands/{task_id}")
        except NotFoundError:
            res = self._get(f"/commands/{task_id}")
        return res.json()
