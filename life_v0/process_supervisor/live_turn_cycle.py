from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .dialogue_events import build_external_turn_event, build_life_turn_event
from .incident_recovery import recover_from_dialogue_turn_exception
from .live_language_turn import LiveLanguageTurnState, refresh_live_language_turn
from .resident_governance_handoff import (
    write_live_turn_waiting_governance_handoff,
)
from .resident_turn_writeback import (
    ResidentTurnWritebackResult,
    write_resident_turn_writeback,
)
from .model_expression import ModelExpressionResult, compose_model_expression
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
    self_model_state: dict[str, Any] | None,
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
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle_ref: str | None,
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
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    append_jsonl: Callable[[Path, list[dict[str, Any]]], None],
    build_external_turn_event_fn: Callable[..., dict[str, Any]] = build_external_turn_event,
    compose_life_response_fn: Callable[..., str] = compose_life_response,
    build_life_turn_event_fn: Callable[..., dict[str, Any]] = build_life_turn_event,
    refresh_live_language_turn_fn: Callable[..., LiveLanguageTurnState] = refresh_live_language_turn,
    write_resident_turn_writeback_fn: Callable[..., ResidentTurnWritebackResult] = write_resident_turn_writeback,
    write_live_turn_waiting_governance_handoff_fn: Callable[..., dict[str, Any]] = write_live_turn_waiting_governance_handoff,
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
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
    )

    try:
        generated_at = now_iso()
        state_dir = terminal_dir.parent
        live_language_turn = refresh_live_language_turn_fn(
            run_id=run_id,
            generated_at=generated_at,
            external_utterance=external_utterance,
            language_dir=language_dir,
            state_dir=state_dir,
            relation_scope_index=_read_json_if_exists(
                language_dir / "relation_scope_language_index.json",
                {"relation_scopes": [{"relation_role": "friend"}]},
            ),
            shared_term_registry=shared_term_registry,
            language_state=_read_json_if_exists(
                language_dir / "language_relationship_state.json",
                {},
            ),
            commitment_repair_index=commitment_index,
            self_narrative_trace=self_narrative_trace,
            life_state=_read_json_if_exists(state_dir / "life_state.json", {}),
            source_doc_refs=source_doc_refs,
            replay_cue_bundle=replay_cue_bundle,
            offline_consolidation_frame=offline_consolidation_frame,
            growth_patch_candidate_queue=growth_patch_candidate_queue,
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
            belief_state=belief_state,
            prediction_error_field=prediction_error_field,
            active_sampling_plan=active_sampling_plan,
            memory_write_gate=memory_write_gate,
            signal_media_runtime=signal_media_runtime,
            write_json=write_json,
        )
        brain_graph = _read_json_if_exists(
            state_dir / "neural_life_core" / "brain_graph.json",
            {},
        )
        network_state = _read_json_if_exists(
            state_dir / "neural_life_core" / "network_state.json",
            {},
        )
        prediction_workspace = _read_json_if_exists(
            state_dir / "prediction" / "prediction_workspace_frame.json",
            {},
        )
        workspace_frame = _read_json_if_exists(
            state_dir / "consciousness" / "workspace_frame.json",
            {},
        )
        _attach_live_language_turn_refs(
            external_turn,
            live_language_turn=live_language_turn,
        )
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
            expression_plan=live_language_turn.expression_plan,
            life_context_frame=life_context_frame,
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
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
            responsibility_loop_state=responsibility_loop_state,
            world_contact_summary=world_contact_summary,
            pain_regret_repair_report=pain_regret_repair_report,
            self_model_state=self_model_state,
            terminal_life_loop_state=terminal_life_loop_state,
        )
        model_expression = compose_model_expression(
            run_id=run_id,
            generated_at=now_iso(),
            external_utterance=external_utterance,
            deterministic_response=life_response,
            language_dir=language_dir,
            reports_dir=reports_dir,
            relationship_graph=relationship_graph,
            relationship_timeline=relationship_timeline,
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
            language_percept=live_language_turn.language_percept,
            semantic_map=live_language_turn.semantic_map,
            inner_speech=live_language_turn.inner_speech,
            expression_monitor=live_language_turn.expression_monitor,
            expression_plan=live_language_turn.expression_plan,
            life_context_frame=life_context_frame,
            replay_cue_bundle=replay_cue_bundle,
            offline_consolidation_frame=offline_consolidation_frame,
            growth_patch_candidate_queue=growth_patch_candidate_queue,
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
            responsibility_loop_state=responsibility_loop_state,
            world_contact_summary=world_contact_summary,
            pain_regret_repair_report=pain_regret_repair_report,
            self_model_state=self_model_state,
            terminal_life_loop_state=terminal_life_loop_state,
            brain_graph=brain_graph,
            network_state=network_state,
            prediction_workspace=prediction_workspace,
            workspace_frame=workspace_frame,
            write_json=write_json,
        )
        life_response = model_expression.response_text
        life_turn = build_life_turn_event_fn(
            turn_id=life_turn_id,
            generated_at=now_iso(),
            utterance=life_response,
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
            terminal_life_loop_state=terminal_life_loop_state,
            signal_media_runtime=signal_media_runtime,
            belief_state=belief_state,
            prediction_error_field=prediction_error_field,
            active_sampling_plan=active_sampling_plan,
            memory_write_gate=memory_write_gate,
            state_merge_guard=state_merge_guard,
            signal_media_runtime_ref=signal_media_runtime_ref,
            belief_state_ref=belief_state_ref,
            prediction_error_field_ref=prediction_error_field_ref,
            active_sampling_plan_ref=active_sampling_plan_ref,
            memory_write_gate_ref=memory_write_gate_ref,
            state_merge_guard_ref=state_merge_guard_ref,
            responsibility_loop_state_ref=responsibility_loop_state_ref,
            world_contact_summary_ref=world_contact_summary_ref,
            pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        )
        _attach_live_language_turn_refs(
            life_turn,
            live_language_turn=live_language_turn,
        )
        _attach_model_expression_refs(
            life_turn,
            model_expression=model_expression,
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
            self_model_state=self_model_state,
            source_doc_refs=source_doc_refs,
            readme_block_refs=readme_block_refs,
            runtime_carrier_refs=runtime_carrier_refs,
            replay_cue_bundle_ref=replay_cue_bundle_ref,
            signal_media_runtime=signal_media_runtime,
            belief_state=belief_state,
            prediction_error_field=prediction_error_field,
            active_sampling_plan=active_sampling_plan,
            memory_write_gate=memory_write_gate,
            state_merge_guard=state_merge_guard,
            signal_media_runtime_ref=signal_media_runtime_ref,
            belief_state_ref=belief_state_ref,
            prediction_error_field_ref=prediction_error_field_ref,
            active_sampling_plan_ref=active_sampling_plan_ref,
            memory_write_gate_ref=memory_write_gate_ref,
            state_merge_guard_ref=state_merge_guard_ref,
            responsibility_loop_state_ref=responsibility_loop_state_ref,
            world_contact_summary_ref=world_contact_summary_ref,
            pain_regret_repair_report_ref=pain_regret_repair_report_ref,
            language_percept_ref=live_language_turn.language_percept_ref,
            semantic_map_ref=live_language_turn.semantic_map_ref,
            inner_speech_ref=live_language_turn.inner_speech_ref,
            expression_monitor_ref=live_language_turn.expression_monitor_ref,
            expression_plan_ref=live_language_turn.expression_plan_ref,
            live_semantic_focus=live_language_turn.semantic_map.get("semantic_focus"),
            live_ambiguity_flags=list(
                live_language_turn.language_percept.get("ambiguity_flags", [])
            ),
            live_repair_trigger_candidates=list(
                live_language_turn.language_percept.get("repair_trigger_candidates", [])
            ),
            prediction_workspace=prediction_workspace,
            workspace_frame=workspace_frame,
            brain_graph=brain_graph,
            network_state=network_state,
            now_iso=now_iso,
            write_json=write_json,
            append_jsonl=append_jsonl,
        )
        write_live_turn_waiting_governance_handoff_fn(
            run_id=run_id,
            generated_at=now_iso(),
            terminal_dir=terminal_dir,
            safe_terminal_loop=turn_writeback.safe_terminal_loop,
            terminal_life_loop_state=turn_writeback.terminal_life_loop_state,
            relationship_timeline=_read_json_if_exists(
                relationship_dir / "relationship_timeline.json",
                relationship_timeline,
            ),
            commitment_expression_plan=_read_json_if_exists(
                language_dir / "commitment_expression_plan.json",
                commitment_expression_plan,
            ),
            apology_repair_language_trace=_read_json_if_exists(
                language_dir / "apology_repair_language_trace.json",
                apology_repair_language_trace,
            ),
            external_turn_ref=turn_writeback.external_turn_ref,
            life_turn_ref=turn_writeback.life_turn_ref,
            responsibility_loop_state_ref=responsibility_loop_state_ref,
            world_contact_summary_ref=world_contact_summary_ref,
            pain_regret_repair_report_ref=pain_regret_repair_report_ref,
            write_json=write_json,
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


def _read_json_if_exists(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return fallback


def _attach_live_language_turn_refs(
    event: dict[str, Any],
    *,
    live_language_turn: LiveLanguageTurnState,
) -> None:
    event["language_percept_ref"] = live_language_turn.language_percept_ref
    event["semantic_map_ref"] = live_language_turn.semantic_map_ref
    event["inner_speech_ref"] = live_language_turn.inner_speech_ref
    event["expression_monitor_ref"] = live_language_turn.expression_monitor_ref
    event["expression_plan_ref"] = live_language_turn.expression_plan_ref
    event["live_semantic_focus"] = live_language_turn.semantic_map.get("semantic_focus")
    event["live_ambiguity_flags"] = list(
        live_language_turn.language_percept.get("ambiguity_flags", [])
    )
    event["live_repair_trigger_candidates"] = list(
        live_language_turn.language_percept.get("repair_trigger_candidates", [])
    )


def _attach_model_expression_refs(
    event: dict[str, Any],
    *,
    model_expression: ModelExpressionResult,
) -> None:
    event["model_expression_state_ref"] = model_expression.state_ref
    event["model_expression_report_ref"] = model_expression.report_ref
    event["model_expression_status"] = model_expression.state.get(
        "model_expression_status"
    )
    event["model_expression_applied"] = model_expression.applied
    if model_expression.state.get("post_expression_gate_status"):
        event["post_expression_gate_status"] = model_expression.state[
            "post_expression_gate_status"
        ]
    if model_expression.state.get("post_expression_gate_fallback_reason"):
        event["post_expression_gate_fallback_reason"] = model_expression.state[
            "post_expression_gate_fallback_reason"
        ]
    if model_expression.state.get("fallback_reason"):
        event["model_expression_fallback_reason"] = model_expression.state[
            "fallback_reason"
        ]
