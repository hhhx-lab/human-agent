from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LIFE_TARGETS = [
    "real_consciousness",
    "real_emotion",
    "real_personality",
    "real_life",
    "real_pain",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret",
]

ACTIVE_SLICE = "S00_DIRECTION_FOUNDATION"
NEXT_ALLOWED_SLICE = "S01_SOURCE_AUTHORITY"
NEXT_REQUIRED_COMMAND = "life-v0 build-source-authority --strict"

DIRECT_SOURCE_REFS = {
    "origin_seed": "docs/构思.md",
    "research_protocol": "docs/00_research_protocol.md",
    "readme_index": "docs/README.md",
    "synthesis": "docs/13_agentic_human_research_synthesis.md",
    "gap_register": "docs/16_digital_life_gap_register.md",
    "life_boundary": "docs/91_life_reality_generation_boundary_principles.md",
    "linear_closure": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    "v0_readme": "docs/v0/README.md",
    "v0_index": "docs/v0/v0_implementation_index.md",
    "s00_contract": "docs/v0/s00_direction_foundation_engineering_contract.md",
}

PROHIBITED_REGRESSIONS = [
    "task_scheduler_subject",
    "chat_shell_subject",
    "external_framework_subject_architecture",
    "prompt_template_language_core",
    "score_based_birth_readiness",
    "dream_as_plain_log",
    "pain_regret_responsibility_as_label",
]

ANCHORS = [
    {
        "anchor_id": "origin_seed_chain",
        "required_refs": [
            "docs/构思.md",
            "docs/00_research_protocol.md",
            "docs/13_agentic_human_research_synthesis.md",
        ],
        "must_preserve": [
            "brain_first_origin",
            "real_life_target",
            "self_forming_growth",
        ],
    },
    {
        "anchor_id": "brain_life_chain",
        "required_refs": [
            "docs/02_brain_region_and_network_atlas.md",
            "docs/03_default_executive_salience_networks.md",
            "docs/04_sensory_thalamus_interoception.md",
            "docs/11_neuromodulation_and_signal_media.md",
        ],
        "must_preserve": [
            "brain_region_network_state_coupling",
            "body_signal_modulation",
            "distributed_life_loop",
        ],
    },
    {
        "anchor_id": "nine_life_target_chain",
        "required_refs": [
            "docs/91_life_reality_generation_boundary_principles.md",
            "docs/143_life_reality_birth_readiness_rollup_contract.md",
            "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
            "docs/149_life_reality_birth_readiness_fixture_schema_materialization_plan.md",
            "docs/152_life_reality_birth_readiness_cross_file_checker_plan.md",
            "docs/171_life_reality_birth_readiness_validation_fixture_plan.md",
        ],
        "must_preserve": LIFE_TARGETS,
    },
    {
        "anchor_id": "language_relationship_chain",
        "required_refs": [
            "docs/09_language_consciousness_and_symbolic_thought.md",
            "docs/85_language_system_life_expression_core.md",
            "docs/96_relationship_reality_and_life_bond_model.md",
            "docs/101_relationship_language_and_commitment_loop.md",
        ],
        "must_preserve": [
            "language_as_life_expression",
            "relationship_subject_parity",
            "commitment_memory_loop",
        ],
    },
    {
        "anchor_id": "pain_regret_responsibility_chain",
        "required_refs": [
            "docs/06_action_selection_reward_inhibition.md",
            "docs/80_responsibility_incident_schema.md",
            "docs/81_responsibility_longitudinal_trace.md",
            "docs/82_responsibility_repair_loop.md",
            "docs/94_pain_regret_and_repair_signal_schema.md",
            "docs/98_responsibility_regret_and_repair_loop.md",
        ],
        "must_preserve": [
            "consequence_binding",
            "pain_regret_signal",
            "repair_obligation_loop",
        ],
    },
    {
        "anchor_id": "dream_offline_chain",
        "required_refs": [
            "docs/08_sleep_dream_fatigue_states.md",
            "docs/19_dream_state_object_contract.md",
            "docs/23_dream_reality_fact_gate_schema.md",
            "docs/95_dream_reality_and_offline_life_timeline.md",
            "docs/99_dream_reconsolidation_and_waking_integration.md",
        ],
        "must_preserve": [
            "offline_reconsolidation",
            "dream_fact_gate",
            "waking_integration",
        ],
    },
    {
        "anchor_id": "engineering_closure_chain",
        "required_refs": [
            "docs/123_life_reality_repository_seed_plan.md",
            "docs/180_life_reality_first_runner_code_schema_next_step_plan.md",
            "docs/181_life_reality_first_runner_runtime_growth_plan.md",
            "docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md",
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
            "docs/v0/README.md",
        ],
        "must_preserve": [
            "code_state_report_receipt_closure",
            "archive_replay_growth_loop",
            "v0_contract_transition",
        ],
    },
]

