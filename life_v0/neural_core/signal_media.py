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
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    network_state = network_state or {}
    repair_profile = queue_e_repair_modulation_profile or {}
    pressure_level = repair_profile.get("pressure_level", "quiet")
    pressure_scale = _repair_pressure_scale(pressure_level)
    modulation_vector = {
        "arousal_gain": _clamp(0.68 + pressure_scale * 0.08),
        "expected_uncertainty": _clamp(0.34 + pressure_scale * 0.06),
        "unexpected_uncertainty": _clamp(0.21 + pressure_scale * 0.11),
        "relationship_pressure": _clamp(0.29 + pressure_scale * 0.19),
        "repair_drive": _clamp(0.47 + pressure_scale * 0.29),
        "fatigue_load": 0.26,
        "control_cost": _clamp(0.39 + pressure_scale * 0.13),
        "stress_pulse": _clamp(0.22 + pressure_scale * 0.16),
        "allostatic_load": _clamp(0.31 + pressure_scale * 0.12),
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
            "interoceptive_precision": 0.58,
            "memory_precision": 0.63,
            "language_precision": _clamp(0.67 + pressure_scale * 0.08),
            "relationship_precision": _clamp(0.74 + pressure_scale * 0.1),
            "action_precision": _clamp(0.52 - pressure_scale * 0.08),
            "expected_uncertainty_weight": modulation_vector["expected_uncertainty"],
            "unexpected_uncertainty_weight": modulation_vector["unexpected_uncertainty"],
            "repair_priority": "repair_before_action",
            "stage_effect": "hold_for_evidence",
            "queue_e_attention_target": repair_attention_target,
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


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)
