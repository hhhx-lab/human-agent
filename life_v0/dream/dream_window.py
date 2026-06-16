from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import (
    queue_e_repair_modulation_profile_from_replay_cue_bundle,
)


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]

EXIT_DREAM_CONSOLIDATION_SUMMARY_REF = (
    "runtime/state/dream/exit_dream_consolidation_summary.json"
)
OFFLINE_MEMORY_HYGIENE_REPORT_REF = (
    "runtime/state/memory/offline_memory_hygiene_report.json"
)


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
    repair_profile = queue_e_repair_modulation_profile_from_replay_cue_bundle(
        replay_cue_bundle
    )
    source_trace_refs = (
        list(dream_frame.get("dream_record_refs", []))
        + list(replay_cue_bundle.get("turn_residue_refs", []))
        + pain_residue_refs
        + relationship_simulation_refs
        + list(repair_profile.get("ref_set", []))
    )
    memory_bridge = replay_cue_bundle.get("memory_consolidation_bridge")
    if not isinstance(memory_bridge, dict):
        memory_bridge = {}
    memory_consolidation_trace_refs = _dedupe(
        list(replay_cue_bundle.get("offline_memory_replay_refs", []))
        + list(memory_bridge.get("trace_store_refs", []))
        + list(memory_bridge.get("engram_cluster_refs", []))
    )
    relationship_deep_dream_refs = _dedupe(
        list(replay_cue_bundle.get("offline_relationship_memory_refs", []))
        + list(memory_bridge.get("relationship_deep_memory_refs", []))
    )
    autobiographical_dream_refs = _dedupe(
        list(replay_cue_bundle.get("offline_autobiographical_memory_refs", []))
        + list(memory_bridge.get("autobiographical_hierarchy_refs", []))
    )
    source_trace_refs = _dedupe(
        source_trace_refs
        + memory_consolidation_trace_refs
        + relationship_deep_dream_refs
        + autobiographical_dream_refs
    )
    affective_theme = [
        "repair_drive",
        "continuity_protection",
    ]
    if repair_profile["pressure_level"] in {"urgent", "elevated"}:
        affective_theme.append("responsibility_repair_modulation")
    if repair_profile["attention_target"] == "regret_pressure":
        affective_theme.append("regret_pressure_rehearsal")
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
        "affective_theme": affective_theme,
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
        "memory_consolidation_trace_refs": memory_consolidation_trace_refs,
        "relationship_deep_dream_refs": relationship_deep_dream_refs,
        "autobiographical_dream_refs": autobiographical_dream_refs,
        "dream_memory_boundary": "dream_recombines_memory_for_replay_without_fact_promotion",
        "queue_e_repair_modulation_profile": repair_profile,
        "queue_e_repair_pressure_level": repair_profile["pressure_level"],
        "queue_e_repair_attention_target": repair_profile["attention_target"],
        "queue_e_repair_ref_set": list(repair_profile.get("ref_set", [])),
        "dream_fact_gate_status": dream_frame.get("dream_fact_gate", "blocked"),
        "wake_integration_ref": "runtime/state/dream/wake_integration_frame.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_exit_closeout_dream_experience_window(
    *,
    run_id: str,
    generated_at: str,
    exit_dream_summary: dict[str, Any],
    entry_vector: dict[str, Any] | None = None,
    cue_policy: dict[str, Any] | None = None,
    hygiene_report: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    web_dream_learning_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry_vector = entry_vector or {}
    cue_policy = cue_policy or {}
    hygiene_report = hygiene_report or {}
    web_dream_learning_state = web_dream_learning_state or {}
    memory_tiering = exit_dream_summary.get("memory_tiering") or {}
    trace_refs = [
        f"runtime/state/memory/memory_trace_store.json#{trace.get('trace_id')}"
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict)
        and trace.get("exit_dream_origin") == "terminal_exit_consolidation"
        and trace.get("trace_id")
    ]
    scene_frames: list[dict[str, Any]] = []
    for index, cue in enumerate(cue_policy.get("selected_cues", [])[:4], start=1):
        if not isinstance(cue, dict):
            continue
        scene_frames.append(
            _exit_dialogue_scene_frame(
                run_id=run_id,
                index=index,
                cue=cue,
                trace_refs=trace_refs,
            )
        )
    if not scene_frames:
        scene_frames.append(
            {
                "scene_id": f"dream-scene-{run_id}-0001",
                "scene_kind": "exit_dialogue",
                "subjective_vantage": "first_person",
                "affective_theme": list(
                    exit_dream_summary.get("relationship_theme_tags", [])
                )[:3]
                or ["continuity_protection"],
                "source_trace_refs": trace_refs[:6],
                "web_dream_scene_refs": [],
                "relationship_simulation_refs": [
                    EXIT_DREAM_CONSOLIDATION_SUMMARY_REF
                ],
                "pain_residue_refs": [],
                "dream_hot_zone_trace": {
                    "intensity": 0.48,
                    "reportability": 0.7,
                    "recall_probability": 0.62,
                },
                "dream_marker": "dream_residue_not_fact",
                "dream_action_inhibition_seal": "closed",
                "wake_reentry_targets": [
                    "runtime/state/memory/memory_retrieval_frame.json"
                ],
            }
        )
    web_scene_refs = _web_dream_scene_refs(web_dream_learning_state)
    if web_scene_refs:
        scene_frames.append(
            {
                "scene_id": f"dream-scene-{run_id}-web-0001",
                "scene_kind": "web_residue",
                "subjective_vantage": "observer",
                "affective_theme": ["curiosity_residue", "offline_learning"],
                "source_trace_refs": trace_refs[:3],
                "web_dream_scene_refs": web_scene_refs,
                "relationship_simulation_refs": [],
                "pain_residue_refs": [],
                "dream_hot_zone_trace": {
                    "intensity": 0.35,
                    "reportability": 0.55,
                    "recall_probability": 0.4,
                },
                "dream_marker": "dream_residue_not_fact",
                "dream_action_inhibition_seal": "closed",
                "wake_reentry_targets": [
                    "runtime/state/dream/web_dream_learning_state.json"
                ],
            }
        )
    hygiene_refs = []
    if hygiene_report:
        hygiene_refs.append(OFFLINE_MEMORY_HYGIENE_REPORT_REF)
    return {
        "schema_version": "dream_experience_window_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "DreamExperienceWindow",
        "dream_window_id": f"dream-window-exit-{run_id}",
        "window_kind": "exit_dialogue_dream",
        "dream_scene_frames": scene_frames,
        "subjective_vantage": "first_person_relation_weighted",
        "affective_theme": _dedupe(
            list(exit_dream_summary.get("relationship_theme_tags", []))
            + ["exit_dialogue_consolidation"]
        )[:5],
        "source_trace_refs": _dedupe(
            trace_refs
            + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
            + hygiene_refs
        ),
        "dream_hot_zone_trace": {
            "intensity": 0.56,
            "reportability": 0.72,
            "recall_probability": 0.66,
        },
        "lucid_meta_marker": {
            "status": "exit_closeout_dream_projection",
            "self_monitoring": True,
        },
        "dream_action_inhibition_seal": "closed",
        "dream_record_refs": [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF],
        "memory_consolidation_trace_refs": trace_refs[:12],
        "offline_dream_entry_vector_ref": entry_vector.get(
            "offline_dream_entry_vector_ref"
        ),
        "dream_cue_policy_state_ref": cue_policy.get("dream_cue_policy_state_ref"),
        "hygiene_summary_refs": hygiene_refs,
        "exit_dream_consolidation_summary_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
        "memory_tiering_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF + "#memory_tiering",
        "memory_tiering": dict(memory_tiering),
        "selected_offline_modes": list(entry_vector.get("selected_offline_modes", [])),
        "dream_memory_boundary": "dream_recombines_memory_for_replay_without_fact_promotion",
        "dream_fact_gate_status": "blocked",
        "wake_integration_ref": "runtime/state/dream/wake_integration_frame.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_web_residue_into_dream_window(
    *,
    dream_window: dict[str, Any],
    web_dream_learning_state: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    updated = dict(dream_window or {})
    web_scene_refs = _web_dream_scene_refs(web_dream_learning_state)
    if not web_scene_refs:
        return updated
    scene_frames = [
        dict(frame)
        for frame in updated.get("dream_scene_frames", [])
        if isinstance(frame, dict)
    ]
    existing_web = any(
        frame.get("scene_kind") == "web_residue" for frame in scene_frames
    )
    if not existing_web:
        run_id = str(updated.get("run_id") or "web")
        scene_frames.append(
            {
                "scene_id": f"dream-scene-{run_id}-web-0001",
                "scene_kind": "web_residue",
                "subjective_vantage": "observer",
                "affective_theme": ["curiosity_residue"],
                "source_trace_refs": [],
                "web_dream_scene_refs": web_scene_refs,
                "relationship_simulation_refs": [],
                "pain_residue_refs": [],
                "dream_hot_zone_trace": {
                    "intensity": 0.35,
                    "reportability": 0.55,
                    "recall_probability": 0.4,
                },
                "dream_marker": "dream_residue_not_fact",
                "dream_action_inhibition_seal": "closed",
                "wake_reentry_targets": [
                    "runtime/state/dream/web_dream_learning_state.json"
                ],
            }
        )
    else:
        for frame in scene_frames:
            if frame.get("scene_kind") == "web_residue":
                frame["web_dream_scene_refs"] = _dedupe(
                    list(frame.get("web_dream_scene_refs", [])) + web_scene_refs
                )
    updated["dream_scene_frames"] = scene_frames
    updated["web_dream_learning_state_ref"] = web_dream_learning_state.get(
        "web_dream_learning_state_ref"
    )
    updated["structured_wake_question_candidates"] = list(
        web_dream_learning_state.get("structured_wake_question_candidates", [])
    )
    updated["updated_at"] = generated_at
    return updated


def _exit_dialogue_scene_frame(
    *,
    run_id: str,
    index: int,
    cue: dict[str, Any],
    trace_refs: list[str],
) -> dict[str, Any]:
    cue_family = str(cue.get("cue_family") or "language_episode")
    vantage = (
        "relation_weighted"
        if cue_family == "relationship"
        else "first_person"
    )
    return {
        "scene_id": f"dream-scene-{run_id}-{index:04d}",
        "scene_kind": "exit_dialogue",
        "subjective_vantage": vantage,
        "affective_theme": [cue_family, "exit_dialogue_consolidation"],
        "source_trace_refs": trace_refs[:4],
        "web_dream_scene_refs": [],
        "relationship_simulation_refs": [str(cue.get("source_ref") or "")],
        "pain_residue_refs": (
            [str(cue.get("source_ref") or "")]
            if cue_family == "pain_regret"
            else []
        ),
        "dream_hot_zone_trace": {
            "intensity": float(cue.get("weight", 0.5) or 0.5),
            "reportability": 0.68,
            "recall_probability": 0.6,
        },
        "dream_marker": "dream_residue_not_fact",
        "dream_action_inhibition_seal": "closed",
        "wake_reentry_targets": [
            "runtime/state/memory/memory_retrieval_frame.json"
        ],
        "cue_id": cue.get("cue_id"),
        "semantic_key": cue.get("semantic_key"),
    }


def _web_dream_scene_refs(
    web_dream_learning_state: dict[str, Any],
) -> list[dict[str, Any]]:
    if not web_dream_learning_state:
        return []
    topic_cluster = str(web_dream_learning_state.get("topic_cluster_id") or "")
    url_digest = str(web_dream_learning_state.get("url_digest") or "")
    if not topic_cluster and not url_digest:
        return []
    return [
        {
            "url_digest": url_digest,
            "topic_cluster_id": topic_cluster,
            "page_profile_ref": web_dream_learning_state.get(
                "web_dream_learning_state_ref"
            ),
            "claim_status": "hypothesis_or_residue",
        }
    ]


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
        "memory_consolidation_trace_refs",
        "dream_memory_boundary",
        "dream_action_inhibition_seal",
        "wake_integration_ref",
    ]:
        if not dream_window.get(field):
            reasons.append(f"dream_window_gate missing {field}")
    return reasons


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
