from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .idle_strategy import extract_idle_governance_fields


RESIDENT_GOVERNANCE_EXPLANATION_REF = (
    "runtime/reports/latest/digital_life_resident_governance_explanation.json"
)


@dataclass(frozen=True)
class ResidentGovernanceExplanationResult:
    report: dict[str, Any]


def write_resident_governance_explanation(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    idle_strategy_ref: str | None,
    idle_strategy_state: dict[str, Any] | None,
    persistent_process_report_ref: str | None,
    resident_governance_report_ref: str | None,
    resident_governance_state_ref: str | None,
    resident_governance_snapshot_ref: str | None,
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
    exit_reason: str,
    write_json: Callable[[Path, dict[str, Any]], None],
    relationship_resume_summary: dict[str, Any] | None = None,
    trait_slow_variable_summary: dict[str, Any] | None = None,
    background_convergence_summary_ref: str | None = None,
    background_convergence_history_ref: str | None = None,
) -> ResidentGovernanceExplanationResult:
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
    background_carryover_generation = _int_or_zero(
        idle_governance.get("background_carryover_generation")
    )
    relationship_resume = _relationship_resume_summary(
        idle_governance=idle_governance,
        relationship_resume_summary=relationship_resume_summary,
    )
    trait_summary = _trait_slow_variable_summary(
        idle_governance=idle_governance,
        trait_slow_variable_summary=trait_slow_variable_summary,
    )
    background_convergence = _background_convergence_summary(
        idle_governance=idle_governance,
        explicit_summary_ref=background_convergence_summary_ref,
    )
    offline_learning_cumulative_focus = _offline_learning_cumulative_focus(
        idle_governance
    )
    dominant_driver_family = _dominant_driver_family(idle_governance)
    next_wake_expectation = _next_wake_expectation(
        dominant_driver_family=dominant_driver_family
    )
    identity_consciousness_birth_refs = _identity_consciousness_birth_refs(idle_governance)
    report = {
        "schema_version": "digital_life_resident_governance_explanation_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "explanation_id": f"resident-governance-explanation-{run_id}",
        "idle_strategy_ref": idle_strategy_ref,
        "persistent_process_report_ref": persistent_process_report_ref,
        "resident_governance_report_ref": resident_governance_report_ref,
        "resident_governance_state_ref": resident_governance_state_ref,
        "resident_governance_snapshot_ref": resident_governance_snapshot_ref,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "exit_reason": exit_reason,
        "dominant_driver_family": dominant_driver_family,
        "next_wake_expectation": next_wake_expectation,
        "background_continuity_active": bool(
            idle_governance.get("background_continuity_mode")
        ),
        "background_carryover_generation": background_carryover_generation,
        "background_carryover_parent_run_id": idle_governance.get(
            "background_carryover_parent_run_id"
        ),
        "background_carryover_source_ref_set": list(
            idle_governance.get("background_carryover_source_ref_set", [])
        ),
        "background_lineage_depth_band": idle_governance.get(
            "background_lineage_depth_band"
        ),
        "background_lineage_waiting_posture": idle_governance.get(
            "background_lineage_waiting_posture"
        ),
        "background_lineage_cadence_weight": idle_governance.get(
            "background_lineage_cadence_weight"
        ),
        "background_lineage_evidence_ref_count": idle_governance.get(
            "background_lineage_evidence_ref_count"
        ),
        "background_lineage_governance_profile": idle_governance.get(
            "background_lineage_governance_profile",
            {},
        ),
        "background_relationship_stage": relationship_resume.get(
            "relationship_stage"
        ),
        "background_relationship_stage_reason": relationship_resume.get(
            "relationship_stage_reason"
        ),
        "background_relationship_subject_ref": relationship_resume.get(
            "relationship_subject_ref"
        ),
        "background_self_model_ref": (
            idle_governance.get("background_self_model_ref")
            if trait_summary
            else None
        ),
        "background_trait_slow_variable_summary": trait_summary,
        "background_convergence_summary_ref": background_convergence.get(
            "background_convergence_summary_ref"
        ),
        "background_convergence_history_ref": (
            background_convergence_history_ref
            or idle_governance.get("background_convergence_history_ref")
        ),
        "background_convergence_history_trend_state": idle_governance.get(
            "background_convergence_history_trend_state"
        ),
        "background_convergence_history_window_size": idle_governance.get(
            "background_convergence_history_window_size"
        ),
        "background_dominant_convergence_pressure_level": idle_governance.get(
            "background_dominant_convergence_pressure_level"
        ),
        "background_dominant_convergence_state": idle_governance.get(
            "background_dominant_convergence_state"
        ),
        "background_trait_convergence_history_focus": idle_governance.get(
            "background_trait_convergence_history_focus"
        ),
        "background_trait_convergence_unstable_names": list(
            idle_governance.get("background_trait_convergence_unstable_names", [])
        ),
        "background_trait_convergence_stable_names": list(
            idle_governance.get("background_trait_convergence_stable_names", [])
        ),
        "background_trait_convergence_history_profile": idle_governance.get(
            "background_trait_convergence_history_profile", {}
        ),
        "background_convergence_state": background_convergence.get(
            "background_convergence_state"
        ),
        "background_convergence_pressure_level": background_convergence.get(
            "background_convergence_pressure_level"
        ),
        "background_convergence_attention_target": background_convergence.get(
            "background_convergence_attention_target"
        ),
        "background_relationship_stage_continuity": background_convergence.get(
            "background_relationship_stage_continuity"
        ),
        "background_trait_convergence_score": background_convergence.get(
            "background_trait_convergence_score"
        ),
        "background_trait_convergence_summary": background_convergence.get(
            "background_trait_convergence_summary",
            {},
        ),
        "background_resume_focus": _background_resume_focus(
            relationship_resume=relationship_resume,
            trait_slow_variable_summary=trait_summary,
        ),
        "background_convergence_focus": _background_convergence_focus(
            background_convergence
        ),
        "offline_learning_cumulative_focus": offline_learning_cumulative_focus,
        "queue_f_focus_active": bool(identity_consciousness_birth_refs),
        "identity_consciousness_birth_refs": identity_consciousness_birth_refs,
        "continuity_story": _compose_continuity_story(
            idle_governance=idle_governance,
            dominant_driver_family=dominant_driver_family,
            next_wake_expectation=next_wake_expectation,
            background_carryover_generation=background_carryover_generation,
            relationship_resume=relationship_resume,
            trait_slow_variable_summary=trait_summary,
            background_convergence=background_convergence,
            completed_turns=completed_turns,
            incident_count=incident_count,
            relaunch_recovery_count=relaunch_recovery_count,
        ),
    }
    report.update(idle_governance)
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(reports_dir / "digital_life_resident_governance_explanation.json", report)
    return ResidentGovernanceExplanationResult(report=report)


