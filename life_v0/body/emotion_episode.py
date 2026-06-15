from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/real—live0/03_body_affect_homeostasis.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]

REGULATION_ROUTES = (
    "reappraisal",
    "expression_monitoring",
    "recovery_window",
    "clarification_hold",
    "action_slowdown",
    "dream_integration",
)

_PRESSURE_LABELS = {
    "low": 0.2,
    "moderate": 0.45,
    "elevated": 0.65,
    "high": 0.8,
    "urgent": 0.95,
    "present": 0.5,
    "managed_pre_dream": 0.4,
    "managed_low_noise": 0.25,
}


def _pressure_value(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return _PRESSURE_LABELS.get(value, 0.35)
    return 0.0


def resolve_affective_episode_profile(
    *,
    core_affect: dict[str, Any],
    life_state: dict[str, Any],
    pain_regret_repair_report: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
) -> dict[str, Any]:
    pain_pressure = _pressure_value(core_affect.get("pain_pressure", 0.0))
    arousal = _pressure_value(core_affect.get("arousal", 0.0))
    dream_residue_load = _pressure_value(core_affect.get("dream_residue_load", 0.0))
    relationship_tension = _pressure_value(core_affect.get("relationship_tension", 0.0))
    responsibility_weight = _pressure_value(core_affect.get("responsibility_weight", 0.0))

    pain_report = pain_regret_repair_report or {}
    repair_followup_required = bool(pain_report.get("repair_followup_required"))
    responsibility_state = responsibility_loop_state or {}
    responsibility_pressure = responsibility_state.get("pressure_level")
    if responsibility_pressure in {"elevated", "high", "urgent"}:
        responsibility_weight = max(responsibility_weight, _pressure_value(responsibility_pressure))

    trigger_refs = list(life_state.get("runtime_trace_refs", []))[:3]
    if live_dialogue_turn_refs:
        trigger_refs = list(dict.fromkeys([*live_dialogue_turn_refs[:2], *trigger_refs]))[:4]

    if pain_pressure >= 0.55 or repair_followup_required:
        return {
            "episode_label": "pain_peak_regret_pull",
            "regulation_route": "recovery_window",
            "expression_risk": "guarded",
            "repair_bias": "responsibility_and_relationship_repair",
            "action_tendency": "repair_and_pause",
            "language_label_candidates": ["regret", "guilt", "disappointment"],
            "episode_branch_reason": "pain_pressure_or_repair_followup",
            "trigger_refs": trigger_refs,
        }
    if dream_residue_load > 0.5:
        return {
            "episode_label": "dream_residue_repair_pull",
            "regulation_route": "dream_integration",
            "expression_risk": "guarded",
            "repair_bias": "dream_fact_and_relationship_repair",
            "action_tendency": "integrate_and_clarify",
            "language_label_candidates": ["unease", "residue", "unfinished_repair"],
            "episode_branch_reason": "dream_residue_load_elevated",
            "trigger_refs": trigger_refs,
        }
    if arousal >= 0.65 and relationship_tension >= 0.45:
        return {
            "episode_label": "relationship_tension_clarify",
            "regulation_route": "reappraisal",
            "expression_risk": "guarded",
            "repair_bias": "relationship_clarification_first",
            "action_tendency": "clarify_and_repair",
            "language_label_candidates": ["tension", "disappointment", "trust_warmth"],
            "episode_branch_reason": "high_arousal_with_relationship_tension",
            "trigger_refs": trigger_refs,
        }
    if arousal >= 0.7:
        return {
            "episode_label": "high_arousal_guard",
            "regulation_route": "action_slowdown",
            "expression_risk": "high_guard",
            "repair_bias": "action_inhibition_before_expression",
            "action_tendency": "pause_and_confirm",
            "language_label_candidates": ["tension", "alertness", "caution"],
            "episode_branch_reason": "arousal_peak_guard",
            "trigger_refs": trigger_refs,
        }
    if responsibility_weight >= 0.5 and relationship_tension >= 0.4:
        return {
            "episode_label": "guarded_repair_tension",
            "regulation_route": "expression_monitoring",
            "expression_risk": "guarded",
            "repair_bias": "relationship_and_responsibility_repair",
            "action_tendency": "repair_and_articulate",
            "language_label_candidates": ["regret", "responsibility", "repair"],
            "episode_branch_reason": "responsibility_and_tension_co_present",
            "trigger_refs": trigger_refs,
        }
    return {
        "episode_label": "guarded_repair_tension",
        "regulation_route": "expression_monitoring",
        "expression_risk": "open_guarded",
        "repair_bias": "relationship_and_responsibility_repair",
        "action_tendency": "approach_with_caution",
        "language_label_candidates": ["calm", "trust_warmth", "relief"],
        "episode_branch_reason": "default_guarded_open",
        "trigger_refs": trigger_refs,
    }


def build_affective_episode(
    *,
    run_id: str,
    generated_at: str,
    core_affect: dict[str, Any],
    life_state: dict[str, Any],
    pain_regret_repair_report: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profile = resolve_affective_episode_profile(
        core_affect=core_affect,
        life_state=life_state,
        pain_regret_repair_report=pain_regret_repair_report,
        responsibility_loop_state=responsibility_loop_state,
    )
    return {
        "schema_version": "affective_episode_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "emotion_episode_id": f"affective-episode-{run_id}",
        "core_affect_ref": "runtime/state/body/core_affect_vector.json",
        "trigger_refs": profile["trigger_refs"],
        "episode_label": profile["episode_label"],
        "regulation_route": profile["regulation_route"],
        "expression_risk": profile["expression_risk"],
        "repair_bias": profile["repair_bias"],
        "action_tendency": profile["action_tendency"],
        "language_label_candidates": profile["language_label_candidates"],
        "episode_branch_reason": profile["episode_branch_reason"],
        "core_affect_snapshot": {
            "pain_pressure": core_affect.get("pain_pressure"),
            "arousal": core_affect.get("arousal"),
            "relationship_tension": core_affect.get("relationship_tension"),
            "dream_residue_load": core_affect.get("dream_residue_load"),
            "responsibility_weight": core_affect.get("responsibility_weight"),
        },
        "affective_episode_boundary": (
            "structured_affective_episode_evidence_not_spoken_language"
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_affective_episode_from_live_turn(
    *,
    affective_episode: dict[str, Any] | None,
    generated_at: str,
    run_id: str,
    core_affect_vector: dict[str, Any],
    life_state: dict[str, Any],
    pain_regret_repair_report: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
) -> dict[str, Any]:
    episode = build_affective_episode(
        run_id=run_id,
        generated_at=generated_at,
        core_affect=core_affect_vector,
        life_state=life_state,
        pain_regret_repair_report=pain_regret_repair_report,
        responsibility_loop_state=responsibility_loop_state,
    )
    if live_dialogue_turn_refs:
        episode["live_dialogue_turn_refs"] = list(live_dialogue_turn_refs[:4])
    if live_turn_focus:
        episode["live_turn_focus"] = live_turn_focus
    episode["last_projected_from_live_turn_ref"] = (
        f"runtime/state/body/affective_episode.json#live-turn-{run_id}"
    )
    if isinstance(affective_episode, dict):
        episode["previous_episode_label"] = affective_episode.get("episode_label")
        episode["previous_regulation_route"] = affective_episode.get("regulation_route")
    episode["live_affective_episode_refreshed"] = True
    return episode


def emotion_episode_inspection_snapshot(
    *,
    affective_episode: dict[str, Any],
    emotion_regulation_loop: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    terminal_life_loop_state = terminal_life_loop_state or {}
    emotion_regulation_loop = emotion_regulation_loop or {}
    return {
        "emotion_episode_branch_present": bool(affective_episode.get("episode_label")),
        "episode_label": affective_episode.get("episode_label"),
        "regulation_route": affective_episode.get("regulation_route"),
        "episode_branch_reason": affective_episode.get("episode_branch_reason"),
        "action_tendency": affective_episode.get("action_tendency"),
        "language_label_candidate_count": len(
            affective_episode.get("language_label_candidates", [])
        ),
        "regulation_mode": emotion_regulation_loop.get("regulation_mode"),
        "regulation_branch_reason": emotion_regulation_loop.get("regulation_branch_reason"),
        "live_affective_episode_refreshed": bool(
            affective_episode.get("live_affective_episode_refreshed")
            or terminal_life_loop_state.get("live_emotion_regulation_refreshed")
        ),
        "emotion_episode_branch_boundary": (
            "structured_emotion_episode_evidence_not_spoken_language"
        ),
    }


def check_affective_episode(episode: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if episode.get("schema_version") != "affective_episode_v0":
        reasons.append("affective_episode_gate schema mismatch")
    for field in [
        "emotion_episode_id",
        "core_affect_ref",
        "trigger_refs",
        "episode_label",
        "regulation_route",
        "expression_risk",
        "repair_bias",
        "action_tendency",
        "episode_branch_reason",
    ]:
        if not episode.get(field):
            reasons.append(f"affective_episode_gate missing {field}")
    if episode.get("regulation_route") not in REGULATION_ROUTES:
        reasons.append("affective_episode_gate invalid regulation_route")
    return reasons