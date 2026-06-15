from __future__ import annotations

import hashlib
from typing import Any


EVENT_SEGMENTATION_FRAME_REF = "runtime/state/memory/event_segmentation_frame.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_event_segmentation_frame(
    *,
    run_id: str,
    generated_at: str,
    engram_index: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    episodes = [
        _episode(
            run_id=run_id,
            episode_kind="live_language_seed_episode",
            candidate_trace_kind="episodic",
            memory_route="fast_episodic_buffer",
            source_refs=_dedupe(
                _string_list((engram_index or {}).get("live_dialogue_turn_refs"))
                + _string_list((engram_index or {}).get("live_language_turn_refs"))
                + ["runtime/state/memory/engram_index.json"]
            ),
            cue_refs=_string_list((memory_retrieval_frame or {}).get("cue_terms")),
            salience_tags=["current_language", "event_boundary_seed"],
        ),
        _episode(
            run_id=run_id,
            episode_kind="relationship_seed_episode",
            candidate_trace_kind="relationship",
            memory_route="relationship_memory",
            source_refs=_dedupe(
                _string_list((relationship_memory or {}).get("shared_memory_refs"))
                + _string_list((relationship_memory or {}).get("timeline_refs"))
                + ["runtime/state/memory/relationship_memory.json"]
            ),
            cue_refs=_dedupe(
                _string_list((relationship_memory or {}).get("relationship_theme_tags"))
                + ["relationship", "shared_memory", "relation_scope"]
            ),
            salience_tags=["relationship_weight", "shared_language"],
        ),
        _episode(
            run_id=run_id,
            episode_kind="autobiographical_seed_episode",
            candidate_trace_kind="autobiographical",
            memory_route="autobiographical_stack",
            source_refs=_dedupe(
                _string_list((autobiographical_stack or {}).get("anchor_refs"))
                + _string_list((autobiographical_stack or {}).get("turn_refs"))
                + ["runtime/state/self/autobiographical_stack.json"]
            ),
            cue_refs=["autobiographical", "self_continuity", "old_self_anchor"],
            salience_tags=["identity_weight", "continuity"],
        ),
        _episode(
            run_id=run_id,
            episode_kind="responsibility_repair_seed_episode",
            candidate_trace_kind="responsibility",
            memory_route="responsibility_memory",
            source_refs=_dedupe(
                _string_list(
                    (responsibility_ledger or {}).get("responsibility_event_refs")
                )
                + _string_list(
                    (responsibility_ledger or {}).get("repair_obligations")
                )
                + _string_list(
                    (engram_index or {}).get("responsibility_memory_refs")
                )
                + ["runtime/state/responsibility/responsibility_ledger.json"]
            ),
            cue_refs=["responsibility", "regret", "repair", "commitment"],
            salience_tags=["responsibility_pressure", "repair_drive"],
        ),
        _episode(
            run_id=run_id,
            episode_kind="dream_residue_seed_episode",
            candidate_trace_kind="dream_residue",
            memory_route="dream_residue_sandbox",
            source_refs=_dedupe(
                _string_list((engram_index or {}).get("dream_memory_refs"))
                + _string_list(
                    (memory_retrieval_frame or {}).get("dream_residue_hits")
                )
                + ["runtime/state/dream/exit_dream_consolidation_summary.json"]
            ),
            cue_refs=["dream", "next_wake", "sandbox"],
            salience_tags=["dream_boundary", "not_factual_trace"],
        ),
        _episode(
            run_id=run_id,
            episode_kind="low_value_context_seed_episode",
            candidate_trace_kind="context",
            memory_route="deep_sediment",
            source_refs=_dedupe(
                _string_list((memory_trace_store or {}).get("index_refs"))
                + _string_list(
                    (state_merge_guard or {}).get("state_merge_change_source_refs")
                )
                + ["runtime/state/memory/memory_trace_store.json"]
            ),
            cue_refs=["deep_sediment", "low_value_context"],
            salience_tags=["low_value", "background_context"],
        ),
    ]
    episodes = [episode for episode in episodes if episode["source_refs"]]
    return {
        "schema_version": "event_segmentation_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "frame_ref": EVENT_SEGMENTATION_FRAME_REF,
        "segmentation_policy": "episode_boundary_from_life_state_not_token_chunks",
        "episode_count": len(episodes),
        "episode_kind_order": [episode["episode_kind"] for episode in episodes],
        "episodes": episodes,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _episode(
    *,
    run_id: str,
    episode_kind: str,
    candidate_trace_kind: str,
    memory_route: str,
    source_refs: list[str],
    cue_refs: list[str],
    salience_tags: list[str],
) -> dict[str, Any]:
    seed = "|".join([run_id, episode_kind] + source_refs[:4])
    return {
        "event_boundary_ref": f"event-boundary-{_short_hash(seed)}",
        "episode_kind": episode_kind,
        "candidate_trace_kind": candidate_trace_kind,
        "memory_route": memory_route,
        "source_refs": _dedupe(source_refs),
        "cue_refs": _dedupe(cue_refs),
        "salience_tags": _dedupe(salience_tags),
        "segmentation_boundary": "episode_boundary_not_token_chunk",
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


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
