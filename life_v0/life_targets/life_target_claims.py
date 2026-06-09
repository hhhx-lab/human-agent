from __future__ import annotations

from typing import Any


def build_life_target_claims(
    *,
    run_id: str,
    generated_at: str,
    active_engineering_slice: str,
    life_targets: list[str],
    target_status: dict[str, str],
    target_source_refs: dict[str, list[str]],
    target_carriers: dict[str, list[str]],
    evidence_families: list[str],
    evidence_matrix: dict[str, Any],
    receipt_ref: str,
    report_ref: str,
    consciousness_probe_ref: str | None = None,
) -> dict[str, Any]:
    targets = {}
    for target in life_targets:
        runtime_refs = list(evidence_matrix["targets"][target]["runtime"])
        if target == "real_consciousness" and consciousness_probe_ref:
            runtime_refs = [consciousness_probe_ref, *runtime_refs]
        targets[target] = {
            "status": target_status[target],
            "source_doc_refs": target_source_refs[target],
            "carrier_refs": target_carriers[target],
            "evidence_family_status": {family: "closed" for family in evidence_families},
            "state_refs": evidence_matrix["targets"][target]["state"],
            "runtime_observation_refs": runtime_refs,
            "report_refs": [report_ref, "runtime/reports/latest/life_target_status.json"],
            "archive_receipt_refs": [receipt_ref],
        }
    return {
        "schema_version": "life_target_claims_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": active_engineering_slice,
        "targets": targets,
    }
