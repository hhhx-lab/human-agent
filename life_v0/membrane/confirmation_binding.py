from __future__ import annotations

import hashlib
from typing import Any


SOURCE_DOC_REFS = [
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/79_confirmation_fixture_catalog.md",
    "docs/144_life_reality_language_runtime_action_bridge_fixture_plan.md",
    "docs/147_life_reality_language_action_bridge_schema_materialization_plan.md",
    "docs/150_life_reality_language_action_cross_file_checker_plan.md",
]


def build_confirmation_binding(
    *,
    run_id: str,
    generated_at: str,
    action_intent_queue: dict[str, Any],
    world_contact_gate: dict[str, Any],
) -> dict[str, Any]:
    action_intents = list(action_intent_queue.get("action_intents", []))
    required_action_intent_ids = [
        intent.get("action_intent_id")
        for intent in action_intents
        if intent.get("requires_confirmation")
    ]
    scope_source = "|".join(
        sorted(
            filter(
                None,
                [
                    world_contact_gate.get("contact_mode"),
                    *required_action_intent_ids,
                ],
            )
        )
    )
    scope_digest = hashlib.sha256(scope_source.encode("utf-8")).hexdigest()[:16] if scope_source else "shadow-only-scope"
    requires_confirmation = bool(required_action_intent_ids)
    return {
        "schema_version": "confirmation_binding_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "confirmation_binding_id": f"confirmation-binding-{run_id}",
        "action_intent_queue_ref": "runtime/state/membrane/action_intent_queue.json",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "requires_confirmation": requires_confirmation,
        "confirmation_status": "pending" if requires_confirmation else "not_required",
        "required_action_intent_ids": required_action_intent_ids,
        "scope_digest": scope_digest,
        "reuse_guard": "single_scope_digest_single_action_intent",
        "confirmation_routes": [
            "runtime/state/membrane/confirmation_binding.json",
            "runtime/reports/latest/world_contact_audit_report.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_confirmation_binding(binding: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if binding.get("schema_version") != "confirmation_binding_v0":
        reasons.append("confirmation_binding_gate schema mismatch")
    for field in [
        "confirmation_binding_id",
        "action_intent_queue_ref",
        "world_contact_gate_ref",
        "confirmation_status",
        "scope_digest",
        "reuse_guard",
        "confirmation_routes",
        "source_doc_refs",
    ]:
        if not binding.get(field):
            reasons.append(f"confirmation_binding_gate missing {field}")
    return reasons
