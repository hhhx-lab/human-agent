from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .heartbeat import write_waiting_heartbeat
from .incident_recovery import record_recovery_continuity
from .relaunch_recovery import detect_and_normalize_interrupted_previous_state
from ..shell_command import run_digital_life_shell_command


@dataclass(frozen=True)
class ResidentSupervisionContext:
    terminal_dir: Path
    language_dir: Path
    relationship_dir: Path
    body_rhythm_pulse: dict[str, Any]
    need_state_vector: dict[str, Any]
    body_resource_budget: dict[str, Any]
    core_affect_vector: dict[str, Any]
    safe_terminal_loop: dict[str, Any]
    terminal_life_loop_state: dict[str, Any]
    life_context_frame: dict[str, Any]
    relation_turn_frame: dict[str, Any]
    shared_term_registry: dict[str, Any]
    self_narrative_trace: dict[str, Any]
    commitment_index: dict[str, Any]
    expression_plan: dict[str, Any]
    relationship_graph: dict[str, Any]
    relationship_timeline: dict[str, Any]
    commitment_expression_plan: dict[str, Any]
    apology_repair_language_trace: dict[str, Any]
    replay_cue_bundle: dict[str, Any]
    offline_consolidation_frame: dict[str, Any]
    growth_patch_candidate_queue: dict[str, Any]
    replay_cue_bundle_ref: str | None
    offline_consolidation_frame_ref: str | None
    growth_patch_candidate_queue_ref: str | None
    growth_patch_candidate_ids: list[str]
    replay_residue_ref_count: int
    dream_window_ref_count: int
    growth_patch_candidate_count: int
    relaunch_recovery_count: int
    last_relaunch_recovery_report_ref: str | None
    heartbeat_counter: int


@dataclass(frozen=True)
class ResidentSupervisionBootstrapResult:
    exit_code: int
    report: dict[str, Any]
    context: ResidentSupervisionContext | None


