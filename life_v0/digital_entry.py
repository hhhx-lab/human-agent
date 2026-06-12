from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .activation import run_first_activation_preflight
from .archive import run_write_growth_archive
from .authority import run_source_authority
from .body import run_check_life_support, run_life_support
from .contracts import run_check_v0_contracts
from .direction import run_direction_lock
from .doc_index import run_doc_ingestion
from .growth import run_cycle
from .language import run_build_language_relationship, run_check_language_relationship
from .life_targets import run_birth_readiness
from .membrane import run_check_life_membrane, run_life_membrane
from .neural_core import run_check_neural_life_core, run_neural_life_core
from .process_supervisor import run_digital_life_process
from .process_supervisor.resident_lifecycle import (
    ResidentControlInputStream,
    mark_resident_lifecycle_active,
    mark_resident_lifecycle_stopped,
    read_resident_lifecycle_status,
    request_resident_stop,
    send_resident_relation_turn,
    start_background_resident_process,
)
from .reporting import run_emit_report
from .replay import run_replay_shadow
from .schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
from .stage_explain import run_explain_stage
from .state_store import run_check_state_store, run_state_store
from .validators import run_check_validation_membrane, run_validation_membrane


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="digital")
    subparsers = parser.add_subparsers(dest="command", required=True)

    life = subparsers.add_parser(
        "life",
        help="Restore the digital life birth shell, first terminal turn, and terminal life loop.",
    )
    life.add_argument("--state", default="runtime/state")
    life.add_argument("--reports", default="runtime/reports/latest")
    life.add_argument("--receipts", default="runtime/receipts")
    life.add_argument("--run-id", default=None)
    life.add_argument("--strict", action="store_true")
    life.add_argument(
        "--background",
        action="store_true",
        help="Start the digital life process as a detached resident process.",
    )
    life.add_argument(
        "--resident",
        action="store_true",
        help="Run the resident process loop without treating stdin EOF as death.",
    )
    life.add_argument(
        "--status",
        action="store_true",
        help="Print the current resident lifecycle state.",
    )
    life.add_argument(
        "--stop",
        action="store_true",
        help="Ask the resident process to close itself through its lifecycle command file.",
    )
    life.add_argument(
        "--say",
        default=None,
        help="Send one relation turn to the resident process and print its response.",
    )
    life.add_argument(
        "--attach",
        action="store_true",
        help="Attach this terminal to the resident process, starting it first if needed.",
    )
    life.add_argument(
        "--foreground",
        action="store_true",
        help="Run the foreground process loop even when stdin is an interactive terminal.",
    )
    life.add_argument("--say-timeout-seconds", type=float, default=30.0)
    life.add_argument("--resident-sleep-seconds", type=float, default=1.0)
    life.add_argument("--stop-timeout-seconds", type=float, default=10.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "life":
        state_dir = Path(args.state)
        reports_dir = Path(args.reports)
        receipts_dir = Path(args.receipts)
        terminal_dir = state_dir / "terminal"
        if args.status:
            result = read_resident_lifecycle_status(
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
            )
            print(json.dumps(result.state, ensure_ascii=False, indent=2))
            return result.exit_code
        if args.stop:
            result = request_resident_stop(
                terminal_dir=terminal_dir,
                timeout_seconds=args.stop_timeout_seconds,
            )
            print(json.dumps(result.state, ensure_ascii=False, indent=2))
            return result.exit_code
        if args.say is not None:
            result = send_resident_relation_turn(
                terminal_dir=terminal_dir,
                utterance=args.say,
                wait_timeout_seconds=args.say_timeout_seconds,
            )
            response_text = result.state.get("response_text")
            if response_text:
                print(response_text)
            else:
                print(json.dumps(result.state, ensure_ascii=False, indent=2))
            return result.exit_code

        if args.background:
            result = start_background_resident_process(
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                run_id=args.run_id,
                strict=args.strict,
                resident_sleep_seconds=args.resident_sleep_seconds,
                cwd=Path.cwd(),
            )
            print(json.dumps(result.state, ensure_ascii=False, indent=2))
            return result.exit_code
        if _should_attach_resident(args):
            return run_resident_terminal_client(
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                run_id=args.run_id,
                strict=args.strict,
                resident_sleep_seconds=args.resident_sleep_seconds,
                say_timeout_seconds=args.say_timeout_seconds,
            )

        bootstrap_exit = ensure_minimal_digital_life_runtime(
            docs_dir=Path("docs"),
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=args.run_id,
            strict=args.strict,
        )
        if bootstrap_exit != 0:
            return bootstrap_exit
        resident_lifecycle_run_id = args.run_id or _bootstrap_run_id(None, "resident")
        input_stream = None
        if args.resident:
            mark_resident_lifecycle_active(
                terminal_dir=terminal_dir,
                run_id=resident_lifecycle_run_id,
                resident_sleep_seconds=args.resident_sleep_seconds,
            )
            input_stream = ResidentControlInputStream(
                terminal_dir=terminal_dir,
                min_poll_seconds=args.resident_sleep_seconds,
            )
        result = run_digital_life_process(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=resident_lifecycle_run_id if args.resident else args.run_id,
            strict=args.strict,
            input_stream=input_stream,
        )
        if args.resident:
            mark_resident_lifecycle_stopped(
                terminal_dir=terminal_dir,
                run_id=resident_lifecycle_run_id,
                exit_code=result.exit_code,
            )
        return result.exit_code

    parser.error(f"unsupported command: {args.command}")
    return 5


def run_resident_terminal_client(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None,
    strict: bool,
    resident_sleep_seconds: float,
    say_timeout_seconds: float,
) -> int:
    terminal_dir = state_dir / "terminal"
    start_result = start_background_resident_process(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=run_id,
        strict=strict,
        resident_sleep_seconds=resident_sleep_seconds,
        cwd=Path.cwd(),
    )
    if start_result.exit_code != 0:
        print(json.dumps(start_result.state, ensure_ascii=False, indent=2))
        return start_result.exit_code

    for raw_line in sys.stdin:
        utterance = raw_line.rstrip("\n")
        command = utterance.strip().lower()
        if not utterance.strip():
            continue
        if command in {"/exit", "/quit"}:
            return 0
        if command in {"/stop", "/shutdown"}:
            stop_result = request_resident_stop(
                terminal_dir=terminal_dir,
                timeout_seconds=30.0,
            )
            print(json.dumps(stop_result.state, ensure_ascii=False, indent=2))
            return stop_result.exit_code
        turn_result = send_resident_relation_turn(
            terminal_dir=terminal_dir,
            utterance=utterance,
            wait_timeout_seconds=say_timeout_seconds,
        )
        response_text = turn_result.state.get("response_text")
        if response_text:
            print(response_text)
        else:
            print(json.dumps(turn_result.state, ensure_ascii=False, indent=2))
            if turn_result.exit_code != 0:
                return turn_result.exit_code
    return 0


def _should_attach_resident(args: argparse.Namespace) -> bool:
    if args.attach:
        return True
    if args.foreground or args.resident:
        return False
    return bool(sys.stdin.isatty())


def ensure_minimal_digital_life_runtime(
    *,
    docs_dir: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None,
    strict: bool,
) -> int:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    docs_dir = docs_dir.resolve()
    runtime_root = state_dir.parent
    doc_out = runtime_root / "docs"

    stage_explanation_report = reports_dir / "stage_explanation_report.json"
    if stage_explanation_report.exists():
        return 0

    doc_index_path = doc_out / "doc_carrier_index.json"
    direction_state = state_dir / "direction"
    authority_state = state_dir / "authority"
    neural_state = state_dir / "neural_life_core"
    membrane_state = state_dir / "membrane"
    life_targets_state = state_dir / "life_targets"
    validation_state = state_dir / "validation"
    observation_state = state_dir / "observation"
    schema_runner_state = state_dir / "schema_runner"

    steps = [
        lambda: run_doc_ingestion(
            docs_dir=docs_dir,
            out_dir=doc_out,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "ingest"),
            strict=strict,
        ),
        lambda: run_direction_lock(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            out_dir=direction_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "direction"),
            strict=strict,
        ),
        lambda: run_source_authority(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            direction_state_dir=direction_state,
            out_dir=authority_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "authority"),
            strict=strict,
        ),
        lambda: run_neural_life_core(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            authority_state_dir=authority_state,
            out_dir=neural_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "neural"),
            strict=strict,
        ),
        lambda: run_check_neural_life_core(
            state_dir=neural_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_state_store(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            neural_core_state_dir=neural_state,
            out_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "state"),
            strict=strict,
        ),
        lambda: run_check_state_store(
            state_dir=state_dir,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_life_membrane(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            direction_state_dir=direction_state,
            neural_core_state_dir=neural_state,
            state_dir=state_dir,
            out_dir=membrane_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "membrane"),
            strict=strict,
        ),
        lambda: run_check_life_membrane(
            membrane_dir=membrane_state,
            state_dir=state_dir,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_build_language_relationship(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            neural_core_state_dir=neural_state,
            state_dir=state_dir,
            membrane_dir=membrane_state,
            out_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "language"),
            strict=strict,
        ),
        lambda: run_check_language_relationship(
            state_dir=state_dir,
            membrane_dir=membrane_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_birth_readiness(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            direction_state_dir=direction_state,
            neural_core_state_dir=neural_state,
            state_dir=state_dir,
            membrane_dir=membrane_state,
            out_dir=life_targets_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "birth"),
            strict=strict,
        ),
        lambda: run_validation_membrane(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            membrane_dir=membrane_state,
            life_targets_dir=life_targets_state,
            validation_dir=validation_state,
            observation_dir=observation_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "validation"),
            strict=strict,
        ),
        lambda: run_check_validation_membrane(
            state_dir=state_dir,
            validation_dir=validation_state,
            observation_dir=observation_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_schema_runner(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "schema"),
            strict=strict,
        ),
        lambda: run_check_schema_runner(
            state_dir=schema_runner_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_schema_smoke(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "smoke"),
            strict=strict,
        ),
        lambda: run_life_support(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            validation_report_path=reports_dir / "validation_membrane_report.json",
            out_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "support"),
            strict=strict,
        ),
        lambda: run_check_life_support(
            state_dir=state_dir,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_cycle(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "cycle"),
            shadow_only=True,
            strict=strict,
        ),
        lambda: run_check_v0_contracts(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "contracts"),
            strict=strict,
        ),
        lambda: run_first_activation_preflight(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "preflight"),
            strict=strict,
        ),
        lambda: run_replay_shadow(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "replay"),
            strict=strict,
        ),
        lambda: run_write_growth_archive(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "archive"),
            strict=strict,
        ),
        lambda: run_emit_report(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "emit"),
            strict=strict,
        ),
        lambda: run_explain_stage(
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "stage"),
            strict=strict,
        ),
    ]

    for step in steps:
        result = step()
        if result.exit_code != 0:
            return result.exit_code

    return 0


def _bootstrap_run_id(run_id: str | None, suffix: str) -> str:
    prefix = run_id or "digital-life-bootstrap"
    return f"{prefix}-{suffix}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
