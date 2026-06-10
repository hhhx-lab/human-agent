from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from .background_lineage_state import build_resident_background_lineage_state
from .idle_strategy import IDLE_STRATEGY_STATE_REF, extract_idle_governance_fields
from .persistent_process import (
    RESIDENT_GOVERNANCE_REPORT_REF,
    RESIDENT_GOVERNANCE_SNAPSHOT_REF,
)


RESIDENT_GOVERNANCE_STATE_REF = "runtime/state/terminal/resident_governance_state.json"
RESUMED_DIALOGUE_PACKET_REF = "runtime/reports/latest/resumed_external_dialogue_packet.json"
DIALOGUE_WRITEBACK_BUNDLE_REF = "runtime/reports/latest/dialogue_writeback_bundle.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
COMMITMENT_EXPRESSION_PLAN_REF = "runtime/state/language/commitment_expression_plan.json"
APOLOGY_REPAIR_LANGUAGE_TRACE_REF = "runtime/state/language/apology_repair_language_trace.json"


def write_live_turn_waiting_governance_handoff(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any] | None,
    commitment_expression_plan: dict[str, Any] | None,
    apology_repair_language_trace: dict[str, Any] | None,
    external_turn_ref: str,
    life_turn_ref: str,
    responsibility_loop_state_ref: str | None,
    world_contact_summary_ref: str | None,
    pain_regret_repair_report_ref: str | None,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any]:
    idle_strategy_state = _read_json_if_exists(terminal_dir / "idle_strategy_state.json")
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    resident_governance_state = {
        "schema_version": "resident_governance_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "active",
        "governance_mode": "foreground_terminal_residency",
        "governance_phase": "live_turn_waiting_handoff",
        "waiting_mode": terminal_life_loop_state.get(
            "current_mode",
            safe_terminal_loop.get("current_mode", "restored_waiting_for_external_turn"),
        ),
        "heartbeat_counter": int(
            terminal_life_loop_state.get(
                "heartbeat_counter",
                safe_terminal_loop.get("heartbeat_counter", 0),
            )
        ),
        "idle_strategy_ref": IDLE_STRATEGY_STATE_REF,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "resident_governance_report_ref": RESIDENT_GOVERNANCE_REPORT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_heartbeat_packet_ref": safe_terminal_loop.get("last_heartbeat_packet_ref"),
        "last_dialogue_packet_ref": RESUMED_DIALOGUE_PACKET_REF,
        "dialogue_writeback_bundle_ref": DIALOGUE_WRITEBACK_BUNDLE_REF,
        "last_external_turn_ref": external_turn_ref,
        "last_life_turn_ref": life_turn_ref,
        "relationship_timeline_ref": _ref_if_present(
            payload=relationship_timeline,
            ref=RELATIONSHIP_TIMELINE_REF,
        ),
        "commitment_expression_plan_ref": _ref_if_present(
            payload=commitment_expression_plan,
            ref=COMMITMENT_EXPRESSION_PLAN_REF,
        ),
        "apology_repair_language_trace_ref": _ref_if_present(
            payload=apology_repair_language_trace,
            ref=APOLOGY_REPAIR_LANGUAGE_TRACE_REF,
        ),
        "long_horizon_language_refs": [
            ref
            for ref in [
                _ref_if_present(
                    payload=relationship_timeline,
                    ref=RELATIONSHIP_TIMELINE_REF,
                ),
                _ref_if_present(
                    payload=commitment_expression_plan,
                    ref=COMMITMENT_EXPRESSION_PLAN_REF,
                ),
                _ref_if_present(
                    payload=apology_repair_language_trace,
                    ref=APOLOGY_REPAIR_LANGUAGE_TRACE_REF,
                ),
            ]
            if ref
        ],
        "next_required_action": "refresh_waiting_heartbeat_before_next_external_turn",
        "handoff_origin": "live_turn_cycle_completed",
    }
    if responsibility_loop_state_ref:
        resident_governance_state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resident_governance_state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resident_governance_state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resident_governance_state["membrane_guard_refs"] = membrane_guard_refs
    resident_governance_state.update(extract_idle_governance_fields(idle_strategy_state))
    resident_background_lineage_state = build_resident_background_lineage_state(
        resident_governance_state,
        governance_phase="live_turn_waiting_handoff",
        status="active",
    )
    if resident_background_lineage_state:
        resident_governance_state["resident_background_lineage_state"] = (
            resident_background_lineage_state
        )
    write_json(terminal_dir / "resident_governance_state.json", resident_governance_state)
    return resident_governance_state


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def _ref_if_present(*, payload: dict[str, Any] | None, ref: str) -> str | None:
    if not payload:
        return None
    return ref
