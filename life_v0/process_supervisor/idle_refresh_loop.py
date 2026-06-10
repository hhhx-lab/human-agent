from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TextIO

from .heartbeat import write_waiting_heartbeat
from .turn_io import poll_input_line


@dataclass(frozen=True)
class IdleRefreshLoopResult:
    heartbeat_counter: int
    external_utterance: str | None
    exit_reason: str | None


def wait_for_next_external_relation_turn(
    *,
    input_stream: TextIO,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    reports_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    schema_cross_file_logic: dict[str, Any] | None = None,
    schema_run_manifest: dict[str, Any] | None = None,
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    schema_cross_file_logic_ref: str | None = None,
    schema_run_manifest_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    heartbeat_counter: int,
    poll_timeout_seconds: float = 0.05,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    poll_input_line_fn: Callable[[TextIO], str | None] | None = None,
    write_waiting_heartbeat_fn: Callable[..., int] = write_waiting_heartbeat,
) -> IdleRefreshLoopResult:
    while True:
        effective_poll_timeout_seconds = poll_timeout_seconds
        if poll_input_line_fn is None:
            effective_poll_timeout_seconds = _resolve_idle_poll_timeout_seconds(
                terminal_dir=terminal_dir,
                default_timeout_seconds=poll_timeout_seconds,
            )
            raw_line = poll_input_line(
                input_stream,
                timeout_seconds=effective_poll_timeout_seconds,
            )
        else:
            raw_line = poll_input_line_fn(input_stream)
        if raw_line is None:
            heartbeat_counter = write_waiting_heartbeat_fn(
                run_id=run_id,
                generated_at=generated_at,
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                relationship_timeline=relationship_timeline,
                commitment_expression_plan=commitment_expression_plan,
                apology_repair_language_trace=apology_repair_language_trace,
                body_rhythm_pulse=body_rhythm_pulse,
                need_state_vector=need_state_vector,
                self_narrative_trace=self_narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                source_doc_refs=source_doc_refs,
                readme_block_refs=readme_block_refs,
                runtime_carrier_refs=runtime_carrier_refs,
                replay_cue_bundle=replay_cue_bundle,
                offline_consolidation_frame=offline_consolidation_frame,
                growth_patch_candidate_queue=growth_patch_candidate_queue,
                nightmare_risk=nightmare_risk,
                belief_learning_plan=belief_learning_plan,
                language_learning_plan=language_learning_plan,
                relationship_learning_plan=relationship_learning_plan,
                signal_media_runtime=signal_media_runtime,
                belief_state=belief_state,
                prediction_error_field=prediction_error_field,
                active_sampling_plan=active_sampling_plan,
                memory_write_gate=memory_write_gate,
                state_merge_guard=state_merge_guard,
                schema_cross_file_logic=schema_cross_file_logic,
                schema_run_manifest=schema_run_manifest,
                replay_cue_bundle_ref=replay_cue_bundle_ref,
                offline_consolidation_frame_ref=offline_consolidation_frame_ref,
                growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
                nightmare_risk_ref=nightmare_risk_ref,
                belief_learning_plan_ref=belief_learning_plan_ref,
                language_learning_plan_ref=language_learning_plan_ref,
                relationship_learning_plan_ref=relationship_learning_plan_ref,
                signal_media_runtime_ref=signal_media_runtime_ref,
                belief_state_ref=belief_state_ref,
                prediction_error_field_ref=prediction_error_field_ref,
                active_sampling_plan_ref=active_sampling_plan_ref,
                memory_write_gate_ref=memory_write_gate_ref,
                state_merge_guard_ref=state_merge_guard_ref,
                schema_cross_file_logic_ref=schema_cross_file_logic_ref,
                schema_run_manifest_ref=schema_run_manifest_ref,
                growth_patch_candidate_ids=growth_patch_candidate_ids,
                replay_residue_ref_count=replay_residue_ref_count,
                dream_window_ref_count=dream_window_ref_count,
                growth_patch_candidate_count=growth_patch_candidate_count,
                responsibility_loop_state=responsibility_loop_state,
                world_contact_summary=world_contact_summary,
                pain_regret_repair_report=pain_regret_repair_report,
                responsibility_loop_state_ref=responsibility_loop_state_ref,
                world_contact_summary_ref=world_contact_summary_ref,
                pain_regret_repair_report_ref=pain_regret_repair_report_ref,
                now_iso=now_iso,
                write_json=write_json,
            )
            continue

        if raw_line == "":
            return IdleRefreshLoopResult(
                heartbeat_counter=heartbeat_counter,
                external_utterance=None,
                exit_reason="eof",
            )

        external_utterance = raw_line.strip()
        if not external_utterance:
            continue
        if external_utterance == "/exit":
            return IdleRefreshLoopResult(
                heartbeat_counter=heartbeat_counter,
                external_utterance=None,
                exit_reason="explicit_exit",
            )

        return IdleRefreshLoopResult(
            heartbeat_counter=heartbeat_counter,
            external_utterance=external_utterance,
            exit_reason=None,
        )


def _resolve_idle_poll_timeout_seconds(
    *,
    terminal_dir: Path,
    default_timeout_seconds: float,
) -> float:
    strategy_path = terminal_dir / "idle_strategy_state.json"
    if not strategy_path.exists():
        return default_timeout_seconds

    try:
        payload = json.loads(strategy_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return default_timeout_seconds

    heartbeat_interval_ms = payload.get("heartbeat_interval_ms")
    try:
        timeout_seconds = float(heartbeat_interval_ms) / 1000.0
    except (TypeError, ValueError):
        return default_timeout_seconds

    if timeout_seconds <= 0:
        return default_timeout_seconds
    return timeout_seconds
