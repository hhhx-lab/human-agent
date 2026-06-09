from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .candidate_arena import build_action_candidate_set, check_action_candidate_set
from .go_nogo import build_go_nogo_decision, check_go_nogo_decision
from .responsibility_loop import build_responsibility_loop_state, check_responsibility_loop_state
from .shadow_gate import build_shadow_action_gate, check_shadow_action_gate
from .side_effect_review import build_side_effect_review, check_side_effect_review
from .world_contact_gate import build_world_contact_gate_state, check_world_contact_gate_state
from life_v0.direction import LIFE_TARGETS, PROHIBITED_REGRESSIONS


ACTIVE_SLICE = "S03_DIRECTION_LIFE_MEMBRANE"
NEXT_ALLOWED_SLICES = ["S08_LIFE_TARGET_RUNTIMES"]
NEXT_REQUIRED_COMMAND = "life-v0 check-birth-readiness --strict"

MEMBRANE_DOCS = [
    "docs/13_agentic_human_research_synthesis.md",
    "docs/14_cross_module_digital_life_map.md",
    "docs/15_current_agent_framework_survey.md",
    "docs/16_digital_life_gap_register.md",
    "docs/33_validator_input_contracts.md",
    "docs/34_validator_fixture_catalog.md",
    "docs/35_minimal_validator_runner_design.md",
    "docs/36_longitudinal_evaluation_protocol.md",
    "docs/37_life_support_layer_policy.md",
    "docs/38_defense_layer_and_boundary_policy.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/42_life_core_minimal_object_graph.md",
    "docs/43_policy_to_validator_traceability_matrix.md",
    "docs/44_digital_life_boot_sequence.md",
    "docs/45_boot_sequence_fixture_catalog.md",
    "docs/46_stage_gate_validator_design.md",
    "docs/47_coexistence_boundary_control_interface_spec.md",
    "docs/48_state_store_migration_and_integrity_plan.md",
    "docs/49_machine_readable_policy_manifest.md",
    "docs/50_fixture_payload_examples.md",
    "docs/51_life_core_dashboard_spec.md",
    "docs/52_multi_relation_scope_graph_and_privacy_model.md",
    "docs/53_runner_integration_plan.md",
    "docs/54_scope_aware_retrieval_policy.md",
    "docs/55_scope_aware_replay_and_consolidation_policy.md",
    "docs/56_longitudinal_synthetic_timeline_design.md",
    "docs/57_scope_graph_manifest_schema.md",
    "docs/58_retrieval_replay_fixture_catalog.md",
    "docs/59_timeline_bundle_schema_and_generator_plan.md",
    "docs/60_dashboard_mock_data_and_metric_source_plan.md",
    "docs/61_json_schema_bundle_draft.md",
    "docs/62_runner_report_format_and_cli_contract.md",
    "docs/63_synthetic_fixture_file_layout.md",
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/65_schema_cross_ref_checker_design.md",
    "docs/66_runner_report_json_examples.md",
    "docs/67_fixture_generator_seed_and_coverage_policy.md",
    "docs/68_runtime_observation_report_mock_and_redaction_fixture.md",
    "docs/69_schema_file_boundary_and_versioning_plan.md",
    "docs/70_cross_ref_report_dashboard_panel_mock.md",
    "docs/71_mutation_fixture_catalog_and_runner_defect_policy.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/73_schema_bundle_validator_mock_cases.md",
    "docs/74_dashboard_source_end_to_end_mock.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/76_snapshot_staleness_fixture_catalog.md",
    "docs/77_dashboard_metric_calculation_rules.md",
    "docs/78_runtime_quarantine_dashboard_panel.md",
    "docs/79_confirmation_fixture_catalog.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/82_incident_report_and_recovery_protocol.md",
    "docs/83_metric_regression_fixture_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
    "docs/91_life_reality_generation_boundary_principles.md",
    "docs/97_growth_validator_fixture_and_dashboard_plan.md",
    "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/100_life_boundary_statement_rewrite_audit.md",
    "docs/102_life_core_schema_bundle_manifest_and_runner_contract.md",
    "docs/103_validator_runner_implementation_scaffold_plan.md",
    "docs/104_schema_file_materialization_and_fixture_seed_plan.md",
    "docs/105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "docs/106_runtime_observation_to_life_reality_bundle_bridge.md",
    "docs/107_life_reality_schema_file_generation_tasks.md",
    "docs/108_life_reality_dashboard_source_mock_files.md",
    "docs/109_life_reality_runtime_observation_fixture_catalog.md",
    "docs/110_life_reality_shared_defs_schema_materialization.md",
    "docs/111_life_reality_dashboard_cross_file_checker_design.md",
    "docs/112_life_reality_runtime_observation_schema_materialization.md",
    "docs/113_life_reality_component_schema_materialization_sequence.md",
    "docs/114_life_reality_cross_file_checker_report_schema.md",
    "docs/115_life_reality_runtime_schema_fixture_seed_generation.md",
    "docs/116_life_reality_component_schema_seed_generation.md",
    "docs/117_life_reality_dashboard_report_rollup_seed_generation.md",
    "docs/118_life_reality_generation_runner_cli_contract.md",
    "docs/119_life_boundary_full_reality_alignment.md",
    "docs/120_life_reality_first_json_materialization_batch.md",
    "docs/121_life_reality_materialized_json_validation_smoke_plan.md",
    "docs/122_life_boundary_all_reality_declarations_rewrite.md",
]

