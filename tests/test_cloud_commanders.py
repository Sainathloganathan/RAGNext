"""
Unit tests for Cloud Commanders SDK.
"""

import unittest
from unittest.mock import MagicMock, patch
from cloud_commanders import (
    CloudCommandersClient,
    CloudCommandersError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    HealthResponse,
    QueryResponse,
    Citation,
)


class TestCloudCommandersClient(unittest.TestCase):

    def setUp(self):
        self.api_key = "cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo"
        self.base_url = "http://127.0.0.1:8000"
        self.client = CloudCommandersClient(
            base_url=self.base_url,
            api_key=self.api_key,
            max_retries=1,
            timeout=5.0,
        )

    def test_initialization(self):
        self.assertEqual(self.client.base_url, "http://127.0.0.1:8000")
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertIn("Authorization", self.client._default_headers)
        self.assertEqual(
            self.client._default_headers["Authorization"],
            f"Bearer {self.api_key}",
        )
        self.assertEqual(
            self.client._default_headers["X-API-Key"],
            self.api_key,
        )

    def test_repr_masks_api_key(self):
        rep = repr(self.client)
        self.assertIn("http://127.0.0.1:8000", rep)
        self.assertNotIn(self.api_key, rep)
        self.assertIn("cc_liv", rep)
        self.assertIn("yPgo", rep)

    @patch("requests.Session.request")
    def test_health_success(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.text = '{"status": "healthy", "version": "1.0.0", "team": "Cyber Knights"}'
        mock_resp.json.return_value = {
            "status": "healthy",
            "version": "1.0.0",
            "team": "Cyber Knights",
        }
        mock_request.return_value = mock_resp

        health = self.client.health()
        self.assertIsInstance(health, HealthResponse)
        self.assertEqual(health.status, "healthy")
        self.assertEqual(health.team, "Cyber Knights")

    @patch("requests.Session.request")
    def test_query_rag_success(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.text = '{"success": true}'
        mock_resp.json.return_value = {
            "success": True,
            "query": "What is the policy allowance?",
            "intent": "CURRENT",
            "latencyMs": 42.5,
            "result": {
                "answer": "The remote work allowance is 20 days under Policy v3.0.",
                "confidence": "HIGH",
                "citations": [
                    {
                        "documentTitle": "Remote Work Policy",
                        "versionNumber": "3.0",
                        "page": 1,
                        "text": "Remote employees receive 20 days per annum.",
                    }
                ],
            },
        }
        mock_request.return_value = mock_resp

        res = self.client.query("What is the policy allowance?")
        self.assertIsInstance(res, QueryResponse)
        self.assertIn("20 days", res.answer)
        self.assertEqual(res.intent, "CURRENT")
        self.assertEqual(len(res.citations), 1)
        self.assertEqual(res.citations[0].version_number, "3.0")
        self.assertEqual(res.citations[0].page, 1)

    @patch("requests.Session.request")
    def test_authentication_error(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.text = '{"error": "Invalid API key"}'
        mock_resp.json.return_value = {"error": "Invalid API key"}
        mock_request.return_value = mock_resp

        with self.assertRaises(AuthenticationError) as ctx:
            self.client.get("/api/protected")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Invalid API key", str(ctx.exception))

    @patch("requests.Session.request")
    def test_not_found_error(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = '{"error": "Document not found"}'
        mock_resp.json.return_value = {"error": "Document not found"}
        mock_request.return_value = mock_resp

        with self.assertRaises(NotFoundError):
            self.client.documents.get("non-existent-id")

    @patch("requests.Session.request")
    def test_validation_error(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = '{"error": "Question cannot be empty"}'
        mock_resp.json.return_value = {"error": "Question cannot be empty"}
        mock_request.return_value = mock_resp

        with self.assertRaises(ValidationError):
            self.client.chat.query("")


if __name__ == "__main__":
    unittest.main()
