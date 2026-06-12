from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from .background_lineage_state import build_resident_background_lineage_state
from .handoff_profile import active_handoff_profile_fields
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
LINEAGE_PRESENCE_KEYS = [
    "relationship_presence",
    "trait_convergence_presence",
    "heartbeat_cadence_presence",
    "language_presence",
    "state_merge_presence",
    "prediction_write_gate_presence",
    "identity_consciousness_birth_presence",
    "offline_learning_presence",
    "dream_wake_presence",
    "autonomous_activity_presence",
    "resident_process_identity_presence",
    "body_presence",
    "birth_repair_presence",
    "life_constraint_presence",
]


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
    resident_governance_state.update(
        _merge_live_language_governance(
            extract_idle_governance_fields(idle_strategy_state),
            terminal_life_loop_state,
        )
    )
    resident_background_lineage_state = _merge_handoff_lineage_state(
        existing_lineage_state=_dict_or_empty(
            terminal_life_loop_state.get("resident_background_lineage_state")
        ),
        rebuilt_lineage_state=build_resident_background_lineage_state(
            resident_governance_state,
            governance_phase="live_turn_waiting_handoff",
            status="active",
        ),
    )
    if resident_background_lineage_state:
        resident_governance_state["resident_background_lineage_state"] = (
            resident_background_lineage_state
        )
    handoff_profile = _build_live_turn_waiting_handoff_profile(
        resident_governance_state=resident_governance_state,
        resident_background_lineage_state=resident_background_lineage_state,
    )
    resident_governance_state["live_turn_waiting_handoff_profile"] = handoff_profile
    terminal_life_loop_state.update(active_handoff_profile_fields(handoff_profile))
    write_json(terminal_dir / "terminal_life_loop_state.json", terminal_life_loop_state)
    write_json(terminal_dir / "resident_governance_state.json", resident_governance_state)
    return resident_governance_state


def _build_live_turn_waiting_handoff_profile(
    *,
    resident_governance_state: dict[str, Any],
    resident_background_lineage_state: dict[str, Any],
) -> dict[str, Any]:
    live_language_refs = _string_list(
        resident_governance_state.get("live_language_turn_refs")
    )
    long_horizon_language_refs = _string_list(
        resident_governance_state.get("long_horizon_language_refs")
    )
    carried_presence_keys = [
        key for key in LINEAGE_PRESENCE_KEYS if resident_background_lineage_state.get(key)
    ]
    handoff_evidence_refs = _dedupe_string_list(
        _string_list(resident_background_lineage_state.get("evidence_refs"))
        + long_horizon_language_refs
        + [
            ref
            for ref in [
                resident_governance_state.get("idle_strategy_ref"),
                resident_governance_state.get("terminal_life_loop_state_ref"),
                resident_governance_state.get(
                    "background_resident_governance_explanation_ref"
                ),
                resident_governance_state.get("dialogue_writeback_bundle_ref"),
                resident_governance_state.get("last_dialogue_packet_ref"),
                resident_governance_state.get("last_external_turn_ref"),
                resident_governance_state.get("last_life_turn_ref"),
            ]
            if ref
        ]
    )
    return {
        "schema_version": "live_turn_waiting_handoff_profile_v0",
        "handoff_origin": resident_governance_state.get("handoff_origin"),
        "governance_phase": resident_governance_state.get("governance_phase"),
        "waiting_mode": resident_governance_state.get("waiting_mode"),
        "next_required_action": resident_governance_state.get("next_required_action"),
        "background_governance_driver_family": resident_governance_state.get(
            "background_governance_driver_family"
        ),
        "background_next_wake_expectation": resident_governance_state.get(
            "background_next_wake_expectation"
        ),
        "lineage_depth_band": resident_background_lineage_state.get("depth_band"),
        "lineage_parent_run_id": resident_background_lineage_state.get("parent_run_id"),
        "live_language_ref_count": len(live_language_refs),
        "last_live_semantic_focus": resident_governance_state.get(
            "last_live_semantic_focus"
        ),
        "long_horizon_language_ref_count": len(long_horizon_language_refs),
        "carried_presence_keys": carried_presence_keys,
        "handoff_evidence_refs": handoff_evidence_refs,
        "handoff_evidence_ref_count": len(handoff_evidence_refs),
    }


def _merge_handoff_lineage_state(
    *,
    existing_lineage_state: dict[str, Any],
    rebuilt_lineage_state: dict[str, Any],
) -> dict[str, Any]:
    if not existing_lineage_state:
        return rebuilt_lineage_state
    if not rebuilt_lineage_state:
        merged = dict(existing_lineage_state)
    else:
        merged = dict(rebuilt_lineage_state)
        for key, value in existing_lineage_state.items():
            if key.endswith("_presence") and value:
                merged[key] = value
            elif key == "evidence_refs":
                merged[key] = _dedupe_string_list(
                    _string_list(value) + _string_list(rebuilt_lineage_state.get(key))
                )
            elif key not in merged or _is_empty_scalar(merged[key]):
                merged[key] = value
            elif isinstance(merged[key], (list, dict)) and not merged[key]:
                merged[key] = value
    merged["schema_version"] = "resident_background_lineage_state_v0"
    merged["governance_phase"] = "live_turn_waiting_handoff"
    merged["status"] = "active"
    return merged


def _is_empty_scalar(value: Any) -> bool:
    return value is None or value == "" or value is False


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


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


def _merge_live_language_governance(
    idle_governance: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
) -> dict[str, Any]:
    current_refs = _dedupe_string_list(
        _string_list(terminal_life_loop_state.get("live_language_turn_refs"))
        or _string_list(idle_governance.get("live_language_turn_refs"))
    )
    current_focus = (
        terminal_life_loop_state.get("last_live_semantic_focus")
        or idle_governance.get("last_live_semantic_focus")
    )
    background_refs = _dedupe_string_list(
        _string_list(idle_governance.get("background_live_language_turn_refs"))
    )
    background_focus = idle_governance.get("background_last_live_semantic_focus")
    all_refs = _dedupe_string_list(current_refs + background_refs)
    if current_refs:
        idle_governance["live_language_turn_refs"] = current_refs
    if current_focus:
        idle_governance["last_live_semantic_focus"] = current_focus
    if all_refs or current_focus or background_focus:
        idle_governance["live_language_presence_profile"] = {
            "schema_version": "live_language_presence_profile_v0",
            "continuity_mode": (
                "current_turn_plus_background_language_presence"
                if current_refs and background_refs
                else "current_turn_language_presence"
                if current_refs
                else "background_language_presence"
            ),
            "live_language_turn_refs": current_refs,
            "last_live_semantic_focus": current_focus,
            "background_live_language_turn_refs": background_refs,
            "background_last_live_semantic_focus": background_focus,
            "ref_count": len(all_refs),
            "ref_set": all_refs,
        }
    return idle_governance


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe_string_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
