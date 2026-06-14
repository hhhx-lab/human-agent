from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STATE_INSPECTION_CATEGORIES = {
    "state",
    "context",
    "memory",
    "dream",
    "body",
    "emotion",
    "inner_environment",
    "relationship",
    "language",
    "cognition",
    "consciousness",
    "thinking",
    "personality",
    "ability",
    "perception",
    "proactive_voice",
}


def build_resident_state_inspection(
    *,
    terminal_dir: Path,
    category: str,
) -> dict[str, Any]:
    normalized = _normalize_category(category)
    state_root = terminal_dir.parent
    reports_dir = state_root.parent / "reports" / "latest"
    payload = {
        "schema_version": "resident_state_inspection_v0",
        "category": normalized,
        "available_categories": sorted(STATE_INSPECTION_CATEGORIES),
        "inspection_scope": "terminal_view_only_not_relation_turn",
    }
    if normalized == "state":
        payload["state"] = _collect_state_summary(
            terminal_dir=terminal_dir,
            reports_dir=reports_dir,
        )
    elif normalized == "context":
        context = _collect_files(
            state_root,
            {
                "life_context_frame": "terminal/life_context_frame.json",
                "relation_turn_frame": "terminal/relation_turn_frame.json",
                "language_percept": "language/language_percept_frame.json",
                "relationship_timeline": "relationship/relationship_timeline.json",
                "dialogue_memory_summary": "memory/dialogue_memory_summary.json",
            },
        )
        context["relation_context_summary"] = _collect_relation_context_summary(
            context
        )
        payload["context"] = context
    elif normalized == "memory":
        memory = _collect_files(
            state_root,
            {
                "relationship_memory": "memory/relationship_memory.json",
                "dialogue_memory_summary": "memory/dialogue_memory_summary.json",
                "engram_index": "memory/engram_index.json",
                "autobiographical_stack": "self/autobiographical_stack.json",
                "memory_retrieval": "memory/memory_retrieval_frame.json",
                "memory_write_gate": "memory/memory_write_gate.json",
                "state_merge_guard": "memory/state_merge_guard.json",
                "life_state": "life_state.json",
            },
        )
        payload["memory"] = memory
        payload["memory"]["tiering"] = _collect_memory_tiering(memory)
        payload["memory"]["tier_summary"] = _collect_memory_tier_summary(memory)
        payload["memory"]["reconstructive_memory_summary"] = (
            _collect_reconstructive_memory_summary(memory)
        )
    elif normalized == "dream":
        dream = _collect_files(
            state_root,
            {
                "offline_entry_gate": "dream/offline_entry_gate.json",
                "exit_dream_consolidation_summary": (
                    "dream/exit_dream_consolidation_summary.json"
                ),
                "dream_experience_window": "dream/dream_experience_window.json",
                "wake_integration_frame": "dream/wake_integration_frame.json",
                "dream_fact_gate_decision": "dream/dream_fact_gate_decision.json",
                "nightmare_loop_risk": "dream/nightmare_loop_risk.json",
                "web_dream_learning_state": "dream/web_dream_learning_state.json",
                "offline_learning_cumulative_profile": (
                    "growth/offline_learning_cumulative_profile.json"
                ),
                "resident_sleep_cycle_state": (
                    "terminal/resident_sleep_cycle_state.json"
                ),
            },
        )
        payload["dream"] = dream
        payload["dream"]["memory_tiering"] = _collect_memory_tiering(dream)
        payload["dream"]["tier_summary"] = _collect_memory_tier_summary(dream)
        payload["dream"]["dream_wake_fact_summary"] = (
            _collect_dream_wake_fact_summary(dream)
        )
    elif normalized == "body":
        body = _collect_files(
            state_root,
            {
                "body_rhythm_pulse": "body/body_rhythm_pulse.json",
                "need_state_vector": "body/need_state_vector.json",
                "body_resource_budget": "body/body_resource_budget.json",
                "core_affect_vector": "body/core_affect_vector.json",
                "signal_media_runtime": "signal/signal_media_runtime.json",
                "idle_strategy": "terminal/idle_strategy_state.json",
            },
        )
        body["body_grounding_summary"] = _collect_body_grounding_summary(body)
        payload["body"] = body
    elif normalized == "emotion":
        emotion = _collect_files(
            state_root,
            {
                "core_affect_vector": "body/core_affect_vector.json",
                "affective_episode": "body/affective_episode.json",
                "emotion_regulation_loop": "body/emotion_regulation_loop.json",
                "body_resource_budget": "body/body_resource_budget.json",
                "pain_regret_repair_report": (
                    "../reports/latest/pain_regret_repair_report.json"
                ),
                "signal_media_runtime": "signal/signal_media_runtime.json",
            },
        )
        emotion["emotion_regulation_summary"] = (
            _collect_emotion_regulation_summary(emotion)
        )
        payload["emotion"] = emotion
    elif normalized == "inner_environment":
        inner_environment = _collect_files(
            state_root,
            {
                "need_state_vector": "body/need_state_vector.json",
                "body_resource_budget": "body/body_resource_budget.json",
                "body_rhythm_pulse": "body/body_rhythm_pulse.json",
                "signal_media_runtime": "signal/signal_media_runtime.json",
                "idle_strategy": "terminal/idle_strategy_state.json",
            },
        )
        inner_environment["modulation_summary"] = (
            _collect_inner_environment_modulation_summary(inner_environment)
        )
        payload["inner_environment"] = inner_environment
    elif normalized == "relationship":
        relationship = _collect_files(
            state_root,
            {
                "relationship_subject_graph": (
                    "relationship/relationship_subject_graph.json"
                ),
                "relationship_timeline": "relationship/relationship_timeline.json",
                "commitment_truth_state": "relationship/commitment_truth_state.json",
                "commitment_expression_plan": (
                    "language/commitment_expression_plan.json"
                ),
                "apology_repair_language_trace": (
                    "language/apology_repair_language_trace.json"
                ),
            },
        )
        relationship["continuity_summary"] = (
            _collect_relationship_continuity_summary(relationship)
        )
        payload["relationship"] = relationship
    elif normalized == "language":
        language = _collect_files(
            state_root,
            {
                "language_percept": "language/language_percept_frame.json",
                "semantic_map": "language/semantic_map_frame.json",
                "inner_speech": "language/inner_speech_frame.json",
                "expression_monitor": "language/expression_monitor_state.json",
                "expression_plan": "language/expression_plan.json",
                "model_expression_state": "language/model_expression_state.json",
                "relationship_memory": "memory/relationship_memory.json",
                "dialogue_memory_summary": "memory/dialogue_memory_summary.json",
                "memory_retrieval": "memory/memory_retrieval_frame.json",
                "exit_dream_consolidation_summary": (
                    "dream/exit_dream_consolidation_summary.json"
                ),
                "core_affect_vector": "body/core_affect_vector.json",
                "body_resource_budget": "body/body_resource_budget.json",
                "signal_media_runtime": "signal/signal_media_runtime.json",
                "relationship_timeline": "relationship/relationship_timeline.json",
                "commitment_truth_state": "relationship/commitment_truth_state.json",
                "responsibility_loop_state": (
                    "action/responsibility_loop_state.json"
                ),
                "pain_regret_repair_report": (
                    "../reports/latest/pain_regret_repair_report.json"
                ),
                "belief_state_frame": "prediction/belief_state_frame.json",
                "prediction_error_field": "prediction/prediction_error_field.json",
                "active_sampling_plan": "prediction/active_sampling_plan.json",
                "resident_autonomous_activity": (
                    "terminal/resident_autonomous_activity_state.json"
                ),
                "proactive_state": "terminal/resident_terminal_proactive_state.json",
            },
        )
        language["generation_consumption_summary"] = (
            _collect_language_generation_consumption_summary(language)
        )
        payload["language"] = language
    elif normalized == "cognition":
        cognition = _collect_files(
            state_root,
            {
                "workspace_frame": "consciousness/workspace_frame.json",
                "broadcast_frame": "consciousness/broadcast_frame.json",
                "metacognition_state": "consciousness/metacognition_state.json",
                "belief_state_frame": "prediction/belief_state_frame.json",
                "prediction_error_field": "prediction/prediction_error_field.json",
                "active_sampling_plan": "prediction/active_sampling_plan.json",
                "memory_write_gate": "memory/memory_write_gate.json",
                "state_merge_guard": "memory/state_merge_guard.json",
            },
        )
        cognition["workspace_summary"] = _collect_cognitive_workspace_summary(
            cognition
        )
        payload["cognition"] = cognition
    elif normalized == "consciousness":
        consciousness = _collect_files(
            state_root,
            {
                "workspace_frame": "consciousness/workspace_frame.json",
                "broadcast_frame": "consciousness/broadcast_frame.json",
                "metacognition_state": "consciousness/metacognition_state.json",
                "consciousness_probe": (
                    "consciousness/consciousness_probe_bundle.json"
                ),
                "birth_readiness_rollup": (
                    "life_targets/birth_readiness_rollup.json"
                ),
                "birth_readiness_stage_gate": (
                    "life_targets/birth_readiness_stage_gate.json"
                ),
                "terminal_life_loop": "terminal/terminal_life_loop_state.json",
                "resident_governance": "terminal/resident_governance_state.json",
            },
        )
        consciousness["reportability_summary"] = (
            _collect_consciousness_reportability_summary(consciousness)
        )
        payload["consciousness"] = consciousness
    elif normalized == "thinking":
        thinking = _collect_files(
            state_root,
            {
                "resident_self_thinking": (
                    "self/resident_self_thinking_state.json"
                ),
                "self_model": "self/self_model.json",
                "inner_speech": "language/inner_speech_frame.json",
                "consciousness_probe": (
                    "consciousness/consciousness_probe_bundle.json"
                ),
                "background_convergence_summary": (
                    "terminal/background_convergence_summary.json"
                ),
                "background_convergence_history": (
                    "terminal/background_convergence_history.json"
                ),
                "resident_autonomous_activity": (
                    "terminal/resident_autonomous_activity_state.json"
                ),
            },
        )
        thinking["self_thinking_summary"] = _collect_self_thinking_summary(
            thinking
        )
        payload["thinking"] = thinking
    elif normalized == "personality":
        personality = _collect_files(
            state_root,
            {
                "self_model": "self/self_model.json",
                "autobiographical_stack": "self/autobiographical_stack.json",
                "trait_drift_monitor": "body/trait_drift_monitor.json",
                "background_convergence_summary": (
                    "terminal/background_convergence_summary.json"
                ),
                "background_convergence_history": (
                    "terminal/background_convergence_history.json"
                ),
            },
        )
        personality["convergence_summary"] = (
            _collect_personality_convergence_summary(personality)
        )
        payload["personality"] = personality
    elif normalized == "ability":
        ability = _collect_files(
            state_root,
            {
                "birth_readiness_rollup": (
                    "life_targets/birth_readiness_rollup.json"
                ),
                "birth_readiness_stage_gate": (
                    "life_targets/birth_readiness_stage_gate.json"
                ),
                "live0_acceptance_audit": (
                    "../reports/latest/live0_acceptance_audit_report.json"
                ),
                "v0_contract_file_index": "contracts/v0_contract_file_index.json",
            },
        )
        ability["birth_readiness_summary"] = (
            _collect_ability_birth_readiness_summary(ability)
        )
        payload["ability"] = ability
    elif normalized == "perception":
        perception = _collect_files(
            state_root,
            {
                "visual_observation_frame": (
                    "perception/visual_observation_frame.json"
                ),
                "world_contact_summary": "membrane/world_contact_summary.json",
                "belief_state_frame": "prediction/belief_state_frame.json",
                "prediction_workspace_frame": (
                    "prediction/prediction_workspace_frame.json"
                ),
                "active_sampling_plan": "prediction/active_sampling_plan.json",
            },
        )
        perception["world_contact_summary_view"] = (
            _collect_perception_world_contact_summary(perception)
        )
        payload["perception"] = perception
    elif normalized == "proactive_voice":
        proactive_voice = _collect_files(
            state_root,
            {
                "proactive_state": "terminal/resident_terminal_proactive_state.json",
                "proactive_events": "terminal/resident_terminal_proactive_events.jsonl",
            },
        )
        proactive_voice["coverage_summary"] = _collect_proactive_voice_summary(
            proactive_voice
        )
        payload["proactive_voice"] = proactive_voice
    return payload


