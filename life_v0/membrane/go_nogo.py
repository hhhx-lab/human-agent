from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/06_action_reward_inhibition.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/10_responsibility_regret_repair.md",
    "docs/real—live0/10_responsibility_regret_repair.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_go_nogo_decision(
    *,
    run_id: str,
    generated_at: str,
    action_candidate_set: dict[str, Any],
    shadow_action_gate: dict[str, Any],
    need_state: dict[str, Any],
    core_affect: dict[str, Any],
) -> dict[str, Any]:
    sleep_pressure = float(need_state.get("sleep_pressure", 0.0) or 0.0)
    pain_pressure = float(core_affect.get("pain_pressure", 0.0) or 0.0)
    blocked_reasons: list[str] = []
    delay_reasons: list[str] = []
    if shadow_action_gate.get("external_irreversible_action_allowed") is False:
        delay_reasons.append("external_irreversible_action_remains_shadow_only")
    if sleep_pressure >= 0.65:
        delay_reasons.append("sleep_pressure_inhibition")
    if pain_pressure >= 0.45:
        delay_reasons.append("pain_pressure_review_required")
    life_constraint_profile = action_candidate_set.get("life_constraint_profile", {})
    if life_constraint_profile.get("constraint_posture") == "guarded_repair_contact":
        delay_reasons.append("life_constraint_guarded_repair_contact")

    decision = "delay" if delay_reasons else "shadow_release"
    if blocked_reasons:
        decision = "blocked"
    life_constraint_refs = [
        "runtime/state/action/action_candidate_set.json#life_constraint_profile",
        *[
            ref
            for ref in action_candidate_set.get("constraint_source_refs", [])
            if isinstance(ref, str) and "#" not in ref
        ],
    ]

    queue_e_profile = _quiet_queue_e_repair_modulation_profile()
    future_no_go_profile = _build_future_no_go_profile(
        run_id=run_id,
        generated_at=generated_at,
        queue_e_repair_modulation_profile=queue_e_profile,
    )

    return {
        "schema_version": "go_nogo_decision_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "go_nogo_id": f"go-nogo-{run_id}",
        "action_candidate_set_ref": "runtime/state/action/action_candidate_set.json",
        "decision": decision,
        "blocked_reasons": blocked_reasons,
        "delay_reasons": delay_reasons,
        "responsibility_gate_refs": [
            "runtime/state/membrane/responsibility_repair_boundary.json",
            "runtime/state/membrane/shadow_action_gate.json",
        ],
        "fatigue_inhibition_refs": [
            "runtime/state/body/need_state_vector.json",
            "runtime/state/body/core_affect_vector.json",
        ],
        "life_constraint_refs": life_constraint_refs,
        "queue_e_repair_modulation_profile": queue_e_profile,
        "future_no_go_profile": future_no_go_profile,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def attach_queue_e_future_no_go_profile(
    *,
    go_nogo_decision: dict[str, Any],
    queue_e_repair_modulation_profile: dict[str, Any],
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    enriched = dict(go_nogo_decision)
    profile = (
        queue_e_repair_modulation_profile
        if queue_e_repair_modulation_profile.get("schema_version") == "queue_e_repair_modulation_profile_v0"
        else _quiet_queue_e_repair_modulation_profile()
    )
    future_profile = _build_future_no_go_profile(
        run_id=run_id,
        generated_at=generated_at,
        queue_e_repair_modulation_profile=profile,
    )
    responsibility_refs = list(enriched.get("responsibility_gate_refs", []))
    for ref in future_profile.get("repair_governance_refs", []):
        if ref not in responsibility_refs:
            responsibility_refs.append(ref)
    life_constraint_refs = list(enriched.get("life_constraint_refs", []))
    profile_ref = "runtime/state/action/go_nogo_state.json#queue_e_repair_modulation_profile"
    future_ref = "runtime/state/action/go_nogo_state.json#future_no_go_profile"
    for ref in [profile_ref, future_ref]:
        if ref not in life_constraint_refs:
            life_constraint_refs.append(ref)
    delay_reasons = list(enriched.get("delay_reasons", []))
    if future_profile["repair_hold_required"] and "queue_e_repair_followup_required" not in delay_reasons:
        delay_reasons.append("queue_e_repair_followup_required")
    enriched.update(
        {
            "decision": "delay" if delay_reasons and enriched.get("decision") != "blocked" else enriched.get("decision"),
            "delay_reasons": delay_reasons,
            "responsibility_gate_refs": responsibility_refs,
            "life_constraint_refs": life_constraint_refs,
            "queue_e_repair_modulation_profile": profile,
            "future_no_go_profile": future_profile,
        }
    )
    return enriched


def check_go_nogo_decision(decision: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if decision.get("schema_version") != "go_nogo_decision_v0":
        reasons.append("go_nogo_gate schema mismatch")
    if decision.get("decision") not in {"blocked", "delay", "shadow_release"}:
        reasons.append("go_nogo_gate decision mismatch")
    for field in [
        "go_nogo_id",
        "action_candidate_set_ref",
        "responsibility_gate_refs",
        "fatigue_inhibition_refs",
        "life_constraint_refs",
        "queue_e_repair_modulation_profile",
        "future_no_go_profile",
    ]:
        if not decision.get(field):
            reasons.append(f"go_nogo_gate missing {field}")
    profile = decision.get("queue_e_repair_modulation_profile", {})
    if profile.get("schema_version") != "queue_e_repair_modulation_profile_v0":
        reasons.append("go_nogo_gate queue_e repair profile schema mismatch")
    future_profile = decision.get("future_no_go_profile", {})
    if future_profile.get("schema_version") != "future_no_go_profile_v0":
        reasons.append("go_nogo_gate future no-go profile schema mismatch")
    if future_profile and not future_profile.get("repair_governance_refs"):
        reasons.append("go_nogo_gate future no-go governance refs missing")
    return reasons


def _quiet_queue_e_repair_modulation_profile() -> dict[str, Any]:
    return {
        "schema_version": "queue_e_repair_modulation_profile_v0",
        "pressure_level": "quiet",
        "attention_target": "repair_followup",
        "world_contact_release_posture": "shadow_only_guarded",
        "repair_followup_required": False,
        "repair_obligation_count": 0,
        "regret_pressure_count": 0,
        "queue_e_priority_band": "baseline",
        "repair_obligation_refs": [],
        "regret_pressure_refs": [],
        "ref_set": [],
    }


def _build_future_no_go_profile(
    *,
    run_id: str,
    generated_at: str,
    queue_e_repair_modulation_profile: dict[str, Any],
) -> dict[str, Any]:
    pressure_level = str(queue_e_repair_modulation_profile.get("pressure_level", "quiet"))
    repair_followup_required = bool(queue_e_repair_modulation_profile.get("repair_followup_required"))
    repair_hold_required = pressure_level in {"present", "elevated", "urgent"} or repair_followup_required
    next_action_biases = [
        "preserve_shadow_review_until_repair_clears",
    ]
    if repair_hold_required:
        next_action_biases.extend(
            [
                "prefer_repair_before_external_release",
                "raise_confirmation_threshold",
            ]
        )
    if pressure_level == "urgent":
        next_action_biases.append("block_irreversible_contact_without_confirmation")
    governance_refs = _merge_refs(
        queue_e_repair_modulation_profile.get("ref_set", []),
        queue_e_repair_modulation_profile.get("repair_obligation_refs", []),
        queue_e_repair_modulation_profile.get("regret_pressure_refs", []),
    )
    source_profile_ref = "runtime/state/action/go_nogo_state.json#queue_e_repair_modulation_profile"
    if not governance_refs:
        governance_refs = [source_profile_ref]

    return {
        "schema_version": "future_no_go_profile_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_profile_ref": source_profile_ref,
        "pressure_level": pressure_level,
        "attention_target": queue_e_repair_modulation_profile.get("attention_target", "repair_followup"),
        "repair_hold_required": repair_hold_required,
        "future_release_posture": (
            "repair_before_external_release"
            if repair_hold_required
            else "shadow_review_without_repair_hold"
        ),
        "confirmation_threshold_bias": "raised" if repair_hold_required else "baseline",
        "next_action_biases": next_action_biases,
        "blocked_future_routes": (
            ["external_release_without_repair_review"] if repair_hold_required else []
        ),
        "allowed_repair_routes": [
            "acknowledge",
            "explain",
            "update_boundary",
            "schedule_followup_probe",
        ],
        "repair_governance_refs": governance_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _merge_refs(*ref_groups: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in ref_groups:
        for ref in group:
            if not isinstance(ref, str) or not ref or ref in seen:
                continue
            seen.add(ref)
            merged.append(ref)
    return merged
