from __future__ import annotations

import json
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
    signal_media_runtime: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    body_presence_profile: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
    indexes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    engram_index = engram_index or {}
    relationship_memory = relationship_memory or {}
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    indexes = indexes or {}
    body_signal_modulation = _body_signal_write_modulation(
        signal_media_runtime=signal_media_runtime,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        body_presence_profile=body_presence_profile,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )
    stage_policy = _stage_policy_from_body_signal(body_signal_modulation)
    long_term_governance_refs = [
        "runtime/state/memory/state_merge_guard.json#promotion_routes",
        "runtime/state/memory/state_merge_guard.json#quarantine_routes",
        "runtime/state/memory/state_merge_guard.json#repair_routes",
        "runtime/state/memory/state_merge_guard.json#merge_routes",
    ]
    if body_signal_modulation:
        long_term_governance_refs.append("body_signal_write_modulation")
    return {
        "schema_version": "memory_write_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "gate_id": f"memory-write-gate-{run_id}",
        "stage_policy": stage_policy,
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
            "current_signal_profile": body_signal_modulation if body_signal_modulation else None,
        },
        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
        "long_term_governance_refs": long_term_governance_refs,
        "body_signal_write_modulation": (
            body_signal_modulation if body_signal_modulation else None
        ),
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


def project_memory_write_gate_with_signal_body(
    *,
    memory_write_gate: dict[str, Any],
    signal_media_runtime: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    body_presence_profile: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not memory_write_gate:
        return {}
    updated = json.loads(json.dumps(memory_write_gate))
    body_signal_modulation = _body_signal_write_modulation(
        signal_media_runtime=signal_media_runtime,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        body_presence_profile=body_presence_profile,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )
    if not body_signal_modulation:
        return updated

    updated["stage_policy"] = _stage_policy_from_body_signal(body_signal_modulation)
    updated["body_signal_write_modulation"] = body_signal_modulation
    life_support = dict(updated.get("life_support_pressure_update", {}))
    tracked_fields = _dedupe(
        _string_list(life_support.get("tracked_fields"))
        + [
            "fatigue_load",
            "relationship_pressure",
            "repair_drive",
            "unexpected_uncertainty",
            "pain_pressure",
            "dream_residue_load",
            "offline_learning_pressure_level",
            "offline_learning_generation",
        ]
    )
    life_support["tracked_fields"] = tracked_fields
    life_support["current_signal_profile"] = body_signal_modulation
    life_support["high_load_effect"] = body_signal_modulation.get(
        "write_bias",
        "defer_noncritical_memory_commit",
    )
    updated["life_support_pressure_update"] = life_support
    updated["long_term_governance_refs"] = _dedupe(
        _string_list(updated.get("long_term_governance_refs"))
        + ["body_signal_write_modulation"]
    )
    return updated


def _body_signal_write_modulation(
    *,
    signal_media_runtime: dict[str, Any] | None,
    body_resource_budget: dict[str, Any] | None,
    core_affect_vector: dict[str, Any] | None,
    body_presence_profile: dict[str, Any] | None,
    offline_learning_cumulative_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    modulation_vector = signal_media_runtime.get("modulation_vector", {})
    if not isinstance(modulation_vector, dict):
        modulation_vector = {}
    signal_body_profile = signal_media_runtime.get("body_signal_profile", {})
    if not isinstance(signal_body_profile, dict):
        signal_body_profile = {}
    offline_learning_profile = _offline_learning_signal_profile(
        offline_learning_cumulative_profile
    ) or _offline_learning_signal_profile(
        signal_media_runtime.get("offline_learning_cumulative_profile")
    ) or _offline_learning_signal_profile(signal_body_profile)
    body_resource_budget = body_resource_budget or {}
    core_affect_vector = core_affect_vector or {}
    body_presence_profile = body_presence_profile or {}
    if not any(
        [
            signal_media_runtime,
            body_resource_budget,
            core_affect_vector,
            body_presence_profile,
            offline_learning_profile,
        ]
    ):
        return {}

    fatigue_load = _float_signal(
        modulation_vector.get("fatigue_load")
        if modulation_vector.get("fatigue_load") is not None
        else signal_body_profile.get("fatigue_load"),
        default=_fatigue_load_scale(
            body_presence_profile.get("fatigue_load")
            or (body_resource_budget.get("fatigue_state") or {}).get("level")
        ),
    )
    repair_drive = _float_signal(
        modulation_vector.get("repair_drive"),
        default=_repair_drive_signal(
            signal_body_profile.get("repair_drive")
            or body_presence_profile.get("repair_drive")
            or core_affect_vector.get("repair_drive")
            or (body_resource_budget.get("maintenance_pressure") or {}).get(
                "repair_drive"
            )
        ),
    )
    relationship_pressure = _float_signal(
        modulation_vector.get("relationship_pressure"),
        default=_float_signal(
            signal_body_profile.get("relationship_tension")
            or core_affect_vector.get("relationship_tension"),
            default=0.0,
        ),
    )
    unexpected_uncertainty = _float_signal(
        modulation_vector.get("unexpected_uncertainty"),
        default=0.0,
    )
    pain_pressure = _float_signal(
        signal_body_profile.get("pain_pressure")
        if signal_body_profile.get("pain_pressure") is not None
        else core_affect_vector.get("pain_pressure"),
        default=0.0,
    )
    dream_residue_load = _float_signal(
        signal_body_profile.get("dream_residue_load")
        if signal_body_profile.get("dream_residue_load") is not None
        else core_affect_vector.get("dream_residue_load"),
        default=0.0,
    )
    responsibility_weight = _float_signal(
        signal_body_profile.get("responsibility_weight")
        if signal_body_profile.get("responsibility_weight") is not None
        else core_affect_vector.get("responsibility_weight"),
        default=0.0,
    )
    if offline_learning_profile:
        offline_scale = _offline_learning_pressure_scale(
            offline_learning_profile.get("pressure_level")
        )
        generation_scale = min(
            1.0,
            max(
                0.0,
                float(_int_or_zero(offline_learning_profile.get("generation"))) / 4.0,
            ),
        )
        dream_residue_load = max(
            dream_residue_load,
            _clamp(0.24 + offline_scale * 0.38 + generation_scale * 0.12),
        )
        repair_drive = max(
            repair_drive,
            _clamp(
                0.22
                + offline_scale * 0.34
                + (
                    0.16
                    if offline_learning_profile.get(
                        "relationship_reconsolidation_required"
                    )
                    else 0.0
                )
            ),
        )
        unexpected_uncertainty = max(
            unexpected_uncertainty,
            _clamp(0.24 + offline_scale * 0.28),
        )
        if (
            offline_learning_profile.get("attention_target")
            == "relationship_learning_plan"
        ):
            relationship_pressure = max(
                relationship_pressure,
                _clamp(0.26 + offline_scale * 0.38),
            )
    write_bias = signal_body_profile.get("memory_write_bias")
    if not write_bias:
        if fatigue_load >= 0.65 or pain_pressure >= 0.65 or unexpected_uncertainty >= 0.65:
            write_bias = "defer_noncritical_memory_commit"
        elif repair_drive >= 0.7 or responsibility_weight >= 0.7:
            write_bias = "repair_evidence_first"
        elif (
            offline_learning_profile.get("relationship_reconsolidation_required")
            is True
            or offline_learning_profile.get("attention_target")
            == "relationship_learning_plan"
        ):
            write_bias = "relationship_context_first"
        elif relationship_pressure >= 0.65:
            write_bias = "relationship_context_first"
        else:
            write_bias = "baseline_candidate_gate"

    body_signal_refs = _dedupe(
        _string_list(signal_body_profile.get("body_ref_set"))
        + _string_list(signal_body_profile.get("offline_learning_ref_set"))
        + _string_list(offline_learning_profile.get("ref_set"))
        + _string_list(body_presence_profile.get("body_ref_set"))
        + _string_list(
            [
                "runtime/state/signal/signal_media_runtime.json"
                if signal_media_runtime
                else None,
                "runtime/state/body/body_resource_budget.json"
                if body_resource_budget
                else None,
                "runtime/state/body/core_affect_vector.json"
                if core_affect_vector
                else None,
            ]
        )
    )
    adjustments = []
    if fatigue_load >= 0.65:
        adjustments.append("defer_low_salience_write_until_recovery")
    if unexpected_uncertainty >= 0.65:
        adjustments.append("raise_source_evidence_threshold")
    if pain_pressure >= 0.65:
        adjustments.append("protect_pain_trace_from_fast_overwrite")
    if repair_drive >= 0.7 or responsibility_weight >= 0.7:
        adjustments.append("prioritize_repair_obligation_memory")
    if dream_residue_load >= 0.55:
        adjustments.append("route_residue_to_dream_replay_before_promotion")
    if offline_learning_profile.get("pressure_level") in {"elevated", "urgent"}:
        adjustments.append("preserve_offline_learning_refs_for_reconsolidation")
    if (
        offline_learning_profile.get("relationship_reconsolidation_required") is True
        or offline_learning_profile.get("attention_target")
        == "relationship_learning_plan"
    ):
        adjustments.append("route_offline_learning_to_relationship_replay")

    return {
        "schema_version": "body_signal_memory_gate_profile_v0",
        "fatigue_load": fatigue_load,
        "repair_drive": repair_drive,
        "relationship_pressure": relationship_pressure,
        "unexpected_uncertainty": unexpected_uncertainty,
        "pain_pressure": pain_pressure,
        "dream_residue_load": dream_residue_load,
        "offline_learning_generation": offline_learning_profile.get("generation"),
        "offline_learning_pressure_level": offline_learning_profile.get(
            "pressure_level"
        ),
        "offline_learning_attention_target": offline_learning_profile.get(
            "attention_target"
        ),
        "offline_learning_integration_mode": offline_learning_profile.get(
            "integration_mode"
        ),
        "offline_learning_relationship_reconsolidation_required": (
            offline_learning_profile.get("relationship_reconsolidation_required")
        ),
        "responsibility_weight": responsibility_weight,
        "write_bias": write_bias,
        "candidate_gate_adjustments": adjustments,
        "body_signal_refs": body_signal_refs,
        "body_signal_ref_count": len(body_signal_refs),
    }


def _stage_policy_from_body_signal(body_signal_modulation: dict[str, Any]) -> str:
    if not body_signal_modulation:
        return "candidate_first_fail_closed"
    write_bias = str(body_signal_modulation.get("write_bias", ""))
    if write_bias == "defer_noncritical_memory_commit":
        return "candidate_first_body_signal_guarded"
    if write_bias == "repair_evidence_first":
        return "candidate_first_repair_guarded"
    if write_bias == "relationship_context_first":
        return "candidate_first_relationship_guarded"
    return "candidate_first_fail_closed"


def _offline_learning_signal_profile(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    ref_set = _dedupe(
        _string_list(value.get("ref_set"))
        + _string_list(value.get("offline_learning_cumulative_ref_set"))
        + _string_list(value.get("offline_learning_ref_set"))
    )
    generation = _int_or_zero(
        value.get("generation")
        or value.get("offline_learning_cumulative_generation")
        or value.get("offline_learning_generation")
    )
    pressure_level = str(
        value.get("pressure_level")
        or value.get("offline_learning_cumulative_pressure_level")
        or value.get("offline_learning_pressure_level")
        or "quiet"
    )
    attention_target = str(
        value.get("attention_target")
        or value.get("offline_learning_cumulative_attention_target")
        or value.get("offline_learning_attention_target")
        or "baseline_offline_learning_maintenance"
    )
    if not any([ref_set, generation, pressure_level != "quiet"]):
        return {}
    return {
        "schema_version": "offline_learning_body_signal_profile_v0",
        "generation": generation,
        "pressure_level": pressure_level,
        "attention_target": attention_target,
        "integration_mode": str(
            value.get("integration_mode")
            or value.get("offline_learning_cumulative_integration_mode")
            or value.get("offline_learning_integration_mode")
            or "baseline_offline_learning_maintenance"
        ),
        "relationship_reconsolidation_required": bool(
            value.get("relationship_reconsolidation_required")
            or value.get(
                "offline_learning_cumulative_relationship_reconsolidation_required"
            )
            or value.get("offline_learning_relationship_reconsolidation_required")
        ),
        "ref_set": ref_set,
    }


def _offline_learning_pressure_scale(value: Any) -> float:
    return {
        "quiet": 0.0,
        "present": 0.35,
        "elevated": 0.72,
        "urgent": 1.0,
    }.get(str(value or "quiet"), 0.0)


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _fatigue_load_scale(value: Any) -> float:
    if isinstance(value, (int, float)):
        return _clamp(float(value))
    text = str(value or "").lower()
    if not text:
        return 0.0
    if text in {"critical", "exhausted", "offline_ready"}:
        return 0.92
    if text in {"high_load", "high", "overloaded"}:
        return 0.78
    if text in {"elevated_guard", "elevated", "guarded"}:
        return 0.62
    if text in {"managed_low_noise", "managed", "low"}:
        return 0.26
    return 0.34


def _repair_drive_signal(value: Any) -> float:
    if isinstance(value, (int, float)):
        return _clamp(float(value))
    text = str(value or "").lower()
    if text in {"active", "high", "urgent", "repair_required"}:
        return 0.76
    if text in {"present", "elevated", "guarded"}:
        return 0.58
    if text in {"quiet", "none", "low"}:
        return 0.16
    return 0.0


def _float_signal(value: Any, *, default: float) -> float:
    if isinstance(value, (int, float)):
        return _clamp(float(value))
    try:
        return _clamp(float(str(value)))
    except (TypeError, ValueError):
        return default


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, tuple):
        return [str(item) for item in value if item]
    if isinstance(value, str) and value:
        return [value]
    return []


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
