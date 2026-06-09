from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .continuity_writeback import build_idle_continuity_frame, record_idle_continuity


def write_waiting_heartbeat(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    reports_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> int:
    heartbeat_counter = int(safe_terminal_loop.get("heartbeat_counter", 0)) + 1
    heartbeat_report_ref = "runtime/reports/latest/digital_life_waiting_heartbeat.json"
    heartbeat_packet = {
        "schema_version": "digital_life_waiting_heartbeat_v0",
        "run_id": run_id,
        "generated_at": now_iso(),
        "status": "closed",
        "heartbeat_counter": heartbeat_counter,
        "waiting_mode": "restored_waiting_for_external_turn",
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "next_required_action": "await_next_external_relation_turn",
    }

    safe_terminal_loop["current_mode"] = "restored_waiting_for_external_turn"
    safe_terminal_loop["last_heartbeat_mode"] = "restored_waiting_for_external_turn"
    safe_terminal_loop["heartbeat_counter"] = heartbeat_counter
    safe_terminal_loop["last_heartbeat_packet_ref"] = heartbeat_report_ref
    write_json(terminal_dir / "safe_terminal_loop_state.json", safe_terminal_loop)

    terminal_life_loop_state["current_mode"] = "restored_waiting_for_external_turn"
    terminal_life_loop_state["heartbeat_counter"] = heartbeat_counter
    terminal_life_loop_state["last_heartbeat_packet_ref"] = heartbeat_report_ref
    terminal_life_loop_state["next_required_action"] = "await_next_external_relation_turn"
    write_json(terminal_dir / "terminal_life_loop_state.json", terminal_life_loop_state)

    record_idle_continuity(
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        relationship_graph=relationship_graph,
        heartbeat_counter=heartbeat_counter,
        heartbeat_report_ref=heartbeat_report_ref,
    )
    write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)
    write_json(language_dir / "commitment_repair_language_index.json", commitment_index)
    write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    idle_continuity_frame = build_idle_continuity_frame(
        run_id=run_id,
        generated_at=generated_at,
        heartbeat_counter=heartbeat_counter,
        heartbeat_report_ref=heartbeat_report_ref,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
    )
    write_json(terminal_dir / "idle_continuity_frame.json", idle_continuity_frame)
    write_json(reports_dir / "digital_life_waiting_heartbeat.json", heartbeat_packet)
    return heartbeat_counter
