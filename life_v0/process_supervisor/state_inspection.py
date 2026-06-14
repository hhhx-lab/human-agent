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
        payload["body"] = _collect_files(
            state_root,
            {
                "body_rhythm_pulse": "body/body_rhythm_pulse.json",
                "need_state_vector": "body/need_state_vector.json",
                "body_resource_budget": "body/body_resource_budget.json",
                "core_affect_vector": "body/core_affect_vector.json",
            },
        )
    elif normalized == "emotion":
        payload["emotion"] = _collect_files(
            state_root,
            {
                "core_affect_vector": "body/core_affect_vector.json",
                "emotion_regulation_loop": "body/emotion_regulation_loop.json",
                "pain_regret_repair_report": (
                    "../reports/latest/pain_regret_repair_report.json"
                ),
                "signal_media_runtime": "signal/signal_media_runtime.json",
            },
        )
    elif normalized == "inner_environment":
        payload["inner_environment"] = _collect_files(
            state_root,
            {
                "need_state_vector": "body/need_state_vector.json",
                "body_resource_budget": "body/body_resource_budget.json",
                "body_rhythm_pulse": "body/body_rhythm_pulse.json",
                "signal_media_runtime": "signal/signal_media_runtime.json",
                "idle_strategy": "terminal/idle_strategy_state.json",
            },
        )
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
        payload["language"] = _collect_files(
            state_root,
            {
                "language_percept": "language/language_percept_frame.json",
                "semantic_map": "language/semantic_map_frame.json",
                "inner_speech": "language/inner_speech_frame.json",
                "expression_monitor": "language/expression_monitor_state.json",
                "expression_plan": "language/expression_plan.json",
                "model_expression_state": "language/model_expression_state.json",
            },
        )
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
