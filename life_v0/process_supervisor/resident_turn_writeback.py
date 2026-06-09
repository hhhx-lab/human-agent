from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..growth.offline_learning_profile import (
    BELIEF_LEARNING_PLAN_REF,
    LANGUAGE_LEARNING_PLAN_REF,
    NIGHTMARE_RISK_REF,
    RELATIONSHIP_LEARNING_PLAN_REF,
)
from ..language.apology_repair_language import build_apology_repair_language_trace
from ..language.commitment_expression import build_commitment_expression_plan
from ..language.dialogue_log import collect_dialogue_turn_refs
from ..language.relationship_timeline import build_relationship_timeline
from ..state_store.life_state import project_responsibility_language_continuity
from ..state_store.relationship_memory import project_relationship_memory
from ..terminal_loop.dialogue_writeback import build_dialogue_writeback_bundle
from ..terminal_loop.persistent_wait_bridge import build_persistent_wait_bridge


DIALOGUE_LOG_REF = "runtime/state/language/dialogue_turn_log.jsonl"
SAFE_TERMINAL_LOOP_REF = "runtime/state/terminal/safe_terminal_loop_state.json"
TERMINAL_LIFE_LOOP_REF = "runtime/state/terminal/terminal_life_loop_state.json"
RELATIONSHIP_GRAPH_REF = "runtime/state/relationship/relationship_subject_graph.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
RELATIONSHIP_MEMORY_REF = "runtime/state/memory/relationship_memory.json#shared_memory_refs"
RELATIONSHIP_REPAIR_HISTORY_REF = "runtime/state/memory/relationship_memory.json#repair_history_refs"
RELATIONSHIP_MEMORY_OFFLINE_REF = "runtime/state/memory/relationship_memory.json#offline_learning_refs"
COMMITMENT_EXPRESSION_PLAN_REF = "runtime/state/language/commitment_expression_plan.json"
APOLOGY_REPAIR_LANGUAGE_TRACE_REF = "runtime/state/language/apology_repair_language_trace.json"
COMMITMENT_TRUTH_OPEN_REF = "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs"
COMMITMENT_TRUTH_REPAIR_REF = "runtime/state/relationship/commitment_truth_state.json#repair_required_refs"
RESPONSIBILITY_EVENT_REF = "runtime/state/responsibility/responsibility_ledger.json#responsibility_events"
RESPONSIBILITY_OBLIGATION_REF = "runtime/state/responsibility/responsibility_ledger.json#repair_obligations"
LIFE_STATE_RESPONSIBILITY_REF = "runtime/state/life_state.json#responsibility_bindings"
LIFE_STATE_REGRET_REF = "runtime/state/life_state.json#regret_events"
LIFE_STATE_PAIN_REF = "runtime/state/life_state.json#pain_events"
LIFE_STATE_RELATIONSHIP_MEMORY_REF = "runtime/state/life_state.json#memory_index.relationship_memory_refs"
LIFE_STATE_RESPONSIBILITY_MEMORY_REF = "runtime/state/life_state.json#memory_index.responsibility_memory_refs"
LIFE_STATE_DREAM_MEMORY_REF = "runtime/state/life_state.json#memory_index.dream_memory_refs"
LIFE_STATE_LANGUAGE_OFFLINE_REF = "runtime/state/life_state.json#language_state.offline_learning_refs"
LIFE_STATE_RELATIONSHIP_SUBJECTS_REF = "runtime/state/life_state.json#relationship_subjects"
DIALOGUE_WRITEBACK_BUNDLE_REF = "runtime/reports/latest/dialogue_writeback_bundle.json"
RESUMED_DIALOGUE_PACKET_REF = "runtime/reports/latest/resumed_external_dialogue_packet.json"


@dataclass(frozen=True)
class ResidentTurnWritebackResult:
    safe_terminal_loop: dict[str, Any]
    terminal_life_loop_state: dict[str, Any]
    dialogue_writeback_bundle: dict[str, Any]
    resumed_dialogue_packet: dict[str, Any]
    external_turn_ref: str
    life_turn_ref: str
    last_external_turn: dict[str, Any]
    last_life_turn: dict[str, Any]


