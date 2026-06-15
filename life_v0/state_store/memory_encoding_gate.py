from __future__ import annotations

from typing import Any


MEMORY_ENCODING_GATE_REF = "runtime/state/memory/memory_encoding_gate.json"

SOURCE_DOC_REFS = [
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/29_memory_validator_rules.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
]


def build_memory_encoding_gate(
    *,
    run_id: str,
    generated_at: str,
    event_segmentation_frame: dict[str, Any],
    memory_trace_store: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidates = []
    for episode in event_segmentation_frame.get("episodes", []):
        if not isinstance(episode, dict):
            continue
        candidate_kind = episode.get("candidate_trace_kind") or "episodic"
        is_dream = candidate_kind == "dream_residue"
        candidates.append(
            {
                "candidate_trace_ref": (
                    "runtime/state/memory/memory_trace_store.json"
                    f"#candidate:{episode.get('event_boundary_ref')}"
                ),
                "event_boundary_ref": episode.get("event_boundary_ref"),
                "episode_kind": episode.get("episode_kind"),
                "candidate_trace_kind": candidate_kind,
                "encoding_decision": "sandbox_candidate" if is_dream else "candidate_trace",
                "source_refs": _string_list(episode.get("source_refs")),
                "retrieval_cues": _string_list(episode.get("cue_refs")),
                "write_gate_route": "memory_write_gate_then_state_merge_guard",
                "fact_boundary": (
                    "dream_hypothesis_not_factual_trace"
                    if is_dream
                    else "source_refs_required_before_active_trace"
                ),
            }
        )
    return {
        "schema_version": "memory_encoding_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "gate_ref": MEMORY_ENCODING_GATE_REF,
        "encoding_policy": "candidate_trace_before_long_term_memory",
        "candidate_trace_count": len(candidates),
        "candidate_traces": candidates,
        "candidate_trace_store_refs": [
            "runtime/state/memory/memory_trace_store.json"
        ],
        "memory_write_gate_ref": "runtime/state/memory/memory_write_gate.json"
        if memory_write_gate
        else None,
        "encoding_boundaries": [
            "source_refs_required",
            "dream_hypothesis_not_factual_trace",
            "relationship_scope_required",
            "candidate_before_active_trace",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, tuple):
        return [str(item) for item in value if item]
    if isinstance(value, set):
        return [str(item) for item in sorted(value) if item]
    return [str(value)] if value else []
