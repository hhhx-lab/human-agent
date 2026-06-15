from __future__ import annotations

from typing import Any


def world_contact_validation_repair_hold_closed(payload: dict[str, Any]) -> bool:
    return (
        payload.get("schema_version") == "world_contact_validation_v0"
        and payload.get("repair_hold_required") is True
        and payload.get("confirmation_threshold_bias") == "raised"
        and payload.get("future_no_go_profile_ref")
        == "runtime/state/action/go_nogo_state.json#future_no_go_profile"
        and payload.get("body_pressure_profile_ref")
        == "runtime/state/action/go_nogo_state.json#body_pressure_profile"
        and bool(payload.get("blocked_future_routes"))
        and bool(payload.get("allowed_repair_routes"))
        and bool(payload.get("repair_governance_refs"))
    )


def live_queue_e_world_contact_handoff_closeout_audited(
    process_report: dict[str, Any],
    handoff_state: dict[str, Any],
    terminal_loop: dict[str, Any],
) -> bool:
    live_refresh_signal = bool(
        handoff_state.get("last_projected_from_live_turn_ref")
        or handoff_state.get("live_turn_focus")
        or handoff_state.get("live_responsibility_consciousness_context_refs")
        or terminal_loop.get("live_queue_e_world_contact_handoff_refreshed")
    )
    if not live_refresh_signal:
        return True
    report_profile = process_report.get(
        "live_queue_e_world_contact_handoff_report_profile"
    )
    if not isinstance(report_profile, dict):
        report_profile = {}
    return (
        report_profile.get("schema_version")
        == "live_queue_e_world_contact_handoff_report_profile_v0"
        and process_report.get("live_queue_e_world_contact_handoff_report_boundary")
        == "live_queue_e_world_contact_handoff_structured_report_not_spoken_language"
        and bool(process_report.get("live_queue_e_world_contact_handoff_refreshed"))
    )


def _criterion_probe_status(
    live0_audit: dict[str, Any],
    *,
    criterion_id: str,
    probe_id: str,
) -> str | None:
    criteria = live0_audit.get("criteria")
    if not isinstance(criteria, list):
        return None
    for criterion in criteria:
        if not isinstance(criterion, dict):
            continue
        if criterion.get("criterion_id") != criterion_id:
            continue
        probes = criterion.get("probes")
        if not isinstance(probes, list):
            return None
        for probe in probes:
            if not isinstance(probe, dict):
                continue
            if probe.get("probe_id") == probe_id:
                status = probe.get("status")
                return str(status) if status not in (None, "") else None
    return None


def _criterion_status(live0_audit: dict[str, Any], criterion_id: str) -> str | None:
    criteria = live0_audit.get("criteria")
    if not isinstance(criteria, list):
        return None
    for criterion in criteria:
        if not isinstance(criterion, dict):
            continue
        if criterion.get("criterion_id") == criterion_id:
            status = criterion.get("status")
            return str(status) if status not in (None, "") else None
    return None


def live0_gate_f_inspection_snapshot(
    *,
    world_contact_validation: dict[str, Any] | None = None,
    process_report: dict[str, Any] | None = None,
    handoff: dict[str, Any] | None = None,
    terminal_loop: dict[str, Any] | None = None,
    live0_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    world_contact_validation = world_contact_validation or {}
    process_report = process_report or {}
    handoff = handoff or {}
    terminal_loop = terminal_loop or {}
    live0_audit = live0_audit or {}

    repair_hold_validated = world_contact_validation_repair_hold_closed(
        world_contact_validation
    )
    handoff_closeout_audited = live_queue_e_world_contact_handoff_closeout_audited(
        process_report,
        handoff,
        terminal_loop,
    )
    criterion_status = _criterion_status(
        live0_audit,
        "f_equal_relationship_dialogue_growth",
    )
    repair_hold_probe_status = _criterion_probe_status(
        live0_audit,
        criterion_id="f_equal_relationship_dialogue_growth",
        probe_id="queue_e_world_contact_repair_hold_validated",
    )
    closeout_probe_status = _criterion_probe_status(
        live0_audit,
        criterion_id="f_equal_relationship_dialogue_growth",
        probe_id="live_queue_e_world_contact_handoff_closeout_audited",
    )
    if repair_hold_probe_status is None:
        repair_hold_probe_status = "passed" if repair_hold_validated else "blocked"
    if closeout_probe_status is None:
        closeout_probe_status = "passed" if handoff_closeout_audited else "blocked"

    gate_f_closed = (
        criterion_status == "closed"
        if criterion_status
        else repair_hold_validated and handoff_closeout_audited
    )

    return {
        "live0_gate_f_present": bool(
            world_contact_validation
            or process_report
            or handoff
            or live0_audit
        ),
        "live0_gate_f_criterion_id": "f_equal_relationship_dialogue_growth",
        "live0_gate_f_criterion_status": criterion_status,
        "queue_e_world_contact_repair_hold_validation_closed": repair_hold_validated,
        "queue_e_world_contact_repair_hold_validated_probe_status": (
            repair_hold_probe_status
        ),
        "live_queue_e_handoff_closeout_audit_closed": handoff_closeout_audited,
        "live_queue_e_world_contact_handoff_closeout_probe_status": (
            closeout_probe_status
        ),
        "live0_gate_f_closed": gate_f_closed,
        "live0_gate_f_inspection_boundary": (
            "structured_live0_gate_f_evidence_not_spoken_language"
        ),
    }