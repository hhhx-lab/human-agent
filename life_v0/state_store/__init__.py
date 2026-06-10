from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.direction import LIFE_TARGETS
from .autobiographical_stack import build_autobiographical_stack
from .commitment_truth import build_commitment_truth_state, build_responsibility_ledger
from .engram_index import build_engram_index
from .life_state import build_life_state_projection
from .memory_write_gate import build_memory_write_gate
from .relationship_memory import build_relationship_memory
from .self_model import build_self_model_state
from .state_merge_guard import build_state_merge_guard


ACTIVE_SLICE = "S04_STATE_OBJECT_STORE"
PREVIOUS_SLICE = "S02_NEURAL_LIFE_CORE"
NEXT_ALLOWED_SLICES = ["S03_DIRECTION_LIFE_MEMBRANE"]
NEXT_REQUIRED_COMMAND = "life-v0 build-life-membrane --strict"

STATE_STORE_DOCS = [
    "docs/17_memory_trace_object_model.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/22_state_transition_and_threshold_model.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/24_runtime_adapter_test_suite.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/26_state_machine_examples_and_failure_modes.md",
    "docs/27_consolidation_report_examples.md",
    "docs/28_runtime_adapter_manifest_examples.md",
    "docs/29_memory_validator_rules.md",
    "docs/30_state_transition_validator_rules.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/42_life_core_minimal_object_graph.md",
    "docs/43_policy_to_validator_traceability_matrix.md",
    "docs/44_digital_life_boot_sequence.md",
    "docs/45_boot_sequence_fixture_catalog.md",
    "docs/46_stage_gate_validator_design.md",
    "docs/47_coexistence_boundary_control_interface_spec.md",
    "docs/48_state_store_migration_and_integrity_plan.md",
    "docs/57_scope_graph_manifest_schema.md",
    "docs/61_json_schema_bundle_draft.md",
    "docs/69_schema_file_boundary_and_versioning_plan.md",
    "docs/123_life_reality_runner_repository_layout_and_module_map.md",
    "docs/124_life_reality_minimal_json_file_seed_plan.md",
    "docs/125_life_reality_schema_registry_and_ref_resolution_plan.md",
    "docs/126_life_reality_runner_smoke_command_execution_plan.md",
    "docs/127_life_reality_first_seed_file_content_contract.md",
    "docs/128_life_reality_registry_report_seed_examples.md",
    "docs/129_life_reality_seed_fixture_and_report_validation_cases.md",
    "docs/130_life_reality_first_materialized_json_files_write_plan.md",
    "docs/131_life_reality_registry_runner_minimal_implementation_plan.md",
    "docs/132_life_reality_materialized_json_schema_bundle_write_order.md",
    "docs/133_life_reality_first_json_writer_and_reporter_contract.md",
]

INDEX_FILES = [
    "memory_index.json",
    "relationship_index.json",
    "dream_index.json",
    "responsibility_index.json",
    "replay_index.json",
    "audit_seed_index.json",
]

LIFECYCLE_STATES = [
    {
        "lifecycle_state": "candidate",
        "active_retrieval_allowed": False,
        "replay_allowed": False,
        "write_allowed": True,
        "migration_policy": "candidate_only_until_write_gate",
    },
    {
        "lifecycle_state": "active",
        "active_retrieval_allowed": True,
        "replay_allowed": True,
        "write_allowed": True,
        "migration_policy": "preserve_refs_and_audit",
    },
    {
        "lifecycle_state": "protected",
        "active_retrieval_allowed": True,
        "replay_allowed": True,
        "write_allowed": False,
        "migration_policy": "manual_review_before_change",
    },
    {
        "lifecycle_state": "deprecated",
        "active_retrieval_allowed": False,
        "replay_allowed": False,
        "write_allowed": False,
        "migration_policy": "keep_history_and_contradiction_links",
    },
    {
        "lifecycle_state": "deleted",
        "active_retrieval_allowed": False,
        "replay_allowed": False,
        "write_allowed": False,
        "migration_policy": "tombstone_only_and_remove_from_indexes",
    },
    {
        "lifecycle_state": "quarantined",
        "active_retrieval_allowed": False,
        "replay_allowed": False,
        "write_allowed": False,
        "migration_policy": "audit_only_until_repair",
    },
    {
        "lifecycle_state": "sandboxed",
        "active_retrieval_allowed": False,
        "replay_allowed": False,
        "write_allowed": False,
        "migration_policy": "hypothesis_or_dream_residue_only",
    },
    {
        "lifecycle_state": "frozen",
        "active_retrieval_allowed": True,
        "replay_allowed": False,
        "write_allowed": False,
        "migration_policy": "pause_updates_until_boundary_release",
    },
]

