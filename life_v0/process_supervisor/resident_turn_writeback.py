from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..body.trait_drift import build_trait_drift_monitor_from_self_model
from ..life_targets.consciousness_probes import (
    project_consciousness_probe_bundle_from_live_turn,
)
from ..life_targets.queue_e_world_contact_handoff import (
    HANDOFF_PROFILE_REF,
    project_queue_e_world_contact_repair_hold_handoff_from_live_turn,
)
from ..membrane.responsibility_loop import (
    project_responsibility_loop_with_consciousness_context,
)
from ..growth.offline_learning_profile import (
    BELIEF_LEARNING_PLAN_REF,
    LANGUAGE_LEARNING_PLAN_REF,
    NIGHTMARE_RISK_REF,
    RELATIONSHIP_LEARNING_PLAN_REF,
)
from ..neural_core.brain_graph import project_brain_graph_from_live_turn
from ..neural_core.multiscale_region_graph import (
    project_multiscale_region_graph_from_live_turn,
)
from ..neural_core.broadcast import project_broadcast_frame_from_live_turn
from ..neural_core.metacognition import project_metacognition_state_from_live_turn
from ..neural_core.network_state import project_network_state_from_live_turn
from ..neural_core.workspace import project_workspace_frame_from_live_turn
from ..language.apology_repair_language import build_apology_repair_language_trace
from ..language.commitment_expression import build_commitment_expression_plan
from ..language.expression_monitor import (
    project_expression_plan_with_queue_e_repair_modulation,
)
from ..language.ref_consistency import project_language_relationship_ref_consistency_profile
from ..language.semantic_map import project_semantic_map_from_live_evidence
from ..language.shared_terms import (
    SHARED_TERM_REGISTRY_REF,
    project_shared_term_registry_from_live_evidence,
)
from ..language.dialogue_log import collect_dialogue_turn_refs
from ..language.relationship_timeline import build_relationship_timeline
from ..state_store.autobiographical_stack import (
    project_autobiographical_stack_from_live_turn,
)
from ..state_store.engram_index import project_engram_index_from_live_turn
from ..state_store.life_state import project_responsibility_language_continuity
from ..state_store.memory_retrieval import (
    MEMORY_RETRIEVAL_FRAME_REF,
    memory_retrieval_context_summary,
    project_memory_retrieval_from_live_turn,
)
from ..state_store.relationship_memory import project_relationship_memory
from ..state_store.memory_write_gate import (
    project_memory_write_gate_with_consciousness_context,
    project_memory_write_gate_with_signal_body,
)
from ..state_store.state_merge_guard import (
    project_state_merge_guard_with_relationship_memory,
)
from ..terminal_turn.context_accumulation import (
    CONTEXT_ACCUMULATION_WINDOW_REF,
    project_context_accumulation_window_from_live_turn,
)
from ..terminal_turn.turn_transition import (
    TURN_TRANSITION_TRACE_REF,
    project_turn_transition_trace_from_live_turn,
)
from ..terminal_loop.dialogue_writeback import build_dialogue_writeback_bundle
from ..terminal_loop.persistent_wait_bridge import build_persistent_wait_bridge
from .continuity_evolution import evolve_relationship_and_self_model
from .dialogue_events import (
    attach_prediction_write_gate_lineage_fallback,
    build_background_trait_convergence_payload,
    build_life_constraint_payload,
    build_offline_learning_cumulative_payload,
    build_prediction_write_gate_payload,
    build_queue_e_birth_repair_payload,
    build_queue_e_world_contact_handoff_payload,
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
ENGRAM_INDEX_REF = "runtime/state/memory/engram_index.json"
ENGRAM_INDEX_LIVE_DIALOGUE_REF = "runtime/state/memory/engram_index.json#live_dialogue_turn_refs"
ENGRAM_INDEX_LIVE_LANGUAGE_REF = "runtime/state/memory/engram_index.json#live_language_turn_refs"
ENGRAM_INDEX_RELATIONSHIP_REF = "runtime/state/memory/engram_index.json#relationship_memory_refs"
ENGRAM_INDEX_OFFLINE_REF = "runtime/state/memory/engram_index.json#offline_learning_refs"
AUTOBIOGRAPHICAL_STACK_REF = "runtime/state/self/autobiographical_stack.json"
AUTOBIOGRAPHICAL_STACK_TURN_REF = "runtime/state/self/autobiographical_stack.json#turn_refs"
AUTOBIOGRAPHICAL_STACK_LIVE_LANGUAGE_REF = "runtime/state/self/autobiographical_stack.json#live_language_turn_refs"
AUTOBIOGRAPHICAL_STACK_RELATIONSHIP_REF = "runtime/state/self/autobiographical_stack.json#relationship_turn_refs"
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
LIFE_STATE_MEMORY_RETRIEVAL_REF = "runtime/state/life_state.json#memory_index.memory_retrieval_refs"
DIALOGUE_WRITEBACK_BUNDLE_REF = "runtime/reports/latest/dialogue_writeback_bundle.json"
RESUMED_DIALOGUE_PACKET_REF = "runtime/reports/latest/resumed_external_dialogue_packet.json"
LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
SEMANTIC_MAP_REF = "runtime/state/language/semantic_map_frame.json"
INNER_SPEECH_REF = "runtime/state/language/inner_speech_frame.json"
EXPRESSION_MONITOR_REF = "runtime/state/language/expression_monitor_state.json"
EXPRESSION_PLAN_REF = "runtime/state/language/expression_plan.json"
BRAIN_GRAPH_REF = "runtime/state/neural_life_core/brain_graph.json"
MULTISCALE_REGION_GRAPH_REF = (
    "runtime/state/neural_life_core/multiscale_region_graph.json"
)
NETWORK_STATE_REF = "runtime/state/neural_life_core/network_state.json"
PREDICTION_WORKSPACE_REF = "runtime/state/prediction/prediction_workspace_frame.json"
WORKSPACE_FRAME_REF = "runtime/state/consciousness/workspace_frame.json"
BROADCAST_FRAME_REF = "runtime/state/consciousness/broadcast_frame.json"
METACOGNITION_STATE_REF = "runtime/state/consciousness/metacognition_state.json"
CONSCIOUSNESS_PROBE_REF = "runtime/state/consciousness/consciousness_probe_bundle.json"
MEMORY_WRITE_GATE_REF = "runtime/state/memory/memory_write_gate.json"
MEMORY_WRITE_GATE_CONSCIOUSNESS_CONTEXT_REF = (
    "runtime/state/memory/memory_write_gate.json#consciousness_write_context"
)
RESPONSIBILITY_LOOP_STATE_REF = "runtime/state/action/responsibility_loop_state.json"
CONSCIOUSNESS_CHAIN_WRITEBACK_REFS = [
    WORKSPACE_FRAME_REF,
    BROADCAST_FRAME_REF,
    METACOGNITION_STATE_REF,
    CONSCIOUSNESS_PROBE_REF,
    MEMORY_WRITE_GATE_CONSCIOUSNESS_CONTEXT_REF,
    f"{RESPONSIBILITY_LOOP_STATE_REF}#consciousness_context_profile",
    HANDOFF_PROFILE_REF,
]
CONTEXT_ACCUMULATION_WRITEBACK_REFS = [
    CONTEXT_ACCUMULATION_WINDOW_REF,
    TURN_TRANSITION_TRACE_REF,
    LANGUAGE_PERCEPT_REF,
    SEMANTIC_MAP_REF,
]
_LIVE_CONSCIOUSNESS_LINEAGE_FIELD_KEYS = (
    "resident_background_lineage_consciousness_write_context_refs",
    "resident_background_lineage_consciousness_write_context_bias",
    "resident_background_lineage_consciousness_write_context_ref_count",
    "resident_background_lineage_consciousness_write_context_workspace_candidate_count",
    "resident_background_lineage_consciousness_write_context_broadcast_target_count",
    "resident_background_lineage_consciousness_write_context_reportability_flag_count",
    "resident_background_lineage_consciousness_write_context_candidate_gate_adjustments",
    "resident_background_lineage_consciousness_write_context_boundary",
)
_LIVE_QUEUE_E_HANDOFF_LINEAGE_FIELD_KEYS = (
    "resident_background_lineage_live_queue_e_world_contact_handoff_refreshed",
    "resident_background_lineage_live_responsibility_consciousness_context_refs",
    "resident_background_lineage_world_contact_live_turn_focus",
    "resident_background_lineage_world_contact_handoff_boundary",
    "resident_background_lineage_world_contact_last_projected_from_live_turn_ref",
)


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
    prediction_workspace: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
    brain_graph: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
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
    live_turn_focus = live_semantic_focus or (
        live_language_turn_refs[-1] if live_language_turn_refs else None
    )
    state_dir = terminal_dir.parent
    memory_retrieval_frame = project_memory_retrieval_from_live_turn(
        memory_retrieval_frame=_read_json_if_exists(
            state_dir / "memory" / "memory_retrieval_frame.json"
        ),
        run_id=run_id,
        generated_at=generated_at,
        external_utterance=external_utterance,
        semantic_map=_read_json_if_exists(language_dir / "semantic_map_frame.json"),
        language_percept=_read_json_if_exists(language_dir / "language_percept_frame.json"),
        engram_index=_read_json_if_exists(state_dir / "memory" / "engram_index.json"),
        relationship_memory=_read_json_if_exists(state_dir / "memory" / "relationship_memory.json"),
        autobiographical_stack=_read_json_if_exists(state_dir / "self" / "autobiographical_stack.json"),
        dialogue_memory_summary=_read_json_if_exists(state_dir / "memory" / "dialogue_memory_summary.json"),
        life_state=_read_json_if_exists(state_dir / "life_state.json"),
        responsibility_loop_state=_read_json_if_exists(state_dir / "action" / "responsibility_loop_state.json"),
        state_merge_guard=_read_json_if_exists(state_dir / "memory" / "state_merge_guard.json"),
        live_language_turn_refs=live_language_turn_refs,
        dialogue_turn_refs=[external_turn_ref, life_turn_ref],
    )
    write_json(
        state_dir / "memory" / "memory_retrieval_frame.json",
        memory_retrieval_frame,
    )
    memory_retrieval_summary = memory_retrieval_context_summary(
        memory_retrieval_frame
    )
    exit_dream_next_wake_governance = memory_retrieval_frame.get(
        "exit_dream_next_wake_governance"
    )
    if not isinstance(exit_dream_next_wake_governance, dict):
        exit_dream_next_wake_governance = {}
    exit_dream_next_wake_memory_cue_refs = _dedupe_refs(
        _string_list(
            exit_dream_next_wake_governance.get("next_wake_memory_cue_refs")
        )
    )
    exit_dream_next_wake_governance_refs = _dedupe_refs(
        _string_list(exit_dream_next_wake_governance.get("governance_refs"))
    )
    exit_dream_memory_write_gate_ref = exit_dream_next_wake_governance.get(
        "memory_write_gate_ref"
    )
    exit_dream_state_merge_guard_ref = exit_dream_next_wake_governance.get(
        "state_merge_guard_ref"
    )
    exit_dream_fact_boundary_ref = exit_dream_next_wake_governance.get(
        "dream_fact_boundary_ref"
    )
    exit_dream_next_wake_candidate_boundary = (
        exit_dream_next_wake_governance.get("candidate_boundary")
    )
    exit_dream_next_wake_ref_set = _dedupe_refs(
        exit_dream_next_wake_memory_cue_refs
        + exit_dream_next_wake_governance_refs
        + [
            str(ref)
            for ref in [
                exit_dream_memory_write_gate_ref,
                exit_dream_state_merge_guard_ref,
                exit_dream_fact_boundary_ref,
            ]
            if ref
        ]
    )
    memory_retrieval_ref_set = _dedupe_refs(
        [
            MEMORY_RETRIEVAL_FRAME_REF,
            *list(memory_retrieval_frame.get("activated_engram_refs", [])),
            *list(memory_retrieval_frame.get("relationship_memory_hits", [])),
            *list(memory_retrieval_frame.get("autobiographical_hits", [])),
            *list(
                memory_retrieval_frame.get(
                    "autobiographical_responsibility_repair_hits", []
                )
            ),
            *list(memory_retrieval_frame.get("dream_residue_hits", [])),
            *list(memory_retrieval_frame.get("responsibility_hits", [])),
            *exit_dream_next_wake_ref_set,
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
        "memory_retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "memory_retrieval_reconstruction_focus": memory_retrieval_summary.get(
            "reconstruction_focus"
        ),
        "memory_retrieval_cue_terms": memory_retrieval_summary.get("cue_terms", []),
        "memory_retrieval_activated_ref_count": memory_retrieval_summary.get(
            "activated_engram_ref_count"
        ),
        "memory_retrieval_relationship_hit_count": memory_retrieval_summary.get(
            "relationship_hit_count"
        ),
        "memory_retrieval_dream_residue_hit_count": memory_retrieval_summary.get(
            "dream_residue_hit_count"
        ),
        "memory_retrieval_responsibility_hit_count": memory_retrieval_summary.get(
            "responsibility_hit_count"
        ),
        "memory_retrieval_autobiographical_repair_hit_count": (
            memory_retrieval_summary.get(
                "autobiographical_responsibility_repair_hit_count"
            )
        ),
        "memory_retrieval_autobiographical_repair_pressure_level": (
            memory_retrieval_summary.get("autobiographical_repair_pressure_level")
        ),
        "memory_retrieval_autobiographical_repair_attention_target": (
            memory_retrieval_summary.get("autobiographical_repair_attention_target")
        ),
        "memory_retrieval_autobiographical_repair_projection_boundary": (
            memory_retrieval_summary.get(
                "autobiographical_repair_projection_boundary"
            )
        ),
        "memory_retrieval_autobiographical_repair_retrieval_boundary": (
            memory_retrieval_summary.get(
                "autobiographical_repair_retrieval_boundary"
            )
        ),
        "memory_retrieval_ref_set": memory_retrieval_ref_set,
        "exit_dream_next_wake_governance_ref": (
            "runtime/state/memory/memory_retrieval_frame.json#exit_dream_next_wake_governance"
            if exit_dream_next_wake_governance
            else None
        ),
        "exit_dream_next_wake_memory_cue_refs": (
            exit_dream_next_wake_memory_cue_refs
        ),
        "exit_dream_next_wake_governance_refs": (
            exit_dream_next_wake_governance_refs
        ),
        "exit_dream_memory_write_gate_ref": exit_dream_memory_write_gate_ref,
        "exit_dream_state_merge_guard_ref": exit_dream_state_merge_guard_ref,
        "exit_dream_fact_boundary_ref": exit_dream_fact_boundary_ref,
        "exit_dream_next_wake_candidate_boundary": (
            exit_dream_next_wake_candidate_boundary
        ),
        "next_required_action": "await_next_external_relation_turn",
    }
    write_json(
        terminal_dir / "terminal_life_loop_state.json",
        updated_terminal_life_loop_state,
    )
    offline_learning_cumulative_payload = build_offline_learning_cumulative_payload(
        terminal_life_loop_state
    )
    resident_background_lineage_payload = build_resident_background_lineage_payload(
        terminal_life_loop_state
    )

    continuity_refresh = _refresh_long_horizon_continuity(
        state_dir=state_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state,
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        offline_learning_cumulative_profile=offline_learning_cumulative_payload,
        resident_background_lineage_payload=resident_background_lineage_payload,
        generated_at=generated_at,
        source_doc_refs=source_doc_refs,
        live_language_turn_refs=live_language_turn_refs,
        memory_retrieval_frame=memory_retrieval_frame,
        live_turn_focus=live_turn_focus,
        prediction_workspace=prediction_workspace,
        workspace_frame=workspace_frame,
        brain_graph=brain_graph,
        network_state=network_state,
        body_resource_budget=None,
        write_json=write_json,
        dialogue_turn_refs=[external_turn_ref, life_turn_ref],
    )
    effective_memory_write_gate = memory_write_gate
    live_consciousness_chain_profile: dict[str, Any] = {}
    live_queue_e_handoff_profile: dict[str, Any] = {}
    live_context_accumulation_profile: dict[str, Any] = {}
    live_shared_term_promotion_profile: dict[str, Any] = {}
    if continuity_refresh:
        effective_memory_write_gate = (
            continuity_refresh.get("memory_write_gate") or memory_write_gate
        )
        live_consciousness_chain_profile = _live_consciousness_chain_profile(
            continuity_refresh
        )
        live_queue_e_handoff_profile = _live_queue_e_handoff_terminal_profile(
            continuity_refresh
        )
        live_context_accumulation_profile = _live_context_accumulation_profile(
            continuity_refresh
        )
        live_shared_term_promotion_profile = _live_shared_term_promotion_profile(
            continuity_refresh
        )
        if live_consciousness_chain_profile:
            updated_terminal_life_loop_state.update(live_consciousness_chain_profile)
        if live_queue_e_handoff_profile:
            updated_terminal_life_loop_state.update(live_queue_e_handoff_profile)
            _merge_live_queue_e_handoff_into_lineage_state(
                updated_terminal_life_loop_state,
                live_queue_e_handoff_profile=live_queue_e_handoff_profile,
                handoff_profile=continuity_refresh.get(
                    "queue_e_world_contact_handoff_profile"
                ),
            )
        if live_context_accumulation_profile:
            updated_terminal_life_loop_state.update(live_context_accumulation_profile)
        if live_shared_term_promotion_profile:
            updated_terminal_life_loop_state.update(live_shared_term_promotion_profile)
        if (
            live_consciousness_chain_profile
            or live_queue_e_handoff_profile
            or live_context_accumulation_profile
            or live_shared_term_promotion_profile
        ):
            write_json(
                terminal_dir / "terminal_life_loop_state.json",
                updated_terminal_life_loop_state,
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
        updated_terminal_life_loop_state
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
    cross_wake_trait_drift_update_mode_summary = (
        background_trait_convergence_payload.get(
            "cross_wake_trait_drift_update_mode_summary", {}
        )
    )
    if not isinstance(cross_wake_trait_drift_update_mode_summary, dict):
        cross_wake_trait_drift_update_mode_summary = {}
    cross_wake_trait_drift_recalibration_names = list(
        background_trait_convergence_payload.get(
            "cross_wake_trait_drift_recalibration_names", []
        )
    )
    cross_wake_trait_drift_stabilized_names = list(
        background_trait_convergence_payload.get(
            "cross_wake_trait_drift_stabilized_names", []
        )
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
    resident_background_lineage_growth_self_modification_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_growth_self_modification_refs", []
        )
    )
    resident_background_lineage_state_merge_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_state_merge_refs", []
        )
    )
    resident_background_lineage_identity_consciousness_birth_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_identity_consciousness_birth_refs", []
        )
    )
    resident_background_lineage_resident_process_identity_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_resident_process_identity_refs", []
        )
    )
    resident_background_lineage_dream_wake_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_dream_wake_refs", []
        )
    )
    resident_background_lineage_autonomous_activity_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_autonomous_activity_refs", []
        )
    )
    resident_background_lineage_birth_repair_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_birth_repair_refs", []
        )
    )
    resident_background_lineage_world_contact_handoff_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_world_contact_handoff_refs", []
        )
    )
    resident_background_lineage_life_constraint_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_life_constraint_refs", []
        )
    )
    resident_background_lineage_heartbeat_cadence_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_heartbeat_cadence_refs", []
        )
    )
    resident_background_lineage_body_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_body_refs", []
        )
    )
    resident_background_lineage_prediction_write_gate_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_prediction_write_gate_refs", []
        )
    )
    resident_background_lineage_memory_retrieval_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_memory_retrieval_refs", []
        )
    )
    resident_background_lineage_autobiographical_repair_carrier_refs = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_autobiographical_repair_carrier_refs",
            [],
        )
    )
    resident_background_lineage_trait_drift_update_mode_summary = (
        resident_background_lineage_payload.get(
            "resident_background_lineage_trait_drift_update_mode_summary",
            {},
        )
    )
    if not isinstance(
        resident_background_lineage_trait_drift_update_mode_summary, dict
    ):
        resident_background_lineage_trait_drift_update_mode_summary = {}
    resident_background_lineage_trait_drift_recalibration_names = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_trait_drift_recalibration_names",
            [],
        )
    )
    resident_background_lineage_trait_drift_stabilized_names = list(
        resident_background_lineage_payload.get(
            "resident_background_lineage_trait_drift_stabilized_names",
            [],
        )
    )
    offline_learning_cumulative_refs = list(
        offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_evidence_refs", []
        )
    )
    offline_learning_cumulative_integration_mode = (
        offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_integration_mode"
        )
    )
    offline_learning_cumulative_relationship_reconsolidation_required = (
        offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_relationship_reconsolidation_required"
        )
    )
    queue_e_birth_repair_payload = build_queue_e_birth_repair_payload(
        updated_terminal_life_loop_state
    )
    queue_e_birth_repair_refs = list(
        queue_e_birth_repair_payload.get("queue_e_birth_repair_refs", [])
    )
    queue_e_world_contact_handoff_payload = build_queue_e_world_contact_handoff_payload(
        updated_terminal_life_loop_state
    )
    queue_e_world_contact_handoff_refs = list(
        queue_e_world_contact_handoff_payload.get(
            "queue_e_world_contact_handoff_refs", []
        )
    )
    if live_queue_e_handoff_profile:
        if queue_e_world_contact_handoff_refs:
            resident_background_lineage_world_contact_handoff_refs = list(
                queue_e_world_contact_handoff_refs
            )
        else:
            resident_background_lineage_world_contact_handoff_refs = _dedupe_refs(
                _string_list(
                    live_queue_e_handoff_profile.get("queue_e_world_contact_ref_set")
                )
            )
    life_constraint_payload = build_life_constraint_payload(
        updated_terminal_life_loop_state
    )
    life_constraint_refs = list(
        life_constraint_payload.get("life_constraint_evidence_refs", [])
    )
    resident_background_lineage_refs = _dedupe_refs(
        resident_background_lineage_refs
        + resident_background_lineage_language_refs
        + resident_background_lineage_state_merge_refs
        + resident_background_lineage_identity_consciousness_birth_refs
        + resident_background_lineage_resident_process_identity_refs
        + resident_background_lineage_offline_learning_refs
        + resident_background_lineage_growth_self_modification_refs
        + resident_background_lineage_dream_wake_refs
        + resident_background_lineage_autonomous_activity_refs
        + resident_background_lineage_birth_repair_refs
        + resident_background_lineage_world_contact_handoff_refs
        + resident_background_lineage_life_constraint_refs
        + resident_background_lineage_heartbeat_cadence_refs
        + resident_background_lineage_body_refs
        + resident_background_lineage_prediction_write_gate_refs
        + resident_background_lineage_memory_retrieval_refs
        + resident_background_lineage_autobiographical_repair_carrier_refs
        + life_constraint_refs
        + queue_e_birth_repair_refs
        + queue_e_world_contact_handoff_refs
    )
    prediction_write_gate_payload = build_prediction_write_gate_payload(
        terminal_life_loop_state=updated_terminal_life_loop_state,
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=effective_memory_write_gate,
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
    if (
        prediction_write_gate_refs
        and not resident_background_lineage_prediction_write_gate_refs
    ):
        resident_background_lineage_prediction_write_gate_refs = list(
            prediction_write_gate_refs
        )
    if resident_background_lineage_prediction_write_gate_refs:
        resident_background_lineage_refs = _dedupe_refs(
            resident_background_lineage_refs
            + resident_background_lineage_prediction_write_gate_refs
        )
    resident_background_lineage_body_signal_refs = _dedupe_refs(
        list(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_refs"
            )
            or []
        )
        + list(prediction_write_gate_payload.get("body_signal_refs") or [])
    )
    resident_background_lineage_body_signal_write_bias = (
        resident_background_lineage_payload.get(
            "resident_background_lineage_body_signal_write_bias"
        )
        or prediction_write_gate_payload.get("body_signal_write_bias")
    )
    resident_background_lineage_body_signal_candidate_gate_adjustments = _dedupe_refs(
        list(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_candidate_gate_adjustments"
            )
            or []
        )
        + list(
            prediction_write_gate_payload.get(
                "body_signal_candidate_gate_adjustments"
            )
            or []
        )
    )
    if resident_background_lineage_body_signal_refs:
        resident_background_lineage_refs = _dedupe_refs(
            resident_background_lineage_refs
            + resident_background_lineage_body_signal_refs
        )
    if live_consciousness_chain_profile:
        resident_background_lineage_consciousness_write_context_refs = _dedupe_refs(
            list(
                prediction_write_gate_payload.get("consciousness_write_context_refs")
                or []
            )
            or _string_list(
                live_consciousness_chain_profile.get("consciousness_write_context_refs")
            )
        )
        resident_background_lineage_consciousness_write_context_bias = (
            prediction_write_gate_payload.get("consciousness_write_context_bias")
            or live_consciousness_chain_profile.get("consciousness_write_context_bias")
        )
        resident_background_lineage_consciousness_write_context_candidate_gate_adjustments = (
            _dedupe_refs(
                list(
                    prediction_write_gate_payload.get(
                        "consciousness_write_context_candidate_gate_adjustments"
                    )
                    or []
                )
            )
        )
    else:
        resident_background_lineage_consciousness_write_context_refs = _dedupe_refs(
            list(
                resident_background_lineage_payload.get(
                    "resident_background_lineage_consciousness_write_context_refs"
                )
                or []
            )
            + list(
                prediction_write_gate_payload.get("consciousness_write_context_refs")
                or []
            )
        )
        resident_background_lineage_consciousness_write_context_bias = (
            resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_bias"
            )
            or prediction_write_gate_payload.get("consciousness_write_context_bias")
        )
        resident_background_lineage_consciousness_write_context_candidate_gate_adjustments = _dedupe_refs(
            list(
                resident_background_lineage_payload.get(
                    "resident_background_lineage_consciousness_write_context_candidate_gate_adjustments"
                )
                or []
            )
            + list(
                prediction_write_gate_payload.get(
                    "consciousness_write_context_candidate_gate_adjustments"
                )
                or []
            )
        )
    if resident_background_lineage_consciousness_write_context_refs:
        resident_background_lineage_refs = _dedupe_refs(
            resident_background_lineage_refs
            + resident_background_lineage_consciousness_write_context_refs
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
            LIFE_STATE_MEMORY_RETRIEVAL_REF,
            "runtime/state/life_state.json#growth_self_modification_index",
            "runtime/state/life_state.json#memory_index.growth_self_modification_refs",
            "runtime/state/life_state.json#language_state.growth_self_modification_refs",
        ],
        engram_index_writeback_refs=[
            ENGRAM_INDEX_REF,
            ENGRAM_INDEX_LIVE_DIALOGUE_REF,
            ENGRAM_INDEX_LIVE_LANGUAGE_REF,
            ENGRAM_INDEX_RELATIONSHIP_REF,
            ENGRAM_INDEX_OFFLINE_REF,
        ],
        autobiographical_writeback_refs=[
            AUTOBIOGRAPHICAL_STACK_REF,
            AUTOBIOGRAPHICAL_STACK_TURN_REF,
            AUTOBIOGRAPHICAL_STACK_LIVE_LANGUAGE_REF,
            AUTOBIOGRAPHICAL_STACK_RELATIONSHIP_REF,
            "runtime/state/self/autobiographical_stack.json#growth_self_modification_projection",
            "runtime/state/self/autobiographical_stack.json#growth_self_modification_refs",
            "runtime/state/self/autobiographical_stack.json#responsibility_repair_projection",
            "runtime/state/self/autobiographical_stack.json#autobiographical_responsibility_refs",
            "runtime/state/self/autobiographical_stack.json#autobiographical_regret_refs",
            "runtime/state/self/autobiographical_stack.json#autobiographical_repair_refs",
            "runtime/state/self/autobiographical_stack.json#queue_e_repair_refs",
        ],
        brain_graph_writeback_refs=[BRAIN_GRAPH_REF],
        network_state_writeback_refs=[NETWORK_STATE_REF],
        workspace_frame_writeback_refs=CONSCIOUSNESS_CHAIN_WRITEBACK_REFS,
        prediction_workspace_writeback_refs=[PREDICTION_WORKSPACE_REF],
        memory_retrieval_writeback_refs=memory_retrieval_ref_set,
        replay_cue_refs=replay_cue_refs,
        terminal_state_refs=[
            SAFE_TERMINAL_LOOP_REF,
            TERMINAL_LIFE_LOOP_REF,
            *CONTEXT_ACCUMULATION_WRITEBACK_REFS,
        ],
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        background_trait_convergence_refs=background_trait_convergence_refs,
        cross_wake_trait_convergence_refs=cross_wake_trait_convergence_refs,
        cross_wake_trait_drift_update_mode_summary=(
            cross_wake_trait_drift_update_mode_summary
        ),
        cross_wake_trait_drift_recalibration_names=(
            cross_wake_trait_drift_recalibration_names
        ),
        cross_wake_trait_drift_stabilized_names=(
            cross_wake_trait_drift_stabilized_names
        ),
        resident_background_lineage_refs=resident_background_lineage_refs,
        life_constraint_refs=life_constraint_refs,
        queue_e_birth_repair_refs=queue_e_birth_repair_refs,
        resident_background_lineage_trait_drift_update_mode_summary=(
            resident_background_lineage_trait_drift_update_mode_summary
        ),
        resident_background_lineage_trait_drift_recalibration_names=(
            resident_background_lineage_trait_drift_recalibration_names
        ),
        resident_background_lineage_trait_drift_stabilized_names=(
            resident_background_lineage_trait_drift_stabilized_names
        ),
        resident_background_lineage_state_merge_refs=(
            resident_background_lineage_state_merge_refs
        ),
        resident_background_lineage_identity_consciousness_birth_refs=(
            resident_background_lineage_identity_consciousness_birth_refs
        ),
        resident_background_lineage_resident_process_identity_refs=(
            resident_background_lineage_resident_process_identity_refs
        ),
        resident_background_lineage_offline_learning_refs=(
            resident_background_lineage_offline_learning_refs
        ),
        resident_background_lineage_growth_self_modification_refs=(
            resident_background_lineage_growth_self_modification_refs
        ),
        resident_background_lineage_dream_wake_refs=(
            resident_background_lineage_dream_wake_refs
        ),
        resident_background_lineage_autonomous_activity_refs=(
            resident_background_lineage_autonomous_activity_refs
        ),
        resident_background_lineage_birth_repair_refs=(
            resident_background_lineage_birth_repair_refs
        ),
        resident_background_lineage_world_contact_handoff_refs=(
            resident_background_lineage_world_contact_handoff_refs
        ),
        resident_background_lineage_life_constraint_refs=(
            resident_background_lineage_life_constraint_refs
        ),
        resident_background_lineage_heartbeat_cadence_refs=(
            resident_background_lineage_heartbeat_cadence_refs
        ),
        resident_background_lineage_body_refs=resident_background_lineage_body_refs,
        resident_background_lineage_body_signal_refs=(
            resident_background_lineage_body_signal_refs
        ),
        resident_background_lineage_body_signal_write_bias=(
            str(resident_background_lineage_body_signal_write_bias)
            if resident_background_lineage_body_signal_write_bias
            else None
        ),
        resident_background_lineage_body_signal_fatigue_load=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_fatigue_load"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_fatigue_load"
            )
            is not None
            else prediction_write_gate_payload.get("body_signal_fatigue_load")
        ),
        resident_background_lineage_body_signal_pain_pressure=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_pain_pressure"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_pain_pressure"
            )
            is not None
            else prediction_write_gate_payload.get("body_signal_pain_pressure")
        ),
        resident_background_lineage_body_signal_dream_residue_load=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_dream_residue_load"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_dream_residue_load"
            )
            is not None
            else prediction_write_gate_payload.get("body_signal_dream_residue_load")
        ),
        resident_background_lineage_body_signal_repair_drive=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_repair_drive"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_repair_drive"
            )
            is not None
            else prediction_write_gate_payload.get("body_signal_repair_drive")
        ),
        resident_background_lineage_body_signal_unexpected_uncertainty=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_unexpected_uncertainty"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_unexpected_uncertainty"
            )
            is not None
            else prediction_write_gate_payload.get(
                "body_signal_unexpected_uncertainty"
            )
        ),
        resident_background_lineage_body_signal_ref_count=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_ref_count"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_body_signal_ref_count"
            )
            is not None
            else prediction_write_gate_payload.get("body_signal_ref_count")
        ),
        resident_background_lineage_body_signal_candidate_gate_adjustments=(
            resident_background_lineage_body_signal_candidate_gate_adjustments
        ),
        resident_background_lineage_consciousness_write_context_refs=(
            resident_background_lineage_consciousness_write_context_refs
        ),
        resident_background_lineage_consciousness_write_context_bias=(
            str(resident_background_lineage_consciousness_write_context_bias)
            if resident_background_lineage_consciousness_write_context_bias
            else None
        ),
        resident_background_lineage_consciousness_write_context_ref_count=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_ref_count"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_ref_count"
            )
            is not None
            else prediction_write_gate_payload.get(
                "consciousness_write_context_ref_count"
            )
        ),
        resident_background_lineage_consciousness_write_context_workspace_candidate_count=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_workspace_candidate_count"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_workspace_candidate_count"
            )
            is not None
            else prediction_write_gate_payload.get(
                "consciousness_write_context_workspace_candidate_count"
            )
        ),
        resident_background_lineage_consciousness_write_context_broadcast_target_count=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_broadcast_target_count"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_broadcast_target_count"
            )
            is not None
            else prediction_write_gate_payload.get(
                "consciousness_write_context_broadcast_target_count"
            )
        ),
        resident_background_lineage_consciousness_write_context_reportability_flag_count=(
            resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_reportability_flag_count"
            )
            if resident_background_lineage_payload.get(
                "resident_background_lineage_consciousness_write_context_reportability_flag_count"
            )
            is not None
            else prediction_write_gate_payload.get(
                "consciousness_write_context_reportability_flag_count"
            )
        ),
        resident_background_lineage_consciousness_write_context_candidate_gate_adjustments=(
            resident_background_lineage_consciousness_write_context_candidate_gate_adjustments
        ),
        resident_background_lineage_consciousness_write_context_boundary=(
            str(
                resident_background_lineage_payload.get(
                    "resident_background_lineage_consciousness_write_context_boundary"
                )
                or prediction_write_gate_payload.get(
                    "consciousness_write_context_boundary"
                )
            )
            if (
                resident_background_lineage_payload.get(
                    "resident_background_lineage_consciousness_write_context_boundary"
                )
                or prediction_write_gate_payload.get(
                    "consciousness_write_context_boundary"
                )
            )
            else None
        ),
        resident_background_lineage_prediction_write_gate_refs=(
            resident_background_lineage_prediction_write_gate_refs
        ),
        resident_background_lineage_memory_retrieval_refs=(
            resident_background_lineage_memory_retrieval_refs
        ),
        resident_background_lineage_autobiographical_repair_carrier_refs=(
            resident_background_lineage_autobiographical_repair_carrier_refs
        ),
        offline_learning_cumulative_refs=offline_learning_cumulative_refs,
        offline_learning_cumulative_integration_mode=(
            str(offline_learning_cumulative_integration_mode)
            if offline_learning_cumulative_integration_mode
            else None
        ),
        offline_learning_cumulative_relationship_reconsolidation_required=(
            bool(
                offline_learning_cumulative_relationship_reconsolidation_required
            )
            if offline_learning_cumulative_relationship_reconsolidation_required
            is not None
            else None
        ),
        prediction_write_gate_refs=prediction_write_gate_refs,
        queue_e_world_contact_handoff_refs=queue_e_world_contact_handoff_refs,
        live_language_turn_refs=live_language_turn_refs,
        exit_dream_next_wake_memory_cue_refs=(
            exit_dream_next_wake_memory_cue_refs
        ),
        exit_dream_next_wake_governance_refs=(
            exit_dream_next_wake_governance_refs
        ),
        exit_dream_memory_write_gate_ref=(
            str(exit_dream_memory_write_gate_ref)
            if exit_dream_memory_write_gate_ref
            else None
        ),
        exit_dream_state_merge_guard_ref=(
            str(exit_dream_state_merge_guard_ref)
            if exit_dream_state_merge_guard_ref
            else None
        ),
        exit_dream_fact_boundary_ref=(
            str(exit_dream_fact_boundary_ref)
            if exit_dream_fact_boundary_ref
            else None
        ),
        exit_dream_next_wake_candidate_boundary=(
            str(exit_dream_next_wake_candidate_boundary)
            if exit_dream_next_wake_candidate_boundary
            else None
        ),
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
        "memory_retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "memory_retrieval_autobiographical_repair_hit_count": (
            memory_retrieval_summary.get(
                "autobiographical_responsibility_repair_hit_count"
            )
        ),
        "memory_retrieval_autobiographical_repair_pressure_level": (
            memory_retrieval_summary.get("autobiographical_repair_pressure_level")
        ),
        "memory_retrieval_autobiographical_repair_attention_target": (
            memory_retrieval_summary.get("autobiographical_repair_attention_target")
        ),
        "memory_retrieval_autobiographical_repair_projection_boundary": (
            memory_retrieval_summary.get(
                "autobiographical_repair_projection_boundary"
            )
        ),
        "memory_retrieval_autobiographical_repair_retrieval_boundary": (
            memory_retrieval_summary.get(
                "autobiographical_repair_retrieval_boundary"
            )
        ),
        "exit_dream_next_wake_governance_ref": (
            "runtime/state/memory/memory_retrieval_frame.json#exit_dream_next_wake_governance"
            if exit_dream_next_wake_governance
            else None
        ),
        "exit_dream_next_wake_memory_cue_refs": (
            exit_dream_next_wake_memory_cue_refs
        ),
        "exit_dream_next_wake_governance_refs": (
            exit_dream_next_wake_governance_refs
        ),
        "exit_dream_memory_write_gate_ref": exit_dream_memory_write_gate_ref,
        "exit_dream_state_merge_guard_ref": exit_dream_state_merge_guard_ref,
        "exit_dream_fact_boundary_ref": exit_dream_fact_boundary_ref,
        "exit_dream_next_wake_candidate_boundary": (
            exit_dream_next_wake_candidate_boundary
        ),
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
        lineage_packet_update = {
            key: value
            for key, value in resident_background_lineage_payload.items()
            if key != "resident_background_lineage_state"
        }
        if live_consciousness_chain_profile:
            for stale_key in _LIVE_CONSCIOUSNESS_LINEAGE_FIELD_KEYS:
                lineage_packet_update.pop(stale_key, None)
        if live_queue_e_handoff_profile:
            for stale_key in _LIVE_QUEUE_E_HANDOFF_LINEAGE_FIELD_KEYS:
                lineage_packet_update.pop(stale_key, None)
        resumed_dialogue_packet.update(lineage_packet_update)
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
    if queue_e_birth_repair_payload:
        resumed_dialogue_packet.update(
            {
                key: value
                for key, value in queue_e_birth_repair_payload.items()
                if key != "queue_e_birth_repair_waiting_profile"
            }
        )
    if queue_e_world_contact_handoff_payload:
        resumed_dialogue_packet.update(
            {
                key: value
                for key, value in queue_e_world_contact_handoff_payload.items()
                if key != "queue_e_world_contact_handoff_profile"
            }
        )
        if live_queue_e_handoff_profile:
            _apply_live_queue_e_handoff_lineage_fields(
                resumed_dialogue_packet,
                queue_e_world_contact_handoff_payload=queue_e_world_contact_handoff_payload,
                live_queue_e_handoff_profile=live_queue_e_handoff_profile,
            )
    if life_constraint_payload:
        resumed_dialogue_packet.update(life_constraint_payload)
    if resident_background_lineage_refs:
        resumed_dialogue_packet["resident_background_lineage_evidence_refs"] = (
            resident_background_lineage_refs
        )
    if resident_background_lineage_growth_self_modification_refs:
        resumed_dialogue_packet[
            "resident_background_lineage_growth_self_modification_refs"
        ] = resident_background_lineage_growth_self_modification_refs
    if resident_background_lineage_memory_retrieval_refs:
        resumed_dialogue_packet[
            "resident_background_lineage_memory_retrieval_refs"
        ] = resident_background_lineage_memory_retrieval_refs
    if resident_background_lineage_autobiographical_repair_carrier_refs:
        resumed_dialogue_packet[
            "resident_background_lineage_autobiographical_repair_carrier_refs"
        ] = resident_background_lineage_autobiographical_repair_carrier_refs
    if prediction_write_gate_payload:
        resumed_dialogue_packet.update(prediction_write_gate_payload)
        attach_prediction_write_gate_lineage_fallback(
            resumed_dialogue_packet,
            prediction_write_gate_payload,
        )
        if live_consciousness_chain_profile:
            _apply_live_consciousness_lineage_fields(
                resumed_dialogue_packet,
                prediction_write_gate_payload=prediction_write_gate_payload,
                live_consciousness_chain_profile=live_consciousness_chain_profile,
            )
    if continuity_refresh is not None:
        resumed_dialogue_packet["relationship_timeline_ref"] = RELATIONSHIP_TIMELINE_REF
        resumed_dialogue_packet["commitment_expression_plan_ref"] = COMMITMENT_EXPRESSION_PLAN_REF
        resumed_dialogue_packet["apology_repair_language_trace_ref"] = (
            APOLOGY_REPAIR_LANGUAGE_TRACE_REF
        )
        resumed_dialogue_packet["brain_graph_ref"] = BRAIN_GRAPH_REF
        resumed_dialogue_packet["network_state_ref"] = NETWORK_STATE_REF
        resumed_dialogue_packet["workspace_frame_ref"] = WORKSPACE_FRAME_REF
        resumed_dialogue_packet["broadcast_frame_ref"] = BROADCAST_FRAME_REF
        resumed_dialogue_packet["metacognition_ref"] = METACOGNITION_STATE_REF
        resumed_dialogue_packet["consciousness_probe_ref"] = CONSCIOUSNESS_PROBE_REF
        resumed_dialogue_packet["memory_write_gate_consciousness_context_ref"] = (
            MEMORY_WRITE_GATE_CONSCIOUSNESS_CONTEXT_REF
        )
        resumed_dialogue_packet["queue_e_world_contact_handoff_profile_ref"] = (
            HANDOFF_PROFILE_REF
        )
        resumed_dialogue_packet["prediction_workspace_ref"] = PREDICTION_WORKSPACE_REF
        resumed_dialogue_packet["engram_index_ref"] = ENGRAM_INDEX_REF
        resumed_dialogue_packet["autobiographical_stack_ref"] = (
            AUTOBIOGRAPHICAL_STACK_REF
        )
        resumed_dialogue_packet["life_state_ref"] = "runtime/state/life_state.json"
        resumed_dialogue_packet["context_accumulation_ref"] = (
            CONTEXT_ACCUMULATION_WINDOW_REF
        )
        resumed_dialogue_packet["turn_transition_ref"] = TURN_TRANSITION_TRACE_REF
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
    self_narrative_trace: dict[str, Any] | None,
    commitment_index: dict[str, Any],
    offline_learning_cumulative_profile: dict[str, Any] | None,
    resident_background_lineage_payload: dict[str, Any] | None,
    generated_at: str,
    source_doc_refs: list[str],
    live_language_turn_refs: list[str] | None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    live_turn_focus: str | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
    brain_graph: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    dialogue_turn_refs: list[str] | None = None,
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
    engram_index_path = state_dir / "memory" / "engram_index.json"
    life_state_path = state_dir / "life_state.json"
    autobiographical_stack_path = state_dir / "self" / "autobiographical_stack.json"
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
    engram_index = _read_json_if_exists(engram_index_path)
    life_state = _read_json(life_state_path)
    autobiographical_stack = _read_json_if_exists(autobiographical_stack_path)
    persisted_self_model_state = _read_json(self_model_path)
    previous_trait_drift_monitor = _read_json_if_exists(trait_drift_monitor_path)
    responsibility_loop_state = _read_json(responsibility_loop_path)
    world_contact_summary = _read_json_if_exists(world_contact_summary_path)
    pain_regret_repair_report = _read_json_if_exists(pain_regret_repair_report_path)
    background_continuity_profile = _continuity_background_profile_for_evolution(
        life_state.get("background_continuity_profile"),
        resident_background_lineage_payload,
    )

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
        background_continuity_profile=background_continuity_profile,
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
    refresh_run_id = str(
        refreshed_relationship_timeline.get("run_id")
        or relationship_timeline.get("run_id")
        or "resident-turn-writeback"
    )
    refreshed_autobiographical_stack = (
        project_autobiographical_stack_from_live_turn(
            autobiographical_stack=autobiographical_stack,
            generated_at=generated_at,
            run_id=refresh_run_id,
            dialogue_turn_refs=dialogue_turn_refs,
            live_language_turn_refs=live_language_turn_refs,
            self_narrative_trace=self_narrative_trace,
            self_model_state=evolved_self_model_state,
            relationship_graph=evolved_relationship_graph,
            relationship_timeline=refreshed_relationship_timeline,
            engram_index=engram_index,
            relationship_memory=refreshed_relationship_memory,
            commitment_truth_state=commitment_truth_state,
            responsibility_ledger=responsibility_ledger,
            commitment_repair_index=commitment_index,
            apology_repair_language_trace=refreshed_apology_repair_language_trace,
            responsibility_loop_state=responsibility_loop_state,
            world_contact_summary=world_contact_summary,
            pain_regret_repair_report=pain_regret_repair_report,
            trigger_ref=RESUMED_DIALOGUE_PACKET_REF,
        )
    )
    refreshed_engram_index = project_engram_index_from_live_turn(
        engram_index=engram_index,
        generated_at=generated_at,
        run_id=refresh_run_id,
        dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        relationship_memory=refreshed_relationship_memory,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        state_merge_guard=refreshed_state_merge_guard,
        autobiographical_stack=refreshed_autobiographical_stack,
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )
    refreshed_life_state = project_responsibility_language_continuity(
        life_state=life_state,
        background_continuity_profile=background_continuity_profile,
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
        memory_retrieval_frame=memory_retrieval_frame,
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
        engram_index=refreshed_engram_index,
        additional_runtime_trace_refs=[
            ref
            for ref in [
                ENGRAM_INDEX_REF,
                MEMORY_RETRIEVAL_FRAME_REF if memory_retrieval_frame else None,
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
    updated_brain_graph = project_brain_graph_from_live_turn(
        brain_graph=_read_json_if_exists(state_dir / "neural_life_core" / "brain_graph.json"),
        generated_at=generated_at,
        run_id=refresh_run_id,
        dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        self_model_state=evolved_self_model_state,
        network_state=_read_json_if_exists(state_dir / "neural_life_core" / "network_state.json"),
        workspace_frame=_read_json_if_exists(state_dir / "consciousness" / "workspace_frame.json"),
    )
    updated_multiscale_region_graph = project_multiscale_region_graph_from_live_turn(
        multiscale_region_graph=_read_json_if_exists(
            state_dir / "neural_life_core" / "multiscale_region_graph.json"
        ),
        generated_at=generated_at,
        run_id=refresh_run_id,
        dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        self_model_state=evolved_self_model_state,
        network_state=_read_json_if_exists(state_dir / "neural_life_core" / "network_state.json"),
        workspace_frame=_read_json_if_exists(state_dir / "consciousness" / "workspace_frame.json"),
        signal_media_runtime=signal_media_runtime,
    )
    if refreshed_state_merge_guard:
        write_json(state_merge_guard_path, refreshed_state_merge_guard)
    write_json(autobiographical_stack_path, refreshed_autobiographical_stack)
    write_json(engram_index_path, refreshed_engram_index)
    updated_network_state = project_network_state_from_live_turn(
        network_state=_read_json_if_exists(state_dir / "neural_life_core" / "network_state.json"),
        generated_at=generated_at,
        run_id=refresh_run_id,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
        signal_media_runtime=signal_media_runtime,
        brain_graph=updated_brain_graph,
        multiscale_region_graph=updated_multiscale_region_graph,
        workspace_frame=_read_json_if_exists(state_dir / "consciousness" / "workspace_frame.json"),
        prediction_workspace=_read_json_if_exists(state_dir / "prediction" / "prediction_workspace_frame.json"),
        body_resource_budget=body_resource_budget,
    )
    updated_workspace_frame = project_workspace_frame_from_live_turn(
        workspace_frame=_read_json_if_exists(state_dir / "consciousness" / "workspace_frame.json"),
        generated_at=generated_at,
        run_id=refresh_run_id,
        prediction_workspace=_read_json_if_exists(state_dir / "prediction" / "prediction_workspace_frame.json"),
        network_state=updated_network_state,
        engram_index=refreshed_engram_index,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
    )
    updated_broadcast_frame = project_broadcast_frame_from_live_turn(
        broadcast_frame=_read_json_if_exists(state_dir / "consciousness" / "broadcast_frame.json"),
        generated_at=generated_at,
        workspace_frame=updated_workspace_frame,
        run_id=refresh_run_id,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
    )
    updated_metacognition_state = project_metacognition_state_from_live_turn(
        metacognition_state=_read_json_if_exists(
            state_dir / "consciousness" / "metacognition_state.json"
        ),
        generated_at=generated_at,
        broadcast_frame=updated_broadcast_frame,
        workspace_frame=updated_workspace_frame,
        run_id=refresh_run_id,
        memory_retrieval_frame=memory_retrieval_frame,
        expression_monitor_state=_read_json_if_exists(
            language_dir / "expression_monitor_state.json"
        ),
        live_turn_focus=live_turn_focus,
    )
    updated_network_state = project_network_state_from_live_turn(
        network_state=updated_network_state,
        generated_at=generated_at,
        run_id=refresh_run_id,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
        signal_media_runtime=signal_media_runtime,
        brain_graph=updated_brain_graph,
        multiscale_region_graph=updated_multiscale_region_graph,
        workspace_frame=updated_workspace_frame,
        prediction_workspace=_read_json_if_exists(
            state_dir / "prediction" / "prediction_workspace_frame.json"
        ),
        body_resource_budget=body_resource_budget,
        metacognition_state=updated_metacognition_state,
        broadcast_frame=updated_broadcast_frame,
        go_nogo_state=_read_json_if_exists(state_dir / "action" / "go_nogo_state.json"),
    )
    write_json(state_dir / "neural_life_core" / "brain_graph.json", updated_brain_graph)
    write_json(
        state_dir / "neural_life_core" / "multiscale_region_graph.json",
        updated_multiscale_region_graph,
    )
    write_json(state_dir / "neural_life_core" / "network_state.json", updated_network_state)
    write_json(state_dir / "consciousness" / "workspace_frame.json", updated_workspace_frame)
    write_json(state_dir / "consciousness" / "broadcast_frame.json", updated_broadcast_frame)
    write_json(
        state_dir / "consciousness" / "metacognition_state.json",
        updated_metacognition_state,
    )
    consciousness_dir = state_dir / "consciousness"
    consciousness_dir.mkdir(parents=True, exist_ok=True)
    memory_write_gate_path = state_dir / "memory" / "memory_write_gate.json"
    updated_consciousness_probe = project_consciousness_probe_bundle_from_live_turn(
        consciousness_probe_bundle=_read_json_if_exists(
            consciousness_dir / "consciousness_probe_bundle.json"
        ),
        generated_at=generated_at,
        workspace_frame=updated_workspace_frame,
        broadcast_frame=updated_broadcast_frame,
        metacognition_state=updated_metacognition_state,
        prediction_workspace=prediction_workspace
        or _read_json_if_exists(state_dir / "prediction" / "prediction_workspace_frame.json"),
        expression_plan=expression_plan,
        commitment_truth_state=commitment_truth_state,
        run_id=refresh_run_id,
        live_language_turn_refs=live_language_turn_refs,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_turn_focus=live_turn_focus,
    )
    updated_memory_write_gate = project_memory_write_gate_with_consciousness_context(
        memory_write_gate=_read_json_if_exists(memory_write_gate_path),
        workspace_frame=updated_workspace_frame,
        broadcast_frame=updated_broadcast_frame,
        metacognition_state=updated_metacognition_state,
        consciousness_probe_bundle=updated_consciousness_probe,
    )
    if updated_memory_write_gate:
        updated_memory_write_gate = project_memory_write_gate_with_signal_body(
            memory_write_gate=updated_memory_write_gate,
            signal_media_runtime=signal_media_runtime
            or _read_json_if_exists(state_dir / "signal" / "signal_media_runtime.json"),
            body_resource_budget=body_resource_budget
            or _read_json_if_exists(state_dir / "body" / "body_resource_budget.json"),
            core_affect_vector=_read_json_if_exists(
                state_dir / "body" / "core_affect_vector.json"
            ),
            offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        )
    updated_responsibility_loop_state = (
        project_responsibility_loop_with_consciousness_context(
            responsibility_loop_state=responsibility_loop_state,
            generated_at=generated_at,
            workspace_frame=updated_workspace_frame,
            broadcast_frame=updated_broadcast_frame,
            metacognition_state=updated_metacognition_state,
            consciousness_probe_bundle=updated_consciousness_probe,
            live_turn_focus=live_turn_focus,
        )
    )
    write_json(
        consciousness_dir / "consciousness_probe_bundle.json",
        updated_consciousness_probe,
    )
    if updated_memory_write_gate:
        write_json(memory_write_gate_path, updated_memory_write_gate)
    if updated_responsibility_loop_state:
        write_json(responsibility_loop_path, updated_responsibility_loop_state)
    refreshed_expression_plan = project_expression_plan_with_queue_e_repair_modulation(
        expression_plan=expression_plan,
        responsibility_loop_state=updated_responsibility_loop_state
        or responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    write_json(expression_plan_path, refreshed_expression_plan)
    expression_plan = refreshed_expression_plan
    life_targets_dir = state_dir / "life_targets"
    life_targets_dir.mkdir(parents=True, exist_ok=True)
    updated_queue_e_handoff_profile = (
        project_queue_e_world_contact_repair_hold_handoff_from_live_turn(
            handoff_profile=_read_json_if_exists(
                life_targets_dir / "queue_e_world_contact_repair_hold_handoff.json"
            ),
            generated_at=generated_at,
            world_contact_validation=_read_json_if_exists(
                state_dir / "validation" / "world_contact_validation.json"
            ),
            validation_rollup=_read_json_if_exists(
                state_dir / "validation" / "validation_rollup.json"
            ),
            schema_runner_manifest=_read_json_if_exists(
                state_dir / "schema_runner" / "run_manifest.json"
            ),
            responsibility_loop_state=updated_responsibility_loop_state,
            live_turn_focus=live_turn_focus,
            live_dialogue_turn_refs=dialogue_turn_refs,
        )
    )
    write_json(
        life_targets_dir / "queue_e_world_contact_repair_hold_handoff.json",
        updated_queue_e_handoff_profile,
    )
    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    language_percept = _read_json_if_exists(language_dir / "language_percept_frame.json")
    semantic_map = _read_json_if_exists(language_dir / "semantic_map_frame.json")
    relation_scope_index = _read_json_if_exists(
        language_dir / "relation_scope_language_index.json"
    )
    relationship_subject = next(
        (
            item
            for item in evolved_relationship_graph.get("subjects", [])
            if isinstance(item, dict)
        ),
        {},
    )
    expression_monitor_state = _read_json_if_exists(
        language_dir / "expression_monitor_state.json"
    )
    narrative_trace = self_narrative_trace or _read_json_if_exists(
        language_dir / "self_narrative_language_trace.json"
    )
    updated_context_accumulation = project_context_accumulation_window_from_live_turn(
        context_accumulation=_read_json_if_exists(
            terminal_dir / "context_accumulation_window.json"
        ),
        generated_at=generated_at,
        relationship_graph=evolved_relationship_graph,
        language_percept=language_percept,
        semantic_map=semantic_map,
        expression_monitor=expression_monitor_state,
        relation_scope_index=relation_scope_index,
        self_narrative_trace=narrative_trace,
        commitment_truth_state=commitment_truth_state,
        dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
        run_id=refresh_run_id,
    )
    updated_turn_transition = project_turn_transition_trace_from_live_turn(
        turn_transition=_read_json_if_exists(terminal_dir / "turn_transition_trace.json"),
        generated_at=generated_at,
        dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
        semantic_focus=updated_context_accumulation.get("semantic_focus"),
        unresolved_commitment_refs=list(
            updated_context_accumulation.get("unresolved_commitment_refs", [])
        ),
        run_id=refresh_run_id,
    )
    write_json(
        terminal_dir / "context_accumulation_window.json",
        updated_context_accumulation,
    )
    write_json(terminal_dir / "turn_transition_trace.json", updated_turn_transition)
    shared_term_registry_path = language_dir / "shared_term_registry.json"
    existing_shared_term_registry = _read_json_if_exists(shared_term_registry_path)
    refreshed_shared_term_registry = project_shared_term_registry_from_live_evidence(
        shared_term_registry=existing_shared_term_registry,
        generated_at=generated_at,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        language_percept=language_percept,
        semantic_map=semantic_map,
        context_accumulation=updated_context_accumulation,
        relation_scope_index=relation_scope_index,
        dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
    )
    if refreshed_shared_term_registry:
        write_json(shared_term_registry_path, refreshed_shared_term_registry)
    if language_percept and semantic_map:
        semantic_map = project_semantic_map_from_live_evidence(
            semantic_map=semantic_map,
            language_percept=language_percept,
            relationship_timeline=refreshed_relationship_timeline,
            commitment_truth_state=commitment_truth_state,
            context_accumulation=updated_context_accumulation,
            relation_scope_index=relation_scope_index,
            shared_term_registry=refreshed_shared_term_registry
            or existing_shared_term_registry,
            relationship_stage=relationship_subject.get("relationship_stage"),
            generated_at=generated_at,
        )
        write_json(language_dir / "semantic_map_frame.json", semantic_map)
    ref_consistency_profile = project_language_relationship_ref_consistency_profile(
        generated_at=generated_at,
        language_percept=language_percept or {},
        semantic_map=semantic_map or {},
        relation_scope_index=relation_scope_index or {},
        shared_term_registry=refreshed_shared_term_registry
        or existing_shared_term_registry
        or {},
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        self_model_state=evolved_self_model_state,
        inner_speech=_read_json_if_exists(language_dir / "inner_speech_frame.json"),
        expression_plan=expression_plan,
    )
    write_json(
        language_dir / "language_relationship_ref_consistency.json",
        ref_consistency_profile,
    )
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
        "expression_plan": refreshed_expression_plan,
        "apology_repair_language_trace": refreshed_apology_repair_language_trace,
        "relationship_memory": refreshed_relationship_memory,
        "state_merge_guard": refreshed_state_merge_guard,
        "autobiographical_stack": refreshed_autobiographical_stack,
        "engram_index": refreshed_engram_index,
        "brain_graph": updated_brain_graph,
        "network_state": updated_network_state,
        "workspace_frame": updated_workspace_frame,
        "broadcast_frame": updated_broadcast_frame,
        "metacognition_state": updated_metacognition_state,
        "consciousness_probe_bundle": updated_consciousness_probe,
        "memory_write_gate": updated_memory_write_gate,
        "responsibility_loop_state": updated_responsibility_loop_state,
        "queue_e_world_contact_handoff_profile": updated_queue_e_handoff_profile,
        "context_accumulation_window": updated_context_accumulation,
        "turn_transition_trace": updated_turn_transition,
        "shared_term_registry": refreshed_shared_term_registry,
        "self_model_state": evolved_self_model_state,
        "life_state": refreshed_life_state,
        "memory_retrieval_frame": memory_retrieval_frame or {},
    }


def _live_queue_e_handoff_terminal_profile(
    continuity_refresh: dict[str, Any],
) -> dict[str, Any]:
    handoff = continuity_refresh.get("queue_e_world_contact_handoff_profile")
    if not isinstance(handoff, dict) or not handoff:
        return {}
    profile: dict[str, Any] = {
        "live_queue_e_world_contact_handoff_refreshed": True,
        "queue_e_world_contact_handoff_status": handoff.get("handoff_status"),
        "queue_e_world_contact_handoff_profile_ref": HANDOFF_PROFILE_REF,
        "queue_e_world_contact_repair_hold_required": handoff.get(
            "repair_hold_required"
        ),
        "queue_e_world_contact_confirmation_threshold_bias": handoff.get(
            "confirmation_threshold_bias"
        ),
        "queue_e_world_contact_future_release_posture": handoff.get(
            "future_release_posture"
        ),
        "queue_e_world_contact_body_pressure_profile_ref": handoff.get(
            "body_pressure_profile_ref"
        ),
        "queue_e_world_contact_blocked_future_routes": list(
            handoff.get("blocked_future_routes", [])
        ),
        "queue_e_world_contact_allowed_repair_routes": list(
            handoff.get("allowed_repair_routes", [])
        ),
        "queue_e_world_contact_repair_governance_refs": list(
            handoff.get("repair_governance_refs", [])
        ),
        "queue_e_world_contact_ref_set": _dedupe_refs(
            _string_list(handoff.get("ref_set"))
        ),
        "live_queue_e_world_contact_handoff_boundary": (
            handoff.get("handoff_boundary")
            or "queue_e_world_contact_handoff_live_turn_evidence_not_spoken_language"
        ),
    }
    if handoff.get("repair_hold_required") is True:
        profile["queue_e_world_contact_pressure_level"] = "elevated"
        profile["queue_e_world_contact_waiting_posture"] = (
            "world_contact_repair_handoff_hold_waiting"
        )
        profile["queue_e_world_contact_attention_target"] = (
            "world_contact_validation_schema_handoff"
        )
    live_turn_focus = handoff.get("live_turn_focus")
    if live_turn_focus:
        profile["live_turn_focus"] = live_turn_focus
    live_responsibility_refs = _string_list(
        handoff.get("live_responsibility_consciousness_context_refs")
    )
    if live_responsibility_refs:
        profile["live_responsibility_consciousness_context_refs"] = (
            live_responsibility_refs
        )
    if profile.get("queue_e_world_contact_ref_set"):
        profile["queue_e_world_contact_handoff_refs"] = profile[
            "queue_e_world_contact_ref_set"
        ]
    return profile


def _merge_live_queue_e_handoff_into_lineage_state(
    terminal_life_loop_state: dict[str, Any],
    *,
    live_queue_e_handoff_profile: dict[str, Any],
    handoff_profile: Any,
) -> None:
    lineage_state = terminal_life_loop_state.get("resident_background_lineage_state")
    if not isinstance(lineage_state, dict):
        lineage_state = {}
    handoff_presence = lineage_state.get("world_contact_handoff_presence")
    if not isinstance(handoff_presence, dict):
        handoff_presence = {}
    refreshed_profile = (
        handoff_profile if isinstance(handoff_profile, dict) else {}
    )
    merged_presence = dict(handoff_presence)
    for key, value in (
        ("handoff_status", live_queue_e_handoff_profile.get("queue_e_world_contact_handoff_status")),
        ("profile_ref", live_queue_e_handoff_profile.get("queue_e_world_contact_handoff_profile_ref")),
        ("repair_hold_required", live_queue_e_handoff_profile.get("queue_e_world_contact_repair_hold_required")),
        (
            "confirmation_threshold_bias",
            live_queue_e_handoff_profile.get("queue_e_world_contact_confirmation_threshold_bias"),
        ),
        (
            "future_release_posture",
            live_queue_e_handoff_profile.get("queue_e_world_contact_future_release_posture"),
        ),
        (
            "body_pressure_profile_ref",
            live_queue_e_handoff_profile.get("queue_e_world_contact_body_pressure_profile_ref"),
        ),
        (
            "waiting_posture",
            live_queue_e_handoff_profile.get("queue_e_world_contact_waiting_posture"),
        ),
        (
            "attention_target",
            live_queue_e_handoff_profile.get("queue_e_world_contact_attention_target"),
        ),
        (
            "pressure_level",
            live_queue_e_handoff_profile.get("queue_e_world_contact_pressure_level"),
        ),
        ("live_turn_focus", live_queue_e_handoff_profile.get("live_turn_focus") or refreshed_profile.get("live_turn_focus")),
        (
            "handoff_boundary",
            live_queue_e_handoff_profile.get("live_queue_e_world_contact_handoff_boundary")
            or refreshed_profile.get("handoff_boundary"),
        ),
        (
            "last_projected_from_live_turn_ref",
            refreshed_profile.get("last_projected_from_live_turn_ref"),
        ),
    ):
        if value not in {None, ""}:
            merged_presence[key] = value
    merged_presence["live_queue_e_world_contact_handoff_refreshed"] = True
    live_responsibility_refs = _dedupe_refs(
        _string_list(live_queue_e_handoff_profile.get("live_responsibility_consciousness_context_refs"))
        + _string_list(refreshed_profile.get("live_responsibility_consciousness_context_refs"))
    )
    if live_responsibility_refs:
        merged_presence["live_responsibility_consciousness_context_refs"] = (
            live_responsibility_refs
        )
    ref_set = _dedupe_refs(
        _string_list(merged_presence.get("ref_set"))
        + _string_list(live_queue_e_handoff_profile.get("queue_e_world_contact_ref_set"))
        + live_responsibility_refs
    )
    if ref_set:
        merged_presence["ref_set"] = ref_set
    if refreshed_profile:
        merged_presence["queue_e_world_contact_handoff_profile"] = refreshed_profile
    lineage_state["world_contact_handoff_presence"] = merged_presence
    terminal_life_loop_state["resident_background_lineage_state"] = lineage_state


def _apply_live_queue_e_handoff_lineage_fields(
    payload: dict[str, Any],
    *,
    queue_e_world_contact_handoff_payload: dict[str, Any],
    live_queue_e_handoff_profile: dict[str, Any],
) -> None:
    handoff_refs = _dedupe_refs(
        list(queue_e_world_contact_handoff_payload.get("queue_e_world_contact_handoff_refs") or [])
        or _string_list(live_queue_e_handoff_profile.get("queue_e_world_contact_ref_set"))
    )
    if handoff_refs:
        payload["resident_background_lineage_world_contact_handoff_refs"] = handoff_refs
        payload["queue_e_world_contact_handoff_refs"] = handoff_refs
    payload["resident_background_lineage_live_queue_e_world_contact_handoff_refreshed"] = True
    live_responsibility_refs = _dedupe_refs(
        _string_list(
            queue_e_world_contact_handoff_payload.get(
                "live_responsibility_consciousness_context_refs"
            )
        )
        or _string_list(
            live_queue_e_handoff_profile.get("live_responsibility_consciousness_context_refs")
        )
    )
    if live_responsibility_refs:
        payload[
            "resident_background_lineage_live_responsibility_consciousness_context_refs"
        ] = live_responsibility_refs
        payload["live_responsibility_consciousness_context_refs"] = (
            live_responsibility_refs
        )
    live_turn_focus = (
        queue_e_world_contact_handoff_payload.get("live_turn_focus")
        or live_queue_e_handoff_profile.get("live_turn_focus")
    )
    if live_turn_focus:
        payload["resident_background_lineage_world_contact_live_turn_focus"] = (
            str(live_turn_focus)
        )
        payload["live_turn_focus"] = str(live_turn_focus)
    handoff_boundary = (
        queue_e_world_contact_handoff_payload.get(
            "live_queue_e_world_contact_handoff_boundary"
        )
        or live_queue_e_handoff_profile.get("live_queue_e_world_contact_handoff_boundary")
    )
    if handoff_boundary:
        payload["resident_background_lineage_world_contact_handoff_boundary"] = str(
            handoff_boundary
        )
        payload["live_queue_e_world_contact_handoff_boundary"] = str(handoff_boundary)


def _apply_live_consciousness_lineage_fields(
    payload: dict[str, Any],
    *,
    prediction_write_gate_payload: dict[str, Any],
    live_consciousness_chain_profile: dict[str, Any],
) -> None:
    consciousness_refs = _dedupe_refs(
        list(
            prediction_write_gate_payload.get("consciousness_write_context_refs")
            or []
        )
        or _string_list(
            live_consciousness_chain_profile.get("consciousness_write_context_refs")
        )
    )
    if consciousness_refs:
        payload["resident_background_lineage_consciousness_write_context_refs"] = (
            consciousness_refs
        )
        payload["consciousness_write_context_refs"] = consciousness_refs
        payload["resident_background_lineage_consciousness_write_context_ref_count"] = (
            len(consciousness_refs)
        )
        payload["consciousness_write_context_ref_count"] = len(consciousness_refs)
    field_map = (
        (
            "consciousness_write_context_bias",
            "resident_background_lineage_consciousness_write_context_bias",
        ),
        (
            "consciousness_write_context_workspace_candidate_count",
            "resident_background_lineage_consciousness_write_context_workspace_candidate_count",
        ),
        (
            "consciousness_write_context_broadcast_target_count",
            "resident_background_lineage_consciousness_write_context_broadcast_target_count",
        ),
        (
            "consciousness_write_context_reportability_flag_count",
            "resident_background_lineage_consciousness_write_context_reportability_flag_count",
        ),
        (
            "consciousness_write_context_boundary",
            "resident_background_lineage_consciousness_write_context_boundary",
        ),
    )
    for source_key, target_key in field_map:
        value = prediction_write_gate_payload.get(source_key)
        if value in {None, ""}:
            value = live_consciousness_chain_profile.get(source_key)
        if value not in {None, ""}:
            payload[source_key] = value
            payload[target_key] = value
    adjustments = _dedupe_refs(
        list(
            prediction_write_gate_payload.get(
                "consciousness_write_context_candidate_gate_adjustments"
            )
            or []
        )
    )
    if adjustments:
        payload["consciousness_write_context_candidate_gate_adjustments"] = adjustments
        payload[
            "resident_background_lineage_consciousness_write_context_candidate_gate_adjustments"
        ] = adjustments


def _live_shared_term_promotion_profile(
    continuity_refresh: dict[str, Any],
) -> dict[str, Any]:
    shared_term_registry = continuity_refresh.get("shared_term_registry")
    if not isinstance(shared_term_registry, dict) or not shared_term_registry:
        return {}
    return {
        "live_shared_term_promotion_refreshed": True,
        "shared_term_registry_ref": SHARED_TERM_REGISTRY_REF,
        "live_shared_term_promotion_count": len(
            [
                term
                for term in shared_term_registry.get("shared_terms", [])
                if isinstance(term, dict)
                and term.get("promotion_gate_status")
                in {"promoted", "seed", "seed_reinforced"}
            ]
        ),
        "live_shared_term_promotion_candidate_count": int(
            shared_term_registry.get("shared_term_promotion_candidate_count", 0)
        ),
        "live_shared_term_promotion_relation_scope": shared_term_registry.get(
            "shared_term_promotion_relation_scope"
        ),
        "live_shared_term_promotion_dialogue_turn_count": int(
            shared_term_registry.get("shared_term_promotion_dialogue_turn_count", 0)
        ),
        "live_shared_term_promotion_boundary": (
            shared_term_registry.get("shared_term_promotion_boundary")
            or "structured_shared_term_promotion_not_spoken_language"
        ),
    }


def _live_context_accumulation_profile(
    continuity_refresh: dict[str, Any],
) -> dict[str, Any]:
    context_accumulation = continuity_refresh.get("context_accumulation_window")
    if not isinstance(context_accumulation, dict) or not context_accumulation:
        return {}
    return {
        "live_context_accumulation_refreshed": True,
        "context_accumulation_ref": CONTEXT_ACCUMULATION_WINDOW_REF,
        "turn_transition_ref": TURN_TRANSITION_TRACE_REF,
        "live_context_accumulation_semantic_focus": context_accumulation.get(
            "semantic_focus"
        ),
        "live_context_accumulation_dialogue_turn_restore_ref_count": len(
            list(context_accumulation.get("dialogue_turn_restore_refs", []))
        ),
        "live_context_accumulation_shared_term_surface_count": len(
            list(context_accumulation.get("shared_term_surfaces", []))
        ),
        "live_context_accumulation_boundary": (
            "live_context_accumulation_structured_evidence_not_spoken_language"
        ),
    }


def _live_consciousness_chain_profile(
    continuity_refresh: dict[str, Any],
) -> dict[str, Any]:
    memory_write_gate = continuity_refresh.get("memory_write_gate")
    if not isinstance(memory_write_gate, dict):
        memory_write_gate = {}
    consciousness_context = memory_write_gate.get("consciousness_write_context")
    if not isinstance(consciousness_context, dict):
        consciousness_context = {}
    broadcast_frame = continuity_refresh.get("broadcast_frame")
    if not isinstance(broadcast_frame, dict):
        broadcast_frame = {}
    metacognition_state = continuity_refresh.get("metacognition_state")
    if not isinstance(metacognition_state, dict):
        metacognition_state = {}
    consciousness_probe = continuity_refresh.get("consciousness_probe_bundle")
    if not isinstance(consciousness_probe, dict):
        consciousness_probe = {}

    profile: dict[str, Any] = {
        "live_consciousness_chain_refreshed": True,
        "last_workspace_frame_ref": WORKSPACE_FRAME_REF,
        "last_broadcast_frame_ref": BROADCAST_FRAME_REF,
        "last_metacognition_ref": METACOGNITION_STATE_REF,
        "last_consciousness_probe_ref": CONSCIOUSNESS_PROBE_REF,
        "last_memory_write_gate_consciousness_context_ref": (
            MEMORY_WRITE_GATE_CONSCIOUSNESS_CONTEXT_REF
        ),
        "live_broadcast_target_count": len(
            list(broadcast_frame.get("broadcast_targets", []))
        ),
        "live_metacognition_uncertainty_count": len(
            list(metacognition_state.get("uncertainty_flags", []))
        ),
        "live_consciousness_probe_reportability_flag_count": len(
            list(consciousness_probe.get("reportability_flags", []))
        ),
        "live_consciousness_chain_boundary": (
            "live_consciousness_chain_structured_evidence_not_spoken_language"
        ),
    }
    live_turn_focus = (
        broadcast_frame.get("live_turn_focus")
        or metacognition_state.get("live_turn_focus")
        or consciousness_probe.get("live_turn_focus")
    )
    if live_turn_focus:
        profile["live_turn_focus"] = live_turn_focus
    if consciousness_context:
        profile["consciousness_write_context_refs"] = _dedupe_refs(
            _string_list(consciousness_context.get("ref_set"))
        )
        profile["consciousness_write_context_ref_count"] = len(
            profile["consciousness_write_context_refs"]
        )
        profile["consciousness_write_context_workspace_candidate_count"] = (
            consciousness_context.get("workspace_candidate_count")
        )
        profile["consciousness_write_context_broadcast_target_count"] = (
            consciousness_context.get("broadcast_target_count")
        )
        profile["consciousness_write_context_reportability_flag_count"] = (
            consciousness_context.get("reportability_flag_count")
        )
        profile["consciousness_write_context_bias"] = consciousness_context.get(
            "write_attention_bias"
        )
        profile["consciousness_write_context_candidate_gate_adjustments"] = (
            consciousness_context.get("candidate_gate_adjustments")
        )
        profile["consciousness_write_context_boundary"] = consciousness_context.get(
            "boundary"
        )
    return profile


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _continuity_background_profile_for_evolution(
    background_continuity_profile: Any,
    resident_background_lineage_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    profile = (
        dict(background_continuity_profile)
        if isinstance(background_continuity_profile, dict)
        else {}
    )
    lineage_payload = (
        resident_background_lineage_payload
        if isinstance(resident_background_lineage_payload, dict)
        else {}
    )
    if (
        lineage_payload.get("resident_background_lineage_schema_version")
        or lineage_payload.get("resident_background_lineage_generation") is not None
    ):
        profile.setdefault("background_continuity_mode", "closed_process_carryover")
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_self_modification_pressure_level",
        target_key="background_growth_self_modification_pressure_level",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_self_modification_attention_target",
        target_key="background_growth_self_modification_attention_target",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_self_modification_waiting_posture",
        target_key="background_growth_self_modification_waiting_posture",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_self_modification_boundary",
        target_key="background_growth_self_modification_boundary",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_active_domain_count",
        target_key="background_growth_active_domain_count",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_pressure_count",
        target_key="background_growth_pressure_count",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_patch_candidate_count",
        target_key="background_growth_patch_candidate_count",
    )
    _copy_if_present(
        profile,
        lineage_payload,
        source_key="resident_background_lineage_growth_archive_receipt_count",
        target_key="background_growth_archive_receipt_count",
    )
    growth_presence = lineage_payload.get(
        "resident_background_lineage_growth_self_modification_presence"
    )
    if isinstance(growth_presence, dict) and growth_presence:
        profile["background_growth_self_modification_presence"] = dict(growth_presence)
    growth_refs = _dedupe_refs(
        _string_list(
            lineage_payload.get("resident_background_lineage_growth_self_modification_refs")
        )
    )
    growth_state_refs = _dedupe_refs(
        _string_list(
            lineage_payload.get(
                "resident_background_lineage_growth_self_modification_state_refs"
            )
        )
    )
    growth_learning_plan_refs = _dedupe_refs(
        _string_list(
            lineage_payload.get(
                "resident_background_lineage_growth_learning_plan_refs"
            )
        )
    )
    if growth_refs:
        profile["background_growth_self_modification_ref_set"] = growth_refs
    if growth_state_refs:
        profile["background_growth_self_modification_state_refs"] = growth_state_refs
    if growth_learning_plan_refs:
        profile["background_growth_learning_plan_refs"] = growth_learning_plan_refs
    return profile


def _copy_if_present(
    target: dict[str, Any],
    source: dict[str, Any],
    *,
    source_key: str,
    target_key: str,
) -> None:
    value = source.get(source_key)
    if value not in (None, "", [], {}):
        target[target_key] = value


def _dedupe_refs(refs: list[str | None]) -> list[str]:
    result: list[str] = []
    for ref in refs:
        if ref and ref not in result:
            result.append(ref)
    return result


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]
