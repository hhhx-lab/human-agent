from __future__ import annotations

from typing import Any


def build_idle_continuity_frame(
    *,
    run_id: str,
    generated_at: str,
    heartbeat_counter: int,
    heartbeat_report_ref: str,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    relationship_timeline_ref: str | None = None,
    commitment_expression_plan_ref: str | None = None,
    apology_repair_language_trace_ref: str | None = None,
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
) -> dict[str, Any]:
    replay_seed_refs = ["runtime/state/life_state.json#memory_index.replay_cues"]
    if replay_cue_bundle_ref:
        replay_seed_refs.append(replay_cue_bundle_ref)
    return {
        "schema_version": "idle_continuity_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "idle_continuity_id": f"idle-continuity-{run_id}-{heartbeat_counter:04d}",
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_ref": heartbeat_report_ref,
        "self_narrative_idle_refs": [heartbeat_report_ref],
        "commitment_idle_refs": [heartbeat_report_ref],
        "relationship_idle_refs": [heartbeat_report_ref],
        "replay_seed_refs": replay_seed_refs,
        "waiting_state": "restored_waiting_for_external_turn",
        "self_narrative_ref": "runtime/state/language/self_narrative_language_trace.json",
        "commitment_index_ref": "runtime/state/language/commitment_repair_language_index.json",
        "relationship_graph_ref": "runtime/state/relationship/relationship_subject_graph.json",
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "long_horizon_language_refs": [
            ref
            for ref in [
                relationship_timeline_ref,
                commitment_expression_plan_ref,
                apology_repair_language_trace_ref,
            ]
            if ref
        ],
        "replay_cue_bundle_ref": replay_cue_bundle_ref,
        "offline_consolidation_frame_ref": offline_consolidation_frame_ref,
        "growth_patch_candidate_queue_ref": growth_patch_candidate_queue_ref,
        "growth_patch_candidate_ids": list(growth_patch_candidate_ids or []),
        "replay_residue_ref_count": replay_residue_ref_count,
        "dream_window_ref_count": dream_window_ref_count,
        "growth_patch_candidate_count": growth_patch_candidate_count,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }


def record_idle_continuity(
    *,
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    heartbeat_counter: int,
    heartbeat_report_ref: str,
) -> None:
    self_narrative_trace.setdefault("idle_continuity_refs", [])
    self_narrative_trace["idle_continuity_refs"].append(heartbeat_report_ref)
    self_narrative_trace["idle_continuity_counter"] = heartbeat_counter
    self_narrative_trace["last_idle_continuity"] = {
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_ref": heartbeat_report_ref,
    }

    commitment_index.setdefault("idle_presence_refs", [])
    commitment_index["idle_presence_refs"].append(heartbeat_report_ref)
    commitment_index["idle_presence_counter"] = heartbeat_counter
    commitment_index["last_idle_presence"] = {
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_ref": heartbeat_report_ref,
    }

    relationship_graph.setdefault("idle_presence_refs", [])
    relationship_graph["idle_presence_refs"].append(heartbeat_report_ref)
    relationship_graph["idle_presence_counter"] = heartbeat_counter

    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        subjects[0]["idle_presence_counter"] = heartbeat_counter
        subjects[0]["last_idle_continuity_event_kind"] = "waiting_heartbeat_refresh"
        subjects[0]["last_idle_continuity_report_ref"] = heartbeat_report_ref
