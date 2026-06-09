from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/65_schema_cross_ref_checker_design.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "docs/154_life_reality_cross_file_checker_rule_bundle.md",
    "docs/157_life_reality_cross_file_checker_audit_examples.md",
    "docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_cross_file_logic(
    *,
    run_id: str,
    generated_at: str,
    action_intent_queue: dict[str, Any],
    confirmation_binding: dict[str, Any],
    observation_truth_review: dict[str, Any],
    world_contact_validation: dict[str, Any],
    prediction_trace_validation: dict[str, Any],
    validation_rollup: dict[str, Any],
    boundary_audit: dict[str, Any],
    responsibility_loop: dict[str, Any],
    consistency_logic: dict[str, Any],
    comparison_trace: dict[str, Any],
) -> dict[str, Any]:
    intent_count = len(action_intent_queue.get("action_intents", []))
    confirmation_required = bool(confirmation_binding.get("requires_confirmation"))
    missing_fields = list(observation_truth_review.get("missing_fields", []))
    world_contact_findings = list(world_contact_validation.get("validation_findings", []))
    prediction_links = list(prediction_trace_validation.get("missing_prediction_links", []))
    validation_guarded = list(validation_rollup.get("guarded_gates", []))
    audit_findings = list(boundary_audit.get("audit_findings", []))
    inconsistency_findings = list(consistency_logic.get("inconsistency_findings", []))
    repair_obligations = list(responsibility_loop.get("repair_obligation_refs", []))
    growth_refs = list(responsibility_loop.get("growth_reentry_refs", []))
    dream_refs = list(responsibility_loop.get("dream_reentry_refs", []))
    suppressed_branches = list(comparison_trace.get("suppressed_branch_refs", []))

    findings: list[dict[str, Any]] = []
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0001",
            "finding_kind": "responsibility_truth_alignment",
            "severity": "guarded_medium" if missing_fields or prediction_links else "guarded_low",
            "state_refs": [
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/validation/observation_truth_review.json",
                "runtime/state/validation/prediction_trace_validation.json",
            ],
            "summary": "repair obligations stay aligned with truth review completeness",
            "repair_priority": "high" if missing_fields or prediction_links else "medium",
        }
    )
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0002",
            "finding_kind": "intent_confirmation_alignment",
            "severity": "guarded_medium" if confirmation_required or world_contact_findings else "guarded_low",
            "state_refs": [
                "runtime/state/membrane/action_intent_queue.json",
                "runtime/state/membrane/confirmation_binding.json",
                "runtime/state/validation/world_contact_validation.json",
            ],
            "summary": "action intents remain aligned with confirmation and world-contact validation",
            "repair_priority": "high" if confirmation_required or world_contact_findings else "medium",
        }
    )
    if audit_findings or suppressed_branches:
        findings.append(
            {
                "finding_id": f"cross-file-{run_id}-0003",
                "finding_kind": "boundary_counterfactual_coupling",
                "severity": "guarded_medium",
                "state_refs": [
                    "runtime/state/validation/boundary_audit_state.json",
                    "runtime/state/schema_runner/comparison_trace.json",
                ],
                "summary": "boundary findings remain coupled to suppressed counterfactual branches",
                "repair_priority": "high",
            }
        )
    else:
        findings.append(
            {
                "finding_id": f"cross-file-{run_id}-0003",
                "finding_kind": "growth_reentry_linkage",
                "severity": "guarded_low",
                "state_refs": [
                    "runtime/state/action/responsibility_loop_state.json",
                    "runtime/state/schema_runner/comparison_trace.json",
                ],
                "summary": "responsibility loop preserves dream and growth reentry continuity",
                "repair_priority": "medium",
            }
        )

    repair_priority_refs = [
        "runtime/state/action/responsibility_loop_state.json",
        "runtime/state/schema_runner/comparison_trace.json",
    ]
    if intent_count:
        repair_priority_refs.append("runtime/state/membrane/action_intent_queue.json")
    if confirmation_required or world_contact_findings:
        repair_priority_refs.append("runtime/state/membrane/confirmation_binding.json")
        repair_priority_refs.append("runtime/state/validation/world_contact_validation.json")
    if audit_findings:
        repair_priority_refs.append("runtime/state/validation/boundary_audit_state.json")
    if missing_fields:
        repair_priority_refs.append("runtime/state/validation/observation_truth_review.json")
    if prediction_links:
        repair_priority_refs.append("runtime/state/validation/prediction_trace_validation.json")
    if validation_guarded:
        repair_priority_refs.append("runtime/state/validation/validation_rollup.json")
    if growth_refs:
        repair_priority_refs.extend(growth_refs[:1])
    if dream_refs:
        repair_priority_refs.extend(dream_refs[:1])

    bridge_refs = [
        "runtime/state/language/commitment_repair_language_index.json",
        "runtime/state/relationship/commitment_truth_state.json#repair_required_refs",
        "runtime/state/responsibility/responsibility_ledger.json#repair_obligations",
        "runtime/state/memory/relationship_memory.json#repair_history_refs",
        "runtime/state/growth/growth_patch_candidate_queue.json",
        "runtime/state/dream/offline_consolidation_frame.json",
        "runtime/state/validation/validation_rollup.json#gate_status",
    ]

    return {
        "schema_version": "cross_file_logic_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "cross_file_logic_id": f"cross-file-logic-{run_id}",
        "status": "closed" if not inconsistency_findings else "guarded_closed",
        "state_refs": [
            "runtime/state/membrane/action_intent_queue.json",
            "runtime/state/membrane/confirmation_binding.json",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/prediction_trace_validation.json",
            "runtime/state/validation/validation_rollup.json",
            "runtime/state/validation/boundary_audit_state.json",
            "runtime/state/schema_runner/consistency_logic.json",
            "runtime/state/schema_runner/comparison_trace.json",
        ],
        "cross_file_findings": findings,
        "repair_priority_refs": repair_priority_refs,
        "closure_status_refs": [
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/prediction_trace_validation.json",
            "runtime/state/validation/validation_rollup.json",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/action_intent_queue.json",
            "runtime/state/membrane/confirmation_binding.json",
        ],
        "package_local_gate_refs": [
            "validation_rollup_gate",
            "prediction_trace_validation_gate",
            "world_contact_validation_gate",
            "cross_file_logic_gate",
        ],
        "bridge_refs": bridge_refs,
        "repair_obligation_refs": repair_obligations,
        "blocked_growth_refs": growth_refs if inconsistency_findings else [],
        "blocked_dream_refs": dream_refs if missing_fields else [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_cross_file_logic(state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state.get("schema_version") != "cross_file_logic_v0":
        reasons.append("cross_file_logic_gate schema mismatch")
    for field in [
        "cross_file_logic_id",
        "status",
        "state_refs",
        "cross_file_findings",
        "repair_priority_refs",
        "closure_status_refs",
        "package_local_gate_refs",
        "bridge_refs",
        "source_doc_refs",
    ]:
        if not state.get(field):
            reasons.append(f"cross_file_logic_gate missing {field}")
    return reasons
