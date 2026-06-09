from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .background_continuity import load_background_continuity_profile
from .continuity_writeback import build_idle_continuity_frame, record_idle_continuity
from .idle_strategy import (
    IDLE_STRATEGY_STATE_REF,
    decide_idle_strategy,
    extract_idle_governance_fields,
)
from .persistent_process import (
    RESIDENT_GOVERNANCE_REPORT_REF,
    RESIDENT_GOVERNANCE_SNAPSHOT_REF,
    RESIDENT_GOVERNANCE_STATE_REF,
)


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
    relationship_timeline: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> int:
    heartbeat_counter = int(safe_terminal_loop.get("heartbeat_counter", 0)) + 1
    heartbeat_report_ref = "runtime/reports/latest/digital_life_waiting_heartbeat.json"
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    background_continuity_profile = load_background_continuity_profile(
        terminal_dir=terminal_dir,
        reports_dir=reports_dir,
    )
    idle_strategy = decide_idle_strategy(
        run_id=run_id,
        generated_at=generated_at,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        idle_continuity_frame=None,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        background_continuity_profile=background_continuity_profile,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
    )
    world_contact_release_posture = str(
        idle_strategy.get("world_contact_release_posture")
        or (world_contact_summary or {}).get("release_posture", "shadow_only_guarded")
    )
    repair_followup_required = bool(
        idle_strategy.get("repair_followup_required")
        or (pain_regret_repair_report or {}).get("repair_followup_required")
        or (responsibility_loop_state or {}).get("repair_followup_required")
    )
    waiting_mode = str(
        idle_strategy.get("waiting_mode", "restored_waiting_for_external_turn")
    )
    heartbeat_packet = {
        "schema_version": "digital_life_waiting_heartbeat_v0",
        "run_id": run_id,
        "generated_at": now_iso(),
        "status": "closed",
        "heartbeat_counter": heartbeat_counter,
        "waiting_mode": waiting_mode,
        "idle_strategy_ref": IDLE_STRATEGY_STATE_REF,
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "next_required_action": "await_next_external_relation_turn",
    }
    if responsibility_loop_state_ref:
        heartbeat_packet["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        heartbeat_packet["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        heartbeat_packet["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        heartbeat_packet["membrane_guard_refs"] = membrane_guard_refs
    if world_contact_release_posture:
        heartbeat_packet["world_contact_release_posture"] = world_contact_release_posture
    if repair_followup_required:
        heartbeat_packet["repair_followup_required"] = True
    heartbeat_packet.update(extract_idle_governance_fields(idle_strategy))

    safe_terminal_loop["current_mode"] = waiting_mode
    safe_terminal_loop["last_heartbeat_mode"] = waiting_mode
    safe_terminal_loop["heartbeat_counter"] = heartbeat_counter
    safe_terminal_loop["last_heartbeat_packet_ref"] = heartbeat_report_ref
    safe_terminal_loop["idle_strategy_ref"] = IDLE_STRATEGY_STATE_REF
    safe_terminal_loop["resident_governance_state_ref"] = RESIDENT_GOVERNANCE_STATE_REF
    write_json(terminal_dir / "safe_terminal_loop_state.json", safe_terminal_loop)

    terminal_life_loop_state["current_mode"] = waiting_mode
    terminal_life_loop_state["heartbeat_counter"] = heartbeat_counter
    terminal_life_loop_state["last_heartbeat_packet_ref"] = heartbeat_report_ref
    terminal_life_loop_state["next_required_action"] = "await_next_external_relation_turn"
    terminal_life_loop_state["idle_strategy_ref"] = IDLE_STRATEGY_STATE_REF
    terminal_life_loop_state["resident_governance_state_ref"] = RESIDENT_GOVERNANCE_STATE_REF
    for field in (
        "relationship_timeline_ref",
        "commitment_expression_plan_ref",
        "apology_repair_language_trace_ref",
        "long_horizon_language_refs",
    ):
        if field in idle_strategy:
            terminal_life_loop_state[field] = idle_strategy[field]
    if responsibility_loop_state_ref:
        terminal_life_loop_state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        terminal_life_loop_state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        terminal_life_loop_state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        terminal_life_loop_state["membrane_guard_refs"] = membrane_guard_refs
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
        relationship_timeline_ref=idle_strategy.get("relationship_timeline_ref"),
        commitment_expression_plan_ref=idle_strategy.get("commitment_expression_plan_ref"),
        apology_repair_language_trace_ref=idle_strategy.get("apology_repair_language_trace_ref"),
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        world_contact_release_posture=world_contact_release_posture,
        repair_followup_required=repair_followup_required,
        offline_learning_pressure_level=idle_strategy.get("offline_learning_pressure_level"),
        offline_learning_attention_target=idle_strategy.get("offline_learning_attention_target"),
        background_continuity_mode=idle_strategy.get("background_continuity_mode"),
        background_carryover_pressure_level=idle_strategy.get("background_carryover_pressure_level"),
        background_carryover_attention_target=idle_strategy.get("background_carryover_attention_target"),
        background_carryover_generation=idle_strategy.get("background_carryover_generation"),
        background_carryover_parent_run_id=idle_strategy.get("background_carryover_parent_run_id"),
        background_carryover_source_ref_set=idle_strategy.get("background_carryover_source_ref_set"),
        background_continuity_ref_set=idle_strategy.get("background_continuity_ref_set"),
    )
    write_json(terminal_dir / "idle_continuity_frame.json", idle_continuity_frame)
    resident_governance_state = {
        "schema_version": "resident_governance_state_v0",
        "run_id": run_id,
        "generated_at": now_iso(),
        "status": "active",
        "governance_mode": "foreground_terminal_residency",
        "governance_phase": "waiting_heartbeat_active",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "idle_strategy_ref": IDLE_STRATEGY_STATE_REF,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "resident_governance_report_ref": RESIDENT_GOVERNANCE_REPORT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_heartbeat_packet_ref": heartbeat_report_ref,
        "relationship_timeline_ref": idle_strategy.get("relationship_timeline_ref"),
        "commitment_expression_plan_ref": idle_strategy.get("commitment_expression_plan_ref"),
        "apology_repair_language_trace_ref": idle_strategy.get("apology_repair_language_trace_ref"),
        "long_horizon_language_refs": list(idle_strategy.get("long_horizon_language_refs", [])),
        "next_required_action": "await_next_external_relation_turn",
    }
    if responsibility_loop_state_ref:
        resident_governance_state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resident_governance_state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resident_governance_state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resident_governance_state["membrane_guard_refs"] = membrane_guard_refs
    resident_governance_state.update(extract_idle_governance_fields(idle_strategy))
    write_json(terminal_dir / "resident_governance_state.json", resident_governance_state)
    idle_strategy["idle_continuity_ref"] = "runtime/state/terminal/idle_continuity_frame.json"
    write_json(terminal_dir / "idle_strategy_state.json", idle_strategy)
    write_json(reports_dir / "digital_life_waiting_heartbeat.json", heartbeat_packet)
    return heartbeat_counter
