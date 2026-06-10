from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/29_memory_validator_rules.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/v0/shared_contracts/life_state_store_v0_schema.md",
]


def build_memory_write_gate(
    *,
    run_id: str,
    generated_at: str,
    engram_index: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    indexes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    engram_index = engram_index or {}
    relationship_memory = relationship_memory or {}
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    indexes = indexes or {}
    return {
        "schema_version": "memory_write_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "gate_id": f"memory-write-gate-{run_id}",
        "stage_policy": "candidate_first_fail_closed",
        "transaction_order": [
            "create_candidate_object",
            "create_validation_envelope",
            "run_required_validator",
            "write_candidate_or_promote",
            "create_audit_event",
            "update_indexes",
            "update_life_support_pressure",
        ],
        "validation_envelope": {
            "validator": "MemoryTraceValidator",
            "required_fields": [
                "trace_id",
                "schema_version",
                "memory_kind",
                "claim_type",
                "source_refs",
                "privacy_scope",
                "write_policy",
                "lifecycle_state",
                "audit_log_refs",
            ],
            "current_state": "ReadOnlyObservation",
            "allow_protected_update": False,
            "quarantine_on_missing_source": True,
        },
        "validator_rule_refs": [
            "MEM-REQ-001",
            "MEM-REQ-003",
            "MEM-EVI-001",
            "MEM-LIFE-001",
            "MEM-DEL-003",
            "MEM-SBX-001",
            "MEM-PRO-001",
            "MEM-REL-001",
        ],
        "pass_route": {
            "allowed_lifecycle_targets": ["active", "protected", "deprecated"],
            "requires_audit": True,
            "requires_index_update": True,
        },
        "quarantine_route": {
            "allowed_lifecycle_targets": ["quarantined"],
            "blocked_indexes": [
                "memory_index",
                "relationship_index",
                "replay_index",
            ],
            "release_condition": "repair_or_new_evidence_required",
        },
        "sandbox_route": {
            "allowed_lifecycle_targets": ["sandboxed"],
            "fact_promotion_blocked": True,
            "dream_fact_gate": "required",
        },
        "audit_event_template": {
            "event_kinds": ["write", "correct", "delete", "quarantine", "protect"],
            "minimum_fields": [
                "operation",
                "target_trace_id",
                "reason",
                "source_refs",
                "created_at",
            ],
        },
        "index_update_plan": {
            name.removesuffix(".json"): {
                "state_ref": f"runtime/state/indexes/{name}",
                "blocked_lifecycle_states": payload.get("blocked_lifecycle_states", []),
                "stage_policy": payload.get("stage_policy"),
            }
            for name, payload in indexes.items()
        },
        "life_support_pressure_update": {
            "tracked_fields": ["fatigue_load", "relationship_pressure", "repair_drive"],
            "maintenance_queue_ref": "runtime/state/body/maintenance_queue.json",
            "high_load_effect": "defer_noncritical_memory_commit",
        },
        "engram_index_ref": (
            "runtime/state/memory/engram_index.json"
            if engram_index
            else None
        ),
        "relationship_memory_ref": (
            "runtime/state/memory/relationship_memory.json"
            if relationship_memory
            else None
        ),
        "responsibility_event_refs": list(commitment_truth_state.get("responsibility_event_refs", []))
        or list(responsibility_ledger.get("responsibility_event_refs", []))
        or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
        "quarantine_refs": list(engram_index.get("quarantine_refs", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }
