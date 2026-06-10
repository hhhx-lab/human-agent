from __future__ import annotations

import json
from typing import Any


SOURCE_DOC_REFS = [
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/29_memory_validator_rules.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/48_state_store_migration_and_integrity_plan.md",
    "docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md",
    "docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md",
]


def build_state_merge_guard(
    *,
    run_id: str,
    generated_at: str,
    memory_write_gate: dict[str, Any],
    relationship_memory: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    indexes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    relationship_memory = relationship_memory or {}
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    indexes = indexes or {}
    blocked_indexes = list(memory_write_gate.get("quarantine_route", {}).get("blocked_indexes", []))
    return {
        "schema_version": "state_merge_guard_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "guard_id": f"state-merge-guard-{run_id}",
        "memory_write_gate_ref": "runtime/state/memory/memory_write_gate.json",
        "stage_policy": "long_term_merge_fail_closed",
        "promotion_routes": [
            {
                "route_id": "candidate_to_active_memory",
                "from_lifecycle": "candidate",
                "to_lifecycle": "active",
                "requires": [
                    "validation_envelope_passed",
                    "audit_event_created",
                    "source_refs_intact",
                ],
                "index_update_refs": _index_refs(indexes, exclude=blocked_indexes),
            },
            {
                "route_id": "candidate_to_protected_memory",
                "from_lifecycle": "candidate",
                "to_lifecycle": "protected",
                "requires": [
                    "identity_or_relationship_anchor",
                    "manual_review_before_change",
                    "protected_update_block_enabled",
                ],
                "index_update_refs": ["runtime/state/indexes/memory_index.json"],
            },
        ],
        "quarantine_routes": [
            {
                "route_id": "missing_source_or_conflict_quarantine",
                "to_lifecycle": "quarantined",
                "blocked_indexes": blocked_indexes,
                "release_condition": memory_write_gate.get("quarantine_route", {}).get(
                    "release_condition",
                    "repair_or_new_evidence_required",
                ),
                "audit_ref": "runtime/state/memory/memory_write_gate.json#audit_event_template",
            }
        ],
        "repair_routes": [
            {
                "route_id": "responsibility_repair_before_promotion",
                "responsibility_event_refs": _dedupe(
                    list(commitment_truth_state.get("responsibility_event_refs", []))
                    + list(responsibility_ledger.get("responsibility_event_refs", []))
                ),
                "repair_obligation_refs": _dedupe(
                    list(commitment_truth_state.get("repair_required_refs", []))
                    + list(responsibility_ledger.get("repair_obligations", []))
                ),
                "repair_gate": "repair_obligation_tracking",
            }
        ],
        "merge_routes": [
            {
                "route_id": "relationship_memory_merge",
                "target_ref": "runtime/state/memory/relationship_memory.json",
                "source_refs": _dedupe(
                    list(relationship_memory.get("shared_memory_refs", []))
                    + list(relationship_memory.get("repair_history_refs", []))
                    + list(relationship_memory.get("responsibility_event_refs", []))
                ),
                "merge_policy": "append_with_dedupe_and_audit",
            },
            {
                "route_id": "life_state_continuity_merge",
                "target_ref": "runtime/state/life_state.json",
                "source_refs": [
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
                "merge_policy": "record_guard_ref_before_long_term_promotion",
            },
        ],
        "long_term_change_sources": {
            "prediction_error_resolution_refs": [
                "runtime/state/prediction/prediction_error_field.json#error_events"
            ],
            "offline_learning_writeback_refs": [
                "runtime/state/growth/belief_learning_plan.json",
                "runtime/state/growth/relationship_learning_plan.json",
            ],
            "relationship_memory_ref": "runtime/state/memory/relationship_memory.json",
        },
        "slow_variable_update_policy": {
            "target_ref": "runtime/state/self/self_model.json#trait_slow_variables",
            "allowed_effects": [
                "trust_persistence_adjustment",
                "repair_seriousness_adjustment",
                "continuity_drive_adjustment",
            ],
            "requires_merge_audit": True,
        },
        "downstream_refs": [
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/life_state.json",
            "runtime/state/self/self_model.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_state_merge_guard_with_relationship_memory(
    *,
    state_merge_guard: dict[str, Any],
    relationship_memory: dict[str, Any],
) -> dict[str, Any]:
    if not state_merge_guard:
        return {}
    relationship_memory = relationship_memory or {}
    updated = json.loads(json.dumps(state_merge_guard))
    change_sources = dict(updated.get("long_term_change_sources", {}))
    relationship_change_sources = relationship_memory.get("long_term_change_sources", {})

    for field in [
        "prediction_error_resolution_refs",
        "offline_learning_writeback_refs",
        "repair_responsibility_refs",
        "offline_learning_cumulative_refs",
        "queue_e_repair_modulation_refs",
    ]:
        change_sources[field] = _dedupe(
            list(change_sources.get(field, []))
            + list(relationship_change_sources.get(field, []))
        )

    change_sources["relationship_memory_ref"] = "runtime/state/memory/relationship_memory.json"
    change_sources["relationship_memory_offline_refs"] = _dedupe(
        list(change_sources.get("relationship_memory_offline_refs", []))
        + list(relationship_memory.get("offline_learning_refs", []))
        + list(relationship_memory.get("offline_learning_cumulative_refs", []))
    )
    change_sources["relationship_memory_repair_refs"] = _dedupe(
        list(change_sources.get("relationship_memory_repair_refs", []))
        + list(relationship_memory.get("repair_history_refs", []))
        + list(relationship_memory.get("queue_e_repair_refs", []))
    )
    updated["long_term_change_sources"] = change_sources
    updated["last_projected_from_relationship_memory_ref"] = (
        "runtime/state/memory/relationship_memory.json"
    )

    merge_routes = list(updated.get("merge_routes", []))
    relationship_source_refs = _dedupe(
        list(relationship_memory.get("shared_memory_refs", []))
        + list(relationship_memory.get("repair_history_refs", []))
        + list(relationship_memory.get("responsibility_event_refs", []))
        + list(relationship_memory.get("timeline_refs", []))
        + list(relationship_memory.get("offline_learning_refs", []))
        + list(relationship_memory.get("queue_e_repair_refs", []))
    )
    for route in merge_routes:
        if route.get("route_id") != "relationship_memory_merge":
            continue
        route["source_refs"] = _dedupe(
            list(route.get("source_refs", [])) + relationship_source_refs
        )
        route["source_change_refs"] = relationship_source_refs
        route["source_change_count"] = len(relationship_source_refs)
    updated["merge_routes"] = merge_routes
    updated["downstream_refs"] = _dedupe(
        list(updated.get("downstream_refs", []))
        + [
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/life_state.json",
            "runtime/state/self/self_model.json",
        ]
    )
    return updated


def _index_refs(indexes: dict[str, dict[str, Any]], *, exclude: list[str]) -> list[str]:
    refs: list[str] = []
    for filename in indexes:
        index_name = filename.removesuffix(".json")
        if index_name in exclude:
            continue
        refs.append(f"runtime/state/indexes/{filename}")
    return refs


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
