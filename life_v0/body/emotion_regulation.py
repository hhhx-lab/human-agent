from __future__ import annotations

from typing import Any

from life_v0.body.emotion_episode import _pressure_value


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/real—live0/03_body_affect_homeostasis.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]

ROUTE_TO_MODE = {
    "reappraisal": "reappraisal_then_articulate",
    "expression_monitoring": "hold_then_articulate",
    "recovery_window": "recovery_window_hold",
    "clarification_hold": "clarification_hold_then_articulate",
    "action_slowdown": "slowdown_then_confirm",
    "dream_integration": "dream_consolidation_hold",
}


def resolve_emotion_regulation_profile(
    *,
    episode: dict[str, Any],
    core_affect: dict[str, Any] | None = None,
    recovery_path: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    core_affect = core_affect or {}
    recovery_path = recovery_path or {}
    body_resource_budget = body_resource_budget or {}

    regulation_route = episode.get("regulation_route", "expression_monitoring")
    arousal = _pressure_value(core_affect.get("arousal", 0.0))
    pain_pressure = _pressure_value(core_affect.get("pain_pressure", 0.0))
    fatigue_state = body_resource_budget.get("fatigue_state", {})
    fatigue_level = fatigue_state.get("level", "managed_low_noise")
    recovery_blocked = bool(recovery_path.get("blocked_reasons"))

    regulation_mode = ROUTE_TO_MODE.get(regulation_route, "hold_then_articulate")
    suppression_cost = 0.18
    expression_delay_required = episode.get("expression_risk") in {"guarded", "high_guard"}
    regulation_branch_reason = f"episode_route_{regulation_route}"

    if regulation_route == "recovery_window":
        suppression_cost = 0.28
        expression_delay_required = True
        regulation_branch_reason = "recovery_window_for_pain_or_repair_followup"
    elif regulation_route == "dream_integration":
        suppression_cost = 0.22
        regulation_branch_reason = "dream_consolidation_before_expression"
    elif regulation_route == "action_slowdown":
        suppression_cost = 0.32
        expression_delay_required = True
        regulation_branch_reason = "arousal_peak_action_slowdown"
    elif regulation_route == "reappraisal":
        suppression_cost = 0.2
        regulation_branch_reason = "reappraisal_before_relationship_clarification"
    elif arousal >= 0.7 and regulation_route == "expression_monitoring":
        regulation_mode = "slowdown_then_confirm"
        regulation_route = "action_slowdown"
        suppression_cost = 0.3
        expression_delay_required = True
        regulation_branch_reason = "arousal_override_to_action_slowdown"

    if fatigue_level in {"elevated", "high", "critical"} and regulation_route in {
        "expression_monitoring",
        "reappraisal",
    }:
        regulation_route = "recovery_window"
        regulation_mode = "recovery_window_hold"
        suppression_cost = max(suppression_cost, 0.26)
        expression_delay_required = True
        regulation_branch_reason = "fatigue_bias_to_recovery_window"

    if recovery_blocked and regulation_route != "dream_integration":
        suppression_cost = min(0.4, suppression_cost + 0.06)
        regulation_branch_reason = f"{regulation_branch_reason}_recovery_path_blocked"

    if pain_pressure >= 0.55 and regulation_route == "expression_monitoring":
        regulation_route = "recovery_window"
        regulation_mode = "recovery_window_hold"
        suppression_cost = max(suppression_cost, 0.27)
        expression_delay_required = True
        regulation_branch_reason = "pain_pressure_bias_to_recovery_window"

    return {
        "regulation_route": regulation_route,
        "regulation_mode": regulation_mode,
        "suppression_cost": round(suppression_cost, 3),
        "expression_delay_required": expression_delay_required,
        "regulation_branch_reason": regulation_branch_reason,
    }


def build_emotion_regulation_loop(
    *,
    run_id: str,
    generated_at: str,
    episode: dict[str, Any],
    recovery_path: dict[str, Any],
    core_affect: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profile = resolve_emotion_regulation_profile(
        episode=episode,
        core_affect=core_affect,
        recovery_path=recovery_path,
        body_resource_budget=body_resource_budget,
    )
    return {
        "schema_version": "emotion_regulation_loop_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "emotion_regulation_id": f"emotion-regulation-{run_id}",
        "episode_ref": "runtime/state/body/affective_episode.json",
        "regulation_route": profile["regulation_route"],
        "regulation_mode": profile["regulation_mode"],
        "regulation_branch_reason": profile["regulation_branch_reason"],
        "suppression_cost": profile["suppression_cost"],
        "expression_delay_required": profile["expression_delay_required"],
        "recovery_route_refs": ["runtime/state/body/recovery_path.json"],
        "emotion_regulation_boundary": (
            "structured_emotion_regulation_evidence_not_spoken_language"
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_emotion_regulation_from_live_turn(
    *,
    emotion_regulation: dict[str, Any] | None,
    generated_at: str,
    run_id: str,
    episode: dict[str, Any],
    core_affect_vector: dict[str, Any],
    recovery_path: dict[str, Any],
    body_resource_budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    regulation = build_emotion_regulation_loop(
        run_id=run_id,
        generated_at=generated_at,
        episode=episode,
        recovery_path=recovery_path,
        core_affect=core_affect_vector,
        body_resource_budget=body_resource_budget,
    )
    regulation["last_projected_from_live_turn_ref"] = (
        f"runtime/state/body/emotion_regulation_loop.json#live-turn-{run_id}"
    )
    regulation["live_emotion_regulation_refreshed"] = True
    if isinstance(emotion_regulation, dict):
        regulation["previous_regulation_mode"] = emotion_regulation.get("regulation_mode")
        regulation["previous_regulation_route"] = emotion_regulation.get("regulation_route")
    return regulation


def emotion_regulation_inspection_snapshot(
    *,
    affective_episode: dict[str, Any],
    emotion_regulation_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    terminal_life_loop_state = terminal_life_loop_state or {}
    return {
        "emotion_regulation_branch_present": bool(
            emotion_regulation_loop.get("regulation_mode")
        ),
        "regulation_route": emotion_regulation_loop.get("regulation_route")
        or affective_episode.get("regulation_route"),
        "regulation_mode": emotion_regulation_loop.get("regulation_mode"),
        "regulation_branch_reason": emotion_regulation_loop.get("regulation_branch_reason"),
        "expression_delay_required": emotion_regulation_loop.get("expression_delay_required"),
        "suppression_cost": emotion_regulation_loop.get("suppression_cost"),
        "episode_label": affective_episode.get("episode_label"),
        "episode_branch_reason": affective_episode.get("episode_branch_reason"),
        "live_emotion_regulation_refreshed": bool(
            emotion_regulation_loop.get("live_emotion_regulation_refreshed")
            or terminal_life_loop_state.get("live_emotion_regulation_refreshed")
        ),
        "emotion_regulation_branch_boundary": (
            "structured_emotion_regulation_evidence_not_spoken_language"
        ),
    }


def check_emotion_regulation_loop(regulation: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if regulation.get("schema_version") != "emotion_regulation_loop_v0":
        reasons.append("emotion_regulation_gate schema mismatch")
    for field in [
        "emotion_regulation_id",
        "episode_ref",
        "regulation_route",
        "regulation_mode",
        "regulation_branch_reason",
        "suppression_cost",
        "recovery_route_refs",
    ]:
        if field not in regulation or regulation.get(field) in ("", []):
            reasons.append(f"emotion_regulation_gate missing {field}")
    return reasons