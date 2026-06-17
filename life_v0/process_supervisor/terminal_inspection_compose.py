from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state_inspection import (
    _collect_language_generation_consumption_summary,
    _collect_relation_context_summary,
    _collect_self_thinking_summary,
    build_resident_state_inspection,
)


COMPOSITE_CATEGORIES = frozenset(
    {
        "me",
        "turn",
        "recall",
        "express",
        "carry",
        "background",
        "converge",
    }
)


def build_composite_state_inspection(
    *,
    terminal_dir: Path,
    category: str,
) -> dict[str, Any]:
    normalized = str(category or "").strip().lower().lstrip("/")
    builders = {
        "me": _build_me_inspection,
        "turn": _build_turn_inspection,
        "recall": _build_recall_inspection,
        "express": _build_express_inspection,
        "carry": _build_carry_inspection,
        "background": _build_background_inspection,
        "converge": _build_converge_inspection,
    }
    builder = builders.get(normalized)
    if builder is None:
        return {
            "schema_version": "resident_state_inspection_v0",
            "category": normalized,
            "inspection_scope": "terminal_view_only_not_relation_turn",
            "error": "unknown_composite_category",
        }
    return builder(terminal_dir=terminal_dir)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _build_me_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    state_root = terminal_dir.parent
    loop = _read_json(terminal_dir / "terminal_life_loop_state.json")
    lifecycle = _read_json(terminal_dir / "resident_lifecycle_state.json")
    language = build_resident_state_inspection(terminal_dir=terminal_dir, category="language")
    relationship = build_resident_state_inspection(terminal_dir=terminal_dir, category="relationship")
    memory = build_resident_state_inspection(terminal_dir=terminal_dir, category="memory")
    dream = build_resident_state_inspection(terminal_dir=terminal_dir, category="dream")
    state = build_resident_state_inspection(terminal_dir=terminal_dir, category="state")
    lang_summary = _extract_language_summary(language)
    rel_payload = relationship.get("relationship") if isinstance(relationship.get("relationship"), dict) else {}
    mem_payload = memory.get("memory") if isinstance(memory.get("memory"), dict) else {}
    dream_payload = dream.get("dream") if isinstance(dream.get("dream"), dict) else {}
    state_payload = state.get("state") if isinstance(state.get("state"), dict) else {}
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "me",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_me_overview_v0",
        "me": {
            "life_name": lifecycle.get("life_name") or loop.get("life_name"),
            "lifecycle_status": lifecycle.get("status"),
            "waiting_mode": loop.get("current_mode") or loop.get("resident_waiting_mode"),
            "last_live_semantic_focus": loop.get("last_live_semantic_focus"),
            "relationship_stage": _nested(rel_payload, ["relationship_subject_graph", "subjects", 0, "relationship_stage"]),
            "semantic_focus": lang_summary.get("semantic_focus"),
            "expression_posture": lang_summary.get("expression_monitor_status"),
            "model_expression_status": lang_summary.get("model_expression_status"),
            "memory_recall_mode": _nested(mem_payload, ["memory_retrieval", "retrieval_mode"]),
            "dream_residue_present": bool(_nested(dream_payload, ["exit_dream_consolidation_summary"])),
            "autonomous_next_kind": _nested(state_payload, ["resident_autonomous_activity_state", "covered_activity_kinds"]),
            "proactive_status": loop.get("resident_terminal_proactive_status"),
            "next_required_action": loop.get("next_required_action"),
            "honest_notes": [
                "检查面只读，不触发关系回合",
                "身体/信号在 live 会话中可能是启动快照，见 /body /signal",
            ],
        },
    }


