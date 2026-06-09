from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TextIO

from .idle_refresh_loop import IdleRefreshLoopResult, wait_for_next_external_relation_turn
from .live_turn_cycle import LiveTurnCycleResult, run_live_turn_cycle


@dataclass(frozen=True)
class ProcessSessionLoopResult:
    turn_counter: int
    completed_turns: int
    incident_count: int
    heartbeat_counter: int
    exit_reason: str
    safe_terminal_loop: dict[str, Any]
    terminal_life_loop_state: dict[str, Any]
    last_external_turn: dict[str, Any] | None
    last_life_turn: dict[str, Any] | None
    last_incident_report_ref: str | None
    last_recovery_report_ref: str | None


def run_process_session_loop(
    *,
    run_id: str,
    generated_at: str,
    input_stream: TextIO,
    terminal_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    reports_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    body_resource_budget: dict[str, Any],
    core_affect_vector: dict[str, Any],
    life_context_frame: dict[str, Any],
    relation_turn_frame: dict[str, Any],
    shared_term_registry: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    expression_plan: dict[str, Any],
    relationship_graph: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    offline_consolidation_frame: dict[str, Any],
    growth_patch_candidate_queue: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle_ref: str | None,
    offline_consolidation_frame_ref: str | None,
    growth_patch_candidate_queue_ref: str | None,
    growth_patch_candidate_ids: list[str],
    replay_residue_ref_count: int,
    dream_window_ref_count: int,
    growth_patch_candidate_count: int,
    heartbeat_counter: int,
    turn_counter: int,
    completed_turns: int = 0,
    incident_count: int = 0,
    emit_output: Callable[[str], None] | None = None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    append_jsonl: Callable[[Path, list[dict[str, Any]]], None],
    wait_for_next_external_relation_turn_fn: Callable[..., IdleRefreshLoopResult] = wait_for_next_external_relation_turn,
    run_live_turn_cycle_fn: Callable[..., LiveTurnCycleResult] = run_live_turn_cycle,
) -> ProcessSessionLoopResult:
    emit_output = emit_output or (lambda text: None)
    last_external_turn: dict[str, Any] | None = None
    last_life_turn: dict[str, Any] | None = None
    last_incident_report_ref: str | None = None
    last_recovery_report_ref: str | None = None

    while True:
        idle_refresh = wait_for_next_external_relation_turn_fn(
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
            source_doc_refs=source_doc_refs,
            readme_block_refs=readme_block_refs,
            runtime_carrier_refs=runtime_carrier_refs,
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
            now_iso=now_iso,
            write_json=write_json,
        )
        heartbeat_counter = idle_refresh.heartbeat_counter
        if idle_refresh.exit_reason is not None:
            return ProcessSessionLoopResult(
                turn_counter=turn_counter,
                completed_turns=completed_turns,
                incident_count=incident_count,
                heartbeat_counter=heartbeat_counter,
                exit_reason=idle_refresh.exit_reason,
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                last_external_turn=last_external_turn,
                last_life_turn=last_life_turn,
                last_incident_report_ref=last_incident_report_ref,
                last_recovery_report_ref=last_recovery_report_ref,
            )

        external_utterance = idle_refresh.external_utterance
        if external_utterance is None:
            continue

        live_turn_cycle = run_live_turn_cycle_fn(
            run_id=run_id,
            incident_count=incident_count,
            turn_counter=turn_counter,
            external_utterance=external_utterance,
            terminal_dir=terminal_dir,
            language_dir=language_dir,
            relationship_dir=relationship_dir,
            reports_dir=reports_dir,
            safe_terminal_loop=safe_terminal_loop,
            terminal_life_loop_state=terminal_life_loop_state,
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
            self_narrative_trace=self_narrative_trace,
            commitment_index=commitment_index,
            relationship_graph=relationship_graph,
            shared_term_registry=shared_term_registry,
            relation_turn_frame=relation_turn_frame,
            expression_plan=expression_plan,
            life_context_frame=life_context_frame,
            replay_cue_bundle=replay_cue_bundle,
            offline_consolidation_frame=offline_consolidation_frame,
            growth_patch_candidate_queue=growth_patch_candidate_queue,
            source_doc_refs=source_doc_refs,
            readme_block_refs=readme_block_refs,
            runtime_carrier_refs=runtime_carrier_refs,
            replay_cue_bundle_ref=replay_cue_bundle_ref,
            now_iso=now_iso,
            write_json=write_json,
            append_jsonl=append_jsonl,
        )
        turn_counter = live_turn_cycle.turn_counter
        completed_turns += live_turn_cycle.completed_turns_delta
        incident_count += live_turn_cycle.incident_count_delta
        safe_terminal_loop = live_turn_cycle.safe_terminal_loop
        terminal_life_loop_state = live_turn_cycle.terminal_life_loop_state
        if live_turn_cycle.last_external_turn is not None:
            last_external_turn = live_turn_cycle.last_external_turn
        if live_turn_cycle.last_life_turn is not None:
            last_life_turn = live_turn_cycle.last_life_turn
        if live_turn_cycle.last_incident_report_ref is not None:
            last_incident_report_ref = live_turn_cycle.last_incident_report_ref
        if live_turn_cycle.last_recovery_report_ref is not None:
            last_recovery_report_ref = live_turn_cycle.last_recovery_report_ref

        emit_output(live_turn_cycle.emitted_output)