def _collect_state_summary(
    *,
    terminal_dir: Path,
    reports_dir: Path,
) -> dict[str, Any]:
    state = {
        "resident_lifecycle": _compact_json(
            terminal_dir / "resident_lifecycle_state.json"
        ),
        "relation_queue": _compact_json(
            terminal_dir / "resident_relation_queue_state.json"
        ),
        "autonomous_activity": _compact_json(
            terminal_dir / "resident_autonomous_activity_state.json"
        ),
        "idle_strategy": _compact_json(terminal_dir / "idle_strategy_state.json"),
        "resident_governance": _compact_json(
            terminal_dir / "resident_governance_state.json"
        ),
        "terminal_life_loop": _compact_json(
            terminal_dir / "terminal_life_loop_state.json"
        ),
        "terminal_input_profile": _compact_json(
            terminal_dir / "terminal_input_profile.json"
        ),
        "waiting_heartbeat": _compact_json(
            reports_dir / "digital_life_waiting_heartbeat.json"
        ),
    }
    state["resident_continuity_summary"] = _collect_resident_continuity_summary(
        state
    )
    return state


def _collect_resident_continuity_summary(section: dict[str, Any]) -> dict[str, Any]:
    lifecycle = _extract_compact_value(section.get("resident_lifecycle", {}))
    relation_queue = _extract_compact_value(section.get("relation_queue", {}))
    autonomous_activity = _extract_compact_value(
        section.get("autonomous_activity", {})
    )
    idle_strategy = _extract_compact_value(section.get("idle_strategy", {}))
    governance = _extract_compact_value(section.get("resident_governance", {}))
    terminal_loop = _extract_compact_value(section.get("terminal_life_loop", {}))
    input_profile = _extract_compact_value(
        section.get("terminal_input_profile", {})
    )
    heartbeat = _extract_compact_value(section.get("waiting_heartbeat", {}))
    lineage = _extract_nested_value(
        terminal_loop,
        "resident_background_lineage_state",
    )
    world_contact_presence = _extract_nested_value(
        lineage,
        "world_contact_handoff_presence",
    )
    identity_birth_presence = _extract_nested_value(
        lineage,
        "identity_consciousness_birth_presence",
    )
    domain_presence = {
        "resident_lifecycle": bool(lifecycle),
        "relation_queue": bool(relation_queue),
        "autonomous_activity": bool(autonomous_activity),
        "idle_strategy": bool(idle_strategy),
        "resident_governance": bool(governance),
        "terminal_life_loop": bool(terminal_loop),
        "terminal_input_profile": bool(input_profile),
        "waiting_heartbeat": bool(heartbeat),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "resident_continuity_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "lifecycle_status": lifecycle.get("status"),
        "lifecycle_phase": lifecycle.get("phase"),
        "life_name": lifecycle.get("life_name"),
        "pid_present": bool(lifecycle.get("pid")),
        "relation_queue_status": relation_queue.get("status"),
        "pending_relation_turn_count": _first_non_empty(
            relation_queue.get("pending_relation_turn_count"),
            _count_any(relation_queue.get("pending_relation_turn_refs")),
        ),
        "autonomous_activity_status": autonomous_activity.get("status"),
        "autonomous_activity_count": autonomous_activity.get("activity_count"),
        "autonomous_cycle_phase_index": autonomous_activity.get(
            "cycle_phase_index"
        ),
        "autonomous_cycle_phase_count": autonomous_activity.get(
            "cycle_phase_count"
        ),
        "last_autonomous_activity_kind": autonomous_activity.get(
            "last_activity_kind"
        ),
        "governance_phase": governance.get("governance_phase"),
        "waiting_mode": _first_non_empty(
            governance.get("waiting_mode"),
            heartbeat.get("waiting_mode"),
            terminal_loop.get("current_mode"),
        ),
        "next_required_action": _first_non_empty(
            governance.get("next_required_action"),
            heartbeat.get("next_required_action"),
            idle_strategy.get("next_idle_action"),
        ),
        "idle_waiting_posture": idle_strategy.get("waiting_posture"),
        "heartbeat_counter": heartbeat.get("heartbeat_counter"),
        "heartbeat_interval_ms": idle_strategy.get("heartbeat_interval_ms"),
        "terminal_current_mode": terminal_loop.get("current_mode"),
        "previous_live_turn_handoff_status": terminal_loop.get(
            "previous_live_turn_waiting_handoff_carry_status"
        ),
        "input_mode": input_profile.get("input_mode"),
        "line_editing_refs": _tier_refs(
            _extract_nested_value(input_profile, "line_editing"),
            [
                "backspace",
                "ctrl_u",
                "ctrl_d",
                "ctrl_c",
                "escape_sequence_policy",
            ],
        ),
        "lineage_ref_count": _count_any(
            lineage.get("resident_background_lineage_refs")
        ),
        "world_contact_handoff_status": world_contact_presence.get(
            "handoff_status"
        ),
        "world_contact_repair_hold_required": bool(
            world_contact_presence.get("repair_hold_required")
        ),
        "birth_readiness_waiting_posture": identity_birth_presence.get(
            "birth_readiness_waiting_posture"
        ),
        "governance_attention_target": idle_strategy.get(
            "governance_attention_target"
        ),
        "governance_attention_reason": idle_strategy.get(
            "governance_attention_reason"
        ),
        "state_boundary": (
            "resident_state_summary_is_inspection_not_life_speech"
        ),
    }


def _collect_files(root: Path, file_map: dict[str, str]) -> dict[str, Any]:
    collected: dict[str, Any] = {}
    for key, relative in file_map.items():
        collected[key] = _compact_json(root / relative)
    return collected


