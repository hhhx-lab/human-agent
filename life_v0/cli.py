from __future__ import annotations

import argparse
import json
from pathlib import Path

from .authority import run_source_authority
from .direction import run_direction_lock
from .doc_index import run_doc_ingestion
from .life_targets import run_birth_readiness
from .membrane import run_check_life_membrane, run_life_membrane
from .neural_core import run_check_neural_life_core, run_neural_life_core
from .state_store import run_check_state_store, run_state_store
from .validators import run_check_validation_membrane, run_validation_membrane


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

    direction = subparsers.add_parser(
        "build-direction-lock",
        help="Build the S00 direction lock after P0 document ingestion.",
    )
    direction.add_argument("--docs", default="docs")
    direction.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    direction.add_argument("--out", default="runtime/state/direction")
    direction.add_argument("--reports", default="runtime/reports/latest")
    direction.add_argument("--receipts", default="runtime/receipts")
    direction.add_argument("--run-id", default=None)
    direction.add_argument("--strict", action="store_true")

    authority = subparsers.add_parser(
        "build-source-authority",
        help="Build the S01 source authority registry after S00 direction lock.",
    )
    authority.add_argument("--docs", default="docs")
    authority.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    authority.add_argument("--direction", default="runtime/state/direction")
    authority.add_argument("--out", default="runtime/state/authority")
    authority.add_argument("--reports", default="runtime/reports/latest")
    authority.add_argument("--receipts", default="runtime/receipts")
    authority.add_argument("--run-id", default=None)
    authority.add_argument("--strict", action="store_true")

    neural_core = subparsers.add_parser(
        "build-neural-life-core",
        help="Build the S02 neural life core after S01 source authority.",
    )
    neural_core.add_argument("--docs", default="docs")
    neural_core.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    neural_core.add_argument("--authority", default="runtime/state/authority")
    neural_core.add_argument("--out", default="runtime/state/neural_life_core")
    neural_core.add_argument("--reports", default="runtime/reports/latest")
    neural_core.add_argument("--receipts", default="runtime/receipts")
    neural_core.add_argument("--run-id", default=None)
    neural_core.add_argument("--strict", action="store_true")

    neural_core_check = subparsers.add_parser(
        "check-neural-life-core",
        help="Check the S02 neural life core state and stage gates.",
    )
    neural_core_check.add_argument("--state", default="runtime/state/neural_life_core")
    neural_core_check.add_argument("--reports", default="runtime/reports/latest")
    neural_core_check.add_argument("--strict", action="store_true")

    state_store = subparsers.add_parser(
        "build-state-store",
        help="Build the S04 life state object store after S02 neural life core.",
    )
    state_store.add_argument("--docs", default="docs")
    state_store.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    state_store.add_argument("--neural-core", default="runtime/state/neural_life_core")
    state_store.add_argument("--out", default="runtime/state")
    state_store.add_argument("--reports", default="runtime/reports/latest")
    state_store.add_argument("--receipts", default="runtime/receipts")
    state_store.add_argument("--run-id", default=None)
    state_store.add_argument("--strict", action="store_true")

    state_store_check = subparsers.add_parser(
        "check-state-store",
        help="Check the S04 life state object store state and stage gates.",
    )
    state_store_check.add_argument("--state", default="runtime/state")
    state_store_check.add_argument("--reports", default="runtime/reports/latest")
    state_store_check.add_argument("--strict", action="store_true")

    membrane = subparsers.add_parser(
        "build-life-membrane",
        help="Build the S03 life membrane after S04 state object store.",
    )
    membrane.add_argument("--docs", default="docs")
    membrane.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    membrane.add_argument("--direction", default="runtime/state/direction")
    membrane.add_argument("--neural-core", default="runtime/state/neural_life_core")
    membrane.add_argument("--state", default="runtime/state")
    membrane.add_argument("--out", default="runtime/state/membrane")
    membrane.add_argument("--reports", default="runtime/reports/latest")
    membrane.add_argument("--receipts", default="runtime/receipts")
    membrane.add_argument("--run-id", default=None)
    membrane.add_argument("--strict", action="store_true")

    membrane_check = subparsers.add_parser(
        "check-life-membrane",
        help="Check the S03 life membrane state and stage gates.",
    )
    membrane_check.add_argument("--membrane", default="runtime/state/membrane")
    membrane_check.add_argument("--state", default="runtime/state")
    membrane_check.add_argument("--reports", default="runtime/reports/latest")
    membrane_check.add_argument("--strict", action="store_true")

    birth_readiness = subparsers.add_parser(
        "check-birth-readiness",
        help="Build the S08 life target status and birth readiness rollup after S03 life membrane.",
    )
    birth_readiness.add_argument("--docs", default="docs")
    birth_readiness.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    birth_readiness.add_argument("--direction", default="runtime/state/direction")
    birth_readiness.add_argument("--neural-core", default="runtime/state/neural_life_core")
    birth_readiness.add_argument("--state", default="runtime/state")
    birth_readiness.add_argument("--membrane", default="runtime/state/membrane")
    birth_readiness.add_argument("--out", default="runtime/state/life_targets")
    birth_readiness.add_argument("--reports", default="runtime/reports/latest")
    birth_readiness.add_argument("--receipts", default="runtime/receipts")
    birth_readiness.add_argument("--run-id", default=None)
    birth_readiness.add_argument("--strict", action="store_true")

    validation = subparsers.add_parser(
        "run-validation-membrane",
        help="Build the S05 validation membrane observation layer after S08 birth readiness.",
    )
    validation.add_argument("--docs", default="docs")
    validation.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    validation.add_argument("--state", default="runtime/state")
    validation.add_argument("--membrane", default="runtime/state/membrane")
    validation.add_argument("--life-targets", default="runtime/state/life_targets")
    validation.add_argument("--validation", default="runtime/state/validation")
    validation.add_argument("--observation", default="runtime/state/observation")
    validation.add_argument("--reports", default="runtime/reports/latest")
    validation.add_argument("--receipts", default="runtime/receipts")
    validation.add_argument("--run-id", default=None)
    validation.add_argument("--strict", action="store_true")

    validation_check = subparsers.add_parser(
        "check-validation-membrane",
        help="Check the S05 validation membrane observation state and stage gates.",
    )
    validation_check.add_argument("--state", default="runtime/state")
    validation_check.add_argument("--validation", default="runtime/state/validation")
    validation_check.add_argument("--observation", default="runtime/state/observation")
    validation_check.add_argument("--reports", default="runtime/reports/latest")
    validation_check.add_argument("--strict", action="store_true")

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

    if args.command == "build-direction-lock":
        result = run_direction_lock(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "build-source-authority":
        result = run_source_authority(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            direction_state_dir=Path(args.direction),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "build-neural-life-core":
        result = run_neural_life_core(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            authority_state_dir=Path(args.authority),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-neural-life-core":
        result = run_check_neural_life_core(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "build-state-store":
        result = run_state_store(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            neural_core_state_dir=Path(args.neural_core),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-state-store":
        result = run_check_state_store(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "build-life-membrane":
        result = run_life_membrane(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            direction_state_dir=Path(args.direction),
            neural_core_state_dir=Path(args.neural_core),
            state_dir=Path(args.state),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-life-membrane":
        result = run_check_life_membrane(
            membrane_dir=Path(args.membrane),
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-birth-readiness":
        result = run_birth_readiness(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            direction_state_dir=Path(args.direction),
            neural_core_state_dir=Path(args.neural_core),
            state_dir=Path(args.state),
            membrane_dir=Path(args.membrane),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "run-validation-membrane":
        result = run_validation_membrane(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            state_dir=Path(args.state),
            membrane_dir=Path(args.membrane),
            life_targets_dir=Path(args.life_targets),
            validation_dir=Path(args.validation),
            observation_dir=Path(args.observation),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-validation-membrane":
        result = run_check_validation_membrane(
            state_dir=Path(args.state),
            validation_dir=Path(args.validation),
            observation_dir=Path(args.observation),
            reports_dir=Path(args.reports),
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    parser.error(f"unsupported command: {args.command}")
    return 5
