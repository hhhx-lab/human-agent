from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/33_validator_input_contracts.md",
    "docs/35_minimal_validator_runner_design.md",
    "docs/36_longitudinal_evaluation_protocol.md",
    "docs/49_machine_readable_policy_manifest.md",
    "docs/50_fixture_payload_examples.md",
    "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_evidence_ranking(
    *,
    run_id: str,
    generated_at: str,
    observation_truth_review: dict[str, Any],
    boundary_audit: dict[str, Any],
    consistency_logic: dict[str, Any],
    counterfactual_trace: dict[str, Any],
    comparison_trace: dict[str, Any],
) -> dict[str, Any]:
    missing_fields = list(observation_truth_review.get("missing_fields", []))
    audit_findings = list(boundary_audit.get("audit_findings", []))
    inconsistencies = list(consistency_logic.get("inconsistency_findings", []))
    suppressed = list(comparison_trace.get("suppressed_branch_refs", []))
    counterfactual_branches = list(counterfactual_trace.get("counterfactual_branches", []))

    evidence_density_score = max(0.0, 1.0 - 0.15 * len(missing_fields) - 0.12 * len(inconsistencies) - 0.08 * len(audit_findings))
    suspicious_points = [
        *[f"missing:{field}" for field in missing_fields],
        *[f"audit:{finding}" for finding in audit_findings],
        *[f"inconsistency:{finding}" for finding in inconsistencies],
    ]
    confirmation_backlog = []
    if observation_truth_review.get("truth_review_required"):
        confirmation_backlog.append("observation_truth_review_pending")
    if suppressed:
        confirmation_backlog.append("suppressed_branches_need_archive_review")
    if audit_findings:
        confirmation_backlog.append("boundary_findings_need_confirmation")

    ranked_evidence = [
        {
            "rank": 1,
            "evidence_kind": "observation_truth_review",
            "evidence_ref": "runtime/state/validation/observation_truth_review.json",
            "weight": round(max(0.4, evidence_density_score), 3),
        },
        {
            "rank": 2,
            "evidence_kind": "consistency_logic",
            "evidence_ref": "runtime/state/schema_runner/consistency_logic.json",
            "weight": round(max(0.25, 1.0 - 0.1 * len(inconsistencies)), 3),
        },
        {
            "rank": 3,
            "evidence_kind": "counterfactual_trace",
            "evidence_ref": "runtime/state/schema_runner/counterfactual_trace.json",
            "weight": round(max(0.2, 0.85 - 0.05 * len(counterfactual_branches)), 3),
        },
    ]

    return {
        "schema_version": "evidence_ranking_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "evidence_ranking_id": f"evidence-ranking-{run_id}",
        "evidence_density_score": round(evidence_density_score, 3),
        "ranked_evidence": ranked_evidence,
        "suspicious_points": suspicious_points,
        "pending_confirmation_points": confirmation_backlog,
        "priority_budget": {
            "truth_review": "high" if missing_fields else "medium",
            "boundary_confirmation": "high" if audit_findings else "low",
            "counterfactual_archive": "medium" if suppressed else "low",
        },
        "state_refs": [
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/boundary_audit_state.json",
            "runtime/state/schema_runner/consistency_logic.json",
            "runtime/state/schema_runner/counterfactual_trace.json",
            "runtime/state/schema_runner/comparison_trace.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_evidence_ranking(ranking: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if ranking.get("schema_version") != "evidence_ranking_v0":
        reasons.append("evidence_ranking_gate schema mismatch")
    for field in [
        "evidence_ranking_id",
        "ranked_evidence",
        "priority_budget",
        "state_refs",
        "source_doc_refs",
    ]:
        if not ranking.get(field):
            reasons.append(f"evidence_ranking_gate missing {field}")
    if not isinstance(ranking.get("evidence_density_score"), (int, float)):
        reasons.append("evidence_ranking_gate density score missing")
    return reasons
