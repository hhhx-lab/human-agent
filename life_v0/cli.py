from __future__ import annotations

import argparse
import json
from pathlib import Path

from .doc_index import run_doc_ingestion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="life-v0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser(
        "ingest-docs",
        help="Build the P0 document carrier index before first activation.",
    )
    ingest.add_argument("--docs", default="docs")
    ingest.add_argument("--out", default="runtime/docs")
    ingest.add_argument("--reports", default="runtime/reports/latest")
    ingest.add_argument("--receipts", default="runtime/receipts")
    ingest.add_argument("--run-id", default=None)
    ingest.add_argument("--strict", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ingest-docs":
        result = run_doc_ingestion(
            docs_dir=Path(args.docs),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    parser.error(f"unsupported command: {args.command}")
    return 5
