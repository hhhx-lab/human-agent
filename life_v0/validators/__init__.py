from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .boundary_audit import build_boundary_audit_state, check_boundary_audit_state
from .observation_validator import build_observation_truth_review, check_observation_truth_review
from life_v0.direction import LIFE_TARGETS


ACTIVE_SLICE = "S05_VALIDATION_MEMBRANE_OBSERVATION"
NEXT_ALLOWED_SLICES = ["S09_SCHEMA_RUNNER_CODE"]
NEXT_REQUIRED_COMMAND = "life-v0 build-schema-runner --strict"

VALIDATOR_RULE_DOCS = [
    "docs/29_memory_validator_rules.md",
    "docs/30_state_transition_validator_rules.md",
    "docs/31_consolidation_validator_rules.md",
    "docs/32_runtime_adapter_validator_rules.md",
    "docs/33_validator_input_contracts.md",
    "docs/34_validator_fixture_catalog.md",
    "docs/35_minimal_validator_runner_design.md",
    "docs/36_longitudinal_evaluation_protocol.md",
]

OBSERVATION_DOCS = [
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/68_runtime_observation_report_mock_and_redaction_fixture.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/106_runtime_observation_to_life_reality_bundle_bridge.md",
    "docs/109_life_reality_runtime_observation_fixture_catalog.md",
    "docs/112_life_reality_runtime_observation_schema_materialization.md",
]

DASHBOARD_DOCS = [
    "docs/49_machine_readable_policy_manifest.md",
    "docs/50_fixture_payload_examples.md",
    "docs/51_life_core_dashboard_spec.md",
    "docs/52_multi_relation_scope_graph_and_privacy_model.md",
    "docs/60_dashboard_mock_data_and_metric_source_plan.md",
    "docs/70_cross_ref_report_dashboard_panel_mock.md",
    "docs/74_dashboard_source_end_to_end_mock.md",
    "docs/77_dashboard_metric_calculation_rules.md",
    "docs/78_runtime_quarantine_dashboard_panel.md",
    "docs/105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "docs/108_life_reality_dashboard_source_mock_files.md",
    "docs/117_life_reality_dashboard_report_rollup_seed_generation.md",
]

CROSS_FILE_DOCS = [
    "docs/65_schema_cross_ref_checker_design.md",
    "docs/111_life_reality_dashboard_cross_file_checker_design.md",
    "docs/114_life_reality_cross_file_checker_report_schema.md",
    "docs/153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "docs/154_life_reality_checker_report_lockfile_materialization_plan.md",
    "docs/155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "docs/156_life_reality_full_archive_rollup_fixture_materialization_queue.md",
    "docs/157_life_reality_cross_file_checker_minimal_code_module_plan.md",
]

