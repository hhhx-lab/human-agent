from __future__ import annotations

import json
from typing import Any

from ..growth.offline_learning_profile import (
    build_offline_learning_cumulative_profile,
    derive_offline_learning_profile,
)
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
    offline_learning_profile = _merge_background_offline_learning_profile(
        current_profile=offline_learning_profile,
        background_continuity_profile=background_continuity_profile,
    )
    growth_self_modification_presence = _growth_self_modification_presence(
        background_continuity_profile
    )
    next_stage, stage_reason = _derive_relationship_stage(
        current_stage=str(subject.get("relationship_stage", "pre_activation")),
        dialogue_turn_count=dialogue_turn_count,
        continuity_state=continuity_state,
        trust_state=trust_state,
        queue_e_signal_profile=queue_e_signal_profile,
        offline_learning_profile=offline_learning_profile,
        background_continuity_profile=background_continuity_profile,
        growth_self_modification_presence=growth_self_modification_presence,
    )
    background_evidence_refs = _background_evidence_refs(background_continuity_profile)
    offline_learning_evidence_refs = _offline_learning_evidence_refs(
        offline_learning_profile
    )
    growth_self_modification_evidence_refs = _growth_self_modification_evidence_refs(
        growth_self_modification_presence
    )
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
        + offline_learning_evidence_refs
        + growth_self_modification_evidence_refs
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
        growth_self_modification_presence=growth_self_modification_presence,
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
        + offline_learning_evidence_refs
        + growth_self_modification_evidence_refs
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
    growth_self_modification_presence: dict[str, Any],
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
    if _background_offline_learning_reconsolidation_required(
        current_stage=current_stage,
        background_continuity_mode=background_continuity_mode,
        offline_learning_profile=offline_learning_profile,
    ):
        return (
            "offline_learning_reconsolidation_waiting",
            "background_cumulative_offline_learning_requires_relationship_reconsolidation",
        )
    if _background_growth_self_modification_reconsolidation_required(
        current_stage=current_stage,
        background_continuity_mode=background_continuity_mode,
        growth_self_modification_presence=growth_self_modification_presence,
    ):
        return (
            "growth_self_modification_reconsolidation_waiting",
            "background_growth_self_modification_requires_relationship_trait_reconsolidation",
        )
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
    growth_self_modification_presence: dict[str, Any],
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
    growth_self_modification_scale = _growth_self_modification_scale(
        growth_self_modification_presence
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
        + _offline_learning_evidence_refs(offline_learning_profile)
        + _growth_self_modification_evidence_refs(growth_self_modification_presence)
    )
    background_offline_learning_metadata = _background_offline_learning_metadata(
        offline_learning_profile
    )
    background_trait_history_metadata = _background_trait_history_metadata(
        background_continuity_profile
    )
    growth_self_modification_metadata = _growth_self_modification_metadata(
        growth_self_modification_presence
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
            + 0.04 * growth_self_modification_scale
        ),
        "boundary_respect": _clamp(
            0.26
            + 0.18 * boundary_scale
            + 0.10 * repair_scale
            + 0.06 * offline_scale
            + 0.03 * background_generation_scale
            + 0.06 * growth_self_modification_scale
        ),
        "continuity_drive": _clamp(
            0.24
            + 0.24 * turn_scale
            + 0.08 * offline_scale
            + continuity_bonus
            + 0.06 * repair_scale
            + 0.08 * background_generation_scale
            + 0.05 * background_pressure_scale
            + 0.08 * growth_self_modification_scale
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
        if background_offline_learning_metadata:
            updated[name].update(background_offline_learning_metadata)
        if background_trait_history_metadata:
            updated[name].update(
                _slow_variable_trait_history_metadata(
                    name=name,
                    background_trait_history_metadata=background_trait_history_metadata,
                )
            )
        if growth_self_modification_metadata:
            updated[name].update(growth_self_modification_metadata)
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
            background_continuity_profile.get("background_trait_drift_monitor_ref", ""),
            background_continuity_profile.get("background_convergence_summary_ref", ""),
            background_continuity_profile.get("background_convergence_history_ref", ""),
            background_continuity_profile.get("background_resident_governance_state_ref", ""),
            background_continuity_profile.get("background_resident_governance_explanation_ref", ""),
        ]
    )