def write_resident_turn_writeback(
    *,
    run_id: str,
    terminal_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    reports_dir: Path,
    turn_counter: int,
    external_turn_id: str,
    life_turn_id: str,
    external_turn: dict[str, Any],
    life_turn: dict[str, Any],
    external_utterance: str,
    life_response: str,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle_ref: str | None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    append_jsonl: Callable[[Path, list[dict[str, Any]]], None],
) -> ResidentTurnWritebackResult:
    append_jsonl(language_dir / "dialogue_turn_log.jsonl", [external_turn, life_turn])

    external_turn_ref = f"{DIALOGUE_LOG_REF}#line-{turn_counter - 1}"
    life_turn_ref = f"{DIALOGUE_LOG_REF}#line-{turn_counter}"

    self_narrative_trace.setdefault("narrative_turn_refs", [])
    self_narrative_trace["narrative_turn_refs"].extend([external_turn_ref, life_turn_ref])
    self_narrative_trace["last_external_turn"] = {
        "turn_id": external_turn_id,
        "utterance": external_utterance,
    }
    self_narrative_trace["last_life_turn"] = {
        "turn_id": life_turn_id,
        "utterance": life_response,
    }
    write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)

    commitment_index.setdefault("recent_dialogue_turn_refs", [])
    commitment_index["recent_dialogue_turn_refs"].extend([external_turn_id, life_turn_id])
    commitment_index["last_external_turn_utterance"] = external_utterance
    commitment_index["last_life_turn_utterance"] = life_response
    write_json(language_dir / "commitment_repair_language_index.json", commitment_index)

    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        subjects[0]["relationship_stage"] = "active_dialogue"
        subjects[0]["last_external_turn_utterance"] = external_utterance
        subjects[0]["last_life_turn_utterance"] = life_response
    write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    generated_at = now_iso()
    updated_safe_terminal_loop = build_persistent_wait_bridge(
        run_id=run_id,
        generated_at=generated_at,
        status="closed",
        safe_terminal_loop=safe_terminal_loop,
        last_dialogue_packet_ref=RESUMED_DIALOGUE_PACKET_REF,
    )
    write_json(terminal_dir / "safe_terminal_loop_state.json", updated_safe_terminal_loop)

    updated_terminal_life_loop_state = {
        **terminal_life_loop_state,
        "current_mode": "restored_waiting_for_external_turn",
        "last_turn_status": "closed",
        "last_turn_mode": "resumed_external_dialogue_loop",
        "last_external_turn_utterance": external_utterance,
        "last_life_turn_utterance": life_response,
        "last_dialogue_packet_ref": RESUMED_DIALOGUE_PACKET_REF,
        "next_required_action": "await_next_external_relation_turn",
    }
    write_json(
        terminal_dir / "terminal_life_loop_state.json",
        updated_terminal_life_loop_state,
    )

    state_dir = terminal_dir.parent
    continuity_refresh = _refresh_long_horizon_continuity(
        state_dir=state_dir,
        language_dir=language_dir,
        relationship_dir=relationship_dir,
        relationship_graph=relationship_graph,
        commitment_index=commitment_index,
        generated_at=generated_at,
        source_doc_refs=source_doc_refs,
        write_json=write_json,
    )

    replay_cue_refs = ["runtime/state/life_state.json#memory_index.replay_cues"]
    if replay_cue_bundle_ref:
        replay_cue_refs.append(replay_cue_bundle_ref)
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    dialogue_writeback_bundle = build_dialogue_writeback_bundle(
        run_id=run_id,
        generated_at=generated_at,
        status="closed",
        dialogue_event_refs=[external_turn_ref, life_turn_ref],
        self_narrative_writeback_refs=[external_turn_ref, life_turn_ref],
        relationship_writeback_refs=[
            RELATIONSHIP_GRAPH_REF,
            RELATIONSHIP_MEMORY_REF,
            RELATIONSHIP_REPAIR_HISTORY_REF,
            RELATIONSHIP_MEMORY_OFFLINE_REF,
        ],
        relationship_timeline_writeback_refs=[RELATIONSHIP_TIMELINE_REF],
        commitment_writeback_refs=list(commitment_index.get("commitment_refs", []))
        + [
            COMMITMENT_TRUTH_OPEN_REF,
            COMMITMENT_TRUTH_REPAIR_REF,
        ],
        commitment_expression_writeback_refs=[COMMITMENT_EXPRESSION_PLAN_REF],
        apology_repair_writeback_refs=[APOLOGY_REPAIR_LANGUAGE_TRACE_REF],
        responsibility_writeback_refs=[
            RESPONSIBILITY_EVENT_REF,
            RESPONSIBILITY_OBLIGATION_REF,
            *membrane_guard_refs,
        ],
        life_state_writeback_refs=[
            LIFE_STATE_RESPONSIBILITY_REF,
            LIFE_STATE_REGRET_REF,
            LIFE_STATE_PAIN_REF,
            LIFE_STATE_RELATIONSHIP_MEMORY_REF,
            LIFE_STATE_RESPONSIBILITY_MEMORY_REF,
            LIFE_STATE_DREAM_MEMORY_REF,
            LIFE_STATE_LANGUAGE_OFFLINE_REF,
            LIFE_STATE_RELATIONSHIP_SUBJECTS_REF,
        ],
        replay_cue_refs=replay_cue_refs,
        terminal_state_refs=[SAFE_TERMINAL_LOOP_REF, TERMINAL_LIFE_LOOP_REF],
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
    )
    write_json(reports_dir / "dialogue_writeback_bundle.json", dialogue_writeback_bundle)

    resumed_dialogue_packet = {
        "schema_version": "resumed_external_dialogue_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "dialogue_mode": "resumed_relation_continuation",
        "external_turn_ref": external_turn_ref,
        "life_turn_ref": life_turn_ref,
        "external_utterance": external_utterance,
        "life_utterance": life_response,
        "life_context_frame_ref": "runtime/state/terminal/life_context_frame.json",
        "relation_turn_frame_ref": "runtime/state/terminal/relation_turn_frame.json",
        "expression_plan_ref": "runtime/state/language/expression_plan.json",
        "dialogue_writeback_bundle_ref": DIALOGUE_WRITEBACK_BUNDLE_REF,
        "next_required_action": "await_next_external_relation_turn",
    }
    if responsibility_loop_state_ref:
        resumed_dialogue_packet["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resumed_dialogue_packet["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resumed_dialogue_packet["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resumed_dialogue_packet["membrane_guard_refs"] = membrane_guard_refs
    if continuity_refresh is not None:
        resumed_dialogue_packet["relationship_timeline_ref"] = RELATIONSHIP_TIMELINE_REF
        resumed_dialogue_packet["commitment_expression_plan_ref"] = COMMITMENT_EXPRESSION_PLAN_REF
        resumed_dialogue_packet["apology_repair_language_trace_ref"] = (
            APOLOGY_REPAIR_LANGUAGE_TRACE_REF
        )
        resumed_dialogue_packet["life_state_ref"] = "runtime/state/life_state.json"
    write_json(reports_dir / "resumed_external_dialogue_packet.json", resumed_dialogue_packet)

    return ResidentTurnWritebackResult(
        safe_terminal_loop=updated_safe_terminal_loop,
        terminal_life_loop_state=updated_terminal_life_loop_state,
        dialogue_writeback_bundle=dialogue_writeback_bundle,
        resumed_dialogue_packet=resumed_dialogue_packet,
        external_turn_ref=external_turn_ref,
        life_turn_ref=life_turn_ref,
        last_external_turn=external_turn,
        last_life_turn=life_turn,
    )


def _refresh_long_horizon_continuity(
    *,
    state_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    relationship_graph: dict[str, Any],
    commitment_index: dict[str, Any],
    generated_at: str,
    source_doc_refs: list[str],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any] | None:
    relationship_timeline_path = relationship_dir / "relationship_timeline.json"
    commitment_expression_path = language_dir / "commitment_expression_plan.json"
    apology_repair_path = language_dir / "apology_repair_language_trace.json"
    expression_plan_path = language_dir / "expression_plan.json"
    commitment_truth_path = relationship_dir / "commitment_truth_state.json"
    responsibility_ledger_path = state_dir / "responsibility" / "responsibility_ledger.json"
    relationship_memory_path = state_dir / "memory" / "relationship_memory.json"
    life_state_path = state_dir / "life_state.json"
    responsibility_loop_path = state_dir / "action" / "responsibility_loop_state.json"

    required_paths = [
        relationship_timeline_path,
        commitment_expression_path,
        apology_repair_path,
        expression_plan_path,
        commitment_truth_path,
        responsibility_ledger_path,
        relationship_memory_path,
        life_state_path,
        responsibility_loop_path,
    ]
    if any(not path.exists() for path in required_paths):
        return None

    relationship_timeline = _read_json(relationship_timeline_path)
    commitment_expression_plan = _read_json(commitment_expression_path)
    apology_repair_language_trace = _read_json(apology_repair_path)
    expression_plan = _read_json(expression_plan_path)
    commitment_truth_state = _read_json(commitment_truth_path)
    responsibility_ledger = _read_json(responsibility_ledger_path)
    relationship_memory = _read_json(relationship_memory_path)
    life_state = _read_json(life_state_path)
    responsibility_loop_state = _read_json(responsibility_loop_path)

    nightmare_risk = _read_json_if_exists(state_dir / "dream" / "nightmare_loop_risk.json")
    belief_learning_plan = _read_json_if_exists(
        state_dir / "growth" / "belief_learning_plan.json"
    )
    language_learning_plan = _read_json_if_exists(
        state_dir / "growth" / "language_learning_plan.json"
    )
    relationship_learning_plan = _read_json_if_exists(
        state_dir / "growth" / "relationship_learning_plan.json"
    )

    dialogue_turn_refs = collect_dialogue_turn_refs(
        language_dir / "dialogue_turn_log.jsonl",
        [],
    )
    dialogue_turn_entries = [{"dialogue_turn_ref": ref} for ref in dialogue_turn_refs]

    refreshed_relationship_timeline = build_relationship_timeline(
        run_id=str(relationship_timeline.get("run_id") or commitment_expression_plan.get("run_id") or "resident-turn-writeback"),
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
    refreshed_commitment_expression_plan = build_commitment_expression_plan(
        run_id=str(commitment_expression_plan.get("run_id") or refreshed_relationship_timeline.get("run_id") or "resident-turn-writeback"),
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
        run_id=str(apology_repair_language_trace.get("run_id") or refreshed_commitment_expression_plan.get("run_id") or "resident-turn-writeback"),
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
        relationship_graph=relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        commitment_repair_index=commitment_index,
        last_contact_refs=[
            "runtime/state/language/dialogue_turn_log.jsonl",
            "runtime/state/language/inner_speech_frame.json",
            RESUMED_DIALOGUE_PACKET_REF,
        ],
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
    )
    refreshed_life_state = project_responsibility_language_continuity(
        life_state=life_state,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        relationship_memory=refreshed_relationship_memory,
        relationship_graph=relationship_graph,
        relationship_timeline=refreshed_relationship_timeline,
        commitment_expression_plan=refreshed_commitment_expression_plan,
        apology_repair_language_trace=refreshed_apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop_state,
        commitment_repair_index=commitment_index,
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
        additional_runtime_trace_refs=[
            ref
            for ref in [
                NIGHTMARE_RISK_REF if nightmare_risk else None,
                BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
                LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
                RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None,
            ]
            if ref
        ],
    )

    write_json(relationship_timeline_path, refreshed_relationship_timeline)
    write_json(commitment_expression_path, refreshed_commitment_expression_plan)
    write_json(apology_repair_path, refreshed_apology_repair_language_trace)
    write_json(relationship_memory_path, refreshed_relationship_memory)
    write_json(life_state_path, refreshed_life_state)
    return {
        "relationship_timeline": refreshed_relationship_timeline,
        "commitment_expression_plan": refreshed_commitment_expression_plan,
        "apology_repair_language_trace": refreshed_apology_repair_language_trace,
        "relationship_memory": refreshed_relationship_memory,
        "life_state": refreshed_life_state,
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)
