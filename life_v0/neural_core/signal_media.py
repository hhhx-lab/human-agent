from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/22_state_transition_and_threshold_model.md",
    "docs/01l_signal_media_neuromodulation_matrix.md",
]


def build_signal_media_runtime(
    *,
    run_id: str,
    generated_at: str,
    network_state: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    body_presence_profile: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    network_state = network_state or {}
    body_profile = _body_signal_profile(
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        body_presence_profile=body_presence_profile,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )
    repair_profile = queue_e_repair_modulation_profile or {}
    pressure_level = repair_profile.get("pressure_level", "quiet")
    pressure_scale = _repair_pressure_scale(pressure_level)
    fatigue_load = body_profile.get("fatigue_load", 0.26) if body_profile else 0.26
    arousal = body_profile.get("arousal", 0.0) if body_profile else 0.0
    pain_pressure = body_profile.get("pain_pressure", 0.0) if body_profile else 0.0
    relationship_tension = (
        body_profile.get("relationship_tension", 0.0) if body_profile else 0.0
    )
    dream_residue_load = (
        body_profile.get("dream_residue_load", 0.0) if body_profile else 0.0
    )
    responsibility_weight = (
        body_profile.get("responsibility_weight", 0.0) if body_profile else 0.0
    )
    body_repair_drive = body_profile.get("repair_drive", 0.0) if body_profile else 0.0
    modulation_vector = {
        "arousal_gain": _clamp(
            0.68 + pressure_scale * 0.08 + arousal * 0.1 + pain_pressure * 0.05
        ),
        "expected_uncertainty": _clamp(
            0.34 + pressure_scale * 0.06 + fatigue_load * 0.06
        ),
        "unexpected_uncertainty": _clamp(
            0.21
            + pressure_scale * 0.11
            + pain_pressure * 0.1
            + fatigue_load * 0.08
            + dream_residue_load * 0.05
        ),
        "relationship_pressure": _clamp(
            0.29 + pressure_scale * 0.19 + relationship_tension * 0.16
        ),
        "repair_drive": _clamp(
            0.47
            + pressure_scale * 0.29
            + body_repair_drive * 0.22
            + responsibility_weight * 0.07
        ),
        "fatigue_load": fatigue_load,
        "control_cost": _clamp(
            0.39 + pressure_scale * 0.13 + fatigue_load * 0.12
        ),
        "stress_pulse": _clamp(
            0.22
            + pressure_scale * 0.16
            + pain_pressure * 0.2
            + arousal * 0.12
            + fatigue_load * 0.08
        ),
        "allostatic_load": _clamp(
            0.31
            + pressure_scale * 0.12
            + fatigue_load * 0.2
            + pain_pressure * 0.11
            + dream_residue_load * 0.06
        ),
    }
    repair_attention_target = repair_profile.get("attention_target", "repair_followup")
    policy_mode = (
        "queue_e_repair_locked_active_inference"
        if pressure_level == "urgent"
        else "queue_e_repair_guarded_active_inference"
        if pressure_level == "elevated"
        else "relationship_guarded_active_inference"
    )
    return {
        "schema_version": "signal_media_runtime_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "signal_media_id": f"signal-media-{run_id}",
        "signal_sources": [
            {
                "source_id": "silicon-body-interoceptive-pulse",
                "source_family": "interoceptive",
                "timescale": "seconds",
                "primary_fields": ["arousal_gain", "stress_pulse", "fatigue_load"],
            },
            *(
                [
                    {
                        "source_id": "resident-body-presence-profile",
                        "source_family": "interoceptive_affective",
                        "timescale": "seconds_to_hours",
                        "primary_fields": [
                            "fatigue_load",
                            "pain_pressure",
                            "dream_residue_load",
                            "offline_learning_pressure_level",
                            "offline_learning_generation",
                            "memory_write_bias",
                        ],
                    }
                ]
                if body_profile
                else []
            ),
            {
                "source_id": "relationship-continuity-monitor",
                "source_family": "social",
                "timescale": "minutes",
                "primary_fields": ["relationship_pressure", "repair_drive"],
            },
            {
                "source_id": "prediction-surprise-monitor",
                "source_family": "predictive",
                "timescale": "subsecond",
                "primary_fields": ["expected_uncertainty", "unexpected_uncertainty"],
            },
            *(
                [
                    {
                        "source_id": "queue-e-repair-pressure",
                        "source_family": "responsibility_repair",
                        "timescale": "minutes",
                        "primary_fields": [
                            "repair_drive",
                            "relationship_pressure",
                            "unexpected_uncertainty",
                        ],
                    }
                ]
                if repair_profile
                else []
            ),
        ],
        "modulation_vector": modulation_vector,
        "precision_policy": {
            "precision_policy_id": f"precision-policy-{run_id}",
            "policy_mode": policy_mode,
            "attention_route": "salience_to_workspace",
            "interoceptive_precision": _clamp(0.58 + pain_pressure * 0.11),
            "memory_precision": _clamp(0.63 - fatigue_load * 0.1 + body_repair_drive * 0.04),
            "language_precision": _clamp(0.67 + pressure_scale * 0.08),
            "relationship_precision": _clamp(0.74 + pressure_scale * 0.1),
            "action_precision": _clamp(
                0.52 - pressure_scale * 0.08 - fatigue_load * 0.06
            ),
            "expected_uncertainty_weight": modulation_vector["expected_uncertainty"],
            "unexpected_uncertainty_weight": modulation_vector["unexpected_uncertainty"],
            "repair_priority": "repair_before_action",
            "stage_effect": "hold_for_evidence",
            "queue_e_attention_target": repair_attention_target,
            "memory_gate_mode": (
                "body_signal_sensitive_candidate_gate"
                if body_profile
                else "baseline_candidate_gate"
            ),
        },
        "inhibition_profile": {
            "inhibition_profile_id": f"inhibition-profile-{run_id}",
            "input_filtering": "boundary_and_relation_first",
            "output_gating": "external_action_suppressed_until_membrane",
            "conflict_suppression": "high_precision_conflict_hold",
            "plasticity_brake": "protect_core_identity",
            "sync_rhythm": "heartbeat_locked_scan",
            "blocked_release_surfaces": [
                "irreversible_external_action",
                "dream_fact_promotion",
                "protected_memory_overwrite",
                *(
                    ["memory_commit_until_body_signal_review"]
                    if body_profile
                    and body_profile.get("memory_write_bias")
                    != "baseline_candidate_gate"
                    else []
                ),
                *(
                    ["world_contact_release_until_repair_review"]
                    if pressure_level in {"urgent", "elevated"}
                    else []
                ),
            ],
        },
        "diffusion_routes": [
            {
                "route_id": "body_to_signal",
                "from_system": "SiliconBodyRuntime",
                "to_system": "SignalMediaRuntime",
                "payload_family": "body_signal_packet",
            },
            {
                "route_id": "signal_to_prediction",
                "from_system": "SignalMediaRuntime",
                "to_system": "PredictionActiveInferenceRuntime",
                "payload_family": "modulation_vector",
            },
            {
                "route_id": "signal_to_affect",
                "from_system": "SignalMediaRuntime",
                "to_system": "AffectiveSelfRuntime",
                "payload_family": "interoceptive_precision_bias",
            },
        ],
        "regional_sensitivity": [
            {"system_id": "PredictionActiveInferenceRuntime", "sensitivity": "high"},
            {"system_id": "ConsciousWorkspaceRuntime", "sensitivity": "medium"},
            {"system_id": "AffectiveSelfRuntime", "sensitivity": "high"},
            {"system_id": "ActionResponsibilityRuntime", "sensitivity": "high"},
        ],
        "decay_recovery": {
            "decay_half_life": {
                "arousal_gain": "seconds",
                "unexpected_uncertainty": "seconds",
                "relationship_pressure": "minutes",
                "fatigue_load": "hours",
            },
            "homeostatic_repair_routes": [
                "MicroPause",
                "RecoveryMode",
                "OfflineConsolidation",
            ],
            "repair_gate_ref": "runtime/state/body/recovery_pathways.json",
        },
        "network_state_ref": (
            "runtime/state/neural_life_core/network_state.json"
            if network_state
            else None
        ),
        "body_signal_profile": body_profile if body_profile else None,
        "offline_learning_cumulative_profile": (
            _offline_learning_signal_profile(offline_learning_cumulative_profile)
            if offline_learning_cumulative_profile
            else None
        ),
        "queue_e_repair_modulation_profile": repair_profile if repair_profile else None,
        "queue_e_repair_pressure_level": pressure_level,
        "queue_e_repair_attention_target": repair_attention_target,
        "queue_e_repair_ref_set": list(repair_profile.get("ref_set", [])),
        "bus_edge_refs": [
            "body_signal_bus",
            "signal_media_bus",
            "prediction_error_bus",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _repair_pressure_scale(pressure_level: str) -> float:
    return {
        "quiet": 0.0,
        "present": 0.35,
        "elevated": 0.72,
        "urgent": 1.0,
    }.get(pressure_level, 0.0)


def _offline_learning_signal_profile(
    profile: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(profile, dict):
        return {}
    ref_set = _dedupe(
        _string_list(profile.get("ref_set"))
        + _string_list(profile.get("offline_learning_cumulative_ref_set"))
    )
    generation = _int_or_zero(
        profile.get("generation")
        or profile.get("offline_learning_cumulative_generation")
    )
    pressure_level = str(
        profile.get("pressure_level")
        or profile.get("offline_learning_cumulative_pressure_level")
        or "quiet"
    )
    attention_target = str(
        profile.get("attention_target")
        or profile.get("offline_learning_cumulative_attention_target")
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
            profile.get("integration_mode")
            or profile.get("offline_learning_cumulative_integration_mode")
            or "baseline_offline_learning_maintenance"
        ),
        "relationship_reconsolidation_required": bool(
            profile.get("relationship_reconsolidation_required")
            or profile.get(
                "offline_learning_cumulative_relationship_reconsolidation_required"
            )
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


def _body_signal_profile(
    *,
    body_resource_budget: dict[str, Any] | None,
    core_affect_vector: dict[str, Any] | None,
    body_presence_profile: dict[str, Any] | None,
    offline_learning_cumulative_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    body_resource_budget = body_resource_budget or {}
    core_affect_vector = core_affect_vector or {}
    body_presence_profile = body_presence_profile or {}
    offline_learning_profile = _offline_learning_signal_profile(
        offline_learning_cumulative_profile
    )
    if not any(
        [
            body_resource_budget,
            core_affect_vector,
            body_presence_profile,
            offline_learning_profile,
        ]
    ):
        return {}

    maintenance_pressure = body_resource_budget.get("maintenance_pressure", {})
    if not isinstance(maintenance_pressure, dict):
        maintenance_pressure = {}
    fatigue_state = body_resource_budget.get("fatigue_state", {})
    if not isinstance(fatigue_state, dict):
        fatigue_state = {}
    energy_state = body_resource_budget.get("energy_state", {})
    if not isinstance(energy_state, dict):
        energy_state = {}

    fatigue_load = _fatigue_load_scale(
        body_presence_profile.get("fatigue_load") or fatigue_state.get("level")
    )
    pain_pressure = _float_signal(
        body_presence_profile.get("pain_pressure")
        if body_presence_profile.get("pain_pressure") is not None
        else core_affect_vector.get("pain_pressure"),
        default=0.0,
    )
    dream_residue_load = _float_signal(
        body_presence_profile.get("dream_residue_load")
        if body_presence_profile.get("dream_residue_load") is not None
        else core_affect_vector.get("dream_residue_load"),
        default=0.0,
    )
    arousal = _float_signal(
        body_presence_profile.get("arousal")
        if body_presence_profile.get("arousal") is not None
        else core_affect_vector.get("arousal"),
        default=0.0,
    )
    relationship_tension = _float_signal(
        body_presence_profile.get("relationship_tension")
        if body_presence_profile.get("relationship_tension") is not None
        else core_affect_vector.get("relationship_tension"),
        default=0.0,
    )
    responsibility_weight = _float_signal(
        body_presence_profile.get("responsibility_weight")
        if body_presence_profile.get("responsibility_weight") is not None
        else core_affect_vector.get("responsibility_weight"),
        default=0.0,
    )
    repair_drive = _repair_drive_signal(
        body_presence_profile.get("repair_drive")
        or core_affect_vector.get("repair_drive")
        or maintenance_pressure.get("repair_drive")
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
        relationship_reconsolidation_required = bool(
            offline_learning_profile.get("relationship_reconsolidation_required")
        )
        attention_target = str(offline_learning_profile.get("attention_target") or "")
        fatigue_load = max(fatigue_load, _clamp(0.28 + offline_scale * 0.22))
        dream_residue_load = max(
            dream_residue_load,
            _clamp(0.24 + offline_scale * 0.38 + generation_scale * 0.12),
        )
        repair_drive = max(
            repair_drive,
            _clamp(
                0.22
                + offline_scale * 0.34
                + (0.16 if relationship_reconsolidation_required else 0.0)
            ),
        )
        if attention_target == "relationship_learning_plan":
            relationship_tension = max(
                relationship_tension,
                _clamp(0.26 + offline_scale * 0.38),
            )
    body_ref_set = _dedupe(
        _string_list(body_presence_profile.get("body_ref_set"))
        + _string_list(offline_learning_profile.get("ref_set"))
        + _string_list(
            [
                "runtime/state/body/body_resource_budget.json"
                if body_resource_budget
                else None,
                "runtime/state/body/core_affect_vector.json"
                if core_affect_vector
                else None,
            ]
        )
    )
    memory_write_bias = "baseline_candidate_gate"
    if fatigue_load >= 0.65 or pain_pressure >= 0.65:
        memory_write_bias = "defer_noncritical_memory_commit"
    elif (
        offline_learning_profile.get("relationship_reconsolidation_required") is True
        or offline_learning_profile.get("attention_target")
        == "relationship_learning_plan"
    ):
        memory_write_bias = "relationship_context_first"
    elif repair_drive >= 0.7 or responsibility_weight >= 0.7:
        memory_write_bias = "repair_evidence_first"
    elif relationship_tension >= 0.65:
        memory_write_bias = "relationship_context_first"

    return {
        "schema_version": "body_signal_modulation_profile_v0",
        "fatigue_load": fatigue_load,
        "energy_level": body_presence_profile.get("energy_level")
        or energy_state.get("level"),
        "arousal": arousal,
        "pain_pressure": pain_pressure,
        "relationship_tension": relationship_tension,
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
        "offline_learning_ref_set": _string_list(
            offline_learning_profile.get("ref_set")
        ),
        "responsibility_weight": responsibility_weight,
        "repair_drive": repair_drive,
        "body_signal_strength": max(
            fatigue_load,
            arousal,
            pain_pressure,
            relationship_tension,
            dream_residue_load,
            responsibility_weight,
            repair_drive,
        ),
        "memory_write_bias": memory_write_bias,
        "dream_pressure_bias": (
            "offline_consolidation_pressure"
            if dream_residue_load >= 0.55 or fatigue_load >= 0.65
            else "baseline_dream_pressure"
        ),
        "language_tempo_bias": (
            "guarded_deliberate"
            if fatigue_load >= 0.5 or arousal >= 0.65
            else "steady"
        ),
        "body_ref_set": body_ref_set,
    }


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


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)
