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
        payload["context"] = _collect_files(
            state_root,
            {
                "life_context_frame": "terminal/life_context_frame.json",
                "relation_turn_frame": "terminal/relation_turn_frame.json",
                "language_percept": "language/language_percept_frame.json",
                "relationship_timeline": "relationship/relationship_timeline.json",
                "dialogue_memory_summary": "memory/dialogue_memory_summary.json",
            },
        )
    elif normalized == "memory":
        memory = _collect_files(
            state_root,
            {
                "relationship_memory": "memory/relationship_memory.json",
                "dialogue_memory_summary": "memory/dialogue_memory_summary.json",
                "engram_index": "memory/engram_index.json",
                "autobiographical_stack": "self/autobiographical_stack.json",
            },
        )
        payload["memory"] = memory
        payload["memory"]["tiering"] = _collect_memory_tiering(memory)
        payload["memory"]["tier_summary"] = _collect_memory_tier_summary(memory)
    elif normalized == "dream":
        dream = _collect_files(
            state_root,
            {
                "exit_dream_consolidation_summary": (
                    "dream/exit_dream_consolidation_summary.json"
                ),
                "dream_experience_window": "dream/dream_experience_window.json",
                "wake_integration_frame": "dream/wake_integration_frame.json",
                "dream_fact_gate_decision": "dream/dream_fact_gate_decision.json",
                "web_dream_learning_state": "dream/web_dream_learning_state.json",
                "resident_sleep_cycle_state": (
                    "terminal/resident_sleep_cycle_state.json"
                ),
            },
        )
        payload["dream"] = dream
        payload["dream"]["memory_tiering"] = _collect_memory_tiering(dream)
        payload["dream"]["tier_summary"] = _collect_memory_tier_summary(dream)
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
        payload["relationship"] = _collect_files(
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
        payload["cognition"] = _collect_files(
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
    elif normalized == "personality":
        payload["personality"] = _collect_files(
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
    elif normalized == "ability":
        payload["ability"] = _collect_files(
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
    elif normalized == "perception":
        payload["perception"] = _collect_files(
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
    return {
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