def _dominant_driver_family(idle_governance: dict[str, Any]) -> str:
    background_generation = _int_or_zero(
        idle_governance.get("background_carryover_generation")
    )
    background_mode = idle_governance.get("background_continuity_mode")
    attention_target = str(idle_governance.get("governance_attention_target") or "")
    attention_reason = str(idle_governance.get("governance_attention_reason") or "")
    convergence_state = str(
        idle_governance.get("background_convergence_state") or ""
    )
    convergence_pressure = str(
        idle_governance.get("background_convergence_pressure_level") or ""
    )
    convergence_attention_target = str(
        idle_governance.get("background_convergence_attention_target") or ""
    )
    convergence_history_trend = str(
        idle_governance.get("background_convergence_history_trend_state") or ""
    )
    convergence_target_active = (
        attention_target
        in {
            "relationship_stage_convergence",
            "trait_slow_variable_recalibration",
            "trait_slow_variable_convergence",
            "background_convergence_summary",
            "background_convergence_history_recalibration",
            "background_convergence_history_stability",
        }
        or (
            bool(convergence_attention_target)
            and attention_target == convergence_attention_target
        )
        or "background_convergence" in attention_reason
        or "cross_process_continuity" in attention_reason
    )
    birth_waiting_posture = str(idle_governance.get("birth_readiness_waiting_posture") or "")
    consciousness_waiting_posture = str(
        idle_governance.get("consciousness_waiting_posture") or ""
    )
    offline_learning_pressure = str(
        idle_governance.get("offline_learning_pressure_level") or ""
    )
    offline_learning_cumulative_pressure = str(
        idle_governance.get("offline_learning_cumulative_pressure_level") or ""
    )
    if _pressure_rank(offline_learning_cumulative_pressure) > _pressure_rank(
        offline_learning_pressure
    ):
        offline_learning_pressure = offline_learning_cumulative_pressure
    offline_pressure = str(idle_governance.get("offline_pressure_level") or "")
    repair_followup_required = bool(idle_governance.get("repair_followup_required"))

    if attention_target == "background_convergence_history_recalibration" or (
        convergence_history_trend
        in {"recent_recalibration_pressure", "elevated_pressure_watch"}
        and convergence_target_active
    ):
        return "background_history_recalibration_hold"
    if attention_target == "background_convergence_history_stability" or (
        convergence_history_trend == "integrating_cross_wake_convergence"
        and convergence_target_active
    ):
        return "background_history_stability_hold"
    if convergence_target_active and (
        convergence_pressure == "elevated"
        or convergence_state == "recalibrating_cross_process_continuity"
        or convergence_attention_target
        in {"relationship_stage_convergence", "trait_slow_variable_recalibration"}
    ):
        return "background_convergence_recalibration"
    if convergence_target_active and (
        convergence_pressure == "present"
        or convergence_attention_target == "trait_slow_variable_convergence"
    ):
        return "background_trait_convergence_hold"
    if background_mode and background_generation >= 2:
        return "persistent_background_continuity"
    if background_mode:
        return "background_continuity_carryover"
    if attention_target == "apology_repair_language_trace" or repair_followup_required:
        return "queue_e_repair_guard"
    if birth_waiting_posture == "birth_blocked_waiting" and (
        attention_target == "birth_readiness_stage_gate"
        or "birth_readiness" in attention_reason
    ):
        return "birth_readiness_repair_hold"
    if consciousness_waiting_posture == "consciousness_probe_blocked_waiting" and (
        attention_target == "consciousness_probe_bundle"
        or "consciousness" in attention_reason
    ):
        return "consciousness_probe_repair_hold"
    if (
        birth_waiting_posture == "birth_open_waiting"
        and attention_target == "birth_readiness_stage_gate"
    ):
        return "birth_readiness_presence_hold"
    if (
        consciousness_waiting_posture == "consciousness_reportable_waiting"
        and attention_target == "consciousness_probe_bundle"
    ):
        return "consciousness_reportable_presence"
    if offline_learning_pressure in {"urgent", "elevated", "present"}:
        return "offline_learning_reconsolidation"
    if offline_pressure in {"elevated", "present"}:
        return "replay_growth_reconsolidation"
    if attention_target in {"commitment_expression_plan", "relationship_timeline"}:
        return "long_horizon_language_continuity"
    if attention_reason == "no_long_horizon_language_refs":
        return "baseline_waiting_presence"
    return "resident_governance_hold"


