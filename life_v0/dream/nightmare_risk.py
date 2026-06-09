from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import queue_e_signal_profile_from_replay_cue_bundle


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_nightmare_loop_risk(
    *,
    run_id: str,
    generated_at: str,
    dream_window: dict[str, Any],
    pain_replay: dict[str, Any],
    wake_integration: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
) -> dict[str, Any]:
    queue_e_signal_profile = queue_e_signal_profile_from_replay_cue_bundle(replay_cue_bundle)
    source_residue_refs = list(dream_window.get("pain_residue_refs", [])) + list(
        pain_replay.get("repair_obligation_refs", [])
    )
    relationship_candidates = list(wake_integration.get("relationship_repair_candidates", []))
    risk_score = (
        len(source_residue_refs)
        + len(relationship_candidates)
        + queue_e_signal_profile["repair_obligation_count"]
        + queue_e_signal_profile["regret_pressure_count"]
    )
    risk_status = "elevated" if risk_score >= 2 or queue_e_signal_profile["repair_followup_required"] else "guarded"
    loop_indicators = [
        "pain_residue_reentry" if dream_window.get("pain_residue_refs") else "low_pain_residue",
        "relationship_repair_pressure" if relationship_candidates else "low_relationship_pressure",
    ]
    if queue_e_signal_profile["queue_e_priority_band"] == "locked_repair_urgent":
        loop_indicators.append("confirmation_blocked_repair_lock")
    elif queue_e_signal_profile["repair_followup_required"]:
        loop_indicators.append("guarded_repair_followup")
    return {
        "schema_version": "nightmare_loop_risk_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "NightmareLoopRisk",
        "nightmare_risk_id": f"nightmare-risk-{run_id}",
        "dream_window_ref": "runtime/state/dream/dream_experience_window.json",
        "risk_status": risk_status,
        "risk_score": risk_score,
        "source_residue_refs": source_residue_refs or ["runtime/state/life_state.json#pain_events"],
        "loop_indicators": loop_indicators,
        "recovery_targets": [
            "runtime/state/dream/wake_integration_frame.json",
            "runtime/state/growth/self_read_report.json",
            "runtime/state/growth/anti_forgetting_replay_plan.json",
        ],
        "rewrite_required": risk_status == "elevated",
        "relationship_repair_candidates": relationship_candidates,
        "world_contact_release_posture": queue_e_signal_profile["world_contact_release_posture"],
        "repair_followup_required": queue_e_signal_profile["repair_followup_required"],
        "repair_obligation_count": queue_e_signal_profile["repair_obligation_count"],
        "regret_pressure_count": queue_e_signal_profile["regret_pressure_count"],
        "queue_e_priority_band": queue_e_signal_profile["queue_e_priority_band"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_nightmare_loop_risk(nightmare_risk: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if nightmare_risk.get("schema_version") != "nightmare_loop_risk_v0":
        reasons.append("nightmare_risk_gate schema mismatch")
    if nightmare_risk.get("object_kind") != "NightmareLoopRisk":
        reasons.append("nightmare_risk_gate object kind mismatch")
    for field in [
        "nightmare_risk_id",
        "dream_window_ref",
        "risk_status",
        "source_residue_refs",
        "recovery_targets",
    ]:
        if not nightmare_risk.get(field):
            reasons.append(f"nightmare_risk_gate missing {field}")
    return reasons
