from __future__ import annotations

from typing import Any


def build_prediction_workspace_frame(
    run_id: str,
    generated_at: str,
    language_continuity: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    prediction_error_field = prediction_error_field or {}
    active_sampling_plan = active_sampling_plan or {}
    signal_media_runtime = signal_media_runtime or {}
    repair_profile = (
        active_sampling_plan.get("queue_e_repair_modulation_profile")
        or prediction_error_field.get("queue_e_repair_modulation_profile")
        or belief_state.get("queue_e_repair_modulation_profile")
        or signal_media_runtime.get("queue_e_repair_modulation_profile")
        or {}
    )
    pressure_level = repair_profile.get("pressure_level", "quiet")
    continuity = {
        "shared_language_refs": list((language_continuity or {}).get("shared_language_refs", [])),
        "expression_monitor_refs": list((language_continuity or {}).get("expression_monitor_refs", [])),
        "relation_scope_refs": list((language_continuity or {}).get("relation_scope_refs", [])),
        "commitment_refs": list((language_continuity or {}).get("commitment_refs", [])),
        "self_narrative_trace_refs": list((language_continuity or {}).get("self_narrative_trace_refs", [])),
        "dialogue_turn_log_refs": list((language_continuity or {}).get("dialogue_turn_log_refs", [])),
        "language_percept_refs": list((language_continuity or {}).get("language_percept_refs", [])),
        "semantic_map_refs": list((language_continuity or {}).get("semantic_map_refs", [])),
        "semantic_ambiguity_refs": list((language_continuity or {}).get("semantic_ambiguity_refs", [])),
        "prediction_error_refs": list((language_continuity or {}).get("prediction_error_refs", [])),
        "signal_media_refs": list((language_continuity or {}).get("signal_media_refs", [])),
        "semantic_prediction_focus": (language_continuity or {}).get("semantic_prediction_focus"),
    }
    has_language_handoff = bool(continuity["language_percept_refs"] or continuity["semantic_map_refs"])
    has_ambiguity_queue = bool(continuity["semantic_ambiguity_refs"])
    semantic_focus = continuity["semantic_prediction_focus"] or "continuity-seed-focus"
    language_handoff_refs = _dedupe(
        list(continuity["language_percept_refs"])
        + list(continuity["semantic_map_refs"])
        + (
            ["runtime/state/language/semantic_map_frame.json#ambiguity_queue"]
            if has_ambiguity_queue
            else []
        )
    )
    return {
        "schema_version": "prediction_workspace_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": "S02_NEURAL_LIFE_CORE",
        "source_runtime": "PredictionActiveInferenceRuntime",
        "workspace_frame_target_ref": "runtime/state/consciousness/workspace_frame.json",
        "source_doc_refs": [
            "docs/01v_prediction_active_inference_runtime_matrix.md",
            "docs/04_sensory_thalamus_interoception.md",
            "docs/10_consciousness_attention_workspace.md",
            "docs/11_neuromodulation_and_signal_media.md",
        ],
        "workspace_contents": {
            "candidate_explanations": (
                [
                    {
                        "explanation_id": "semantic-focus-v0-0001",
                        "explanation_family": "language_semantic_handoff",
                        "focus": semantic_focus,
                    }
                ]
                if semantic_focus
                else []
            ),
            "precision_state": (
                signal_media_runtime.get("precision_policy", {}).get("policy_mode")
                or ("semantic_handoff_seeded" if has_language_handoff else "seed_only")
            ),
            "active_sampling_mode": (
                active_sampling_plan.get("selected_route")
                or ("clarify_ambiguity" if has_ambiguity_queue else "observation_first")
            ),
            "language_continuity_focus": continuity,
            "belief_scope": belief_state.get("state_scope"),
            "sampling_stage_effect": active_sampling_plan.get("stage_effect"),
            "queue_e_repair_pressure_level": pressure_level,
            "queue_e_repair_attention_target": repair_profile.get("attention_target", "repair_followup"),
        },
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json"
            if belief_state
            else None
        ),
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "active_sampling_plan_ref": (
            "runtime/state/prediction/active_sampling_plan.json"
            if active_sampling_plan
            else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "queue_e_repair_modulation_profile": repair_profile if repair_profile else None,
        "queue_e_repair_pressure_level": pressure_level,
        "queue_e_repair_attention_target": repair_profile.get("attention_target", "repair_followup"),
        "queue_e_repair_ref_set": list(repair_profile.get("ref_set", [])),
        "bus_edge_refs": [
            "prediction_error_bus",
            "conscious_broadcast_bus",
        ],
        "downstream_systems": [
            "ConsciousWorkspaceRuntime",
            "LanguageRelationshipRuntime",
        ],
        "language_handoff_refs": language_handoff_refs,
        "language_prediction_focus": semantic_focus,
        "semantic_ambiguity_refs": list(continuity["semantic_ambiguity_refs"]),
    }


def project_prediction_workspace_from_live_language_turn(
    *,
    prediction_workspace_frame: dict[str, Any],
    language_percept: dict[str, Any],
    semantic_map: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    if not prediction_workspace_frame:
        return {}
    updated = dict(prediction_workspace_frame)
    ambiguity_queue = list(semantic_map.get("ambiguity_queue", []))
    language_continuity = {
        "language_percept_refs": ["runtime/state/language/language_percept_frame.json"],
        "semantic_map_refs": ["runtime/state/language/semantic_map_frame.json"],
        "semantic_ambiguity_refs": [
            f"runtime/state/language/semantic_map_frame.json#ambiguity_queue:{flag}"
            for flag in ambiguity_queue[:8]
        ],
        "semantic_prediction_focus": semantic_map.get("semantic_focus"),
        "percept_focus_trace": list(language_percept.get("percept_focus_trace", []))[:8],
    }
    rebuilt = build_prediction_workspace_frame(
        run_id=str(updated.get("run_id") or "live-language-handoff"),
        generated_at=generated_at,
        language_continuity=language_continuity,
        belief_state=_read_nested_workspace_input(updated, "belief_state_ref"),
        prediction_error_field=_read_nested_workspace_input(
            updated, "prediction_error_ref"
        ),
        active_sampling_plan=_read_nested_workspace_input(
            updated, "active_sampling_plan_ref"
        ),
        signal_media_runtime=_read_nested_workspace_input(updated, "signal_media_ref"),
    )
    workspace_contents = dict(rebuilt.get("workspace_contents", {}))
    workspace_contents["live_language_handoff"] = {
        "schema_version": "live_language_handoff_v0",
        "generated_at": generated_at,
        "semantic_focus": semantic_map.get("semantic_focus"),
        "ambiguity_ref_count": len(ambiguity_queue),
        "percept_focus_ref_count": len(language_percept.get("percept_focus_trace", [])),
    }
    rebuilt["workspace_contents"] = workspace_contents
    rebuilt["live_language_handoff_refreshed"] = True
    return rebuilt


def _read_nested_workspace_input(
    frame: dict[str, Any],
    ref_key: str,
) -> dict[str, Any]:
    ref = frame.get(ref_key)
    if not isinstance(ref, str) or not ref:
        return {}
    return {"ref": ref}


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
