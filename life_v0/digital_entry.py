from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

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
from .process_supervisor.state_inspection import (
    STATE_INSPECTION_CATEGORIES,
    build_resident_state_inspection,
)
from .process_supervisor.terminal_input import (
    build_terminal_input_profile,
    read_interactive_line_with_idle_voice,
    write_terminal_input_profile,
)
from .process_supervisor.proactive_terminal_voice import (
    build_resident_proactive_terminal_event,
    write_resident_proactive_terminal_event,
)
from .process_supervisor.model_expression import (
    ModelExpressionTransport,
    compose_model_expression,
)
from .process_supervisor.terminal_ui import (
    render_dialogue_box,
    render_digital_life_banner,
    render_input_prompt,
    render_life_opening,
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
        help="Print a compact resident lifecycle status for the terminal.",
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
    life.add_argument(
        "--json",
        action="store_true",
        help="Print the full machine-readable lifecycle JSON for --status or --stop.",
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
            print(_format_lifecycle_output(result.state, action="status", full=args.json))
            return result.exit_code
        if args.stop:
            result = request_resident_stop(
                terminal_dir=terminal_dir,
                timeout_seconds=args.stop_timeout_seconds,
            )
            print(_format_lifecycle_output(result.state, action="stop", full=args.json))
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
            elif args.json:
                print(
                    json.dumps(
                        _format_relation_send_unreleased_output(result.state),
                        ensure_ascii=False,
                        indent=2,
                    )
                )
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

    life_name = str(start_result.state.get("life_name") or "").strip() or None
    print(
        render_digital_life_banner(
            life_name=life_name,
            status=str(start_result.state.get("status") or "resident"),
        )
    )
    print(render_life_opening(start_result.state, life_name=life_name))

    if sys.stdin.isatty():
        write_terminal_input_profile(
            terminal_dir=terminal_dir,
            profile=build_terminal_input_profile(
                input_stream=sys.stdin,
                idle_voice_interval_seconds=90.0,
            ),
        )
        return _run_interactive_resident_terminal_client(
            terminal_dir=terminal_dir,
            life_name=life_name,
            say_timeout_seconds=say_timeout_seconds,
        )

    for raw_line in sys.stdin:
        utterance = raw_line.rstrip("\n")
        exit_code = _handle_resident_terminal_utterance(
            terminal_dir=terminal_dir,
            utterance=utterance,
            life_name=life_name,
            say_timeout_seconds=say_timeout_seconds,
        )
        if exit_code is not None:
            return exit_code
    return 0


def _run_interactive_resident_terminal_client(
    *,
    terminal_dir: Path,
    life_name: str | None,
    say_timeout_seconds: float,
    read_line_fn: Callable[..., str] | None = None,
    idle_voice_interval_seconds: float = 90.0,
) -> int:
    def idle_voice_fn() -> bool:
        return _emit_resident_proactive_terminal_voice(
            terminal_dir=terminal_dir,
            life_name=life_name,
        )

    while True:
        try:
            prompt = render_input_prompt(life_name=life_name)
            if read_line_fn is None:
                utterance = read_interactive_line_with_idle_voice(
                    prompt=prompt,
                    idle_voice_fn=idle_voice_fn,
                    idle_voice_interval_seconds=idle_voice_interval_seconds,
                )
            else:
                utterance = read_line_fn(
                    prompt=prompt,
                    idle_voice_fn=idle_voice_fn,
                )
        except KeyboardInterrupt:
            print()
            return 130
        except EOFError:
            print()
            return 0
        exit_code = _handle_resident_terminal_utterance(
            terminal_dir=terminal_dir,
            utterance=utterance,
            life_name=life_name,
            say_timeout_seconds=say_timeout_seconds,
        )
        if exit_code is not None:
            return exit_code


def _handle_resident_terminal_utterance(
    *,
    terminal_dir: Path,
    utterance: str,
    life_name: str | None,
    say_timeout_seconds: float,
) -> int | None:
    command = utterance.strip().lower()
    if not utterance.strip():
        return None
    if command in {"/help", "/commands"}:
        print(
            render_dialogue_box(
                "终端命令",
                "\n".join(
                    [
                        "/state 查看常驻状态",
                        "/context 查看关系上下文",
                        "/memory 查看记忆摘要",
                        "/dream 查看梦境和离线整合",
                        "/body 查看身体和内环境",
                        "/emotion 查看情绪和调节",
                        "/relationship 查看关系",
                        "/language 查看语言系统",
                        "/cognition 查看工作区、预测和写门",
                        "/consciousness 查看意识工作区和可报告性",
                        "/thinking 查看思考和内言语状态",
                        "/personality 查看人格慢变量",
                        "/ability 查看能力和出生准备",
                        "/vision 查看视觉/感知状态",
                        "/proactive 查看主动发话状态",
                        "/exit 离开当前终端；/stop 请求停止常驻进程",
                    ]
                ),
            )
        )
        return None
    if command.lstrip("/") in STATE_INSPECTION_CATEGORIES or command in {
        "/status",
        "/记忆",
        "/梦境",
        "/身体",
        "/情绪",
        "/inner",
        "/内环境",
        "/关系",
        "/语言",
        "/认知",
        "/意识",
        "/思考",
        "/上下文",
        "/人格",
        "/性格",
        "/能力",
        "/视觉",
        "/感知",
        "/vision",
        "/visual",
        "/proactive",
        "/主动",
        "/主动语音",
        "/voice",
    }:
        inspection = build_resident_state_inspection(
            terminal_dir=terminal_dir,
            category=command,
        )
        print(
            render_dialogue_box(
                "状态查看",
                json.dumps(inspection, ensure_ascii=False, indent=2),
            )
        )
        return None
    if command in {"/exit", "/quit"}:
        print(
            render_dialogue_box(
                "终端连接",
                json.dumps(
                    {
                        "terminal_session": "detached",
                        "resident_process": "kept_alive",
                        "state_persistence": "runtime/state",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            )
        )
        return 0
    if command in {"/stop", "/shutdown"}:
        stop_result = request_resident_stop(
            terminal_dir=terminal_dir,
            timeout_seconds=30.0,
        )
        print(
            render_dialogue_box(
                "Digital Life",
                json.dumps(
                    _lifecycle_terminal_summary(stop_result.state, action="stop"),
                    ensure_ascii=False,
                    indent=2,
                ),
            )
        )
        return stop_result.exit_code
    turn_result = send_resident_relation_turn(
        terminal_dir=terminal_dir,
        utterance=utterance,
        wait_timeout_seconds=say_timeout_seconds,
    )
    response_text = turn_result.state.get("response_text")
    if response_text:
        print(render_dialogue_box(life_name or "Digital Life", str(response_text)))
    elif turn_result.exit_code != 0:
        return turn_result.exit_code
    return None


def _emit_resident_proactive_terminal_voice(
    *,
    terminal_dir: Path,
    life_name: str | None,
    now_iso=None,
    model_transport: ModelExpressionTransport | None = None,
    environ: dict[str, str] | None = None,
) -> bool:
    event = build_resident_proactive_terminal_event(
        terminal_dir=terminal_dir,
        life_name=life_name,
        now_iso=now_iso or _now_iso,
    )
    state_root = terminal_dir.parent
    generated_at = str(event.get("generated_at") or _now_iso())
    model_result = compose_model_expression(
        run_id="resident-proactive-" + str(event.get("composition_fingerprint") or "event"),
        generated_at=generated_at,
        external_utterance="open_terminal_idle",
        audited_expression_material=json.dumps(
            {
                key: value
                for key, value in event.items()
                if key not in {"utterance"}
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        language_dir=state_root / "language",
        reports_dir=state_root.parent / "reports" / "latest",
        terminal_life_loop_state=_read_runtime_json(
            terminal_dir / "terminal_life_loop_state.json"
        ),
        relationship_memory=_read_runtime_json(
            state_root / "memory" / "relationship_memory.json"
        ),
        dialogue_memory_summary=_read_runtime_json(
            state_root / "memory" / "dialogue_memory_summary.json"
        ),
        memory_retrieval_frame=_read_runtime_json(
            state_root / "memory" / "memory_retrieval_frame.json"
        ),
        repo_root=Path.cwd(),
        environ=environ,
        transport=model_transport,
        write_json=_write_runtime_json,
    )
    event["utterance"] = model_result.response_text
    event["model_expression_status"] = model_result.state.get(
        "model_expression_status"
    )
    event["model_expression_state_ref"] = model_result.state_ref
    event["model_expression_report_ref"] = model_result.report_ref
    event["post_expression_gate_status"] = model_result.state.get(
        "post_expression_gate_status"
    )
    written = write_resident_proactive_terminal_event(
        terminal_dir=terminal_dir,
        event=event,
    )
    utterance = str(written.get("utterance") or "").strip()
    if not utterance:
        return False
    print(render_dialogue_box(life_name or "Digital Life", utterance))
    return True


def _read_runtime_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_runtime_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _format_relation_send_unreleased_output(state: dict) -> dict:
    response_event = state.get("response_event")
    response_status = None
    if isinstance(response_event, dict):
        response_status = response_event.get("status")
    return {
        "schema_version": "resident_relation_send_result_v0",
        "send_status": state.get("send_status"),
        "response_status": response_status,
        "natural_language_released": False,
        "resident_lifecycle_state_ref": state.get("resident_lifecycle_state_ref"),
        "resident_relation_inbox_ref": state.get("resident_relation_inbox_ref"),
        "resident_relation_outbox_ref": state.get("resident_relation_outbox_ref"),
        "resident_relation_queue_state_ref": state.get(
            "resident_relation_queue_state_ref"
        ),
        "pid": state.get("pid"),
        "pid_alive": state.get("pid_alive"),
    }


def _should_attach_resident(args: argparse.Namespace) -> bool:
    if args.attach:
        return True
    if args.foreground or args.resident:
        return False
    return bool(sys.stdin.isatty())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _format_lifecycle_output(
    state: dict,
    *,
    action: str,
    full: bool,
) -> str:
    if full:
        return json.dumps(state, ensure_ascii=False, indent=2)
    return json.dumps(
        _lifecycle_terminal_summary(state, action=action),
        ensure_ascii=False,
        indent=2,
    )


def _lifecycle_terminal_summary(state: dict, *, action: str) -> dict:
    long_term = state.get("resident_long_term_residency_status") or {}
    summary = {
        "schema_version": "resident_lifecycle_terminal_summary_v0",
        "action": action,
        "status": state.get("status"),
        "run_id": state.get("run_id"),
        "pid": state.get("pid"),
        "pid_alive": state.get("pid_alive"),
        "life_name": state.get("life_name"),
        "life_name_id": state.get("life_name_id"),
        "life_name_lock_state": state.get("life_name_lock_state"),
        "residency_mode": state.get("residency_mode"),
        "residency_posture": state.get("residency_posture"),
        "relation_queue_status": state.get("resident_relation_queue_status"),
        "relation_last_completed_sequence": state.get(
            "resident_relation_last_completed_sequence"
        ),
        "autonomous_activity_count": state.get("resident_autonomous_activity_count"),
        "autonomous_activity_last_kind": state.get(
            "resident_autonomous_activity_last_kind"
        ),
        "autonomous_activity_cycle_completion_count": state.get(
            "resident_autonomous_activity_cycle_completion_count"
        ),
        "autonomous_activity_cycle_coverage_complete": state.get(
            "resident_autonomous_activity_cycle_coverage_complete"
        ),
        "autonomous_activity_next_kind": state.get(
            "resident_autonomous_activity_next_kind"
        ),
        "waiting_heartbeat_counter": state.get("resident_waiting_heartbeat_counter"),
        "waiting_mode": state.get("resident_waiting_mode"),
        "next_required_action": state.get("resident_next_required_action"),
        "governance_phase": state.get("resident_governance_phase"),
        "governance_attention_target": state.get(
            "resident_governance_attention_target"
        ),
        "idle_probe_mode": state.get("resident_idle_probe_mode"),
        "next_idle_action": state.get("resident_next_idle_action"),
        "heartbeat_interval_ms": state.get("resident_heartbeat_interval_ms"),
        "terminal_current_mode": state.get("resident_terminal_current_mode"),
        "resident_process_lease_state": state.get("resident_process_lease_state"),
        "resident_process_identity_continuity_state": state.get(
            "resident_process_identity_continuity_state"
        ),
        "resident_process_lease_history_event_count": state.get(
            "resident_process_lease_history_event_count"
        ),
        "persistent_process_status": state.get("resident_persistent_process_status")
        or long_term.get("persistent_process_status"),
        "background_convergence_state": state.get(
            "resident_background_convergence_state"
        )
        or long_term.get("background_convergence_state"),
        "background_convergence_pressure_level": state.get(
            "resident_background_convergence_pressure_level"
        )
        or long_term.get("background_convergence_pressure_level"),
        "evidence_refs": long_term.get("evidence_refs", []),
        "full_json_hint": "pass --json to print the complete lifecycle evidence tree",
    }
    return {key: value for key, value in summary.items() if value is not None}


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
