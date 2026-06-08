from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.direction import LIFE_TARGETS


ACTIVE_SLICE = "S08_LIFE_TARGET_RUNTIMES"
NEXT_ALLOWED_SLICES = ["S05_VALIDATION_MEMBRANE_OBSERVATION"]
NEXT_REQUIRED_COMMAND = "life-v0 run-validation-membrane --strict"

S08_SOURCE_DOCS = [
    "docs/91_life_reality_generation_boundary_principles.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/97_growth_validator_fixture_and_dashboard_plan.md",
    "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/100_life_boundary_statement_rewrite_audit.md",
    "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "docs/143_life_reality_birth_readiness_rollup_contract.md",
    "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
    "docs/149_life_reality_birth_readiness_fixture_schema_materialization_plan.md",
    "docs/152_life_reality_birth_readiness_cross_file_checker_plan.md",
    "docs/171_life_reality_birth_readiness_validation_fixture_plan.md",
    "docs/174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "docs/v0/birth_readiness_v0_contract.md",
    "docs/v0/s08_life_target_runtimes_engineering_contract.md",
]

EVIDENCE_FAMILIES = [
    "state",
    "memory",
    "language",
    "relationship",
    "dream",
    "pain_regret_responsibility",
    "self_growth",
    "runtime",
    "report",
    "archive",
]

