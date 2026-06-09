from __future__ import annotations

from typing import Any


def build_commitment_truth_state(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "commitment_truth_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "default_commitment_mode": "truth_tracking_required",
        "source_doc_refs": [
            "docs/94_pain_regret_and_repair_signal_schema.md",
            "docs/96_real_relationship_longitudinal_timeline.md",
            "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
        ],
        "open_commitments": [],
        "open_commitment_refs": [
            "runtime/state/language/commitment_repair_language_index.json#commitment-v0-0001"
        ],
        "repair_required_refs": [],
        "responsibility_event_refs": [
            "runtime/state/responsibility/responsibility_ledger.json#responsibility-event-v0-0001"
        ],
    }


def build_responsibility_ledger(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "responsibility_ledger_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "default_repair_mode": "repair_obligation_tracking",
        "source_doc_refs": [
            "docs/81_coexistence_event_review_and_responsibility_loop.md",
            "docs/82_incident_report_and_recovery_protocol.md",
            "docs/94_pain_regret_and_repair_signal_schema.md",
        ],
        "responsibility_events": [],
        "responsibility_event_refs": [
            "runtime/state/responsibility/responsibility_ledger.json#responsibility-event-v0-0001"
        ],
        "repair_obligations": [],
    }


def project_commitment_truth_state(
    *,
    commitment_truth_state: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    commitment_repair_index: dict[str, Any] | None = None,
) -> dict[str, Any]:
    responsibility_loop_state = responsibility_loop_state or {}
    commitment_repair_index = commitment_repair_index or {}
    updated = {
        **commitment_truth_state,
        "open_commitments": list(commitment_truth_state.get("open_commitments", [])),
        "open_commitment_refs": list(commitment_truth_state.get("open_commitment_refs", [])),
        "repair_required_refs": list(commitment_truth_state.get("repair_required_refs", [])),
        "responsibility_event_refs": list(commitment_truth_state.get("responsibility_event_refs", [])),
    }

    updated["open_commitment_refs"] = _dedupe(
        updated["open_commitment_refs"] + list(commitment_repair_index.get("commitment_refs", []))
    )
    updated["repair_required_refs"] = _dedupe(
        updated["repair_required_refs"]
        + list(responsibility_loop_state.get("repair_obligation_refs", []))
        + list(commitment_repair_index.get("repair_obligation_refs", []))
    )
    updated["responsibility_event_refs"] = _dedupe(
        updated["responsibility_event_refs"]
        + [
            item.get("responsibility_event_id")
            for item in responsibility_loop_state.get("responsibility_attribution_events", [])
            if isinstance(item, dict) and item.get("responsibility_event_id")
        ]
    )
    updated["regret_trace_refs"] = _dedupe(
        list(commitment_truth_state.get("regret_trace_refs", []))
        + list(commitment_repair_index.get("regret_trace_refs", []))
    )
    updated["repair_language_trace_refs"] = _dedupe(
        list(commitment_truth_state.get("repair_language_trace_refs", []))
        + list(commitment_repair_index.get("repair_language_refs", []))
    )
    return updated


def project_responsibility_ledger(
    *,
    responsibility_ledger: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    responsibility_loop_state = responsibility_loop_state or {}
    updated = {
        **responsibility_ledger,
        "responsibility_events": list(responsibility_ledger.get("responsibility_events", [])),
        "responsibility_event_refs": list(responsibility_ledger.get("responsibility_event_refs", [])),
        "repair_obligations": list(responsibility_ledger.get("repair_obligations", [])),
    }

    attribution_events = [
        item
        for item in responsibility_loop_state.get("responsibility_attribution_events", [])
        if isinstance(item, dict)
    ]
    updated["responsibility_events"] = attribution_events or updated["responsibility_events"]
    updated["responsibility_event_refs"] = _dedupe(
        updated["responsibility_event_refs"]
        + [
            item.get("responsibility_event_id")
            for item in attribution_events
            if item.get("responsibility_event_id")
        ]
    )
    updated["repair_obligations"] = _dedupe(
        updated["repair_obligations"] + list(responsibility_loop_state.get("repair_obligation_refs", []))
    )
    updated["counterfactual_repair_refs"] = _dedupe(
        list(responsibility_ledger.get("counterfactual_repair_refs", []))
        + [
            item.get("counterfactual_id")
            for item in responsibility_loop_state.get("counterfactual_repair_frames", [])
            if isinstance(item, dict) and item.get("counterfactual_id")
        ]
    )
    return updated


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