def _build_turn_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    state_root = terminal_dir.parent
    language_dir = state_root / "language"
    loop = _read_json(terminal_dir / "terminal_life_loop_state.json")
    percept = _read_json(language_dir / "language_percept_frame.json")
    semantic = _read_json(language_dir / "semantic_map_frame.json")
    expression_plan = _read_json(language_dir / "expression_plan.json")
    model_state = _read_json(language_dir / "model_expression_state.json")
    language_section = {
        "language_percept": percept,
        "semantic_map": semantic,
        "expression_plan": expression_plan,
        "model_expression_state": model_state,
        "terminal_life_loop_state": loop,
    }
    lang_summary = _collect_language_generation_consumption_summary(language_section)
    gate = _nested(model_state, ["post_expression_gate"]) or {}
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "turn",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_last_turn_chain_v0",
        "turn": {
            "last_live_semantic_focus": loop.get("last_live_semantic_focus"),
            "last_external_utterance": loop.get("last_external_turn_utterance"),
            "last_life_utterance": loop.get("last_life_turn_utterance"),
            "semantic_focus": lang_summary.get("semantic_focus"),
            "memory_recall_refs": semantic.get("memory_recall_refs"),
            "memory_grounding_refs": expression_plan.get("memory_grounding_refs"),
            "dream_fact_boundary": expression_plan.get("dream_fact_boundary"),
            "expression_goal": lang_summary.get("expression_plan_goal"),
            "expression_monitor_status": lang_summary.get("expression_monitor_status"),
            "model_expression_status": lang_summary.get("model_expression_status"),
            "post_expression_gate_status": gate.get("gate_status") or gate.get("status"),
            "expression_release_path": model_state.get("expression_release_path"),
            "expression_release_tier": model_state.get("expression_release_tier"),
            "missing_evidence_flags": gate.get("missing_evidence_flags"),
            "live_language_turn_refs": loop.get("live_language_turn_refs"),
        },
    }


def _build_recall_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    state_root = terminal_dir.parent
    retrieval = _read_json(state_root / "memory" / "memory_retrieval_frame.json")
    semantic = _read_json(state_root / "language" / "semantic_map_frame.json")
    plan = _read_json(state_root / "language" / "expression_plan.json")
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "recall",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_memory_recall_v0",
        "recall": {
            "retrieval_mode": retrieval.get("retrieval_mode"),
            "activated_engram_refs": retrieval.get("activated_engram_refs"),
            "cue_terms": retrieval.get("cue_terms"),
            "reconstruction_focus": retrieval.get("reconstruction_focus"),
            "semantic_map_memory_recall_refs": semantic.get("memory_recall_refs"),
            "expression_plan_grounding_refs": plan.get("memory_grounding_refs"),
            "recall_reached_semantic_map": bool(semantic.get("memory_recall_refs")),
            "recall_reached_expression_plan": bool(plan.get("memory_grounding_refs")),
        },
    }


def _build_express_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    state_root = terminal_dir.parent
    plan = _read_json(state_root / "language" / "expression_plan.json")
    monitor = _read_json(state_root / "language" / "expression_monitor_state.json")
    model_state = _read_json(state_root / "language" / "model_expression_state.json")
    gate = _nested(model_state, ["post_expression_gate"]) or {}
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "express",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_expression_release_v0",
        "express": {
            "semantic_goal": plan.get("semantic_goal"),
            "expression_tempo_mode": plan.get("expression_tempo_mode"),
            "release_caution_level": plan.get("release_caution_level"),
            "fatigue_pressure": plan.get("fatigue_pressure"),
            "delay_or_release_decision": monitor.get("delay_or_release_decision"),
            "monitor_status": monitor.get("monitor_status"),
            "queue_e_repair_pressure_level": plan.get("queue_e_repair_pressure_level"),
            "model_expression_status": model_state.get("model_expression_status"),
            "post_expression_gate_status": gate.get("gate_status") or gate.get("status"),
            "missing_evidence_flags": gate.get("missing_evidence_flags"),
            "can_speak_naturally": (
                gate.get("gate_status") or gate.get("status")
            )
            == "accepted"
            and model_state.get("model_expression_status") == "model_expression_applied",
        },
    }


def _build_carry_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    state_root = terminal_dir.parent
    reports_dir = state_root.parent / "reports" / "latest"
    context = build_resident_state_inspection(terminal_dir=terminal_dir, category="context")
    ctx_payload = context.get("context") if isinstance(context.get("context"), dict) else {}
    resume = _read_json(reports_dir / "resumed_external_dialogue_packet.json")
    accumulation = _read_json(terminal_dir / "context_accumulation_window.json")
    rel_summary = _collect_relation_context_summary(ctx_payload)
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "carry",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_cross_wake_carry_v0",
        "carry": {
            "relation_role": rel_summary.get("relation_role"),
            "relationship_stage": rel_summary.get("relationship_stage"),
            "semantic_focus": rel_summary.get("semantic_focus"),
            "shared_term_surfaces": rel_summary.get("shared_term_surfaces"),
            "relationship_timeline_restore_refs": resume.get("relationship_timeline_restore_refs"),
            "commitment_expression_restore_refs": resume.get("commitment_expression_restore_refs"),
            "apology_repair_restore_refs": resume.get("apology_repair_restore_refs"),
            "live_language_turn_refs": resume.get("live_language_turn_refs")
            or accumulation.get("live_language_turn_refs"),
            "language_event_bundle_ref": resume.get("language_event_bundle_ref"),
        },
    }


