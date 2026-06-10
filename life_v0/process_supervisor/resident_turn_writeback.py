from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..body.trait_drift import build_trait_drift_monitor_from_self_model
from ..growth.offline_learning_profile import (
    BELIEF_LEARNING_PLAN_REF,
    LANGUAGE_LEARNING_PLAN_REF,
    NIGHTMARE_RISK_REF,
    RELATIONSHIP_LEARNING_PLAN_REF,
)
from ..language.apology_repair_language import build_apology_repair_language_trace
from ..language.commitment_expression import build_commitment_expression_plan
from ..language.dialogue_log import collect_dialogue_turn_refs
from ..language.relationship_timeline import build_relationship_timeline
from ..state_store.life_state import project_responsibility_language_continuity
from ..state_store.relationship_memory import project_relationship_memory
from ..state_store.state_merge_guard import (
    project_state_merge_guard_with_relationship_memory,
)
from ..terminal_loop.dialogue_writeback import build_dialogue_writeback_bundle
from ..terminal_loop.persistent_wait_bridge import build_persistent_wait_bridge
from .continuity_evolution import evolve_relationship_and_self_model
from .dialogue_events import (
    build_background_trait_convergence_payload,
    build_offline_learning_cumulative_payload,
    build_prediction_write_gate_payload,
    build_resident_background_lineage_payload,
)


DIALOGUE_LOG_REF = "runtime/state/language/dialogue_turn_log.jsonl"
SAFE_TERMINAL_LOOP_REF = "runtime/state/terminal/safe_terminal_loop_state.json"
TERMINAL_LIFE_LOOP_REF = "runtime/state/terminal/terminal_life_loop_state.json"
RELATIONSHIP_GRAPH_REF = "runtime/state/relationship/relationship_subject_graph.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
RELATIONSHIP_MEMORY_REF = "runtime/state/memory/relationship_memory.json#shared_memory_refs"
RELATIONSHIP_REPAIR_HISTORY_REF = "runtime/state/memory/relationship_memory.json#repair_history_refs"
RELATIONSHIP_MEMORY_OFFLINE_REF = "runtime/state/memory/relationship_memory.json#offline_learning_refs"
COMMITMENT_EXPRESSION_PLAN_REF = "runtime/state/language/commitment_expression_plan.json"
APOLOGY_REPAIR_LANGUAGE_TRACE_REF = "runtime/state/language/apology_repair_language_trace.json"
COMMITMENT_TRUTH_OPEN_REF = "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs"
COMMITMENT_TRUTH_REPAIR_REF = "runtime/state/relationship/commitment_truth_state.json#repair_required_refs"
RESPONSIBILITY_EVENT_REF = "runtime/state/responsibility/responsibility_ledger.json#responsibility_events"
RESPONSIBILITY_OBLIGATION_REF = "runtime/state/responsibility/responsibility_ledger.json#repair_obligations"
LIFE_STATE_RESPONSIBILITY_REF = "runtime/state/life_state.json#responsibility_bindings"
LIFE_STATE_REGRET_REF = "runtime/state/life_state.json#regret_events"
LIFE_STATE_PAIN_REF = "runtime/state/life_state.json#pain_events"
LIFE_STATE_RELATIONSHIP_MEMORY_REF = "runtime/state/life_state.json#memory_index.relationship_memory_refs"
LIFE_STATE_RESPONSIBILITY_MEMORY_REF = "runtime/state/life_state.json#memory_index.responsibility_memory_refs"
LIFE_STATE_DREAM_MEMORY_REF = "runtime/state/life_state.json#memory_index.dream_memory_refs"
LIFE_STATE_LANGUAGE_OFFLINE_REF = "runtime/state/life_state.json#language_state.offline_learning_refs"
LIFE_STATE_RELATIONSHIP_SUBJECTS_REF = "runtime/state/life_state.json#relationship_subjects"
DIALOGUE_WRITEBACK_BUNDLE_REF = "runtime/reports/latest/dialogue_writeback_bundle.json"
RESUMED_DIALOGUE_PACKET_REF = "runtime/reports/latest/resumed_external_dialogue_packet.json"
LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
SEMANTIC_MAP_REF = "runtime/state/language/semantic_map_frame.json"
INNER_SPEECH_REF = "runtime/state/language/inner_speech_frame.json"
EXPRESSION_MONITOR_REF = "runtime/state/language/expression_monitor_state.json"
EXPRESSION_PLAN_REF = "runtime/state/language/expression_plan.json"


