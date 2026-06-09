from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

from .dialogue_events import build_external_turn_event, build_life_turn_event
from .heartbeat import write_waiting_heartbeat
from .idle_refresh_loop import wait_for_next_external_relation_turn
from .idle_strategy import IDLE_STRATEGY_STATE_REF
from .incident_recovery import (
    record_recovery_continuity,
    recover_from_dialogue_turn_exception,
)
from .process_closeout import close_digital_life_process
from .resident_turn_writeback import write_resident_turn_writeback
from .relaunch_recovery import detect_and_normalize_interrupted_previous_state
from .response_surface import compose_life_response
from ..shell_command import run_digital_life_shell_command


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
    "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "docs/90_language_event_examples_and_timeline_bundle.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
    "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
    "docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md",
    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "RunnerCliRuntime",
    "ComputerPeripheralRuntime",
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
]

# Keep these names as compatibility shims while the organ split settles into the
# wider process-supervisor test and patch surface.
_build_external_turn_event = build_external_turn_event
_build_life_turn_event = build_life_turn_event
_compose_life_response = compose_life_response


@dataclass(frozen=True)
class DigitalLifeProcessResult:
    exit_code: int
    report: dict[str, Any]


def run_digital_life_process(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> DigitalLifeProcessResult:
    run_id = run_id or _default_run_id("digital-life-process-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    input_stream = input_stream or sys.stdin
    output_stream = output_stream or sys.stdout

    terminal_dir = state_dir / "terminal"
    previous_safe_terminal_loop = _read_json_if_exists(terminal_dir / "safe_terminal_loop_state.json")
    previous_terminal_life_loop_state = _read_json_if_exists(terminal_dir / "terminal_life_loop_state.json")

    shell_result = run_digital_life_shell_command(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=f"{run_id}-restore",
        strict=strict,
    )
    if shell_result.exit_code != 0:
        return DigitalLifeProcessResult(exit_code=shell_result.exit_code, report=shell_result.report)

    language_dir = state_dir / "language"
    relationship_dir = state_dir / "relationship"

    _read_json(terminal_dir / "session_envelope.json")
    safe_terminal_loop = _read_json(terminal_dir / "safe_terminal_loop_state.json")
    terminal_life_loop_state = _read_json(terminal_dir / "terminal_life_loop_state.json")
    life_context_frame = _read_json_if_exists(terminal_dir / "life_context_frame.json")
    relation_turn_frame = _read_json_if_exists(terminal_dir / "relation_turn_frame.json")
    shared_term_registry = _read_json(language_dir / "shared_term_registry.json")
    self_narrative_trace = _read_json(language_dir / "self_narrative_language_trace.json")
    commitment_index = _read_json(language_dir / "commitment_repair_language_index.json")
    expression_plan = _read_json_if_exists(language_dir / "expression_plan.json")
    relationship_graph = _read_json(relationship_dir / "relationship_subject_graph.json")
    replay_cue_bundle = _read_json_if_exists(state_dir / "replay" / "replay_cue_bundle.json")
    offline_consolidation_frame = _read_json_if_exists(state_dir / "dream" / "offline_consolidation_frame.json")
    growth_patch_candidate_queue = _read_json_if_exists(state_dir / "growth" / "growth_patch_candidate_queue.json")
    replay_cue_bundle_ref = (
        "runtime/state/replay/replay_cue_bundle.json" if replay_cue_bundle else None
    )
    offline_consolidation_frame_ref = (
        "runtime/state/dream/offline_consolidation_frame.json" if offline_consolidation_frame else None
    )
    growth_patch_candidate_queue_ref = (
        "runtime/state/growth/growth_patch_candidate_queue.json" if growth_patch_candidate_queue else None
    )
    growth_patch_candidate_ids = [
        candidate.get("growth_patch_candidate_id")
        for candidate in growth_patch_candidate_queue.get("candidates", [])
        if isinstance(candidate, dict) and candidate.get("growth_patch_candidate_id")
    ]
    replay_residue_ref_count = len(replay_cue_bundle.get("turn_residue_refs", []))
    dream_window_ref_count = len(offline_consolidation_frame.get("dream_window_refs", []))
    growth_patch_candidate_count = len(growth_patch_candidate_queue.get("candidates", []))

    relaunch_recovery_count = 0
    last_relaunch_recovery_report_ref: str | None = None
    relaunch_recovery_report = detect_and_normalize_interrupted_previous_state(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        previous_safe_terminal_loop=previous_safe_terminal_loop,
        previous_terminal_life_loop_state=previous_terminal_life_loop_state,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        write_json=_write_json,
    )
    if relaunch_recovery_report is not None:
        relaunch_recovery_count = 1
        last_relaunch_recovery_report_ref = "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json"
        safe_terminal_loop["last_relaunch_recovery_report_ref"] = last_relaunch_recovery_report_ref
        terminal_life_loop_state["last_relaunch_recovery_report_ref"] = last_relaunch_recovery_report_ref
        record_recovery_continuity(
            self_narrative_trace=self_narrative_trace,
            commitment_index=commitment_index,
            relationship_graph=relationship_graph,
            event_kind="relaunch_recovery_normalization",
            report_ref=last_relaunch_recovery_report_ref,
            details={
                "previous_safe_terminal_mode": relaunch_recovery_report.get("previous_safe_terminal_mode"),
                "previous_terminal_loop_mode": relaunch_recovery_report.get("previous_terminal_loop_mode"),
                "normalized_mode": relaunch_recovery_report.get("normalized_mode"),
            },
        )
        _write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)
        _write_json(language_dir / "commitment_repair_language_index.json", commitment_index)
        _write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    reports_dir.mkdir(parents=True, exist_ok=True)
    heartbeat_counter = write_waiting_heartbeat(
        run_id=run_id,
        generated_at=generated_at,
        terminal_dir=terminal_dir,
        reports_dir=reports_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        relationship_graph=relationship_graph,
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        now_iso=_now_iso,
        write_json=_write_json,
    )

    _print_line(output_stream, "当前生命回合已恢复。输入新的关系性回合，使用 /exit 结束本次生命进程。")

    turn_counter = _current_dialogue_turn_count(language_dir / "dialogue_turn_log.jsonl")
    completed_turns = 0
    incident_count = 0
    last_external_turn: dict[str, Any] | None = None
    last_life_turn: dict[str, Any] | None = None
    last_incident_report_ref: str | None = None
    last_recovery_report_ref: str | None = None

    while True:
        idle_refresh = wait_for_next_external_relation_turn(
            input_stream=input_stream,
            run_id=run_id,
            generated_at=generated_at,
            terminal_dir=terminal_dir,
            reports_dir=reports_dir,
            language_dir=language_dir,
            relationship_dir=relationship_dir,
            safe_terminal_loop=safe_terminal_loop,
            terminal_life_loop_state=terminal_life_loop_state,
            self_narrative_trace=self_narrative_trace,
            commitment_index=commitment_index,
            relationship_graph=relationship_graph,
            source_doc_refs=SOURCE_DOC_REFS,
            readme_block_refs=READ_ME_BLOCK_REFS,
            runtime_carrier_refs=RUNTIME_CARRIER_REFS,
            replay_cue_bundle=replay_cue_bundle,
            offline_consolidation_frame=offline_consolidation_frame,
            growth_patch_candidate_queue=growth_patch_candidate_queue,
            replay_cue_bundle_ref=replay_cue_bundle_ref,
            offline_consolidation_frame_ref=offline_consolidation_frame_ref,
            growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
            growth_patch_candidate_ids=growth_patch_candidate_ids,
            replay_residue_ref_count=replay_residue_ref_count,
            dream_window_ref_count=dream_window_ref_count,
            growth_patch_candidate_count=growth_patch_candidate_count,
            heartbeat_counter=heartbeat_counter,
            now_iso=_now_iso,
            write_json=_write_json,
        )
        heartbeat_counter = idle_refresh.heartbeat_counter
        if idle_refresh.exit_reason is not None:
            exit_reason = idle_refresh.exit_reason
            break
        external_utterance = idle_refresh.external_utterance
        if external_utterance is None:
            continue

        turn_counter += 1
        external_turn_id = f"dialogue-turn-live-{turn_counter:04d}"
        external_turn = _build_external_turn_event(
            turn_id=external_turn_id,
            generated_at=_now_iso(),
            utterance=external_utterance,
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
        )
        try:
            turn_counter += 1
            life_turn_id = f"dialogue-turn-live-{turn_counter:04d}"
            life_response = _compose_life_response(
                external_utterance=external_utterance,
                relationship_graph=relationship_graph,
                shared_term_registry=shared_term_registry,
                commitment_index=commitment_index,
                relation_turn_frame=relation_turn_frame,
                expression_plan=expression_plan,
                life_context_frame=life_context_frame,
                replay_cue_bundle=replay_cue_bundle,
                offline_consolidation_frame=offline_consolidation_frame,
                growth_patch_candidate_queue=growth_patch_candidate_queue,
            )
            life_turn = _build_life_turn_event(
                turn_id=life_turn_id,
                generated_at=_now_iso(),
                utterance=life_response,
                shared_term_registry=shared_term_registry,
                commitment_index=commitment_index,
            )
            turn_writeback = write_resident_turn_writeback(
                run_id=run_id,
                terminal_dir=terminal_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                reports_dir=reports_dir,
                turn_counter=turn_counter,
                external_turn_id=external_turn_id,
                life_turn_id=life_turn_id,
                external_turn=external_turn,
                life_turn=life_turn,
                external_utterance=external_utterance,
                life_response=life_response,
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                self_narrative_trace=self_narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                source_doc_refs=SOURCE_DOC_REFS,
                readme_block_refs=READ_ME_BLOCK_REFS,
                runtime_carrier_refs=RUNTIME_CARRIER_REFS,
                replay_cue_bundle_ref=replay_cue_bundle_ref,
                now_iso=_now_iso,
                write_json=_write_json,
                append_jsonl=_append_jsonl,
            )
            safe_terminal_loop = turn_writeback.safe_terminal_loop
            terminal_life_loop_state = turn_writeback.terminal_life_loop_state
            last_external_turn = turn_writeback.last_external_turn
            last_life_turn = turn_writeback.last_life_turn
            completed_turns += 1

            _print_line(output_stream, f"生命回合输出: {life_response}")
        except Exception as exc:
            incident_count += 1
            incident_recovery = recover_from_dialogue_turn_exception(
                run_id=run_id,
                incident_count=incident_count,
                external_utterance=external_utterance,
                exc=exc,
                reports_dir=reports_dir,
                terminal_dir=terminal_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                self_narrative_trace=self_narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                write_json=_write_json,
                now_iso=_now_iso,
            )
            last_incident_report_ref = incident_recovery.incident_report_ref
            last_recovery_report_ref = incident_recovery.recovery_report_ref
            _print_line(output_stream, "生命回合处理出现异常，已执行异常恢复并回到等待态。")
            continue

    closeout = close_digital_life_process(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        heartbeat_counter=heartbeat_counter,
        completed_turns=completed_turns,
        incident_count=incident_count,
        relaunch_recovery_count=relaunch_recovery_count,
        exit_reason=exit_reason,
        last_incident_report_ref=last_incident_report_ref,
        last_recovery_report_ref=last_recovery_report_ref,
        last_relaunch_recovery_report_ref=last_relaunch_recovery_report_ref,
        last_external_turn=last_external_turn,
        last_life_turn=last_life_turn,
        waiting_mode=terminal_life_loop_state.get(
            "current_mode", "restored_waiting_for_external_turn"
        ),
        idle_strategy_ref=IDLE_STRATEGY_STATE_REF,
        last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
        last_dialogue_packet_ref=safe_terminal_loop.get("last_dialogue_packet_ref"),
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
        life_context_frame=life_context_frame,
        relation_turn_frame=relation_turn_frame,
        expression_plan=expression_plan,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        write_json=_write_json,
    )
    return DigitalLifeProcessResult(exit_code=0, report=closeout.report_bundle.report)


def _current_dialogue_turn_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])


def _append_jsonl(path: Path, payloads: list[dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for payload in payloads:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _print_line(stream: TextIO, text: str) -> None:
    stream.write(text + "\n")
    stream.flush()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
