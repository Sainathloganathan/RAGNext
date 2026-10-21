"""
Command line interface for Cloud Commanders SDK.
"""

import argparse
import json
import sys
from .client import CloudCommandersClient


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cloud_commanders",
        description="Cloud Commanders CLI Tool",
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="Base URL of Cloud Commanders API (default: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--api-key",
        default="cc_live_piuHBXmNvPlBQBttpAw28kDMlDfVqIMItSz-ebyyPgo",
        help="API Key (default: cc_live_...)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Health check
    subparsers.add_parser("health", help="Check server health")

    # Query command
    query_parser = subparsers.add_parser("query", help="Ask a question to the RAG engine")
    query_parser.add_argument("question", help="The question to ask")
    query_parser.add_argument("--doc-id", default=None, help="Target document ID")
    query_parser.add_argument("--status", default=None, help="Status filter (e.g. Active)")

    # Documents command
    subparsers.add_parser("documents", help="List all indexed documents")

    args = parser.parse_args()

    client = CloudCommandersClient(base_url=args.url, api_key=args.api_key)

    if args.command == "health" or args.command is None:
        try:
            print(f"Connecting to {args.url} ...")
            health = client.health()
            print(json.dumps(health.raw or {"status": health.status}, indent=2))
        except Exception as e:
            print(f"Error checking health: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "query":
        try:
            print(f"Querying: '{args.question}' ...")
            res = client.query(args.question, document_id=args.doc_id, status_filter=args.status)
            print(f"\n--- Answer ---")
            print(res.answer)
            if res.citations:
                print(f"\n--- Citations ({len(res.citations)}) ---")
                for c in res.citations:
                    print(f" • [v{c.version_number} - Page {c.page}] {c.document_title}: {c.text}")
        except Exception as e:
            print(f"Query error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "documents":
        try:
            docs = client.documents.list()
            print(f"Found {len(docs)} documents:")
            for d in docs:
                print(f" • [{d.id}] {d.title} (Active: v{d.active_version})")
        except Exception as e:
            print(f"Error listing documents: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
