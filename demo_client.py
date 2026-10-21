"""
Demonstration script for CloudCommandersClient.

Runs the exact instantiation snippet and demonstrates:
- Health check
- Listing documents
- Version-aware RAG query with citations
- Authenticated remote command execution
"""

import sys
from cloud_commanders import CloudCommandersClient, CloudCommandersError

# Exact instantiation snippet requested
client = CloudCommandersClient(
    base_url="http://127.0.0.1:8000",
    api_key="cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo",
)


def run_demo():
    print("=" * 65)
    print(" Cloud Commanders Client Demonstration")
    print(f" Initialized: {client}")
    print("=" * 65)

    try:
        # 1. Check Server Health
        print("\n[1] Checking Server Health...")
        health = client.health()
        print(f"    Status:      {health.status}")
        print(f"    Product:     {health.product or 'N/A'}")
        print(f"    Team:        {health.team or 'N/A'}")
        print(f"    Raw Payload: {health.raw}")

        # 2. List Documents
        print("\n[2] Fetching Documents...")
        docs = client.documents.list()
        print(f"    Found {len(docs)} document(s):")
        for d in docs:
            print(f"     • [{d.id}] {d.title} (Active: v{d.active_version}) - {d.category}")

        # 3. Perform Version-Aware Query
        query_text = "What is the current remote work policy allowance?"
        print(f"\n[3] Querying RAG Engine: '{query_text}'...")
        res = client.query(query_text)
        print(f"    Answer:     {res.answer}")
        print(f"    Intent:     {res.intent}")
        print(f"    Latency:    {res.latency_ms} ms")
        print(f"    Citations:  ({len(res.citations)} citation(s))")
        for c in res.citations:
            print(f"     • [{c.document_title} v{c.version_number}, Page {c.page}]: \"{c.text}\"")

        # 4. Command Orchestration
        print("\n[4] Executing Commander Task...")
        cmd_result = client.commands.execute("verify_version_consistency")
        print(f"    Task Status: {cmd_result.get('status')}")
        print(f"    Output:      {cmd_result.get('output')}")

        print("\n" + "=" * 65)
        print(" All operations completed successfully!")
        print("=" * 65)

    except CloudCommandersError as e:
        print(f"\n[!] Cloud Commanders Error ({type(e).__name__}): {e}", file=sys.stderr)
        print("    Tip: Ensure the server at http://127.0.0.1:8000 is running.", file=sys.stderr)
        print("    You can start the mock server in another terminal via: python mock_server.py", file=sys.stderr)
    except Exception as e:
        print(f"\n[!] Unexpected Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    run_demo()