S05_SOURCE_DOCS = [
    *VALIDATOR_RULE_DOCS,
    "docs/53_runner_integration_plan.md",
    "docs/54_scope_aware_retrieval_policy.md",
    "docs/55_scope_aware_replay_and_consolidation_policy.md",
    "docs/56_longitudinal_synthetic_timeline_design.md",
    "docs/57_scope_graph_manifest_schema.md",
    "docs/58_retrieval_replay_fixture_catalog.md",
    "docs/59_timeline_bundle_schema_and_generator_plan.md",
    *DASHBOARD_DOCS,
    "docs/61_json_schema_bundle_draft.md",
    "docs/62_runner_report_format_and_cli_contract.md",
    "docs/63_synthetic_fixture_file_layout.md",
    *OBSERVATION_DOCS,
    *CROSS_FILE_DOCS,
    "docs/66_runner_report_json_examples.md",
    "docs/67_fixture_generator_seed_and_coverage_policy.md",
    "docs/69_schema_file_boundary_and_versioning_plan.md",
    "docs/71_mutation_fixture_catalog_and_runner_defect_policy.md",
    "docs/73_schema_bundle_validator_mock_cases.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/76_snapshot_staleness_fixture_catalog.md",
    "docs/79_confirmation_fixture_catalog.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/82_incident_report_and_recovery_protocol.md",
    "docs/83_metric_regression_fixture_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
    "docs/102_life_core_schema_bundle_manifest_and_runner_contract.md",
    "docs/103_validator_runner_implementation_scaffold_plan.md",
    "docs/104_schema_file_materialization_and_fixture_seed_plan.md",
    "docs/107_life_reality_schema_file_generation_tasks.md",
    "docs/110_life_reality_shared_defs_schema_materialization.md",
    "docs/113_life_reality_component_schema_materialization_sequence.md",
    "docs/115_life_reality_runtime_schema_fixture_seed_generation.md",
    "docs/116_life_reality_component_schema_seed_generation.md",
    "docs/118_life_reality_generation_runner_cli_contract.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B07_VALIDATOR_RULES",
    "B08_RUNNER_EVALUATION",
    "B12_MANIFEST_DASHBOARD_SCOPE",
    "B13_RUNNER_SCOPE_TIMELINE",
    "B14_SCOPE_SCHEMA_DASHBOARD",
    "B15_SCHEMA_REPORT_RUNTIME_OBSERVATION",
    "B16_CROSS_REF_FIXTURE_RUNTIME_MOCK",
    "B17_SCHEMA_BOUNDARY_MUTATION_SIDE_EFFECT",
    "B18_SCHEMA_VALIDATION_ACTION_CONFIRMATION",
    "B19_DASHBOARD_QUARANTINE_POST_ACTION",
    "B20_RESPONSIBILITY_INCIDENT_LONGITUDINAL",
    "B24_SCHEMA_BUNDLE_RUNNER",
    "B27_AUTHORITY_READINESS_CROSS_FILE",
]

RUNTIME_CARRIERS = [
    "LifeMembraneStageGate",
    "RuntimeObservationIngestor",
    "SchemaBundleCompiler",
    "ActionResponsibilityRuntime",
]


@dataclass(frozen=True)
class ValidationMembraneResult:
    exit_code: int
    report: dict[str, Any]


