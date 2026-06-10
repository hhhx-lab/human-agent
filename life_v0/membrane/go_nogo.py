from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/06_action_reward_inhibition.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
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
        "source_doc_refs": SOURCE_DOC_REFS,
    }


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
    ]:
        if not decision.get(field):
            reasons.append(f"go_nogo_gate missing {field}")
    return reasons
