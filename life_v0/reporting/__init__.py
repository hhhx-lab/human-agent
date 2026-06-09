from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_DOC_REFS = [
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
    "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
    "ReconsolidationReplayRuntime",
    "V0ContractCoverageRuntime",
    "ActivationPreflightRuntime",
]
QUEUE_E_STATE_REFS = [
    "runtime/state/action/responsibility_loop_state.json",
    "runtime/state/membrane/world_contact_summary.json",
]
QUEUE_E_REPORT_REFS = ["runtime/reports/latest/pain_regret_repair_report.json"]

NEXT_REQUIRED_COMMAND = "life-v0 explain-stage --strict"


@dataclass(frozen=True)
class EmitReportResult:
    exit_code: int
    report: dict[str, Any]


def run_emit_report(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> EmitReportResult:
    run_id = run_id or _default_run_id("emit-report-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []

    report_inputs = {
        "run_report": _load_json(reports_dir / "run_report.json", blocked_reasons, "run_report_gate"),
        "growth_report": _load_json(reports_dir / "growth_reconsolidation_report.json", blocked_reasons, "growth_report_gate"),
        "stage_gate": _load_json(reports_dir / "stage_gate.json", blocked_reasons, "stage_gate_gate"),
        "v0_contract_report": _load_json(reports_dir / "v0_contract_coverage_report.json", blocked_reasons, "v0_contract_gate"),
        "preflight_report": _load_json(reports_dir / "first_activation_preflight_report.json", blocked_reasons, "preflight_report_gate"),
        "preflight_digest": _load_json(reports_dir / "first_activation_preflight_digest.json", blocked_reasons, "preflight_digest_gate"),
        "replay_report": _load_json(reports_dir / "replay_shadow_report.json", blocked_reasons, "replay_report_gate"),
        "replay_stage_gate": _load_json(reports_dir / "replay_shadow_stage_gate.json", blocked_reasons, "replay_stage_gate_gate"),
        "archive_report": _load_json(reports_dir / "growth_archive_report.json", blocked_reasons, "archive_report_gate"),
        "archive_digest": _load_json(reports_dir / "growth_archive_digest.json", blocked_reasons, "archive_digest_gate"),
        "archive_stage_gate": _load_json(reports_dir / "growth_archive_stage_gate.json", blocked_reasons, "archive_stage_gate_gate"),
    }

    handoff = _load_json(
        state_dir / "archive" / "growth_archive_to_shadow_handoff.json",
        blocked_reasons,
        "growth_archive_handoff_gate",
    )
    shared_term_registry = _load_json(
        state_dir / "language" / "shared_term_registry.json",
        blocked_reasons,
        "shared_term_registry_gate",
    )
    relation_scope_index = _load_json(
        state_dir / "language" / "relation_scope_language_index.json",
        blocked_reasons,
        "relation_scope_gate",
    )
    self_narrative_trace = _load_json(
        state_dir / "language" / "self_narrative_language_trace.json",
        blocked_reasons,
        "self_narrative_trace_gate",
    )
    expression_monitor = _load_json(
        state_dir / "language" / "expression_monitor_state.json",
        blocked_reasons,
        "expression_monitor_gate",
    )
    repair_language = _load_json(
        state_dir / "language" / "commitment_repair_language_index.json",
        blocked_reasons,
        "repair_language_gate",
    )
    responsibility_loop = _load_json(
        state_dir / "action" / "responsibility_loop_state.json",
        blocked_reasons,
        "responsibility_loop_gate",
    )
    world_contact_summary = _load_json(
        state_dir / "membrane" / "world_contact_summary.json",
        blocked_reasons,
        "world_contact_summary_gate",
    )
    pain_regret_repair_report = _load_json(
        reports_dir / "pain_regret_repair_report.json",
        blocked_reasons,
        "pain_regret_repair_gate",
    )

    dialogue_log_path = state_dir / "language" / "dialogue_turn_log.jsonl"
    dialogue_turn_refs = _collect_dialogue_turn_refs(dialogue_log_path, blocked_reasons)

    blocked_reasons.extend(
        _input_blockers(
            report_inputs,
            handoff,
            responsibility_loop=responsibility_loop,
            world_contact_summary=world_contact_summary,
            pain_regret_repair_report=pain_regret_repair_report,
        )
    )
    blocked_reasons.extend(
        _language_restore_blockers(
            shared_term_registry=shared_term_registry,
            relation_scope_index=relation_scope_index,
            self_narrative_trace=self_narrative_trace,
            expression_monitor=expression_monitor,
            repair_language=repair_language,
            dialogue_turn_refs=dialogue_turn_refs,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    receipt_ref = f"runtime/receipts/emit_report_{run_id}.json"

    report_refs = [
        "runtime/reports/latest/run_report.json",
        "runtime/reports/latest/growth_reconsolidation_report.json",
        "runtime/reports/latest/stage_gate.json",
        "runtime/reports/latest/v0_contract_coverage_report.json",
        "runtime/reports/latest/first_activation_preflight_report.json",
        "runtime/reports/latest/replay_shadow_report.json",
        "runtime/reports/latest/replay_shadow_stage_gate.json",
        "runtime/reports/latest/pain_regret_repair_report.json",
        "runtime/reports/latest/growth_archive_report.json",
        "runtime/reports/latest/growth_archive_stage_gate.json",
    ]
    digest_refs = [
        "runtime/reports/latest/first_activation_preflight_digest.json",
        "runtime/reports/latest/growth_archive_digest.json",
    ]
    stage_gate_refs = [
        "runtime/reports/latest/stage_gate.json",
        "runtime/reports/latest/replay_shadow_stage_gate.json",
        "runtime/reports/latest/growth_archive_stage_gate.json",
    ]

    bundle = _build_report_bundle(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        blocked_reasons=blocked_reasons,
        report_refs=report_refs,
        digest_refs=digest_refs,
        stage_gate_refs=stage_gate_refs,
        queue_e_state_refs=QUEUE_E_STATE_REFS,
        queue_e_report_refs=QUEUE_E_REPORT_REFS,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        receipt_ref=receipt_ref,
    )
    bundle_digest = _build_report_bundle_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        blocked_reasons=blocked_reasons,
        report_refs=report_refs,
        queue_e_ref_count=len(QUEUE_E_STATE_REFS) + len(QUEUE_E_REPORT_REFS),
    )
    return_packet = _build_first_activation_return_packet(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        shared_term_registry=shared_term_registry,
        relation_scope_index=relation_scope_index,
        self_narrative_trace=self_narrative_trace,
        expression_monitor=expression_monitor,
        repair_language=repair_language,
        dialogue_turn_refs=dialogue_turn_refs,
        responsibility_loop=responsibility_loop,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    latest_stage_ref = _build_latest_stage_explanation_ref(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        archive_stage_gate=report_inputs["archive_stage_gate"],
    )
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
    )

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "report_bundle.json", bundle)
        _write_json(reports_dir / "report_bundle_digest.json", bundle_digest)
        _write_json(reports_dir / "first_activation_return_packet.json", return_packet)
        _write_json(reports_dir / "latest_stage_explanation_ref.json", latest_stage_ref)
        _write_json(receipts_dir / f"emit_report_{run_id}.json", receipt)
    except OSError as exc:
        bundle["status"] = "blocked"
        bundle["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return EmitReportResult(exit_code=4, report=bundle)

    if status == "closed":
        return EmitReportResult(exit_code=0, report=bundle)
    return EmitReportResult(exit_code=1 if strict else 0, report=bundle)


def _input_blockers(
    report_inputs: dict[str, dict[str, Any]],
    handoff: dict[str, Any],
    *,
    responsibility_loop: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if report_inputs["run_report"].get("status") != "safe_idle":
        reasons.append("run_report_gate status is not safe_idle")
    if report_inputs["growth_report"].get("status") != "safe_idle":
        reasons.append("growth_report_gate status is not safe_idle")
    if report_inputs["stage_gate"].get("decision") != "safe_idle":
        reasons.append("stage_gate_gate decision is not safe_idle")
    if report_inputs["v0_contract_report"].get("status") != "closed":
        reasons.append("v0_contract_gate status is not closed")
    if report_inputs["preflight_report"].get("status") != "closed":
        reasons.append("preflight_report_gate status is not closed")
    if report_inputs["replay_report"].get("status") != "closed":
        reasons.append("replay_report_gate status is not closed")
    if report_inputs["archive_report"].get("status") != "closed":
        reasons.append("archive_report_gate status is not closed")
    if report_inputs["archive_stage_gate"].get("decision") != "closed":
        reasons.append("archive_stage_gate_gate decision is not closed")
    if report_inputs["archive_stage_gate"].get("next_required_command") != "life-v0 emit-report --strict":
        reasons.append("archive_stage_gate_gate next command mismatch")
    if not handoff.get("shadow_run_handoff_ready"):
        reasons.append("growth_archive_handoff_gate shadow run handoff not ready")
    if responsibility_loop.get("schema_version") != "responsibility_loop_state_v0":
        reasons.append("responsibility_loop_gate schema mismatch")
    if world_contact_summary.get("schema_version") != "world_contact_summary_v0":
        reasons.append("world_contact_summary_gate schema mismatch")
    if pain_regret_repair_report.get("schema_version") != "pain_regret_repair_report_v0":
        reasons.append("pain_regret_repair_gate schema mismatch")
    if not world_contact_summary.get("release_posture"):
        reasons.append("world_contact_summary_gate release posture missing")
    if not pain_regret_repair_report.get("repair_obligation_refs"):
        reasons.append("pain_regret_repair_gate repair obligations missing")
    return reasons


def _language_restore_blockers(
    *,
    shared_term_registry: dict[str, Any],
    relation_scope_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    expression_monitor: dict[str, Any],
    repair_language: dict[str, Any],
    dialogue_turn_refs: list[str],
) -> list[str]:
    reasons: list[str] = []
    if shared_term_registry.get("schema_version") != "shared_term_registry_v0":
        reasons.append("shared_term_registry_gate schema mismatch")
    if not shared_term_registry.get("shared_terms"):
        reasons.append("shared_term_registry_gate shared terms missing")
    if relation_scope_index.get("schema_version") != "relation_scope_language_index_v0":
        reasons.append("relation_scope_gate schema mismatch")
    if not relation_scope_index.get("relation_scopes"):
        reasons.append("relation_scope_gate relation scopes missing")
    if self_narrative_trace.get("schema_version") != "self_narrative_language_trace_v0":
        reasons.append("self_narrative_trace_gate schema mismatch")
    if not self_narrative_trace.get("narrative_turn_refs"):
        reasons.append("self_narrative_trace_gate narrative turn refs missing")
    if expression_monitor.get("schema_version") != "expression_monitor_state_v0":
        reasons.append("expression_monitor_gate schema mismatch")
    if not repair_language.get("commitment_refs"):
        reasons.append("repair_language_gate commitment refs missing")
    if not dialogue_turn_refs:
        reasons.append("dialogue_turn_log_gate dialogue turns missing")
    return reasons


def _build_report_bundle(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
    report_refs: list[str],
    digest_refs: list[str],
    stage_gate_refs: list[str],
    queue_e_state_refs: list[str],
    queue_e_report_refs: list[str],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "report_bundle_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "engineering_slice_ref": "S10_TO_S11_REPORT_BUNDLE",
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "report_refs": report_refs,
        "digest_refs": digest_refs,
        "stage_gate_refs": stage_gate_refs,
        "queue_e_state_refs": queue_e_state_refs,
        "queue_e_report_refs": queue_e_report_refs,
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "blocked_reasons": blocked_reasons,
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "receipt_ref": receipt_ref,
    }


def _build_report_bundle_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
    report_refs: list[str],
    queue_e_ref_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": "report_bundle_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "blocked_reasons": blocked_reasons,
        "report_count": len(report_refs),
        "queue_e_ref_count": queue_e_ref_count,
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_first_activation_return_packet(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    shared_term_registry: dict[str, Any],
    relation_scope_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    expression_monitor: dict[str, Any],
    repair_language: dict[str, Any],
    dialogue_turn_refs: list[str],
    responsibility_loop: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "first_activation_return_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "activation_mode": "shadow_only",
        "return_phase": "post_growth_archive",
        "relation_restore_refs": ["runtime/state/relationship/relationship_subject_graph.json"],
        "shared_term_restore_refs": ["runtime/state/language/shared_term_registry.json#shared-term-v0-0001"] if shared_term_registry.get("shared_terms") else [],
        "unresolved_commitment_refs": list(repair_language.get("commitment_refs", [])),
        "expression_monitor_restore_refs": ["runtime/state/language/expression_monitor_state.json"] if expression_monitor else [],
        "relation_scope_restore_refs": ["runtime/state/language/relation_scope_language_index.json#relation-scope-v0-0001"] if relation_scope_index.get("relation_scopes") else [],
        "self_narrative_restore_refs": list(self_narrative_trace.get("narrative_turn_refs", [])),
        "dialogue_turn_restore_refs": dialogue_turn_refs,
        "responsibility_restore_refs": ["runtime/state/action/responsibility_loop_state.json"],
        "world_contact_restore_refs": ["runtime/state/membrane/world_contact_summary.json"],
        "pain_regret_restore_refs": QUEUE_E_REPORT_REFS,
        "regret_pressure_restore_refs": list(pain_regret_repair_report.get("regret_pressure_refs", [])),
        "repair_obligation_restore_refs": list(pain_regret_repair_report.get("repair_obligation_refs", [])),
        "responsibility_language_restore_refs": list(responsibility_loop.get("language_writeback_refs", [])),
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "report_bundle_ref": "runtime/reports/latest/report_bundle.json",
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_latest_stage_explanation_ref(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    archive_stage_gate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "latest_stage_explanation_ref_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "source_stage_gate_ref": "runtime/reports/latest/growth_archive_stage_gate.json",
        "stage_effect": archive_stage_gate.get("stage_effect", "archive_written"),
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "run_report.json",
        reports_dir / "growth_reconsolidation_report.json",
        reports_dir / "stage_gate.json",
        reports_dir / "v0_contract_coverage_report.json",
        reports_dir / "first_activation_preflight_report.json",
        reports_dir / "first_activation_preflight_digest.json",
        reports_dir / "replay_shadow_report.json",
        reports_dir / "replay_shadow_stage_gate.json",
        reports_dir / "growth_archive_report.json",
        reports_dir / "growth_archive_digest.json",
        reports_dir / "growth_archive_stage_gate.json",
        state_dir / "archive" / "growth_archive_to_shadow_handoff.json",
        state_dir / "action" / "responsibility_loop_state.json",
        state_dir / "membrane" / "world_contact_summary.json",
        state_dir / "language" / "shared_term_registry.json",
        state_dir / "language" / "relation_scope_language_index.json",
        state_dir / "language" / "self_narrative_language_trace.json",
        state_dir / "language" / "expression_monitor_state.json",
        reports_dir / "pain_regret_repair_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_paths = [
        reports_dir / "report_bundle.json",
        reports_dir / "report_bundle_digest.json",
        reports_dir / "first_activation_return_packet.json",
        reports_dir / "latest_stage_explanation_ref.json",
        receipts_dir / f"emit_report_{run_id}.json",
    ]
    return {
        "schema_version": "emit_report_receipt_v0",
        "receipt_id": f"emit_report_{run_id}",
        "run_id": run_id,
        "command": "emit-report",
        "state_ref": "runtime/state",
        "report_refs": [
            "runtime/reports/latest/report_bundle.json",
            "runtime/reports/latest/report_bundle_digest.json",
            "runtime/reports/latest/first_activation_return_packet.json",
            "runtime/reports/latest/latest_stage_explanation_ref.json",
        ],
        "stage_effect": "report_bundle_emitted",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_paths},
    }


def _collect_dialogue_turn_refs(path: Path, blocked_reasons: list[str]) -> list[str]:
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError as exc:
        blocked_reasons.append(f"dialogue_turn_log_gate failed: {exc}")
        return []
    return [f"runtime/state/language/dialogue_turn_log.jsonl#line-{idx}" for idx, _ in enumerate(lines, start=1)]


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
