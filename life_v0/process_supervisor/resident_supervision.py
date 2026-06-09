from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..language.apology_repair_language import build_apology_repair_language_trace
from ..language.apology_repair_language import (
    project_apology_repair_language_trace_with_offline_learning,
)
from ..language.commitment_expression import build_commitment_expression_plan
from ..language.commitment_expression import (
    project_commitment_expression_plan_with_offline_learning,
)
from ..language.dialogue_log import collect_dialogue_turn_refs
from ..language.relationship_timeline import build_relationship_timeline
from ..language.relationship_timeline import (
    project_relationship_timeline_with_offline_learning,
)
from .heartbeat import write_waiting_heartbeat
from .incident_recovery import record_recovery_continuity
from .offline_learning_signals import (
    BELIEF_LEARNING_PLAN_REF,
    LANGUAGE_LEARNING_PLAN_REF,
    NIGHTMARE_RISK_REF,
    RELATIONSHIP_LEARNING_PLAN_REF,
)
from .continuity_evolution import evolve_relationship_and_self_model
from .relaunch_recovery import detect_and_normalize_interrupted_previous_state
from ..shell_command import run_digital_life_shell_command
from ..state_store.life_state import project_responsibility_language_continuity
from ..state_store.relationship_memory import project_relationship_memory


