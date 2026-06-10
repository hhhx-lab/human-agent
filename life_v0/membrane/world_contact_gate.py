from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
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
    contact_mode = "shadow_only" if decision in {"delay", "shadow_release"} else "blocked"
    life_constraint_refs = [
        "runtime/state/action/action_candidate_set.json#life_constraint_profile",
        *[
            ref
            for ref in go_nogo_decision.get("life_constraint_refs", [])
            if isinstance(ref, str)
        ],
    ]
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
        "allowed_contacts": [
            "observation_only",
            "language_shadow_expression",
            "receipt_generation",
        ],
        "blocked_contacts": list(shadow_action_gate.get("blocked_action_classes", []))
        + ["external_irreversible_action"],
        "life_constraint_refs": list(dict.fromkeys(life_constraint_refs)),
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
    ]:
        if not state.get(field):
            reasons.append(f"world_contact_gate missing {field}")
    return reasons