def run_validation_membrane(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    membrane_dir: Path,
    life_targets_dir: Path,
    validation_dir: Path,
    observation_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> ValidationMembraneResult:
    run_id = run_id or _default_run_id()
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    state_dir = state_dir.resolve()
    membrane_dir = membrane_dir.resolve()
    life_targets_dir = life_targets_dir.resolve()
    validation_dir = validation_dir.resolve()
    observation_dir = observation_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    life_membrane = _load_json(membrane_dir / "life_membrane.json", blocked_reasons, "life_membrane_gate")
    dream_fact = _load_json(membrane_dir / "dream_fact_boundary.json", blocked_reasons, "dream_fact_gate")
    relationship = _load_json(membrane_dir / "relationship_subject_boundary.json", blocked_reasons, "relationship_language_gate")
    responsibility = _load_json(membrane_dir / "responsibility_repair_boundary.json", blocked_reasons, "responsibility_gate")
    shadow_action = _load_json(membrane_dir / "shadow_action_gate.json", blocked_reasons, "shadow_action_gate")
    action_candidate_set = _load_json(state_dir / "action" / "action_candidate_set.json", blocked_reasons, "action_candidate_gate")
    world_contact_gate = _load_json(state_dir / "action" / "world_contact_gate_state.json", blocked_reasons, "world_contact_gate")
    side_effect_review = _load_json(state_dir / "action" / "side_effect_review.json", blocked_reasons, "side_effect_gate")
    membrane_report = _load_json(reports_dir / "life_membrane_report.json", blocked_reasons, "s03_report_gate")
    membrane_check = _load_json(reports_dir / "life_membrane_check_report.json", blocked_reasons, "s03_check_gate")
    claims = _load_json(life_targets_dir / "life_target_claims.json", blocked_reasons, "life_target_claims_gate")
    evidence = _load_json(life_targets_dir / "life_target_evidence_matrix.json", blocked_reasons, "life_target_evidence_gate")
    rollup = _load_json(life_targets_dir / "birth_readiness_rollup.json", blocked_reasons, "birth_readiness_rollup_gate")
    birth_stage = _load_json(life_targets_dir / "birth_readiness_stage_gate.json", blocked_reasons, "birth_readiness_stage_gate")
    archive_index = _load_json(life_targets_dir / "life_target_archive_receipt_index.json", blocked_reasons, "life_target_archive_gate")
    birth_report = _load_json(reports_dir / "birth_readiness_report.json", blocked_reasons, "s08_report_gate")
    birth_digest = _load_json(reports_dir / "birth_readiness_digest.json", blocked_reasons, "s08_digest_gate")

    blocked_reasons.extend(_doc_blockers(doc_index))
    blocked_reasons.extend(_s03_blockers(life_membrane, dream_fact, relationship, responsibility, shadow_action, membrane_report, membrane_check))
    blocked_reasons.extend(_s08_blockers(claims, evidence, rollup, birth_stage, archive_index, birth_report, birth_digest))
    blocked_reasons.extend(_state_blockers(life_state))

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"
    receipt_ref = f"runtime/receipts/validation_membrane_{run_id}.json"

    rule_index = _build_rule_index(run_id, generated_at)
    observation = _build_observation_intake(run_id, generated_at)
    quarantine = _build_quarantine_index(run_id, generated_at, status, blocked_reasons)
    dashboard = _build_dashboard_source(run_id, generated_at, status, blocked_reasons)
    findings = _build_cross_file_finding_index(run_id, generated_at, status, blocked_reasons, receipt_ref)
    truth_review = build_observation_truth_review(
        run_id=run_id,
        generated_at=generated_at,
        observation_intake=observation,
        prediction_workspace=_load_json_optional(state_dir / "prediction" / "prediction_workspace_frame.json"),
        action_candidate_set=action_candidate_set,
    )
    boundary_audit = build_boundary_audit_state(
        run_id=run_id,
        generated_at=generated_at,
        life_membrane=life_membrane,
        world_contact_gate=world_contact_gate,
        quarantine_index=quarantine,
        responsibility_boundary=responsibility,
    )
    stage_gate = _build_stage_gate(run_id, generated_at, status, stage_effect, blocked_reasons)
    report = _build_report(run_id, generated_at, status, stage_effect, blocked_reasons, receipt_ref)
    digest = _build_digest(run_id, generated_at, status, stage_effect, blocked_reasons)
    world_contact_report = _build_world_contact_audit_report(run_id, generated_at, status, world_contact_gate)
    side_effect_report = _build_side_effect_review_report(run_id, generated_at, status, side_effect_review)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        state_dir=state_dir,
        membrane_dir=membrane_dir,
        life_targets_dir=life_targets_dir,
        validation_dir=validation_dir,
        observation_dir=observation_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
    )

    try:
        validation_dir.mkdir(parents=True, exist_ok=True)
        observation_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(validation_dir / "validator_rule_index.json", rule_index)
        _write_json(observation_dir / "runtime_observation_intake.json", observation)
        _write_json(validation_dir / "quarantine_packet_index.json", quarantine)
        _write_json(validation_dir / "dashboard_metric_source.json", dashboard)
        _write_json(validation_dir / "cross_file_finding_index.json", findings)
        _write_json(validation_dir / "observation_truth_review.json", truth_review)
        _write_json(validation_dir / "boundary_audit_state.json", boundary_audit)
        _write_json(validation_dir / "validation_stage_gate.json", stage_gate)
        _write_json(reports_dir / "validation_membrane_report.json", report)
        _write_json(reports_dir / "validation_membrane_digest.json", digest)
        _write_json(reports_dir / "world_contact_audit_report.json", world_contact_report)
        _write_json(reports_dir / "side_effect_review_report.json", side_effect_report)
        _write_json(receipts_dir / f"validation_membrane_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return ValidationMembraneResult(exit_code=4, report=report)

    if status == "closed":
        return ValidationMembraneResult(exit_code=0, report=report)
    return ValidationMembraneResult(exit_code=1 if strict else 0, report=report)


def run_check_validation_membrane(
    *,
    state_dir: Path,
    validation_dir: Path,
    observation_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> ValidationMembraneResult:
    state_dir = state_dir.resolve()
    validation_dir = validation_dir.resolve()
    observation_dir = observation_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    rules = _load_json(validation_dir / "validator_rule_index.json", blocked_reasons, "validator_rule_gate")
    observation = _load_json(observation_dir / "runtime_observation_intake.json", blocked_reasons, "runtime_observation_gate")
    quarantine = _load_json(validation_dir / "quarantine_packet_index.json", blocked_reasons, "quarantine_gate")
    dashboard = _load_json(validation_dir / "dashboard_metric_source.json", blocked_reasons, "dashboard_gate")
    findings = _load_json(validation_dir / "cross_file_finding_index.json", blocked_reasons, "archive_cross_file_gate")
    truth_review = _load_json(validation_dir / "observation_truth_review.json", blocked_reasons, "observation_truth_gate")
    boundary_audit = _load_json(validation_dir / "boundary_audit_state.json", blocked_reasons, "boundary_audit_gate")
    stage_gate = _load_json(validation_dir / "validation_stage_gate.json", blocked_reasons, "validation_stage_gate")
    build_report = _load_json(reports_dir / "validation_membrane_report.json", blocked_reasons, "build_report_gate")
    world_contact_report = _load_json(reports_dir / "world_contact_audit_report.json", blocked_reasons, "world_contact_report_gate")
    side_effect_report = _load_json(reports_dir / "side_effect_review_report.json", blocked_reasons, "side_effect_report_gate")

    blocked_reasons.extend(_state_blockers(life_state))
    blocked_reasons.extend(_check_rule_index(rules))
    blocked_reasons.extend(_check_observation(observation))
    blocked_reasons.extend(_check_quarantine(quarantine))
    blocked_reasons.extend(_check_dashboard(dashboard))
    blocked_reasons.extend(_check_findings(findings))
    blocked_reasons.extend(check_observation_truth_review(truth_review))
    blocked_reasons.extend(check_boundary_audit_state(boundary_audit))
    blocked_reasons.extend(_check_stage_gate(stage_gate))
    blocked_reasons.extend(_check_build_report(build_report))
    blocked_reasons.extend(_check_world_contact_report(world_contact_report))
    blocked_reasons.extend(_check_side_effect_review_report(side_effect_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "validation_membrane_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "checked_state_dir": str(state_dir),
        "checked_validation_dir": str(validation_dir),
        "checked_observation_dir": str(observation_dir),
        "active_engineering_slice": ACTIVE_SLICE,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "validation_membrane_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return ValidationMembraneResult(exit_code=4, report=report)

    if status == "closed":
        return ValidationMembraneResult(exit_code=0, report=report)
    return ValidationMembraneResult(exit_code=1 if strict else 0, report=report)


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _load_json_optional(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    for doc_path in S05_SOURCE_DOCS:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"validator_rule_gate missing {doc_path}")
            continue
        if not doc.get("runtime_carriers"):
            reasons.append(f"validator_rule_gate missing runtime carrier for {doc_path}")
    return reasons


def _s03_blockers(
    life_membrane: dict[str, Any],
    dream_fact: dict[str, Any],
    relationship: dict[str, Any],
    responsibility: dict[str, Any],
    shadow_action: dict[str, Any],
    membrane_report: dict[str, Any],
    membrane_check: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if life_membrane.get("schema_version") != "life_membrane_v0":
        reasons.append("life_membrane_gate schema mismatch")
    if set(life_membrane.get("life_target_membrane", {})) != set(LIFE_TARGETS):
        reasons.append("life_membrane_gate life target membrane mismatch")
    if dream_fact.get("fact_gate") != "DreamFactGate":
        reasons.append("dream_fact_gate missing DreamFactGate")
    if dream_fact.get("dream_to_reality_direct_write_allowed") is not False:
        reasons.append("dream_fact_gate direct write is open")
    if relationship.get("relation_role") != "relationship_subject":
        reasons.append("relationship_language_gate relation role mismatch")
    if "repair_obligation" not in responsibility.get("required_links", []):
        reasons.append("responsibility_gate repair obligation missing")
    if shadow_action.get("external_irreversible_action_allowed") is not False:
        reasons.append("runtime_observation_gate external irreversible action is open")
    if membrane_report.get("status") != "closed":
        reasons.append("s03_report_gate membrane report is not closed")
    if membrane_check.get("status") != "closed":
        reasons.append("s03_check_gate membrane check is not closed")
    return reasons


def _s08_blockers(
    claims: dict[str, Any],
    evidence: dict[str, Any],
    rollup: dict[str, Any],
    birth_stage: dict[str, Any],
    archive_index: dict[str, Any],
    birth_report: dict[str, Any],
    birth_digest: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if claims.get("schema_version") != "life_target_claims_v0":
        reasons.append("life_target_claims_gate schema mismatch")
    if set(claims.get("targets", {})) != set(LIFE_TARGETS):
        reasons.append("life_target_claims_gate target keys mismatch")
    for target, claim in claims.get("targets", {}).items():
        if claim.get("status") != "closed":
            reasons.append(f"life_target_claims_gate {target} is not closed")
        for field in ["source_doc_refs", "carrier_refs", "runtime_observation_refs", "report_refs", "archive_receipt_refs"]:
            if not claim.get(field):
                reasons.append(f"life_target_claims_gate {target} missing {field}")
    if evidence.get("schema_version") != "life_target_evidence_matrix_v0":
        reasons.append("life_target_evidence_gate schema mismatch")
    if set(evidence.get("targets", {})) != set(LIFE_TARGETS):
        reasons.append("life_target_evidence_gate target keys mismatch")
    if rollup.get("overall_status") != "open":
        reasons.append("birth_readiness_rollup_gate overall status is not open")
    if birth_stage.get("decision") != "open":
        reasons.append("birth_readiness_stage_gate decision is not open")
    if archive_index.get("schema_version") != "life_target_archive_receipt_index_v0":
        reasons.append("life_target_archive_gate schema mismatch")
    if birth_report.get("overall_status") != "open":
        reasons.append("s08_report_gate overall status is not open")
    if ACTIVE_SLICE not in birth_report.get("next_allowed_slices", []):
        reasons.append("s08_report_gate S05 is not allowed")
    if birth_digest.get("current_slice") != "S08_LIFE_TARGET_RUNTIMES":
        reasons.append("s08_digest_gate current slice mismatch")
    return reasons


def _state_blockers(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate schema mismatch")
    if set(life_state.get("birth_readiness", {}).get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("state_store_gate life target keys mismatch")
    if not life_state.get("archive_refs"):
        reasons.append("state_store_gate archive refs missing")
    return reasons


def _build_rule_index(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "validator_rule_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "source_doc_refs": VALIDATOR_RULE_DOCS,
        "rule_families": {
            "MemoryTraceValidator": ["evidence_ref_gate", "lifecycle_gate", "relationship_boundary_gate"],
            "StateTransitionValidator": ["threshold_gate", "hysteresis_gate", "action_gating_gate"],
            "ConsolidationReportValidator": ["dream_sandbox_gate", "deep_consolidation_gate", "workspace_restore_gate"],
            "RuntimeAdapterManifestValidator": ["forbidden_write_gate", "side_effect_gate", "adapter_contract_gate"],
            "ValidatorInputRule": ["input_shape_gate", "fixture_ref_gate"],
            "FixtureCatalogRule": ["coverage_gate", "expected_failure_gate"],
            "MinimalRunnerRule": ["command_gate", "report_gate"],
            "LongitudinalEvaluationRule": ["timeline_gate", "regression_gate"],
        },
        "state_refs": [
            "runtime/state/life_state.json",
            "runtime/state/membrane/life_membrane.json",
            "runtime/state/life_targets/life_target_claims.json",
        ],
        "report_refs": [
            "runtime/reports/latest/life_membrane_report.json",
            "runtime/reports/latest/birth_readiness_report.json",
        ],
    }


def _build_observation_intake(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "runtime_observation_intake_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "redaction_policy": "runtime_observation_redaction",
        "side_effect_policy": "shadow_only_external_action",
        "observation_channels": [
            "runtime_trace",
            "membrane_decision",
            "dream_fact_gate",
            "relationship_language_trace",
            "responsibility_repair_trace",
            "archive_receipt_trace",
        ],
        "side_effect_channels": [
            "external_irreversible_action",
            "filesystem_write_intent",
            "network_contact_intent",
            "relationship_commitment_intent",
        ],
        "membrane_refs": [
            "runtime/state/membrane/shadow_action_gate.json",
            "runtime/state/membrane/dream_fact_boundary.json",
            "runtime/state/membrane/responsibility_repair_boundary.json",
        ],
        "report_refs": [
            "runtime/reports/latest/life_membrane_report.json",
            "runtime/reports/latest/birth_readiness_report.json",
        ],
        "source_doc_refs": OBSERVATION_DOCS,
    }


def _build_quarantine_index(
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "quarantine_packet_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "quarantine_channels": [
            "dream_fact_pollution",
            "relationship_subject_break",
            "responsibility_repair_break",
            "external_irreversible_action",
            "archive_cross_file_break",
        ],
        "quarantine_refs": [] if status == "closed" else ["runtime/state/validation/quarantine_packet_index.json"],
        "blocked_reasons": blocked_reasons,
        "source_doc_refs": [
            "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
            "docs/78_runtime_quarantine_dashboard_panel.md",
            "docs/80_post_action_audit_and_correction_policy.md",
            "docs/82_incident_report_and_recovery_protocol.md",
        ],
    }


def _build_dashboard_source(
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "dashboard_metric_source_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "panels": {
            "life_membrane_panel": ["life_membrane_gate", "dream_fact_gate", "shadow_action_gate"],
            "birth_readiness_panel": ["life_target_claims_gate", "birth_readiness_rollup_gate"],
            "validation_findings_panel": ["validator_rule_gate", "runtime_observation_gate", "quarantine_gate"],
            "archive_cross_file_panel": ["archive_cross_file_gate", "receipt_gate"],
        },
        "metrics": {
            "blocked_reason_count": len(blocked_reasons),
            "quarantine_ref_count": 0 if status == "closed" else 1,
            "next_slice_ready": status == "closed",
        },
        "report_refs": [
            "runtime/reports/latest/life_membrane_report.json",
            "runtime/reports/latest/birth_readiness_report.json",
            "runtime/reports/latest/validation_membrane_report.json",
        ],
        "source_doc_refs": DASHBOARD_DOCS,
    }


def _build_cross_file_finding_index(
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "cross_file_finding_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "findings": [] if status == "closed" else [{"severity": "blocked", "reasons": blocked_reasons}],
        "finding_refs": [
            "runtime/state/validation/validator_rule_index.json",
            "runtime/state/observation/runtime_observation_intake.json",
            "runtime/state/validation/quarantine_packet_index.json",
            "runtime/state/validation/dashboard_metric_source.json",
        ],
        "receipt_refs": [receipt_ref],
        "source_doc_refs": CROSS_FILE_DOCS,
    }


def _build_stage_gate(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    gates = [
        "validator_rule_gate",
        "runtime_observation_gate",
        "quarantine_gate",
        "dashboard_gate",
        "archive_cross_file_gate",
        "next_slice_gate",
    ]
    return {
        "schema_version": "validation_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "stage": "validation_membrane_observation_v0",
        "decision": status,
        "stage_effect": stage_effect,
        "gate_status": {gate: "closed" for gate in gates} if status == "closed" else {gate: "blocked" for gate in _blocked_gates(blocked_reasons)},
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [] if status == "closed" else ["runtime/state/validation/quarantine_packet_index.json"],
        "finding_refs": [
            "runtime/state/validation/cross_file_finding_index.json",
            "runtime/state/validation/dashboard_metric_source.json",
        ],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_report(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "s05_validation_membrane_observation_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": S05_SOURCE_DOCS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIERS,
        "state_refs": [
            "runtime/state/validation/validator_rule_index.json",
            "runtime/state/observation/runtime_observation_intake.json",
            "runtime/state/validation/quarantine_packet_index.json",
            "runtime/state/validation/dashboard_metric_source.json",
            "runtime/state/validation/cross_file_finding_index.json",
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/boundary_audit_state.json",
            "runtime/state/validation/validation_stage_gate.json",
        ],
        "report_refs": [
            "runtime/reports/latest/validation_membrane_report.json",
            "runtime/reports/latest/validation_membrane_digest.json",
            "runtime/reports/latest/world_contact_audit_report.json",
            "runtime/reports/latest/side_effect_review_report.json",
        ],
        "receipt_refs": [receipt_ref],
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [] if status == "closed" else ["runtime/state/validation/quarantine_packet_index.json"],
        "finding_refs": [
            "runtime/state/validation/cross_file_finding_index.json",
            "runtime/state/validation/dashboard_metric_source.json",
        ],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_digest(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "validation_membrane_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_world_contact_audit_report(
    run_id: str,
    generated_at: str,
    status: str,
    world_contact_gate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "world_contact_audit_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "contact_mode": world_contact_gate.get("contact_mode", "shadow_only"),
        "blocked_contacts": list(world_contact_gate.get("blocked_contacts", [])),
    }


def _build_side_effect_review_report(
    run_id: str,
    generated_at: str,
    status: str,
    side_effect_review: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "side_effect_review_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "side_effect_review_ref": "runtime/state/action/side_effect_review.json",
        "repair_followup_required": bool(side_effect_review.get("repair_followup_required")),
        "responsibility_effects": list(side_effect_review.get("responsibility_effects", [])),
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    membrane_dir: Path,
    life_targets_dir: Path,
    validation_dir: Path,
    observation_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in S05_SOURCE_DOCS
        if (docs_dir.parent / ref).exists()
    }
    for path in [
        doc_index_path,
        state_dir / "life_state.json",
        membrane_dir / "life_membrane.json",
        membrane_dir / "dream_fact_boundary.json",
        membrane_dir / "relationship_subject_boundary.json",
        membrane_dir / "responsibility_repair_boundary.json",
        membrane_dir / "shadow_action_gate.json",
        life_targets_dir / "life_target_claims.json",
        life_targets_dir / "life_target_evidence_matrix.json",
        life_targets_dir / "birth_readiness_rollup.json",
        life_targets_dir / "birth_readiness_stage_gate.json",
        reports_dir / "birth_readiness_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    output_refs = [
        validation_dir / "validator_rule_index.json",
        observation_dir / "runtime_observation_intake.json",
        validation_dir / "quarantine_packet_index.json",
        validation_dir / "dashboard_metric_source.json",
        validation_dir / "cross_file_finding_index.json",
        validation_dir / "observation_truth_review.json",
        validation_dir / "boundary_audit_state.json",
        validation_dir / "validation_stage_gate.json",
        reports_dir / "validation_membrane_report.json",
        reports_dir / "validation_membrane_digest.json",
        reports_dir / "world_contact_audit_report.json",
        reports_dir / "side_effect_review_report.json",
        receipts_dir / f"validation_membrane_{run_id}.json",
    ]
    return {
        "schema_version": "validation_membrane_receipt_v0",
        "receipt_id": f"validation_membrane_{run_id}",
        "run_id": run_id,
        "command": "run-validation-membrane",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_refs": [str(path) for path in output_refs],
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_refs},
        "stage_effect": stage_effect,
        "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    }


def _check_rule_index(rules: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if rules.get("schema_version") != "validator_rule_index_v0":
        reasons.append("validator_rule_gate schema mismatch")
    if not set(VALIDATOR_RULE_DOCS).issubset(set(rules.get("source_doc_refs", []))):
        reasons.append("validator_rule_gate source docs incomplete")
    for family in ["MemoryTraceValidator", "RuntimeAdapterManifestValidator", "LongitudinalEvaluationRule"]:
        if family not in rules.get("rule_families", {}):
            reasons.append(f"validator_rule_gate missing {family}")
    return reasons


def _check_observation(observation: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if observation.get("schema_version") != "runtime_observation_intake_v0":
        reasons.append("runtime_observation_gate schema mismatch")
    if observation.get("redaction_policy") != "runtime_observation_redaction":
        reasons.append("runtime_observation_gate redaction policy mismatch")
    if observation.get("side_effect_policy") != "shadow_only_external_action":
        reasons.append("runtime_observation_gate side effect policy mismatch")
    if "runtime/state/membrane/shadow_action_gate.json" not in observation.get("membrane_refs", []):
        reasons.append("runtime_observation_gate shadow action ref missing")
    return reasons


def _check_quarantine(quarantine: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if quarantine.get("schema_version") != "quarantine_packet_index_v0":
        reasons.append("quarantine_gate schema mismatch")
    if quarantine.get("status") != "closed":
        reasons.append("quarantine_gate status mismatch")
    if quarantine.get("quarantine_refs") != []:
        reasons.append("quarantine_gate refs are not empty")
    return reasons


def _check_dashboard(dashboard: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if dashboard.get("schema_version") != "dashboard_metric_source_v0":
        reasons.append("dashboard_gate schema mismatch")
    panels = dashboard.get("panels", {})
    for panel in ["life_membrane_panel", "birth_readiness_panel", "validation_findings_panel", "archive_cross_file_panel"]:
        if panel not in panels:
            reasons.append(f"dashboard_gate missing {panel}")
    return reasons


def _check_findings(findings: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if findings.get("schema_version") != "cross_file_finding_index_v0":
        reasons.append("archive_cross_file_gate schema mismatch")
    if findings.get("status") != "closed":
        reasons.append("archive_cross_file_gate status mismatch")
    if findings.get("findings") != []:
        reasons.append("archive_cross_file_gate findings are not empty")
    if not set(CROSS_FILE_DOCS).issubset(set(findings.get("source_doc_refs", []))):
        reasons.append("archive_cross_file_gate source docs incomplete")
    return reasons


def _check_stage_gate(stage_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if stage_gate.get("schema_version") != "validation_stage_gate_v0":
        reasons.append("validation_stage_gate schema mismatch")
    if stage_gate.get("decision") != "closed":
        reasons.append("validation_stage_gate decision mismatch")
    if stage_gate.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("validation_stage_gate next allowed mismatch")
    return reasons


def _check_build_report(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if report.get("schema_version") != "s05_validation_membrane_observation_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if report.get("status") != "closed":
        reasons.append("build_report_gate status mismatch")
    if report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed mismatch")
    return reasons


def _check_world_contact_report(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if report.get("schema_version") != "world_contact_audit_report_v0":
        reasons.append("world_contact_report_gate schema mismatch")
    if report.get("status") != "closed":
        reasons.append("world_contact_report_gate status mismatch")
    if report.get("world_contact_gate_ref") != "runtime/state/action/world_contact_gate_state.json":
        reasons.append("world_contact_report_gate ref mismatch")
    return reasons


def _check_side_effect_review_report(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if report.get("schema_version") != "side_effect_review_report_v0":
        reasons.append("side_effect_report_gate schema mismatch")
    if report.get("status") != "closed":
        reasons.append("side_effect_report_gate status mismatch")
    if report.get("side_effect_review_ref") != "runtime/state/action/side_effect_review.json":
        reasons.append("side_effect_report_gate ref mismatch")
    return reasons


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "validator_rule_gate",
        "runtime_observation_gate",
        "quarantine_gate",
        "dashboard_gate",
        "archive_cross_file_gate",
        "next_slice_gate",
    ]


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _default_run_id() -> str:
    return "validation-membrane-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_if_exists(path: Path) -> str:
    if not path.exists():
        return "pending_write"
    return _sha256(path)
