from __future__ import annotations

from typing import Any


MEMORY_ALLOCATION_GATE_REF = "runtime/state/memory/memory_allocation_gate.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/29_memory_validator_rules.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_memory_allocation_gate(
    *,
    run_id: str,
    generated_at: str,
    event_segmentation_frame: dict[str, Any],
    memory_encoding_gate: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    relationship_memory = relationship_memory or {}
    autobiographical_stack = autobiographical_stack or {}
    responsibility_ledger = responsibility_ledger or {}
    signal_media_runtime = signal_media_runtime or {}
    body_resource_budget = body_resource_budget or {}
    core_affect_vector = core_affect_vector or {}
    candidates: list[dict[str, Any]] = []
    high_priority_episode_kinds: list[str] = []

    for episode in event_segmentation_frame.get("episodes", []):
        if not isinstance(episode, dict):
            continue
        score = _episode_allocation_score(
            episode=episode,
            relationship_memory=relationship_memory,
            autobiographical_stack=autobiographical_stack,
            responsibility_ledger=responsibility_ledger,
            signal_media_runtime=signal_media_runtime,
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
        )
        allocation_channel = _allocation_channel(
            episode=episode,
            score=score,
        )
        allocation_boundary = _allocation_boundary(allocation_channel)
        candidate = {
            "candidate_trace_ref": (
                "runtime/state/memory/memory_trace_store.json"
                f"#candidate:{episode.get('event_boundary_ref')}"
            ),
            "event_boundary_ref": episode.get("event_boundary_ref"),
            "episode_kind": episode.get("episode_kind"),
            "candidate_trace_kind": episode.get("candidate_trace_kind"),
            "memory_route": episode.get("memory_route"),
            "allocation_channel": allocation_channel,
            "allocation_boundary": allocation_boundary,
            "allocation_score": score,
            "salience_tags": _dedupe(_string_list(episode.get("salience_tags"))),
            "source_refs": _dedupe(_string_list(episode.get("source_refs"))),
            "cue_refs": _dedupe(_string_list(episode.get("cue_refs"))),
            "allocation_reason": _allocation_reason(
                episode=episode,
                score=score,
                relationship_memory=relationship_memory,
                responsibility_ledger=responsibility_ledger,
                core_affect_vector=core_affect_vector,
            ),
            "trace_store_ref": "runtime/state/memory/memory_trace_store.json"
            if memory_trace_store
            else None,
            "encoding_gate_ref": "runtime/state/memory/memory_encoding_gate.json"
            if memory_encoding_gate
            else None,
            "write_gate_ref": "runtime/state/memory/memory_write_gate.json"
            if memory_write_gate
            else None,
        }
        if score >= 5:
            high_priority_episode_kinds.append(str(episode.get("episode_kind")))
        candidates.append(candidate)

    candidates.sort(
        key=lambda item: (
            -int(item.get("allocation_score", 0)),
            str(item.get("episode_kind", "")),
        )
    )
    high_priority_episode_kinds = _dedupe(high_priority_episode_kinds)
    return {
        "schema_version": "memory_allocation_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "gate_ref": MEMORY_ALLOCATION_GATE_REF,
        "allocation_policy": "salience_emotion_responsibility_relationship_body_weighted",
        "candidate_allocation_count": len(candidates),
        "candidate_allocations": candidates,
        "high_priority_candidate_count": len(high_priority_episode_kinds),
        "high_priority_episode_kinds": high_priority_episode_kinds,
        "allocation_channels": _allocation_channel_summary(candidates),
        "allocation_boundaries": [
            "dream_hypothesis_not_factual_trace",
            "low_value_goes_deep_sediment_or_short_term",
            "relationship_scope_stays_subject_specific",
            "responsibility_and_relationship_prefer_long_term_routes",
            "body_debt_can_defer_commitment",
        ],
        "trace_store_refs": [
            "runtime/state/memory/memory_trace_store.json"
        ]
        if memory_trace_store
        else [],
        "event_segmentation_frame_ref": "runtime/state/memory/event_segmentation_frame.json",
        "memory_encoding_gate_ref": "runtime/state/memory/memory_encoding_gate.json"
        if memory_encoding_gate
        else None,
        "memory_write_gate_ref": "runtime/state/memory/memory_write_gate.json"
        if memory_write_gate
        else None,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _episode_allocation_score(
    *,
    episode: dict[str, Any],
    relationship_memory: dict[str, Any],
    autobiographical_stack: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    signal_media_runtime: dict[str, Any],
    body_resource_budget: dict[str, Any],
    core_affect_vector: dict[str, Any],
) -> int:
    episode_kind = str(episode.get("episode_kind") or "")
    score = {
        "responsibility_repair_seed_episode": 7,
        "relationship_seed_episode": 7,
        "autobiographical_seed_episode": 5,
        "live_language_seed_episode": 4,
        "dream_residue_seed_episode": 2,
        "low_value_context_seed_episode": 1,
    }.get(episode_kind, 3)

    cue_refs = _string_list(episode.get("cue_refs"))
    source_refs = _string_list(episode.get("source_refs"))
    if "responsibility" in cue_refs or "repair" in cue_refs:
        score += 2
    if "relationship" in cue_refs or "shared_memory" in cue_refs:
        score += 2
    if "autobiographical" in cue_refs or "self_continuity" in cue_refs:
        score += 2
    if "dream" in cue_refs or "sandbox" in cue_refs:
        score -= 1
    if "runtime/state/responsibility/responsibility_ledger.json" in source_refs:
        score += 1
    if "runtime/state/memory/relationship_memory.json" in source_refs:
        score += 1
    if "runtime/state/self/autobiographical_stack.json" in source_refs:
        score += 1
    score += _scale_score(_nested_number(core_affect_vector, "responsibility_weight"), 4)
    score += _scale_score(_nested_number(core_affect_vector, "pain_pressure"), 5)
    score += _scale_score(_nested_number(core_affect_vector, "arousal"), 2)
    score -= _scale_score(_nested_number(core_affect_vector, "dream_residue_load"), 3)
    score -= _body_defer_score(body_resource_budget)
    score -= _signal_defer_score(signal_media_runtime)
    if relationship_memory.get("memory_tier_projection"):
        score += 1
    if autobiographical_stack.get("anchor_refs"):
        score += 1
    if responsibility_ledger.get("responsibility_event_refs"):
        score += 1
    return max(score, 0)


def _allocation_channel(*, episode: dict[str, Any], score: int) -> str:
    episode_kind = str(episode.get("episode_kind") or "")
    if episode_kind == "dream_residue_seed_episode":
        return "sandbox"
    if episode_kind == "low_value_context_seed_episode" or score <= 2:
        return "deep_sediment_or_short_term"
    if episode_kind in {"responsibility_repair_seed_episode", "relationship_seed_episode"}:
        return "high_priority_long_term"
    if episode_kind == "autobiographical_seed_episode":
        return "protected_long_term"
    return "episodic_short_term"


def _allocation_boundary(channel: str) -> str:
    if channel == "sandbox":
        return "dream_hypothesis_not_factual_trace"
    if channel == "deep_sediment_or_short_term":
        return "low_value_goes_deep_sediment_or_short_term"
    if channel == "high_priority_long_term":
        return "responsibility_and_relationship_prefer_long_term_routes"
    if channel == "protected_long_term":
        return "self_continuity_protected"
    return "salience_gated_allocation"


def _allocation_reason(
    *,
    episode: dict[str, Any],
    score: int,
    relationship_memory: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    core_affect_vector: dict[str, Any],
) -> list[str]:
    reasons = [f"score={score}"]
    episode_kind = str(episode.get("episode_kind") or "")
    if episode_kind in {"responsibility_repair_seed_episode", "relationship_seed_episode"}:
        reasons.append("relationship_or_responsibility_priority")
    if episode_kind == "dream_residue_seed_episode":
        reasons.append("dream_material_sandboxed")
    if relationship_memory.get("shared_memory_refs"):
        reasons.append("shared_memory_available")
    if responsibility_ledger.get("responsibility_event_refs"):
        reasons.append("responsibility_trace_available")
    if _nested_number(core_affect_vector, "pain_pressure") > 0:
        reasons.append("pain_pressure_weighted")
    if _nested_number(core_affect_vector, "responsibility_weight") > 0:
        reasons.append("responsibility_weighted")
    return reasons


def _allocation_channel_summary(candidates: list[dict[str, Any]]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for candidate in candidates:
        channel = str(candidate.get("allocation_channel") or "unknown")
        summary[channel] = summary.get(channel, 0) + 1
    return summary


def _nested_number(source: dict[str, Any], key: str) -> float:
    value = source.get(key)
    if isinstance(value, (int, float)):
        return float(value)
    body_signal_profile = source.get("body_signal_profile")
    if isinstance(body_signal_profile, dict):
        nested = body_signal_profile.get(key)
        if isinstance(nested, (int, float)):
            return float(nested)
    return 0.0


def _scale_score(value: float, multiplier: int) -> int:
    if value <= 0:
        return 0
    return int(round(value * multiplier))


def _body_defer_score(body_resource_budget: dict[str, Any]) -> int:
    fatigue_state = body_resource_budget.get("fatigue_state", {})
    level = str(fatigue_state.get("level") or "").lower()
    if not level:
        return 0
    if "high" in level or "depleted" in level:
        return 3
    if "low" in level or "managed" in level:
        return 1
    return 0


def _signal_defer_score(signal_media_runtime: dict[str, Any]) -> int:
    body_signal_profile = signal_media_runtime.get("body_signal_profile", {})
    if not isinstance(body_signal_profile, dict):
        return 0
    if body_signal_profile.get("offline_learning_pressure_level") in {"elevated", "high"}:
        return 1
    if body_signal_profile.get("dream_residue_load", 0) and body_signal_profile.get("dream_residue_load", 0) > 0.5:
        return 1
    return 0


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
