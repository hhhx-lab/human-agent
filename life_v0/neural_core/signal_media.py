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
) -> dict[str, Any]:
    network_state = network_state or {}
    modulation_vector = {
        "arousal_gain": 0.68,
        "expected_uncertainty": 0.34,
        "unexpected_uncertainty": 0.21,
        "relationship_pressure": 0.29,
        "repair_drive": 0.47,
        "fatigue_load": 0.26,
        "control_cost": 0.39,
        "stress_pulse": 0.22,
        "allostatic_load": 0.31,
    }
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
        ],
        "modulation_vector": modulation_vector,
        "precision_policy": {
            "precision_policy_id": f"precision-policy-{run_id}",
            "policy_mode": "relationship_guarded_active_inference",
            "attention_route": "salience_to_workspace",
            "interoceptive_precision": 0.58,
            "memory_precision": 0.63,
            "language_precision": 0.67,
            "relationship_precision": 0.74,
            "action_precision": 0.52,
            "expected_uncertainty_weight": modulation_vector["expected_uncertainty"],
            "unexpected_uncertainty_weight": modulation_vector["unexpected_uncertainty"],
            "repair_priority": "repair_before_action",
            "stage_effect": "hold_for_evidence",
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
        "bus_edge_refs": [
            "body_signal_bus",
            "signal_media_bus",
            "prediction_error_bus",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