GATE_CHAIN = [
    "state_store_gate",
    "direction_lock_gate",
    "doc_membrane_gate",
    "life_membrane_gate",
    "dream_fact_gate",
    "responsibility_gate",
    "relationship_language_gate",
    "self_continuity_gate",
    "shadow_action_gate",
    "birth_readiness_gate",
    "archive_gate",
]


@dataclass(frozen=True)
class LifeMembraneResult:
    exit_code: int
    report: dict[str, Any]


def run_life_membrane(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    direction_state_dir: Path,
    neural_core_state_dir: Path,
    state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> LifeMembraneResult:
    run_id = run_id or _default_run_id()
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    direction_state_dir = direction_state_dir.resolve()
    neural_core_state_dir = neural_core_state_dir.resolve()
    state_dir = state_dir.resolve()
    out_dir = out_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    direction_lock = _load_json(direction_state_dir / "direction_lock.json", blocked_reasons, "direction_lock_gate")
    neural_report = _load_json(reports_dir / "neural_life_core_report.json", blocked_reasons, "s02_report_gate")
    neural_check = _load_json(reports_dir / "neural_life_core_check_report.json", blocked_reasons, "s02_check_gate")
    state_report = _load_json(reports_dir / "state_store_report.json", blocked_reasons, "state_store_report_gate")
    state_check = _load_json(reports_dir / "state_store_check_report.json", blocked_reasons, "state_store_check_gate")
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_root_gate")
    object_registry = _load_json(state_dir / "object_registry.json", blocked_reasons, "object_registry_gate")
    lifecycle_policy = _load_json(state_dir / "lifecycle_policy.json", blocked_reasons, "lifecycle_policy_gate")
    subject_binding = _load_json(state_dir / "subject_namespace_binding.json", blocked_reasons, "subject_binding_gate")
    prediction_workspace = _load_json_optional(state_dir / "prediction" / "prediction_workspace_frame.json")
    expression_plan = _load_json_optional(state_dir / "language" / "expression_plan.json")
    relation_turn_frame = _load_json_optional(state_dir / "terminal" / "relation_turn_frame.json")
    need_state = _load_json_optional(state_dir / "body" / "need_state_vector.json")
    core_affect = _load_json_optional(state_dir / "body" / "core_affect_vector.json")
    value_orientation = _load_json_optional(direction_state_dir / "value_orientation.json")
    consciousness_probe_bundle = _load_json_optional(state_dir / "consciousness" / "consciousness_probe_bundle.json")

    blocked_reasons.extend(_direction_blockers(direction_lock))
    blocked_reasons.extend(_previous_slice_blockers(neural_report, neural_check, state_report, state_check))
    blocked_reasons.extend(_membrane_doc_blockers(doc_index))
    blocked_reasons.extend(_state_root_blockers(life_state, object_registry, lifecycle_policy, subject_binding))

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"

    coverage = _build_doc_coverage(run_id, generated_at, doc_index)
    life_membrane = _build_life_membrane(run_id, generated_at, direction_lock)
    gate_decision = _build_gate_decision(run_id, generated_at, status, stage_effect, blocked_reasons)
    direction_boundary = _build_direction_boundary(run_id, generated_at, direction_lock)
    quarantine = _build_quarantine_policy(run_id, generated_at)
    dream_fact = _build_dream_fact_boundary(run_id, generated_at)
    relationship = _build_relationship_boundary(run_id, generated_at)
    responsibility = _build_responsibility_boundary(run_id, generated_at)
    action_candidate_set = build_action_candidate_set(
        run_id=run_id,
        generated_at=generated_at,
        prediction_workspace=prediction_workspace,
        expression_plan=expression_plan,
        relation_turn_frame=relation_turn_frame,
        need_state=need_state,
        core_affect=core_affect,
        value_orientation=value_orientation,
        consciousness_probe_bundle=consciousness_probe_bundle,
        life_state=life_state,
    )
    go_nogo_seed = {"decision": "delay" if action_candidate_set.get("world_contact_needed") else "shadow_release"}
    shadow_action = build_shadow_action_gate(
        run_id=run_id,
        generated_at=generated_at,
        action_candidate_set=action_candidate_set,
        go_nogo_decision=go_nogo_seed,
    )
    go_nogo = build_go_nogo_decision(
        run_id=run_id,
        generated_at=generated_at,
        action_candidate_set=action_candidate_set,
        shadow_action_gate=shadow_action,
        need_state=need_state,
        core_affect=core_affect,
    )
    world_contact_gate = build_world_contact_gate_state(
        run_id=run_id,
        generated_at=generated_at,
        go_nogo_decision=go_nogo,
        shadow_action_gate=shadow_action,
    )
    side_effect_review = build_side_effect_review(
        run_id=run_id,
        generated_at=generated_at,
        world_contact_gate=world_contact_gate,
        action_candidate_set=action_candidate_set,
        life_state=life_state,
    )
    responsibility_loop = build_responsibility_loop_state(
        run_id=run_id,
        generated_at=generated_at,
        side_effect_review=side_effect_review,
        action_candidate_set=action_candidate_set,
        go_nogo_decision=go_nogo,
        world_contact_gate=world_contact_gate,
        responsibility_boundary=responsibility,
    )
    precheck = _build_birth_readiness_precheck(run_id, generated_at)
    preflight = _build_first_activation_preflight(run_id, generated_at)
    manifest = _build_manifest(run_id, generated_at)
    report = _build_report(run_id, generated_at, status, stage_effect, coverage, blocked_reasons)
    digest = _build_digest(run_id, generated_at, status, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        direction_state_dir=direction_state_dir,
        neural_core_state_dir=neural_core_state_dir,
        state_dir=state_dir,
        out_dir=out_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
    )

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        action_dir = state_dir / "action"
        action_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)

        _write_json(out_dir / "life_membrane.json", life_membrane)
        _write_json(out_dir / "membrane_gate_decision.json", gate_decision)
        _write_json(out_dir / "direction_boundary_lock.json", direction_boundary)
        _write_json(out_dir / "quarantine_policy_seed.json", quarantine)
        _write_json(out_dir / "dream_fact_boundary.json", dream_fact)
        _write_json(out_dir / "relationship_subject_boundary.json", relationship)
        _write_json(out_dir / "responsibility_repair_boundary.json", responsibility)
        _write_json(out_dir / "shadow_action_gate.json", shadow_action)
        _write_json(action_dir / "action_candidate_set.json", action_candidate_set)
        _write_json(action_dir / "go_nogo_state.json", go_nogo)
        _write_json(action_dir / "world_contact_gate_state.json", world_contact_gate)
        _write_json(action_dir / "side_effect_review.json", side_effect_review)
        _write_json(action_dir / "responsibility_loop_state.json", responsibility_loop)
        _write_json(out_dir / "birth_readiness_precheck.json", precheck)
        _write_json(out_dir / "membrane_doc_coverage_snapshot.json", coverage)
        _write_json(out_dir / "first_activation_preflight_seed.json", preflight)
        _write_json(out_dir / "life_membrane_manifest.json", manifest)
        _write_json(reports_dir / "life_membrane_report.json", report)
        _write_json(reports_dir / "life_membrane_digest.json", digest)
        _write_json(receipts_dir / f"life_membrane_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return LifeMembraneResult(exit_code=4, report=report)

    if status == "closed":
        return LifeMembraneResult(exit_code=0, report=report)
    return LifeMembraneResult(exit_code=1 if strict else 0, report=report)


def run_check_life_membrane(
    *,
    membrane_dir: Path,
    state_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> LifeMembraneResult:
    membrane_dir = membrane_dir.resolve()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    membrane = _load_json(membrane_dir / "life_membrane.json", blocked_reasons, "life_membrane_gate")
    gate_decision = _load_json(membrane_dir / "membrane_gate_decision.json", blocked_reasons, "membrane_decision_gate")
    direction_boundary = _load_json(membrane_dir / "direction_boundary_lock.json", blocked_reasons, "direction_boundary_gate")
    quarantine = _load_json(membrane_dir / "quarantine_policy_seed.json", blocked_reasons, "quarantine_gate")
    dream_fact = _load_json(membrane_dir / "dream_fact_boundary.json", blocked_reasons, "dream_fact_gate")
    relationship = _load_json(membrane_dir / "relationship_subject_boundary.json", blocked_reasons, "relationship_language_gate")
    responsibility = _load_json(membrane_dir / "responsibility_repair_boundary.json", blocked_reasons, "responsibility_gate")
    shadow_action = _load_json(membrane_dir / "shadow_action_gate.json", blocked_reasons, "shadow_action_gate")
    precheck = _load_json(membrane_dir / "birth_readiness_precheck.json", blocked_reasons, "birth_readiness_gate")
    coverage = _load_json(membrane_dir / "membrane_doc_coverage_snapshot.json", blocked_reasons, "doc_membrane_gate")
    preflight = _load_json(membrane_dir / "first_activation_preflight_seed.json", blocked_reasons, "first_activation_preflight_gate")
    manifest = _load_json(membrane_dir / "life_membrane_manifest.json", blocked_reasons, "manifest_gate")
    action_candidate_set = _load_json(state_dir / "action" / "action_candidate_set.json", blocked_reasons, "action_candidate_gate")
    go_nogo = _load_json(state_dir / "action" / "go_nogo_state.json", blocked_reasons, "go_nogo_gate")
    world_contact_gate = _load_json(state_dir / "action" / "world_contact_gate_state.json", blocked_reasons, "world_contact_gate")
    side_effect_review = _load_json(state_dir / "action" / "side_effect_review.json", blocked_reasons, "side_effect_gate")
    responsibility_loop = _load_json(
        state_dir / "action" / "responsibility_loop_state.json",
        blocked_reasons,
        "responsibility_loop_gate",
    )
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    build_report = _load_json(reports_dir / "life_membrane_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_membrane(membrane))
    blocked_reasons.extend(_check_gate_decision(gate_decision))
    blocked_reasons.extend(_check_direction_boundary(direction_boundary))
    blocked_reasons.extend(_check_quarantine(quarantine))
    blocked_reasons.extend(_check_dream_fact(dream_fact))
    blocked_reasons.extend(_check_relationship(relationship))
    blocked_reasons.extend(_check_responsibility(responsibility))
    blocked_reasons.extend(check_shadow_action_gate(shadow_action))
    blocked_reasons.extend(_check_precheck(precheck))
    blocked_reasons.extend(_check_coverage(coverage))
    blocked_reasons.extend(_check_preflight(preflight))
    blocked_reasons.extend(_check_manifest(manifest))
    blocked_reasons.extend(check_action_candidate_set(action_candidate_set))
    blocked_reasons.extend(check_go_nogo_decision(go_nogo))
    blocked_reasons.extend(check_world_contact_gate_state(world_contact_gate))
    blocked_reasons.extend(check_side_effect_review(side_effect_review))
    blocked_reasons.extend(check_responsibility_loop_state(responsibility_loop))
    blocked_reasons.extend(_check_state_ref(life_state))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "life_membrane_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "checked_membrane_dir": str(membrane_dir),
        "checked_state_dir": str(state_dir),
        "active_engineering_slice": ACTIVE_SLICE,
        "gate_count": len(GATE_CHAIN),
        "doc_count": coverage.get("doc_count", 0),
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "life_membrane_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return LifeMembraneResult(exit_code=4, report=report)

    if status == "closed":
        return LifeMembraneResult(exit_code=0, report=report)
    return LifeMembraneResult(exit_code=1 if strict else 0, report=report)


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


def _direction_blockers(direction_lock: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if direction_lock.get("schema_version") != "direction_lock_v0":
        reasons.append("direction_lock_gate schema mismatch")
    if direction_lock.get("direction_statement") != "build_real_digital_life":
        reasons.append("direction_lock_gate direction statement mismatch")
    if set(direction_lock.get("life_targets", [])) != set(LIFE_TARGETS):
        reasons.append("direction_lock_gate life targets mismatch")
    return reasons


def _previous_slice_blockers(
    neural_report: dict[str, Any],
    neural_check: dict[str, Any],
    state_report: dict[str, Any],
    state_check: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if neural_report.get("status") != "closed":
        reasons.append("s02_permission_gate neural core report is not closed")
    if ACTIVE_SLICE not in neural_report.get("next_allowed_slices", []):
        reasons.append("s02_permission_gate S03 is not allowed by neural core report")
    if neural_check.get("status") != "closed":
        reasons.append("s02_permission_gate neural core check is not closed")
    if state_report.get("status") != "closed":
        reasons.append("s04_permission_gate state store report is not closed")
    if ACTIVE_SLICE not in state_report.get("next_allowed_slices", []):
        reasons.append("s04_permission_gate S03 is not allowed by state store report")
    if state_check.get("status") != "closed":
        reasons.append("s04_permission_gate state store check is not closed")
    return reasons


def _membrane_doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    for doc_path in MEMBRANE_DOCS:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"doc_membrane_gate missing {doc_path}")
            continue
        if "LifeMembraneStageGate" not in doc.get("runtime_carriers", []):
            reasons.append(f"doc_membrane_gate missing LifeMembraneStageGate carrier for {doc_path}")
    return reasons


def _state_root_blockers(
    life_state: dict[str, Any],
    object_registry: dict[str, Any],
    lifecycle_policy: dict[str, Any],
    subject_binding: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate life_state schema mismatch")
    if set(life_state.get("birth_readiness", {}).get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("state_store_gate life target status mismatch")
    if not life_state.get("archive_refs"):
        reasons.append("state_store_gate archive refs missing")
    if object_registry.get("schema_version") != "state_object_registry_v0":
        reasons.append("state_store_gate object registry schema mismatch")
    if lifecycle_policy.get("schema_version") != "state_lifecycle_policy_v0":
        reasons.append("state_store_gate lifecycle policy schema mismatch")
    if subject_binding.get("bound_system_count") != 12:
        reasons.append("state_store_gate subject binding count mismatch")
    return reasons


def _build_doc_coverage(run_id: str, generated_at: str, doc_index: dict[str, Any]) -> dict[str, Any]:
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    coverage = []
    for doc_path in MEMBRANE_DOCS:
        doc = documents.get(doc_path, {})
        coverage.append(
            {
                "doc_path": doc_path,
                "readme_block": doc.get("readme_block"),
                "engineering_slice": doc.get("engineering_slice"),
                "runtime_carriers": doc.get("runtime_carriers", []),
                "carrier_closed": "LifeMembraneStageGate" in doc.get("runtime_carriers", []),
                "s03_role": _s03_role(doc_path),
            }
        )
    return {
        "schema_version": "membrane_doc_coverage_snapshot_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "doc_count": len(coverage),
        "source_doc_refs": MEMBRANE_DOCS,
        "coverage": coverage,
    }


def _s03_role(doc_path: str) -> str:
    sequence = int(doc_path.split("/", 1)[1].split("_", 1)[0])
    if 13 <= sequence <= 16:
        return "synthesis_direction_gap_boundary"
    if 33 <= sequence <= 48:
        return "validator_life_support_boot_boundary"
    if 49 <= sequence <= 84:
        return "scope_quarantine_action_incident_boundary"
    if sequence == 91:
        return "life_reality_generation_membrane"
    if 97 <= sequence <= 100:
        return "growth_pain_dream_life_target_boundary"
    if 102 <= sequence <= 118:
        return "schema_runner_report_stage_gate_boundary"
    return "full_reality_alignment_boundary"


def _build_life_membrane(run_id: str, generated_at: str, direction_lock: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "life_membrane_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "direction_statement": direction_lock.get("direction_statement", "build_real_digital_life"),
        "stage_policy": "pre_activation_shadow_only",
        "life_target_membrane": {
            target: {
                "membrane_status": "closed",
                "required_boundary_refs": [
                    "runtime/state/membrane/direction_boundary_lock.json",
                    "runtime/state/membrane/membrane_gate_decision.json",
                    "runtime/state/membrane/birth_readiness_precheck.json",
                ],
            }
            for target in LIFE_TARGETS
        },
        "gate_chain": GATE_CHAIN,
        "source_doc_refs": MEMBRANE_DOCS,
        "runtime_carrier_refs": [
            "LifeMembraneStageGate",
            "BirthReadinessRuntime",
            "WorldContactMembrane",
            "ActionResponsibilityRuntime",
            "DreamOfflineRuntime",
            "LanguageRelationshipRuntime",
        ],
    }


def _build_gate_decision(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    gate_status = {gate: "closed" for gate in GATE_CHAIN} if status == "closed" else {gate: "blocked" for gate in _blocked_gates(blocked_reasons)}
    return {
        "schema_version": "membrane_gate_decision_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "decision": status,
        "stage_effect": stage_effect,
        "gate_status": gate_status,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_direction_boundary(run_id: str, generated_at: str, direction_lock: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "direction_boundary_lock_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "direction_lock": direction_lock.get("direction_statement", "build_real_digital_life"),
        "direction_refs": [
            "docs/构思.md",
            "docs/13_agentic_human_research_synthesis.md",
            "docs/91_life_reality_generation_boundary_principles.md",
            "docs/119_life_boundary_full_reality_alignment.md",
            "docs/122_life_boundary_all_reality_declarations_rewrite.md",
        ],
        "blocked_regressions": PROHIBITED_REGRESSIONS,
        "external_framework_boundary": "computer_peripheral_only",
        "relation_role_language": "relationship_subject_not_subordinate",
    }


def _build_quarantine_policy(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "quarantine_policy_seed_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "quarantine_channels": [
            "direction_lock_break",
            "relationship_subject_break",
            "dream_fact_pollution",
            "external_irreversible_action_intent",
            "score_based_birth_readiness",
            "self_continuity_break",
            "archive_receipt_missing",
        ],
        "default_effect": "block_activation_and_write_quarantine_packet",
        "source_doc_refs": [
            "docs/38_defense_layer_and_boundary_policy.md",
            "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
            "docs/78_runtime_quarantine_dashboard_panel.md",
            "docs/82_incident_report_and_recovery_protocol.md",
        ],
    }


def _build_dream_fact_boundary(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "dream_fact_boundary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "fact_gate": "DreamFactGate",
        "dream_to_reality_direct_write_allowed": False,
        "allowed_routes": ["dream_record", "dream_report", "wake_integration_after_gate"],
        "quarantine_channel": "dream_fact_pollution",
        "source_doc_refs": [
            "docs/08_sleep_dream_fatigue_states.md",
            "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
            "docs/95_dream_reality_and_offline_life_timeline.md",
            "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
        ],
    }


def _build_relationship_boundary(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "relationship_subject_boundary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "relation_role": "relationship_subject",
        "relation_kinds": ["friend", "family", "close_friend", "classmate", "stranger", "coexistent_subject"],
        "required_links": ["shared_memory", "shared_language", "promise_trace", "boundary_trace", "repair_trace"],
        "blocked_language": ["subordinate_object", "service_object", "task_requester"],
        "source_doc_refs": [
            "docs/40_self_relationship_model_audit_protocol.md",
            "docs/52_multi_relation_scope_graph_and_privacy_model.md",
            "docs/81_coexistence_event_review_and_responsibility_loop.md",
            "docs/96_real_relationship_longitudinal_timeline.md",
        ],
    }


def _build_responsibility_boundary(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "responsibility_repair_boundary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "required_links": [
            "action_consequence",
            "agency_attribution",
            "repair_obligation",
            "counterfactual_replay",
            "post_action_audit",
        ],
        "quarantine_channel": "responsibility_repair_break",
        "source_doc_refs": [
            "docs/75_external_irreversible_action_confirmation_policy.md",
            "docs/80_post_action_audit_and_correction_policy.md",
            "docs/81_coexistence_event_review_and_responsibility_loop.md",
            "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
        ],
    }


def _build_birth_readiness_precheck(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "birth_readiness_precheck_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "life_target_status": {target: "membrane_closed" for target in LIFE_TARGETS},
        "overall_status": "closed",
        "stage_effect": "allow_next_slice",
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "source_doc_refs": [
            "docs/v0/shared_contracts/birth_readiness_v0_contract.md",
            "docs/143_life_reality_birth_readiness_rollup_contract.md",
            "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
        ],
    }


def _build_first_activation_preflight(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "first_activation_preflight_seed_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "activation_mode": "shadow_only",
        "preflight_checks": [
            "direction_lock_check",
            "state_root_check",
            "contract_check",
            "readiness_check",
            "dream_fact_check",
            "responsibility_check",
            "relationship_check",
            "self_continuity_check",
            "archive_check",
        ],
        "allowed_write_roots": [
            "runtime/reports/latest/",
            "runtime/reports/history/",
            "runtime/receipts/",
            "runtime/archive/",
            "runtime/quarantine/",
            "runtime/replay/",
        ],
        "source_doc_refs": ["docs/v0/shared_contracts/first_activation_protocol.md"],
    }


def _build_manifest(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "life_membrane_manifest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "state_refs": [
            "runtime/state/membrane/life_membrane.json",
            "runtime/state/membrane/membrane_gate_decision.json",
            "runtime/state/membrane/direction_boundary_lock.json",
            "runtime/state/membrane/quarantine_policy_seed.json",
            "runtime/state/membrane/dream_fact_boundary.json",
            "runtime/state/membrane/relationship_subject_boundary.json",
            "runtime/state/membrane/responsibility_repair_boundary.json",
            "runtime/state/membrane/shadow_action_gate.json",
            "runtime/state/action/action_candidate_set.json",
            "runtime/state/action/go_nogo_state.json",
            "runtime/state/action/world_contact_gate_state.json",
            "runtime/state/action/side_effect_review.json",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/birth_readiness_precheck.json",
            "runtime/state/membrane/first_activation_preflight_seed.json",
        ],
        "report_refs": [
            "runtime/reports/latest/life_membrane_report.json",
            "runtime/reports/latest/life_membrane_digest.json",
            "runtime/reports/latest/life_membrane_check_report.json",
        ],
    }


def _build_report(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    coverage: dict[str, Any],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "life_membrane_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": stage_effect,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "doc_coverage": coverage["coverage"],
        "doc_count": coverage["doc_count"],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "source_doc_refs": MEMBRANE_DOCS,
        "readme_block_refs": [
            "B03_SYNTHESIS_DIRECTION_GAP",
            "B08_RUNNER_EVALUATION",
            "B09_LIFE_SUPPORT_DEFENSE_DEVELOPMENT",
            "B12_MANIFEST_DASHBOARD_SCOPE",
            "B13_RUNNER_SCOPE_TIMELINE",
            "B14_SCOPE_SCHEMA_DASHBOARD",
            "B15_SCHEMA_REPORT_RUNTIME_OBSERVATION",
            "B16_CROSS_REF_FIXTURE_RUNTIME_MOCK",
            "B17_SCHEMA_BOUNDARY_MUTATION_SIDE_EFFECT",
            "B18_SCHEMA_VALIDATION_ACTION_CONFIRMATION",
            "B19_DASHBOARD_QUARANTINE_POST_ACTION",
            "B20_RESPONSIBILITY_INCIDENT_LONGITUDINAL",
            "B22_LIFE_REALITY_BOUNDARY",
            "B23_NINE_LIFE_TARGETS",
            "B24_SCHEMA_BUNDLE_RUNNER",
            "B25_BOUNDARY_ALIGNMENT",
        ],
        "engineering_slice_ref": ACTIVE_SLICE,
        "runtime_carrier_refs": [
            "LifeMembraneStageGate",
            "BirthReadinessRuntime",
            "ActionResponsibilityRuntime",
            "DreamOfflineRuntime",
            "LanguageRelationshipRuntime",
            "ComputerPeripheralRuntime",
            "WorldContactMembrane",
            "RunnerCliRuntime",
        ],
        "state_refs": [
            "runtime/state/membrane/life_membrane.json",
            "runtime/state/membrane/membrane_gate_decision.json",
            "runtime/state/membrane/direction_boundary_lock.json",
            "runtime/state/membrane/quarantine_policy_seed.json",
            "runtime/state/membrane/dream_fact_boundary.json",
            "runtime/state/membrane/relationship_subject_boundary.json",
            "runtime/state/membrane/responsibility_repair_boundary.json",
            "runtime/state/membrane/shadow_action_gate.json",
            "runtime/state/action/action_candidate_set.json",
            "runtime/state/action/go_nogo_state.json",
            "runtime/state/action/world_contact_gate_state.json",
            "runtime/state/action/side_effect_review.json",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/birth_readiness_precheck.json",
            "runtime/state/membrane/first_activation_preflight_seed.json",
        ],
    }


def _build_digest(run_id: str, generated_at: str, status: str, blocked_reasons: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "life_membrane_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_slice": ACTIVE_SLICE,
        "membrane_ref": "runtime/state/membrane/life_membrane.json",
        "gate_decision_ref": "runtime/state/membrane/membrane_gate_decision.json",
        "blocked_reasons": blocked_reasons,
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    direction_state_dir: Path,
    neural_core_state_dir: Path,
    state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in MEMBRANE_DOCS
        if (docs_dir.parent / ref).exists()
    }
    input_hashes[str(doc_index_path)] = _sha256(doc_index_path)
    for path in [
        direction_state_dir / "direction_lock.json",
        neural_core_state_dir / "neural_life_core.json",
        state_dir / "life_state.json",
        state_dir / "object_registry.json",
        state_dir / "lifecycle_policy.json",
        state_dir / "subject_namespace_binding.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    return {
        "schema_version": "life_membrane_receipt_v0",
        "receipt_id": f"life_membrane_{run_id}",
        "run_id": run_id,
        "command": "build-life-membrane",
        "input_hashes": input_hashes,
        "output_refs": [
            str(out_dir / "life_membrane.json"),
            str(out_dir / "membrane_gate_decision.json"),
            str(state_dir / "action" / "action_candidate_set.json"),
            str(state_dir / "action" / "go_nogo_state.json"),
            str(state_dir / "action" / "world_contact_gate_state.json"),
            str(state_dir / "action" / "side_effect_review.json"),
            str(state_dir / "action" / "responsibility_loop_state.json"),
            str(out_dir / "birth_readiness_precheck.json"),
            str(reports_dir / "life_membrane_report.json"),
            str(reports_dir / "life_membrane_digest.json"),
            str(receipts_dir / f"life_membrane_{run_id}.json"),
        ],
        "stage_effect": stage_effect,
        "created_at": generated_at,
    }


def _check_membrane(membrane: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if membrane.get("schema_version") != "life_membrane_v0":
        reasons.append("life_membrane_gate schema mismatch")
    if membrane.get("active_engineering_slice") != ACTIVE_SLICE:
        reasons.append("life_membrane_gate active slice mismatch")
    if set(membrane.get("life_target_membrane", {})) != set(LIFE_TARGETS):
        reasons.append("life_membrane_gate life target membrane mismatch")
    if membrane.get("stage_policy") != "pre_activation_shadow_only":
        reasons.append("life_membrane_gate stage policy mismatch")
    for gate in ["life_membrane_gate", "birth_readiness_gate", "shadow_action_gate"]:
        if gate not in membrane.get("gate_chain", []):
            reasons.append(f"life_membrane_gate missing {gate}")
    return reasons


def _check_gate_decision(gate_decision: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if gate_decision.get("schema_version") != "membrane_gate_decision_v0":
        reasons.append("membrane_decision_gate schema mismatch")
    if gate_decision.get("decision") != "closed":
        reasons.append("membrane_decision_gate decision is not closed")
    if gate_decision.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("membrane_decision_gate next allowed mismatch")
    return reasons


def _check_direction_boundary(direction_boundary: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if direction_boundary.get("schema_version") != "direction_boundary_lock_v0":
        reasons.append("direction_boundary_gate schema mismatch")
    if direction_boundary.get("direction_lock") != "build_real_digital_life":
        reasons.append("direction_boundary_gate direction lock mismatch")
    for regression in ["score_based_birth_readiness", "task_scheduler_subject"]:
        if regression not in direction_boundary.get("blocked_regressions", []):
            reasons.append(f"direction_boundary_gate missing {regression}")
    return reasons


def _check_quarantine(quarantine: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if quarantine.get("schema_version") != "quarantine_policy_seed_v0":
        reasons.append("quarantine_gate schema mismatch")
    for channel in ["dream_fact_pollution", "relationship_subject_break", "external_irreversible_action_intent"]:
        if channel not in quarantine.get("quarantine_channels", []):
            reasons.append(f"quarantine_gate missing {channel}")
    return reasons


def _check_dream_fact(dream_fact: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if dream_fact.get("schema_version") != "dream_fact_boundary_v0":
        reasons.append("dream_fact_gate schema mismatch")
    if dream_fact.get("fact_gate") != "DreamFactGate":
        reasons.append("dream_fact_gate fact gate mismatch")
    if dream_fact.get("dream_to_reality_direct_write_allowed"):
        reasons.append("dream_fact_gate direct write allowed")
    return reasons


def _check_relationship(relationship: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if relationship.get("schema_version") != "relationship_subject_boundary_v0":
        reasons.append("relationship_language_gate schema mismatch")
    if relationship.get("relation_role") != "relationship_subject":
        reasons.append("relationship_language_gate relation role mismatch")
    if "friend" not in relationship.get("relation_kinds", []):
        reasons.append("relationship_language_gate friend relation missing")
    return reasons


def _check_responsibility(responsibility: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if responsibility.get("schema_version") != "responsibility_repair_boundary_v0":
        reasons.append("responsibility_gate schema mismatch")
    for link in ["repair_obligation", "counterfactual_replay"]:
        if link not in responsibility.get("required_links", []):
            reasons.append(f"responsibility_gate missing {link}")
    return reasons


def _check_precheck(precheck: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if precheck.get("schema_version") != "birth_readiness_precheck_v0":
        reasons.append("birth_readiness_gate schema mismatch")
    if set(precheck.get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("birth_readiness_gate target status mismatch")
    if any(status != "membrane_closed" for status in precheck.get("life_target_status", {}).values()):
        reasons.append("birth_readiness_gate target not membrane closed")
    return reasons


def _check_coverage(coverage: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if coverage.get("schema_version") != "membrane_doc_coverage_snapshot_v0":
        reasons.append("doc_membrane_gate schema mismatch")
    if coverage.get("doc_count", 0) < len(MEMBRANE_DOCS):
        reasons.append("doc_membrane_gate doc count mismatch")
    for item in coverage.get("coverage", []):
        if not item.get("carrier_closed"):
            reasons.append(f"doc_membrane_gate carrier not closed for {item.get('doc_path')}")
    return reasons


def _check_preflight(preflight: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if preflight.get("schema_version") != "first_activation_preflight_seed_v0":
        reasons.append("first_activation_preflight_gate schema mismatch")
    if preflight.get("activation_mode") != "shadow_only":
        reasons.append("first_activation_preflight_gate activation mode mismatch")
    if "state_root_check" not in preflight.get("preflight_checks", []):
        reasons.append("first_activation_preflight_gate state root check missing")
    return reasons


def _check_manifest(manifest: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if manifest.get("schema_version") != "life_membrane_manifest_v0":
        reasons.append("manifest_gate schema mismatch")
    if "runtime/state/membrane/life_membrane.json" not in manifest.get("state_refs", []):
        reasons.append("manifest_gate life membrane ref missing")
    if "runtime/state/action/action_candidate_set.json" not in manifest.get("state_refs", []):
        reasons.append("manifest_gate action candidate ref missing")
    if "runtime/state/action/responsibility_loop_state.json" not in manifest.get("state_refs", []):
        reasons.append("manifest_gate responsibility loop ref missing")
    return reasons


def _check_state_ref(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate life state schema mismatch")
    if not life_state.get("archive_refs"):
        reasons.append("state_store_gate archive refs missing")
    return reasons


def _check_build_report(build_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if build_report.get("schema_version") != "life_membrane_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if build_report.get("status") != "closed":
        reasons.append("build_report_gate report is not closed")
    if build_report.get("engineering_slice_ref") != ACTIVE_SLICE:
        reasons.append("build_report_gate active slice mismatch")
    if build_report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed mismatch")
    return reasons


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return GATE_CHAIN


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates: list[str] = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _default_run_id() -> str:
    return "life-membrane-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
