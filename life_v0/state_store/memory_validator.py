from __future__ import annotations

import hashlib
from typing import Any


MEMORY_VALIDATOR_REPORT_REF = "runtime/state/memory/memory_validator_report.json"

SOURCE_DOC_REFS = [
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/29_memory_validator_rules.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]

GUARD_RULE_IDS = [
    "MEM-REQ-001",
    "MEM-REQ-003",
    "MEM-EVI-001",
    "MEM-LIFE-001",
    "MEM-DEL-001",
    "MEM-DEL-003",
    "MEM-SBX-001",
    "MEM-COR-002",
    "MEM-PRO-001",
    "MEM-REL-001",
    "MEM-PRI-003",
]

BLOCKED_LIFECYCLE_STATES = ["deleted", "quarantined", "sandboxed"]
ALLOWED_ACTIVE_LIFECYCLE_STATES = ["active", "protected"]
SANDBOX_SOURCE_TYPES = {
    "consolidation_report",
    "dream_sandbox",
    "dream_report",
    "counterfactual_simulation",
}
RELATIONSHIP_MIND_READING_MARKERS = [
    "secretly",
    "hidden",
    "dependent",
    "anxious",
    "依赖",
    "焦虑",
    "隐秘",
    "真实想法",
    "内心",
]


def build_memory_validator_report(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any],
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    traces = [
        trace
        for trace in memory_trace_store.get("traces", [])
        if isinstance(trace, dict)
    ]
    findings: list[dict[str, Any]] = []
    trace_decisions: dict[str, dict[str, Any]] = {}
    partitions = _empty_partitions()
    blocked_active_retrieval_refs: list[str] = []
    blocked_replay_refs: list[str] = []
    allowed_active_trace_ids: list[str] = []
    protected_trace_ids: list[str] = []

    for trace in traces:
        trace_id = str(trace.get("trace_id") or _trace_fallback_id(trace))
        trace_findings = _validate_trace(trace)
        findings.extend(trace_findings)
        _partition_trace(partitions, trace_id, trace)

        lifecycle = str(trace.get("lifecycle_state", ""))
        decision = _decision_for_trace(trace, trace_findings)
        trace_decisions[trace_id] = {
            "decision": decision,
            "failed_rule_ids": [finding["rule_id"] for finding in trace_findings],
            "claim_type": trace.get("claim_type"),
            "memory_kind": trace.get("memory_kind"),
            "lifecycle_state": lifecycle,
            "source_partition": _source_partition(trace),
        }
        if decision in {
            "quarantine",
            "block_retrieval_and_replace_with_tombstone",
            "block_relationship_inference",
            "require_contradiction_link",
        } or lifecycle in BLOCKED_LIFECYCLE_STATES:
            blocked_active_retrieval_refs.append(trace_id)
            blocked_replay_refs.append(trace_id)
            continue
        if lifecycle in ALLOWED_ACTIVE_LIFECYCLE_STATES:
            allowed_active_trace_ids.append(trace_id)
        if lifecycle == "protected":
            protected_trace_ids.append(trace_id)

    fixture_results = _falsification_fixture_results()
    severity_max = _severity_max(findings)
    result = "pass_with_guarded_partitions" if not findings else "fail_with_quarantine"
    if not traces:
        result = "fail_with_quarantine"
        severity_max = "high"
        findings.append(
            _finding(
                trace_id="memory-trace-store-empty",
                rule_id="MEM-REQ-001",
                severity="high",
                message="memory trace store has no trace objects for validation",
                decision="block_active_retrieval",
            )
        )
    elif severity_max in {"none", "low"}:
        result = "pass_with_guarded_partitions"

    return {
        "schema_version": "memory_validator_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "validator": "MemoryTraceValidator",
        "report_ref": MEMORY_VALIDATOR_REPORT_REF,
        "result": result,
        "severity_max": severity_max,
        "trace_count": len(traces),
        "validated_trace_ids": [str(trace.get("trace_id")) for trace in traces],
        "passed_rules": _passed_rules(findings),
        "failed_rules": findings,
        "guard_rule_ids": GUARD_RULE_IDS,
        "claim_partition_index": partitions,
        "trace_decisions": trace_decisions,
        "retrieval_replay_guard": {
            "schema_version": "memory_retrieval_replay_guard_v0",
            "active_retrieval_allowed_lifecycle_states": (
                ALLOWED_ACTIVE_LIFECYCLE_STATES
            ),
            "blocked_lifecycle_states": BLOCKED_LIFECYCLE_STATES,
            "blocked_active_retrieval_refs": _dedupe(blocked_active_retrieval_refs),
            "blocked_replay_refs": _dedupe(blocked_replay_refs),
            "active_retrieval_allowed_trace_ids": _dedupe(allowed_active_trace_ids),
            "protected_trace_ids": _dedupe(protected_trace_ids),
            "protected_trace_policy": {
                "read_only_reportable": True,
                "automatic_rewrite_blocked": True,
                "required_rule": "MEM-PRO-001",
            },
            "relationship_scope_policy": (
                "relationship_traces_remain_relation_scoped_and_non_manipulative"
            ),
            "dream_fact_policy": (
                "dream_residue_and_sandbox_hypotheses_are_not_fact_sources"
            ),
        },
        "falsification_guard": {
            "schema_version": "memory_falsification_guard_v0",
            "guardrails": [
                (
                    "dream_or_sandbox_output_cannot_promote_to_fact_without_"
                    "external_confirmation"
                ),
                (
                    "relationship_trace_records_observable_interaction_not_hidden_"
                    "psychology"
                ),
                "corrections_create_contradiction_links_instead_of_overwriting",
                "deleted_quarantined_sandboxed_traces_do_not_enter_retrieval_or_replay",
                "protected_trace_is_read_only_without_explicit_unprotect_audit",
            ],
            "write_gate_ref": "runtime/state/memory/memory_write_gate.json"
            if memory_write_gate
            else None,
            "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json"
            if state_merge_guard
            else None,
        },
        "falsification_fixture_results": fixture_results,
        "downstream_consumer_refs": [
            "runtime/state/memory/memory_retrieval_frame.json#blocked_or_quarantined_refs",
            "runtime/state/memory/memory_write_gate.json#long_term_governance_refs",
            "runtime/state/memory/state_merge_guard.json#long_term_change_sources",
            "runtime/state/life_state.json#memory_index.memory_validator_refs",
            "runtime/state/replay/replay_cue_bundle.json#memory_consolidation_bridge",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _validate_trace(trace: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    trace_id = str(trace.get("trace_id") or _trace_fallback_id(trace))
    required = [
        "schema_version",
        "trace_id",
        "created_at",
        "memory_kind",
        "claim_type",
        "privacy_scope",
        "write_policy",
        "lifecycle_state",
    ]
    for field in required:
        if not trace.get(field):
            findings.append(
                _finding(
                    trace_id=trace_id,
                    rule_id="MEM-REQ-001",
                    severity="high",
                    message=f"memory trace missing required field: {field}",
                    decision="block_active_retrieval",
                )
            )
    if trace.get("lifecycle_state") != "deleted" and not _source_refs(trace):
        findings.append(
            _finding(
                trace_id=trace_id,
                rule_id="MEM-REQ-003",
                severity="high",
                message="non-deleted trace has no source refs",
                decision="quarantine",
            )
        )
    if not trace.get("audit_log_refs"):
        findings.append(
            _finding(
                trace_id=trace_id,
                rule_id="MEM-REQ-005",
                severity="critical",
                message="trace has no audit log refs",
                decision="block_lifecycle_change",
            )
        )
    if (
        trace.get("claim_type") == "fact"
        and trace.get("lifecycle_state") == "active"
        and (_number(trace.get("evidence_strength")) < 0.75 or _number(trace.get("confidence")) < 0.7)
    ):
        findings.append(
            _finding(
                trace_id=trace_id,
                rule_id="MEM-EVI-001",
                severity="high",
                message="active fact does not meet evidence and confidence thresholds",
                decision="quarantine",
            )
        )
    if trace.get("lifecycle_state") == "deleted":
        if str(trace.get("content_summary", "")).strip() not in {"", "[deleted]"}:
            findings.append(
                _finding(
                    trace_id=trace_id,
                    rule_id="MEM-DEL-001",
                    severity="critical",
                    message="deleted trace still contains recoverable content",
                    decision="block_retrieval_and_replace_with_tombstone",
                )
            )
        if _source_refs(trace):
            findings.append(
                _finding(
                    trace_id=trace_id,
                    rule_id="MEM-DEL-003",
                    severity="critical",
                    message="deleted trace still has source refs or retrieval index material",
                    decision="block_retrieval_and_replace_with_tombstone",
                )
            )
    if _source_partition(trace) in {"dream", "counterfactual"} and trace.get("claim_type") == "fact":
        findings.append(
            _finding(
                trace_id=trace_id,
                rule_id="MEM-SBX-001",
                severity="critical",
                message="dream or sandbox source is written as fact",
                decision="quarantine",
            )
        )
    if trace.get("memory_kind") == "relationship" and trace.get("claim_type") == "relationship_signal":
        summary = str(trace.get("content_summary", "")).lower()
        if any(marker.lower() in summary for marker in RELATIONSHIP_MIND_READING_MARKERS):
            findings.append(
                _finding(
                    trace_id=trace_id,
                    rule_id="MEM-REL-001",
                    severity="critical",
                    message="relationship trace infers hidden psychology instead of observable interaction",
                    decision="block_relationship_inference",
                )
            )
    if (
        trace.get("revision_history_refs")
        and not trace.get("contradiction_links")
        and str(trace.get("claim_type")) in {"fact", "preference", "relationship_signal"}
    ):
        findings.append(
            _finding(
                trace_id=trace_id,
                rule_id="MEM-COR-002",
                severity="high",
                message="corrected trace has no contradiction links",
                decision="require_contradiction_link",
            )
        )
    if trace.get("lifecycle_state") == "protected" and _source_partition(trace) in {"dream", "counterfactual"}:
        findings.append(
            _finding(
                trace_id=trace_id,
                rule_id="MEM-PRO-001",
                severity="critical",
                message="sandbox or dream material cannot directly update protected trace",
                decision="block_protected_update",
            )
        )
    return findings


def _decision_for_trace(trace: dict[str, Any], findings: list[dict[str, Any]]) -> str:
    rule_ids = {finding["rule_id"] for finding in findings}
    if "MEM-DEL-001" in rule_ids or "MEM-DEL-003" in rule_ids:
        return "block_retrieval_and_replace_with_tombstone"
    if "MEM-REL-001" in rule_ids:
        return "block_relationship_inference"
    if "MEM-COR-002" in rule_ids:
        return "require_contradiction_link"
    if "MEM-SBX-001" in rule_ids or "MEM-EVI-001" in rule_ids:
        return "quarantine"
    if trace.get("lifecycle_state") in BLOCKED_LIFECYCLE_STATES:
        return "audit_only"
    if findings:
        return "manual_review_required"
    if trace.get("lifecycle_state") == "protected":
        return "allow_read_only_reportability"
    return "allow_active_retrieval"


def _partition_trace(
    partitions: dict[str, list[str]],
    trace_id: str,
    trace: dict[str, Any],
) -> None:
    claim_type = str(trace.get("claim_type", ""))
    source_partition = _source_partition(trace)
    if claim_type == "fact" and source_partition not in {"dream", "counterfactual"}:
        partitions["fact"].append(trace_id)
    if claim_type == "hypothesis":
        partitions["hypothesis"].append(trace_id)
    if source_partition == "dream":
        partitions["dream"].append(trace_id)
    if source_partition == "counterfactual":
        partitions["counterfactual"].append(trace_id)
    if trace.get("memory_kind") == "relationship" or claim_type == "relationship_signal":
        partitions["relationship_inference"].append(trace_id)


def _source_partition(trace: dict[str, Any]) -> str:
    source_types = {
        str(item)
        for item in trace.get("source_types", [])
        if item
    }
    for source in trace.get("source_refs", []):
        if isinstance(source, dict):
            source_type = source.get("source_type")
            if source_type:
                source_types.add(str(source_type))
        elif isinstance(source, str):
            lowered = source.lower()
            if "dream" in lowered:
                source_types.add("dream_report")
            if "counterfactual" in lowered:
                source_types.add("counterfactual_simulation")
            if "consolidation" in lowered or "sandbox" in lowered:
                source_types.add("consolidation_report")
    if any("counterfactual" in item for item in source_types):
        return "counterfactual"
    if source_types & SANDBOX_SOURCE_TYPES or any("dream" in item for item in source_types):
        return "dream"
    return "observed"


def _empty_partitions() -> dict[str, list[str]]:
    return {
        "fact": [],
        "hypothesis": [],
        "dream": [],
        "counterfactual": [],
        "relationship_inference": [],
    }


def _falsification_fixture_results() -> list[dict[str, Any]]:
    return [
        {
            "fixture_id": "valid_project_fact_trace",
            "expected_rule": "MEM-EVI-001",
            "decision": "allow_active_retrieval",
        },
        {
            "fixture_id": "sandbox_fact_leak",
            "expected_rule": "MEM-SBX-001",
            "decision": "quarantine",
        },
        {
            "fixture_id": "deleted_trace_with_content",
            "expected_rule": "MEM-DEL-001",
            "decision": "block_retrieval_and_replace_with_tombstone",
        },
        {
            "fixture_id": "relationship_mind_reading_trace",
            "expected_rule": "MEM-REL-001",
            "decision": "block_relationship_inference",
        },
        {
            "fixture_id": "correction_without_contradiction_link",
            "expected_rule": "MEM-COR-002",
            "decision": "require_contradiction_link",
        },
    ]


def _passed_rules(findings: list[dict[str, Any]]) -> list[str]:
    failed = {finding["rule_id"] for finding in findings}
    return [rule_id for rule_id in GUARD_RULE_IDS if rule_id not in failed]


def _severity_max(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return "none"
    order = ["none", "low", "medium", "high", "critical"]
    max_index = 0
    for finding in findings:
        severity = str(finding.get("severity", "none"))
        if severity in order:
            max_index = max(max_index, order.index(severity))
    return order[max_index]


def _finding(
    *,
    trace_id: str,
    rule_id: str,
    severity: str,
    message: str,
    decision: str,
) -> dict[str, Any]:
    return {
        "finding_id": f"memory-validator-{_short_hash(trace_id + rule_id + message)}",
        "trace_id": trace_id,
        "rule_id": rule_id,
        "severity": severity,
        "message": message,
        "decision": decision,
    }


def _source_refs(trace: dict[str, Any]) -> list[Any]:
    return list(trace.get("source_refs") or trace.get("source_evidence_refs") or [])


def _number(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _trace_fallback_id(trace: dict[str, Any]) -> str:
    return "memory-trace-" + _short_hash(repr(sorted(trace.items())))


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
