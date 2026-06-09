from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
]


def build_relationship_memory(
    *,
    run_id: str,
    generated_at: str,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    repair_refs = list(commitment_truth_state.get("repair_required_refs", [])) or [
        "runtime/state/relationship/commitment_truth_state.json#repair_required_refs"
    ]
    return {
        "schema_version": "relationship_memory_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "relationship_memory_id": f"relationship-memory-{run_id}",
        "subject_refs": ["runtime/state/relationship/relationship_subject_graph.json#rel-v0-0001"],
        "shared_memory_refs": [
            "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
            "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs",
        ],
        "repair_history_refs": repair_refs,
        "last_contact_refs": ["runtime/state/language/inner_speech_frame.json"],
        "timeline_seed_refs": [
            "docs/96_real_relationship_longitudinal_timeline.md",
            "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
        ],
        "responsibility_event_refs": list(responsibility_ledger.get("responsibility_event_refs", []))
        or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
