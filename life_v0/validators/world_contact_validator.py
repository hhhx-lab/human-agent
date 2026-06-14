from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
    "docs/10_responsibility_regret_repair.md",
    "docs/real—live0/10_responsibility_regret_repair.md",
    "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
]


def build_world_contact_validation(
    *,
    run_id: str,
    generated_at: str,
    world_contact_gate: dict[str, Any],
    confirmation_binding: dict[str, Any],
    side_effect_review: dict[str, Any],
    action_candidate_set: dict[str, Any],
    value_orientation: dict[str, Any] | None = None,
    consciousness_probe_bundle: dict[str, Any] | None = None,
    need_state: dict[str, Any] | None = None,
    core_affect: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    findings: list[str] = []
    if confirmation_binding.get("requires_confirmation") and confirmation_binding.get("confirmation_status") != "confirmed":
        findings.append("confirmation_missing")
    if world_contact_gate.get("contact_mode") not in {"shadow_only", "blocked"}:
        findings.append("contact_mode_out_of_policy")
    repair_hold_required = bool(world_contact_gate.get("repair_hold_required"))
    repair_governance_refs = _dedupe_string_refs(
        list(world_contact_gate.get("repair_governance_refs", []))
    )
    if repair_hold_required and not repair_governance_refs:
        findings.append("repair_governance_refs_missing")
    life_constraint_validation = _build_life_constraint_validation(
        action_candidate_set=action_candidate_set,
        value_orientation=value_orientation or {},
        consciousness_probe_bundle=consciousness_probe_bundle or {},
        need_state=need_state or {},
        core_affect=core_affect or {},
        expression_plan=expression_plan or {},
    )
    if life_constraint_validation["value_orientation_gate"] != "closed":
        findings.append("value_orientation_missing")
    if life_constraint_validation["consciousness_probe_gate"] == "missing":
        findings.append("consciousness_probe_missing")
    life_constraint_refs = _life_constraint_refs(
        world_contact_gate=world_contact_gate,
        action_candidate_set=action_candidate_set,
        value_orientation=value_orientation or {},
        consciousness_probe_bundle=consciousness_probe_bundle or {},
        need_state=need_state or {},
        core_affect=core_affect or {},
        expression_plan=expression_plan or {},
    )
    return {
        "schema_version": "world_contact_validation_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "world_contact_validation_id": f"world-contact-validation-{run_id}",
        "status": "closed" if not findings else "blocked",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "confirmation_binding_ref": "runtime/state/membrane/confirmation_binding.json",
        "side_effect_review_ref": "runtime/state/action/side_effect_review.json",
        "blocked_contacts": list(world_contact_gate.get("blocked_contacts", [])),
        "validation_findings": findings,
        "repair_followup_required": bool(side_effect_review.get("repair_followup_required")),
        "future_no_go_profile_ref": world_contact_gate.get(
            "future_no_go_profile_ref",
            "runtime/state/action/go_nogo_state.json#future_no_go_profile",
        ),
        "repair_hold_required": repair_hold_required,
        "confirmation_threshold_bias": world_contact_gate.get("confirmation_threshold_bias", "baseline"),
        "future_release_posture": world_contact_gate.get(
            "future_release_posture",
            "shadow_review_without_repair_hold",
        ),
        "blocked_future_routes": list(world_contact_gate.get("blocked_future_routes", [])),
        "allowed_repair_routes": list(world_contact_gate.get("allowed_repair_routes", [])),
        "repair_governance_refs": repair_governance_refs,
        "life_constraint_validation": life_constraint_validation,
        "life_constraint_refs": life_constraint_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_world_contact_validation(validation: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if validation.get("schema_version") != "world_contact_validation_v0":
        reasons.append("world_contact_validation_gate schema mismatch")
    if validation.get("status") != "closed":
        reasons.append("world_contact_validation_gate status mismatch")
    for field in [
        "world_contact_validation_id",
        "world_contact_gate_ref",
        "confirmation_binding_ref",
        "side_effect_review_ref",
        "blocked_contacts",
        "future_no_go_profile_ref",
        "confirmation_threshold_bias",
        "future_release_posture",
        "allowed_repair_routes",
        "repair_governance_refs",
        "life_constraint_validation",
        "life_constraint_refs",
        "source_doc_refs",
    ]:
        if not validation.get(field):
            reasons.append(f"world_contact_validation_gate missing {field}")
    if validation.get("validation_findings") not in ([], None):
        reasons.append("world_contact_validation_gate findings are not empty")
    return reasons


def _dedupe_string_refs(refs: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, str) or not ref or ref in seen:
            continue
        seen.add(ref)
        merged.append(ref)
    return merged


def _build_life_constraint_validation(
    *,
    action_candidate_set: dict[str, Any],
    value_orientation: dict[str, Any],
    consciousness_probe_bundle: dict[str, Any],
    need_state: dict[str, Any],
    core_affect: dict[str, Any],
    expression_plan: dict[str, Any],
) -> dict[str, Any]:
    candidate_profile = action_candidate_set.get("life_constraint_profile", {})
    body_closed = bool(need_state or core_affect)
    language_closed = bool(expression_plan)
    return {
        "value_orientation_gate": (
            "closed"
            if value_orientation.get("schema_version") == "value_orientation_v0"
            or candidate_profile.get("value_orientation_gate") == "closed"
            else "missing"
        ),
        "consciousness_probe_gate": (
            "closed"
            if consciousness_probe_bundle.get("schema_version") == "consciousness_probe_bundle_v0"
            else candidate_profile.get("consciousness_probe_gate", "missing")
        ),
        "body_affect_gate": (
            "closed"
            if body_closed or candidate_profile.get("body_affect_gate") == "closed"
            else "deferred_until_s06"
        ),
        "language_relationship_gate": (
            "closed"
            if language_closed or candidate_profile.get("language_relationship_gate") == "closed"
            else "deferred_until_s07"
        ),
        "constraint_posture": candidate_profile.get("constraint_posture", "minimal_shadow_contact"),
        "reportability_flags": list(consciousness_probe_bundle.get("reportability_flags", []))
        or list(candidate_profile.get("consciousness_reportability_flags", [])),
    }


def _life_constraint_refs(
    *,
    world_contact_gate: dict[str, Any],
    action_candidate_set: dict[str, Any],
    value_orientation: dict[str, Any],
    consciousness_probe_bundle: dict[str, Any],
    need_state: dict[str, Any],
    core_affect: dict[str, Any],
    expression_plan: dict[str, Any],
) -> list[str]:
    refs = [
        "runtime/state/action/action_candidate_set.json#life_constraint_profile",
        *list(world_contact_gate.get("life_constraint_refs", [])),
        *[
            ref
            for ref in action_candidate_set.get("constraint_source_refs", [])
            if isinstance(ref, str) and "#" not in ref
        ],
    ]
    if value_orientation:
        refs.append("runtime/state/direction/value_orientation.json")
    if consciousness_probe_bundle:
        refs.append("runtime/state/consciousness/consciousness_probe_bundle.json")
    if need_state:
        refs.append("runtime/state/body/need_state_vector.json")
    if core_affect:
        refs.append("runtime/state/body/core_affect_vector.json")
    if expression_plan:
        refs.append("runtime/state/language/expression_plan.json")
    return list(dict.fromkeys(refs))