def _next_wake_expectation(*, dominant_driver_family: str) -> str:
    if dominant_driver_family == "background_history_recalibration_hold":
        return "recalibrate_cross_wake_convergence_history_before_accepting_external_turn"
    if dominant_driver_family == "background_history_stability_hold":
        return "stabilize_cross_wake_convergence_history_before_accepting_external_turn"
    if dominant_driver_family == "background_convergence_recalibration":
        return "recalibrate_background_convergence_before_accepting_external_turn"
    if dominant_driver_family == "background_trait_convergence_hold":
        return "stabilize_background_trait_convergence_before_accepting_external_turn"
    if dominant_driver_family == "persistent_background_continuity":
        return "resume_background_lineage_before_accepting_external_turn"
    if dominant_driver_family == "background_continuity_carryover":
        return "reopen_background_carryover_before_accepting_external_turn"
    if dominant_driver_family == "queue_e_repair_guard":
        return "re_evaluate_repair_guard_before_world_contact_release"
    if dominant_driver_family == "birth_readiness_repair_hold":
        return "repair_birth_readiness_before_accepting_external_turn"
    if dominant_driver_family == "consciousness_probe_repair_hold":
        return "repair_consciousness_reportability_before_accepting_external_turn"
    if dominant_driver_family == "birth_readiness_presence_hold":
        return "re_enter_birth_readiness_presence_before_accepting_external_turn"
    if dominant_driver_family == "consciousness_reportable_presence":
        return "re_anchor_consciousness_probe_before_accepting_external_turn"
    if dominant_driver_family == "offline_learning_reconsolidation":
        return "re_enter_offline_learning_hold_before_accepting_external_turn"
    if dominant_driver_family == "replay_growth_reconsolidation":
        return "refresh_replay_growth_hold_before_accepting_external_turn"
    if dominant_driver_family == "long_horizon_language_continuity":
        return "re_anchor_long_horizon_language_before_accepting_external_turn"
    if dominant_driver_family == "baseline_waiting_presence":
        return "accept_external_turn_when_present"
    return "resume_waiting_governance_before_accepting_external_turn"