def _build_background_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    state = build_resident_state_inspection(terminal_dir=terminal_dir, category="state")
    dream = build_resident_state_inspection(terminal_dir=terminal_dir, category="dream")
    growth = build_resident_state_inspection(terminal_dir=terminal_dir, category="growth")
    proactive = build_resident_state_inspection(terminal_dir=terminal_dir, category="proactive_voice")
    thinking = build_resident_state_inspection(terminal_dir=terminal_dir, category="thinking")
    state_payload = state.get("state") if isinstance(state.get("state"), dict) else {}
    auto = _nested(state_payload, ["resident_autonomous_activity_state"]) or {}
    thinking_payload = thinking.get("thinking") if isinstance(thinking.get("thinking"), dict) else {}
    thinking_summary = _collect_self_thinking_summary(thinking_payload)
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "background",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_background_activity_v0",
        "background": {
            "activity_count": auto.get("activity_count"),
            "covered_activity_kinds": auto.get("covered_activity_kinds"),
            "missing_activity_kinds": auto.get("missing_activity_kinds"),
            "cycle_coverage_complete": auto.get("cycle_coverage_complete"),
            "thinking_mode": thinking_summary.get("thinking_mode"),
            "thinking_status": thinking_summary.get("thinking_status"),
            "thinking_honest_note": "self_thinking 当前多为活动记账，见代码 resident_autonomous_activity",
            "proactive_status": _nested(proactive.get("proactive_voice"), ["resident_terminal_proactive_state", "status"]),
            "web_dream_status": _nested(dream.get("dream"), ["web_dream_learning_state", "status"]),
            "growth_shadow_only": True,
        },
    }


def _build_converge_inspection(*, terminal_dir: Path) -> dict[str, Any]:
    personality = build_resident_state_inspection(terminal_dir=terminal_dir, category="personality")
    language = build_resident_state_inspection(terminal_dir=terminal_dir, category="language")
    state_root = terminal_dir.parent
    plasticity = _read_json(state_root / "language" / "language_plasticity_update.json")
    rhythm = _read_json(state_root / "language" / "language_rhythm_trace.json")
    pers_payload = personality.get("personality") if isinstance(personality.get("personality"), dict) else {}
    return {
        "schema_version": "resident_state_inspection_v0",
        "category": "converge",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "summary_kind": "composite_slow_convergence_v0",
        "converge": {
            "trait_slow_variables": _nested(pers_payload, ["personality_convergence_summary", "trait_slow_variables"]),
            "trait_update_modes": _nested(pers_payload, ["personality_convergence_summary", "trait_update_modes"]),
            "promoted_shared_term_count": plasticity.get("promoted_shared_term_count"),
            "expression_tempo_mode": plasticity.get("expression_tempo_mode"),
            "tempo_history_count": len(rhythm.get("tempo_history", []))
            if isinstance(rhythm.get("tempo_history"), list)
            else 0,
            "shared_term_promotion_count": _extract_language_summary(language).get(
                "shared_term_promotion_count"
            ),
        },
    }


def _extract_language_summary(language_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = language_inspection.get("language")
    if not isinstance(payload, dict):
        return {}
    section = dict(payload)
    if "language_generation_consumption_summary" in section:
        nested = section["language_generation_consumption_summary"]
        if isinstance(nested, dict):
            return nested
    return _collect_language_generation_consumption_summary(section)


def _nested(value: Any, path: list[Any]) -> Any:
    current = value
    for key in path:
        if isinstance(key, int):
            if not isinstance(current, list) or key >= len(current):
                return None
            current = current[key]
            continue
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current
