from __future__ import annotations

from typing import Any


def build_inner_speech_frame(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    source_doc_refs: list[str],
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "inner_speech_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "attention_focus": "relationship_subject_and_responsibility_trace",
        "affective_modulation": "guarded_but_expressive",
        "responsibility_constraint": "no_untraced_commitment",
        "old_self_anchor_refs": list(life_state.get("self_model", {}).get("old_self_anchors", [])),
        "percept_ref": "runtime/state/language/language_percept_frame.json" if language_percept else None,
        "semantic_map_ref": "runtime/state/language/semantic_map_frame.json" if semantic_map else None,
        "semantic_focus": (semantic_map or {}).get("semantic_focus"),
        "bus_channel_refs": ["inner_language_bus", "conscious_broadcast_bus"],
        "source_doc_refs": source_doc_refs,
    }
