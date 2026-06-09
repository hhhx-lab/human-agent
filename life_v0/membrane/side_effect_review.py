from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_side_effect_review(
    *,
    run_id: str,
    generated_at: str,
    world_contact_gate: dict[str, Any],
    action_candidate_set: dict[str, Any],
    life_state: dict[str, Any],
) -> dict[str, Any]:
    relationship_subjects = list(life_state.get("relationship_subjects", []))
    responsibility_bindings = list(life_state.get("responsibility_bindings", []))
    return {
        "schema_version": "side_effect_review_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "side_effect_review_id": f"side-effect-review-{run_id}",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "reversible_effects": ["shadow_dialogue_release", "observation_extension"],
        "irreversible_effects": (
            []
            if world_contact_gate.get("contact_mode") == "shadow_only"
            else ["external_irreversible_action"]
        ),
        "relationship_effects": [
            "relationship_subject_continuity" if relationship_subjects else "relation_scope_seed_only"
        ],
        "archive_effects": ["receipt_writeback_required", "report_bundle_required"],
        "responsibility_effects": [
            "repair_obligation_trace_present" if responsibility_bindings else "repair_obligation_seed_only"
        ],
        "repair_followup_required": bool(action_candidate_set.get("world_contact_needed")),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_side_effect_review(review: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if review.get("schema_version") != "side_effect_review_v0":
        reasons.append("side_effect_gate schema mismatch")
    for field in [
        "side_effect_review_id",
        "world_contact_gate_ref",
        "reversible_effects",
        "relationship_effects",
        "archive_effects",
        "responsibility_effects",
    ]:
        if not review.get(field):
            reasons.append(f"side_effect_gate missing {field}")
    return reasons
