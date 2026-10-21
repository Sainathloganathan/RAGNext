"""
Local Cloud Commanders Mock / Proxy Server (Port 8000).
Run this to test CloudCommandersClient locally against live endpoints.

Usage:
    python mock_server.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import re

EXPECTED_API_KEY = "cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo"
PORT = 8000


class CloudCommandersHandler(BaseHTTPRequestHandler):

    def _send_json(self, status: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def _verify_auth(self) -> bool:
        auth_header = self.headers.get("Authorization", "")
        api_key_header = self.headers.get("X-API-Key", "")

        bearer_match = re.match(r"^Bearer\s+(.+)$", auth_header)
        token = bearer_match.group(1) if bearer_match else ""

        if token == EXPECTED_API_KEY or api_key_header == EXPECTED_API_KEY:
            return True

        self._send_json(401, {
            "success": False,
            "error": "Unauthorized: Invalid or missing Cloud Commanders API key.",
            "providedToken": token or api_key_header,
        })
        return False

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Root or health endpoints
        if path in ("/", "/api/health", "/health"):
            if not self._verify_auth():
                return
            return self._send_json(200, {
                "status": "healthy",
                "product": "Cloud Commanders — Version-Aware RAG Engine",
                "version": "1.0.0",
                "team": "Cyber Knights",
                "port": PORT,
                "authenticated": True,
            })

        # Documents list
        if path == "/api/documents":
            if not self._verify_auth():
                return
            return self._send_json(200, {
                "success": True,
                "documents": [
                    {
                        "id": "doc-001",
                        "title": "Remote Work Security Policy",
                        "category": "Security",
                        "department": "IT Operations",
                        "versionsCount": 3,
                        "activeVersion": "3.0",
                    },
                    {
                        "id": "doc-002",
                        "title": "Annual Leave Policy Manual",
                        "category": "HR",
                        "department": "People & Culture",
                        "versionsCount": 3,
                        "activeVersion": "3.0",
                    },
                ],
            })

        if not self._verify_auth():
            return

        self._send_json(404, {"success": False, "error": f"Endpoint '{path}' not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if not self._verify_auth():
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        # Chat / RAG query endpoint
        if path in ("/api/chat", "/chat"):
            question = payload.get("question", "")
            if not question.strip():
                return self._send_json(400, {"success": False, "error": "Question cannot be empty"})

            # Sample intelligent response
            return self._send_json(200, {
                "success": True,
                "query": question,
                "intent": "CURRENT",
                "latencyMs": 35.8,
                "eligibleVersions": [
                    {"id": "v3-id", "versionNumber": "3.0", "status": "Active", "documentId": "doc-001"}
                ],
                "result": {
                    "answer": f"According to Remote Work Security Policy v3.0, remote employees are authorized up to 20 remote days per annum, subject to VPN and MFA compliance.",
                    "confidence": "HIGH",
                    "statusNote": "Resolved exclusively against active document version v3.0.",
                    "citations": [
                        {
                            "versionNumber": "3.0",
                            "documentTitle": "Remote Work Security Policy",
                            "page": 1,
                            "chunkId": "chunk-v3-p1",
                            "score": 0.94,
                            "text": "Section 4.1: Eligible employees receive an annual quota of 20 remote working days.",
                        }
                    ],
                },
            })

        # Commands execute endpoint
        if path in ("/api/commands/execute", "/commands"):
            cmd = payload.get("command", "status")
            return self._send_json(200, {
                "success": True,
                "taskId": "task-cmd-901",
                "status": "COMPLETED",
                "command": cmd,
                "output": f"Command '{cmd}' executed successfully.",
            })

        self._send_json(404, {"success": False, "error": f"Endpoint '{path}' not found"})

    def log_message(self, format, *args):
        # Clean logging
        print(f"[CloudCommanders Mock 8000] {self.address_string()} - {format % args}")


def run_server():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, CloudCommandersHandler)
    print(f"===========================================================")
    print(f" Cloud Commanders Local Server running on http://127.0.0.1:{PORT}")
    print(f" Authentication Key: {EXPECTED_API_KEY}")
    print(f" Press Ctrl+C to terminate.")
    print(f"===========================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
