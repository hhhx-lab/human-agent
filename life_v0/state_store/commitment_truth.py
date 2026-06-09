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
