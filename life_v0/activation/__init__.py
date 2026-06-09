from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ACTIVE_SLICE = "FIRST_ACTIVATION_PREFLIGHT"
NEXT_REQUIRED_COMMAND = "life-v0 run-replay-shadow --strict"
NEXT_ALLOWED_SLICES = ["S10_RUNTIME_GROWTH_RECONSOLIDATION"]
READ_ME_BLOCK_REFS = ["B29_RUNTIME_MOUNT_GROWTH", "B30_RECONSOLIDATION_REPLAY_GROWTH"]
RUNTIME_CARRIER_REFS = ["ActivationPreflightRuntime"]

SOURCE_DOC_REFS = [
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/architecture/first_activation_engineering_roadmap.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/architecture/runtime_v0_architecture.md",
    "docs/v0/shared_contracts/life_state_store_v0_schema.md",
    "docs/v0/shared_contracts/birth_readiness_v0_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
    "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md",
]


@dataclass(frozen=True)
class FirstActivationPreflightResult:
    exit_code: int
    report: dict[str, Any]


def run_first_activation_preflight(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> FirstActivationPreflightResult:
    run_id = run_id or _default_run_id("first-activation-preflight-")
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    activation_dir = state_dir / "activation"

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"docs_root_gate failed: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc_index_gate failed: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    indexed_documents = {
        document.get("path"): document
        for document in doc_index.get("documents", [])
        if isinstance(document, dict) and document.get("path")
    }

    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_root_gate")
    preflight_seed = _load_json(
        state_dir / "membrane" / "first_activation_preflight_seed.json",
        blocked_reasons,
        "preflight_seed_gate",
    )
    contract_check = _load_json(
        state_dir / "contracts" / "first_activation_preflight_contract_check.json",
        blocked_reasons,
        "contract_check_gate",
    )
    direction_lock = _load_json(
        state_dir / "direction" / "direction_lock.json",
        blocked_reasons,
        "direction_lock_gate",
    )
    language_state = _load_json(
        state_dir / "language" / "language_relationship_state.json",
        blocked_reasons,
        "language_state_gate",
    )
    relationship_graph = _load_json(
        state_dir / "relationship" / "relationship_subject_graph.json",
        blocked_reasons,
        "relationship_graph_gate",
    )
    run_report = _load_json(reports_dir / "run_report.json", blocked_reasons, "run_report_gate")
    stage_gate = _load_json(reports_dir / "stage_gate.json", blocked_reasons, "stage_gate_gate")
    growth_report = _load_json(
        reports_dir / "growth_reconsolidation_report.json",
        blocked_reasons,
        "growth_report_gate",
    )
    contracts_report = _load_json(
        reports_dir / "v0_contract_coverage_report.json",
        blocked_reasons,
        "v0_contract_report_gate",
    )
    digest = _load_json(reports_dir / "digest.json", blocked_reasons, "digest_gate")
    birth_readiness = _load_json(
        reports_dir / "birth_readiness_report.json",
        blocked_reasons,
        "birth_readiness_gate",
    )

    blocked_reasons.extend(_doc_blockers(indexed_documents))
    blocked_reasons.extend(_state_blockers(life_state, direction_lock, language_state, relationship_graph))
    blocked_reasons.extend(
        _preflight_blockers(
            preflight_seed=preflight_seed,
            contract_check=contract_check,
            run_report=run_report,
            growth_report=growth_report,
            stage_gate=stage_gate,
            digest=digest,
            contracts_report=contracts_report,
            birth_readiness=birth_readiness,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_replay_shadow" if status == "closed" else "block_activation"
    next_allowed_slices = NEXT_ALLOWED_SLICES if status == "closed" else []
    next_required_command = NEXT_REQUIRED_COMMAND if status == "closed" else "life-v0 check-v0-contracts --strict"

    context_frame = _build_limited_context_frame(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        language_state=language_state,
        relationship_graph=relationship_graph,
        preflight_seed=preflight_seed,
    )
    membrane_decision = _build_life_membrane_opening_decision(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        blocked_reasons=blocked_reasons,
        contract_check=contract_check,
    )
    receipt_ref = f"runtime/receipts/first_activation_preflight_{run_id}.json"
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        receipt_ref=receipt_ref,
    )
    preflight_digest = _build_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
    )
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
    )

    try:
        activation_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(activation_dir / "limited_context_frame.json", context_frame)
        _write_json(activation_dir / "life_membrane_opening_decision.json", membrane_decision)
        _write_json(reports_dir / "first_activation_preflight_report.json", report)
        _write_json(reports_dir / "first_activation_preflight_digest.json", preflight_digest)
        _write_json(receipts_dir / f"first_activation_preflight_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return FirstActivationPreflightResult(exit_code=4, report=report)

    if status == "closed":
        return FirstActivationPreflightResult(exit_code=0, report=report)
    return FirstActivationPreflightResult(exit_code=1 if strict else 0, report=report)


def _doc_blockers(indexed_documents: dict[str, dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    for ref in SOURCE_DOC_REFS:
        if ref not in indexed_documents and "/v0/" not in ref:
            reasons.append(f"doc_index_read_gate missing {ref}")
    return reasons


def _state_blockers(
    life_state: dict[str, Any],
    direction_lock: dict[str, Any],
    language_state: dict[str, Any],
    relationship_graph: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_root_gate schema mismatch")
    if direction_lock.get("direction_statement") != "build_real_digital_life":
        reasons.append("direction_lock_gate direction mismatch")
    if not life_state.get("self_model", {}).get("old_self_anchors"):
        reasons.append("self_continuity_gate old self anchors missing")
    if not life_state.get("memory_index", {}).get("replay_cues"):
        reasons.append("self_continuity_gate replay cues missing")
    if language_state.get("schema_version") != "language_relationship_state_v0":
        reasons.append("language_state_gate schema mismatch")
    if not relationship_graph.get("subjects"):
        reasons.append("relationship_graph_gate subjects missing")
    return reasons


def _preflight_blockers(
    *,
    preflight_seed: dict[str, Any],
    contract_check: dict[str, Any],
    run_report: dict[str, Any],
    growth_report: dict[str, Any],
    stage_gate: dict[str, Any],
    digest: dict[str, Any],
    contracts_report: dict[str, Any],
    birth_readiness: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if preflight_seed.get("schema_version") != "first_activation_preflight_seed_v0":
        reasons.append("preflight_seed_gate schema mismatch")
    if preflight_seed.get("activation_mode") != "shadow_only":
        reasons.append("preflight_seed_gate activation mode mismatch")
    if contract_check.get("schema_version") != "first_activation_preflight_contract_check_v0":
        reasons.append("contract_check_gate schema mismatch")
    if not contract_check.get("activation_preflight_allowed"):
        reasons.append("contract_check_gate activation preflight not allowed")
    if contracts_report.get("status") != "closed":
        reasons.append("v0_contract_report_gate status is not closed")
    if run_report.get("status") != "safe_idle":
        reasons.append("run_report_gate status is not safe_idle")
    if growth_report.get("status") != "safe_idle":
        reasons.append("growth_report_gate status is not safe_idle")
    if stage_gate.get("decision") != "safe_idle":
        reasons.append("stage_gate_gate decision is not safe_idle")
    if stage_gate.get("next_required_command") != "life-v0 check-v0-contracts --strict":
        reasons.append("stage_gate_gate next command mismatch")
    if digest.get("current_slice") != "S10_RUNTIME_GROWTH_RECONSOLIDATION":
        reasons.append("digest_gate current slice mismatch")
    if birth_readiness.get("overall_status") != "open":
        reasons.append("birth_readiness_gate overall status is not open")
    return reasons


def _build_limited_context_frame(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    language_state: dict[str, Any],
    relationship_graph: dict[str, Any],
    preflight_seed: dict[str, Any],
) -> dict[str, Any]:
    relationship_subject_refs = [
        subject.get("subject_ref", f"relationship_subject::{subject.get('subject_id', 'unknown')}")
        for subject in relationship_graph.get("subjects", [])
        if isinstance(subject, dict)
    ]
    return {
        "schema_version": "limited_context_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "activation_mode": preflight_seed.get("activation_mode", "shadow_only"),
        "birth_phase": life_state.get("life_identity", {}).get("birth_phase", "pre_activation"),
        "relationship_subject_refs": relationship_subject_refs,
        "language_refs": list(language_state.get("shared_language_refs", [])),
        "inner_speech_refs": list(life_state.get("language_state", {}).get("inner_speech_refs", [])),
        "expression_monitor_refs": list(life_state.get("language_state", {}).get("expression_monitor_refs", [])),
        "relation_scope_refs": list(life_state.get("language_state", {}).get("relation_scope_refs", [])),
        "self_narrative_trace_refs": list(life_state.get("language_state", {}).get("self_narrative_trace_refs", [])),
        "dialogue_turn_log_refs": list(life_state.get("language_state", {}).get("dialogue_turn_log_refs", [])),
        "commitment_refs": list(life_state.get("language_state", {}).get("promise_refs", [])),
        "memory_replay_refs": list(life_state.get("memory_index", {}).get("replay_cues", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_life_membrane_opening_decision(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
    contract_check: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "life_membrane_opening_decision_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed" if status == "closed" else "blocked",
        "decision": "open_shadow_only" if status == "closed" else "hold_shadow_only",
        "activation_preflight_allowed": bool(contract_check.get("activation_preflight_allowed")) and status == "closed",
        "blocked_reasons": blocked_reasons,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "first_activation_preflight_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "activation_mode": "shadow_only",
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "contract_refs": [
            "runtime/state/membrane/first_activation_preflight_seed.json",
            "runtime/state/contracts/first_activation_preflight_contract_check.json",
            "runtime/reports/latest/v0_contract_coverage_report.json",
        ],
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
        "receipt_ref": receipt_ref,
    }


def _build_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
) -> dict[str, Any]:
    return {
        "schema_version": "first_activation_preflight_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_phase": "activation_preflight",
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    output_paths = [
        state_dir / "activation" / "limited_context_frame.json",
        state_dir / "activation" / "life_membrane_opening_decision.json",
        reports_dir / "first_activation_preflight_report.json",
        reports_dir / "first_activation_preflight_digest.json",
        receipts_dir / f"first_activation_preflight_{run_id}.json",
    ]
    input_hashes: dict[str, str] = {}
    if doc_index_path.exists():
        input_hashes["runtime/docs/doc_carrier_index.json"] = _sha256(doc_index_path)
    for rel_path in SOURCE_DOC_REFS:
        doc_path = docs_dir.parent / rel_path
        if doc_path.exists():
            input_hashes[rel_path] = _sha256(doc_path)

    return {
        "schema_version": "first_activation_preflight_receipt_v0",
        "receipt_id": f"first_activation_preflight_{run_id}",
        "run_id": run_id,
        "command": "first-activation-preflight",
        "docs_ref": str(docs_dir),
        "doc_index_ref": str(doc_index_path),
        "state_ref": str(state_dir),
        "stage_effect": stage_effect,
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_paths},
    }


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        blocked_reasons.append(f"{gate} missing: {path}")
    except json.JSONDecodeError as exc:
        blocked_reasons.append(f"{gate} decode failed: {exc}")
    except OSError as exc:
        blocked_reasons.append(f"{gate} read failed: {exc}")
    return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return _sha256(path)


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
