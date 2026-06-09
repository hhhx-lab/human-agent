from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/29_memory_validator_rules.md",
]


def build_engram_index(
    *,
    run_id: str,
    generated_at: str,
    autobiographical_stack: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    relationship_memory = relationship_memory or {}
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    replay_cue_bundle = replay_cue_bundle or {}
    return {
        "schema_version": "engram_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "engram_index_id": f"engram-index-{run_id}",
        "autobiographical_memory_refs": list((autobiographical_stack or {}).get("anchor_refs", []))
        or ["runtime/state/self/autobiographical_stack.json#anchor_refs"],
        "relationship_memory_refs": list(relationship_memory.get("shared_memory_refs", []))
        or ["runtime/state/memory/relationship_memory.json#shared_memory_refs"],
        "dream_memory_refs": ["runtime/state/dream/dream_consolidation_frame.json#dream_record_refs"],
        "responsibility_memory_refs": list(commitment_truth_state.get("responsibility_event_refs", []))
        or list(responsibility_ledger.get("responsibility_event_refs", []))
        or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
        "replay_cue_refs": list(replay_cue_bundle.get("anti_forgetting_targets", []))
        or [
            "runtime/state/replay/replay_cue_bundle.json",
            "runtime/state/life_state.json#memory_index.replay_cues",
        ],
        "anti_forgetting_anchor_refs": list((autobiographical_stack or {}).get("anchor_refs", []))
        or ["runtime/state/self/autobiographical_stack.json#anchor_refs"],
        "quarantine_refs": [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
