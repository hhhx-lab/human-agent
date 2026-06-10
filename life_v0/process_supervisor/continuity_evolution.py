from __future__ import annotations

import json
from typing import Any

from ..growth.offline_learning_profile import derive_offline_learning_profile
from ..membrane.queue_e_signals import derive_queue_e_signal_profile


RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
WORLD_CONTACT_SUMMARY_REF = "runtime/state/membrane/world_contact_summary.json"
PAIN_REGRET_REPAIR_REPORT_REF = "runtime/reports/latest/pain_regret_repair_report.json"
RESPONSIBILITY_LOOP_STATE_REF = "runtime/state/action/responsibility_loop_state.json"
NIGHTMARE_RISK_REF = "runtime/state/dream/nightmare_loop_risk.json"
BELIEF_LEARNING_PLAN_REF = "runtime/state/growth/belief_learning_plan.json"
LANGUAGE_LEARNING_PLAN_REF = "runtime/state/growth/language_learning_plan.json"
RELATIONSHIP_LEARNING_PLAN_REF = "runtime/state/growth/relationship_learning_plan.json"
TRAIT_DRIFT_MONITOR_REF = "runtime/state/body/trait_drift_monitor.json"


def evolve_relationship_and_self_model(
    *,
    generated_at: str,
    relationship_graph: dict[str, Any],
    self_model_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    apology_repair_language_trace: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    responsibility_loop_state = responsibility_loop_state or {}
    world_contact_summary = world_contact_summary or {}
    pain_regret_repair_report = pain_regret_repair_report or {}
    nightmare_risk = nightmare_risk or {}
    belief_learning_plan = belief_learning_plan or {}
    language_learning_plan = language_learning_plan or {}
    relationship_learning_plan = relationship_learning_plan or {}
    background_continuity_profile = background_continuity_profile or {}

    updated_relationship_graph = json.loads(json.dumps(relationship_graph))
    updated_self_model_state = json.loads(json.dumps(self_model_state))

    subject = _first_subject(updated_relationship_graph)
    if not subject:
        return {
            "relationship_graph": updated_relationship_graph,
            "self_model_state": updated_self_model_state,
        }

    dialogue_turn_count = len(relationship_timeline.get("dialogue_turn_refs", []))
    continuity_state = _continuity_state(relationship_timeline)
    trust_state = _trust_state(relationship_timeline)
    queue_e_signal_profile = derive_queue_e_signal_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    offline_learning_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    next_stage, stage_reason = _derive_relationship_stage(
        current_stage=str(subject.get("relationship_stage", "pre_activation")),
        dialogue_turn_count=dialogue_turn_count,
        continuity_state=continuity_state,
        trust_state=trust_state,
        queue_e_signal_profile=queue_e_signal_profile,
        offline_learning_profile=offline_learning_profile,
        background_continuity_profile=background_continuity_profile,
    )
    background_evidence_refs = _background_evidence_refs(background_continuity_profile)
    subject["relationship_stage"] = next_stage
    subject["relationship_stage_reason"] = stage_reason
    subject["relationship_stage_turn_count"] = dialogue_turn_count
    subject["relationship_stage_evidence_refs"] = _dedupe(
        [
            RELATIONSHIP_TIMELINE_REF,
            WORLD_CONTACT_SUMMARY_REF if world_contact_summary else "",
            PAIN_REGRET_REPAIR_REPORT_REF if pain_regret_repair_report else "",
            RESPONSIBILITY_LOOP_STATE_REF if responsibility_loop_state else "",
            NIGHTMARE_RISK_REF if nightmare_risk else "",
            BELIEF_LEARNING_PLAN_REF if belief_learning_plan else "",
            LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else "",
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else "",
        ]
        + background_evidence_refs
    )

    updated_self_model_state["trait_slow_variables"] = _evolve_trait_slow_variables(
        previous_variables=updated_self_model_state.get("trait_slow_variables", {}),
        generated_at=generated_at,
        relationship_stage=next_stage,
        dialogue_turn_count=dialogue_turn_count,
        continuity_state=continuity_state,
        trust_state=trust_state,
        queue_e_signal_profile=queue_e_signal_profile,
        offline_learning_profile=offline_learning_profile,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        background_continuity_profile=background_continuity_profile,
    )
    updated_self_model_state["growth_window_refs"] = _dedupe(
        list(updated_self_model_state.get("growth_window_refs", []))
        + [
            RELATIONSHIP_TIMELINE_REF + "#longitudinal_stage_gates",
            TRAIT_DRIFT_MONITOR_REF,
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else "",
            LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else "",
            BELIEF_LEARNING_PLAN_REF if belief_learning_plan else "",
        ]
        + background_evidence_refs
    )
    updated_self_model_state["last_relationship_stage"] = next_stage
    updated_self_model_state["last_trait_evolution_generated_at"] = generated_at
    updated_self_model_state["last_trait_evolution_reason"] = stage_reason
    return {
        "relationship_graph": updated_relationship_graph,
        "self_model_state": updated_self_model_state,
    }


def _derive_relationship_stage(
    *,
    current_stage: str,
    dialogue_turn_count: int,
    continuity_state: str,
    trust_state: str,
    queue_e_signal_profile: dict[str, Any],
    offline_learning_profile: dict[str, Any],
    background_continuity_profile: dict[str, Any],
) -> tuple[str, str]:
    repair_followup_required = bool(queue_e_signal_profile.get("repair_followup_required"))
    world_contact_release_posture = str(
        queue_e_signal_profile.get("world_contact_release_posture", "shadow_only_guarded")
    )
    queue_e_priority_band = str(queue_e_signal_profile.get("queue_e_priority_band", "baseline"))
    offline_pressure_level = str(
        offline_learning_profile.get("offline_learning_pressure_level", "quiet")
    )
    background_continuity_mode = str(
        background_continuity_profile.get("background_continuity_mode", "")
    )
    background_carryover_generation = _int_or_zero(
        background_continuity_profile.get("background_carryover_generation")
    )
    background_relationship_stage = str(
        background_continuity_profile.get("background_relationship_stage") or ""
    )
    background_relationship_stage_reason = str(
        background_continuity_profile.get("background_relationship_stage_reason") or ""
    )

    if (
        dialogue_turn_count >= 4
        and world_contact_release_posture == "confirmation_blocked"
    ):
        return (
            "boundary_guarded_repair",
            "confirmation_blocked_boundary_guard_after_multi_turn_dialogue",
        )
    if dialogue_turn_count >= 3 and (
        repair_followup_required
        or queue_e_priority_band in {"repair_guarded", "locked_repair_urgent"}
        or "repair" in continuity_state
    ):
        return ("repair_guarded_continuity", "repair_followup_required_after_multi_turn_dialogue")
    if dialogue_turn_count >= 6 and offline_pressure_level in {"quiet", "present"}:
        return (
            "shared_continuity",
            "shared_history_accumulated_without_active_repair_lock",
        )
    if dialogue_turn_count >= 2:
        return ("active_dialogue", "dialogue_turns_accumulated")
    if (
        background_relationship_stage
        and background_continuity_mode == "closed_process_carryover"
        and current_stage
        in {
            "pre_activation",
            "restored_waiting",
            "background_continuity_waiting",
            background_relationship_stage,
        }
    ):
        return (
            background_relationship_stage,
            background_relationship_stage_reason
            or "background_resume_relationship_stage_preserved_before_dialogue",
        )
    if (
        background_continuity_mode == "closed_process_carryover"
        and background_carryover_generation >= 2
        and current_stage in {
            "pre_activation",
            "restored_waiting",
            "background_continuity_waiting",
        }
    ):
        return (
            "background_continuity_waiting",
            "persistent_background_continuity_lineage_preserved_before_dialogue",
        )
    if current_stage == "restored_waiting":
        return ("restored_waiting", "restored_waiting_preserved_before_dialogue")
    if trust_state:
        return ("active_dialogue", "trust_trace_seeded_before_multi_turn_threshold")
    return ("pre_activation", "pre_activation_seed_preserved")


def _evolve_trait_slow_variables(
    *,
    previous_variables: dict[str, Any],
    generated_at: str,
    relationship_stage: str,
    dialogue_turn_count: int,
    continuity_state: str,
    trust_state: str,
    queue_e_signal_profile: dict[str, Any],
    offline_learning_profile: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    apology_repair_language_trace: dict[str, Any],
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    turn_scale = min(dialogue_turn_count / 6.0, 1.0)
    repair_scale = 1.0 if queue_e_signal_profile.get("repair_followup_required") else 0.0
    boundary_scale = _boundary_scale(
        str(queue_e_signal_profile.get("world_contact_release_posture", "shadow_only_guarded"))
    )
    offline_scale = _offline_scale(
        str(offline_learning_profile.get("offline_learning_pressure_level", "quiet"))
    )
    trust_bonus = 0.10 if trust_state == "repairing" else 0.05 if trust_state else 0.0
    continuity_bonus = 0.10 if "continuity" in continuity_state else 0.0
    repair_obligation_count = int(queue_e_signal_profile.get("repair_obligation_count", 0))
    regret_pressure_count = int(queue_e_signal_profile.get("regret_pressure_count", 0))
    background_generation_scale = _background_generation_scale(
        _int_or_zero(background_continuity_profile.get("background_carryover_generation"))
    )
    background_pressure_scale = _background_pressure_scale(
        str(background_continuity_profile.get("background_carryover_pressure_level", "light"))
    )
    background_trait_values = _background_trait_values(background_continuity_profile)
    background_trait_update_counts = _background_trait_update_counts(
        background_continuity_profile
    )
    evidence_refs = _dedupe(
        [
            RELATIONSHIP_TIMELINE_REF,
            WORLD_CONTACT_SUMMARY_REF,
            PAIN_REGRET_REPAIR_REPORT_REF,
            RESPONSIBILITY_LOOP_STATE_REF,
            commitment_expression_plan and "runtime/state/language/commitment_expression_plan.json",
            apology_repair_language_trace and "runtime/state/language/apology_repair_language_trace.json",
        ]
        + _background_evidence_refs(background_continuity_profile)
    )

    target_values = {
        "trust_persistence": _clamp(
            0.22
            + 0.32 * turn_scale
            + 0.10 * repair_scale
            + trust_bonus
            + 0.05 * continuity_bonus
            - 0.06 * boundary_scale
            + 0.04 * background_generation_scale
            + 0.03 * background_pressure_scale
        ),
        "dialogue_warmth": _clamp(
            0.24
            + 0.24 * turn_scale
            + 0.05 * (1.0 - repair_scale)
            - 0.08 * boundary_scale
            + 0.04 * continuity_bonus
            + 0.02 * background_generation_scale
        ),
        "repair_seriousness": _clamp(
            0.28
            + 0.22 * repair_scale
            + 0.08 * min(repair_obligation_count, 3)
            + 0.06 * min(regret_pressure_count, 3)
            + 0.08 * offline_scale
            + 0.04 * background_pressure_scale
        ),
        "boundary_respect": _clamp(
            0.26
            + 0.18 * boundary_scale
            + 0.10 * repair_scale
            + 0.06 * offline_scale
            + 0.03 * background_generation_scale
        ),
        "continuity_drive": _clamp(
            0.24
            + 0.24 * turn_scale
            + 0.08 * offline_scale
            + continuity_bonus
            + 0.06 * repair_scale
            + 0.08 * background_generation_scale
            + 0.05 * background_pressure_scale
        ),
    }

    updated: dict[str, Any] = {}
    for name, value in target_values.items():
        previous_payload = previous_variables.get(name, {})
        previous_value = _extract_previous_value(previous_payload)
        background_resume_value = background_trait_values.get(name)
        value, background_inertia_weight = _apply_background_trait_inertia(
            target_value=value,
            background_resume_value=background_resume_value,
            background_generation_scale=background_generation_scale,
            background_pressure_scale=background_pressure_scale,
        )
        trend_reference = previous_value
        if trend_reference is None:
            trend_reference = background_resume_value
        update_count = max(
            _extract_update_count(previous_payload),
            background_trait_update_counts.get(name, 0),
        )
        updated[name] = {
            "value": round(value, 3),
            "trend": _trend(trend_reference, value),
            "update_count": update_count + 1,
            "last_relationship_stage": relationship_stage,
            "last_generated_at": generated_at,
            "evidence_refs": evidence_refs,
        }
        if background_resume_value is not None:
            updated[name]["background_resume_value"] = round(background_resume_value, 3)
            updated[name]["background_inertia_weight"] = round(
                background_inertia_weight,
                3,
            )
    return updated


def _first_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}


def _continuity_state(relationship_timeline: dict[str, Any]) -> str:
    reports = relationship_timeline.get("relationship_continuity_reports", [])
    if reports and isinstance(reports[0], dict):
        return str(reports[0].get("continuity_state", ""))
    return ""


def _trust_state(relationship_timeline: dict[str, Any]) -> str:
    trajectories = relationship_timeline.get("trust_trajectories", [])
    if trajectories and isinstance(trajectories[0], dict):
        return str(trajectories[0].get("current_trust_state", ""))
    return ""


def _boundary_scale(world_contact_release_posture: str) -> float:
    if world_contact_release_posture == "confirmation_blocked":
        return 1.0
    if world_contact_release_posture == "shadow_only_guarded":
        return 0.35
    return 0.0


def _offline_scale(offline_learning_pressure_level: str) -> float:
    mapping = {
        "quiet": 0.0,
        "present": 0.25,
        "elevated": 0.5,
        "urgent": 0.75,
    }
    return mapping.get(offline_learning_pressure_level, 0.0)


def _background_generation_scale(background_carryover_generation: int) -> float:
    if background_carryover_generation >= 3:
        return 1.0
    if background_carryover_generation == 2:
        return 0.6
    if background_carryover_generation == 1:
        return 0.2
    return 0.0


def _background_pressure_scale(background_carryover_pressure_level: str) -> float:
    mapping = {
        "light": 0.0,
        "present": 0.35,
        "elevated": 0.6,
    }
    return mapping.get(background_carryover_pressure_level, 0.0)


def _background_evidence_refs(background_continuity_profile: dict[str, Any]) -> list[str]:
    return _dedupe(
        list(background_continuity_profile.get("background_continuity_ref_set", []))
        + list(background_continuity_profile.get("background_carryover_source_ref_set", []))
        + list(
            background_continuity_profile.get(
                "background_relationship_stage_evidence_refs",
                [],
            )
        )
        + [
            background_continuity_profile.get("background_relationship_subject_ref", ""),
            background_continuity_profile.get("background_self_model_ref", ""),
        ]
    )


def _extract_previous_value(previous_payload: Any) -> float | None:
    if isinstance(previous_payload, dict):
        value = previous_payload.get("value")
        if isinstance(value, (int, float)):
            return float(value)
        return None
    if isinstance(previous_payload, (int, float)):
        return float(previous_payload)
    return None


def _extract_update_count(previous_payload: Any) -> int:
    if isinstance(previous_payload, dict):
        count = previous_payload.get("update_count")
        if isinstance(count, int):
            return count
    return 0


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _background_trait_values(
    background_continuity_profile: dict[str, Any],
) -> dict[str, float]:
    summary = background_continuity_profile.get(
        "background_trait_slow_variable_summary",
        {},
    )
    if not isinstance(summary, dict):
        return {}
    values: dict[str, float] = {}
    for name, payload in summary.items():
        value: Any
        if isinstance(payload, dict):
            value = payload.get("value")
        else:
            value = payload
        if isinstance(value, (int, float)):
            values[str(name)] = _clamp(float(value))
    return values


def _background_trait_update_counts(
    background_continuity_profile: dict[str, Any],
) -> dict[str, int]:
    summary = background_continuity_profile.get(
        "background_trait_slow_variable_summary",
        {},
    )
    if not isinstance(summary, dict):
        return {}
    counts: dict[str, int] = {}
    for name, payload in summary.items():
        if isinstance(payload, dict) and isinstance(payload.get("update_count"), int):
            counts[str(name)] = payload["update_count"]
    return counts


def _apply_background_trait_inertia(
    *,
    target_value: float,
    background_resume_value: float | None,
    background_generation_scale: float,
    background_pressure_scale: float,
) -> tuple[float, float]:
    if background_resume_value is None:
        return target_value, 0.0
    inertia_weight = min(
        0.70,
        0.40 + 0.20 * background_generation_scale + 0.10 * background_pressure_scale,
    )
    return (
        _clamp(
            (1.0 - inertia_weight) * target_value
            + inertia_weight * background_resume_value
        ),
        inertia_weight,
    )


def _trend(previous_value: float | None, current_value: float) -> str:
    if previous_value is None:
        return "seeded"
    delta = current_value - previous_value
    if delta >= 0.08:
        return "rising"
    if delta <= -0.08:
        return "falling"
    return "stable"


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _dedupe(items: list[Any]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result