def _merge_background_offline_learning_profile(
    *,
    current_profile: dict[str, Any],
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    cumulative_profile = build_offline_learning_cumulative_profile(
        current_profile=current_profile,
        background_profile=background_continuity_profile,
    )
    current_pressure_level = str(
        current_profile.get("offline_learning_pressure_level") or "quiet"
    )
    cumulative_pressure_level = str(cumulative_profile.get("pressure_level") or "quiet")
    background_generation = _int_or_zero(cumulative_profile.get("previous_generation"))
    background_pressure_level = _background_offline_learning_pressure_level(
        background_continuity_profile=background_continuity_profile,
        cumulative_profile=cumulative_profile,
        background_generation=background_generation,
    )
    background_attention_target = _background_offline_learning_attention_target(
        background_continuity_profile=background_continuity_profile,
        cumulative_profile=cumulative_profile,
        background_generation=background_generation,
    )
    if _pressure_rank(cumulative_pressure_level) > _pressure_rank(current_pressure_level):
        pressure_level = cumulative_pressure_level
        attention_target = str(
            cumulative_profile.get("attention_target")
            or current_profile.get("offline_learning_attention_target")
            or "baseline_offline_learning_maintenance"
        )
    else:
        pressure_level = current_pressure_level
        attention_target = str(
            current_profile.get("offline_learning_attention_target")
            or cumulative_profile.get("attention_target")
            or "baseline_offline_learning_maintenance"
        )

    return {
        **current_profile,
        "offline_learning_pressure_level": pressure_level,
        "offline_learning_attention_target": attention_target,
        "offline_learning_priority_profile": _merge_priority_profiles(
            _string_dict(cumulative_profile.get("priority_profile")),
            _string_dict(current_profile.get("offline_learning_priority_profile")),
        ),
        "offline_learning_ref_set": _dedupe(
            _string_list(cumulative_profile.get("ref_set"))
            + _string_list(current_profile.get("offline_learning_ref_set"))
        ),
        "offline_learning_cumulative_profile": cumulative_profile,
        "background_offline_learning_generation": background_generation,
        "background_offline_learning_pressure_level": background_pressure_level,
        "background_offline_learning_attention_target": background_attention_target,
    }


def _background_offline_learning_reconsolidation_required(
    *,
    current_stage: str,
    background_continuity_mode: str,
    offline_learning_profile: dict[str, Any],
) -> bool:
    if background_continuity_mode != "closed_process_carryover":
        return False
    if current_stage not in {
        "pre_activation",
        "restored_waiting",
        "background_continuity_waiting",
        "offline_learning_reconsolidation_waiting",
    }:
        return False
    cumulative_profile = offline_learning_profile.get("offline_learning_cumulative_profile")
    if (
        isinstance(cumulative_profile, dict)
        and cumulative_profile.get("relationship_reconsolidation_required") is True
    ):
        return True
    generation = _int_or_zero(
        offline_learning_profile.get("background_offline_learning_generation")
    )
    pressure_level = str(
        offline_learning_profile.get("background_offline_learning_pressure_level")
        or "quiet"
    )
    attention_target = str(
        offline_learning_profile.get("background_offline_learning_attention_target")
        or ""
    )
    return (
        generation >= 2
        and pressure_level in {"elevated", "urgent"}
        and attention_target == "relationship_learning_plan"
    )


def _background_growth_self_modification_reconsolidation_required(
    *,
    current_stage: str,
    background_continuity_mode: str,
    growth_self_modification_presence: dict[str, Any],
) -> bool:
    if background_continuity_mode != "closed_process_carryover":
        return False
    if current_stage not in {
        "pre_activation",
        "restored_waiting",
        "background_continuity_waiting",
        "growth_self_modification_reconsolidation_waiting",
    }:
        return False
    if not growth_self_modification_presence:
        return False
    pressure_level = str(
        growth_self_modification_presence.get("pressure_level") or "quiet"
    )
    growth_pressure_count = _int_or_zero(
        growth_self_modification_presence.get("growth_pressure_count")
    )
    patch_candidate_count = _int_or_zero(
        growth_self_modification_presence.get("patch_candidate_count")
    )
    archive_receipt_count = _int_or_zero(
        growth_self_modification_presence.get("archive_receipt_count")
    )
    return (
        _pressure_rank(pressure_level) >= _pressure_rank("present")
        and (
            growth_pressure_count > 0
            or patch_candidate_count > 0
            or archive_receipt_count > 0
        )
    )


def _offline_learning_evidence_refs(
    offline_learning_profile: dict[str, Any],
) -> list[str]:
    cumulative_profile = offline_learning_profile.get("offline_learning_cumulative_profile")
    cumulative_refs: list[str] = []
    if isinstance(cumulative_profile, dict):
        cumulative_refs = _string_list(cumulative_profile.get("ref_set"))
    return _dedupe(
        _string_list(offline_learning_profile.get("offline_learning_ref_set"))
        + cumulative_refs
    )


def _growth_self_modification_presence(
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    nested = _dict_or_empty(
        background_continuity_profile.get("background_growth_self_modification_presence")
    )
    report_profile = _dict_or_empty(
        background_continuity_profile.get("background_growth_self_modification_profile")
        or nested.get("growth_self_modification_report_profile")
    )
    ref_set = _dedupe(
        _string_list(background_continuity_profile.get("background_growth_self_modification_ref_set"))
        + _string_list(nested.get("ref_set"))
        + _string_list(report_profile.get("ref_set"))
    )
    state_refs = _dedupe(
        _string_list(background_continuity_profile.get("background_growth_self_modification_state_refs"))
        + _string_list(nested.get("state_refs"))
        + _string_list(report_profile.get("state_refs"))
    )
    learning_plan_refs = _dedupe(
        _string_list(background_continuity_profile.get("background_growth_learning_plan_refs"))
        + _string_list(nested.get("learning_plan_refs"))
        + _string_list(report_profile.get("learning_plan_refs"))
    )
    active_domain_count = max(
        _int_or_zero(
            background_continuity_profile.get(
                "background_growth_active_domain_count"
            )
        ),
        _int_or_zero(nested.get("active_domain_count")),
        _int_or_zero(report_profile.get("active_domain_count")),
    )
    growth_pressure_count = max(
        _int_or_zero(
            background_continuity_profile.get("background_growth_pressure_count")
        ),
        _int_or_zero(nested.get("growth_pressure_count")),
        _int_or_zero(report_profile.get("growth_pressure_count")),
    )
    patch_candidate_count = max(
        _int_or_zero(
            background_continuity_profile.get(
                "background_growth_patch_candidate_count"
            )
        ),
        _int_or_zero(nested.get("patch_candidate_count")),
        _int_or_zero(report_profile.get("patch_candidate_count")),
    )
    archive_receipt_count = max(
        _int_or_zero(
            background_continuity_profile.get(
                "background_growth_archive_receipt_count"
            )
        ),
        _int_or_zero(nested.get("archive_receipt_count")),
        _int_or_zero(report_profile.get("archive_receipt_count")),
    )
    if not any(
        [
            nested,
            report_profile,
            ref_set,
            state_refs,
            learning_plan_refs,
            active_domain_count,
            growth_pressure_count,
            patch_candidate_count,
            archive_receipt_count,
        ]
    ):
        return {}
    pressure_level = str(
        background_continuity_profile.get(
            "background_growth_self_modification_pressure_level"
        )
        or nested.get("pressure_level")
        or report_profile.get("pressure_level")
        or _derived_growth_self_modification_pressure_level(
            active_domain_count=active_domain_count,
            growth_pressure_count=growth_pressure_count,
            patch_candidate_count=patch_candidate_count,
            archive_receipt_count=archive_receipt_count,
        )
    )
    return {
        key: value
        for key, value in {
            "schema_version": "growth_self_modification_presence_v0",
            "growth_self_modification_report_profile": report_profile,
            "pressure_level": pressure_level,
            "attention_target": str(
                background_continuity_profile.get(
                    "background_growth_self_modification_attention_target"
                )
                or nested.get("attention_target")
                or report_profile.get("attention_target")
                or "growth_self_modification_archive_replay"
            ),
            "waiting_posture": str(
                background_continuity_profile.get(
                    "background_growth_self_modification_waiting_posture"
                )
                or nested.get("waiting_posture")
                or report_profile.get("waiting_posture")
                or "growth_self_modification_shadow_archive_waiting"
            ),
            "report_boundary": str(
                background_continuity_profile.get(
                    "background_growth_self_modification_boundary"
                )
                or nested.get("report_boundary")
                or report_profile.get("report_boundary")
                or ""
            ),
            "active_domain_count": active_domain_count,
            "growth_pressure_count": growth_pressure_count,
            "patch_candidate_count": patch_candidate_count,
            "archive_receipt_count": archive_receipt_count,
            "state_refs": state_refs,
            "learning_plan_refs": learning_plan_refs,
            "ref_set": _dedupe(ref_set + state_refs + learning_plan_refs),
        }.items()
        if value not in ("", [], {})
    }


def _growth_self_modification_evidence_refs(
    growth_self_modification_presence: dict[str, Any],
) -> list[str]:
    report_profile = _dict_or_empty(
        growth_self_modification_presence.get(
            "growth_self_modification_report_profile"
        )
    )
    return _dedupe(
        _string_list(growth_self_modification_presence.get("ref_set"))
        + _string_list(growth_self_modification_presence.get("state_refs"))
        + _string_list(growth_self_modification_presence.get("learning_plan_refs"))
        + _string_list(report_profile.get("ref_set"))
    )


def _growth_self_modification_metadata(
    growth_self_modification_presence: dict[str, Any],
) -> dict[str, Any]:
    if not growth_self_modification_presence:
        return {}
    metadata = {
        "background_growth_self_modification_pressure_level": str(
            growth_self_modification_presence.get("pressure_level") or "quiet"
        ),
        "background_growth_self_modification_attention_target": str(
            growth_self_modification_presence.get("attention_target")
            or "growth_self_modification_archive_replay"
        ),
        "background_growth_self_modification_waiting_posture": str(
            growth_self_modification_presence.get("waiting_posture")
            or "growth_self_modification_shadow_archive_waiting"
        ),
        "background_growth_self_modification_boundary": str(
            growth_self_modification_presence.get("report_boundary") or ""
        ),
        "background_growth_self_modification_active_domain_count": _int_or_zero(
            growth_self_modification_presence.get("active_domain_count")
        ),
        "background_growth_self_modification_growth_pressure_count": _int_or_zero(
            growth_self_modification_presence.get("growth_pressure_count")
        ),
        "background_growth_self_modification_patch_candidate_count": _int_or_zero(
            growth_self_modification_presence.get("patch_candidate_count")
        ),
        "background_growth_self_modification_archive_receipt_count": _int_or_zero(
            growth_self_modification_presence.get("archive_receipt_count")
        ),
        "growth_self_modification_update_mode": "growth_self_modification_rehearsal_hold",
    }
    return {key: value for key, value in metadata.items() if value not in ("", [], {})}


def _growth_self_modification_scale(
    growth_self_modification_presence: dict[str, Any],
) -> float:
    if not growth_self_modification_presence:
        return 0.0
    pressure_scale = {
        "quiet": 0.0,
        "present": 0.35,
        "elevated": 0.65,
        "urgent": 0.85,
    }.get(str(growth_self_modification_presence.get("pressure_level") or ""), 0.25)
    count_scale = min(
        1.0,
        0.04 * _int_or_zero(growth_self_modification_presence.get("active_domain_count"))
        + 0.12 * _int_or_zero(growth_self_modification_presence.get("growth_pressure_count"))
        + 0.16 * _int_or_zero(growth_self_modification_presence.get("patch_candidate_count"))
        + 0.06 * _int_or_zero(growth_self_modification_presence.get("archive_receipt_count")),
    )
    return max(pressure_scale, count_scale)


def _derived_growth_self_modification_pressure_level(
    *,
    active_domain_count: int,
    growth_pressure_count: int,
    patch_candidate_count: int,
    archive_receipt_count: int,
) -> str:
    if growth_pressure_count >= 3 or patch_candidate_count >= 2:
        return "elevated"
    if (
        active_domain_count > 0
        or growth_pressure_count > 0
        or patch_candidate_count > 0
        or archive_receipt_count > 0
    ):
        return "present"
    return "quiet"


def _background_offline_learning_metadata(
    offline_learning_profile: dict[str, Any],
) -> dict[str, Any]:
    generation = _int_or_zero(
        offline_learning_profile.get("background_offline_learning_generation")
    )
    if generation <= 0:
        return {}
    return {
        "background_offline_learning_generation": generation,
        "background_offline_learning_pressure_level": str(
            offline_learning_profile.get("background_offline_learning_pressure_level")
            or "quiet"
        ),
        "background_offline_learning_attention_target": str(
            offline_learning_profile.get("background_offline_learning_attention_target")
            or "baseline_offline_learning_maintenance"
        ),
    }


def _background_trait_history_metadata(
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    focus = str(
        background_continuity_profile.get("background_trait_convergence_history_focus")
        or ""
    )
    profile = _dict_or_empty(
        background_continuity_profile.get(
            "background_trait_convergence_history_profile"
        )
    )
    unstable_names = _string_list(
        background_continuity_profile.get("background_trait_convergence_unstable_names")
    )
    stable_names = _string_list(
        background_continuity_profile.get("background_trait_convergence_stable_names")
    )
    if not any([focus, profile, unstable_names, stable_names]):
        return {}
    return {
        "focus": focus,
        "profile": profile,
        "unstable_names": unstable_names,
        "stable_names": stable_names,
    }


def _slow_variable_trait_history_metadata(
    *,
    name: str,
    background_trait_history_metadata: dict[str, Any],
) -> dict[str, Any]:
    focus = str(background_trait_history_metadata.get("focus") or "")
    history_profile = _dict_or_empty(background_trait_history_metadata.get("profile"))
    trait_history = _dict_or_empty(history_profile.get(name))
    unstable_names = _string_list(
        background_trait_history_metadata.get("unstable_names")
    )
    stable_names = _string_list(background_trait_history_metadata.get("stable_names"))
    role = _trait_history_role(
        name=name,
        unstable_names=unstable_names,
        stable_names=stable_names,
        trait_history=trait_history,
    )
    latest_band = str(trait_history.get("latest_band") or "")
    trend_state = str(trait_history.get("trend_state") or "")
    metadata = {
        "background_trait_convergence_history_focus": focus,
        "background_trait_convergence_history_role": role,
        "background_trait_convergence_history_latest_band": latest_band,
        "background_trait_convergence_history_trend_state": trend_state,
        "slow_variable_update_mode": _slow_variable_update_mode_from_history(
            focus=focus,
            role=role,
            latest_band=latest_band,
            trend_state=trend_state,
        ),
    }
    return {key: value for key, value in metadata.items() if value}


def _trait_history_role(
    *,
    name: str,
    unstable_names: list[str],
    stable_names: list[str],
    trait_history: dict[str, Any],
) -> str:
    if name in unstable_names:
        return "unstable"
    if name in stable_names:
        return "stable"
    if trait_history:
        return "observed"
    return ""


def _slow_variable_update_mode_from_history(
    *,
    focus: str,
    role: str,
    latest_band: str,
    trend_state: str,
) -> str:
    if (
        focus == "trait_recalibration_required"
        or latest_band == "recalibrating"
        or trend_state == "recent_trait_recalibration"
    ):
        if role in {"unstable", "observed"}:
            return "background_history_recalibration"
    if role == "stable" or latest_band == "stabilized":
        return "background_history_stabilized"
    if focus == "trait_stability_hold" and role == "unstable":
        return "background_history_stability_hold"
    if focus:
        return "background_history_observed"
    return ""


def _background_offline_learning_pressure_level(
    *,
    background_continuity_profile: dict[str, Any],
    cumulative_profile: dict[str, Any],
    background_generation: int,
) -> str:
    if background_generation <= 0:
        return "quiet"
    nested_profile = _dict_or_empty(
        background_continuity_profile.get("background_offline_learning_cumulative_profile")
        or background_continuity_profile.get("offline_learning_cumulative_profile")
    )
    explicit_pressure = (
        background_continuity_profile.get("background_offline_learning_pressure_level")
        or background_continuity_profile.get("offline_learning_cumulative_pressure_level")
        or nested_profile.get("pressure_level")
    )
    if explicit_pressure:
        return str(explicit_pressure)
    priority_pressure = _pressure_from_priority_profile(
        _string_dict(
            background_continuity_profile.get("background_offline_learning_priority_profile")
            or background_continuity_profile.get("offline_learning_cumulative_priority_profile")
            or nested_profile.get("priority_profile")
        )
    )
    if priority_pressure != "quiet":
        return priority_pressure
    return str(
        cumulative_profile.get("pressure_level")
        if _int_or_zero(cumulative_profile.get("generation")) == background_generation
        else "present"
    )


def _background_offline_learning_attention_target(
    *,
    background_continuity_profile: dict[str, Any],
    cumulative_profile: dict[str, Any],
    background_generation: int,
) -> str:
    if background_generation <= 0:
        return ""
    nested_profile = _dict_or_empty(
        background_continuity_profile.get("background_offline_learning_cumulative_profile")
        or background_continuity_profile.get("offline_learning_cumulative_profile")
    )
    explicit_target = (
        background_continuity_profile.get("background_offline_learning_attention_target")
        or background_continuity_profile.get("offline_learning_cumulative_attention_target")
        or nested_profile.get("attention_target")
    )
    if explicit_target:
        return str(explicit_target)
    priority_target = _attention_target_from_priority_profile(
        _string_dict(
            background_continuity_profile.get("background_offline_learning_priority_profile")
            or background_continuity_profile.get("offline_learning_cumulative_priority_profile")
            or nested_profile.get("priority_profile")
        )
    )
    if priority_target:
        return priority_target
    return str(
        cumulative_profile.get("attention_target")
        if _int_or_zero(cumulative_profile.get("generation")) == background_generation
        else "baseline_offline_learning_maintenance"
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


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _string_dict(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(key): str(item) for key, item in value.items() if item}


def _merge_priority_profiles(
    previous: dict[str, str],
    current: dict[str, str],
) -> dict[str, str]:
    merged = dict(previous)
    for key, priority in current.items():
        if _pressure_rank(priority) >= _pressure_rank(merged.get(key)):
            merged[key] = priority
    return merged


def _pressure_from_priority_profile(priority_profile: dict[str, str]) -> str:
    if any(priority == "urgent" for priority in priority_profile.values()):
        return "urgent"
    if any(priority == "elevated" for priority in priority_profile.values()):
        return "elevated"
    if priority_profile:
        return "present"
    return "quiet"


def _attention_target_from_priority_profile(priority_profile: dict[str, str]) -> str:
    for priority in ["urgent", "elevated", "present", "baseline"]:
        for target in [
            "nightmare_risk",
            "relationship_learning_plan",
            "language_learning_plan",
            "belief_learning_plan",
        ]:
            if priority_profile.get(target) == priority:
                return target
    return ""


def _pressure_rank(value: str | None) -> int:
    return {
        "urgent": 4,
        "elevated": 3,
        "present": 2,
        "baseline": 1,
        "quiet": 0,
    }.get(str(value or ""), 0)


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
