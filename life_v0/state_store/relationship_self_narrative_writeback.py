from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/real—live0/06_relationship_and_commitment.md",
    "docs/real—live0/04_personality_self_identity.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
]


def apply_relationship_self_narrative_writeback(
    *,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    memory_trace_store: dict[str, Any] | None,
    replay_trace_ids: list[str] | None = None,
    generated_at: str,
) -> dict[str, Any]:
    relationship = dict(relationship_memory or {})
    autobiographical = dict(autobiographical_stack or {})
    trace_ids = list(replay_trace_ids or [])
    live_traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
        and trace.get("lifecycle_state") != "deprecated"
    ]
    if not trace_ids:
        trace_ids = [
            str(trace.get("trace_id"))
            for trace in live_traces[-6:]
            if trace.get("trace_id")
        ]
    narrative_entries: list[dict[str, Any]] = []
    self_entries: list[dict[str, Any]] = []
    for trace_id in trace_ids:
        trace = next(
            (item for item in live_traces if str(item.get("trace_id")) == trace_id),
            None,
        )
        if not trace:
            continue
        semantic_focus = str(trace.get("semantic_focus") or "live_episode")
        digest = str(trace.get("content_summary") or "")[:180]
        subject_id = trace.get("relation_subject_id")
        narrative_id = f"shared-narrative-{trace_id}"
        narrative_entries.append(
            {
                "narrative_id": narrative_id,
                "trace_id": trace_id,
                "relation_subject_id": subject_id,
                "semantic_focus": semantic_focus,
                "narrative_digest": digest,
                "rewrite_kind": "offline_relationship_episode_integration",
                "generated_at": generated_at,
            }
        )
        trace["relationship_narrative_rewrite_ref"] = (
            f"runtime/state/memory/relationship_memory.json#shared_narrative_memory#{narrative_id}"
        )
        self_entries.append(
            {
                "self_narrative_entry_id": f"self-narrative-{trace_id}",
                "trace_id": trace_id,
                "continuity_thread": semantic_focus,
                "self_digest": digest,
                "rewrite_kind": "autobiographical_episode_thread_update",
                "generated_at": generated_at,
            }
        )
    if narrative_entries:
        shared = list(relationship.get("shared_narrative_memory") or [])
        if not isinstance(shared, list):
            shared = []
        shared.extend(narrative_entries)
        relationship["shared_narrative_memory"] = shared[-24:]
        relationship["relationship_narrative_last_rewrite_at"] = generated_at
    if self_entries:
        threads = list(autobiographical.get("general_event_threads") or [])
        if not isinstance(threads, list):
            threads = []
        for entry in self_entries:
            threads.append(
                {
                    "thread_id": entry["self_narrative_entry_id"],
                    "focus": entry["continuity_thread"],
                    "episode_digest": entry["self_digest"],
                    "trace_ref": f"runtime/state/memory/memory_trace_store.json#{entry['trace_id']}",
                }
            )
        autobiographical["general_event_threads"] = threads[-24:]
        autobiographical["self_narrative_last_rewrite_at"] = generated_at
        autobiographical["self_narrative_continuity_score"] = min(
            1.0,
            float(autobiographical.get("self_narrative_continuity_score") or 0.35)
            + len(self_entries) * 0.04,
        )
    return {
        "relationship_memory": relationship,
        "autobiographical_stack": autobiographical,
        "memory_trace_store": memory_trace_store,
        "relationship_narrative_rewrite_count": len(narrative_entries),
        "self_narrative_rewrite_count": len(self_entries),
        "narrative_rewrite_diff": narrative_entries + self_entries,
    }