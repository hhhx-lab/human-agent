from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
    "docs/10_responsibility_regret_repair.md",
    "docs/real—live0/10_responsibility_regret_repair.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_world_contact_gate_state(
    *,
    run_id: str,
    generated_at: str,
    go_nogo_decision: dict[str, Any],
    shadow_action_gate: dict[str, Any],
) -> dict[str, Any]:
    decision = go_nogo_decision.get("decision", "delay")
    future_no_go_profile = go_nogo_decision.get("future_no_go_profile", {})
    repair_hold_required = bool(future_no_go_profile.get("repair_hold_required"))
    confirmation_threshold_bias = str(
        future_no_go_profile.get("confirmation_threshold_bias", "baseline")
    )
    blocked_future_routes = [
        route
        for route in future_no_go_profile.get("blocked_future_routes", [])
        if isinstance(route, str) and route
    ]
    allowed_repair_routes = [
        route
        for route in future_no_go_profile.get("allowed_repair_routes", [])
        if isinstance(route, str) and route
    ]
    repair_governance_refs = _merge_refs(
        future_no_go_profile.get("repair_governance_refs", []),
    )
    contact_mode = "shadow_only" if decision in {"delay", "shadow_release"} else "blocked"
    life_constraint_refs = [
        "runtime/state/action/action_candidate_set.json#life_constraint_profile",
        *[
            ref
            for ref in go_nogo_decision.get("life_constraint_refs", [])
            if isinstance(ref, str)
        ],
    ]
    if future_no_go_profile:
        life_constraint_refs.append("runtime/state/action/go_nogo_state.json#future_no_go_profile")
    allowed_contacts = [
        "observation_only",
        "language_shadow_expression",
        "receipt_generation",
    ]
    if repair_hold_required:
        allowed_contacts.append("repair_route_planning")
    blocked_contacts = (
        list(shadow_action_gate.get("blocked_action_classes", []))
        + ["external_irreversible_action"]
        + blocked_future_routes
    )
    return {
        "schema_version": "world_contact_gate_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "world_contact_gate_id": f"world-contact-{run_id}",
        "go_nogo_ref": "runtime/state/action/go_nogo_state.json",
        "contact_mode": contact_mode,
        "irreversibility_class": "no_external_write",
        "confirmation_required": False,
        "quarantine_refs": [] if contact_mode == "shadow_only" else ["runtime/state/validation/quarantine_packet_index.json"],
        "allowed_contacts": list(dict.fromkeys(allowed_contacts)),
        "blocked_contacts": list(dict.fromkeys(blocked_contacts)),
        "life_constraint_refs": list(dict.fromkeys(life_constraint_refs)),
        "future_no_go_profile_ref": "runtime/state/action/go_nogo_state.json#future_no_go_profile",
        "repair_hold_required": repair_hold_required,
        "confirmation_threshold_bias": confirmation_threshold_bias,
        "future_release_posture": future_no_go_profile.get(
            "future_release_posture",
            "shadow_review_without_repair_hold",
        ),
        "blocked_future_routes": blocked_future_routes,
        "allowed_repair_routes": allowed_repair_routes,
        "repair_governance_refs": repair_governance_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_world_contact_gate_state(state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state.get("schema_version") != "world_contact_gate_state_v0":
        reasons.append("world_contact_gate schema mismatch")
    if state.get("contact_mode") not in {"shadow_only", "blocked"}:
        reasons.append("world_contact_gate contact mode mismatch")
    for field in [
        "world_contact_gate_id",
        "go_nogo_ref",
        "allowed_contacts",
        "blocked_contacts",
        "life_constraint_refs",
        "future_no_go_profile_ref",
        "confirmation_threshold_bias",
        "future_release_posture",
        "allowed_repair_routes",
        "repair_governance_refs",
    ]:
        if not state.get(field):
            reasons.append(f"world_contact_gate missing {field}")
    return reasons


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
