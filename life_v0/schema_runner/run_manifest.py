from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/53_runner_integration_plan.md",
    "docs/66_runner_report_json_examples.md",
    "docs/180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_run_manifest(
    *,
    run_id: str,
    generated_at: str,
    run_status: str,
    stage_effect: str,
    source_doc_refs: list[str],
    input_state_refs: list[str],
    input_report_refs: list[str],
    output_refs: list[str],
    input_hashes: dict[str, str],
    package_local_gate_refs: list[str],
    closure_status_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "schema_runner_run_manifest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": "S09_SCHEMA_RUNNER_CODE",
        "run_status": run_status,
        "stage_effect": stage_effect,
        "command_sequence": [
            "build-schema-runner",
            "check-schema-runner",
            "run-schema-smoke",
        ],
        "input_state_refs": input_state_refs,
        "input_report_refs": input_report_refs,
        "input_hashes": input_hashes,
        "output_refs": output_refs,
        "package_local_gate_refs": package_local_gate_refs,
        "closure_status_refs": closure_status_refs,
        "receipt_ref": f"runtime/receipts/schema_runner_{run_id}.json",
        "source_doc_refs": sorted(set(source_doc_refs + SOURCE_DOC_REFS)),
    }


def check_run_manifest(state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state.get("schema_version") != "schema_runner_run_manifest_v0":
        reasons.append("run_manifest_gate schema mismatch")
    for field in [
        "active_engineering_slice",
        "run_status",
        "command_sequence",
        "input_state_refs",
        "input_report_refs",
        "input_hashes",
        "output_refs",
        "package_local_gate_refs",
        "closure_status_refs",
        "receipt_ref",
        "source_doc_refs",
    ]:
        if not state.get(field):
            reasons.append(f"run_manifest_gate missing {field}")
    return reasons
