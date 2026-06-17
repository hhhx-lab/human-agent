from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPAIR_CLOSEOUT_STATE_REF = "runtime/state/language/repair_closeout_state.json"

_CLOSEOUT_STATES = (
    "active_repair",
    "awaiting_confirmation",
    "confirmed",
    "consolidated",
    "dormant",
)


def build_repair_closeout_state(
    *,
    run_id: str,
    generated_at: str,
    commitment_truth_state: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    previous_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    previous = previous_state or {}
    previous_phase = str(previous.get("closeout_phase") or "")
    if previous_phase in _CLOSEOUT_STATES and previous_phase != "dormant":
        phase = previous_phase
        reason = str(previous.get("closeout_reason") or "repair_closeout_chain_preserved")
    else:
        phase, reason = _derive_initial_closeout_phase(
            commitment_truth_state=commitment_truth_state,
            apology_repair_language_trace=apology_repair_language_trace,
            responsibility_loop_state=responsibility_loop_state,
        )

    return {
        "schema_version": "repair_closeout_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "closeout_phase": phase,
        "closeout_reason": reason,
        "repair_narrative_mode": repair_narrative_mode_from_phase(phase),
        "repair_priority_band": _repair_priority_band(phase),
        "confirmation_count": _int_or_zero(previous.get("confirmation_count")),
        "last_confirmation_at": previous.get("last_confirmation_at"),
        "closeout_state_ref": REPAIR_CLOSEOUT_STATE_REF,
        "source_doc_refs": [
            "runtime/state/relationship/commitment_truth_state.json",
            "runtime/state/language/apology_repair_language_trace.json",
            "runtime/state/action/responsibility_loop_state.json",
        ],
        "repair_closeout_boundary": (
            "structured_repair_closeout_not_spoken_reply"
        ),
    }


def repair_narrative_mode_from_phase(phase: str) -> str:
    if phase in {"active_repair", "awaiting_confirmation"}:
        return "repair_active"
    if phase in {"confirmed", "consolidated"}:
        return "repair_echo"
    return "continuity_primary"


def repair_closeout_allows_repair_focus(
    closeout_state: dict[str, Any] | None,
) -> bool:
    phase = str((closeout_state or {}).get("closeout_phase") or "active_repair")
    return phase in {"active_repair", "awaiting_confirmation"}


def advance_repair_closeout_on_confirmation(
    closeout_state: dict[str, Any] | None,
    *,
    run_id: str,
    generated_at: str,
    feedback_event_type: str | None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(closeout_state or {}))
    updated.setdefault("schema_version", "repair_closeout_state_v0")
    updated["run_id"] = run_id
    updated["generated_at"] = generated_at
    phase = str(updated.get("closeout_phase") or "active_repair")

    if feedback_event_type != "confirmation":
        updated["repair_narrative_mode"] = repair_narrative_mode_from_phase(phase)
        updated["repair_priority_band"] = _repair_priority_band(phase)
        return updated

    confirmation_count = _int_or_zero(updated.get("confirmation_count")) + 1
    updated["confirmation_count"] = confirmation_count
    updated["last_confirmation_at"] = generated_at

    if phase == "active_repair":
        phase = "awaiting_confirmation"
        reason = "memory_confirmation_received_after_repair_surface"
    elif phase == "awaiting_confirmation":
        phase = "confirmed"
        reason = "repair_confirmation_received"
    elif phase == "confirmed":
        phase = "consolidated"
        reason = "repair_confirmation_reinforced"
    elif phase == "consolidated":
        phase = "dormant"
        reason = "repair_closeout_consolidated_to_dormant"
    else:
        reason = str(updated.get("closeout_reason") or "repair_closeout_unchanged")

    if confirmation_count >= 2 and phase in {"confirmed", "consolidated"}:
        phase = "dormant"
        reason = "repair_closeout_fast_track_after_repeated_confirmation"

    updated["closeout_phase"] = phase
    updated["closeout_reason"] = reason
    updated["repair_narrative_mode"] = repair_narrative_mode_from_phase(phase)
    updated["repair_priority_band"] = _repair_priority_band(phase)
    return updated


def project_apology_repair_trace_for_closeout(
    apology_repair_language_trace: dict[str, Any] | None,
    *,
    closeout_state: dict[str, Any] | None,
    generated_at: str,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(apology_repair_language_trace or {}))
    if not updated:
        return {}
    phase = str((closeout_state or {}).get("closeout_phase") or "active_repair")
    if phase == "dormant":
        updated["repair_window_mode"] = "dormant"
        updated["queue_e_repair_pressure_level"] = "baseline"
        updated["queue_e_repair_window_mode"] = "continuity_primary"
        updated["status"] = "closed"
        updated["generated_at"] = generated_at
    elif phase in {"confirmed", "consolidated"}:
        updated["repair_window_mode"] = "echo_only"
        updated["queue_e_repair_pressure_level"] = "present"
        updated["queue_e_repair_window_mode"] = "repair_echo"
        updated["generated_at"] = generated_at
    return updated


def read_repair_closeout_state(language_dir: Path) -> dict[str, Any]:
    path = language_dir / "repair_closeout_state.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _derive_initial_closeout_phase(
    *,
    commitment_truth_state: dict[str, Any] | None,
    apology_repair_language_trace: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
) -> tuple[str, str]:
    repair_required = _string_list(
        (commitment_truth_state or {}).get("repair_required_refs")
    )
    repair_obligations = _string_list(
        (responsibility_loop_state or {}).get("repair_obligation_refs")
    )
    repair_moves = (apology_repair_language_trace or {}).get("repair_language_moves")
    pressure = str(
        (apology_repair_language_trace or {}).get("queue_e_repair_pressure_level")
        or ""
    ).lower()
    if repair_required or repair_obligations:
        return ("active_repair", "repair_obligation_refs_present")
    if isinstance(repair_moves, list) and repair_moves and pressure not in {
        "",
        "baseline",
        "quiet",
    }:
        return ("awaiting_confirmation", "apology_repair_trace_pressure_without_open_obligation")
    return ("dormant", "no_active_repair_obligation")


def _repair_priority_band(phase: str) -> str:
    if phase == "active_repair":
        return "repair_primary"
    if phase == "awaiting_confirmation":
        return "repair_guarded"
    if phase in {"confirmed", "consolidated"}:
        return "repair_echo"
    return "continuity_primary"


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0