def _compact_json(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not payload:
        return {"available": False, "path": _runtime_ref(path)}
    return {
        "available": True,
        "path": _runtime_ref(path),
        "value": _compact_value(payload),
    }


def _compact_value(value: Any, *, depth: int = 0) -> Any:
    if depth >= 4:
        if isinstance(value, dict):
            return {"truncated": True, "keys": sorted(str(key) for key in value)[:12]}
        if isinstance(value, list):
            return {"truncated": True, "count": len(value)}
        return value
    if isinstance(value, dict):
        return {
            str(key): _compact_value(item, depth=depth + 1)
            for key, item in list(value.items())[:32]
        }
    if isinstance(value, list):
        return [_compact_value(item, depth=depth + 1) for item in value[:12]]
    return value


def _collect_memory_tiering(section: dict[str, Any]) -> dict[str, Any]:
    relationship_memory = _extract_compact_value(
        section.get("relationship_memory", {})
    )
    dialogue_memory_summary = _extract_compact_value(
        section.get("dialogue_memory_summary", {})
    )
    engram_index = _extract_compact_value(section.get("engram_index", {}))
    autobiographical_stack = _extract_compact_value(
        section.get("autobiographical_stack", {})
    )
    exit_summary = _extract_compact_value(
        section.get("exit_dream_consolidation_summary", {})
    )
    tiering = _extract_nested_value(exit_summary, "memory_tiering")
    return {
        "relationship_memory_tier_refs": _tier_refs(
            relationship_memory,
            [
                "salient_core_memory_refs",
                "retrievable_context_memory_refs",
                "deep_sediment_memory_refs",
            ],
        ),
        "dialogue_memory_tier_refs": _tier_refs(
            dialogue_memory_summary,
            [
                "deduplicated_episode_summaries",
                "memory_tiering",
            ],
        ),
        "engram_memory_tier_refs": _tier_refs(
            engram_index,
            [
                "memory_tier_index",
                "relationship_memory_refs",
                "dream_memory_refs",
                "autobiographical_memory_refs",
            ],
        ),
        "autobiographical_memory_refs": _tier_refs(
            autobiographical_stack,
            [
                "anchor_refs",
                "turn_refs",
                "narrative_refs",
            ],
        ),
        "exit_dream_memory_tiering": _tier_refs(
            tiering,
            [
                "salient_core_episode_refs",
                "retrievable_context_episode_refs",
                "deep_sediment_episode_refs",
            ],
        ),
    }


def _collect_memory_tier_summary(section: dict[str, Any]) -> dict[str, Any]:
    relationship_memory = _extract_compact_value(
        section.get("relationship_memory", {})
    )
    dialogue_memory_summary = _extract_compact_value(
        section.get("dialogue_memory_summary", {})
    )
    exit_summary = _extract_compact_value(
        section.get("exit_dream_consolidation_summary", {})
    )
    relationship_projection = _extract_nested_value(
        relationship_memory, "memory_tier_projection"
    )
    dialogue_tiering = _extract_nested_value(dialogue_memory_summary, "memory_tiering")
    exit_tiering = _extract_nested_value(exit_summary, "memory_tiering")
    relationship_profile = _extract_nested_value(
        relationship_memory, "relation_person_profile"
    )
    return {
        "relationship_memory_tier_projection_ref": _tier_refs(
            relationship_projection,
            [
                "schema_version",
                "salient_core_episode_refs",
                "retrievable_context_episode_refs",
                "deep_sediment_episode_refs",
                "projection_source_ref",
            ],
        ),
        "dialogue_memory_tiering_ref": _tier_refs(
            dialogue_tiering,
            [
                "schema_version",
                "tier_policy",
                "salient_core_episode_refs",
                "retrievable_context_episode_refs",
                "deep_sediment_episode_refs",
            ],
        ),
        "exit_dream_tiering_ref": _tier_refs(
            exit_tiering,
            [
                "schema_version",
                "tier_policy",
                "salient_core_episode_refs",
                "retrievable_context_episode_refs",
                "deep_sediment_episode_refs",
            ],
        ),
        "next_wake_cues": _tier_refs(
            relationship_memory,
            [
                "next_wake_cues",
            ],
        ),
        "relation_person_profile": _tier_refs(
            relationship_profile,
            [
                "schema_version",
                "observed_names",
                "preference_hypotheses",
                "personality_hypotheses",
                "relationship_stage_hint",
            ],
        ),
    }


def _collect_reconstructive_memory_summary(section: dict[str, Any]) -> dict[str, Any]:
    relationship_memory = _extract_compact_value(
        section.get("relationship_memory", {})
    )
    dialogue_memory_summary = _extract_compact_value(
        section.get("dialogue_memory_summary", {})
    )
    engram_index = _extract_compact_value(section.get("engram_index", {}))
    autobiographical_stack = _extract_compact_value(
        section.get("autobiographical_stack", {})
    )
    memory_retrieval = _extract_compact_value(section.get("memory_retrieval", {}))
    memory_write_gate = _extract_compact_value(section.get("memory_write_gate", {}))
    state_merge_guard = _extract_compact_value(section.get("state_merge_guard", {}))
    life_state = _extract_compact_value(section.get("life_state", {}))
    tiered_recall = _extract_nested_value(memory_retrieval, "tiered_recall")
    reconstruction_inputs = _extract_nested_value(
        memory_retrieval,
        "reconstruction_inputs",
    )
    body_signal_modulation = _extract_nested_value(
        memory_write_gate,
        "body_signal_write_modulation",
    )
    long_term_change_sources = _extract_nested_value(
        state_merge_guard,
        "long_term_change_sources",
    )
    life_memory_index = _extract_nested_value(life_state, "memory_index")
    domain_presence = {
        "relationship_memory": bool(relationship_memory),
        "dialogue_memory_summary": bool(dialogue_memory_summary),
        "engram_index": bool(engram_index),
        "autobiographical_stack": bool(autobiographical_stack),
        "memory_retrieval": bool(memory_retrieval),
        "memory_write_gate": bool(memory_write_gate),
        "state_merge_guard": bool(state_merge_guard),
        "life_state": bool(life_state),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "reconstructive_memory_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "retrieval_mode": memory_retrieval.get("retrieval_mode"),
        "cue_terms": _list_refs(memory_retrieval.get("cue_terms")),
        "cue_term_count": _count_any(memory_retrieval.get("cue_terms")),
        "activated_engram_ref_count": _count_any(
            memory_retrieval.get("activated_refs")
        )
        or _count_any(memory_retrieval.get("activated_engram_refs")),
        "tiered_recall_counts": {
            "salient_core": _count_any(
                tiered_recall.get("salient_core_refs")
            )
            or _count_any(tiered_recall.get("salient_core_episode_refs")),
            "retrievable_context": _count_any(
                tiered_recall.get("retrievable_context_refs")
            )
            or _count_any(
                tiered_recall.get("retrievable_context_episode_refs")
            ),
            "deep_sediment": _count_any(
                tiered_recall.get("deep_sediment_refs")
            )
            or _count_any(tiered_recall.get("deep_sediment_episode_refs")),
        },
        "reconstruction_focus": memory_retrieval.get("reconstruction_focus")
        or reconstruction_inputs.get("reconstruction_focus"),
        "relationship_hit_count": _count_any(
            memory_retrieval.get("relationship_memory_hits")
        ),
        "autobiographical_hit_count": _count_any(
            memory_retrieval.get("autobiographical_hits")
        ),
        "dream_residue_hit_count": _count_any(
            memory_retrieval.get("dream_residue_hits")
        ),
        "responsibility_hit_count": _count_any(
            memory_retrieval.get("responsibility_hits")
        ),
        "blocked_or_quarantined_ref_count": _count_any(
            memory_retrieval.get("blocked_or_quarantined_refs")
        )
        + _count_any(engram_index.get("quarantine_refs")),
        "write_gate_policy": memory_write_gate.get("stage_policy"),
        "write_gate_status": memory_write_gate.get("status"),
        "write_gate_bias": body_signal_modulation.get("write_bias"),
        "write_gate_adjustments": _list_refs(
            body_signal_modulation.get("candidate_gate_adjustments")
        ),
        "state_merge_policy": state_merge_guard.get("stage_policy"),
        "promotion_route_count": _count_any(
            state_merge_guard.get("promotion_routes")
        ),
        "quarantine_route_count": _count_any(
            state_merge_guard.get("quarantine_routes")
        ),
        "repair_route_count": _count_any(state_merge_guard.get("repair_routes")),
        "merge_route_count": _count_any(state_merge_guard.get("merge_routes")),
        "long_term_change_sources": _tier_refs(
            long_term_change_sources,
            [
                "prediction_error_resolution_refs",
                "offline_learning_writeback_refs",
                "offline_learning_cumulative_refs",
                "relationship_memory_repair_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_ref",
            ],
        ),
        "life_state_memory_index": _tier_refs(
            life_memory_index,
            [
                "memory_retrieval_refs",
                "state_merge_guard_refs",
                "engram_index_refs",
                "relationship_memory_refs",
                "replay_cues",
            ],
        ),
        "relationship_observed_names": _list_refs(
            _extract_nested_value(
                relationship_memory,
                "relation_person_profile",
            ).get("observed_names")
        ),
        "memory_boundary": (
            "cue_driven_reconstruction_write_gate_state_merge_not_raw_context_dump"
        ),
    }


def _collect_dream_wake_fact_summary(section: dict[str, Any]) -> dict[str, Any]:
    offline_entry = _extract_compact_value(section.get("offline_entry_gate", {}))
    exit_summary = _extract_compact_value(
        section.get("exit_dream_consolidation_summary", {})
    )
    dream_window = _extract_compact_value(
        section.get("dream_experience_window", {})
    )
    wake_integration = _extract_compact_value(
        section.get("wake_integration_frame", {})
    )
    dream_fact_gate = _extract_compact_value(
        section.get("dream_fact_gate_decision", {})
    )
    nightmare_risk = _extract_compact_value(section.get("nightmare_loop_risk", {}))
    web_dream_learning = _extract_compact_value(
        section.get("web_dream_learning_state", {})
    )
    offline_learning = _extract_compact_value(
        section.get("offline_learning_cumulative_profile", {})
    )
    resident_sleep = _extract_compact_value(
        section.get("resident_sleep_cycle_state", {})
    )
    memory_tiering = _extract_nested_value(exit_summary, "memory_tiering")
    repair_profile = _extract_nested_value(
        wake_integration,
        "queue_e_repair_modulation_profile",
    )
    if not repair_profile:
        repair_profile = _extract_nested_value(
            dream_window,
            "queue_e_repair_modulation_profile",
        )
    domain_presence = {
        "offline_entry_gate": bool(offline_entry),
        "exit_dream_consolidation_summary": bool(exit_summary),
        "dream_experience_window": bool(dream_window),
        "wake_integration_frame": bool(wake_integration),
        "dream_fact_gate_decision": bool(dream_fact_gate),
        "nightmare_loop_risk": bool(nightmare_risk),
        "web_dream_learning_state": bool(web_dream_learning),
        "offline_learning_cumulative_profile": bool(offline_learning),
        "resident_sleep_cycle_state": bool(resident_sleep),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "dream_wake_fact_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "offline_modes": _list_refs(offline_entry.get("offline_modes")),
        "sleep_phase": resident_sleep.get("phase")
        or resident_sleep.get("sleep_phase")
        or resident_sleep.get("current_phase"),
        "dream_window_id": dream_window.get("dream_window_id"),
        "dream_window_kind": dream_window.get("window_kind"),
        "dream_scene_count": _count_any(dream_window.get("dream_scene_frames")),
        "affective_themes": _list_refs(dream_window.get("affective_theme")),
        "source_trace_ref_count": _count_any(
            dream_window.get("source_trace_refs")
        ),
        "pain_residue_ref_count": _count_any(
            dream_window.get("pain_residue_refs")
        ),
        "relationship_simulation_ref_count": _count_any(
            dream_window.get("relationship_simulation_refs")
        ),
        "wake_integration_id": wake_integration.get("wake_integration_id"),
        "wake_archive_requirement": wake_integration.get("archive_requirement"),
        "wake_growth_seed_count": _count_any(
            wake_integration.get("growth_seed_refs")
        ),
        "wake_repair_target_count": _count_any(
            wake_integration.get("repair_modulated_wake_targets")
        ),
        "narrative_candidate_count": _count_any(
            wake_integration.get("narrative_writeback_candidates")
        ),
        "relationship_repair_candidate_count": _count_any(
            wake_integration.get("relationship_repair_candidates")
        ),
        "dream_fact_gate_result": dream_fact_gate.get("gate_result"),
        "allowed_write_kinds": _list_refs(dream_fact_gate.get("allowed_writes")),
        "blocked_write_kinds": _list_refs(dream_fact_gate.get("blocked_writes")),
        "decision_item_count": _count_any(dream_fact_gate.get("decision_items")),
        "nightmare_risk_status": nightmare_risk.get("risk_status"),
        "nightmare_loop_indicators": _list_refs(
            nightmare_risk.get("loop_indicators")
        ),
        "queue_e_repair_pressure_level": repair_profile.get("pressure_level")
        or dream_window.get("queue_e_repair_pressure_level")
        or wake_integration.get("queue_e_repair_pressure_level"),
        "queue_e_repair_attention_target": repair_profile.get("attention_target")
        or dream_window.get("queue_e_repair_attention_target")
        or wake_integration.get("queue_e_repair_attention_target"),
        "offline_learning_generation": offline_learning.get("generation"),
        "offline_learning_pressure_level": offline_learning.get("pressure_level"),
        "offline_learning_attention_target": offline_learning.get(
            "attention_target"
        ),
        "offline_learning_integration_mode": offline_learning.get(
            "integration_mode"
        ),
        "relationship_reconsolidation_required": bool(
            offline_learning.get("relationship_reconsolidation_required")
        ),
        "web_dream_learning_status": web_dream_learning.get("status"),
        "web_topic_candidate_count": _count_any(
            web_dream_learning.get("topic_candidates")
        ),
        "web_wake_question_candidate_count": _count_any(
            web_dream_learning.get("wake_question_candidates")
        ),
        "memory_tier_presence": {
            "salient_core": bool(memory_tiering.get("salient_core_episode_refs")),
            "retrievable_context": bool(
                memory_tiering.get("retrievable_context_episode_refs")
            ),
            "deep_sediment": bool(memory_tiering.get("deep_sediment_episode_refs")),
        },
        "dream_boundary": (
            "dream_residue_wake_review_fact_gate_before_memory_or_action"
        ),
    }


def _collect_relation_context_summary(section: dict[str, Any]) -> dict[str, Any]:
    life_context = _extract_compact_value(section.get("life_context_frame", {}))
    relation_turn = _extract_compact_value(section.get("relation_turn_frame", {}))
    language_percept = _extract_compact_value(section.get("language_percept", {}))
    relationship_timeline = _extract_compact_value(
        section.get("relationship_timeline", {})
    )
    dialogue_memory = _extract_compact_value(
        section.get("dialogue_memory_summary", {})
    )
    relationship_state = _extract_nested_value(
        relationship_timeline,
        "relationship_state",
    )
    common_ground_states = relationship_timeline.get("common_ground_states")
    first_common_ground = (
        common_ground_states[0]
        if isinstance(common_ground_states, list) and common_ground_states
        else {}
    )
    first_common_ground = (
        first_common_ground if isinstance(first_common_ground, dict) else {}
    )
    domain_presence = {
        "life_context_frame": bool(life_context),
        "relation_turn_frame": bool(relation_turn),
        "language_percept": bool(language_percept),
        "relationship_timeline": bool(relationship_timeline),
        "dialogue_memory_summary": bool(dialogue_memory),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "relation_context_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "life_name": life_context.get("life_name"),
        "context_mode": life_context.get("context_mode"),
        "current_relation_subject_ref": life_context.get(
            "current_relation_subject_ref"
        ),
        "active_context_refs": _list_refs(life_context.get("active_context_refs")),
        "relation_turn_id": relation_turn.get("turn_id"),
        "relation_scope": relation_turn.get("relation_scope"),
        "turn_intent": relation_turn.get("turn_intent"),
        "relation_subject_ref": relation_turn.get("relation_subject_ref"),
        "external_utterance_digest_present": bool(
            relation_turn.get("external_utterance_digest")
        ),
        "language_percept_mode": language_percept.get("percept_mode"),
        "language_semantic_focus": language_percept.get("semantic_focus"),
        "relationship_stage": _first_non_empty(
            relationship_timeline.get("relationship_stage"),
            relationship_state.get("relationship_stage"),
        ),
        "shared_terms": _list_refs(first_common_ground.get("shared_terms")),
        "open_misalignment_count": _count_any(
            first_common_ground.get("open_misalignments")
        ),
        "dialogue_episode_count": _count_any(
            dialogue_memory.get("deduplicated_episode_summaries")
        ),
        "next_wake_cue_count": _count_any(dialogue_memory.get("next_wake_cues")),
        "context_boundary": (
            "context_state_view_not_relationship_turn_injection"
        ),
    }


def _collect_ability_birth_readiness_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    readiness_rollup = _extract_compact_value(
        section.get("birth_readiness_rollup", {})
    )
    stage_gate = _extract_compact_value(section.get("birth_readiness_stage_gate", {}))
    live0_audit = _extract_compact_value(section.get("live0_acceptance_audit", {}))
    contract_index = _extract_compact_value(section.get("v0_contract_file_index", {}))
    life_target_status = readiness_rollup.get("life_target_status")
    if not isinstance(life_target_status, dict):
        life_target_status = {}
    gate_status = stage_gate.get("gate_status")
    if not isinstance(gate_status, dict):
        gate_status = {}
    criteria_summary = _extract_nested_value(live0_audit, "criteria_summary")
    criteria = live0_audit.get("criteria")
    if not isinstance(criteria, list):
        criteria = []
    domain_presence = {
        "birth_readiness_rollup": bool(readiness_rollup),
        "birth_readiness_stage_gate": bool(stage_gate),
        "live0_acceptance_audit": bool(live0_audit),
        "v0_contract_file_index": bool(contract_index),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    target_closed = sum(
        1 for status in life_target_status.values() if status == "closed"
    )
    target_open = len(life_target_status) - target_closed
    blocked_reasons = _list_refs(
        readiness_rollup.get("blocked_reasons")
        or stage_gate.get("blocked_reasons")
        or live0_audit.get("blocked_reasons")
    )
    return {
        "schema_version": "ability_birth_readiness_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "birth_readiness_overall_status": readiness_rollup.get("overall_status"),
        "life_target_count": len(life_target_status),
        "life_target_closed_count": target_closed,
        "life_target_open_count": target_open,
        "life_target_open_names": [
            name
            for name, status in life_target_status.items()
            if status != "closed"
        ][:12],
        "stage_gate_decision": stage_gate.get("decision"),
        "stage_effect": stage_gate.get("stage_effect"),
        "gate_closed_count": sum(
            1 for status in gate_status.values() if status == "closed"
        ),
        "gate_open_names": [
            name for name, status in gate_status.items() if status != "closed"
        ][:12],
        "blocked_reasons": blocked_reasons,
        "next_required_command": _first_non_empty(
            stage_gate.get("next_required_command"),
            live0_audit.get("next_required_command"),
        ),
        "queue_e_world_contact_handoff_status": _first_non_empty(
            readiness_rollup.get("queue_e_world_contact_handoff_status"),
            stage_gate.get("queue_e_world_contact_handoff_status"),
        ),
        "queue_e_world_contact_repair_hold_required": bool(
            readiness_rollup.get("queue_e_world_contact_repair_hold_required")
            or stage_gate.get("queue_e_world_contact_repair_hold_required")
        ),
        "queue_e_birth_repair_pressure_level": readiness_rollup.get(
            "queue_e_birth_repair_pressure_level"
        ),
        "live0_acceptance_status": live0_audit.get("status"),
        "live0_acceptance_closed": bool(
            live0_audit.get("live0_acceptance_closed")
        ),
        "criteria_total": criteria_summary.get("criteria_total")
        or _count_any(criteria),
        "criteria_closed": criteria_summary.get("criteria_closed"),
        "criteria_blocked": criteria_summary.get("criteria_blocked"),
        "failed_criteria": _list_refs(criteria_summary.get("failed_criteria")),
        "contract_count": contract_index.get("contract_count"),
        "covered_contract_ref_count": _count_any(
            contract_index.get("covered_contract_refs")
        ),
        "ability_boundary": (
            "ability_summary_is_birth_evidence_view_not_completion_claim"
        ),
    }


def _collect_perception_world_contact_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    visual_observation = _extract_compact_value(
        section.get("visual_observation_frame", {})
    )
    world_contact = _extract_compact_value(section.get("world_contact_summary", {}))
    belief_state = _extract_compact_value(section.get("belief_state_frame", {}))
    prediction_workspace = _extract_compact_value(
        section.get("prediction_workspace_frame", {})
    )
    active_sampling = _extract_compact_value(
        section.get("active_sampling_plan", {})
    )
    workspace_contents = _extract_nested_value(
        prediction_workspace,
        "workspace_contents",
    )
    domain_presence = {
        "visual_observation_frame": bool(visual_observation),
        "world_contact_summary": bool(world_contact),
        "belief_state_frame": bool(belief_state),
        "prediction_workspace_frame": bool(prediction_workspace),
        "active_sampling_plan": bool(active_sampling),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    confirmation_pending_ids = world_contact.get("confirmation_pending_ids")
    return {
        "schema_version": "perception_world_contact_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "observation_mode": visual_observation.get("observation_mode"),
        "observed_surface_count": visual_observation.get(
            "observed_surface_count"
        ),
        "focus_terms": _list_refs(visual_observation.get("focus_terms")),
        "observation_source_ref_count": _count_any(
            visual_observation.get("source_refs")
        ),
        "contact_mode": world_contact.get("contact_mode"),
        "release_posture": world_contact.get("release_posture"),
        "candidate_intent_count": world_contact.get("candidate_intent_count"),
        "blocked_contact_count": world_contact.get("blocked_contact_count"),
        "confirmation_pending_count": _count_any(confirmation_pending_ids),
        "confirmation_pending_ids": _list_refs(confirmation_pending_ids),
        "observation_route_mode": world_contact.get("observation_route_mode"),
        "relationship_effects": _list_refs(world_contact.get("relationship_effects")),
        "repair_obligation_ref_count": _count_any(
            world_contact.get("repair_obligation_refs")
        ),
        "regret_pressure_ref_count": _count_any(
            world_contact.get("regret_pressure_refs")
        ),
        "next_guard_ref_count": _count_any(world_contact.get("next_guard_refs")),
        "belief_focus": belief_state.get("belief_focus"),
        "prediction_focus": _first_non_empty(
            workspace_contents.get("semantic_prediction_focus"),
            prediction_workspace.get("semantic_prediction_focus"),
            belief_state.get("belief_focus"),
        ),
        "candidate_explanation_count": _count_any(
            workspace_contents.get("candidate_explanations")
        )
        or _count_any(prediction_workspace.get("candidate_explanations")),
        "downstream_systems": _list_refs(
            prediction_workspace.get("downstream_systems")
        ),
        "active_sampling_route": active_sampling.get("selected_route"),
        "active_sampling_stage_effect": active_sampling.get("stage_effect"),
        "active_sampling_target_count": _count_any(
            active_sampling.get("sampling_targets")
        ),
        "perception_boundary": (
            "perception_prediction_world_contact_view_not_tool_gateway"
        ),
    }


def _collect_proactive_voice_summary(section: dict[str, Any]) -> dict[str, Any]:
    proactive_state = _extract_compact_value(section.get("proactive_state", {}))
    profile = _extract_nested_value(proactive_state, "last_proactive_voice_profile")
    coverage = _extract_nested_value(proactive_state, "last_profile_coverage")
    if not coverage:
        coverage = _extract_nested_value(profile, "profile_coverage")
    active_domains = coverage.get("active_domains")
    if not isinstance(active_domains, list):
        active_domains = []
    domain_presence = coverage.get("domain_presence")
    if not isinstance(domain_presence, dict):
        domain_presence = {}
    candidate_count = proactive_state.get("last_utterance_candidate_code_count")
    if candidate_count is None:
        candidate_count = profile.get("utterance_candidate_code_count")
    if candidate_count is None:
        candidate_count = profile.get("question_candidate_count")
    return {
        "status": proactive_state.get("status"),
        "release_scope": proactive_state.get("last_release_scope"),
        "natural_language_released": proactive_state.get(
            "last_natural_language_released"
        ),
        "model_expression_status": proactive_state.get(
            "last_model_expression_status"
        ),
        "post_expression_gate_status": proactive_state.get(
            "last_post_expression_gate_status"
        ),
        "focus": proactive_state.get("last_focus"),
        "surface_kind": proactive_state.get("last_proactive_voice_surface_kind")
        or profile.get("surface_kind"),
        "coverage_schema_version": coverage.get("schema_version"),
        "active_domain_count": coverage.get("active_domain_count"),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "utterance_candidate_code_count": candidate_count,
        "event_count": proactive_state.get("event_count"),
        "release_count": proactive_state.get("release_count"),
        "speech_generation_boundary": "state_codes_only_model_expression_required",
    }


def _collect_body_grounding_summary(section: dict[str, Any]) -> dict[str, Any]:
    rhythm = _extract_compact_value(section.get("body_rhythm_pulse", {}))
    need_state = _extract_compact_value(section.get("need_state_vector", {}))
    body_budget = _extract_compact_value(section.get("body_resource_budget", {}))
    core_affect = _extract_compact_value(section.get("core_affect_vector", {}))
    signal_media = _extract_compact_value(section.get("signal_media_runtime", {}))
    idle_strategy = _extract_compact_value(section.get("idle_strategy", {}))
    maintenance_pressure = _extract_nested_value(
        body_budget,
        "maintenance_pressure",
    )
    fatigue_state = _extract_nested_value(body_budget, "fatigue_state")
    energy_state = _extract_nested_value(body_budget, "energy_state")
    body_signal_profile = _extract_nested_value(
        signal_media,
        "body_signal_profile",
    )
    modulation_vector = _extract_nested_value(signal_media, "modulation_vector")
    domain_presence = {
        "body_rhythm_pulse": bool(rhythm),
        "need_state_vector": bool(need_state),
        "body_resource_budget": bool(body_budget),
        "core_affect_vector": bool(core_affect),
        "signal_media_runtime": bool(signal_media),
        "idle_strategy": bool(idle_strategy),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "body_grounding_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "rhythm_state": rhythm.get("rhythm_state"),
        "heartbeat_counter": rhythm.get("heartbeat_counter"),
        "allostatic_load": rhythm.get("allostatic_load")
        or need_state.get("resource_deficit"),
        "resource_deficit": need_state.get("resource_deficit"),
        "repair_drive": _first_non_empty(
            need_state.get("repair_drive"),
            core_affect.get("repair_drive"),
            maintenance_pressure.get("repair_drive"),
            body_signal_profile.get("repair_drive"),
            modulation_vector.get("repair_drive"),
        ),
        "social_readiness": need_state.get("social_readiness"),
        "cognitive_bandwidth": need_state.get("cognitive_bandwidth"),
        "sleep_pressure": need_state.get("sleep_pressure"),
        "energy_level": _first_non_empty(
            energy_state.get("level"),
            body_signal_profile.get("energy_level"),
        ),
        "fatigue_level": _first_non_empty(
            fatigue_state.get("level"),
            rhythm.get("fatigue_load"),
            body_signal_profile.get("fatigue_load"),
        ),
        "core_affect_modulators": {
            "valence": core_affect.get("valence"),
            "arousal": core_affect.get("arousal"),
            "dominance": core_affect.get("dominance"),
            "pain_pressure": core_affect.get("pain_pressure"),
            "relationship_tension": core_affect.get("relationship_tension"),
            "dream_residue_load": core_affect.get("dream_residue_load"),
            "responsibility_weight": core_affect.get("responsibility_weight"),
        },
        "signal_body_profile": _tier_refs(
            body_signal_profile,
            [
                "memory_write_bias",
                "dream_pressure_bias",
                "language_tempo_bias",
                "body_signal_strength",
                "offline_learning_pressure_level",
                "offline_learning_integration_mode",
            ],
        ),
        "waiting_consumption": _tier_refs(
            idle_strategy,
            [
                "waiting_posture",
                "governance_attention_target",
                "governance_attention_reason",
                "next_idle_action",
                "heartbeat_interval_ms",
                "body_waiting_posture",
                "body_signal_write_bias",
            ],
        ),
        "language_modulation_boundary": (
            "body_state_modulates_expression_without_spoken_signal_dump"
        ),
    }


def _collect_emotion_regulation_summary(section: dict[str, Any]) -> dict[str, Any]:
    core_affect = _extract_compact_value(section.get("core_affect_vector", {}))
    affective_episode = _extract_compact_value(
        section.get("affective_episode", {})
    )
    emotion_regulation = _extract_compact_value(
        section.get("emotion_regulation_loop", {})
    )
    body_budget = _extract_compact_value(section.get("body_resource_budget", {}))
    pain_regret_repair = _extract_compact_value(
        section.get("pain_regret_repair_report", {})
    )
    signal_media = _extract_compact_value(section.get("signal_media_runtime", {}))
    maintenance_pressure = _extract_nested_value(
        body_budget,
        "maintenance_pressure",
    )
    fatigue_state = _extract_nested_value(body_budget, "fatigue_state")
    modulation_vector = _extract_nested_value(signal_media, "modulation_vector")
    body_signal_profile = _extract_nested_value(
        signal_media,
        "body_signal_profile",
    )
    domain_presence = {
        "core_affect_vector": bool(core_affect),
        "affective_episode": bool(affective_episode),
        "emotion_regulation_loop": bool(emotion_regulation),
        "body_resource_budget": bool(body_budget),
        "pain_regret_repair_report": bool(pain_regret_repair),
        "signal_media_runtime": bool(signal_media),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "emotion_regulation_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "episode_label": affective_episode.get("episode_label"),
        "expression_risk": affective_episode.get("expression_risk"),
        "repair_bias": affective_episode.get("repair_bias"),
        "regulation_mode": emotion_regulation.get("regulation_mode"),
        "expression_delay_required": emotion_regulation.get(
            "expression_delay_required"
        ),
        "suppression_cost": emotion_regulation.get("suppression_cost"),
        "core_affect_modulators": {
            "valence": core_affect.get("valence"),
            "arousal": core_affect.get("arousal"),
            "pain_pressure": core_affect.get("pain_pressure"),
            "relationship_tension": core_affect.get("relationship_tension"),
            "dream_residue_load": core_affect.get("dream_residue_load"),
            "responsibility_weight": core_affect.get("responsibility_weight"),
            "repair_drive": core_affect.get("repair_drive"),
        },
        "resource_pressure": {
            "fatigue_level": fatigue_state.get("level"),
            "resource_deficit": maintenance_pressure.get("resource_deficit"),
            "maintenance_repair_drive": maintenance_pressure.get("repair_drive"),
        },
        "repair_followup_required": bool(
            pain_regret_repair.get("repair_followup_required")
        ),
        "regret_pressure_ref_count": _count_any(
            pain_regret_repair.get("regret_pressure_refs")
        ),
        "signal_modulation": _tier_refs(
            modulation_vector,
            [
                "arousal",
                "precision",
                "inhibition",
                "repair_drive",
                "language_precision",
            ],
        ),
        "body_signal_modulation": _tier_refs(
            body_signal_profile,
            [
                "memory_write_bias",
                "dream_pressure_bias",
                "language_tempo_bias",
            ],
        ),
        "emotion_release_boundary": (
            "emotion_state_modulates_language_not_template_emotion_speech"
        ),
    }


def _collect_inner_environment_modulation_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    need_state = _extract_compact_value(section.get("need_state_vector", {}))
    body_budget = _extract_compact_value(section.get("body_resource_budget", {}))
    rhythm = _extract_compact_value(section.get("body_rhythm_pulse", {}))
    signal_media = _extract_compact_value(section.get("signal_media_runtime", {}))
    idle_strategy = _extract_compact_value(section.get("idle_strategy", {}))
    maintenance_pressure = _extract_nested_value(
        body_budget,
        "maintenance_pressure",
    )
    fatigue_state = _extract_nested_value(body_budget, "fatigue_state")
    energy_state = _extract_nested_value(body_budget, "energy_state")
    modulation_vector = _extract_nested_value(signal_media, "modulation_vector")
    body_signal_profile = _extract_nested_value(
        signal_media,
        "body_signal_profile",
    )
    domain_presence = {
        "need_state_vector": bool(need_state),
        "body_resource_budget": bool(body_budget),
        "body_rhythm_pulse": bool(rhythm),
        "signal_media_runtime": bool(signal_media),
        "idle_strategy": bool(idle_strategy),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "inner_environment_modulation_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "resource_deficit": need_state.get("resource_deficit"),
        "repair_drive": _first_non_empty(
            need_state.get("repair_drive"),
            maintenance_pressure.get("repair_drive"),
            body_signal_profile.get("repair_drive"),
            modulation_vector.get("repair_drive"),
        ),
        "social_readiness": need_state.get("social_readiness"),
        "cognitive_bandwidth": need_state.get("cognitive_bandwidth"),
        "sleep_pressure": need_state.get("sleep_pressure"),
        "energy_level": energy_state.get("level"),
        "fatigue_level": fatigue_state.get("level") or rhythm.get("fatigue_load"),
        "body_signal_write_bias": body_signal_profile.get("memory_write_bias")
        or idle_strategy.get("body_signal_write_bias"),
        "dream_pressure_bias": body_signal_profile.get("dream_pressure_bias"),
        "language_tempo_bias": body_signal_profile.get("language_tempo_bias"),
        "modulation_vector": _tier_refs(
            modulation_vector,
            [
                "arousal",
                "precision",
                "inhibition",
                "repair_drive",
                "language_precision",
                "heartbeat_cadence_driver",
            ],
        ),
        "waiting_governance": _tier_refs(
            idle_strategy,
            [
                "waiting_posture",
                "governance_attention_target",
                "governance_attention_reason",
                "next_idle_action",
                "heartbeat_interval_ms",
            ],
        ),
        "inspection_boundary": (
            "inner_environment_summary_is_state_view_not_dialogue_response"
        ),
    }


def _collect_language_generation_consumption_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    language_percept = _extract_compact_value(section.get("language_percept", {}))
    semantic_map = _extract_compact_value(section.get("semantic_map", {}))
    inner_speech = _extract_compact_value(section.get("inner_speech", {}))
    expression_monitor = _extract_compact_value(
        section.get("expression_monitor", {})
    )
    expression_plan = _extract_compact_value(section.get("expression_plan", {}))
    model_expression = _extract_compact_value(
        section.get("model_expression_state", {})
    )
    relationship_memory = _extract_compact_value(
        section.get("relationship_memory", {})
    )
    dialogue_memory_summary = _extract_compact_value(
        section.get("dialogue_memory_summary", {})
    )
    memory_retrieval = _extract_compact_value(section.get("memory_retrieval", {}))
    exit_dream_summary = _extract_compact_value(
        section.get("exit_dream_consolidation_summary", {})
    )
    core_affect = _extract_compact_value(section.get("core_affect_vector", {}))
    body_budget = _extract_compact_value(section.get("body_resource_budget", {}))
    signal_media = _extract_compact_value(section.get("signal_media_runtime", {}))
    relationship_timeline = _extract_compact_value(
        section.get("relationship_timeline", {})
    )
    commitment_truth = _extract_compact_value(
        section.get("commitment_truth_state", {})
    )
    responsibility_loop = _extract_compact_value(
        section.get("responsibility_loop_state", {})
    )
    pain_regret_repair = _extract_compact_value(
        section.get("pain_regret_repair_report", {})
    )
    belief_state = _extract_compact_value(section.get("belief_state_frame", {}))
    prediction_error = _extract_compact_value(
        section.get("prediction_error_field", {})
    )
    active_sampling = _extract_compact_value(
        section.get("active_sampling_plan", {})
    )
    resident_autonomous = _extract_compact_value(
        section.get("resident_autonomous_activity", {})
    )
    proactive_state = _extract_compact_value(section.get("proactive_state", {}))
    post_expression_gate = _extract_nested_value(
        model_expression,
        "post_expression_gate",
    )
    model_context_summary = _extract_nested_value(
        model_expression,
        "model_expression_context_summary",
    )

    domain_presence = {
        "language_percept": bool(language_percept),
        "semantic_map": bool(semantic_map),
        "inner_speech": bool(inner_speech),
        "expression_monitor": bool(expression_monitor),
        "expression_plan": bool(expression_plan),
        "model_expression": bool(model_expression),
        "relationship_memory": bool(relationship_memory),
        "dialogue_memory": bool(dialogue_memory_summary),
        "memory_retrieval": bool(memory_retrieval),
        "dream_residue": bool(exit_dream_summary),
        "body_affect": bool(core_affect or body_budget),
        "signal_media": bool(signal_media),
        "relationship": bool(relationship_timeline or commitment_truth),
        "responsibility_repair": bool(responsibility_loop or pain_regret_repair),
        "prediction_attention": bool(
            belief_state or prediction_error or active_sampling
        ),
        "resident_autonomous_activity": bool(resident_autonomous),
        "proactive_voice": bool(proactive_state),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    required_evidence_flags = post_expression_gate.get("required_evidence_flags")
    if not isinstance(required_evidence_flags, list):
        required_evidence_flags = []
    missing_evidence_flags = post_expression_gate.get("missing_evidence_flags")
    if not isinstance(missing_evidence_flags, list):
        missing_evidence_flags = []
    soft_missing_evidence_flags = post_expression_gate.get(
        "soft_missing_evidence_flags"
    )
    if not isinstance(soft_missing_evidence_flags, list):
        soft_missing_evidence_flags = []

    memory_tiering = _extract_nested_value(exit_dream_summary, "memory_tiering")
    relation_profile = _extract_nested_value(
        relationship_memory,
        "relation_person_profile",
    )
    return {
        "schema_version": "language_generation_consumption_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "semantic_focus": semantic_map.get("semantic_focus")
        or language_percept.get("semantic_focus")
        or model_context_summary.get("semantic_focus"),
        "inner_speech_drive_count": _count_any(
            inner_speech.get("inner_drive_states")
        ),
        "expression_monitor_status": expression_monitor.get("monitor_status"),
        "expression_plan_goal": expression_plan.get("semantic_goal"),
        "model_expression_status": model_expression.get("model_expression_status"),
        "post_expression_gate_status": post_expression_gate.get("gate_status"),
        "required_evidence_flags": required_evidence_flags[:12],
        "missing_evidence_flags": missing_evidence_flags[:12],
        "soft_missing_evidence_flags": soft_missing_evidence_flags[:12],
        "memory_reconstruction_focus": memory_retrieval.get(
            "reconstruction_focus"
        ),
        "memory_activated_ref_count": _count_any(
            memory_retrieval.get("activated_refs")
        )
        or _count_any(memory_retrieval.get("activated_engram_refs")),
        "relationship_observed_names": _list_refs(
            relation_profile.get("observed_names")
        ),
        "next_wake_cue_count": _count_any(
            relationship_memory.get("next_wake_cues")
        )
        + _count_any(dialogue_memory_summary.get("next_wake_cues")),
        "dream_memory_tier_presence": {
            "salient_core": bool(memory_tiering.get("salient_core_episode_refs")),
            "retrievable_context": bool(
                memory_tiering.get("retrievable_context_episode_refs")
            ),
            "deep_sediment": bool(memory_tiering.get("deep_sediment_episode_refs")),
        },
        "body_affect_modulators": {
            "arousal": core_affect.get("arousal"),
            "repair_drive": core_affect.get("repair_drive")
            or _extract_nested_value(body_budget, "maintenance_pressure").get(
                "repair_drive"
            ),
            "fatigue_level": _extract_nested_value(
                body_budget,
                "fatigue_state",
            ).get("level"),
        },
        "signal_modulators": _tier_refs(
            _extract_nested_value(signal_media, "modulation_vector"),
            [
                "arousal",
                "precision",
                "inhibition",
                "repair_drive",
                "language_precision",
            ],
        ),
        "relationship_stage": _first_non_empty(
            relationship_timeline.get("relationship_stage"),
            _extract_nested_value(relationship_timeline, "relationship_state").get(
                "relationship_stage"
            ),
            model_context_summary.get("relationship_stage"),
        ),
        "commitment_truth_status": commitment_truth.get("truth_status")
        or commitment_truth.get("stage_status"),
        "repair_followup_required": bool(
            responsibility_loop.get("repair_followup_required")
            or pain_regret_repair.get("repair_followup_required")
        ),
        "regret_pressure_count": _count_any(
            responsibility_loop.get("regret_pressure_candidates")
        )
        + _count_any(pain_regret_repair.get("regret_pressure_refs")),
        "prediction_route": active_sampling.get("selected_route"),
        "prediction_error_count": _count_any(prediction_error.get("error_events")),
        "resident_autonomous_last_activity": resident_autonomous.get(
            "last_activity_kind"
        ),
        "proactive_voice_status": proactive_state.get("status"),
        "language_release_boundary": (
            "state_inspection_only_model_expression_then_post_gate"
        ),
        "fixed_reply_boundary": (
            "no_code_spoken_template_no_inspection_summary_as_reply"
        ),
    }


def _collect_relationship_continuity_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    relationship_graph = _extract_compact_value(
        section.get("relationship_subject_graph", {})
    )
    relationship_timeline = _extract_compact_value(
        section.get("relationship_timeline", {})
    )
    commitment_truth = _extract_compact_value(
        section.get("commitment_truth_state", {})
    )
    commitment_expression = _extract_compact_value(
        section.get("commitment_expression_plan", {})
    )
    apology_repair = _extract_compact_value(
        section.get("apology_repair_language_trace", {})
    )
    subjects = relationship_graph.get("subjects")
    subject = subjects[0] if isinstance(subjects, list) and subjects else {}
    subject = subject if isinstance(subject, dict) else {}
    common_ground_states = relationship_timeline.get("common_ground_states")
    first_common_ground = (
        common_ground_states[0]
        if isinstance(common_ground_states, list) and common_ground_states
        else {}
    )
    first_common_ground = (
        first_common_ground if isinstance(first_common_ground, dict) else {}
    )
    trust_trajectories = relationship_timeline.get("trust_trajectories")
    first_trust = (
        trust_trajectories[0]
        if isinstance(trust_trajectories, list) and trust_trajectories
        else {}
    )
    first_trust = first_trust if isinstance(first_trust, dict) else {}
    continuity_reports = relationship_timeline.get(
        "relationship_continuity_reports"
    )
    first_continuity = (
        continuity_reports[0]
        if isinstance(continuity_reports, list) and continuity_reports
        else {}
    )
    first_continuity = (
        first_continuity if isinstance(first_continuity, dict) else {}
    )
    injury_traces = relationship_timeline.get("relationship_injury_traces")
    longitudinal_gates = relationship_timeline.get("longitudinal_stage_gates")
    domain_presence = {
        "relationship_subject_graph": bool(relationship_graph),
        "relationship_timeline": bool(relationship_timeline),
        "commitment_truth_state": bool(commitment_truth),
        "commitment_expression_plan": bool(commitment_expression),
        "apology_repair_language_trace": bool(apology_repair),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "relationship_continuity_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "relationship_id": subject.get("relationship_id"),
        "relation_role": subject.get("relation_role"),
        "relationship_stage": _first_non_empty(
            subject.get("relationship_stage"),
            relationship_timeline.get("relationship_stage"),
            first_continuity.get("relationship_stage"),
        ),
        "relationship_stage_reason": subject.get("relationship_stage_reason"),
        "relationship_stage_evidence_ref_count": _count_any(
            subject.get("relationship_stage_evidence_refs")
        ),
        "shared_terms": _list_refs(first_common_ground.get("shared_terms")),
        "open_misalignment_count": _count_any(
            first_common_ground.get("open_misalignments")
        ),
        "shared_memory_ref_count": _count_any(
            first_continuity.get("shared_memory_refs")
        ),
        "dialogue_turn_ref_count": _count_any(
            relationship_timeline.get("dialogue_turn_refs")
        ),
        "trust_state": first_trust.get("current_trust_state"),
        "trust_repair_commitment_ref_count": _count_any(
            first_trust.get("repair_commitment_refs")
        ),
        "injury_trace_count": _count_any(injury_traces),
        "repair_open_count": sum(
            1
            for item in injury_traces
            if isinstance(item, dict) and item.get("current_state") == "repair_open"
        )
        if isinstance(injury_traces, list)
        else 0,
        "commitment_truth_status": commitment_truth.get("truth_status")
        or commitment_truth.get("stage_status"),
        "open_commitment_ref_count": _count_any(
            commitment_truth.get("open_commitment_refs")
        ),
        "repair_required_ref_count": _count_any(
            commitment_truth.get("repair_required_refs")
        ),
        "commitment_expression_goal": commitment_expression.get("semantic_goal"),
        "commitment_act_order": _list_refs(
            commitment_expression.get("act_type_order")
        ),
        "commitment_repair_pressure": _first_non_empty(
            commitment_expression.get("repair_pressure"),
            commitment_expression.get("queue_e_repair_pressure_level"),
        ),
        "repair_move_order": _list_refs(apology_repair.get("move_type_order")),
        "repair_move_count": _count_any(apology_repair.get("repair_language_moves")),
        "relationship_injury_ref_count": _count_any(
            apology_repair.get("relationship_injury_refs")
        ),
        "stage_gate_count": _count_any(longitudinal_gates),
        "relationship_boundary": (
            "relationship_state_timeline_commitment_repair_not_service_role_label"
        ),
    }


def _collect_cognitive_workspace_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    workspace = _extract_compact_value(section.get("workspace_frame", {}))
    broadcast = _extract_compact_value(section.get("broadcast_frame", {}))
    metacognition = _extract_compact_value(section.get("metacognition_state", {}))
    belief_state = _extract_compact_value(section.get("belief_state_frame", {}))
    prediction_error = _extract_compact_value(
        section.get("prediction_error_field", {})
    )
    active_sampling = _extract_compact_value(
        section.get("active_sampling_plan", {})
    )
    memory_write_gate = _extract_compact_value(
        section.get("memory_write_gate", {})
    )
    state_merge_guard = _extract_compact_value(section.get("state_merge_guard", {}))
    prediction_contents = _extract_nested_value(
        workspace,
        "prediction_workspace_contents",
    )
    if not prediction_contents:
        prediction_contents = _extract_nested_value(
            workspace,
            "workspace_contents",
        )
    body_signal_modulation = _extract_nested_value(
        memory_write_gate,
        "body_signal_write_modulation",
    )
    domain_presence = {
        "workspace_frame": bool(workspace),
        "broadcast_frame": bool(broadcast),
        "metacognition_state": bool(metacognition),
        "belief_state_frame": bool(belief_state),
        "prediction_error_field": bool(prediction_error),
        "active_sampling_plan": bool(active_sampling),
        "memory_write_gate": bool(memory_write_gate),
        "state_merge_guard": bool(state_merge_guard),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "cognitive_workspace_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "workspace_status": workspace.get("status"),
        "workspace_focus": _first_non_empty(
            workspace.get("live_turn_focus"),
            workspace.get("current_focus"),
            prediction_contents.get("semantic_prediction_focus"),
            belief_state.get("belief_focus"),
        ),
        "candidate_explanation_count": _count_any(
            workspace.get("candidate_explanations")
        )
        or _count_any(prediction_contents.get("candidate_explanations")),
        "workspace_broadcast_targets": _list_refs(
            workspace.get("broadcast_targets")
        ),
        "broadcast_target_count": _count_any(
            broadcast.get("broadcast_targets")
        )
        or _count_any(workspace.get("broadcast_targets")),
        "broadcast_targets": _list_refs(
            broadcast.get("broadcast_targets")
            or workspace.get("broadcast_targets")
        ),
        "salience_rank_count": _count_any(broadcast.get("salience_ranking")),
        "suppressed_content_ref_count": _count_any(
            broadcast.get("suppressed_content_refs")
        ),
        "metacognitive_uncertainty_flags": _list_refs(
            metacognition.get("uncertainty_flags")
        ),
        "metacognitive_reflection_prompt_count": _count_any(
            metacognition.get("reflection_prompts")
        ),
        "expression_risk_ref_count": _count_any(
            metacognition.get("expression_risk_refs")
        ),
        "relationship_tension_ref_count": _count_any(
            metacognition.get("relationship_tension_refs")
        ),
        "belief_focus": belief_state.get("belief_focus"),
        "prediction_error_count": _first_non_empty(
            prediction_error.get("error_count"),
            _count_any(prediction_error.get("error_events")),
        ),
        "prediction_error_events": _list_refs(prediction_error.get("error_events")),
        "active_sampling_route": active_sampling.get("selected_route"),
        "active_sampling_stage_effect": active_sampling.get("stage_effect"),
        "active_sampling_target_count": _count_any(
            active_sampling.get("sampling_targets")
        ),
        "memory_write_gate_policy": memory_write_gate.get("stage_policy"),
        "memory_write_gate_status": memory_write_gate.get("status"),
        "memory_write_bias": body_signal_modulation.get("write_bias"),
        "state_merge_policy": state_merge_guard.get("stage_policy"),
        "state_merge_route_counts": {
            "promotion": _count_any(state_merge_guard.get("promotion_routes")),
            "quarantine": _count_any(state_merge_guard.get("quarantine_routes")),
            "repair": _count_any(state_merge_guard.get("repair_routes")),
            "merge": _count_any(state_merge_guard.get("merge_routes")),
        },
        "cognition_boundary": (
            "workspace_broadcast_metacognition_state_view_not_consciousness_claim"
        ),
    }


def _collect_consciousness_reportability_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    workspace = _extract_compact_value(section.get("workspace_frame", {}))
    broadcast = _extract_compact_value(section.get("broadcast_frame", {}))
    metacognition = _extract_compact_value(section.get("metacognition_state", {}))
    probe = _extract_compact_value(section.get("consciousness_probe", {}))
    readiness_rollup = _extract_compact_value(
        section.get("birth_readiness_rollup", {})
    )
    stage_gate = _extract_compact_value(section.get("birth_readiness_stage_gate", {}))
    terminal_loop = _extract_compact_value(section.get("terminal_life_loop", {}))
    governance = _extract_compact_value(section.get("resident_governance", {}))
    lineage = _extract_nested_value(
        terminal_loop,
        "resident_background_lineage_state",
    )
    identity_birth_presence = _extract_nested_value(
        lineage,
        "identity_consciousness_birth_presence",
    )
    domain_presence = {
        "workspace_frame": bool(workspace),
        "broadcast_frame": bool(broadcast),
        "metacognition_state": bool(metacognition),
        "consciousness_probe": bool(probe),
        "birth_readiness_rollup": bool(readiness_rollup),
        "birth_readiness_stage_gate": bool(stage_gate),
        "terminal_life_loop": bool(terminal_loop),
        "resident_governance": bool(governance),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    reportability_flags = _list_refs(
        probe.get("reportability_flags")
        or identity_birth_presence.get("reportability_flags")
        or governance.get("consciousness_reportability_flags")
    )
    blocked_reasons = _list_refs(
        stage_gate.get("blocked_reasons")
        or readiness_rollup.get("blocked_reasons")
        or identity_birth_presence.get("blocked_reasons")
    )
    return {
        "schema_version": "consciousness_reportability_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "workspace_status": workspace.get("status"),
        "workspace_focus": _first_non_empty(
            workspace.get("live_turn_focus"),
            workspace.get("current_focus"),
        ),
        "workspace_candidate_explanation_count": _count_any(
            workspace.get("candidate_explanations")
        ),
        "workspace_broadcast_target_count": _count_any(
            workspace.get("broadcast_targets")
        ),
        "broadcast_target_count": _count_any(broadcast.get("broadcast_targets")),
        "broadcast_targets": _list_refs(broadcast.get("broadcast_targets")),
        "salience_rank_count": _count_any(broadcast.get("salience_ranking")),
        "metacognitive_uncertainty_flags": _list_refs(
            metacognition.get("uncertainty_flags")
        ),
        "reflection_prompt_count": _count_any(
            metacognition.get("reflection_prompts")
        ),
        "expression_risk_ref_count": _count_any(
            metacognition.get("expression_risk_refs")
        ),
        "probe_status": probe.get("probe_status"),
        "reportability_flags": reportability_flags,
        "reportability_flag_count": len(reportability_flags),
        "probe_refs": _tier_refs(
            probe,
            [
                "workspace_frame_ref",
                "broadcast_frame_ref",
                "metacognition_ref",
                "relationship_continuity_refs",
            ],
        ),
        "relationship_continuity_ref_count": _count_any(
            probe.get("relationship_continuity_refs")
        ),
        "birth_readiness_overall_status": readiness_rollup.get("overall_status"),
        "birth_readiness_stage_decision": stage_gate.get("decision"),
        "birth_readiness_stage_effect": stage_gate.get("stage_effect"),
        "birth_readiness_waiting_posture": _first_non_empty(
            identity_birth_presence.get("birth_readiness_waiting_posture"),
            governance.get("birth_readiness_waiting_posture"),
        ),
        "consciousness_waiting_posture": _first_non_empty(
            identity_birth_presence.get("consciousness_waiting_posture"),
            governance.get("consciousness_waiting_posture"),
        ),
        "blocked_reasons": blocked_reasons,
        "identity_consciousness_birth_ref_count": _count_any(
            identity_birth_presence.get("identity_consciousness_birth_refs")
        )
        + _count_any(lineage.get("resident_background_lineage_identity_consciousness_birth_refs")),
        "consciousness_boundary": (
            "consciousness_state_view_not_consciousness_claim_or_script"
        ),
    }


def _collect_self_thinking_summary(section: dict[str, Any]) -> dict[str, Any]:
    resident_self_thinking = _extract_compact_value(
        section.get("resident_self_thinking", {})
    )
    self_model = _extract_compact_value(section.get("self_model", {}))
    inner_speech = _extract_compact_value(section.get("inner_speech", {}))
    consciousness_probe = _extract_compact_value(
        section.get("consciousness_probe", {})
    )
    background_summary = _extract_compact_value(
        section.get("background_convergence_summary", {})
    )
    background_history = _extract_compact_value(
        section.get("background_convergence_history", {})
    )
    autonomous_activity = _extract_compact_value(
        section.get("resident_autonomous_activity", {})
    )
    slow_variables = self_model.get("trait_slow_variables")
    if not isinstance(slow_variables, dict):
        slow_variables = {}
    inner_drive_states = inner_speech.get("inner_drive_states")
    if not isinstance(inner_drive_states, dict):
        inner_drive_states = {}
    domain_presence = {
        "resident_self_thinking": bool(resident_self_thinking),
        "self_model": bool(self_model),
        "inner_speech": bool(inner_speech),
        "consciousness_probe": bool(consciousness_probe),
        "background_convergence_summary": bool(background_summary),
        "background_convergence_history": bool(background_history),
        "resident_autonomous_activity": bool(autonomous_activity),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "self_thinking_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "activity_kind": resident_self_thinking.get("activity_kind"),
        "thinking_mode": resident_self_thinking.get("thinking_mode"),
        "reflection_targets": _list_refs(
            resident_self_thinking.get("reflection_targets")
        ),
        "self_continuity_policy": resident_self_thinking.get(
            "self_continuity_policy"
        ),
        "thinking_evidence_ref_count": _count_any(
            resident_self_thinking.get("evidence_refs")
        ),
        "identity_mode": self_model.get("identity_mode"),
        "self_narrative_status": self_model.get("self_narrative_status"),
        "slow_variable_count": len(slow_variables),
        "slow_variable_names": list(slow_variables.keys())[:12],
        "growth_window_ref_count": _count_any(self_model.get("growth_window_refs")),
        "inner_speech_focus": inner_speech.get("inner_speech_focus"),
        "inner_drive_names": list(inner_drive_states.keys())[:12],
        "inner_drive_count": len(inner_drive_states),
        "self_reflection_ref_count": _count_any(
            inner_speech.get("self_reflection_refs")
        ),
        "consciousness_probe_status": consciousness_probe.get("probe_status"),
        "reportability_flag_count": _count_any(
            consciousness_probe.get("reportability_flags")
        ),
        "background_convergence_state": background_summary.get(
            "convergence_state"
        ),
        "background_convergence_pressure_level": background_summary.get(
            "convergence_pressure_level"
        ),
        "background_history_trend_state": background_history.get("trend_state"),
        "background_history_focus": background_history.get(
            "trait_convergence_history_focus"
        ),
        "autonomous_last_activity_kind": autonomous_activity.get(
            "last_activity_kind"
        ),
        "autonomous_self_thinking_count": _extract_nested_value(
            autonomous_activity,
            "activity_counts",
        ).get("self_thinking"),
        "thinking_boundary": (
            "thinking_state_view_not_inner_monologue_template"
        ),
    }


def _collect_personality_convergence_summary(
    section: dict[str, Any]
) -> dict[str, Any]:
    self_model = _extract_compact_value(section.get("self_model", {}))
    autobiographical_stack = _extract_compact_value(
        section.get("autobiographical_stack", {})
    )
    trait_drift = _extract_compact_value(section.get("trait_drift_monitor", {}))
    background_summary = _extract_compact_value(
        section.get("background_convergence_summary", {})
    )
    background_history = _extract_compact_value(
        section.get("background_convergence_history", {})
    )
    slow_variables = self_model.get("trait_slow_variables")
    if not isinstance(slow_variables, dict):
        slow_variables = {}
    trait_convergence = background_summary.get("trait_convergence_summary")
    if not isinstance(trait_convergence, dict):
        trait_convergence = {}
    history_profile = background_history.get("trait_convergence_history_profile")
    if not isinstance(history_profile, dict):
        history_profile = {}
    update_modes = trait_drift.get("slow_variable_update_mode_summary")
    if not isinstance(update_modes, dict):
        update_modes = {}
    domain_presence = {
        "self_model": bool(self_model),
        "autobiographical_stack": bool(autobiographical_stack),
        "trait_drift_monitor": bool(trait_drift),
        "background_convergence_summary": bool(background_summary),
        "background_convergence_history": bool(background_history),
    }
    active_domains = [
        name for name, present in domain_presence.items() if bool(present)
    ]
    return {
        "schema_version": "personality_convergence_summary_v0",
        "summary_kind": "inspection_only_not_spoken_response",
        "active_domain_count": len(active_domains),
        "active_domains": active_domains,
        "domain_presence": domain_presence,
        "identity_mode": self_model.get("identity_mode"),
        "self_narrative_status": self_model.get("self_narrative_status"),
        "slow_variable_count": len(slow_variables),
        "slow_variable_names": list(slow_variables.keys())[:12],
        "slow_variable_values": {
            name: _tier_refs(
                payload,
                [
                    "value",
                    "trend",
                    "update_count",
                    "last_relationship_stage",
                    "slow_variable_update_mode",
                    "background_trait_convergence_history_focus",
                    "background_trait_convergence_history_role",
                    "background_trait_convergence_history_latest_band",
                    "background_trait_convergence_history_trend_state",
                    "evidence_refs",
                ],
            )
            for name, payload in list(slow_variables.items())[:12]
            if isinstance(payload, dict)
        },
        "autobiographical_anchor_ref_count": _count_any(
            autobiographical_stack.get("anchor_refs")
        ),
        "autobiographical_turn_ref_count": _count_any(
            autobiographical_stack.get("turn_refs")
        ),
        "growth_window_ref_count": _count_any(self_model.get("growth_window_refs")),
        "trait_drift_direction": trait_drift.get("drift_direction"),
        "trait_drift_targets": _list_refs(trait_drift.get("slow_variable_targets")),
        "trait_drift_update_mode_summary": _compact_value(update_modes),
        "trait_drift_observation_ref_count": _count_any(
            trait_drift.get("drift_observation_refs")
        ),
        "background_convergence_state": background_summary.get(
            "convergence_state"
        ),
        "background_convergence_pressure_level": background_summary.get(
            "convergence_pressure_level"
        ),
        "background_convergence_attention_target": background_summary.get(
            "convergence_attention_target"
        ),
        "relationship_stage_continuity": background_summary.get(
            "relationship_stage_continuity"
        )
        or background_history.get("latest_relationship_stage_continuity"),
        "trait_convergence_score": background_summary.get(
            "trait_convergence_score"
        )
        or background_history.get("latest_trait_convergence_score"),
        "trait_convergence_names": list(trait_convergence.keys())[:12],
        "trait_convergence_recalibration_names": _list_refs(
            background_summary.get(
                "trait_drift_background_history_recalibration_names"
            )
            or background_history.get(
                "trait_drift_background_history_recalibration_names"
            )
            or background_history.get("trait_convergence_unstable_names")
        ),
        "trait_convergence_stable_names": _list_refs(
            background_summary.get(
                "trait_drift_background_history_stabilized_names"
            )
            or background_history.get(
                "trait_drift_background_history_stabilized_names"
            )
            or background_history.get("trait_convergence_stable_names")
        ),
        "background_history_trend_state": background_history.get("trend_state"),
        "background_history_focus": background_history.get(
            "trait_convergence_history_focus"
        ),
        "background_history_window_size": background_history.get(
            "history_window_size"
        ),
        "trait_history_profile": {
            name: _tier_refs(
                payload,
                [
                    "latest_band",
                    "trend_state",
                    "dominant_trait_drift_update_mode",
                    "latest_trait_drift_update_mode",
                ],
            )
            for name, payload in list(history_profile.items())[:12]
            if isinstance(payload, dict)
        },
        "personality_boundary": (
            "personality_slow_variables_convergence_not_prompt_persona_card"
        ),
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _normalize_category(category: str) -> str:
    normalized = str(category or "").strip().lower().lstrip("/")
    aliases = {
        "status": "state",
        "上下文": "context",
        "relation_context": "context",
        "情绪": "emotion",
        "affect": "emotion",
        "inner": "inner_environment",
        "homeostasis": "inner_environment",
        "内环境": "inner_environment",
        "关系": "relationship",
        "记忆": "memory",
        "梦境": "dream",
        "身体": "body",
        "语言": "language",
        "认知": "cognition",
        "意识": "consciousness",
        "conscious": "consciousness",
        "workspace": "consciousness",
        "思考": "thinking",
        "self_thinking": "thinking",
        "inner_speech": "thinking",
        "人格": "personality",
        "性格": "personality",
        "能力": "ability",
        "感知": "perception",
        "视觉": "perception",
        "vision": "perception",
        "visual": "perception",
        "主动": "proactive_voice",
        "主动语音": "proactive_voice",
        "proactive": "proactive_voice",
        "voice": "proactive_voice",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in STATE_INSPECTION_CATEGORIES:
        return "state"
    return normalized


def _runtime_ref(path: Path) -> str:
    parts = path.parts
    if "runtime" in parts:
        index = parts.index("runtime")
        return "/".join(parts[index:])
    return str(path)


def _extract_compact_value(entry: Any) -> dict[str, Any]:
    if isinstance(entry, dict) and entry.get("available") and isinstance(
        entry.get("value"), dict
    ):
        return dict(entry["value"])
    if isinstance(entry, dict):
        return dict(entry)
    return {}


def _extract_nested_value(entry: dict[str, Any], key: str) -> dict[str, Any]:
    value = entry.get(key)
    return value if isinstance(value, dict) else {}


def _tier_refs(entry: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in keys:
        value = entry.get(key)
        if isinstance(value, dict):
            result[key] = _compact_value(value)
        elif isinstance(value, list):
            result[key] = value[:12]
        elif value not in (None, ""):
            result[key] = value
    return result


def _count_any(value: Any) -> int:
    if isinstance(value, dict):
        return len(value)
    if isinstance(value, list):
        return len(value)
    if isinstance(value, tuple):
        return len(value)
    if isinstance(value, str):
        return 1 if value.strip() else 0
    if value:
        return 1
    return 0


def _list_refs(value: Any, limit: int = 12) -> list[Any]:
    if isinstance(value, list):
        return value[:limit]
    if value in (None, ""):
        return []
    return [value]


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None
