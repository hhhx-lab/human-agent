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
        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
        "long_term_change_sources": {
            "prediction_error_resolution_refs": [
                "runtime/state/prediction/prediction_error_field.json#error_events"
            ],
            "offline_learning_writeback_refs": [
                "runtime/state/growth/belief_learning_plan.json",
                "runtime/state/growth/relationship_learning_plan.json",
            ],
            "repair_responsibility_refs": list(responsibility_ledger.get("responsibility_event_refs", []))
            or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
        },
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_relationship_memory(
    *,
    relationship_memory: dict[str, Any],
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    commitment_repair_index: dict[str, Any] | None = None,
    last_contact_refs: list[str] | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
) -> dict[str, Any]:
    relationship_graph = relationship_graph or {}
    relationship_timeline = relationship_timeline or {}
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    commitment_repair_index = commitment_repair_index or {}
    updated = {
        **relationship_memory,
        "subject_refs": list(relationship_memory.get("subject_refs", [])),
        "shared_memory_refs": list(relationship_memory.get("shared_memory_refs", [])),
        "repair_history_refs": list(relationship_memory.get("repair_history_refs", [])),
        "last_contact_refs": list(relationship_memory.get("last_contact_refs", [])),
        "responsibility_event_refs": list(relationship_memory.get("responsibility_event_refs", [])),
        "timeline_refs": list(relationship_memory.get("timeline_refs", [])),
        "offline_learning_refs": list(relationship_memory.get("offline_learning_refs", [])),
    }

    subject_refs = [
        f"runtime/state/relationship/relationship_subject_graph.json#{subject.get('relationship_id')}"
        for subject in relationship_graph.get("subjects", [])
        if isinstance(subject, dict) and subject.get("relationship_id")
    ]
    if subject_refs:
        updated["subject_refs"] = _dedupe(subject_refs)

    updated["shared_memory_refs"] = _dedupe(
        updated["shared_memory_refs"]
        + ["runtime/state/language/language_relationship_state.json#shared_language_refs"]
        + list(commitment_truth_state.get("open_commitment_refs", []))
    )
    updated["repair_history_refs"] = _dedupe(
        updated["repair_history_refs"]
        + list(commitment_truth_state.get("repair_required_refs", []))
        + list(commitment_repair_index.get("regret_trace_refs", []))
        + list(commitment_repair_index.get("repair_language_refs", []))
    )
    updated["last_contact_refs"] = _dedupe(
        (last_contact_refs or []) + updated["last_contact_refs"]
    )
    updated["responsibility_event_refs"] = _dedupe(
        updated["responsibility_event_refs"] + list(responsibility_ledger.get("responsibility_event_refs", []))
    )
    updated["timeline_refs"] = _dedupe(
        updated["timeline_refs"]
        + ["runtime/state/relationship/relationship_timeline.json"]
        + [
            f"runtime/state/relationship/relationship_timeline.json#{item.get('relationship_continuity_report_id')}"
            for item in relationship_timeline.get("relationship_continuity_reports", [])
            if isinstance(item, dict) and item.get("relationship_continuity_report_id")
        ]
    )
    updated["offline_learning_refs"] = _dedupe(
        updated["offline_learning_refs"]
        + [
            ref
            for ref in [
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
            ]
            if ref
        ]
    )
    return updated


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