def _compose_continuity_story(
    *,
    idle_governance: dict[str, Any],
    dominant_driver_family: str,
    next_wake_expectation: str,
    background_carryover_generation: int,
    relationship_resume: dict[str, Any],
    trait_slow_variable_summary: dict[str, Any],
    background_convergence: dict[str, Any],
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
) -> list[str]:
    lines = [
        (
            "resident governance closed with "
            f"{completed_turns} completed dialogue turns, "
            f"{incident_count} incidents, and "
            f"{relaunch_recovery_count} relaunch recoveries"
        )
    ]
    attention_target = idle_governance.get("governance_attention_target") or "waiting_presence_maintenance"
    cadence_profile = idle_governance.get("governance_cadence_profile") or "baseline_waiting_presence"
    lines.append(
        "dominant attention target is "
        f"{attention_target} with cadence {cadence_profile}"
    )
    birth_waiting_posture = idle_governance.get("birth_readiness_waiting_posture")
    if birth_waiting_posture:
        birth_line = "birth readiness posture is " f"{birth_waiting_posture}"
        birth_decision = idle_governance.get("birth_readiness_decision")
        if birth_decision:
            birth_line += f" with decision {birth_decision}"
        birth_next_command = idle_governance.get("birth_readiness_next_required_command")
        if birth_next_command:
            birth_line += f" and next required command {birth_next_command}"
        lines.append(birth_line)
    consciousness_waiting_posture = idle_governance.get("consciousness_waiting_posture")
    if consciousness_waiting_posture:
        consciousness_line = "consciousness posture is " f"{consciousness_waiting_posture}"
        reportability_flags = list(idle_governance.get("consciousness_reportability_flags", []))
        if reportability_flags:
            consciousness_line += (
                " with reportability flags " + ", ".join(reportability_flags)
            )
        lines.append(consciousness_line)
    if idle_governance.get("background_continuity_mode"):
        lineage_line = (
            "background continuity is active at generation "
            f"{background_carryover_generation}"
        )
        if idle_governance.get("background_carryover_parent_run_id"):
            lineage_line += (
                " from parent run "
                f"{idle_governance['background_carryover_parent_run_id']}"
            )
        lines.append(lineage_line)
    if idle_governance.get("background_lineage_depth_band"):
        depth_line = (
            "background lineage depth band is "
            f"{idle_governance['background_lineage_depth_band']}"
        )
        if idle_governance.get("background_lineage_waiting_posture"):
            depth_line += (
                " with waiting posture "
                f"{idle_governance['background_lineage_waiting_posture']}"
            )
        if idle_governance.get("background_lineage_cadence_weight"):
            depth_line += (
                " and cadence weight "
                f"{idle_governance['background_lineage_cadence_weight']}"
            )
        lines.append(depth_line)
    if background_convergence.get("background_convergence_state"):
        convergence_line = (
            "background convergence state is "
            f"{background_convergence['background_convergence_state']}"
        )
        if background_convergence.get("background_convergence_pressure_level"):
            convergence_line += (
                " with pressure "
                f"{background_convergence['background_convergence_pressure_level']}"
            )
        if background_convergence.get("background_convergence_attention_target"):
            convergence_line += (
                " and attention target "
                f"{background_convergence['background_convergence_attention_target']}"
            )
        lines.append(convergence_line)
    if background_convergence.get("background_relationship_stage_continuity"):
        lines.append(
            "background relationship stage continuity is "
            f"{background_convergence['background_relationship_stage_continuity']}"
        )
    if background_convergence.get("background_trait_convergence_score") is not None:
        lines.append(
            "background trait convergence score is "
            f"{background_convergence['background_trait_convergence_score']}"
        )
    if idle_governance.get("background_convergence_history_trend_state"):
        history_line = (
            "background convergence history trend is "
            f"{idle_governance['background_convergence_history_trend_state']}"
        )
        if idle_governance.get("background_convergence_history_window_size"):
            history_line += (
                " across "
                f"{idle_governance['background_convergence_history_window_size']}"
                " wake samples"
            )
        if idle_governance.get("background_dominant_convergence_pressure_level"):
            history_line += (
                " with dominant pressure "
                f"{idle_governance['background_dominant_convergence_pressure_level']}"
            )
        lines.append(history_line)
    if idle_governance.get("background_trait_convergence_history_focus"):
        trait_history_line = (
            "background trait convergence history focus is "
            f"{idle_governance['background_trait_convergence_history_focus']}"
        )
        unstable_names = list(
            idle_governance.get("background_trait_convergence_unstable_names", [])
        )
        stable_names = list(
            idle_governance.get("background_trait_convergence_stable_names", [])
        )
        if unstable_names:
            trait_history_line += (
                " with unstable traits " + ", ".join(sorted(unstable_names))
            )
        if stable_names:
            trait_history_line += (
                " and stable traits " + ", ".join(sorted(stable_names))
            )
        lines.append(trait_history_line)
    offline_learning_cumulative_focus = _offline_learning_cumulative_focus(
        idle_governance
    )
    if offline_learning_cumulative_focus:
        offline_line = (
            "offline learning cumulative profile is generation "
            f"{offline_learning_cumulative_focus.get('generation', 0)}"
        )
        if offline_learning_cumulative_focus.get("pressure_level"):
            offline_line += (
                " with pressure "
                f"{offline_learning_cumulative_focus['pressure_level']}"
            )
        if offline_learning_cumulative_focus.get("attention_target"):
            offline_line += (
                " and attention target "
                f"{offline_learning_cumulative_focus['attention_target']}"
            )
        priority_names = offline_learning_cumulative_focus.get("priority_names", [])
        if priority_names:
            offline_line += " across " + ", ".join(priority_names)
        ref_count = offline_learning_cumulative_focus.get("ref_count")
        if ref_count:
            offline_line += f" with {ref_count} evidence refs"
        lines.append(offline_line)
    convergence_trait_summary = background_convergence.get(
        "background_trait_convergence_summary"
    )
    if isinstance(convergence_trait_summary, dict) and convergence_trait_summary:
        lines.append(
            "background convergence carries trait bands "
            + ", ".join(_trait_convergence_band_pairs(convergence_trait_summary))
        )
    if relationship_resume.get("relationship_stage"):
        relationship_line = (
            "background resume carries relationship stage "
            f"{relationship_resume['relationship_stage']}"
        )
        if relationship_resume.get("relationship_stage_reason"):
            relationship_line += (
                " because "
                f"{relationship_resume['relationship_stage_reason']}"
            )
        lines.append(relationship_line)
    if trait_slow_variable_summary:
        lines.append(
            "background resume carries trait slow variables "
            + ", ".join(sorted(trait_slow_variable_summary.keys()))
        )
    if idle_governance.get("background_trait_drift_monitor_ref"):
        lines.append(
            "background resume carries trait drift monitor ref "
            f"{idle_governance['background_trait_drift_monitor_ref']}"
        )
    lines.append(
        "dominant driver family is "
        f"{dominant_driver_family} and next wake should {next_wake_expectation}"
    )
    return lines


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _identity_consciousness_birth_refs(idle_governance: dict[str, Any]) -> list[str]:
    return [
        ref
        for ref in [
            idle_governance.get("workspace_frame_ref"),
            idle_governance.get("broadcast_frame_ref"),
            idle_governance.get("metacognition_ref"),
            idle_governance.get("consciousness_probe_ref"),
            idle_governance.get("birth_readiness_rollup_ref"),
            idle_governance.get("birth_readiness_stage_gate_ref"),
        ]
        if ref
    ]


