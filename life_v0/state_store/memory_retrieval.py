from __future__ import annotations

import hashlib
import re
from typing import Any


MEMORY_RETRIEVAL_FRAME_REF = "runtime/state/memory/memory_retrieval_frame.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/v0/shared_contracts/life_state_store_v0_schema.md",
    "docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_memory_retrieval_frame(
    *,
    run_id: str,
    generated_at: str,
    cue_sources: dict[str, Any] | None = None,
    external_utterance: str | None = None,
    semantic_map: dict[str, Any] | None = None,
    language_percept: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    dialogue_memory_summary: dict[str, Any] | None = None,
    life_state: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    source_doc_refs: list[str] | None = None,
) -> dict[str, Any]:
    cue_terms = _cue_terms(
        cue_sources=cue_sources,
        external_utterance=external_utterance,
        semantic_map=semantic_map,
        language_percept=language_percept,
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    tiered_recall = _tiered_recall(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
    )
    activated_refs = _activated_refs(
        cue_terms=cue_terms,
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        state_merge_guard=state_merge_guard,
    )
    relationship_hits = _relationship_hits(
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    autobiographical_hits = _autobiographical_hits(autobiographical_stack)
    autobiographical_repair_hits = _autobiographical_responsibility_repair_hits(
        autobiographical_stack
    )
    autobiographical_repair_profile = (
        _autobiographical_responsibility_repair_profile(
            autobiographical_stack,
            autobiographical_repair_hits,
        )
    )
    dream_residue_hits = _dream_residue_hits(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
    )
    exit_dream_next_wake_governance = _exit_dream_next_wake_governance(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        state_merge_guard=state_merge_guard,
    )
    responsibility_hits = _responsibility_hits(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        autobiographical_repair_hits=autobiographical_repair_hits,
    )
    blocked_refs = _blocked_or_quarantined_refs(engram_index, life_state)
    source_docs = _dedupe(_string_list(source_doc_refs) + SOURCE_DOC_REFS)
    return {
        "schema_version": "memory_retrieval_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "retrieval_mode": "cue_driven_reconstructive_recall",
        "retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "cue_sources": _cue_source_summary(
            cue_sources=cue_sources,
            external_utterance=external_utterance,
            semantic_map=semantic_map,
            language_percept=language_percept,
        ),
        "cue_terms": cue_terms,
        "cue_fingerprint": _fingerprint(cue_terms),
        "activated_engram_refs": activated_refs,
        "relationship_memory_hits": relationship_hits,
        "autobiographical_hits": autobiographical_hits,
        "autobiographical_responsibility_repair_hits": (
            autobiographical_repair_hits
        ),
        "autobiographical_responsibility_repair_profile": (
            autobiographical_repair_profile
        ),
        "dream_residue_hits": dream_residue_hits,
        "exit_dream_next_wake_governance": exit_dream_next_wake_governance,
        "responsibility_hits": responsibility_hits,
        "tiered_recall": tiered_recall,
        "reconstruction_inputs": _reconstruction_inputs(
            cue_terms=cue_terms,
            tiered_recall=tiered_recall,
            relationship_hits=relationship_hits,
            autobiographical_hits=autobiographical_hits,
            autobiographical_repair_hits=autobiographical_repair_hits,
            dream_residue_hits=dream_residue_hits,
            responsibility_hits=responsibility_hits,
        ),
        "blocked_or_quarantined_refs": blocked_refs,
        "writeback_candidates": _writeback_candidates(
            activated_refs=activated_refs,
            blocked_refs=blocked_refs,
            exit_dream_governance=exit_dream_next_wake_governance,
        ),
        "consumer_refs": [
            "runtime/state/language/model_expression_state.json#model_expression_context_summary",
            "runtime/reports/latest/dialogue_writeback_bundle.json#memory_retrieval_writeback_refs",
            "runtime/state/life_state.json#memory_index.memory_retrieval_refs",
            "runtime/state/consciousness/workspace_frame.json#memory_retrieval_refs",
        ],
        "source_doc_refs": source_docs,
    }


def project_memory_retrieval_from_live_turn(
    *,
    memory_retrieval_frame: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    external_utterance: str,
    semantic_map: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
    live_language_turn_refs: list[str] | None = None,
    dialogue_turn_refs: list[str] | None = None,
) -> dict[str, Any]:
    previous = memory_retrieval_frame or {}
    cue_sources = {
        "previous_retrieval_frame_ref": (
            MEMORY_RETRIEVAL_FRAME_REF if previous else None
        ),
        "live_language_turn_refs": list(live_language_turn_refs or []),
        "dialogue_turn_refs": list(dialogue_turn_refs or []),
        "semantic_map_ref": "runtime/state/language/semantic_map_frame.json"
        if semantic_map
        else None,
        "language_percept_ref": "runtime/state/language/language_percept_frame.json"
        if language_percept
        else None,
    }
    frame = build_memory_retrieval_frame(
        run_id=run_id,
        generated_at=generated_at,
        cue_sources=cue_sources,
        external_utterance=external_utterance,
        semantic_map=semantic_map,
        language_percept=language_percept,
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        state_merge_guard=state_merge_guard,
    )
    frame["previous_retrieval_fingerprint"] = previous.get("cue_fingerprint")
    frame["previous_activated_ref_count"] = len(
        _string_list(previous.get("activated_engram_refs"))
    )
    frame["live_language_turn_refs"] = list(live_language_turn_refs or [])
    frame["dialogue_turn_refs"] = list(dialogue_turn_refs or [])
    frame["last_external_utterance_sha256"] = _sha256(external_utterance)
    return frame


def memory_retrieval_context_summary(
    memory_retrieval_frame: dict[str, Any] | None,
) -> dict[str, Any]:
    frame = memory_retrieval_frame or {}
    if not frame:
        return {}
    tiered = frame.get("tiered_recall", {})
    reconstruction = frame.get("reconstruction_inputs", {})
    return {
        "memory_retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "retrieval_mode": frame.get("retrieval_mode"),
        "cue_terms": _string_list(frame.get("cue_terms"))[:12],
        "activated_engram_ref_count": len(
            _string_list(frame.get("activated_engram_refs"))
        ),
        "salient_core_ref_count": len(
            _string_list((tiered or {}).get("salient_core_refs"))
        ),
        "retrievable_context_ref_count": len(
            _string_list((tiered or {}).get("retrievable_context_refs"))
        ),
        "deep_sediment_ref_count": len(
            _string_list((tiered or {}).get("deep_sediment_refs"))
        ),
        "relationship_hit_count": len(
            _string_list(frame.get("relationship_memory_hits"))
        ),
        "autobiographical_hit_count": len(
            _string_list(frame.get("autobiographical_hits"))
        ),
        "autobiographical_responsibility_repair_hit_count": len(
            _string_list(frame.get("autobiographical_responsibility_repair_hits"))
        ),
        "autobiographical_repair_pressure_level": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("pressure_level"),
        "autobiographical_repair_attention_target": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("attention_target"),
        "autobiographical_repair_projection_boundary": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("projection_boundary"),
        "autobiographical_repair_retrieval_boundary": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("retrieval_boundary"),
        "autobiographical_repair_boundary": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("retrieval_boundary"),
        "dream_residue_hit_count": len(_string_list(frame.get("dream_residue_hits"))),
        "exit_dream_next_wake_cue_ref_count": len(
            _string_list(
                (frame.get("exit_dream_next_wake_governance") or {}).get(
                    "next_wake_memory_cue_refs"
                )
            )
        ),
        "exit_dream_write_gate_ref": (
            frame.get("exit_dream_next_wake_governance") or {}
        ).get("memory_write_gate_ref"),
        "exit_dream_state_merge_guard_ref": (
            frame.get("exit_dream_next_wake_governance") or {}
        ).get("state_merge_guard_ref"),
        "exit_dream_fact_boundary_ref": (
            frame.get("exit_dream_next_wake_governance") or {}
        ).get("dream_fact_boundary_ref"),
        "responsibility_hit_count": len(_string_list(frame.get("responsibility_hits"))),
        "blocked_or_quarantined_ref_count": len(
            _string_list(frame.get("blocked_or_quarantined_refs"))
        ),
        "reconstruction_focus": (reconstruction or {}).get("reconstruction_focus"),
        "source_doc_refs": _string_list(frame.get("source_doc_refs"))[:8],
    }


def _cue_terms(
    *,
    cue_sources: dict[str, Any] | None,
    external_utterance: str | None,
    semantic_map: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
) -> list[str]:
    terms: list[str] = []
    if isinstance(cue_sources, dict):
        for key, value in cue_sources.items():
            normalized_key = _normalize_cue(str(key))
            if normalized_key:
                terms.append(normalized_key)
            if isinstance(value, str):
                terms.extend(_extract_text_cues(value))
                normalized_value = _normalize_cue(value)
                if normalized_value:
                    terms.append(normalized_value)
            else:
                terms.extend(_string_list(value))
    terms.extend(_extract_text_cues(external_utterance or ""))
    terms.extend(_string_list((semantic_map or {}).get("ambiguity_queue")))
    terms.extend(_string_list((semantic_map or {}).get("relationship_topic_refs")))
    terms.extend(_string_list((semantic_map or {}).get("commitment_trace_refs")))
    terms.extend(_string_list((semantic_map or {}).get("repair_trace_refs")))
    terms.extend(_string_list((language_percept or {}).get("shared_term_hits")))
    terms.extend(_string_list((language_percept or {}).get("repair_trigger_candidates")))
    terms.extend(_string_list((language_percept or {}).get("commitment_trigger_candidates")))
    relation_profile = (relationship_memory or {}).get("relation_person_profile")
    dialogue_profile = (dialogue_memory_summary or {}).get("relation_person_profile")
    if isinstance(relation_profile, dict):
        terms.extend(_string_list(relation_profile.get("observed_names")))
        terms.extend(_string_list(relation_profile.get("preference_hypotheses")))
    if isinstance(dialogue_profile, dict):
        terms.extend(_string_list(dialogue_profile.get("observed_names")))
        terms.extend(_string_list(dialogue_profile.get("preference_hypotheses")))
    terms.extend(_string_list((relationship_memory or {}).get("relationship_theme_tags")))
    terms.extend(_string_list((dialogue_memory_summary or {}).get("relationship_theme_tags")))
    terms.extend(_string_list((relationship_memory or {}).get("next_wake_cues")))
    terms.extend(_string_list((dialogue_memory_summary or {}).get("next_wake_cues")))
    terms.extend(
        _string_list((relationship_memory or {}).get("next_wake_memory_cue_refs"))
    )
    terms.extend(
        _string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs"))
    )
    if isinstance(cue_sources, dict):
        terms.extend(_string_list(cue_sources.get("dialogue_turn_refs")))
        terms.extend(_string_list(cue_sources.get("live_language_turn_refs")))
    return _dedupe([_normalize_cue(term) for term in terms if _normalize_cue(term)])[:48]


def _cue_source_summary(
    *,
    cue_sources: dict[str, Any] | None,
    external_utterance: str | None,
    semantic_map: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "external_utterance_sha256": _sha256(external_utterance or ""),
        "semantic_focus": (semantic_map or {}).get("semantic_focus"),
        "language_percept_ref": (cue_sources or {}).get("language_percept_ref"),
        "semantic_map_ref": (cue_sources or {}).get("semantic_map_ref"),
        "dialogue_turn_refs": _string_list((cue_sources or {}).get("dialogue_turn_refs")),
        "live_language_turn_refs": _string_list((cue_sources or {}).get("live_language_turn_refs")),
        "shared_term_hit_count": len(
            _string_list((language_percept or {}).get("shared_term_hits"))
        ),
        "ambiguity_count": len(_string_list((semantic_map or {}).get("ambiguity_queue"))),
    }


def _tiered_recall(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
) -> dict[str, Any]:
    engram_tier = (engram_index or {}).get("memory_tier_index")
    if not isinstance(engram_tier, dict):
        engram_tier = {}
    relationship_tier = (relationship_memory or {}).get("memory_tier_projection")
    if not isinstance(relationship_tier, dict):
        relationship_tier = {}
    dialogue_tier = (dialogue_memory_summary or {}).get("memory_tiering")
    if not isinstance(dialogue_tier, dict):
        dialogue_tier = {}
    life_tier = ((life_state or {}).get("memory_index") or {}).get("memory_tier_refs")
    if not isinstance(life_tier, dict):
        life_tier = {}
    return {
        "schema_version": "memory_retrieval_tiered_recall_v0",
        "tier_policy": "salient_core_then_context_then_deep_sediment",
        "salient_core_refs": _dedupe(
            _string_list(engram_tier.get("salient_core_refs"))
            + _string_list(relationship_tier.get("salient_core_episode_refs"))
            + _string_list(dialogue_tier.get("salient_core_episode_refs"))
            + _string_list(life_tier.get("salient_core_refs"))
        ),
        "retrievable_context_refs": _dedupe(
            _string_list(engram_tier.get("retrievable_context_refs"))
            + _string_list(relationship_tier.get("retrievable_context_episode_refs"))
            + _string_list(dialogue_tier.get("retrievable_context_episode_refs"))
            + _string_list(life_tier.get("retrievable_context_refs"))
        ),
        "deep_sediment_refs": _dedupe(
            _string_list(engram_tier.get("deep_sediment_refs"))
            + _string_list(relationship_tier.get("deep_sediment_episode_refs"))
            + _string_list(dialogue_tier.get("deep_sediment_episode_refs"))
            + _string_list(life_tier.get("deep_sediment_refs"))
        ),
        "fact_boundary": "retrieval_priority_does_not_promote_dream_or_hypothesis_to_fact",
    }


def _activated_refs(
    *,
    cue_terms: list[str],
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> list[str]:
    refs = []
    refs.extend(_string_list((engram_index or {}).get("live_dialogue_turn_refs")))
    refs.extend(_string_list((engram_index or {}).get("live_language_turn_refs")))
    refs.extend(_string_list((engram_index or {}).get("relationship_memory_refs")))
    refs.extend(_string_list((engram_index or {}).get("autobiographical_memory_refs")))
    refs.extend(_string_list((relationship_memory or {}).get("shared_memory_refs")))
    refs.extend(_string_list((relationship_memory or {}).get("dialogue_summary_refs")))
    refs.extend(_string_list((relationship_memory or {}).get("next_wake_memory_cue_refs")))
    refs.extend(_string_list((autobiographical_stack or {}).get("turn_refs")))
    refs.extend(_string_list((autobiographical_stack or {}).get("narrative_refs")))
    refs.extend(_string_list((autobiographical_stack or {}).get("next_wake_memory_cue_refs")))
    refs.extend(
        _autobiographical_responsibility_repair_hits(autobiographical_stack)
    )
    refs.extend(_string_list((dialogue_memory_summary or {}).get("source_dialogue_refs")))
    refs.extend(_string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs")))
    refs.extend(_string_list(((life_state or {}).get("memory_index") or {}).get("relationship_memory_refs")))
    refs.extend(_string_list(((life_state or {}).get("memory_index") or {}).get("next_wake_memory_cue_refs")))
    refs.extend(_string_list((responsibility_loop_state or {}).get("repair_obligation_refs")))
    refs.extend(_flatten_change_sources((state_merge_guard or {}).get("long_term_change_sources")))
    if not cue_terms:
        refs.extend(
            [
                "runtime/state/memory/engram_index.json",
                "runtime/state/memory/relationship_memory.json",
            ]
        )
    return _dedupe(refs)[:64]


def _relationship_hits(
    *,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
) -> list[str]:
    return _dedupe(
        _string_list((relationship_memory or {}).get("shared_memory_refs"))
        + _string_list((relationship_memory or {}).get("timeline_refs"))
        + _string_list((relationship_memory or {}).get("dialogue_summary_refs"))
        + (
            ["runtime/state/memory/dialogue_memory_summary.json"]
            if dialogue_memory_summary
            else []
        )
    )[:24]


def _autobiographical_hits(autobiographical_stack: dict[str, Any] | None) -> list[str]:
    return _dedupe(
        _string_list((autobiographical_stack or {}).get("anchor_refs"))
        + _string_list((autobiographical_stack or {}).get("turn_refs"))
        + _string_list((autobiographical_stack or {}).get("narrative_refs"))
        + _string_list((autobiographical_stack or {}).get("relationship_turn_refs"))
    )[:24]


def _autobiographical_responsibility_repair_hits(
    autobiographical_stack: dict[str, Any] | None,
) -> list[str]:
    stack = autobiographical_stack or {}
    projection = stack.get("responsibility_repair_projection")
    if not isinstance(projection, dict):
        projection = {}
    return _dedupe(
        _string_list(stack.get("autobiographical_responsibility_refs"))
        + _string_list(stack.get("autobiographical_regret_refs"))
        + _string_list(stack.get("autobiographical_repair_refs"))
        + _string_list(stack.get("queue_e_repair_refs"))
        + _string_list(projection.get("responsibility_refs"))
        + _string_list(projection.get("regret_refs"))
        + _string_list(projection.get("repair_refs"))
        + _string_list(projection.get("queue_e_repair_refs"))
    )[:32]


def _autobiographical_responsibility_repair_profile(
    autobiographical_stack: dict[str, Any] | None,
    repair_hits: list[str],
) -> dict[str, Any]:
    if not repair_hits:
        return {}
    projection = (autobiographical_stack or {}).get(
        "responsibility_repair_projection"
    )
    if not isinstance(projection, dict):
        projection = {}
    return {
        "schema_version": "memory_retrieval_autobiographical_repair_profile_v0",
        "projection_ref": (
            "runtime/state/self/autobiographical_stack.json"
            "#responsibility_repair_projection"
        ),
        "hit_count": len(repair_hits),
        "responsibility_ref_count": len(
            _string_list(projection.get("responsibility_refs"))
        ),
        "regret_ref_count": len(_string_list(projection.get("regret_refs"))),
        "repair_ref_count": len(_string_list(projection.get("repair_refs"))),
        "queue_e_repair_ref_count": len(
            _string_list(projection.get("queue_e_repair_refs"))
        ),
        "pressure_level": projection.get("pressure_level"),
        "attention_target": projection.get("attention_target"),
        "queue_e_priority_band": projection.get("queue_e_priority_band"),
        "repair_followup_required": bool(
            projection.get("repair_followup_required")
        ),
        "projection_boundary": projection.get(
            "projection_boundary",
            "autobiographical_repair_evidence_not_spoken_language",
        ),
        "retrieval_boundary": (
            "autobiographical_repair_retrieval_not_spoken_language"
        ),
    }


def _dream_residue_hits(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
) -> list[str]:
    return _dedupe(
        _string_list((engram_index or {}).get("dream_memory_refs"))
        + _string_list((engram_index or {}).get("exit_dream_consolidation_refs"))
        + _string_list((relationship_memory or {}).get("exit_dream_consolidation_refs"))
        + _string_list((relationship_memory or {}).get("dream_integrated_memory_refs"))
        + _string_list((relationship_memory or {}).get("next_wake_memory_cue_refs"))
        + (
            ["runtime/state/memory/dialogue_memory_summary.json"]
            if dialogue_memory_summary
            else []
        )
        + _string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("dream_memory_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("next_wake_memory_cue_refs"))
    )[:24]


def _responsibility_hits(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
    autobiographical_repair_hits: list[str] | None = None,
) -> list[str]:
    return _dedupe(
        _string_list((engram_index or {}).get("responsibility_memory_refs"))
        + _string_list((relationship_memory or {}).get("responsibility_event_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("responsibility_memory_refs"))
        + _string_list((responsibility_loop_state or {}).get("repair_obligation_refs"))
        + list(autobiographical_repair_hits or [])
    )[:24]


def _blocked_or_quarantined_refs(
    engram_index: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
) -> list[str]:
    return _dedupe(
        _string_list((engram_index or {}).get("quarantine_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("quarantine_refs"))
    )


def _reconstruction_inputs(
    *,
    cue_terms: list[str],
    tiered_recall: dict[str, Any],
    relationship_hits: list[str],
    autobiographical_hits: list[str],
    autobiographical_repair_hits: list[str],
    dream_residue_hits: list[str],
    responsibility_hits: list[str],
) -> dict[str, Any]:
    counts = {
        "cue_count": len(cue_terms),
        "salient_core_count": len(_string_list(tiered_recall.get("salient_core_refs"))),
        "relationship_hit_count": len(relationship_hits),
        "autobiographical_hit_count": len(autobiographical_hits),
        "autobiographical_responsibility_repair_hit_count": len(
            autobiographical_repair_hits
        ),
        "dream_residue_hit_count": len(dream_residue_hits),
        "responsibility_hit_count": len(responsibility_hits),
    }
    if counts["autobiographical_responsibility_repair_hit_count"]:
        focus = "autobiographical_responsibility_repair_reconstruction"
    elif counts["responsibility_hit_count"]:
        focus = "responsibility_memory_reconstruction"
    elif counts["dream_residue_hit_count"]:
        focus = "dream_residue_relation_reconstruction"
    elif counts["relationship_hit_count"]:
        focus = "relationship_continuity_reconstruction"
    elif counts["autobiographical_hit_count"]:
        focus = "autobiographical_continuity_reconstruction"
    else:
        focus = "minimal_context_reconstruction"
    return {
        "schema_version": "memory_reconstruction_inputs_v0",
        "reconstruction_focus": focus,
        "reconstruction_counts": counts,
        "source_priority_order": [
            "current_language_cues",
            "salient_core_memory",
            "relationship_memory",
            "autobiographical_memory",
            "responsibility_memory",
            "dream_residue_with_fact_boundary",
            "deep_sediment_context",
        ],
    }


def _writeback_candidates(
    *,
    activated_refs: list[str],
    blocked_refs: list[str],
    exit_dream_governance: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    blocked = set(blocked_refs)
    candidates: list[dict[str, Any]] = []
    for ref in activated_refs[:16]:
        candidates.append(
            {
                "candidate_ref": ref,
                "writeback_route": "memory_write_gate_then_state_merge_guard",
                "candidate_status": "quarantined_source"
                if ref in blocked
                else "retrieval_reconstruction_candidate",
            }
        )
    governance = exit_dream_governance or {}
    for ref in _string_list(governance.get("next_wake_memory_cue_refs"))[:8]:
        candidates.append(
            {
                "candidate_ref": ref,
                "writeback_route": "exit_dream_memory_write_gate_then_state_merge_guard",
                "candidate_status": "next_wake_cue_reactivation_candidate",
                "memory_write_gate_ref": governance.get("memory_write_gate_ref"),
                "state_merge_guard_ref": governance.get("state_merge_guard_ref"),
                "dream_fact_boundary_ref": governance.get("dream_fact_boundary_ref"),
            }
        )
    return candidates


def _exit_dream_next_wake_governance(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> dict[str, Any]:
    memory_index = (life_state or {}).get("memory_index")
    if not isinstance(memory_index, dict):
        memory_index = {}
    change_sources = (state_merge_guard or {}).get("long_term_change_sources")
    if not isinstance(change_sources, dict):
        change_sources = {}
    projection = (state_merge_guard or {}).get("exit_dream_state_merge_projection")
    if not isinstance(projection, dict):
        projection = {}
    next_wake_refs = _dedupe(
        _string_list((relationship_memory or {}).get("next_wake_memory_cue_refs"))
        + _string_list((engram_index or {}).get("next_wake_memory_cue_refs"))
        + _string_list((autobiographical_stack or {}).get("next_wake_memory_cue_refs"))
        + _string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs"))
        + _string_list(memory_index.get("next_wake_memory_cue_refs"))
        + _string_list(change_sources.get("next_wake_memory_cue_refs"))
        + _string_list(projection.get("next_wake_memory_cue_refs"))
    )
    write_gate_ref = (
        (dialogue_memory_summary or {}).get("memory_write_gate_ref")
        or (relationship_memory or {}).get("memory_write_gate_ref")
        or projection.get("memory_write_gate_ref")
    )
    state_merge_ref = (
        (dialogue_memory_summary or {}).get("state_merge_guard_ref")
        or (relationship_memory or {}).get("state_merge_guard_ref")
    )
    if not state_merge_ref and state_merge_guard:
        state_merge_ref = "runtime/state/memory/state_merge_guard.json"
    dream_fact_boundary_ref = (
        (dialogue_memory_summary or {}).get("dream_fact_boundary_ref")
        or _first_string(change_sources.get("dream_fact_boundary_refs"))
    )
    governance_refs = _dedupe(
        _string_list((relationship_memory or {}).get("exit_dream_governance_refs"))
        + _string_list((engram_index or {}).get("memory_write_gate_refs"))
        + _string_list((engram_index or {}).get("state_merge_guard_refs"))
        + _string_list((autobiographical_stack or {}).get("memory_write_gate_refs"))
        + _string_list((autobiographical_stack or {}).get("state_merge_guard_refs"))
        + _string_list(change_sources.get("exit_dream_write_gate_refs"))
        + ([str(write_gate_ref)] if write_gate_ref else [])
        + ([str(state_merge_ref)] if state_merge_ref else [])
        + ([str(dream_fact_boundary_ref)] if dream_fact_boundary_ref else [])
    )
    if not next_wake_refs and not governance_refs:
        return {}
    return {
        "schema_version": "exit_dream_next_wake_governance_v0",
        "memory_write_gate_ref": write_gate_ref,
        "state_merge_guard_ref": state_merge_ref,
        "dream_fact_boundary_ref": dream_fact_boundary_ref,
        "writeback_route": "memory_write_gate_then_state_merge_guard",
        "next_wake_memory_cue_refs": next_wake_refs[:24],
        "governance_refs": governance_refs[:24],
        "candidate_boundary": "reactivate_as_cue_material_not_fixed_language",
    }


def _extract_text_cues(text: str) -> list[str]:
    if not text:
        return []
    chinese_terms = re.findall(r"[\u4e00-\u9fff]{2,8}", text)
    latin_terms = re.findall(r"[A-Za-z][A-Za-z0-9_\-]{2,32}", text)
    special: list[str] = []
    for marker in [
        "记忆",
        "记住",
        "关系",
        "朋友",
        "家人",
        "梦",
        "梦境",
        "责任",
        "后悔",
        "痛苦",
        "语言",
        "真实",
        "生命",
        "不要机械",
        "模板",
    ]:
        if marker in text:
            special.append(marker)
    return special + chinese_terms[:16] + latin_terms[:12]


def _flatten_change_sources(change_sources: Any) -> list[str]:
    if not isinstance(change_sources, dict):
        return []
    refs: list[str] = []
    for value in change_sources.values():
        refs.extend(_string_list(value))
    return refs


def _normalize_cue(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip())[:96]


def _fingerprint(values: list[str]) -> str:
    return _sha256("\n".join(values))


def _sha256(value: str) -> str:
    return hashlib.sha256(str(value or "").encode("utf-8")).hexdigest()


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    if isinstance(value, str) and value:
        return [value]
    return []


def _first_string(value: Any) -> str | None:
    values = _string_list(value)
    return values[0] if values else None


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
