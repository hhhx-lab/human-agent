from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

from .dialogue_events import build_external_turn_event, build_life_turn_event
from .idle_strategy import IDLE_STRATEGY_STATE_REF
from .live_turn_cycle import run_live_turn_cycle
from .process_closeout import close_digital_life_process
from .process_lease import (
    RESIDENT_PROCESS_LEASE_HISTORY_REF,
    RESIDENT_PROCESS_LEASE_REF,
    close_resident_process_lease,
    open_resident_process_lease,
)
from .process_session_loop import run_process_session_loop
from .resident_supervision import bootstrap_resident_supervision
from .response_surface import compose_life_response
from .terminal_ui import (
    extract_life_response_text,
    render_digital_life_banner,
    render_life_cycle_output,
    render_life_opening,
)
from ..runtime_config import write_digital_life_runtime_config_snapshot


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
    "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "docs/90_language_event_examples_and_timeline_bundle.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
    "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
    "docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md",
    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "RunnerCliRuntime",
    "ComputerPeripheralRuntime",
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
]

# Keep these names as compatibility shims while the organ split settles into the
# wider process-supervisor test and patch surface.
_build_external_turn_event = build_external_turn_event
_build_life_turn_event = build_life_turn_event
_compose_life_response = compose_life_response


@dataclass(frozen=True)
class DigitalLifeProcessResult:
    exit_code: int
    report: dict[str, Any]