@dataclass(frozen=True)
class ResidentTurnWritebackResult:
    safe_terminal_loop: dict[str, Any]
    terminal_life_loop_state: dict[str, Any]
    dialogue_writeback_bundle: dict[str, Any]
    resumed_dialogue_packet: dict[str, Any]
    external_turn_ref: str
    life_turn_ref: str
    last_external_turn: dict[str, Any]
    last_life_turn: dict[str, Any]


def write_resident_turn_writeback(
    *,
    run_id: str,
    terminal_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    reports_dir: Path,
    turn_counter: int,
    external_turn_id: str,
    life_turn_id: str,
    external_turn: dict[str, Any],
    life_turn: dict[str, Any],
    external_utterance: str,
    life_response: str,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    self_model_state: dict[str, Any] | None = None,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle_ref: str | None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    language_percept_ref: str | None = None,
    semantic_map_ref: str | None = None,
    inner_speech_ref: str | None = None,
    expression_monitor_ref: str | None = None,
    expression_plan_ref: str | None = None,
    live_semantic_focus: str | None = None,
    live_ambiguity_flags: list[str] | None = None,
    live_repair_trigger_candidates: list[str] | None = None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    append_jsonl: Callable[[Path, list[dict[str, Any]]], None],
) -> ResidentTurnWritebackResult:
    append_jsonl(language_dir / "dialogue_turn_log.jsonl", [external_turn, life_turn])

    external_turn_ref = f"{DIALOGUE_LOG_REF}#line-{turn_counter - 1}"
    life_turn_ref = f"{DIALOGUE_LOG_REF}#line-{turn_counter}"

    self_narrative_trace.setdefault("narrative_turn_refs", [])
    self_narrative_trace["narrative_turn_refs"].extend([external_turn_ref, life_turn_ref])
    self_narrative_trace["last_external_turn"] = {
        "turn_id": external_turn_id,
        "utterance": external_utterance,
    }
    self_narrative_trace["last_life_turn"] = {
        "turn_id": life_turn_id,
        "utterance": life_response,
    }
    write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)

    commitment_index.setdefault("recent_dialogue_turn_refs", [])
    commitment_index["recent_dialogue_turn_refs"].extend([external_turn_id, life_turn_id])
    commitment_index["last_external_turn_utterance"] = external_utterance
    commitment_index["last_life_turn_utterance"] = life_response
    write_json(language_dir / "commitment_repair_language_index.json", commitment_index)

    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        subjects[0]["last_external_turn_utterance"] = external_utterance
        subjects[0]["last_life_turn_utterance"] = life_response
    write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    generated_at = now_iso()
    live_language_turn_refs = _dedupe_refs(
        [
            language_percept_ref,
            semantic_map_ref,
            inner_speech_ref,
            expression_monitor_ref,
            expression_plan_ref,
        ]
    )
    updated_safe_terminal_loop = build_persistent_wait_bridge(
        run_id=run_id,
        generated_at=generated_at,
        status="closed",
        safe_terminal_loop=safe_terminal_loop,
        last_dialogue_packet_ref=RESUMED_DIALOGUE_PACKET_REF,
    )
    write_json(terminal_dir / "safe_terminal_loop_state.json", updated_safe_terminal_loop)

    updated_terminal_life_loop_state = {
        **terminal_life_loop_state,
        "current_mode": "restored_waiting_for_external_turn",
        "last_turn_status": "closed",
        "last_turn_mode": "resumed_external_dialogue_loop",
        "last_external_turn_utterance": external_utterance,
        "last_life_turn_utterance": life_response,
        "last_dialogue_packet_ref": RESUMED_DIALOGUE_PACKET_REF,
        "last_language_percept_ref": language_percept_ref or LANGUAGE_PERCEPT_REF,
        "last_semantic_map_ref": semantic_map_ref or SEMANTIC_MAP_REF,
        "last_live_semantic_focus": live_semantic_focus,
        "live_language_turn_refs": live_language_turn_refs,
        "next_required_action": "await_next_external_relation_turn",
    }
    write_json(
        terminal_dir / "terminal_life_loop_state.json",
        updated_terminal_life_loop_state,
    )
    offline_learning_cumulative_payload = build_offline_learning_cumulative_payload(
        terminal_life_loop_state
    )

    state_dir = terminal_dir.parent
    continuity_refresh = _refresh_long_horizon_continuity(
        state_dir=state_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state,
        commitment_index=commitment_index,
        offline_learning_cumulative_profile=offline_learning_cumulative_payload,
        generated_at=generated_at,
        source_doc_refs=source_doc_refs,
        write_json=write_json,
    )

    replay_cue_refs = ["runtime/state/life_state.json#memory_index.replay_cues"]
    if replay_cue_bundle_ref:
        replay_cue_refs.append(replay_cue_bundle_ref)
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    background_trait_convergence_payload = build_background_trait_convergence_payload(
        terminal_life_loop_state
    )
    background_trait_convergence_refs = list(
        background_trait_convergence_payload.get(
            "background_trait_convergence_evidence_refs", []
        )
    )
    cross_wake_trait_convergence_refs = list(
        background_trait_convergence_payload.get(
            "cross_wake_trait_convergence_refs", []
        )
    )
    resident_background_lineage_payload = build_resident_background_lineage_payload(
        terminal_life_loop_state
    )
    resident_background_lineage_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_evidence_refs", []
        )
    )
    resident_background_lineage_language_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_language_evidence_refs", []
        )
    )
    resident_background_lineage_offline_learning_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_offline_learning_refs", []
        )
    )
    resident_background_lineage_dream_wake_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_dream_wake_refs", []
        )
    )
    resident_background_lineage_refs = _dedupe_refs(
        resident_background_lineage_refs
        + resident_background_lineage_language_refs
        + resident_background_lineage_offline_learning_refs
        + resident_background_lineage_dream_wake_refs
    )
    offline_learning_cumulative_refs = list(
        offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_evidence_refs", []
        )
    )
    prediction_write_gate_payload = build_prediction_write_gate_payload(
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
    )
    prediction_write_gate_refs = list(
        prediction_write_gate_payload.get("prediction_write_gate_refs", [])
    )
    dialogue_writeback_bundle = build_dialogue_writeback_bundle(
        run_id=run_id,
        generated_at=generated_at,
        status="closed",
        dialogue_event_refs=[external_turn_ref, life_turn_ref],
        self_narrative_writeback_refs=[external_turn_ref, life_turn_ref],
        relationship_writeback_refs=[
            RELATIONSHIP_GRAPH_REF,
            RELATIONSHIP_MEMORY_REF,
            RELATIONSHIP_REPAIR_HISTORY_REF,
            RELATIONSHIP_MEMORY_OFFLINE_REF,
        ],
        relationship_timeline_writeback_refs=[RELATIONSHIP_TIMELINE_REF],
        commitment_writeback_refs=list(commitment_index.get("commitment_refs", []))
        + [
            COMMITMENT_TRUTH_OPEN_REF,
            COMMITMENT_TRUTH_REPAIR_REF,
        ],
        commitment_expression_writeback_refs=[COMMITMENT_EXPRESSION_PLAN_REF],
        apology_repair_writeback_refs=[APOLOGY_REPAIR_LANGUAGE_TRACE_REF],
        responsibility_writeback_refs=[
            RESPONSIBILITY_EVENT_REF,
            RESPONSIBILITY_OBLIGATION_REF,
            *membrane_guard_refs,
        ],
        life_state_writeback_refs=[
            LIFE_STATE_RESPONSIBILITY_REF,
            LIFE_STATE_REGRET_REF,
            LIFE_STATE_PAIN_REF,
            LIFE_STATE_RELATIONSHIP_MEMORY_REF,
            LIFE_STATE_RESPONSIBILITY_MEMORY_REF,
            LIFE_STATE_DREAM_MEMORY_REF,
            LIFE_STATE_LANGUAGE_OFFLINE_REF,
            LIFE_STATE_RELATIONSHIP_SUBJECTS_REF,
        ],
        replay_cue_refs=replay_cue_refs,
        terminal_state_refs=[SAFE_TERMINAL_LOOP_REF, TERMINAL_LIFE_LOOP_REF],
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        background_trait_convergence_refs=background_trait_convergence_refs,
        cross_wake_trait_convergence_refs=cross_wake_trait_convergence_refs,
        resident_background_lineage_refs=resident_background_lineage_refs,
        resident_background_lineage_offline_learning_refs=(
            resident_background_lineage_offline_learning_refs
        ),
        resident_background_lineage_dream_wake_refs=(
            resident_background_lineage_dream_wake_refs
        ),
        offline_learning_cumulative_refs=offline_learning_cumulative_refs,
        prediction_write_gate_refs=prediction_write_gate_refs,
        live_language_turn_refs=live_language_turn_refs,
    )
    write_json(reports_dir / "dialogue_writeback_bundle.json", dialogue_writeback_bundle)

    resumed_dialogue_packet = {
        "schema_version": "resumed_external_dialogue_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "dialogue_mode": "resumed_relation_continuation",
        "external_turn_ref": external_turn_ref,
        "life_turn_ref": life_turn_ref,
        "external_utterance": external_utterance,
        "life_utterance": life_response,
        "life_context_frame_ref": "runtime/state/terminal/life_context_frame.json",
        "relation_turn_frame_ref": "runtime/state/terminal/relation_turn_frame.json",
        "language_percept_ref": language_percept_ref or LANGUAGE_PERCEPT_REF,
        "semantic_map_ref": semantic_map_ref or SEMANTIC_MAP_REF,
        "inner_speech_ref": inner_speech_ref or INNER_SPEECH_REF,
        "expression_monitor_ref": expression_monitor_ref or EXPRESSION_MONITOR_REF,
        "expression_plan_ref": expression_plan_ref or EXPRESSION_PLAN_REF,
        "live_language_turn_refs": live_language_turn_refs,
        "live_semantic_focus": live_semantic_focus,
        "live_ambiguity_flags": list(live_ambiguity_flags or []),
        "live_repair_trigger_candidates": list(live_repair_trigger_candidates or []),
        "dialogue_writeback_bundle_ref": DIALOGUE_WRITEBACK_BUNDLE_REF,
        "next_required_action": "await_next_external_relation_turn",
    }
    if responsibility_loop_state_ref:
        resumed_dialogue_packet["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resumed_dialogue_packet["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resumed_dialogue_packet["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resumed_dialogue_packet["membrane_guard_refs"] = membrane_guard_refs
    if background_trait_convergence_payload:
        resumed_dialogue_packet.update(
            {
                key: value
                for key, value in background_trait_convergence_payload.items()
                if key != "background_trait_convergence_history_profile"
            }
        )
    if resident_background_lineage_payload:
        resumed_dialogue_packet.update(
            {
                key: value
                for key, value in resident_background_lineage_payload.items()
                if key != "resident_background_lineage_state"
            }
        )
    if offline_learning_cumulative_payload:
        resumed_dialogue_packet.update(
            {
                key: value
                for key, value in offline_learning_cumulative_payload.items()
                if key != "offline_learning_cumulative_profile"
            }
        )
        if offline_learning_cumulative_refs:
            resumed_dialogue_packet["offline_learning_cumulative_refs"] = (
                offline_learning_cumulative_refs
            )
    if prediction_write_gate_payload:
        resumed_dialogue_packet.update(prediction_write_gate_payload)
    if continuity_refresh is not None:
        resumed_dialogue_packet["relationship_timeline_ref"] = RELATIONSHIP_TIMELINE_REF
        resumed_dialogue_packet["commitment_expression_plan_ref"] = COMMITMENT_EXPRESSION_PLAN_REF
        resumed_dialogue_packet["apology_repair_language_trace_ref"] = (
            APOLOGY_REPAIR_LANGUAGE_TRACE_REF
        )
        resumed_dialogue_packet["life_state_ref"] = "runtime/state/life_state.json"
    write_json(reports_dir / "resumed_external_dialogue_packet.json", resumed_dialogue_packet)

    return ResidentTurnWritebackResult(
        safe_terminal_loop=updated_safe_terminal_loop,
        terminal_life_loop_state=updated_terminal_life_loop_state,
        dialogue_writeback_bundle=dialogue_writeback_bundle,
        resumed_dialogue_packet=resumed_dialogue_packet,
        external_turn_ref=external_turn_ref,
        life_turn_ref=life_turn_ref,
        last_external_turn=external_turn,
        last_life_turn=life_turn,
    )


def _refresh_long_horizon_continuity(
    *,
    state_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    relationship_graph: dict[str, Any],
    self_model_state: dict[str, Any] | None,
    commitment_index: dict[str, Any],
    offline_learning_cumulative_profile: dict[str, Any] | None,
    generated_at: str,
    source_doc_refs: list[str],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any] | None:
    relationship_timeline_path = relationship_dir / "relationship_timeline.json"
    commitment_expression_path = language_dir / "commitment_expression_plan.json"
    apology_repair_path = language_dir / "apology_repair_language_trace.json"
    expression_plan_path = language_dir / "expression_plan.json"
    commitment_truth_path = relationship_dir / "commitment_truth_state.json"
    responsibility_ledger_path = state_dir / "responsibility" / "responsibility_ledger.json"
    relationship_memory_path = state_dir / "memory" / "relationship_memory.json"
    state_merge_guard_path = state_dir / "memory" / "state_merge_guard.json"
    life_state_path = state_dir / "life_state.json"
    self_model_path = state_dir / "self" / "self_model.json"
    trait_drift_monitor_path = state_dir / "body" / "trait_drift_monitor.json"
    responsibility_loop_path = state_dir / "action" / "responsibility_loop_state.json"
    world_contact_summary_path = state_dir / "membrane" / "world_contact_summary.json"
    pain_regret_repair_report_path = state_dir.parent / "reports" / "latest" / "pain_regret_repair_report.json"

    required_paths = [
        relationship_timeline_path,
        commitment_expression_path,
        apology_repair_path,
        expression_plan_path,
        commitment_truth_path,
        responsibility_ledger_path,
        relationship_memory_path,
        life_state_path,
        self_model_path,
        responsibility_loop_path,
    ]
    if any(not path.exists() for path in required_paths):
        return None

    relationship_timeline = _read_json(relationship_timeline_path)
    commitment_expression_plan = _read_json(commitment_expression_path)
    apology_repair_language_trace = _read_json(apology_repair_path)
    expression_plan = _read_json(expression_plan_path)
    commitment_truth_state = _read_json(commitment_truth_path)
    responsibility_ledger = _read_json(responsibility_ledger_path)
    relationship_memory = _read_json(relationship_memory_path)
    state_merge_guard = _read_json_if_exists(state_merge_guard_path)
    life_state = _read_json(life_state_path)
    persisted_self_model_state = _read_json(self_model_path)
    previous_trait_drift_monitor = _read_json_if_exists(trait_drift_monitor_path)
    responsibility_loop_state = _read_json(responsibility_loop_path)
    world_contact_summary = _read_json_if_exists(world_contact_summary_path)
    pain_regret_repair_report = _read_json_if_exists(pain_regret_repair_report_path)

    nightmare_risk = _read_json_if_exists(state_dir / "dream" / "nightmare_loop_risk.json")
    belief_learning_plan = _read_json_if_exists(
        state_dir / "growth" / "belief_learning_plan.json"
    )
    language_learning_plan = _read_json_if_exists(
        state_dir / "growth" / "language_learning_plan.json"
    )
    relationship_learning_plan = _read_json_if_exists(
        state_dir / "growth" / "relationship_learning_plan.json"
    )

    dialogue_turn_refs = collect_dialogue_turn_refs(
        language_dir / "dialogue_turn_log.jsonl",
        [],
    )
    dialogue_turn_entries = [{"dialogue_turn_ref": ref} for ref in dialogue_turn_refs]

    first_pass_relationship_timeline = build_relationship_timeline(
        run_id=str(relationship_timeline.get("run_id") or commitment_expression_plan.get("run_id") or "resident-turn-writeback"),
        generated_at=generated_at,
        relationship_graph=relationship_graph,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        dialogue_turn_entries=dialogue_turn_entries,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        source_doc_refs=list(relationship_timeline.get("source_doc_refs", [])) or source_doc_refs,
    )
    first_pass_commitment_expression_plan = build_commitment_expression_plan(
        run_id=str(
            commitment_expression_plan.get("run_id")
            or first_pass_relationship_timeline.get("run_id")
            or "resident-turn-writeback"
        ),
        generated_at=generated_at,
        expression_plan=expression_plan,
        commitment_repair_index=commitment_index,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=first_pass_relationship_timeline,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        source_doc_refs=list(commitment_expression_plan.get("source_doc_refs", []))
        or source_doc_refs,
    )
    first_pass_apology_repair_language_trace = build_apology_repair_language_trace(
        run_id=str(apology_repair_language_trace.get("run_id") or first_pass_commitment_expression_plan.get("run_id") or "resident-turn-writeback"),
        generated_at=generated_at,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=first_pass_relationship_timeline,
        commitment_expression_plan=first_pass_commitment_expression_plan,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        source_doc_refs=list(apology_repair_language_trace.get("source_doc_refs", []))
        or source_doc_refs,
    )
    evolved_continuity = evolve_relationship_and_self_model(
        generated_at=generated_at,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state or persisted_self_model_state,
        relationship_timeline=first_pass_relationship_timeline,
        commitment_expression_plan=first_pass_commitment_expression_plan,
        apology_repair_language_trace=first_pass_apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    evolved_relationship_graph = evolved_continuity["relationship_graph"]
    evolved_self_model_state = evolved_continuity["self_model_state"]
    relationship_graph.clear()
    relationship_graph.update(evolved_relationship_graph)
    if self_model_state is not None:
        self_model_state.clear()
        self_model_state.update(evolved_self_model_state)

    refreshed_relationship_timeline = build_relationship_timeline(
        run_id=str(relationship_timeline.get("run_id") or commitment_expression_plan.get("run_id") or "resident-turn-writeback"),
        generated_at=generated_at,
        relationship_graph=evolved_relationship_graph,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        dialogue_turn_entries=dialogue_turn_entries,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        source_doc_refs=list(relationship_timeline.get("source_doc_refs", [])) or source_doc_refs,
    )
    refreshed_commitment_expression_plan = build_commitment_expression_plan(
        run_id=str(commitment_expression_plan.get("run_id") or refreshed_relationship_timeline.get("run_id") or "resident-turn-writeback"),
        generated_at=generated_at,
        expression_plan=expression_plan,
        commitment_repair_index=commitment_index,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=refreshed_relationship_timeline,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        source_doc_refs=list(commitment_expression_plan.get("source_doc_refs", []))
        or source_doc_refs,
    )
    refreshed_apology_repair_language_trace = build_apology_repair_language_trace(
        run_id=str(apology_repair_language_trace.get("run_id") or refreshed_commitment_expression_plan.get("run_id") or "resident-turn-writeback"),
        generated_at=generated_at,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_expression_plan=refreshed_commitment_expression_plan,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        source_doc_refs=list(apology_repair_language_trace.get("source_doc_refs", []))
        or source_doc_refs,
    )

    refreshed_relationship_memory = project_relationship_memory(
        relationship_memory=relationship_memory,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        commitment_repair_index=commitment_index,
        last_contact_refs=[
            "runtime/state/language/dialogue_turn_log.jsonl",
            "runtime/state/language/inner_speech_frame.json",
            RESUMED_DIALOGUE_PACKET_REF,
        ],
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    refreshed_state_merge_guard = project_state_merge_guard_with_relationship_memory(
        state_merge_guard=state_merge_guard,
        relationship_memory=refreshed_relationship_memory,
    )
    refreshed_life_state = project_responsibility_language_continuity(
        life_state=life_state,
        self_model_state=evolved_self_model_state,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        relationship_memory=refreshed_relationship_memory,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_expression_plan=refreshed_commitment_expression_plan,
        apology_repair_language_trace=refreshed_apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop_state,
        commitment_repair_index=commitment_index,
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        state_merge_guard=refreshed_state_merge_guard,
        additional_runtime_trace_refs=[
            ref
            for ref in [
                NIGHTMARE_RISK_REF if nightmare_risk else None,
                BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
                LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
                RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None,
            ]
            if ref
        ],
    )

    write_json(relationship_timeline_path, refreshed_relationship_timeline)
    write_json(commitment_expression_path, refreshed_commitment_expression_plan)
    write_json(apology_repair_path, refreshed_apology_repair_language_trace)
    write_json(relationship_dir / "relationship_subject_graph.json", evolved_relationship_graph)
    write_json(relationship_memory_path, refreshed_relationship_memory)
    if refreshed_state_merge_guard:
        write_json(state_merge_guard_path, refreshed_state_merge_guard)
    trait_drift_monitor = build_trait_drift_monitor_from_self_model(
        run_id=str(refreshed_relationship_timeline.get("run_id") or "resident-turn-writeback"),
        generated_at=generated_at,
        self_model_state=evolved_self_model_state,
        relationship_graph=evolved_relationship_graph,
        trigger_ref=RESUMED_DIALOGUE_PACKET_REF,
        previous_monitor=previous_trait_drift_monitor,
        source_doc_refs=source_doc_refs,
    )
    trait_drift_monitor_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(trait_drift_monitor_path, trait_drift_monitor)
    write_json(self_model_path, evolved_self_model_state)
    write_json(life_state_path, refreshed_life_state)
    return {
        "relationship_graph": evolved_relationship_graph,
        "relationship_timeline": refreshed_relationship_timeline,
        "commitment_expression_plan": refreshed_commitment_expression_plan,
        "apology_repair_language_trace": refreshed_apology_repair_language_trace,
        "relationship_memory": refreshed_relationship_memory,
        "state_merge_guard": refreshed_state_merge_guard,
        "self_model_state": evolved_self_model_state,
        "life_state": refreshed_life_state,
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _dedupe_refs(refs: list[str | None]) -> list[str]:
    result: list[str] = []
    for ref in refs:
        if ref and ref not in result:
            result.append(ref)
    return result