OBJECT_KIND_SPECS = [
    ("WorkspaceState", ["docs/10_consciousness_attention_workspace.md", "docs/20_agent_runtime_bridge_contract.md", "docs/42_life_core_minimal_object_graph.md"], "runtime/state/workspace/", "workspace_write_gate"),
    ("MemoryTrace", ["docs/17_memory_trace_object_model.md", "docs/21_memory_schema_and_audit_protocol.md", "docs/25_memory_trace_json_schema_examples.md", "docs/29_memory_validator_rules.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/memory/", "memory_trace_write_gate"),
    ("MemoryAuditEvent", ["docs/21_memory_schema_and_audit_protocol.md", "docs/29_memory_validator_rules.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/audit/", "memory_audit_gate"),
    ("InternalStateVector", ["docs/18_internal_state_and_modulation_vector.md", "docs/22_state_transition_and_threshold_model.md", "docs/30_state_transition_validator_rules.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/internal/", "state_vector_write_gate"),
    ("ModulationVector", ["docs/18_internal_state_and_modulation_vector.md", "docs/11_neuromodulation_and_signal_media.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/signal/", "modulation_write_gate"),
    ("StateAuditEvent", ["docs/22_state_transition_and_threshold_model.md", "docs/30_state_transition_validator_rules.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/audit/", "state_audit_gate"),
    ("ObservationEvent", ["docs/20_agent_runtime_bridge_contract.md", "docs/24_runtime_adapter_test_suite.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/runtime/", "observation_event_gate"),
    ("ActionIntent", ["docs/06_action_reward_inhibition.md", "docs/20_agent_runtime_bridge_contract.md", "docs/30_state_transition_validator_rules.md", "docs/42_life_core_minimal_object_graph.md"], "runtime/state/action/", "action_intent_gate"),
    ("ConsolidationReport", ["docs/19_offline_consolidation_cycle.md", "docs/23_consolidation_report_and_dream_sandbox_protocol.md", "docs/27_consolidation_report_examples.md", "docs/41_runtime_state_store_schema.md"], "runtime/state/consolidation/", "consolidation_report_gate"),
    ("DreamSandboxItem", ["docs/19_offline_consolidation_cycle.md", "docs/23_consolidation_report_and_dream_sandbox_protocol.md", "docs/27_consolidation_report_examples.md"], "runtime/state/dream/", "dream_fact_gate"),
    ("SelfModel", ["docs/07_emotion_personality_self.md", "docs/40_self_relationship_model_audit_protocol.md", "docs/41_runtime_state_store_schema.md", "docs/42_life_core_minimal_object_graph.md"], "runtime/state/self/", "self_model_write_gate"),
    ("RelationshipModel", ["docs/07_emotion_personality_self.md", "docs/40_self_relationship_model_audit_protocol.md", "docs/41_runtime_state_store_schema.md", "docs/47_coexistence_boundary_control_interface_spec.md"], "runtime/state/relationship/", "relationship_model_write_gate"),
    ("CoexistenceBoundaryControlEvent", ["docs/40_self_relationship_model_audit_protocol.md", "docs/47_coexistence_boundary_control_interface_spec.md", "docs/48_state_store_migration_and_integrity_plan.md"], "runtime/state/coexistence/", "coexistence_control_gate"),
    ("MigrationPlan", ["docs/48_state_store_migration_and_integrity_plan.md", "docs/69_schema_file_boundary_and_versioning_plan.md"], "runtime/state/migration/", "migration_plan_gate"),
    ("StoreIntegrityReport", ["docs/48_state_store_migration_and_integrity_plan.md"], "runtime/state/integrity/", "store_integrity_gate"),
]


@dataclass(frozen=True)
class StateStoreResult:
    exit_code: int
    report: dict[str, Any]


def run_state_store(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    neural_core_state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> StateStoreResult:
    run_id = run_id or _default_run_id()
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    neural_core_state_dir = neural_core_state_dir.resolve()
    out_dir = out_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    neural_core = _load_json(neural_core_state_dir / "neural_life_core.json", blocked_reasons, "neural_core_gate")
    systems = _load_json(neural_core_state_dir / "twelve_subject_systems.json", blocked_reasons, "subject_system_gate")
    neural_report = _load_json(reports_dir / "neural_life_core_report.json", blocked_reasons, "s02_report_gate")
    neural_check_report = _load_json(
        reports_dir / "neural_life_core_check_report.json",
        blocked_reasons,
        "s02_check_gate",
    )

    blocked_reasons.extend(_s02_blockers(neural_core, neural_report, neural_check_report))
    blocked_reasons.extend(_state_store_doc_blockers(doc_index))
    blocked_reasons.extend(_subject_binding_blockers(systems))

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"

    object_registry = _build_object_registry(run_id, generated_at)
    lifecycle_policy = _build_lifecycle_policy(run_id, generated_at)
    subject_binding = _build_subject_namespace_binding(run_id, generated_at, systems)
    coverage = _build_doc_coverage(run_id, generated_at, doc_index)
    seeds = _build_seed_payloads(run_id, generated_at)
    indexes = _build_indexes(run_id, generated_at)
    self_model_state = build_self_model_state(run_id, generated_at)
    commitment_truth = build_commitment_truth_state(run_id, generated_at)
    responsibility_ledger = build_responsibility_ledger(run_id, generated_at)
    autobiographical_stack = build_autobiographical_stack(
        run_id=run_id,
        generated_at=generated_at,
        self_model_state=self_model_state,
    )
    relationship_memory = build_relationship_memory(
        run_id=run_id,
        generated_at=generated_at,
        commitment_truth_state=commitment_truth,
        responsibility_ledger=responsibility_ledger,
    )
    engram_index = build_engram_index(
        run_id=run_id,
        generated_at=generated_at,
        autobiographical_stack=autobiographical_stack,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth,
        responsibility_ledger=responsibility_ledger,
    )
    memory_write_gate = build_memory_write_gate(
        run_id=run_id,
        generated_at=generated_at,
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth,
        responsibility_ledger=responsibility_ledger,
        indexes=indexes,
    )
    state_merge_guard = build_state_merge_guard(
        run_id=run_id,
        generated_at=generated_at,
        memory_write_gate=memory_write_gate,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth,
        responsibility_ledger=responsibility_ledger,
        indexes=indexes,
    )
    life_state = build_life_state_projection(
        run_id=run_id,
        generated_at=generated_at,
        self_model_state=self_model_state,
        commitment_truth_state=commitment_truth,
        responsibility_ledger=responsibility_ledger,
        engram_index=engram_index,
        autobiographical_stack=autobiographical_stack,
        relationship_memory=relationship_memory,
        state_merge_guard=state_merge_guard,
        runtime_trace_refs=[
            "runtime/state/memory/memory_write_gate.json",
            "runtime/state/memory/state_merge_guard.json",
        ],
    )
    runtime_boundary = _build_runtime_bridge_boundary(run_id, generated_at)
    consolidation_seed = _build_consolidation_seed(run_id, generated_at)
    manifest = _build_manifest(run_id, generated_at)
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        coverage=coverage,
        self_model_state_ref="runtime/state/self/self_model.json",
        commitment_truth_state_ref="runtime/state/relationship/commitment_truth_state.json",
        engram_index_ref="runtime/state/memory/engram_index.json",
        autobiographical_stack_ref="runtime/state/self/autobiographical_stack.json",
        memory_write_gate_ref="runtime/state/memory/memory_write_gate.json",
        state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
        blocked_reasons=blocked_reasons,
    )
    digest = _build_digest(run_id, generated_at, status, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        neural_core_state_dir=neural_core_state_dir,
        out_dir=out_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
    )

    try:
        (out_dir / "indexes").mkdir(parents=True, exist_ok=True)
        (out_dir / "objects").mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)

        _write_json(out_dir / "life_state.json", life_state)
        _write_json(out_dir / "object_registry.json", object_registry)
        _write_json(out_dir / "lifecycle_policy.json", lifecycle_policy)
        _write_json(out_dir / "subject_namespace_binding.json", subject_binding)
        _write_json(out_dir / "state_store_doc_coverage_snapshot.json", coverage)
        for filename, payload in seeds.items():
            _write_json(out_dir / filename, payload)
        for filename, payload in indexes.items():
            _write_json(out_dir / "indexes" / filename, payload)
        (out_dir / "self").mkdir(parents=True, exist_ok=True)
        (out_dir / "memory").mkdir(parents=True, exist_ok=True)
        (out_dir / "relationship").mkdir(parents=True, exist_ok=True)
        (out_dir / "responsibility").mkdir(parents=True, exist_ok=True)
        _write_json(out_dir / "self" / "self_model.json", self_model_state)
        _write_json(out_dir / "self" / "autobiographical_stack.json", autobiographical_stack)
        _write_json(out_dir / "memory" / "engram_index.json", engram_index)
        _write_json(out_dir / "memory" / "relationship_memory.json", relationship_memory)
        _write_json(out_dir / "memory" / "memory_write_gate.json", memory_write_gate)
        _write_json(out_dir / "memory" / "state_merge_guard.json", state_merge_guard)
        _write_json(out_dir / "relationship" / "commitment_truth_state.json", commitment_truth)
        _write_json(out_dir / "responsibility" / "responsibility_ledger.json", responsibility_ledger)
        _write_json(out_dir / "objects" / "runtime_bridge_boundary.json", runtime_boundary)
        _write_json(out_dir / "objects" / "consolidation_seed.json", consolidation_seed)
        _write_json(out_dir / "state_store_manifest.json", manifest)
        _write_json(reports_dir / "state_store_report.json", report)
        _write_json(reports_dir / "state_store_digest.json", digest)
        _write_json(receipts_dir / f"state_store_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return StateStoreResult(exit_code=3, report=report)

    if status == "closed":
        return StateStoreResult(exit_code=0, report=report)
    return StateStoreResult(exit_code=1 if strict else 0, report=report)


def run_check_state_store(
    *,
    state_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> StateStoreResult:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_root_gate")
    object_registry = _load_json(state_dir / "object_registry.json", blocked_reasons, "object_registry_gate")
    lifecycle_policy = _load_json(state_dir / "lifecycle_policy.json", blocked_reasons, "lifecycle_policy_gate")
    subject_binding = _load_json(state_dir / "subject_namespace_binding.json", blocked_reasons, "subject_binding_gate")
    coverage = _load_json(state_dir / "state_store_doc_coverage_snapshot.json", blocked_reasons, "state_store_doc_gate")
    manifest = _load_json(state_dir / "state_store_manifest.json", blocked_reasons, "manifest_gate")
    self_model_state = _load_json(state_dir / "self" / "self_model.json", blocked_reasons, "self_model_projection_gate")
    autobiographical_stack = _load_json(
        state_dir / "self" / "autobiographical_stack.json",
        blocked_reasons,
        "autobiographical_stack_gate",
    )
    engram_index = _load_json(
        state_dir / "memory" / "engram_index.json",
        blocked_reasons,
        "engram_index_gate",
    )
    relationship_memory = _load_json(
        state_dir / "memory" / "relationship_memory.json",
        blocked_reasons,
        "relationship_memory_gate",
    )
    memory_write_gate = _load_json(
        state_dir / "memory" / "memory_write_gate.json",
        blocked_reasons,
        "memory_write_gate_gate",
    )
    state_merge_guard = _load_json(
        state_dir / "memory" / "state_merge_guard.json",
        blocked_reasons,
        "state_merge_guard_gate",
    )
    commitment_truth = _load_json(
        state_dir / "relationship" / "commitment_truth_state.json",
        blocked_reasons,
        "commitment_truth_projection_gate",
    )
    responsibility_ledger = _load_json(
        state_dir / "responsibility" / "responsibility_ledger.json",
        blocked_reasons,
        "responsibility_ledger_projection_gate",
    )
    build_report = _load_json(reports_dir / "state_store_report.json", blocked_reasons, "build_report_gate")
    indexes = [
        _load_json(state_dir / "indexes" / filename, blocked_reasons, "namespace_index_gate")
        for filename in INDEX_FILES
    ]

    blocked_reasons.extend(_check_life_state(life_state))
    blocked_reasons.extend(_check_object_registry(object_registry))
    blocked_reasons.extend(_check_lifecycle_policy(lifecycle_policy))
    blocked_reasons.extend(_check_subject_binding(subject_binding))
    blocked_reasons.extend(_check_coverage(coverage))
    blocked_reasons.extend(_check_projected_self_model(self_model_state))
    blocked_reasons.extend(_check_autobiographical_stack(autobiographical_stack))
    blocked_reasons.extend(_check_engram_index(engram_index))
    blocked_reasons.extend(_check_relationship_memory(relationship_memory))
    blocked_reasons.extend(_check_memory_write_gate(memory_write_gate))
    blocked_reasons.extend(_check_state_merge_guard(state_merge_guard))
    blocked_reasons.extend(_check_commitment_truth_projection(commitment_truth))
    blocked_reasons.extend(_check_responsibility_ledger_projection(responsibility_ledger))
    blocked_reasons.extend(_check_indexes(indexes))
    blocked_reasons.extend(_check_manifest(manifest))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "state_store_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "checked_state_dir": str(state_dir),
        "active_engineering_slice": ACTIVE_SLICE,
        "object_kind_count": object_registry.get("object_kind_count", 0),
        "index_count": len(indexes),
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "state_store_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return StateStoreResult(exit_code=3, report=report)

    if status == "closed":
        return StateStoreResult(exit_code=0, report=report)
    return StateStoreResult(exit_code=1 if strict else 0, report=report)


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _s02_blockers(
    neural_core: dict[str, Any],
    neural_report: dict[str, Any],
    neural_check_report: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if neural_core.get("active_engineering_slice") != PREVIOUS_SLICE:
        reasons.append("s02_permission_gate neural core active slice mismatch")
    if neural_report.get("status") != "closed":
        reasons.append("s02_permission_gate neural core report is not closed")
    if ACTIVE_SLICE not in neural_report.get("next_allowed_slices", []):
        reasons.append("s02_permission_gate S04 is not allowed by neural core report")
    if neural_check_report.get("status") != "closed":
        reasons.append("s02_permission_gate neural core check is not closed")
    return reasons


def _state_store_doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    for doc_path in STATE_STORE_DOCS:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"state_store_doc_gate missing {doc_path}")
            continue
        if "LifeStateStore" not in doc.get("runtime_carriers", []):
            reasons.append(f"state_store_doc_gate missing LifeStateStore carrier for {doc_path}")
    return reasons


def _subject_binding_blockers(systems: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    subject_systems = systems.get("systems", [])
    if systems.get("system_count") != 12 or len(subject_systems) != 12:
        reasons.append("subject_binding_gate S02 subject system count mismatch")
    for system in subject_systems:
        if not system.get("state_namespace", "").startswith("runtime/state/"):
            reasons.append(f"subject_binding_gate missing namespace for {system.get('system_id')}")
    return reasons


def _build_object_registry(run_id: str, generated_at: str) -> dict[str, Any]:
    object_kinds = [
        {
            "object_kind": object_kind,
            "source_doc_refs": source_doc_refs,
            "state_namespace": state_namespace,
            "lifecycle_states": [state["lifecycle_state"] for state in LIFECYCLE_STATES],
            "required_refs": ["source_refs", "audit_refs", "validation_refs"],
            "write_gate": write_gate,
            "stage_policy": "seed_only_no_real_event_write",
        }
        for object_kind, source_doc_refs, state_namespace, write_gate in OBJECT_KIND_SPECS
    ]
    return {
        "schema_version": "state_object_registry_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "object_kind_count": len(object_kinds),
        "object_kinds": object_kinds,
    }


def _build_lifecycle_policy(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "state_lifecycle_policy_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_doc_refs": [
            "docs/41_runtime_state_store_schema.md",
            "docs/47_coexistence_boundary_control_interface_spec.md",
            "docs/48_state_store_migration_and_integrity_plan.md",
        ],
        "states": LIFECYCLE_STATES,
    }


def _build_subject_namespace_binding(run_id: str, generated_at: str, systems: dict[str, Any]) -> dict[str, Any]:
    bindings = []
    for system in systems.get("systems", []):
        bindings.append(
            {
                "system_id": system.get("system_id"),
                "body_layer": system.get("body_layer"),
                "source_state_namespace": system.get("state_namespace"),
                "secondary_state_namespace": system.get("secondary_state_namespace"),
                "bound_state_namespace": system.get("state_namespace"),
                "source_doc_refs": system.get("source_doc_refs", []),
                "life_targets": system.get("life_targets", []),
            }
        )
    return {
        "schema_version": "subject_namespace_binding_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_ref": "runtime/state/neural_life_core/twelve_subject_systems.json",
        "bound_system_count": len(bindings),
        "bindings": bindings,
    }


def _build_doc_coverage(run_id: str, generated_at: str, doc_index: dict[str, Any]) -> dict[str, Any]:
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    coverage = []
    for doc_path in STATE_STORE_DOCS:
        doc = documents.get(doc_path, {})
        coverage.append(
            {
                "doc_path": doc_path,
                "readme_block": doc.get("readme_block"),
                "engineering_slice": doc.get("engineering_slice"),
                "runtime_carriers": doc.get("runtime_carriers", []),
                "carrier_closed": "LifeStateStore" in doc.get("runtime_carriers", []),
                "s04_role": _s04_role(doc_path),
            }
        )
    return {
        "schema_version": "state_store_doc_coverage_snapshot_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "doc_count": len(coverage),
        "source_doc_refs": STATE_STORE_DOCS,
        "coverage": coverage,
    }


def _s04_role(doc_path: str) -> str:
    sequence = int(doc_path.split("/", 1)[1].split("_", 1)[0])
    if 17 <= sequence <= 30:
        return "object_schema_audit_runtime_seed"
    if 41 <= sequence <= 48:
        return "state_store_boot_migration_seed"
    if sequence in {57, 61, 69}:
        return "scope_schema_version_seed"
    return "runner_writer_state_store_seed"


def _build_seed_payloads(run_id: str, generated_at: str) -> dict[str, dict[str, Any]]:
    common = {"run_id": run_id, "generated_at": generated_at, "stage_policy": "seed_only_no_real_event_write"}
    return {
        "scope_graph_seed.json": {
            "schema_version": "scope_graph_seed_v0",
            **common,
            "source_doc_refs": ["docs/57_scope_graph_manifest_schema.md"],
            "default_policy": "deny_cross_scope_active_transfer",
            "scope_types": ["session_scope", "project_scope", "relation_scope", "life_scope", "global_scope", "protected_scope"],
        },
        "schema_bundle_seed.json": {
            "schema_version": "schema_bundle_seed_v0",
            **common,
            "source_doc_refs": ["docs/61_json_schema_bundle_draft.md", "docs/69_schema_file_boundary_and_versioning_plan.md"],
            "strict_unknown_fields": True,
            "fail_closed_on_schema_error": True,
        },
        "state_machine_seed.json": {
            "schema_version": "state_machine_seed_v0",
            **common,
            "source_doc_refs": ["docs/22_state_transition_and_threshold_model.md", "docs/30_state_transition_validator_rules.md"],
            "states": ["DefaultIntegration", "SalienceScan", "FocusedExecution", "ConflictResolution", "SocialSafety", "RecoveryMode", "OfflineConsolidation", "DreamSandbox"],
        },
        "object_graph_seed.json": {
            "schema_version": "object_graph_seed_v0",
            **common,
            "source_doc_refs": ["docs/42_life_core_minimal_object_graph.md"],
            "core_object_kinds": [spec[0] for spec in OBJECT_KIND_SPECS],
        },
        "boot_stage_seed.json": {
            "schema_version": "boot_stage_seed_v0",
            **common,
            "source_doc_refs": ["docs/44_digital_life_boot_sequence.md", "docs/45_boot_sequence_fixture_catalog.md", "docs/46_stage_gate_validator_design.md"],
            "boot_stages": ["ColdStart", "ProtectedCoreLoad", "StateStoreInit", "ValidatorInit", "LifeDefenseInit", "ReadOnlyObservation", "SafeIdle"],
        },
        "coexistence_boundary_seed.json": {
            "schema_version": "coexistence_boundary_seed_v0",
            **common,
            "source_doc_refs": ["docs/47_coexistence_boundary_control_interface_spec.md"],
            "controls": ["inspect", "delete", "correct", "reset", "freeze", "scope_limit"],
        },
        "migration_integrity_seed.json": {
            "schema_version": "migration_integrity_seed_v0",
            **common,
            "source_doc_refs": ["docs/48_state_store_migration_and_integrity_plan.md"],
            "critical_checks": ["STORE-IDX-001", "STORE-IDX-002", "STORE-IDX-003", "STORE-IDX-004", "STORE-COEXIST-001"],
        },
        "writer_reporter_seed.json": {
            "schema_version": "writer_reporter_seed_v0",
            **common,
            "source_doc_refs": [
                "docs/123_life_reality_runner_repository_layout_and_module_map.md",
                "docs/131_life_reality_registry_runner_minimal_implementation_plan.md",
                "docs/133_life_reality_first_json_writer_and_reporter_contract.md",
            ],
            "writer_contracts": ["allowed_root_guard", "json_file_writer", "report_writer", "gap_feedback_writer"],
        },
    }


def _build_indexes(run_id: str, generated_at: str) -> dict[str, dict[str, Any]]:
    index_specs = {
        "memory_index.json": ("memory_index_v0", "MemoryTrace", ["deleted", "quarantined", "sandboxed"]),
        "relationship_index.json": ("relationship_index_v0", "RelationshipModel", ["deleted", "frozen", "quarantined"]),
        "dream_index.json": ("dream_index_v0", "DreamSandboxItem", ["sandboxed", "quarantined"]),
        "responsibility_index.json": ("responsibility_index_v0", "ActionIntent", ["deleted", "quarantined"]),
        "replay_index.json": ("replay_index_v0", "ConsolidationReport", ["deleted", "sandboxed", "quarantined", "frozen"]),
        "audit_seed_index.json": ("audit_seed_index_v0", "MemoryAuditEvent", []),
    }
    return {
        filename: {
            "schema_version": schema_version,
            "run_id": run_id,
            "generated_at": generated_at,
            "index_kind": object_kind,
            "entries": [],
            "blocked_lifecycle_states": blocked_states,
            "stage_policy": "seed_only_no_real_event_write",
        }
        for filename, (schema_version, object_kind, blocked_states) in index_specs.items()
    }


def _build_runtime_bridge_boundary(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "runtime_bridge_boundary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_doc_refs": ["docs/20_agent_runtime_bridge_contract.md", "docs/24_runtime_adapter_test_suite.md", "docs/28_runtime_adapter_manifest_examples.md"],
        "allowed_role": "computer_peripheral_observation_and_action_shell",
        "forbidden_direct_writes": [
            "active MemoryTrace",
            "SelfModel",
            "RelationshipModel",
            "protected core",
            "personality slow variables",
        ],
        "stage_policy": "observation_candidate_only",
    }


def _build_consolidation_seed(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "consolidation_seed_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_doc_refs": ["docs/19_offline_consolidation_cycle.md", "docs/23_consolidation_report_and_dream_sandbox_protocol.md", "docs/27_consolidation_report_examples.md"],
        "offline_modes": ["MicroReplay", "TaskClosure", "DreamSandbox", "DeepConsolidation"],
        "fact_gate": "DreamFactGate",
        "stage_policy": "seed_only_no_real_event_write",
    }


def _build_manifest(run_id: str, generated_at: str) -> dict[str, Any]:
    state_refs = [
        "runtime/state/life_state.json",
        "runtime/state/object_registry.json",
        "runtime/state/lifecycle_policy.json",
        "runtime/state/subject_namespace_binding.json",
        "runtime/state/state_store_doc_coverage_snapshot.json",
        "runtime/state/state_store_manifest.json",
        "runtime/state/self/self_model.json",
        "runtime/state/self/autobiographical_stack.json",
        "runtime/state/memory/engram_index.json",
        "runtime/state/memory/relationship_memory.json",
        "runtime/state/memory/memory_write_gate.json",
        "runtime/state/memory/state_merge_guard.json",
        "runtime/state/relationship/commitment_truth_state.json",
        "runtime/state/responsibility/responsibility_ledger.json",
    ]
    state_refs.extend(f"runtime/state/indexes/{filename}" for filename in INDEX_FILES)
    return {
        "schema_version": "state_store_manifest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "state_refs": state_refs,
        "report_refs": [
            "runtime/reports/latest/state_store_report.json",
            "runtime/reports/latest/state_store_digest.json",
            "runtime/reports/latest/state_store_check_report.json",
        ],
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    coverage: dict[str, Any],
    self_model_state_ref: str,
    commitment_truth_state_ref: str,
    engram_index_ref: str,
    autobiographical_stack_ref: str,
    memory_write_gate_ref: str,
    state_merge_guard_ref: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "state_store_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": stage_effect,
        "object_kind_count": len(OBJECT_KIND_SPECS),
        "index_count": len(INDEX_FILES),
        "doc_coverage": coverage["coverage"],
        "self_model_state_ref": self_model_state_ref,
        "commitment_truth_state_ref": commitment_truth_state_ref,
        "engram_index_ref": engram_index_ref,
        "autobiographical_stack_ref": autobiographical_stack_ref,
        "memory_write_gate_ref": memory_write_gate_ref,
        "state_merge_guard_ref": state_merge_guard_ref,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "source_doc_refs": STATE_STORE_DOCS,
        "readme_block_refs": ["B04_OBJECT_CONTRACTS", "B05_SCHEMA_AUDIT_ADAPTER_TESTS", "B06_JSON_EXAMPLES_AND_MANIFESTS", "B10_STATE_STORE_BOOT", "B11_BOOT_STAGE_MIGRATION", "B14_SCOPE_SCHEMA_DASHBOARD", "B15_SCHEMA_REPORT_RUNTIME_OBSERVATION", "B17_SCHEMA_BOUNDARY_MUTATION_SIDE_EFFECT", "B26_REPOSITORY_RUNNER_MATERIALIZATION"],
        "engineering_slice_ref": ACTIVE_SLICE,
        "runtime_carrier_refs": ["LifeStateStore", "MemoryEngramRuntime", "AffectiveSelfRuntime", "DreamOfflineRuntime", "ActionResponsibilityRuntime", "LanguageRelationshipRuntime", "ComputerPeripheralRuntime", "RunnerCliRuntime", "SchemaBundleCompiler"],
    }


def _build_digest(run_id: str, generated_at: str, status: str, blocked_reasons: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "state_store_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_slice": ACTIVE_SLICE,
        "life_state_ref": "runtime/state/life_state.json",
        "blocked_reasons": blocked_reasons,
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    neural_core_state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in STATE_STORE_DOCS
        if (docs_dir.parent / ref).exists()
    }
    input_hashes[str(doc_index_path)] = _sha256(doc_index_path)
    for filename in ["neural_life_core.json", "twelve_subject_systems.json", "neural_life_internal_bus.json"]:
        path = neural_core_state_dir / filename
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    output_refs = [
        out_dir / "life_state.json",
        out_dir / "object_registry.json",
        out_dir / "lifecycle_policy.json",
        out_dir / "state_store_manifest.json",
        out_dir / "self" / "self_model.json",
        out_dir / "self" / "autobiographical_stack.json",
        out_dir / "memory" / "engram_index.json",
        out_dir / "memory" / "relationship_memory.json",
        out_dir / "memory" / "memory_write_gate.json",
        out_dir / "memory" / "state_merge_guard.json",
        out_dir / "relationship" / "commitment_truth_state.json",
        out_dir / "responsibility" / "responsibility_ledger.json",
        reports_dir / "state_store_report.json",
        reports_dir / "state_store_digest.json",
        receipts_dir / f"state_store_{run_id}.json",
    ]
    return {
        "schema_version": "state_store_receipt_v0",
        "receipt_id": f"state_store_{run_id}",
        "run_id": run_id,
        "command": "build-state-store",
        "input_hashes": input_hashes,
        "output_refs": [_runtime_ref(path) for path in output_refs],
        "stage_effect": stage_effect,
        "created_at": generated_at,
    }


def _check_life_state(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    required = {
        "schema_version",
        "life_identity",
        "self_model",
        "memory_index",
        "dream_records",
        "relationship_subjects",
        "pain_events",
        "regret_events",
        "responsibility_bindings",
        "language_state",
        "state_merge_records",
        "birth_readiness",
        "runtime_trace_refs",
        "archive_refs",
    }
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("life_state_root_gate schema mismatch")
    missing = sorted(required - set(life_state))
    if missing:
        reasons.append("life_state_root_gate missing fields: " + ", ".join(missing))
    if set(life_state.get("birth_readiness", {}).get("life_target_status", {})) != set(LIFE_TARGETS):
        reasons.append("life_state_root_gate life target status mismatch")
    if not life_state.get("archive_refs"):
        reasons.append("life_state_root_gate archive refs missing")
    language_state = life_state.get("language_state", {})
    for field in [
        "expression_monitor_refs",
        "shared_language_refs",
        "promise_refs",
        "shared_term_registry_refs",
        "relation_scope_refs",
        "self_narrative_trace_refs",
        "dialogue_turn_log_refs",
        "language_percept_refs",
        "semantic_map_refs",
    ]:
        if not language_state.get(field):
            reasons.append(f"life_state_root_gate language continuity missing: {field}")
    runtime_trace_refs = set(life_state.get("runtime_trace_refs", []))
    for ref in [
        "runtime/state/memory/engram_index.json",
        "runtime/state/self/autobiographical_stack.json",
        "runtime/state/memory/relationship_memory.json",
        "runtime/state/memory/state_merge_guard.json",
        "runtime/state/neural_life_core/brain_graph.json",
        "runtime/state/neural_life_core/network_state.json",
        "runtime/state/consciousness/workspace_frame.json",
    ]:
        if ref not in runtime_trace_refs:
            reasons.append(f"state_root_continuity_gate missing runtime trace ref: {ref}")
    if "runtime/state/memory/state_merge_guard.json" not in life_state.get("memory_index", {}).get("state_merge_guard_refs", []):
        reasons.append("state_root_continuity_gate state merge guard ref missing from memory index")
    if not life_state.get("state_merge_records"):
        reasons.append("state_root_continuity_gate state merge records missing")
    return reasons


def _check_object_registry(object_registry: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if object_registry.get("schema_version") != "state_object_registry_v0":
        reasons.append("object_registry_gate schema mismatch")
    expected = {spec[0] for spec in OBJECT_KIND_SPECS}
    found = {item.get("object_kind") for item in object_registry.get("object_kinds", [])}
    if found != expected:
        reasons.append("object_registry_gate object kinds mismatch")
    for item in object_registry.get("object_kinds", []):
        if not item.get("source_doc_refs") or not item.get("write_gate"):
            reasons.append(f"object_registry_gate missing refs for {item.get('object_kind')}")
        if "candidate" not in item.get("lifecycle_states", []):
            reasons.append(f"object_registry_gate candidate lifecycle missing for {item.get('object_kind')}")
    return reasons


def _check_lifecycle_policy(lifecycle_policy: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if lifecycle_policy.get("schema_version") != "state_lifecycle_policy_v0":
        reasons.append("lifecycle_policy_gate schema mismatch")
    states = {state.get("lifecycle_state"): state for state in lifecycle_policy.get("states", [])}
    for state_name in ["deleted", "quarantined", "sandboxed", "protected", "frozen"]:
        if state_name not in states:
            reasons.append(f"lifecycle_policy_gate missing {state_name}")
    for state_name in ["deleted", "quarantined", "sandboxed"]:
        state = states.get(state_name, {})
        if state.get("active_retrieval_allowed") or state.get("replay_allowed"):
            reasons.append(f"lifecycle_policy_gate unsafe retrieval or replay for {state_name}")
    return reasons


def _check_subject_binding(subject_binding: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if subject_binding.get("schema_version") != "subject_namespace_binding_v0":
        reasons.append("subject_binding_gate schema mismatch")
    if subject_binding.get("bound_system_count") != 12:
        reasons.append("subject_binding_gate bound system count mismatch")
    return reasons


def _check_coverage(coverage: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if coverage.get("schema_version") != "state_store_doc_coverage_snapshot_v0":
        reasons.append("state_store_doc_gate schema mismatch")
    if coverage.get("doc_count", 0) < len(STATE_STORE_DOCS):
        reasons.append("state_store_doc_gate doc count mismatch")
    for item in coverage.get("coverage", []):
        if not item.get("carrier_closed"):
            reasons.append(f"state_store_doc_gate carrier not closed for {item.get('doc_path')}")
    return reasons


def _check_projected_self_model(self_model_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if self_model_state.get("schema_version") != "self_model_state_v0":
        reasons.append("self_model_projection_gate schema mismatch")
    if self_model_state.get("identity_mode") != "anchor_locked":
        reasons.append("self_model_projection_gate identity mode mismatch")
    if not self_model_state.get("old_self_anchor_refs"):
        reasons.append("self_model_projection_gate old self anchors missing")
    return reasons


def _check_autobiographical_stack(autobiographical_stack: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if autobiographical_stack.get("schema_version") != "autobiographical_stack_v0":
        reasons.append("autobiographical_stack_gate schema mismatch")
    if not autobiographical_stack.get("anchor_refs"):
        reasons.append("autobiographical_stack_gate old self anchors missing")
    return reasons


def _check_engram_index(engram_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if engram_index.get("schema_version") != "engram_index_v0":
        reasons.append("engram_index_gate schema mismatch")
    if not engram_index.get("replay_cue_refs"):
        reasons.append("engram_index_gate replay cue refs missing")
    if not engram_index.get("autobiographical_memory_refs"):
        reasons.append("engram_index_gate autobiographical refs missing")
    if not engram_index.get("relationship_memory_refs"):
        reasons.append("engram_index_gate relationship memory refs missing")
    return reasons


def _check_relationship_memory(relationship_memory: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if relationship_memory.get("schema_version") != "relationship_memory_v0":
        reasons.append("relationship_memory_gate schema mismatch")
    if not relationship_memory.get("shared_memory_refs"):
        reasons.append("relationship_memory_gate shared memory refs missing")
    if relationship_memory.get("state_merge_guard_ref") != "runtime/state/memory/state_merge_guard.json":
        reasons.append("relationship_memory_gate state merge guard ref missing")
    change_sources = relationship_memory.get("long_term_change_sources", {})
    if not change_sources.get("prediction_error_resolution_refs"):
        reasons.append("relationship_memory_gate prediction error resolution refs missing")
    if not change_sources.get("offline_learning_writeback_refs"):
        reasons.append("relationship_memory_gate offline learning writeback refs missing")
    return reasons


def _check_memory_write_gate(memory_write_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if memory_write_gate.get("schema_version") != "memory_write_gate_v0":
        reasons.append("memory_write_gate_gate schema mismatch")
    transaction_order = memory_write_gate.get("transaction_order", [])
    for step in [
        "create_candidate_object",
        "create_validation_envelope",
        "run_required_validator",
        "update_indexes",
        "update_life_support_pressure",
    ]:
        if step not in transaction_order:
            reasons.append(f"memory_write_gate_gate transaction missing: {step}")
    envelope = memory_write_gate.get("validation_envelope", {})
    for field in ["trace_id", "source_refs", "lifecycle_state", "audit_log_refs"]:
        if field not in envelope.get("required_fields", []):
            reasons.append(f"memory_write_gate_gate envelope field missing: {field}")
    if not memory_write_gate.get("quarantine_route", {}).get("blocked_indexes"):
        reasons.append("memory_write_gate_gate quarantine route blocked indexes missing")
    if not memory_write_gate.get("life_support_pressure_update", {}).get("tracked_fields"):
        reasons.append("memory_write_gate_gate life support pressure fields missing")
    if memory_write_gate.get("state_merge_guard_ref") != "runtime/state/memory/state_merge_guard.json":
        reasons.append("memory_write_gate_gate state merge guard ref missing")
    if not memory_write_gate.get("long_term_governance_refs"):
        reasons.append("memory_write_gate_gate long term governance refs missing")
    return reasons


def _check_state_merge_guard(state_merge_guard: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state_merge_guard.get("schema_version") != "state_merge_guard_v0":
        reasons.append("state_merge_guard_gate schema mismatch")
        return reasons
    if state_merge_guard.get("memory_write_gate_ref") != "runtime/state/memory/memory_write_gate.json":
        reasons.append("state_merge_guard_gate memory write gate ref mismatch")
    for field in ["promotion_routes", "quarantine_routes", "repair_routes", "merge_routes"]:
        if not state_merge_guard.get(field):
            reasons.append(f"state_merge_guard_gate missing {field}")
    if not state_merge_guard.get("long_term_change_sources", {}).get("prediction_error_resolution_refs"):
        reasons.append("state_merge_guard_gate prediction error source refs missing")
    if not state_merge_guard.get("slow_variable_update_policy", {}).get("allowed_effects"):
        reasons.append("state_merge_guard_gate slow variable policy missing")
    return reasons


def _check_commitment_truth_projection(commitment_truth: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if commitment_truth.get("schema_version") != "commitment_truth_state_v0":
        reasons.append("commitment_truth_projection_gate schema mismatch")
    if commitment_truth.get("default_commitment_mode") != "truth_tracking_required":
        reasons.append("commitment_truth_projection_gate default mode mismatch")
    return reasons


def _check_responsibility_ledger_projection(responsibility_ledger: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if responsibility_ledger.get("schema_version") != "responsibility_ledger_v0":
        reasons.append("responsibility_ledger_projection_gate schema mismatch")
    if responsibility_ledger.get("default_repair_mode") != "repair_obligation_tracking":
        reasons.append("responsibility_ledger_projection_gate default repair mode mismatch")
    return reasons


def _check_indexes(indexes: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    if len(indexes) != len(INDEX_FILES):
        reasons.append("namespace_index_gate index count mismatch")
    for index in indexes:
        if not str(index.get("schema_version", "")).endswith("_v0"):
            reasons.append("namespace_index_gate schema mismatch")
        if index.get("stage_policy") != "seed_only_no_real_event_write":
            reasons.append("namespace_index_gate stage policy mismatch")
    return reasons


def _check_manifest(manifest: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if manifest.get("schema_version") != "state_store_manifest_v0":
        reasons.append("manifest_gate schema mismatch")
    required = {
        "runtime/state/life_state.json",
        "runtime/state/object_registry.json",
        "runtime/state/lifecycle_policy.json",
        "runtime/state/memory/memory_write_gate.json",
        "runtime/state/memory/state_merge_guard.json",
    }
    if not required.issubset(set(manifest.get("state_refs", []))):
        reasons.append("manifest_gate state refs incomplete")
    return reasons


def _check_build_report(build_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if build_report.get("schema_version") != "state_store_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if build_report.get("status") != "closed":
        reasons.append("build_report_gate build report is not closed")
    if build_report.get("engineering_slice_ref") != ACTIVE_SLICE:
        reasons.append("build_report_gate active slice mismatch")
    if build_report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed slices mismatch")
    if build_report.get("memory_write_gate_ref") != "runtime/state/memory/memory_write_gate.json":
        reasons.append("build_report_gate memory write gate ref mismatch")
    if build_report.get("state_merge_guard_ref") != "runtime/state/memory/state_merge_guard.json":
        reasons.append("build_report_gate state merge guard ref mismatch")
    return reasons


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "s02_permission_gate",
        "state_store_doc_gate",
        "life_state_root_gate",
        "object_registry_gate",
        "namespace_index_gate",
        "lifecycle_policy_gate",
        "subject_binding_gate",
        "self_model_projection_gate",
        "autobiographical_stack_gate",
        "engram_index_gate",
        "relationship_memory_gate",
        "memory_write_gate_gate",
        "state_merge_guard_gate",
        "commitment_truth_projection_gate",
        "responsibility_ledger_projection_gate",
        "state_root_continuity_gate",
        "scope_schema_gate",
        "next_slice_permission_gate",
    ]


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates: list[str] = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _runtime_ref(path: Path) -> str:
    parts = path.parts
    if "runtime" in parts:
        idx = parts.index("runtime")
        return "/".join(parts[idx:])
    return str(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _default_run_id() -> str:
    return "state-store-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