def run_digital_life_process(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> DigitalLifeProcessResult:
    run_id = run_id or _default_run_id("digital-life-process-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    input_stream = input_stream or sys.stdin
    output_stream = output_stream or sys.stdout

    try:
        write_digital_life_runtime_config_snapshot(
            repo_root=Path.cwd(),
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=run_id,
            generated_at=generated_at,
            strict=strict,
            write_json=_write_json,
        )
    except ValueError as exc:
        return DigitalLifeProcessResult(
            exit_code=2,
            report={
                "schema_version": "digital_life_process_report_v0",
                "run_id": run_id,
                "generated_at": generated_at,
                "status": "blocked",
                "blocked_reasons": [str(exc)],
                "runtime_config_error": str(exc),
            },
        )

    resident_supervision = bootstrap_resident_supervision(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=run_id,
        generated_at=generated_at,
        strict=strict,
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
        read_json=_read_json,
        read_json_if_exists=_read_json_if_exists,
        write_json=_write_json,
        now_iso=_now_iso,
    )
    if resident_supervision.exit_code != 0 or resident_supervision.context is None:
        return DigitalLifeProcessResult(
            exit_code=resident_supervision.exit_code,
            report=resident_supervision.report,
        )

    supervision = resident_supervision.context
    terminal_dir = supervision.terminal_dir
    language_dir = supervision.language_dir
    relationship_dir = supervision.relationship_dir
    body_rhythm_pulse = supervision.body_rhythm_pulse
    need_state_vector = supervision.need_state_vector
    body_resource_budget = supervision.body_resource_budget
    core_affect_vector = supervision.core_affect_vector
    self_model_state = supervision.self_model_state
    safe_terminal_loop = supervision.safe_terminal_loop
    terminal_life_loop_state = supervision.terminal_life_loop_state
    life_context_frame = supervision.life_context_frame
    relation_turn_frame = supervision.relation_turn_frame
    shared_term_registry = supervision.shared_term_registry
    self_narrative_trace = supervision.self_narrative_trace
    commitment_index = supervision.commitment_index
    expression_plan = supervision.expression_plan
    relationship_graph = supervision.relationship_graph
    relationship_timeline = supervision.relationship_timeline
    commitment_expression_plan = supervision.commitment_expression_plan
    apology_repair_language_trace = supervision.apology_repair_language_trace
    replay_cue_bundle = supervision.replay_cue_bundle
    offline_consolidation_frame = supervision.offline_consolidation_frame
    dream_experience_window = supervision.dream_experience_window
    wake_integration_frame = supervision.wake_integration_frame
    dream_fact_gate_decision = supervision.dream_fact_gate_decision
    growth_patch_candidate_queue = supervision.growth_patch_candidate_queue
    nightmare_risk = supervision.nightmare_risk
    belief_learning_plan = supervision.belief_learning_plan
    language_learning_plan = supervision.language_learning_plan
    relationship_learning_plan = supervision.relationship_learning_plan
    offline_learning_cumulative_profile = supervision.offline_learning_cumulative_profile
    signal_media_runtime = supervision.signal_media_runtime
    belief_state = supervision.belief_state
    prediction_error_field = supervision.prediction_error_field
    active_sampling_plan = supervision.active_sampling_plan
    memory_write_gate = supervision.memory_write_gate
    state_merge_guard = supervision.state_merge_guard
    schema_cross_file_logic = supervision.schema_cross_file_logic
    schema_run_manifest = supervision.schema_run_manifest
    workspace_frame = supervision.workspace_frame
    broadcast_frame = supervision.broadcast_frame
    metacognition_state = supervision.metacognition_state
    consciousness_probe = supervision.consciousness_probe
    birth_readiness_rollup = supervision.birth_readiness_rollup
    birth_readiness_stage_gate = supervision.birth_readiness_stage_gate
    responsibility_loop_state = supervision.responsibility_loop_state
    world_contact_summary = supervision.world_contact_summary
    pain_regret_repair_report = supervision.pain_regret_repair_report
    replay_cue_bundle_ref = supervision.replay_cue_bundle_ref
    offline_consolidation_frame_ref = supervision.offline_consolidation_frame_ref
    dream_experience_window_ref = supervision.dream_experience_window_ref
    wake_integration_frame_ref = supervision.wake_integration_frame_ref
    dream_fact_gate_decision_ref = supervision.dream_fact_gate_decision_ref
    growth_patch_candidate_queue_ref = supervision.growth_patch_candidate_queue_ref
    nightmare_risk_ref = supervision.nightmare_risk_ref
    belief_learning_plan_ref = supervision.belief_learning_plan_ref
    language_learning_plan_ref = supervision.language_learning_plan_ref
    relationship_learning_plan_ref = supervision.relationship_learning_plan_ref
    signal_media_runtime_ref = supervision.signal_media_runtime_ref
    belief_state_ref = supervision.belief_state_ref
    prediction_error_field_ref = supervision.prediction_error_field_ref
    active_sampling_plan_ref = supervision.active_sampling_plan_ref
    memory_write_gate_ref = supervision.memory_write_gate_ref
    state_merge_guard_ref = supervision.state_merge_guard_ref
    schema_cross_file_logic_ref = supervision.schema_cross_file_logic_ref
    schema_run_manifest_ref = supervision.schema_run_manifest_ref
    workspace_frame_ref = supervision.workspace_frame_ref
    broadcast_frame_ref = supervision.broadcast_frame_ref
    metacognition_state_ref = supervision.metacognition_state_ref
    consciousness_probe_ref = supervision.consciousness_probe_ref
    birth_readiness_rollup_ref = supervision.birth_readiness_rollup_ref
    birth_readiness_stage_gate_ref = supervision.birth_readiness_stage_gate_ref
    responsibility_loop_state_ref = supervision.responsibility_loop_state_ref
    world_contact_summary_ref = supervision.world_contact_summary_ref
    pain_regret_repair_report_ref = supervision.pain_regret_repair_report_ref
    background_convergence_summary_ref = supervision.background_convergence_summary_ref
    background_convergence_history_ref = supervision.background_convergence_history_ref
    growth_patch_candidate_ids = supervision.growth_patch_candidate_ids
    replay_residue_ref_count = supervision.replay_residue_ref_count
    dream_window_ref_count = supervision.dream_window_ref_count
    growth_patch_candidate_count = supervision.growth_patch_candidate_count
    relaunch_recovery_count = supervision.relaunch_recovery_count
    last_relaunch_recovery_report_ref = supervision.last_relaunch_recovery_report_ref
    heartbeat_counter = supervision.heartbeat_counter
    open_resident_process_lease(
        run_id=run_id,
        generated_at=generated_at,
        terminal_dir=terminal_dir,
        write_json=_write_json,
    )

    life_name = _life_name_from_state_dir(state_dir)
    _print_line(
        output_stream,
        render_digital_life_banner(
            life_name=life_name,
            status="foreground_life_loop",
        ),
    )
    _print_line(
        output_stream,
        render_life_opening(
            {
                "status": "foreground_life_loop",
                "resident_waiting_mode": terminal_life_loop_state.get(
                    "current_mode",
                    "restored_waiting_for_external_turn",
                ),
                "resident_waiting_heartbeat_counter": heartbeat_counter,
            },
            life_name=life_name,
        ),
    )

    session_loop = run_process_session_loop(
        run_id=run_id,
        generated_at=generated_at,
        input_stream=input_stream,
        terminal_dir=terminal_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        reports_dir=reports_dir,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        self_model_state=self_model_state,
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
        dream_experience_window=dream_experience_window,
        wake_integration_frame=wake_integration_frame,
        dream_fact_gate_decision=dream_fact_gate_decision,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=memory_write_gate,
        state_merge_guard=state_merge_guard,
        schema_cross_file_logic=schema_cross_file_logic,
        schema_run_manifest=schema_run_manifest,
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        metacognition_state=metacognition_state,
        consciousness_probe=consciousness_probe,
        birth_readiness_rollup=birth_readiness_rollup,
        birth_readiness_stage_gate=birth_readiness_stage_gate,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        dream_experience_window_ref=dream_experience_window_ref,
        wake_integration_frame_ref=wake_integration_frame_ref,
        dream_fact_gate_decision_ref=dream_fact_gate_decision_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        signal_media_runtime_ref=signal_media_runtime_ref,
        belief_state_ref=belief_state_ref,
        prediction_error_field_ref=prediction_error_field_ref,
        active_sampling_plan_ref=active_sampling_plan_ref,
        memory_write_gate_ref=memory_write_gate_ref,
        state_merge_guard_ref=state_merge_guard_ref,
        schema_cross_file_logic_ref=schema_cross_file_logic_ref,
        schema_run_manifest_ref=schema_run_manifest_ref,
        workspace_frame_ref=workspace_frame_ref,
        broadcast_frame_ref=broadcast_frame_ref,
        metacognition_state_ref=metacognition_state_ref,
        consciousness_probe_ref=consciousness_probe_ref,
        birth_readiness_rollup_ref=birth_readiness_rollup_ref,
        birth_readiness_stage_gate_ref=birth_readiness_stage_gate_ref,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        heartbeat_counter=heartbeat_counter,
        turn_counter=_current_dialogue_turn_count(language_dir / "dialogue_turn_log.jsonl"),
        emit_output=lambda text: _emit_life_output(
            output_stream=output_stream,
            input_stream=input_stream,
            text=text,
            life_name=life_name,
        ),
        now_iso=_now_iso,
        write_json=_write_json,
        append_jsonl=_append_jsonl,
        run_live_turn_cycle_fn=lambda **kwargs: run_live_turn_cycle(
            **kwargs,
            build_external_turn_event_fn=_build_external_turn_event,
            compose_life_response_fn=_compose_life_response,
            build_life_turn_event_fn=_build_life_turn_event,
        ),
    )

    idle_strategy_state = _read_json_if_exists(terminal_dir / "idle_strategy_state.json")
    expression_plan = _read_json_if_exists(language_dir / "expression_plan.json")
    close_resident_process_lease(
        run_id=run_id,
        generated_at=_now_iso(),
        terminal_dir=terminal_dir,
        heartbeat_counter=session_loop.heartbeat_counter,
        completed_turns=session_loop.completed_turns,
        incident_count=session_loop.incident_count,
        exit_reason=session_loop.exit_reason,
        write_json=_write_json,
    )
    closeout = close_digital_life_process(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        heartbeat_counter=session_loop.heartbeat_counter,
        completed_turns=session_loop.completed_turns,
        incident_count=session_loop.incident_count,
        relaunch_recovery_count=relaunch_recovery_count,
        exit_reason=session_loop.exit_reason,
        last_incident_report_ref=session_loop.last_incident_report_ref,
        last_recovery_report_ref=session_loop.last_recovery_report_ref,
        last_relaunch_recovery_report_ref=last_relaunch_recovery_report_ref,
        last_external_turn=session_loop.last_external_turn,
        last_life_turn=session_loop.last_life_turn,
        waiting_mode=session_loop.terminal_life_loop_state.get(
            "current_mode", "restored_waiting_for_external_turn"
        ),
        idle_strategy_ref=IDLE_STRATEGY_STATE_REF,
        idle_strategy_state=idle_strategy_state,
        terminal_life_loop_state=session_loop.terminal_life_loop_state,
        last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
        last_dialogue_packet_ref=session_loop.safe_terminal_loop.get("last_dialogue_packet_ref"),
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
        life_context_frame=life_context_frame,
        relation_turn_frame=relation_turn_frame,
        expression_plan=expression_plan,
        relationship_graph=session_loop.relationship_graph,
        self_model_state=session_loop.self_model_state,
        relationship_timeline=session_loop.relationship_timeline,
        commitment_expression_plan=session_loop.commitment_expression_plan,
        apology_repair_language_trace=session_loop.apology_repair_language_trace,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        dream_experience_window_ref=dream_experience_window_ref,
        wake_integration_frame_ref=wake_integration_frame_ref,
        dream_fact_gate_decision_ref=dream_fact_gate_decision_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        signal_media_runtime_ref=signal_media_runtime_ref,
        belief_state_ref=belief_state_ref,
        prediction_error_field_ref=prediction_error_field_ref,
        active_sampling_plan_ref=active_sampling_plan_ref,
        memory_write_gate_ref=memory_write_gate_ref,
        state_merge_guard_ref=state_merge_guard_ref,
        background_convergence_summary_ref=background_convergence_summary_ref,
        background_convergence_history_ref=background_convergence_history_ref,
        resident_process_lease_ref=RESIDENT_PROCESS_LEASE_REF,
        resident_process_lease_history_ref=RESIDENT_PROCESS_LEASE_HISTORY_REF,
        write_json=_write_json,
    )
    return DigitalLifeProcessResult(exit_code=0, report=closeout.report_bundle.report)


def _current_dialogue_turn_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])


def _append_jsonl(path: Path, payloads: list[dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for payload in payloads:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _print_line(stream: TextIO, text: str) -> None:
    stream.write(text + "\n")
    stream.flush()


def _emit_life_output(
    *,
    output_stream: TextIO,
    input_stream: TextIO,
    text: str,
    life_name: str | None = None,
) -> None:
    if extract_life_response_text(text):
        _print_line(output_stream, render_life_cycle_output(text, life_name=life_name))
    record_output = getattr(input_stream, "record_output", None)
    if callable(record_output):
        record_output(text)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _life_name_from_state_dir(state_dir: Path) -> str | None:
    registry = _read_json_if_exists(state_dir / "identity" / "life_name_registry.json")
    name = str(registry.get("canonical_name") or "").strip()
    return name or None


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