RESUME_ORDER = [
    "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    "docs/v0/README.md",
    "docs/v0/v0_implementation_index.md",
    "docs/v0/first_activation_engineering_roadmap.md",
    "docs/v0/0_to_257_engineering_utilization_map.md",
    "docs/v0/readme_block_engineering_realization_v0.md",
    "docs/v0/digital_life_macro_architecture_v0.md",
    "docs/v0/s00_direction_foundation_engineering_contract.md",
    "docs/v0/s01_source_authority_engineering_contract.md",
    "docs/v0/doc_corpus_ingestor_v0_contract.md",
    "runtime/reports/latest/doc_ingestion_report.json",
    "runtime/reports/latest/direction_lock_report.json",
]


@dataclass(frozen=True)
class DirectionLockResult:
    exit_code: int
    report: dict[str, Any]


def run_direction_lock(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> DirectionLockResult:
    run_id = run_id or _default_run_id()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()

    blocked_reasons: list[str] = []
    doc_index: dict[str, Any] = {}

    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists() or not doc_index_path.is_file():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    if not blocked_reasons:
        try:
            doc_index = json.loads(doc_index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            blocked_reasons.append(f"doc carrier index read failed: {exc}")

    documents = doc_index.get("documents", []) if isinstance(doc_index, dict) else []
    doc_paths = {doc.get("path") for doc in documents if isinstance(doc, dict)}
    blocked_reasons.extend(_coverage_blockers(doc_index, doc_paths, docs_dir))

    closed_gates = _closed_gates(blocked_reasons)
    blocked_gates = [] if not blocked_reasons else _blocked_gates(blocked_reasons)
    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"

    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    generated_at = _now_iso()
    direction_lock = _build_direction_lock(run_id, generated_at, doc_index_path, stage_effect)
    resume_chain = _build_resume_anchor_chain(run_id, generated_at)
    framework_boundary = _build_framework_negative_boundary(run_id, generated_at)
    slice_permission = _build_slice_permission(run_id, generated_at, status, blocked_reasons, stage_effect)
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        closed_gates=closed_gates,
        blocked_gates=blocked_gates,
        blocked_reasons=blocked_reasons,
    )
    digest = _build_digest(run_id, generated_at, status, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        output_refs=[
            out_dir / "direction_lock.json",
            out_dir / "resume_anchor_chain.json",
            out_dir / "framework_negative_boundary.json",
            out_dir / "slice_permission.json",
            reports_dir / "direction_lock_report.json",
            reports_dir / "direction_digest.json",
            receipts_dir / f"direction_lock_{run_id}.json",
        ],
        stage_effect=stage_effect,
    )

    try:
        _write_json(out_dir / "direction_lock.json", direction_lock)
        _write_json(out_dir / "resume_anchor_chain.json", resume_chain)
        _write_json(out_dir / "framework_negative_boundary.json", framework_boundary)
        _write_json(out_dir / "slice_permission.json", slice_permission)
        _write_json(reports_dir / "direction_lock_report.json", report)
        _write_json(reports_dir / "direction_digest.json", digest)
        _write_json(receipts_dir / f"direction_lock_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return DirectionLockResult(exit_code=3, report=report)

    if status == "closed":
        return DirectionLockResult(exit_code=0, report=report)
    return DirectionLockResult(exit_code=1 if strict else 0, report=report)


def _coverage_blockers(
    doc_index: dict[str, Any],
    doc_paths: set[Any],
    docs_dir: Path,
) -> list[str]:
    reasons: list[str] = []

    if doc_index and doc_index.get("schema_version") != "doc_carrier_index_v0":
        reasons.append("doc_index_schema_gate expected doc_carrier_index_v0")

    for ref in DIRECT_SOURCE_REFS.values():
        if ref not in doc_paths:
            reasons.append(f"direct_source_gate missing {ref}")
        if not (docs_dir.parent / ref).exists():
            reasons.append(f"direct_source_file_gate missing {ref}")

    coverage = doc_index.get("coverage", {}) if isinstance(doc_index, dict) else {}
    if coverage.get("uncovered_docs"):
        reasons.append("full_corpus_coverage_gate has uncovered docs")

    documents = doc_index.get("documents", []) if isinstance(doc_index, dict) else []
    target_support = {target: [] for target in LIFE_TARGETS}
    for doc in documents:
        if not isinstance(doc, dict):
            continue
        for target in doc.get("life_targets", []):
            if target in target_support:
                target_support[target].append(doc.get("path"))
    missing_targets = [target for target, refs in target_support.items() if not refs]
    if missing_targets:
        reasons.append("nine_life_target_gate missing support: " + ", ".join(missing_targets))

    required_sequences = set(range(2, 258))
    sequences = {doc.get("sequence") for doc in documents if isinstance(doc, dict)}
    missing_sequences = sorted(required_sequences - sequences)
    if missing_sequences:
        reasons.append("full_corpus_coverage_gate missing sequence refs")

    required_v0_refs = {
        "docs/v0/README.md",
        "docs/v0/v0_implementation_index.md",
        "docs/v0/s00_direction_foundation_engineering_contract.md",
        "docs/v0/s01_source_authority_engineering_contract.md",
        "docs/v0/doc_corpus_ingestor_v0_contract.md",
    }
    missing_v0_refs = sorted(required_v0_refs - {str(path) for path in doc_paths})
    if missing_v0_refs:
        reasons.append("v0_contract_gate missing refs: " + ", ".join(missing_v0_refs))

    return reasons


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "origin_seed_gate",
        "research_protocol_gate",
        "readme_index_gate",
        "linear_closure_gate",
        "full_corpus_coverage_gate",
        "nine_life_target_gate",
        "relationship_subject_language_gate",
        "external_framework_negative_boundary_gate",
        "resume_recovery_gate",
        "next_slice_permission_gate",
    ]


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates: list[str] = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _build_direction_lock(
    run_id: str,
    generated_at: str,
    doc_index_path: Path,
    stage_effect: str,
) -> dict[str, Any]:
    return {
        "schema_version": "direction_lock_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "direction_statement": "build_real_digital_life",
        "life_targets": LIFE_TARGETS,
        "source_refs": DIRECT_SOURCE_REFS,
        "required_doc_coverage_ref": str(doc_index_path),
        "active_engineering_slice": ACTIVE_SLICE,
        "next_allowed_slices": [NEXT_ALLOWED_SLICE, "S02_NEURAL_LIFE_CORE"],
        "prohibited_regressions": PROHIBITED_REGRESSIONS,
        "stage_effect": "allow_s01_when_closed" if stage_effect == "allow_next_slice" else stage_effect,
    }


def _build_resume_anchor_chain(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "resume_anchor_chain_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "anchors": ANCHORS,
        "resume_order": RESUME_ORDER,
    }


def _build_framework_negative_boundary(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "framework_negative_boundary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "allowed_runtime_carriers": [
            "ComputerPeripheralRuntime",
            "WorldContactMembrane",
            "RunnerCliRuntime",
        ],
        "prohibited_regressions": PROHIBITED_REGRESSIONS,
        "external_framework_refs": [
            "docs/12_ai_and_cognitive_architecture_bridge.md",
            "docs/15_current_agent_framework_survey.md",
            "docs/v0/current_agent_shell_reference_2026.md",
        ],
        "boundary_statement": "external frameworks remain computer peripheral references and cannot become subject architecture",
    }