def bootstrap_resident_supervision(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str,
    generated_at: str,
    strict: bool,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    read_json: Callable[[Path], dict[str, Any]],
    read_json_if_exists: Callable[[Path], dict[str, Any]],
    write_json: Callable[[Path, dict[str, Any]], None],
    now_iso: Callable[[], str],
) -> ResidentSupervisionBootstrapResult:
    terminal_dir = state_dir / "terminal"
    previous_safe_terminal_loop = read_json_if_exists(terminal_dir / "safe_terminal_loop_state.json")
    previous_terminal_life_loop_state = read_json_if_exists(
        terminal_dir / "terminal_life_loop_state.json"
    )

    shell_result = run_digital_life_shell_command(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=f"{run_id}-restore",
        strict=strict,
    )
    if shell_result.exit_code != 0:
        return ResidentSupervisionBootstrapResult(
            exit_code=shell_result.exit_code,
            report=shell_result.report,
            context=None,
        )

    language_dir = state_dir / "language"
    relationship_dir = state_dir / "relationship"
    body_dir = state_dir / "body"

    read_json(terminal_dir / "session_envelope.json")
    safe_terminal_loop = read_json(terminal_dir / "safe_terminal_loop_state.json")
    terminal_life_loop_state = read_json(terminal_dir / "terminal_life_loop_state.json")
    body_rhythm_pulse = read_json_if_exists(body_dir / "body_rhythm_pulse.json")
    need_state_vector = read_json_if_exists(body_dir / "need_state_vector.json")
    body_resource_budget = read_json_if_exists(body_dir / "body_resource_budget.json")
    core_affect_vector = read_json_if_exists(body_dir / "core_affect_vector.json")
    life_context_frame = read_json_if_exists(terminal_dir / "life_context_frame.json")
    relation_turn_frame = read_json_if_exists(terminal_dir / "relation_turn_frame.json")
    shared_term_registry = read_json(language_dir / "shared_term_registry.json")
    self_narrative_trace = read_json(language_dir / "self_narrative_language_trace.json")
    commitment_index = read_json(language_dir / "commitment_repair_language_index.json")
    commitment_expression_plan = read_json_if_exists(language_dir / "commitment_expression_plan.json")
    apology_repair_language_trace = read_json_if_exists(language_dir / "apology_repair_language_trace.json")
    expression_plan = read_json_if_exists(language_dir / "expression_plan.json")
    relationship_graph = read_json(relationship_dir / "relationship_subject_graph.json")
    relationship_timeline = read_json_if_exists(relationship_dir / "relationship_timeline.json")
    replay_cue_bundle = read_json_if_exists(state_dir / "replay" / "replay_cue_bundle.json")
    offline_consolidation_frame = read_json_if_exists(
        state_dir / "dream" / "offline_consolidation_frame.json"
    )
    growth_patch_candidate_queue = read_json_if_exists(
        state_dir / "growth" / "growth_patch_candidate_queue.json"
    )

    replay_cue_bundle_ref = _ref_if_present(
        payload=replay_cue_bundle,
        ref="runtime/state/replay/replay_cue_bundle.json",
    )
    offline_consolidation_frame_ref = _ref_if_present(
        payload=offline_consolidation_frame,
        ref="runtime/state/dream/offline_consolidation_frame.json",
    )
    growth_patch_candidate_queue_ref = _ref_if_present(
        payload=growth_patch_candidate_queue,
        ref="runtime/state/growth/growth_patch_candidate_queue.json",
    )
    growth_patch_candidate_ids = [
        candidate.get("growth_patch_candidate_id")
        for candidate in growth_patch_candidate_queue.get("candidates", [])
        if isinstance(candidate, dict) and candidate.get("growth_patch_candidate_id")
    ]
    replay_residue_ref_count = len(replay_cue_bundle.get("turn_residue_refs", []))
    dream_window_ref_count = len(offline_consolidation_frame.get("dream_window_refs", []))
    growth_patch_candidate_count = len(growth_patch_candidate_queue.get("candidates", []))

    relaunch_recovery_count = 0
    last_relaunch_recovery_report_ref: str | None = None
    relaunch_recovery_report = detect_and_normalize_interrupted_previous_state(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        previous_safe_terminal_loop=previous_safe_terminal_loop,
        previous_terminal_life_loop_state=previous_terminal_life_loop_state,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        write_json=write_json,
    )
    if relaunch_recovery_report is not None:
        relaunch_recovery_count = 1
        last_relaunch_recovery_report_ref = (
            "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json"
        )
        safe_terminal_loop["last_relaunch_recovery_report_ref"] = last_relaunch_recovery_report_ref
        terminal_life_loop_state["last_relaunch_recovery_report_ref"] = (
            last_relaunch_recovery_report_ref
        )
        record_recovery_continuity(
            self_narrative_trace=self_narrative_trace,
            commitment_index=commitment_index,
            relationship_graph=relationship_graph,
            event_kind="relaunch_recovery_normalization",
            report_ref=last_relaunch_recovery_report_ref,
            details={
                "previous_safe_terminal_mode": relaunch_recovery_report.get(
                    "previous_safe_terminal_mode"
                ),
                "previous_terminal_loop_mode": relaunch_recovery_report.get(
                    "previous_terminal_loop_mode"
                ),
                "normalized_mode": relaunch_recovery_report.get("normalized_mode"),
            },
        )
        write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)
        write_json(language_dir / "commitment_repair_language_index.json", commitment_index)
        write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    reports_dir.mkdir(parents=True, exist_ok=True)
    heartbeat_counter = write_waiting_heartbeat(
        run_id=run_id,
        generated_at=generated_at,
        terminal_dir=terminal_dir,
        reports_dir=reports_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        relationship_graph=relationship_graph,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        now_iso=now_iso,
        write_json=write_json,
    )

    context = ResidentSupervisionContext(
        terminal_dir=terminal_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        life_context_frame=life_context_frame,
        relation_turn_frame=relation_turn_frame,
        shared_term_registry=shared_term_registry,
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        expression_plan=expression_plan,
        relationship_graph=relationship_graph,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        relaunch_recovery_count=relaunch_recovery_count,
        last_relaunch_recovery_report_ref=last_relaunch_recovery_report_ref,
        heartbeat_counter=heartbeat_counter,
    )
    return ResidentSupervisionBootstrapResult(
        exit_code=0,
        report=shell_result.report,
        context=context,
    )


def _ref_if_present(*, payload: dict[str, Any], ref: str) -> str | None:
    if not payload:
        return None
    return ref