@dataclass(frozen=True)
class ResidentSupervisionContext:
    terminal_dir: Path
    language_dir: Path
    relationship_dir: Path
    body_rhythm_pulse: dict[str, Any]
    need_state_vector: dict[str, Any]
    body_resource_budget: dict[str, Any]
    core_affect_vector: dict[str, Any]
    self_model_state: dict[str, Any]
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
    nightmare_risk: dict[str, Any]
    belief_learning_plan: dict[str, Any]
    language_learning_plan: dict[str, Any]
    relationship_learning_plan: dict[str, Any]
    responsibility_loop_state: dict[str, Any]
    world_contact_summary: dict[str, Any]
    pain_regret_repair_report: dict[str, Any]
    replay_cue_bundle_ref: str | None
    offline_consolidation_frame_ref: str | None
    growth_patch_candidate_queue_ref: str | None
    nightmare_risk_ref: str | None
    belief_learning_plan_ref: str | None
    language_learning_plan_ref: str | None
    relationship_learning_plan_ref: str | None
    responsibility_loop_state_ref: str | None
    world_contact_summary_ref: str | None
    pain_regret_repair_report_ref: str | None
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
    self_model_state = read_json_if_exists(state_dir / "self" / "self_model.json")
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
    responsibility_loop_state = read_json_if_exists(
        state_dir / "action" / "responsibility_loop_state.json"
    )
    commitment_truth_state = read_json_if_exists(
        state_dir / "relationship" / "commitment_truth_state.json"
    )
    responsibility_ledger = read_json_if_exists(
        state_dir / "responsibility" / "responsibility_ledger.json"
    )
    relationship_memory = read_json_if_exists(
        state_dir / "memory" / "relationship_memory.json"
    )
    life_state = read_json_if_exists(state_dir / "life_state.json")
    world_contact_summary = read_json_if_exists(
        state_dir / "membrane" / "world_contact_summary.json"
    )
    replay_cue_bundle = read_json_if_exists(state_dir / "replay" / "replay_cue_bundle.json")
    offline_consolidation_frame = read_json_if_exists(
        state_dir / "dream" / "offline_consolidation_frame.json"
    )
    growth_patch_candidate_queue = read_json_if_exists(
        state_dir / "growth" / "growth_patch_candidate_queue.json"
    )
    nightmare_risk = read_json_if_exists(state_dir / "dream" / "nightmare_loop_risk.json")
    belief_learning_plan = read_json_if_exists(
        state_dir / "growth" / "belief_learning_plan.json"
    )
    language_learning_plan = read_json_if_exists(
        state_dir / "growth" / "language_learning_plan.json"
    )
    relationship_learning_plan = read_json_if_exists(
        state_dir / "growth" / "relationship_learning_plan.json"
    )
    pain_regret_repair_report = read_json_if_exists(
        reports_dir / "pain_regret_repair_report.json"
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
    nightmare_risk_ref = _ref_if_present(
        payload=nightmare_risk,
        ref=NIGHTMARE_RISK_REF,
    )
    belief_learning_plan_ref = _ref_if_present(
        payload=belief_learning_plan,
        ref=BELIEF_LEARNING_PLAN_REF,
    )
    language_learning_plan_ref = _ref_if_present(
        payload=language_learning_plan,
        ref=LANGUAGE_LEARNING_PLAN_REF,
    )
    relationship_learning_plan_ref = _ref_if_present(
        payload=relationship_learning_plan,
        ref=RELATIONSHIP_LEARNING_PLAN_REF,
    )
    responsibility_loop_state_ref = _ref_if_present(
        payload=responsibility_loop_state,
        ref="runtime/state/action/responsibility_loop_state.json",
    )
    world_contact_summary_ref = _ref_if_present(
        payload=world_contact_summary,
        ref="runtime/state/membrane/world_contact_summary.json",
    )
    pain_regret_repair_report_ref = _ref_if_present(
        payload=pain_regret_repair_report,
        ref="runtime/reports/latest/pain_regret_repair_report.json",
    )
    relationship_timeline = project_relationship_timeline_with_offline_learning(
        relationship_timeline=relationship_timeline,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    commitment_expression_plan = project_commitment_expression_plan_with_offline_learning(
        commitment_expression_plan=commitment_expression_plan,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    apology_repair_language_trace = project_apology_repair_language_trace_with_offline_learning(
        apology_repair_language_trace=apology_repair_language_trace,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    relationship_memory = project_relationship_memory(
        relationship_memory=relationship_memory,
        relationship_graph=relationship_graph,
        relationship_timeline=relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        commitment_repair_index=commitment_index,
        last_contact_refs=list(relationship_memory.get("last_contact_refs", [])),
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
    )
    life_state = project_responsibility_language_continuity(
        life_state=life_state,
        self_model_state=self_model_state,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        relationship_memory=relationship_memory,
        relationship_graph=relationship_graph,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop_state,
        commitment_repair_index=commitment_index,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        additional_runtime_trace_refs=[
            ref
            for ref in [
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
            ]
            if ref
        ],
    )
    continuity_refresh = _refresh_bootstrap_long_horizon_continuity(
        generated_at=generated_at,
        state_dir=state_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        expression_plan=expression_plan,
        commitment_index=commitment_index,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop_state,
        relationship_memory=relationship_memory,
        life_state=life_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        source_doc_refs=source_doc_refs,
    )
    relationship_graph = continuity_refresh["relationship_graph"]
    self_model_state = continuity_refresh["self_model_state"]
    relationship_timeline = continuity_refresh["relationship_timeline"]
    commitment_expression_plan = continuity_refresh["commitment_expression_plan"]
    apology_repair_language_trace = continuity_refresh["apology_repair_language_trace"]
    relationship_memory = continuity_refresh["relationship_memory"]
    life_state = continuity_refresh["life_state"]
    write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)
    write_json(relationship_dir / "relationship_timeline.json", relationship_timeline)
    write_json(language_dir / "commitment_expression_plan.json", commitment_expression_plan)
    write_json(
        language_dir / "apology_repair_language_trace.json",
        apology_repair_language_trace,
    )
    write_json(state_dir / "memory" / "relationship_memory.json", relationship_memory)
    write_json(state_dir / "self" / "self_model.json", self_model_state)
    write_json(state_dir / "life_state.json", life_state)
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
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
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
        self_model_state=self_model_state,
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
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
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
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
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


def _refresh_bootstrap_long_horizon_continuity(
    *,
    generated_at: str,
    state_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    relationship_graph: dict[str, Any],
    self_model_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    apology_repair_language_trace: dict[str, Any],
    expression_plan: dict[str, Any],
    commitment_index: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    responsibility_loop_state: dict[str, Any],
    relationship_memory: dict[str, Any],
    life_state: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
    nightmare_risk: dict[str, Any],
    belief_learning_plan: dict[str, Any],
    language_learning_plan: dict[str, Any],
    relationship_learning_plan: dict[str, Any],
    nightmare_risk_ref: str | None,
    belief_learning_plan_ref: str | None,
    language_learning_plan_ref: str | None,
    relationship_learning_plan_ref: str | None,
    source_doc_refs: list[str],
) -> dict[str, dict[str, Any]]:
    dialogue_turn_refs = collect_dialogue_turn_refs(language_dir / "dialogue_turn_log.jsonl", [])
    dialogue_turn_entries = [{"dialogue_turn_ref": ref} for ref in dialogue_turn_refs]

    first_pass_relationship_timeline = build_relationship_timeline(
        run_id=str(
            relationship_timeline.get("run_id")
            or commitment_expression_plan.get("run_id")
            or "resident-supervision-bootstrap"
        ),
        generated_at=generated_at,
        relationship_graph=relationship_graph,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        dialogue_turn_entries=dialogue_turn_entries,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=list(relationship_timeline.get("source_doc_refs", [])) or source_doc_refs,
    )
    first_pass_commitment_expression_plan = build_commitment_expression_plan(
        run_id=str(
            commitment_expression_plan.get("run_id")
            or first_pass_relationship_timeline.get("run_id")
            or "resident-supervision-bootstrap"
        ),
        generated_at=generated_at,
        expression_plan=expression_plan,
        commitment_repair_index=commitment_index,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=first_pass_relationship_timeline,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=list(commitment_expression_plan.get("source_doc_refs", []))
        or source_doc_refs,
    )
    first_pass_apology_repair_language_trace = build_apology_repair_language_trace(
        run_id=str(
            apology_repair_language_trace.get("run_id")
            or first_pass_commitment_expression_plan.get("run_id")
            or "resident-supervision-bootstrap"
        ),
        generated_at=generated_at,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=first_pass_relationship_timeline,
        commitment_expression_plan=first_pass_commitment_expression_plan,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=list(apology_repair_language_trace.get("source_doc_refs", []))
        or source_doc_refs,
    )
    evolved_continuity = evolve_relationship_and_self_model(
        generated_at=generated_at,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state,
        relationship_timeline=first_pass_relationship_timeline,
        commitment_expression_plan=first_pass_commitment_expression_plan,
        apology_repair_language_trace=first_pass_apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    evolved_relationship_graph = evolved_continuity["relationship_graph"]
    evolved_self_model_state = evolved_continuity["self_model_state"]

    refreshed_relationship_timeline = build_relationship_timeline(
        run_id=str(
            relationship_timeline.get("run_id")
            or commitment_expression_plan.get("run_id")
            or "resident-supervision-bootstrap"
        ),
        generated_at=generated_at,
        relationship_graph=evolved_relationship_graph,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        dialogue_turn_entries=dialogue_turn_entries,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=list(relationship_timeline.get("source_doc_refs", [])) or source_doc_refs,
    )
    refreshed_commitment_expression_plan = build_commitment_expression_plan(
        run_id=str(
            commitment_expression_plan.get("run_id")
            or refreshed_relationship_timeline.get("run_id")
            or "resident-supervision-bootstrap"
        ),
        generated_at=generated_at,
        expression_plan=expression_plan,
        commitment_repair_index=commitment_index,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=refreshed_relationship_timeline,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=list(commitment_expression_plan.get("source_doc_refs", []))
        or source_doc_refs,
    )
    refreshed_apology_repair_language_trace = build_apology_repair_language_trace(
        run_id=str(
            apology_repair_language_trace.get("run_id")
            or refreshed_commitment_expression_plan.get("run_id")
            or "resident-supervision-bootstrap"
        ),
        generated_at=generated_at,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_expression_plan=refreshed_commitment_expression_plan,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=list(apology_repair_language_trace.get("source_doc_refs", []))
        or source_doc_refs,
    )
    refreshed_relationship_memory = project_relationship_memory(
        relationship_memory=relationship_memory,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        commitment_repair_index=commitment_index,
        last_contact_refs=list(relationship_memory.get("last_contact_refs", [])),
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
    )
    refreshed_life_state = project_responsibility_language_continuity(
        life_state=life_state,
        self_model_state=evolved_self_model_state,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        relationship_memory=refreshed_relationship_memory,
        relationship_graph=evolved_relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_expression_plan=refreshed_commitment_expression_plan,
        apology_repair_language_trace=refreshed_apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop_state,
        commitment_repair_index=commitment_index,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        additional_runtime_trace_refs=[
            ref
            for ref in [
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
            ]
            if ref
        ],
    )
    return {
        "relationship_graph": evolved_relationship_graph,
        "self_model_state": evolved_self_model_state,
        "relationship_timeline": refreshed_relationship_timeline,
        "commitment_expression_plan": refreshed_commitment_expression_plan,
        "apology_repair_language_trace": refreshed_apology_repair_language_trace,
        "relationship_memory": refreshed_relationship_memory,
        "life_state": refreshed_life_state,
    }


def _ref_if_present(*, payload: dict[str, Any], ref: str) -> str | None:
    if not payload:
        return None
    return ref