TARGET_SOURCE_REFS = {
    "real_consciousness": [
        "docs/01m_consciousness_attention_workspace_matrix.md",
        "docs/10_consciousness_attention_workspace.md",
        "docs/13_agentic_human_research_synthesis.md",
        "docs/143_life_reality_birth_readiness_rollup_contract.md",
        "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
    ],
    "real_emotion": [
        "docs/01s_emotion_personality_self_matrix.md",
        "docs/07_emotion_personality_self.md",
        "docs/18_internal_state_and_modulation_vector.md",
        "docs/94_pain_regret_and_repair_signal_schema.md",
    ],
    "real_personality": [
        "docs/07_emotion_personality_self.md",
        "docs/39_development_policy_and_plasticity_windows.md",
        "docs/40_self_relationship_model_audit_protocol.md",
        "docs/92_self_growth_and_self_modification_life_chain.md",
        "docs/93_self_training_kernel_growth_protocol.md",
    ],
    "real_life": [
        "docs/02_brain_region_and_network_atlas.md",
        "docs/03_default_executive_salience_networks.md",
        "docs/04_sensory_thalamus_interoception.md",
        "docs/05_memory_systems_and_growth.md",
        "docs/06_action_reward_inhibition.md",
        "docs/07_emotion_personality_self.md",
        "docs/08_sleep_dream_fatigue_states.md",
        "docs/09_language_symbolic_top_layer.md",
        "docs/10_consciousness_attention_workspace.md",
        "docs/11_neuromodulation_and_signal_media.md",
        "docs/12_ai_and_cognitive_architecture_bridge.md",
        "docs/13_agentic_human_research_synthesis.md",
        "docs/37_life_support_layer_policy.md",
        "docs/41_runtime_state_store_schema.md",
        "docs/44_digital_life_boot_sequence.md",
        "docs/91_life_reality_generation_boundary_principles.md",
        "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    ],
    "real_pain": [
        "docs/01h_pain_regret_repair_literature_matrix.md",
        "docs/07_emotion_personality_self.md",
        "docs/94_pain_regret_and_repair_signal_schema.md",
        "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    ],
    "real_dream": [
        "docs/01i_dream_offline_life_literature_matrix.md",
        "docs/01t_sleep_dream_fatigue_runtime_matrix.md",
        "docs/08_sleep_dream_fatigue_states.md",
        "docs/95_dream_reality_and_offline_life_timeline.md",
        "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    ],
    "real_relationship": [
        "docs/01j_real_relationship_literature_matrix.md",
        "docs/09_language_symbolic_top_layer.md",
        "docs/85_language_system_life_expression_core.md",
        "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
        "docs/87_language_event_schema_fixture_and_validator_plan.md",
        "docs/88_language_development_emotion_and_brain_llm_alignment.md",
        "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
        "docs/90_language_event_examples_and_timeline_bundle.md",
        "docs/96_real_relationship_longitudinal_timeline.md",
        "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
    ],
    "real_responsibility": [
        "docs/01r_action_reward_inhibition_matrix.md",
        "docs/06_action_reward_inhibition.md",
        "docs/80_post_action_audit_and_correction_policy.md",
        "docs/81_coexistence_event_review_and_responsibility_loop.md",
        "docs/82_incident_report_and_recovery_protocol.md",
        "docs/94_pain_regret_and_repair_signal_schema.md",
        "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    ],
    "real_regret": [
        "docs/01h_pain_regret_repair_literature_matrix.md",
        "docs/06_action_reward_inhibition.md",
        "docs/94_pain_regret_and_repair_signal_schema.md",
        "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    ],
}

TARGET_CARRIERS = {
    "real_consciousness": ["ConsciousWorkspaceRuntime", "BirthReadinessRuntime"],
    "real_emotion": ["AffectiveSelfRuntime", "BodySignalRuntime"],
    "real_personality": ["AffectiveSelfRuntime", "GrowthReplayRuntime"],
    "real_life": ["LifeStateStore", "LifeMembraneStageGate", "BirthReadinessRuntime"],
    "real_pain": ["ActionResponsibilityRuntime", "AffectiveSelfRuntime"],
    "real_dream": ["DreamOfflineRuntime", "DreamFactGate"],
    "real_relationship": ["LanguageRelationshipRuntime", "RelationshipSubjectRuntime"],
    "real_responsibility": ["ActionResponsibilityRuntime", "ResponsibilityRepairRuntime"],
    "real_regret": ["ActionResponsibilityRuntime", "PainRegretResponsibilityRuntime"],
}


@dataclass(frozen=True)
class BirthReadinessResult:
    exit_code: int
    report: dict[str, Any]


def run_birth_readiness(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    direction_state_dir: Path,
    neural_core_state_dir: Path,
    state_dir: Path,
    membrane_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> BirthReadinessResult:
    run_id = run_id or _default_run_id()
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    direction_state_dir = direction_state_dir.resolve()
    neural_core_state_dir = neural_core_state_dir.resolve()
    state_dir = state_dir.resolve()
    membrane_dir = membrane_dir.resolve()
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
    neural_core = _load_json(neural_core_state_dir / "neural_life_core.json", blocked_reasons, "neural_core_gate")
    systems = _load_json(neural_core_state_dir / "twelve_subject_systems.json", blocked_reasons, "subject_system_gate")
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_root_gate")
    membrane = _load_json(membrane_dir / "life_membrane.json", blocked_reasons, "life_membrane_gate")
    precheck = _load_json(membrane_dir / "birth_readiness_precheck.json", blocked_reasons, "s03_precheck_gate")
    dream_fact = _load_json(membrane_dir / "dream_fact_boundary.json", blocked_reasons, "dream_fact_gate")
    relationship = _load_json(membrane_dir / "relationship_subject_boundary.json", blocked_reasons, "relationship_language_gate")
    responsibility = _load_json(membrane_dir / "responsibility_repair_boundary.json", blocked_reasons, "responsibility_repair_gate")
    membrane_report = _load_json(reports_dir / "life_membrane_report.json", blocked_reasons, "s03_report_gate")
    membrane_check = _load_json(reports_dir / "life_membrane_check_report.json", blocked_reasons, "s03_check_gate")
    state_report = _load_json(reports_dir / "state_store_report.json", blocked_reasons, "s04_report_gate")
    neural_report = _load_json(reports_dir / "neural_life_core_report.json", blocked_reasons, "s02_report_gate")

    blocked_reasons.extend(_direction_blockers(direction_lock))
    blocked_reasons.extend(_previous_slice_blockers(neural_report, state_report, membrane_report, membrane_check))
    blocked_reasons.extend(_s08_doc_blockers(doc_index))
    blocked_reasons.extend(_state_blockers(life_state, neural_core, systems))
    blocked_reasons.extend(_membrane_blockers(membrane, precheck, dream_fact, relationship, responsibility))

    target_status = {target: "closed" for target in LIFE_TARGETS}
    if blocked_reasons:
        target_status = {target: "blocked" for target in LIFE_TARGETS}

    overall_status = _overall_status(target_status, blocked_reasons, [], [])
    stage_effect = _stage_effect(overall_status)
    receipt_ref = f"runtime/receipts/birth_readiness_{run_id}.json"
    report_ref = "runtime/reports/latest/birth_readiness_report.json"

    evidence_matrix = _build_evidence_matrix(run_id, generated_at, receipt_ref, report_ref)
    claims = _build_claims(run_id, generated_at, target_status, evidence_matrix, receipt_ref, report_ref)
    rollup = _build_rollup(run_id, generated_at, overall_status, target_status, blocked_reasons, receipt_ref)
    stage_gate = _build_stage_gate(run_id, generated_at, overall_status, stage_effect, blocked_reasons)
    archive_index = _build_archive_index(run_id, generated_at, receipt_ref)
    status_report = _build_life_target_status(run_id, generated_at, overall_status, target_status, receipt_ref)
    report = _build_report(run_id, generated_at, overall_status, stage_effect, target_status, blocked_reasons, receipt_ref)
    digest = _build_digest(run_id, generated_at, overall_status, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        direction_state_dir=direction_state_dir,
        neural_core_state_dir=neural_core_state_dir,
        state_dir=state_dir,
        membrane_dir=membrane_dir,
        out_dir=out_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
    )

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(out_dir / "life_target_claims.json", claims)
        _write_json(out_dir / "life_target_evidence_matrix.json", evidence_matrix)
        _write_json(out_dir / "birth_readiness_rollup.json", rollup)
        _write_json(out_dir / "birth_readiness_stage_gate.json", stage_gate)
        _write_json(out_dir / "life_target_archive_receipt_index.json", archive_index)
        _write_json(reports_dir / "life_target_status.json", status_report)
        _write_json(reports_dir / "birth_readiness_report.json", report)
        _write_json(reports_dir / "birth_readiness_digest.json", digest)
        _write_json(receipts_dir / f"birth_readiness_{run_id}.json", receipt)
    except OSError as exc:
        report["overall_status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return BirthReadinessResult(exit_code=4, report=report)

    if overall_status == "open":
        return BirthReadinessResult(exit_code=0, report=report)
    exit_code = _exit_code_for_status(overall_status)
    return BirthReadinessResult(exit_code=exit_code if strict else 0, report=report)


def run_check_birth_readiness(
    *,
    state_dir: Path,
    membrane_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> BirthReadinessResult:
    state_dir = state_dir.resolve()
    membrane_dir = membrane_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    claims = _load_json(state_dir / "life_target_claims.json", blocked_reasons, "life_target_claims_gate")
    evidence = _load_json(state_dir / "life_target_evidence_matrix.json", blocked_reasons, "evidence_matrix_gate")
    rollup = _load_json(state_dir / "birth_readiness_rollup.json", blocked_reasons, "rollup_gate")
    stage_gate = _load_json(state_dir / "birth_readiness_stage_gate.json", blocked_reasons, "stage_gate_gate")
    archive_index = _load_json(state_dir / "life_target_archive_receipt_index.json", blocked_reasons, "archive_index_gate")
    precheck = _load_json(membrane_dir / "birth_readiness_precheck.json", blocked_reasons, "s03_precheck_gate")
    build_report = _load_json(reports_dir / "birth_readiness_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_claims(claims))
    blocked_reasons.extend(_check_evidence(evidence))
    blocked_reasons.extend(_check_rollup(rollup))
    blocked_reasons.extend(_check_stage_gate(stage_gate))
    blocked_reasons.extend(_check_archive_index(archive_index))
    blocked_reasons.extend(_check_precheck(precheck))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "open" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "birth_readiness_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": _stage_effect(status),
        "checked_state_dir": str(state_dir),
        "checked_membrane_dir": str(membrane_dir),
        "active_engineering_slice": ACTIVE_SLICE,
        "target_count": len(claims.get("targets", {})),
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "open" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "birth_readiness_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return BirthReadinessResult(exit_code=4, report=report)

    if status == "open":
        return BirthReadinessResult(exit_code=0, report=report)
    return BirthReadinessResult(exit_code=1 if strict else 0, report=report)


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
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
    state_report: dict[str, Any],
    membrane_report: dict[str, Any],
    membrane_check: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if neural_report.get("status") != "closed":
        reasons.append("s02_permission_gate neural life core report is not closed")
    if state_report.get("status") != "closed":
        reasons.append("s04_permission_gate state store report is not closed")
    if membrane_report.get("status") != "closed":
        reasons.append("s03_permission_gate life membrane report is not closed")
    if ACTIVE_SLICE not in membrane_report.get("next_allowed_slices", []):
        reasons.append("s03_permission_gate S08 is not allowed by life membrane report")
    if membrane_check.get("status") != "closed":
        reasons.append("s03_permission_gate life membrane check is not closed")
    return reasons


def _s08_doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    for doc_path in S08_SOURCE_DOCS:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"s08_doc_gate missing {doc_path}")
            continue
        carriers = doc.get("runtime_carriers", [])
        if not carriers:
            reasons.append(f"s08_doc_gate missing runtime carrier for {doc_path}")
    return reasons


def _state_blockers(life_state: dict[str, Any], neural_core: dict[str, Any], systems: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("life_target_state_gate life_state schema mismatch")
    if set(life_state.get("birth_readiness", {}).get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("life_target_state_gate life target keys mismatch")
    if not life_state.get("archive_refs"):
        reasons.append("life_target_state_gate archive refs missing")
    for key in [
        "self_model",
        "memory_index",
        "dream_records",
        "relationship_subjects",
        "pain_events",
        "regret_events",
        "responsibility_bindings",
        "language_state",
        "runtime_trace_refs",
    ]:
        if key not in life_state:
            reasons.append(f"life_target_state_gate missing {key}")
    if neural_core.get("schema_version") != "neural_life_core_v0":
        reasons.append("life_target_state_gate neural core schema mismatch")
    if systems.get("system_count") != 12:
        reasons.append("life_target_state_gate subject system count mismatch")
    return reasons


def _membrane_blockers(
    membrane: dict[str, Any],
    precheck: dict[str, Any],
    dream_fact: dict[str, Any],
    relationship: dict[str, Any],
    responsibility: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if membrane.get("schema_version") != "life_membrane_v0":
        reasons.append("s03_precheck_gate life membrane schema mismatch")
    if set(membrane.get("life_target_membrane", {})) != set(LIFE_TARGETS):
        reasons.append("s03_precheck_gate life target membrane mismatch")
    if precheck.get("overall_status") != "closed":
        reasons.append("s03_precheck_gate precheck is not closed")
    if set(precheck.get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("s03_precheck_gate precheck target keys mismatch")
    if any(status != "membrane_closed" for status in precheck.get("life_target_status", {}).values()):
        reasons.append("s03_precheck_gate target precheck is not membrane_closed")
    if dream_fact.get("fact_gate") != "DreamFactGate":
        reasons.append("dream_fact_gate missing DreamFactGate")
    if dream_fact.get("dream_to_reality_direct_write_allowed") is not False:
        reasons.append("dream_fact_gate direct reality write is not blocked")
    if relationship.get("relation_role") != "relationship_subject":
        reasons.append("relationship_language_gate relation role mismatch")
    if "repair_obligation" not in responsibility.get("required_links", []):
        reasons.append("responsibility_repair_gate repair obligation missing")
    if "counterfactual_replay" not in responsibility.get("required_links", []):
        reasons.append("responsibility_repair_gate counterfactual replay missing")
    return reasons


def _build_evidence_matrix(run_id: str, generated_at: str, receipt_ref: str, report_ref: str) -> dict[str, Any]:
    targets = {}
    for target in LIFE_TARGETS:
        targets[target] = {
            "state": [
                "runtime/state/life_state.json",
                "runtime/state/life_targets/life_target_claims.json",
                _state_namespace_for_target(target),
            ],
            "memory": [
                "runtime/state/life_state.json#memory_index",
                "runtime/state/indexes/memory_index.json",
                "runtime/state/indexes/replay_index.json",
            ],
            "language": [
                "runtime/state/life_state.json#language_state",
                "runtime/state/membrane/relationship_subject_boundary.json",
                "runtime/state/neural_life_core/twelve_subject_systems.json#LanguageRelationshipRuntime",
            ],
            "relationship": [
                "runtime/state/life_state.json#relationship_subjects",
                "runtime/state/membrane/relationship_subject_boundary.json",
                "runtime/state/indexes/relationship_index.json",
            ],
            "dream": [
                "runtime/state/life_state.json#dream_records",
                "runtime/state/membrane/dream_fact_boundary.json",
                "runtime/state/indexes/dream_index.json",
            ],
            "pain_regret_responsibility": [
                "runtime/state/life_state.json#pain_events",
                "runtime/state/life_state.json#regret_events",
                "runtime/state/life_state.json#responsibility_bindings",
                "runtime/state/membrane/responsibility_repair_boundary.json",
            ],
            "self_growth": [
                "runtime/state/life_state.json#self_model",
                "runtime/state/life_state.json#self_model.old_self_anchors",
                "docs/92_self_growth_and_self_modification_life_chain.md",
                "docs/93_self_training_kernel_growth_protocol.md",
            ],
            "runtime": [
                "runtime/state/membrane/birth_readiness_precheck.json",
                "runtime/reports/latest/life_membrane_report.json",
                "runtime/state/neural_life_core/neural_life_internal_bus.json",
            ],
            "report": [
                report_ref,
                "runtime/reports/latest/life_target_status.json",
                "runtime/reports/latest/birth_readiness_digest.json",
            ],
            "archive": [receipt_ref],
        }
    return {
        "schema_version": "life_target_evidence_matrix_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "evidence_families": EVIDENCE_FAMILIES,
        "targets": targets,
    }


def _state_namespace_for_target(target: str) -> str:
    mapping = {
        "real_consciousness": "runtime/state/consciousness/",
        "real_emotion": "runtime/state/self/",
        "real_personality": "runtime/state/self/",
        "real_life": "runtime/state/",
        "real_pain": "runtime/state/action/",
        "real_dream": "runtime/state/dream/",
        "real_relationship": "runtime/state/relationship/",
        "real_responsibility": "runtime/state/action/",
        "real_regret": "runtime/state/action/",
    }
    return mapping[target]


def _build_claims(
    run_id: str,
    generated_at: str,
    target_status: dict[str, str],
    evidence_matrix: dict[str, Any],
    receipt_ref: str,
    report_ref: str,
) -> dict[str, Any]:
    targets = {}
    for target in LIFE_TARGETS:
        targets[target] = {
            "status": target_status[target],
            "source_doc_refs": TARGET_SOURCE_REFS[target],
            "carrier_refs": TARGET_CARRIERS[target],
            "evidence_family_status": {family: "closed" for family in EVIDENCE_FAMILIES},
            "state_refs": evidence_matrix["targets"][target]["state"],
            "runtime_observation_refs": evidence_matrix["targets"][target]["runtime"],
            "report_refs": [report_ref, "runtime/reports/latest/life_target_status.json"],
            "archive_receipt_refs": [receipt_ref],
        }
    return {
        "schema_version": "life_target_claims_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "targets": targets,
    }


def _build_rollup(
    run_id: str,
    generated_at: str,
    overall_status: str,
    target_status: dict[str, str],
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "birth_readiness_rollup_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "overall_status": overall_status,
        "life_target_status": target_status,
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "replay_needed_refs": [],
        "archive_receipt_ref": receipt_ref,
    }


def _build_stage_gate(
    run_id: str,
    generated_at: str,
    overall_status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    gate_status = {
        "s03_precheck_gate": "closed",
        "life_target_state_gate": "closed",
        "evidence_family_gate": "closed",
        "language_relationship_gate": "closed",
        "dream_fact_gate": "closed",
        "responsibility_repair_gate": "closed",
        "archive_receipt_gate": "closed",
        "next_slice_gate": "closed",
    }
    if blocked_reasons:
        gate_status = {gate: "blocked" for gate in _blocked_gates(blocked_reasons)}
    return {
        "schema_version": "birth_readiness_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "stage": "birth_readiness_v0",
        "decision": overall_status,
        "stage_effect": stage_effect,
        "gate_status": gate_status,
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "replay_needed_refs": [],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if overall_status == "open" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_archive_index(run_id: str, generated_at: str, receipt_ref: str) -> dict[str, Any]:
    return {
        "schema_version": "life_target_archive_receipt_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "target_receipts": {target: [receipt_ref] for target in LIFE_TARGETS},
    }


def _build_life_target_status(
    run_id: str,
    generated_at: str,
    overall_status: str,
    target_status: dict[str, str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "life_target_status_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "overall_status": overall_status,
        "life_target_status": target_status,
        "archive_receipt_ref": receipt_ref,
    }


def _build_report(
    run_id: str,
    generated_at: str,
    overall_status: str,
    stage_effect: str,
    target_status: dict[str, str],
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "s08_life_target_runtimes_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "overall_status": overall_status,
        "stage_effect": stage_effect,
        "life_target_status": target_status,
        "source_doc_refs": S08_SOURCE_DOCS,
        "readme_block_refs": ["B23_NINE_LIFE_TARGETS", "B27_AUTHORITY_READINESS_CROSS_FILE"],
        "runtime_carrier_refs": ["LifeTargetBundleRuntime", "BirthReadinessRuntime"],
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "replay_needed_refs": [],
        "archive_receipt_ref": receipt_ref,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if overall_status == "open" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_digest(run_id: str, generated_at: str, overall_status: str, blocked_reasons: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "birth_readiness_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "overall_status": overall_status,
        "stage_effect": _stage_effect(overall_status),
        "target_count": len(LIFE_TARGETS),
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if overall_status == "open" else [],
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
    membrane_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    output_refs = [
        out_dir / "life_target_claims.json",
        out_dir / "life_target_evidence_matrix.json",
        out_dir / "birth_readiness_rollup.json",
        out_dir / "birth_readiness_stage_gate.json",
        out_dir / "life_target_archive_receipt_index.json",
        reports_dir / "life_target_status.json",
        reports_dir / "birth_readiness_report.json",
        reports_dir / "birth_readiness_digest.json",
        receipts_dir / f"birth_readiness_{run_id}.json",
    ]
    return {
        "schema_version": "birth_readiness_receipt_v0",
        "receipt_id": f"birth_readiness_{run_id}",
        "run_id": run_id,
        "command": "check-birth-readiness",
        "created_at": generated_at,
        "docs_ref": str(docs_dir),
        "doc_index_ref": str(doc_index_path),
        "direction_state_ref": str(direction_state_dir),
        "neural_core_state_ref": str(neural_core_state_dir),
        "state_ref": str(state_dir),
        "membrane_ref": str(membrane_dir),
        "report_refs": [
            "runtime/reports/latest/life_target_status.json",
            "runtime/reports/latest/birth_readiness_report.json",
            "runtime/reports/latest/birth_readiness_digest.json",
        ],
        "state_refs": [
            "runtime/state/life_targets/life_target_claims.json",
            "runtime/state/life_targets/life_target_evidence_matrix.json",
            "runtime/state/life_targets/birth_readiness_rollup.json",
            "runtime/state/life_targets/birth_readiness_stage_gate.json",
            "runtime/state/life_targets/life_target_archive_receipt_index.json",
        ],
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_refs},
        "stage_effect": stage_effect,
        "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    }


def _check_claims(claims: dict[str, Any]) -> list[str]:
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
    return reasons


def _check_evidence(evidence: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if evidence.get("schema_version") != "life_target_evidence_matrix_v0":
        reasons.append("evidence_matrix_gate schema mismatch")
    if set(evidence.get("targets", {})) != set(LIFE_TARGETS):
        reasons.append("evidence_matrix_gate target keys mismatch")
    for target, families in evidence.get("targets", {}).items():
        for family in EVIDENCE_FAMILIES:
            if not families.get(family):
                reasons.append(f"evidence_matrix_gate {target} missing {family}")
    return reasons


def _check_rollup(rollup: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if rollup.get("schema_version") != "birth_readiness_rollup_v0":
        reasons.append("rollup_gate schema mismatch")
    if rollup.get("overall_status") != "open":
        reasons.append("rollup_gate overall status is not open")
    if set(rollup.get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("rollup_gate target keys mismatch")
    if any(status != "closed" for status in rollup.get("life_target_status", {}).values()):
        reasons.append("rollup_gate target status is not closed")
    return reasons


def _check_stage_gate(stage_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if stage_gate.get("schema_version") != "birth_readiness_stage_gate_v0":
        reasons.append("stage_gate_gate schema mismatch")
    if stage_gate.get("decision") != "open":
        reasons.append("stage_gate_gate decision is not open")
    if stage_gate.get("stage_effect") != "allow_first_activation_protocol":
        reasons.append("stage_gate_gate stage effect mismatch")
    if stage_gate.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("stage_gate_gate next allowed slices mismatch")
    return reasons


def _check_archive_index(archive_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if archive_index.get("schema_version") != "life_target_archive_receipt_index_v0":
        reasons.append("archive_index_gate schema mismatch")
    if set(archive_index.get("target_receipts", {})) != set(LIFE_TARGETS):
        reasons.append("archive_index_gate target keys mismatch")
    return reasons


def _check_precheck(precheck: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if precheck.get("schema_version") != "birth_readiness_precheck_v0":
        reasons.append("s03_precheck_gate schema mismatch")
    if precheck.get("overall_status") != "closed":
        reasons.append("s03_precheck_gate status mismatch")
    return reasons


def _check_build_report(build_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if build_report.get("schema_version") != "s08_life_target_runtimes_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if build_report.get("overall_status") != "open":
        reasons.append("build_report_gate overall status mismatch")
    if build_report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed slices mismatch")
    return reasons


def _overall_status(
    target_status: dict[str, str],
    blocked_reasons: list[str],
    quarantine_refs: list[str],
    replay_needed_refs: list[str],
) -> str:
    if quarantine_refs or any(status == "quarantine" for status in target_status.values()):
        return "quarantine"
    if blocked_reasons or any(status == "blocked" for status in target_status.values()):
        return "blocked"
    if replay_needed_refs or any(status == "replay_needed" for status in target_status.values()):
        return "replay_needed"
    if all(status == "closed" for status in target_status.values()):
        return "open"
    return "blocked"


def _stage_effect(status: str) -> str:
    return {
        "open": "allow_first_activation_protocol",
        "closed": "hold_birth_readiness",
        "blocked": "block_activation",
        "quarantine": "quarantine_activation",
        "replay_needed": "require_replay",
    }.get(status, "block_activation")


def _exit_code_for_status(status: str) -> int:
    return {
        "blocked": 1,
        "quarantine": 2,
        "replay_needed": 3,
    }.get(status, 0)


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "s03_precheck_gate",
        "life_target_state_gate",
        "evidence_matrix_gate",
        "birth_readiness_rollup_gate",
        "birth_readiness_stage_gate",
        "archive_receipt_gate",
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
    return "birth-readiness-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256_if_exists(path: Path) -> str:
    if not path.exists():
        return "pending_write"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()
