from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_dream_experience_window(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    dream_frame: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
) -> dict[str, Any]:
    pain_residue_refs = list(replay_cue_bundle.get("pain_regret_residue_refs", []))
    relationship_simulation_refs = list(replay_cue_bundle.get("relationship_residue_refs", []))
    source_trace_refs = (
        list(dream_frame.get("dream_record_refs", []))
        + list(replay_cue_bundle.get("turn_residue_refs", []))
        + pain_residue_refs
        + relationship_simulation_refs
    )
    return {
        "schema_version": "dream_experience_window_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "DreamExperienceWindow",
        "dream_window_id": f"dream-window-{run_id}",
        "window_kind": "nrem_like_replay" if dream_frame.get("dream_record_refs") else "micro_dream",
        "dream_scene_frames": [
            {
                "scene_id": f"dream-scene-{run_id}-0001",
                "theme": "relationship_repair_replay",
                "reportability": "guarded_reportable",
            }
        ],
        "subjective_vantage": "first_person_relation_weighted",
        "affective_theme": [
            "repair_drive",
            "continuity_protection",
        ],
        "source_trace_refs": source_trace_refs,
        "dream_hot_zone_trace": {
            "intensity": 0.52,
            "reportability": 0.74,
            "recall_probability": 0.68,
        },
        "lucid_meta_marker": {
            "status": "prepared_for_wake_report",
            "self_monitoring": True,
        },
        "dream_action_inhibition_seal": "closed",
        "dream_record_refs": list(dream_frame.get("dream_record_refs", [])),
        "pain_residue_refs": pain_residue_refs,
        "relationship_simulation_refs": relationship_simulation_refs,
        "dream_fact_gate_status": dream_frame.get("dream_fact_gate", "blocked"),
        "wake_integration_ref": "runtime/state/dream/wake_integration_frame.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_dream_experience_window(dream_window: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if dream_window.get("schema_version") != "dream_experience_window_v0":
        reasons.append("dream_window_gate schema mismatch")
    for field in [
        "dream_window_id",
        "window_kind",
        "dream_scene_frames",
        "subjective_vantage",
        "affective_theme",
        "dream_action_inhibition_seal",
        "wake_integration_ref",
    ]:
        if not dream_window.get(field):
            reasons.append(f"dream_window_gate missing {field}")
    return reasons
