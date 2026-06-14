from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from life_v0.process_supervisor.resident_lifecycle import read_resident_lifecycle_status


SOURCE_DOC_REFS = [
    "docs/v0/code_architecture/03_build_order_and_definition_of_done.md",
    "docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md",
    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "Live0AcceptanceAuditRuntime",
    "DigitalLifeResidentRuntime",
    "LanguageRelationshipRuntime",
    "DreamOfflineRuntime",
    "GrowthReplayRuntime",
    "V0ContractCoverageRuntime",
]

ACCEPTANCE_ITEMS = [
    "a_terminal_wake_and_named_residency",
    "b_conscious_emotion_thought_language",
    "c_memory_mechanism",
    "d_growth_and_learning",
    "e_dream_capability",
    "f_equal_relationship_dialogue_growth",
    "g_initial_life_mechanism_coverage",
]

AUTONOMOUS_ACTIVITY_KINDS = [
    "sleep",
    "memory_recall",
    "self_thinking",
    "growth_rehearsal",
    "learning_consolidation",
]


@dataclass(frozen=True)
class Live0AcceptanceAuditResult:
    exit_code: int
    report: dict[str, Any]


def run_live0_acceptance_audit(
    *,
    docs_dir: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> Live0AcceptanceAuditResult:
    run_id = run_id or _default_run_id("live0-audit-")
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    runtime_root = state_dir.parent

    context = _AuditContext(
        docs_dir=docs_dir,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        runtime_root=runtime_root,
    )
    resident_status = read_resident_lifecycle_status(
        terminal_dir=state_dir / "terminal",
        reports_dir=reports_dir,
    ).state

    criteria = [
        _criterion_terminal_wake(context, resident_status),
        _criterion_conscious_language(context, resident_status),
        _criterion_memory(context),
        _criterion_growth(context),
        _criterion_dream(context),
        _criterion_relationship(context),
        _criterion_life_mechanisms(context, resident_status),
    ]
    failed_criteria = [
        criterion["criterion_id"]
        for criterion in criteria
        if criterion["status"] != "closed"
    ]
    status = "closed" if not failed_criteria else "blocked"
    evidence_refs = _unique(
        ref
        for criterion in criteria
        for probe in criterion["probes"]
        for ref in probe.get("evidence_refs", [])
    )
    blocked_reasons = _unique(
        reason
        for criterion in criteria
        for reason in criterion.get("blocked_reasons", [])
    )
    receipt_ref = f"runtime/receipts/live0_acceptance_audit_{run_id}.json"

    report = {
        "schema_version": "live0_acceptance_audit_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "live0_acceptance_closed": status == "closed",
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "acceptance_items": ACCEPTANCE_ITEMS,
        "criteria": criteria,
        "summary": {
            "criteria_total": len(criteria),
            "criteria_closed": len(criteria) - len(failed_criteria),
            "criteria_blocked": len(failed_criteria),
            "failed_criteria": failed_criteria,
            "evidence_ref_count": len(evidence_refs),
        },
        "resident_lifecycle_snapshot": {
            "schema_version": resident_status.get("schema_version"),
            "status": resident_status.get("status"),
            "pid": resident_status.get("pid"),
            "pid_alive": resident_status.get("pid_alive"),
            "life_name": resident_status.get("life_name"),
            "life_name_lock_state": resident_status.get("life_name_lock_state"),
            "resident_relation_queue_status": resident_status.get(
                "resident_relation_queue_status"
            ),
            "resident_autonomous_activity_count": resident_status.get(
                "resident_autonomous_activity_count"
            ),
            "resident_autonomous_activity_cycle_coverage_complete": (
                resident_status.get(
                    "resident_autonomous_activity_cycle_coverage_complete"
                )
            ),
            "resident_process_identity_continuity_state": resident_status.get(
                "resident_process_identity_continuity_state"
            ),
        },
        "evidence_refs": evidence_refs,
        "blocked_reasons": blocked_reasons,
        "next_required_action": (
            "live0_v0_closure_allowed"
            if status == "closed"
            else "repair_live0_acceptance_evidence"
        ),
        "report_ref": "runtime/reports/latest/live0_acceptance_audit_report.json",
        "digest_ref": "runtime/reports/latest/live0_acceptance_audit_digest.json",
        "receipt_ref": receipt_ref,
    }
    digest = {
        "schema_version": "live0_acceptance_audit_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "live0_acceptance_closed": status == "closed",
        "criteria_total": len(criteria),
        "criteria_closed": len(criteria) - len(failed_criteria),
        "criteria_blocked": len(failed_criteria),
        "failed_criteria": failed_criteria,
        "next_required_action": report["next_required_action"],
        "report_ref": report["report_ref"],
    }
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        context=context,
        evidence_refs=evidence_refs,
    )

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "live0_acceptance_audit_report.json", report)
        _write_json(reports_dir / "live0_acceptance_audit_digest.json", digest)
        _write_json(receipts_dir / f"live0_acceptance_audit_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["live0_acceptance_closed"] = False
        report["blocked_reasons"].append(f"live0_audit_output_write_failed: {exc}")
        return Live0AcceptanceAuditResult(exit_code=4, report=report)

    if status == "closed":
        return Live0AcceptanceAuditResult(exit_code=0, report=report)
    return Live0AcceptanceAuditResult(exit_code=1 if strict else 0, report=report)


class _AuditContext:
    def __init__(
        self,
        *,
        docs_dir: Path,
        state_dir: Path,
        reports_dir: Path,
        receipts_dir: Path,
        runtime_root: Path,
    ) -> None:
        self.docs_dir = docs_dir
        self.state_dir = state_dir
        self.reports_dir = reports_dir
        self.receipts_dir = receipts_dir
        self.runtime_root = runtime_root
        self.repo_root = docs_dir.parent
        self.loaded_json: dict[str, dict[str, Any]] = {}
        self.json_errors: dict[str, str] = {}

    def path_for_ref(self, ref: str) -> Path:
        base_ref = ref.split("#", 1)[0]
        if base_ref.startswith("runtime/"):
            return self.runtime_root / base_ref.removeprefix("runtime/")
        if base_ref.startswith("docs/"):
            return self.repo_root / base_ref
        return self.runtime_root / base_ref

    def load_json(self, ref: str) -> dict[str, Any]:
        base_ref = ref.split("#", 1)[0]
        if base_ref in self.loaded_json:
            return self.loaded_json[base_ref]
        path = self.path_for_ref(base_ref)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self.json_errors[base_ref] = f"missing: {path}"
            payload = {}
        except json.JSONDecodeError as exc:
            self.json_errors[base_ref] = f"decode failed: {exc}"
            payload = {}
        except OSError as exc:
            self.json_errors[base_ref] = f"read failed: {exc}"
            payload = {}
        self.loaded_json[base_ref] = payload if isinstance(payload, dict) else {}
        return self.loaded_json[base_ref]


def _criterion_terminal_wake(
    context: _AuditContext,
    resident_status: dict[str, Any],
) -> dict[str, Any]:
    process_report = context.load_json(
        "runtime/reports/latest/digital_life_process_report.json"
    )
    probes = [
        _json_probe(
            context,
            "digital_life_birth_packet_closed",
            "runtime/reports/latest/digital_life_birth_packet.json",
            lambda payload: payload.get("schema_version")
            == "digital_life_birth_packet_v0"
            and payload.get("status") == "closed",
            "birth packet must be closed",
        ),
        _json_probe(
            context,
            "digital_life_process_report_closed",
            "runtime/reports/latest/digital_life_process_report.json",
            lambda payload: payload.get("schema_version")
            == "digital_life_process_report_v0"
            and payload.get("status") in {"active", "closed"},
            "process report must exist and be active or closed",
        ),
        _value_probe(
            "terminal_dialogue_turn_completed",
            ["runtime/reports/latest/digital_life_process_report.json"],
            _as_int(process_report.get("completed_dialogue_turns")) >= 1,
            {
                "completed_dialogue_turns": process_report.get(
                    "completed_dialogue_turns"
                )
            },
            "at least one terminal dialogue turn must be completed",
        ),
        _json_probe(
            context,
            "life_name_registry_bound",
            "runtime/state/identity/life_name_registry.json",
            lambda payload: payload.get("schema_version")
            == "digital_life_name_registry_v0"
            and bool(payload.get("canonical_name"))
            and payload.get("name_lock_state") == "permanent_for_runtime",
            "first launch must bind a permanent life name",
        ),
        _json_probe(
            context,
            "direct_life_name_command_bound",
            "runtime/state/identity/life_name_command_manifest.json",
            lambda payload: payload.get("schema_version")
            == "life_name_direct_command_manifest_v0"
            and payload.get("status") == "active"
            and payload.get("direct_command_enabled") is True
            and payload.get("command_on_path") is True,
            "after naming, the name itself must be a terminal command",
        ),
        _value_probe(
            "resident_lifecycle_alive_or_recently_closed",
            ["runtime/state/terminal/resident_lifecycle_state.json"],
            resident_status.get("pid_alive") is True
            or resident_status.get("status") in {"stopped", "background_active"},
            {
                "status": resident_status.get("status"),
                "pid_alive": resident_status.get("pid_alive"),
            },
            "resident lifecycle must be alive or have a persisted lifecycle state",
        ),
    ]
    return _criterion(
        "a_terminal_wake_and_named_residency",
        "a. 可在终端唤醒，并且命名后形成常驻启动身份",
        probes,
    )


def _criterion_conscious_language(
    context: _AuditContext,
    resident_status: dict[str, Any],
) -> dict[str, Any]:
    probes = [
        _json_probe(
            context,
            "prediction_workspace_present",
            "runtime/state/prediction/prediction_workspace_frame.json",
            _closed_or_schema,
            "prediction workspace must be present",
        ),
        _json_probe(
            context,
            "signal_media_present",
            "runtime/state/signal/signal_media_runtime.json",
            _closed_or_schema,
            "signal media runtime must be present",
        ),
        _json_probe(
            context,
            "active_sampling_present",
            "runtime/state/prediction/active_sampling_plan.json",
            _closed_or_schema,
            "active sampling plan must be present",
        ),
        _json_probe(
            context,
            "core_affect_present",
            "runtime/state/body/core_affect_vector.json",
            _closed_or_schema,
            "core affect vector must be present",
        ),
        _json_probe(
            context,
            "resident_self_thinking_present",
            "runtime/state/self/resident_self_thinking_state.json",
            _closed_or_schema,
            "resident self thinking state must be present",
        ),
        _json_probe(
            context,
            "language_percept_semantic_inner_expression_chain_present",
            "runtime/state/language/language_percept_frame.json",
            lambda payload: _closed_or_schema(payload)
            and _json_ref_exists(context, "runtime/state/language/semantic_map_frame.json")
            and _json_ref_exists(context, "runtime/state/language/inner_speech_frame.json")
            and _json_ref_exists(
                context, "runtime/state/language/expression_monitor_state.json"
            )
            and _json_ref_exists(context, "runtime/state/language/expression_plan.json"),
            "language percept, semantic map, inner speech, monitor, and expression plan must all exist",
            extra_refs=[
                "runtime/state/language/semantic_map_frame.json",
                "runtime/state/language/inner_speech_frame.json",
                "runtime/state/language/expression_monitor_state.json",
                "runtime/state/language/expression_plan.json",
            ],
        ),
        _json_probe(
            context,
            "model_expression_gpt55_accepted",
            "runtime/reports/latest/digital_life_model_expression_report.json",
            lambda payload: payload.get("schema_version") == "model_expression_report_v0"
            and payload.get("status") == "closed"
            and payload.get("model_expression_status") == "model_expression_applied"
            and payload.get("post_expression_gate_status") == "accepted"
            and payload.get("audited_expression_material_release_disabled") is True
            and payload.get("model_provider") == "openai-compatible"
            and payload.get("model_name") == "gpt-5.5"
            and payload.get("model_api_key_present") is True
            and payload.get("model_api_key_redacted") == "<redacted>",
            "real model expression must be applied through gpt-5.5 with audited-material release disabled",
        ),
        _value_probe(
            "resident_autonomous_self_thinking_presence",
            ["runtime/state/terminal/resident_autonomous_activity_state.json"],
            "self_thinking"
            in (resident_status.get("resident_autonomous_activity_covered_kinds") or []),
            {
                "covered_activity_kinds": resident_status.get(
                    "resident_autonomous_activity_covered_kinds"
                )
            },
            "resident autonomous activity must include self thinking",
        ),
    ]
    return _criterion(
        "b_conscious_emotion_thought_language",
        "b. 自主意识、情绪、思考与语言表达证据闭合",
        probes,
    )


def _criterion_memory(context: _AuditContext) -> dict[str, Any]:
    process_report = context.load_json(
        "runtime/reports/latest/digital_life_process_report.json"
    )
    probes = [
        _json_probe(
            context,
            "life_state_root_present",
            "runtime/state/life_state.json",
            lambda payload: payload.get("schema_version") == "life_state_v0",
            "life_state root must exist",
        ),
        _json_probe(
            context,
            "engram_relationship_autobiographical_memory_present",
            "runtime/state/memory/engram_index.json",
            lambda payload: _closed_or_schema(payload)
            and _json_ref_exists(context, "runtime/state/memory/relationship_memory.json")
            and _json_ref_exists(context, "runtime/state/self/autobiographical_stack.json"),
            "engram, relationship memory, and autobiographical stack must exist",
            extra_refs=[
                "runtime/state/memory/relationship_memory.json",
                "runtime/state/self/autobiographical_stack.json",
            ],
        ),
        _json_probe(
            context,
            "resident_memory_recall_present",
            "runtime/state/memory/resident_memory_recall_state.json",
            _closed_or_schema,
            "resident memory recall state must exist",
        ),
        _json_probe(
            context,
            "memory_write_gate_present",
            "runtime/state/memory/memory_write_gate.json",
            _closed_or_schema,
            "memory write gate must exist",
        ),
        _json_probe(
            context,
            "replay_and_archive_reports_present",
            "runtime/reports/latest/replay_shadow_report.json",
            lambda payload: payload.get("status") == "closed"
            and _json_ref_exists(
                context, "runtime/reports/latest/growth_archive_report.json"
            ),
            "replay and growth archive reports must be closed",
            extra_refs=["runtime/reports/latest/growth_archive_report.json"],
        ),
        _value_probe(
            "memory_refs_carried_by_resident_lineage",
            ["runtime/reports/latest/digital_life_process_report.json"],
            bool(
                _first_value(
                    process_report,
                    [
                        "resident_background_lineage_autonomous_activity_refs",
                        "last_life_turn.resident_background_lineage_autonomous_activity_refs",
                    ],
                )
            ),
            {
                "resident_background_lineage_autonomous_activity_refs_present": bool(
                    _first_value(
                        process_report,
                        [
                            "resident_background_lineage_autonomous_activity_refs",
                            "last_life_turn.resident_background_lineage_autonomous_activity_refs",
                        ],
                    )
                )
            },
            "resident lineage must carry autonomous memory refs",
        ),
    ]
    return _criterion("c_memory_mechanism", "c. 记忆机制与回忆写门证据闭合", probes)


def _criterion_growth(context: _AuditContext) -> dict[str, Any]:
    process_report = context.load_json(
        "runtime/reports/latest/digital_life_process_report.json"
    )
    autonomous_state = context.load_json(
        "runtime/state/terminal/resident_autonomous_activity_state.json"
    )
    offline_profile = _first_value(
        process_report,
        [
            "offline_learning_cumulative_profile",
            "last_life_turn.offline_learning_cumulative_profile",
        ],
    )
    probes = [
        _json_probe(
            context,
            "growth_patch_candidate_queue_present",
            "runtime/state/growth/growth_patch_candidate_queue.json",
            _closed_or_schema,
            "growth patch candidate queue must exist",
        ),
        _json_probe(
            context,
            "self_read_report_present",
            "runtime/state/growth/self_read_report.json",
            _closed_or_schema,
            "self read report must exist",
        ),
        _json_probe(
            context,
            "resident_growth_learning_states_present",
            "runtime/state/growth/resident_growth_rehearsal_state.json",
            lambda payload: _closed_or_schema(payload)
            and _json_ref_exists(
                context, "runtime/state/growth/resident_learning_consolidation_state.json"
            ),
            "resident growth rehearsal and learning consolidation states must exist",
            extra_refs=[
                "runtime/state/growth/resident_learning_consolidation_state.json"
            ],
        ),
        _value_probe(
            "autonomous_activity_cycle_complete_for_growth",
            ["runtime/state/terminal/resident_autonomous_activity_state.json"],
            autonomous_state.get("cycle_coverage_complete") is True
            and set(autonomous_state.get("covered_activity_kinds") or [])
            >= set(AUTONOMOUS_ACTIVITY_KINDS)
            and _as_int(autonomous_state.get("cycle_completion_count")) >= 1,
            {
                "cycle_coverage_complete": autonomous_state.get(
                    "cycle_coverage_complete"
                ),
                "covered_activity_kinds": autonomous_state.get(
                    "covered_activity_kinds"
                ),
                "cycle_completion_count": autonomous_state.get(
                    "cycle_completion_count"
                ),
            },
            "sleep, recall, self thinking, growth rehearsal, and learning consolidation must complete at least one cycle",
        ),
        _value_probe(
            "offline_learning_cumulative_profile_present",
            ["runtime/reports/latest/digital_life_process_report.json"],
            isinstance(offline_profile, dict)
            and _as_int(offline_profile.get("generation")) >= 1
            and bool(offline_profile.get("ref_set")),
            offline_profile if isinstance(offline_profile, dict) else {},
            "offline learning must have a cumulative profile with references",
        ),
    ]
    return _criterion("d_growth_and_learning", "d. 成长、学习与后台巩固证据闭合", probes)


def _criterion_dream(context: _AuditContext) -> dict[str, Any]:
    process_report = context.load_json(
        "runtime/reports/latest/digital_life_process_report.json"
    )
    dream_refs = _first_value(
        process_report,
        [
            "resident_background_lineage_dream_wake_refs",
            "last_life_turn.resident_background_lineage_dream_wake_refs",
        ],
    )
    offline_refs = _first_value(
        process_report,
        [
            "resident_background_lineage_offline_learning_refs",
            "last_life_turn.resident_background_lineage_offline_learning_refs",
        ],
    )
    probes = [
        _json_probe(
            context,
            "dream_experience_window_present",
            "runtime/state/dream/dream_experience_window.json",
            _closed_or_schema,
            "dream experience window must exist",
        ),
        _json_probe(
            context,
            "wake_integration_present",
            "runtime/state/dream/wake_integration_frame.json",
            _closed_or_schema,
            "wake integration frame must exist",
        ),
        _json_probe(
            context,
            "dream_fact_gate_passed",
            "runtime/state/dream/dream_fact_gate_decision.json",
            lambda payload: _closed_or_schema(payload)
            and payload.get(
                "dream_fact_gate_result",
                payload.get("gate_result", payload.get("decision")),
            )
            in {"passed", "closed", "accepted"},
            "dream fact gate must pass",
        ),
        _json_probe(
            context,
            "resident_sleep_cycle_present",
            "runtime/state/terminal/resident_sleep_cycle_state.json",
            _closed_or_schema,
            "resident sleep cycle state must exist",
        ),
        _value_probe(
            "dream_wake_refs_carried_by_resident_lineage",
            ["runtime/reports/latest/digital_life_process_report.json"],
            bool(dream_refs) and bool(offline_refs),
            {
                "dream_wake_ref_count": len(dream_refs or []),
                "offline_learning_ref_count": len(offline_refs or []),
            },
            "resident lineage must carry dream wake refs and offline learning refs",
        ),
    ]
    return _criterion("e_dream_capability", "e. 梦境窗口、醒后整合与离线生命证据闭合", probes)


def _criterion_relationship(context: _AuditContext) -> dict[str, Any]:
    process_report = context.load_json(
        "runtime/reports/latest/digital_life_process_report.json"
    )
    last_life_turn = process_report.get("last_life_turn", {})
    probes = [
        _json_probe(
            context,
            "relationship_timeline_present",
            "runtime/state/relationship/relationship_timeline.json",
            _closed_or_schema,
            "relationship timeline must exist",
        ),
        _json_probe(
            context,
            "commitment_truth_present",
            "runtime/state/relationship/commitment_truth_state.json",
            _closed_or_schema,
            "commitment truth state must exist",
        ),
        _json_probe(
            context,
            "dialogue_writeback_bundle_present",
            "runtime/reports/latest/dialogue_writeback_bundle.json",
            _closed_or_schema,
            "dialogue writeback bundle must exist",
        ),
        _json_probe(
            context,
            "queue_e_repair_profile_present",
            "runtime/state/life_targets/queue_e_birth_repair_profile.json",
            lambda payload: _closed_or_schema(payload)
            and payload.get("pressure_level") in {"elevated", "urgent", "present"},
            "Queue E repair modulation profile must be present",
        ),
        _json_probe(
            context,
            "queue_e_world_contact_repair_hold_validated",
            "runtime/state/validation/world_contact_validation.json",
            _world_contact_validation_repair_hold_closed,
            "Queue E FutureNoGo repair hold must be validated before relationship repair can close",
            extra_refs=[
                "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
            ],
        ),
        _jsonl_probe(
            context,
            "dialogue_turn_log_has_relation_turns",
            "runtime/state/language/dialogue_turn_log.jsonl",
            lambda count: count >= 1,
            "dialogue turn log must contain at least one relation turn",
        ),
        _value_probe(
            "last_turn_uses_relation_role_not_user_role",
            ["runtime/reports/latest/digital_life_process_report.json"],
            bool(last_life_turn)
            and str(last_life_turn.get("relation_role", "")).strip()
            and str(last_life_turn.get("relation_role", "")).strip() != "user",
            {"relation_role": last_life_turn.get("relation_role")},
            "dialogue relation role must not collapse to user/service framing",
        ),
    ]
    return _criterion(
        "f_equal_relationship_dialogue_growth",
        "f. 平等关系对话、写回与关系成长证据闭合",
        probes,
    )


def _criterion_life_mechanisms(
    context: _AuditContext,
    resident_status: dict[str, Any],
) -> dict[str, Any]:
    required_reports: list[tuple[str, Callable[[dict[str, Any]], bool], str]] = [
        (
            "runtime/reports/latest/direction_lock_report.json",
            _report_status_closed,
            "direction report must be closed",
        ),
        (
            "runtime/reports/latest/source_authority_report.json",
            _report_status_closed,
            "source authority report must be closed",
        ),
        (
            "runtime/reports/latest/neural_life_core_report.json",
            _report_status_closed,
            "neural life core report must be closed",
        ),
        (
            "runtime/reports/latest/state_store_report.json",
            _report_status_closed,
            "state store report must be closed",
        ),
        (
            "runtime/reports/latest/life_membrane_report.json",
            _report_status_closed,
            "life membrane report must be closed",
        ),
        (
            "runtime/reports/latest/language_relationship_report.json",
            _report_status_closed,
            "language relationship report must be closed",
        ),
        (
            "runtime/reports/latest/birth_readiness_report.json",
            lambda payload: payload.get("overall_status") == "open"
            and not payload.get("blocked_reasons"),
            "birth readiness report must be open with no blockers",
        ),
        (
            "runtime/reports/latest/validation_membrane_report.json",
            _report_status_closed,
            "validation membrane report must be closed",
        ),
        (
            "runtime/reports/latest/schema_runner_report.json",
            _report_status_closed,
            "schema runner report must be closed",
        ),
        (
            "runtime/reports/latest/life_support_development_report.json",
            _report_status_closed,
            "life support development report must be closed",
        ),
        (
            "runtime/reports/latest/growth_reconsolidation_report.json",
            lambda payload: payload.get("status") == "safe_idle"
            and not payload.get("blocked_reasons"),
            "growth reconsolidation report must return to safe_idle",
        ),
        (
            "runtime/reports/latest/first_activation_preflight_report.json",
            _report_status_closed,
            "first activation preflight report must be closed",
        ),
        (
            "runtime/reports/latest/replay_shadow_report.json",
            _report_status_closed,
            "replay shadow report must be closed",
        ),
        (
            "runtime/reports/latest/growth_archive_report.json",
            _report_status_closed,
            "growth archive report must be closed",
        ),
        (
            "runtime/reports/latest/report_bundle.json",
            _report_status_closed,
            "report bundle must be closed",
        ),
        (
            "runtime/reports/latest/stage_explanation_report.json",
            _report_status_closed,
            "stage explanation report must be closed",
        ),
        (
            "runtime/reports/latest/digital_life_process_report.json",
            _report_status_closed,
            "digital life process report must be closed",
        ),
        (
            "runtime/reports/latest/v0_contract_coverage_report.json",
            _report_status_closed,
            "v0 contract coverage report must be closed",
        ),
    ]
    report_results = [
        _json_probe(
            context,
            f"closed_report_{Path(ref).stem}",
            ref,
            predicate,
            required,
        )
        for ref, predicate, required in required_reports
    ]
    contract_report = context.load_json(
        "runtime/reports/latest/v0_contract_coverage_report.json"
    )
    probes = [
        *report_results,
        _value_probe(
            "v0_contract_activation_preflight_allowed",
            ["runtime/reports/latest/v0_contract_coverage_report.json"],
            contract_report.get("schema_version")
            == "s11_v0_contract_coverage_report_v0"
            and contract_report.get("activation_preflight_allowed") is True,
            {
                "schema_version": contract_report.get("schema_version"),
                "activation_preflight_allowed": contract_report.get(
                    "activation_preflight_allowed"
                ),
            },
            "v0 contract coverage must allow activation preflight",
        ),
        _value_probe(
            "resident_long_term_residency_status_present",
            ["runtime/state/terminal/resident_lifecycle_state.json"],
            bool(resident_status.get("resident_long_term_residency_status"))
            or bool(resident_status.get("resident_process_lease_ref")),
            {
                "resident_process_lease_ref": resident_status.get(
                    "resident_process_lease_ref"
                ),
                "resident_process_identity_continuity_state": resident_status.get(
                    "resident_process_identity_continuity_state"
                ),
            },
            "resident long-term residency evidence must be attached",
        ),
        _json_probe(
            context,
            "queue_e_world_contact_repair_hold_schema_handoff",
            "runtime/state/schema_runner/run_manifest.json",
            _queue_e_world_contact_repair_hold_closed,
            "S09 run manifest must carry Queue E world-contact repair hold handoff",
            extra_refs=[
                "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
                "runtime/state/validation/world_contact_validation.json#repair_hold_required",
                "runtime/state/action/go_nogo_state.json#future_no_go_profile",
            ],
        ),
    ]
    return _criterion(
        "g_initial_life_mechanism_coverage",
        "g. 初步生命机制全层 state/report/receipt 证据闭合",
        probes,
    )


def _criterion(
    criterion_id: str,
    title: str,
    probes: list[dict[str, Any]],
) -> dict[str, Any]:
    failed = [probe for probe in probes if probe["status"] != "passed"]
    return {
        "criterion_id": criterion_id,
        "title": title,
        "status": "closed" if not failed else "blocked",
        "probe_total": len(probes),
        "probe_passed": len(probes) - len(failed),
        "probe_blocked": len(failed),
        "probes": probes,
        "blocked_reasons": [
            f"{criterion_id}.{probe['probe_id']}: {probe['required']}"
            for probe in failed
        ],
    }


def _json_probe(
    context: _AuditContext,
    probe_id: str,
    evidence_ref: str,
    predicate: Callable[[dict[str, Any]], bool],
    required: str,
    *,
    extra_refs: list[str] | None = None,
) -> dict[str, Any]:
    payload = context.load_json(evidence_ref)
    passed = bool(payload) and predicate(payload)
    error = context.json_errors.get(evidence_ref.split("#", 1)[0])
    observed = {
        "schema_version": payload.get("schema_version"),
        "status": payload.get("status"),
    }
    if error:
        observed["error"] = error
    return {
        "probe_id": probe_id,
        "status": "passed" if passed else "blocked",
        "required": required,
        "evidence_refs": [evidence_ref, *(extra_refs or [])],
        "observed": observed,
    }


def _jsonl_probe(
    context: _AuditContext,
    probe_id: str,
    evidence_ref: str,
    predicate: Callable[[int], bool],
    required: str,
) -> dict[str, Any]:
    path = context.path_for_ref(evidence_ref)
    count = _jsonl_count(path)
    passed = predicate(count)
    return {
        "probe_id": probe_id,
        "status": "passed" if passed else "blocked",
        "required": required,
        "evidence_refs": [evidence_ref],
        "observed": {"jsonl_event_count": count, "path": str(path)},
    }


def _value_probe(
    probe_id: str,
    evidence_refs: list[str],
    passed: bool,
    observed: dict[str, Any],
    required: str,
) -> dict[str, Any]:
    return {
        "probe_id": probe_id,
        "status": "passed" if passed else "blocked",
        "required": required,
        "evidence_refs": evidence_refs,
        "observed": observed,
    }


def _closed_or_schema(payload: dict[str, Any]) -> bool:
    if not payload.get("schema_version"):
        return False
    return payload.get("status") in {None, "closed", "active", "ready"}


def _report_status_closed(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "closed"


def _world_contact_validation_repair_hold_closed(payload: dict[str, Any]) -> bool:
    return (
        payload.get("schema_version") == "world_contact_validation_v0"
        and payload.get("repair_hold_required") is True
        and payload.get("confirmation_threshold_bias") == "raised"
        and payload.get("future_no_go_profile_ref")
        == "runtime/state/action/go_nogo_state.json#future_no_go_profile"
        and bool(payload.get("blocked_future_routes"))
        and bool(payload.get("allowed_repair_routes"))
        and bool(payload.get("repair_governance_refs"))
    )


def _queue_e_world_contact_repair_hold_closed(payload: dict[str, Any]) -> bool:
    return (
        payload.get("schema_version")
        in {"validation_rollup_v0", "schema_runner_run_manifest_v0"}
        and payload.get("queue_e_world_contact_repair_hold_required") is True
        and payload.get("queue_e_world_contact_confirmation_threshold_bias") == "raised"
        and payload.get("queue_e_world_contact_future_no_go_profile_ref")
        == "runtime/state/action/go_nogo_state.json#future_no_go_profile"
        and bool(payload.get("queue_e_world_contact_blocked_future_routes"))
        and bool(payload.get("queue_e_world_contact_allowed_repair_routes"))
        and bool(payload.get("queue_e_world_contact_repair_governance_refs"))
    )


def _json_ref_exists(context: _AuditContext, ref: str) -> bool:
    return bool(context.load_json(ref))


def _first_value(payload: dict[str, Any], field_paths: list[str]) -> Any:
    for field_path in field_paths:
        value = _field(payload, field_path)
        if value not in (None, "", [], {}):
            return value
    return None


def _field(payload: dict[str, Any], field_path: str) -> Any:
    value: Any = payload
    for part in field_path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def _jsonl_count(path: Path) -> int:
    try:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    except OSError:
        return 0


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    context: _AuditContext,
    evidence_refs: list[str],
) -> dict[str, Any]:
    evidence_paths = [
        context.path_for_ref(ref)
        for ref in evidence_refs
        if ref.startswith("runtime/")
    ]
    output_paths = [
        context.reports_dir / "live0_acceptance_audit_report.json",
        context.reports_dir / "live0_acceptance_audit_digest.json",
        context.receipts_dir / f"live0_acceptance_audit_{run_id}.json",
    ]
    return {
        "schema_version": "live0_acceptance_audit_receipt_v0",
        "receipt_id": f"live0_acceptance_audit_{run_id}",
        "run_id": run_id,
        "command": "audit-live0",
        "created_at": generated_at,
        "source_doc_refs": SOURCE_DOC_REFS,
        "input_ref_count": len(evidence_refs),
        "input_hashes": {
            str(path): _sha256_if_exists(path)
            for path in evidence_paths
            if path.exists() and path.is_file()
        },
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_paths},
        "report_refs": [
            "runtime/reports/latest/live0_acceptance_audit_report.json",
            "runtime/reports/latest/live0_acceptance_audit_digest.json",
        ],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _unique(values: Any) -> list[Any]:
    seen: set[str] = set()
    result: list[Any] = []
    for value in values:
        marker = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if marker in seen:
            continue
        seen.add(marker)
        result.append(value)
    return result


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