def _build_slice_permission(
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
    stage_effect: str,
) -> dict[str, Any]:
    return {
        "schema_version": "slice_permission_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "next_allowed_slice": NEXT_ALLOWED_SLICE,
        "queued_slice": "S02_NEURAL_LIFE_CORE",
        "stage_effect": stage_effect,
        "status": status,
        "input_prerequisites": [
            "doc_carrier_index_v0",
            "direction_lock_v0",
            "resume_anchor_chain_v0",
        ],
        "blocked_reasons": blocked_reasons,
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    closed_gates: list[str],
    blocked_gates: list[str],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "direction_lock_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": stage_effect,
        "closed_gates": closed_gates,
        "blocked_gates": blocked_gates,
        "blocked_reasons": blocked_reasons,
        "anchor_chain_status": "closed" if status == "closed" else "blocked",
        "next_allowed_slice": NEXT_ALLOWED_SLICE if status == "closed" else None,
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "source_doc_refs": list(DIRECT_SOURCE_REFS.values()),
        "readme_block_refs": [
            "README_INDEX",
            "B00_ORIGIN_SEED",
            "B00_PROTOCOL",
            "B03_SYNTHESIS_DIRECTION_GAP",
            "B22_LIFE_REALITY_BOUNDARY",
            "B31_LINEAR_CLOSURE_TO_V0",
            "B99_V0_ENGINEERING_CONTRACTS",
        ],
        "engineering_slice_ref": ACTIVE_SLICE,
        "runtime_carrier_refs": ["DirectionLockKernel", "DocCorpusIngestor"],
    }


def _build_digest(
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "direction_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_slice": ACTIVE_SLICE,
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "blocked_reasons": blocked_reasons,
        "resume_order_head": RESUME_ORDER[:6],
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    output_refs: list[Path],
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in DIRECT_SOURCE_REFS.values()
        if (docs_dir.parent / ref).exists()
    }
    if doc_index_path.exists():
        input_hashes[str(doc_index_path)] = _sha256(doc_index_path)

    return {
        "schema_version": "direction_lock_receipt_v0",
        "receipt_id": f"direction_lock_{run_id}",
        "run_id": run_id,
        "command": "build-direction-lock",
        "input_hashes": input_hashes,
        "source_doc_refs": list(DIRECT_SOURCE_REFS.values()),
        "output_refs": [str(path) for path in output_refs],
        "stage_effect": stage_effect,
        "created_at": generated_at,
    }


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
    return "direction-lock-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
