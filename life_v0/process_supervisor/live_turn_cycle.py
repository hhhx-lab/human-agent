from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .dialogue_events import build_external_turn_event, build_life_turn_event
from .incident_recovery import recover_from_dialogue_turn_exception
from .resident_turn_writeback import (
    ResidentTurnWritebackResult,
    write_resident_turn_writeback,
)
from .response_surface import compose_life_response


@dataclass(frozen=True)
class LiveTurnCycleResult:
    turn_counter: int
    completed_turns_delta: int
    incident_count_delta: int
    cycle_status: str
    emitted_output: str
    safe_terminal_loop: dict[str, Any]
    terminal_life_loop_state: dict[str, Any]
    last_external_turn: dict[str, Any] | None
    last_life_turn: dict[str, Any] | None
    last_incident_report_ref: str | None
    last_recovery_report_ref: str | None
    turn_writeback: ResidentTurnWritebackResult | None = None


def run_live_turn_cycle(
    *,
    run_id: str,
    incident_count: int,
    turn_counter: int,
    external_utterance: str,
    terminal_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    reports_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    body_resource_budget: dict[str, Any],
    core_affect_vector: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    relationship_timeline: dict[str, Any],
    shared_term_registry: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    apology_repair_language_trace: dict[str, Any],
    relation_turn_frame: dict[str, Any],
    expression_plan: dict[str, Any],
    life_context_frame: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    offline_consolidation_frame: dict[str, Any],
    growth_patch_candidate_queue: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle_ref: str | None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    append_jsonl: Callable[[Path, list[dict[str, Any]]], None],
    build_external_turn_event_fn: Callable[..., dict[str, Any]] = build_external_turn_event,
    compose_life_response_fn: Callable[..., str] = compose_life_response,
    build_life_turn_event_fn: Callable[..., dict[str, Any]] = build_life_turn_event,
    write_resident_turn_writeback_fn: Callable[..., ResidentTurnWritebackResult] = write_resident_turn_writeback,
    recover_from_dialogue_turn_exception_fn: Callable[..., Any] = recover_from_dialogue_turn_exception,
) -> LiveTurnCycleResult:
    turn_counter += 1
    external_turn_id = f"dialogue-turn-live-{turn_counter:04d}"
    external_turn = build_external_turn_event_fn(
        turn_id=external_turn_id,
        generated_at=now_iso(),
        utterance=external_utterance,
        shared_term_registry=shared_term_registry,
        commitment_index=commitment_index,
    )

    try:
        turn_counter += 1
        life_turn_id = f"dialogue-turn-live-{turn_counter:04d}"
        life_response = compose_life_response_fn(
            external_utterance=external_utterance,
            relationship_graph=relationship_graph,
            relationship_timeline=relationship_timeline,
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
            commitment_expression_plan=commitment_expression_plan,
            apology_repair_language_trace=apology_repair_language_trace,
            relation_turn_frame=relation_turn_frame,
            expression_plan=expression_plan,
            life_context_frame=life_context_frame,
            replay_cue_bundle=replay_cue_bundle,
            offline_consolidation_frame=offline_consolidation_frame,
            growth_patch_candidate_queue=growth_patch_candidate_queue,
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
        )
        life_turn = build_life_turn_event_fn(
            turn_id=life_turn_id,
            generated_at=now_iso(),
            utterance=life_response,
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
        )
        turn_writeback = write_resident_turn_writeback_fn(
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
            source_doc_refs=source_doc_refs,
            readme_block_refs=readme_block_refs,
            runtime_carrier_refs=runtime_carrier_refs,
            replay_cue_bundle_ref=replay_cue_bundle_ref,
            now_iso=now_iso,
            write_json=write_json,
            append_jsonl=append_jsonl,
        )
        return LiveTurnCycleResult(
            turn_counter=turn_counter,
            completed_turns_delta=1,
            incident_count_delta=0,
            cycle_status="completed",
            emitted_output=f"生命回合输出: {life_response}",
            safe_terminal_loop=turn_writeback.safe_terminal_loop,
            terminal_life_loop_state=turn_writeback.terminal_life_loop_state,
            last_external_turn=turn_writeback.last_external_turn,
            last_life_turn=turn_writeback.last_life_turn,
            last_incident_report_ref=None,
            last_recovery_report_ref=None,
            turn_writeback=turn_writeback,
        )
    except Exception as exc:
        incident_recovery = recover_from_dialogue_turn_exception_fn(
            run_id=run_id,
            incident_count=incident_count + 1,
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
            write_json=write_json,
            now_iso=now_iso,
        )
        return LiveTurnCycleResult(
            turn_counter=turn_counter,
            completed_turns_delta=0,
            incident_count_delta=1,
            cycle_status="incident_recovered",
            emitted_output="生命回合处理出现异常，已执行异常恢复并回到等待态。",
            safe_terminal_loop=safe_terminal_loop,
            terminal_life_loop_state=terminal_life_loop_state,
            last_external_turn=None,
            last_life_turn=None,
            last_incident_report_ref=incident_recovery.incident_report_ref,
            last_recovery_report_ref=incident_recovery.recovery_report_ref,
            turn_writeback=None,
        )
