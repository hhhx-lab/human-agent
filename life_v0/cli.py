from __future__ import annotations

import argparse
import json
from pathlib import Path

from .activation import run_first_activation_preflight
from .archive import run_write_growth_archive
from .authority import run_source_authority
from .body import run_check_life_support, run_life_support
from .contracts import run_check_v0_contracts
from .digital_life import run_digital_life_birth
from .direction import run_direction_lock
from .doc_index import run_doc_ingestion
from .growth import run_cycle
from .language import run_build_language_relationship, run_check_language_relationship
from .life_targets import run_birth_readiness
from .membrane import run_check_life_membrane, run_life_membrane
from .neural_core import run_check_neural_life_core, run_neural_life_core
from .reporting import run_emit_report
from .replay import run_replay_shadow
from .schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
from .shell_command import run_digital_life_shell_command
from .stage_explain import run_explain_stage
from .state_store import run_check_state_store, run_state_store
from .terminal_loop import run_terminal_life_loop
from .terminal_turn import run_first_terminal_turn
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

    language_relationship = subparsers.add_parser(
        "build-language-relationship",
        help="Build the S07 language and relationship runtime after S03 life membrane.",
    )
    language_relationship.add_argument("--docs", default="docs")
    language_relationship.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    language_relationship.add_argument("--neural-core", default="runtime/state/neural_life_core")
    language_relationship.add_argument("--state", default="runtime/state")
    language_relationship.add_argument("--membrane", default="runtime/state/membrane")
    language_relationship.add_argument("--out", default="runtime/state")
    language_relationship.add_argument("--reports", default="runtime/reports/latest")
    language_relationship.add_argument("--receipts", default="runtime/receipts")
    language_relationship.add_argument("--run-id", default=None)
    language_relationship.add_argument("--strict", action="store_true")

    language_relationship_check = subparsers.add_parser(
        "check-language-relationship",
        help="Check the S07 language and relationship runtime state and stage gates.",
    )
    language_relationship_check.add_argument("--state", default="runtime/state")
    language_relationship_check.add_argument("--membrane", default="runtime/state/membrane")
    language_relationship_check.add_argument("--reports", default="runtime/reports/latest")
    language_relationship_check.add_argument("--strict", action="store_true")

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

    schema_runner = subparsers.add_parser(
        "build-schema-runner",
        help="Build the S09 schema runner code layer after S05 validation membrane.",
    )
    schema_runner.add_argument("--docs", default="docs")
    schema_runner.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    schema_runner.add_argument("--state", default="runtime/state")
    schema_runner.add_argument("--reports", default="runtime/reports/latest")
    schema_runner.add_argument("--receipts", default="runtime/receipts")
    schema_runner.add_argument("--run-id", default=None)
    schema_runner.add_argument("--strict", action="store_true")

    schema_runner_check = subparsers.add_parser(
        "check-schema-runner",
        help="Check the S09 schema runner state and stage gates.",
    )
    schema_runner_check.add_argument("--state", default="runtime/state/schema_runner")
    schema_runner_check.add_argument("--reports", default="runtime/reports/latest")
    schema_runner_check.add_argument("--strict", action="store_true")

    schema_smoke = subparsers.add_parser(
        "run-schema-smoke",
        help="Run the S09 schema runner smoke chain after schema runner build.",
    )
    schema_smoke.add_argument("--state", default="runtime/state")
    schema_smoke.add_argument("--reports", default="runtime/reports/latest")
    schema_smoke.add_argument("--receipts", default="runtime/receipts")
    schema_smoke.add_argument("--run-id", default=None)
    schema_smoke.add_argument("--strict", action="store_true")

    life_support = subparsers.add_parser(
        "build-life-support",
        help="Build the S06 life support development layer after S09 schema runner.",
    )
    life_support.add_argument("--docs", default="docs")
    life_support.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    life_support.add_argument("--state", default="runtime/state")
    life_support.add_argument("--validation", default="runtime/reports/latest/validation_membrane_report.json")
    life_support.add_argument("--out", default="runtime/state")
    life_support.add_argument("--reports", default="runtime/reports/latest")
    life_support.add_argument("--receipts", default="runtime/receipts")
    life_support.add_argument("--run-id", default=None)
    life_support.add_argument("--strict", action="store_true")

    life_support_check = subparsers.add_parser(
        "check-life-support",
        help="Check the S06 life support development state and stage gates.",
    )
    life_support_check.add_argument("--state", default="runtime/state")
    life_support_check.add_argument("--reports", default="runtime/reports/latest")
    life_support_check.add_argument("--strict", action="store_true")

    run_cycle_parser = subparsers.add_parser(
        "run-cycle",
        help="Run the S10 shadow-only runtime growth reconsolidation cycle after S06 life support.",
    )
    run_cycle_parser.add_argument("--state", default="runtime/state")
    run_cycle_parser.add_argument("--reports", default="runtime/reports/latest")
    run_cycle_parser.add_argument("--receipts", default="runtime/receipts")
    run_cycle_parser.add_argument("--run-id", default=None)
    run_cycle_parser.add_argument("--shadow-only", action="store_true", default=True)
    run_cycle_parser.add_argument("--strict", action="store_true")

    v0_contracts = subparsers.add_parser(
        "check-v0-contracts",
        help="Run the S11 v0 contract coverage and activation preflight closure check.",
    )
    v0_contracts.add_argument("--docs", default="docs")
    v0_contracts.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    v0_contracts.add_argument("--state", default="runtime/state")
    v0_contracts.add_argument("--reports", default="runtime/reports/latest")
    v0_contracts.add_argument("--receipts", default="runtime/receipts")
    v0_contracts.add_argument("--run-id", default=None)
    v0_contracts.add_argument("--strict", action="store_true")

    first_activation_preflight = subparsers.add_parser(
        "first-activation-preflight",
        help="Run the first activation preflight after S11 contract coverage closure.",
    )
    first_activation_preflight.add_argument("--docs", default="docs")
    first_activation_preflight.add_argument("--doc-index", default="runtime/docs/doc_carrier_index.json")
    first_activation_preflight.add_argument("--state", default="runtime/state")
    first_activation_preflight.add_argument("--reports", default="runtime/reports/latest")
    first_activation_preflight.add_argument("--receipts", default="runtime/receipts")
    first_activation_preflight.add_argument("--run-id", default=None)
    first_activation_preflight.add_argument("--strict", action="store_true")

    replay_shadow = subparsers.add_parser(
        "run-replay-shadow",
        help="Run the replay/shadow bridge after first activation preflight.",
    )
    replay_shadow.add_argument("--state", default="runtime/state")
    replay_shadow.add_argument("--reports", default="runtime/reports/latest")
    replay_shadow.add_argument("--receipts", default="runtime/receipts")
    replay_shadow.add_argument("--run-id", default=None)
    replay_shadow.add_argument("--strict", action="store_true")

    growth_archive = subparsers.add_parser(
        "write-growth-archive",
        help="Write the growth archive bundle after replay/shadow bridge.",
    )
    growth_archive.add_argument("--state", default="runtime/state")
    growth_archive.add_argument("--reports", default="runtime/reports/latest")
    growth_archive.add_argument("--receipts", default="runtime/receipts")
    growth_archive.add_argument("--run-id", default=None)
    growth_archive.add_argument("--strict", action="store_true")

    emit_report = subparsers.add_parser(
        "emit-report",
        help="Aggregate the latest activation chain reports into a first activation return bundle.",
    )
    emit_report.add_argument("--state", default="runtime/state")
    emit_report.add_argument("--reports", default="runtime/reports/latest")
    emit_report.add_argument("--receipts", default="runtime/receipts")
    emit_report.add_argument("--run-id", default=None)
    emit_report.add_argument("--strict", action="store_true")

    explain_stage = subparsers.add_parser(
        "explain-stage",
        help="Explain the current chain-tail stage after emit-report.",
    )
    explain_stage.add_argument("--reports", default="runtime/reports/latest")
    explain_stage.add_argument("--receipts", default="runtime/receipts")
    explain_stage.add_argument("--run-id", default=None)
    explain_stage.add_argument("--strict", action="store_true")

    digital_life = subparsers.add_parser(
        "digital-life",
        help="Run the minimal digital life birth shell after stage explanation closes.",
    )
    digital_life.add_argument("--state", default="runtime/state")
    digital_life.add_argument("--reports", default="runtime/reports/latest")
    digital_life.add_argument("--receipts", default="runtime/receipts")
    digital_life.add_argument("--run-id", default=None)
    digital_life.add_argument("--strict", action="store_true")

    first_terminal_turn = subparsers.add_parser(
        "first-terminal-turn",
        help="Restore the first terminal turn after digital life birth shell closure.",
    )
    first_terminal_turn.add_argument("--state", default="runtime/state")
    first_terminal_turn.add_argument("--reports", default="runtime/reports/latest")
    first_terminal_turn.add_argument("--receipts", default="runtime/receipts")
    first_terminal_turn.add_argument("--run-id", default=None)
    first_terminal_turn.add_argument("--strict", action="store_true")

    terminal_life_loop = subparsers.add_parser(
        "terminal-life-loop",
        help="Continue the restored terminal life loop after first terminal turn closure.",
    )
    terminal_life_loop.add_argument("--state", default="runtime/state")
    terminal_life_loop.add_argument("--reports", default="runtime/reports/latest")
    terminal_life_loop.add_argument("--receipts", default="runtime/receipts")
    terminal_life_loop.add_argument("--run-id", default=None)
    terminal_life_loop.add_argument("--strict", action="store_true")

    digital_life_shell = subparsers.add_parser(
        "digital life",
        help="Run the one-shot digital life shell that restores birth shell, first terminal turn, and terminal life loop.",
    )
    digital_life_shell.add_argument("--state", default="runtime/state")
    digital_life_shell.add_argument("--reports", default="runtime/reports/latest")
    digital_life_shell.add_argument("--receipts", default="runtime/receipts")
    digital_life_shell.add_argument("--run-id", default=None)
    digital_life_shell.add_argument("--strict", action="store_true")

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

    if args.command == "build-language-relationship":
        result = run_build_language_relationship(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
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

    if args.command == "check-language-relationship":
        result = run_check_language_relationship(
            state_dir=Path(args.state),
            membrane_dir=Path(args.membrane),
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

    if args.command == "build-schema-runner":
        result = run_schema_runner(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-schema-runner":
        result = run_check_schema_runner(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "run-schema-smoke":
        result = run_schema_smoke(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "build-life-support":
        result = run_life_support(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            state_dir=Path(args.state),
            validation_report_path=Path(args.validation),
            out_dir=Path(args.out),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-life-support":
        result = run_check_life_support(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "run-cycle":
        result = run_cycle(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            shadow_only=args.shadow_only,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "check-v0-contracts":
        result = run_check_v0_contracts(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "first-activation-preflight":
        result = run_first_activation_preflight(
            docs_dir=Path(args.docs),
            doc_index_path=Path(args.doc_index),
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "run-replay-shadow":
        result = run_replay_shadow(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "write-growth-archive":
        result = run_write_growth_archive(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "emit-report":
        result = run_emit_report(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "explain-stage":
        result = run_explain_stage(
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "digital-life":
        result = run_digital_life_birth(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "first-terminal-turn":
        result = run_first_terminal_turn(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "terminal-life-loop":
        result = run_terminal_life_loop(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    if args.command == "digital life":
        result = run_digital_life_shell_command(
            state_dir=Path(args.state),
            reports_dir=Path(args.reports),
            receipts_dir=Path(args.receipts),
            run_id=args.run_id,
            strict=args.strict,
        )
        print(json.dumps(result.report, ensure_ascii=False, indent=2))
        return result.exit_code

    parser.error(f"unsupported command: {args.command}")
    return 5