def _relationship_resume_summary(
    *,
    idle_governance: dict[str, Any],
    relationship_resume_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    relationship_resume = dict(relationship_resume_summary or {})
    if not relationship_resume and isinstance(
        idle_governance.get("background_resume_summary"), dict
    ):
        relationship_resume = dict(
            idle_governance["background_resume_summary"].get("relationship") or {}
        )
    if not relationship_resume and idle_governance.get("background_relationship_stage"):
        relationship_resume = {
            "relationship_stage": idle_governance.get("background_relationship_stage")
        }
    if idle_governance.get("background_relationship_subject_ref"):
        relationship_resume.setdefault(
            "relationship_subject_ref",
            idle_governance["background_relationship_subject_ref"],
        )
    if idle_governance.get("background_relationship_stage_reason"):
        relationship_resume.setdefault(
            "relationship_stage_reason",
            idle_governance["background_relationship_stage_reason"],
        )
    if idle_governance.get("background_relationship_stage_turn_count") is not None:
        relationship_resume.setdefault(
            "relationship_stage_turn_count",
            idle_governance["background_relationship_stage_turn_count"],
        )
    if idle_governance.get("background_relationship_stage_evidence_refs"):
        relationship_resume.setdefault(
            "relationship_stage_evidence_refs",
            list(idle_governance["background_relationship_stage_evidence_refs"]),
        )
    return {
        key: value
        for key, value in relationship_resume.items()
        if value is not None and value != "" and value != []
    }


def _trait_slow_variable_summary(
    *,
    idle_governance: dict[str, Any],
    trait_slow_variable_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    if isinstance(trait_slow_variable_summary, dict) and trait_slow_variable_summary:
        return trait_slow_variable_summary
    if isinstance(idle_governance.get("background_trait_slow_variable_summary"), dict):
        return idle_governance["background_trait_slow_variable_summary"]
    if isinstance(idle_governance.get("background_resume_summary"), dict):
        traits = idle_governance["background_resume_summary"].get(
            "trait_slow_variables"
        )
        if isinstance(traits, dict):
            return traits
    return {}


def _background_convergence_summary(
    *,
    idle_governance: dict[str, Any],
    explicit_summary_ref: str | None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    ref = explicit_summary_ref or idle_governance.get("background_convergence_summary_ref")
    if ref:
        summary["background_convergence_summary_ref"] = ref
    for key in [
        "background_convergence_state",
        "background_convergence_pressure_level",
        "background_convergence_attention_target",
        "background_relationship_stage_continuity",
        "background_trait_convergence_score",
        "background_max_trait_delta_from_background",
        "background_average_trait_delta_from_background",
        "background_trait_convergence_summary",
    ]:
        value = idle_governance.get(key)
        if value is not None and value != "" and value != []:
            summary[key] = value
    return summary


def _background_resume_focus(
    *,
    relationship_resume: dict[str, Any],
    trait_slow_variable_summary: dict[str, Any],
) -> dict[str, Any]:
    focus: dict[str, Any] = {}
    if relationship_resume.get("relationship_stage"):
        focus["relationship_stage"] = relationship_resume["relationship_stage"]
    if relationship_resume.get("relationship_stage_reason"):
        focus["relationship_stage_reason"] = relationship_resume[
            "relationship_stage_reason"
        ]
    if trait_slow_variable_summary:
        focus["trait_slow_variable_names"] = sorted(
            trait_slow_variable_summary.keys()
        )
    return focus


def _background_convergence_focus(
    background_convergence: dict[str, Any],
) -> dict[str, Any]:
    focus: dict[str, Any] = {}
    for key in [
        "background_convergence_summary_ref",
        "background_convergence_state",
        "background_convergence_pressure_level",
        "background_convergence_attention_target",
        "background_relationship_stage_continuity",
        "background_trait_convergence_score",
    ]:
        if background_convergence.get(key) is not None:
            focus[key] = background_convergence[key]
    trait_summary = background_convergence.get("background_trait_convergence_summary")
    if isinstance(trait_summary, dict) and trait_summary:
        focus["trait_convergence_names"] = sorted(trait_summary.keys())
        focus["trait_convergence_bands"] = {
            name: payload.get("convergence_band")
            for name, payload in trait_summary.items()
            if isinstance(payload, dict) and payload.get("convergence_band")
        }
    return focus


def _offline_learning_cumulative_focus(
    idle_governance: dict[str, Any],
) -> dict[str, Any]:
    profile = idle_governance.get("offline_learning_cumulative_profile")
    if not isinstance(profile, dict):
        profile = {}
    priority_profile = (
        idle_governance.get("offline_learning_cumulative_priority_profile")
        or profile.get("priority_profile")
        or {}
    )
    if not isinstance(priority_profile, dict):
        priority_profile = {}
    ref_set = (
        idle_governance.get("offline_learning_cumulative_ref_set")
        or profile.get("ref_set")
        or []
    )
    if not isinstance(ref_set, list):
        ref_set = []
    generation = (
        idle_governance.get("offline_learning_cumulative_generation")
        or profile.get("generation")
    )
    pressure_level = (
        idle_governance.get("offline_learning_cumulative_pressure_level")
        or profile.get("pressure_level")
    )
    attention_target = (
        idle_governance.get("offline_learning_cumulative_attention_target")
        or profile.get("attention_target")
    )
    if not any([generation, pressure_level, attention_target, priority_profile, ref_set]):
        return {}
    focus: dict[str, Any] = {
        "generation": _int_or_zero(generation),
        "pressure_level": str(pressure_level or "quiet"),
        "attention_target": str(
            attention_target or "baseline_offline_learning_maintenance"
        ),
        "priority_profile": {
            str(key): str(value)
            for key, value in priority_profile.items()
            if value is not None
        },
        "priority_names": sorted(str(key) for key in priority_profile.keys()),
        "ref_count": len(ref_set),
        "ref_set": [str(ref) for ref in ref_set if ref],
    }
    current_pressure = profile.get("current_pressure_level")
    if current_pressure:
        focus["current_pressure_level"] = str(current_pressure)
    previous_generation = profile.get("previous_generation")
    if previous_generation is not None:
        focus["previous_generation"] = _int_or_zero(previous_generation)
    return focus


def _trait_convergence_band_pairs(
    trait_summary: dict[str, Any],
) -> list[str]:
    pairs: list[str] = []
    for name in sorted(trait_summary.keys()):
        payload = trait_summary[name]
        if isinstance(payload, dict) and payload.get("convergence_band"):
            pairs.append(f"{name}:{payload['convergence_band']}")
        else:
            pairs.append(str(name))
    return pairs


def _pressure_rank(pressure_level: str) -> int:
    return {
        "urgent": 4,
        "elevated": 3,
        "present": 2,
        "baseline": 1,
        "quiet": 0,
    }.get(str(pressure_level or ""), 0)
