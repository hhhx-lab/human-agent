from __future__ import annotations

import json
from typing import Any

from life_v0.growth.offline_learning_profile import (
    normalize_offline_learning_cumulative_profile,
)


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


def project_engram_index_from_live_turn(
    *,
    engram_index: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_engram_index(engram_index, generated_at, run_id)
    relationship_memory = relationship_memory or {}
    relationship_timeline = relationship_timeline or {}
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    state_merge_guard = state_merge_guard or {}
    autobiographical_stack = autobiographical_stack or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", []))
        + list(dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    updated["autobiographical_memory_refs"] = _dedupe(
        list(updated.get("autobiographical_memory_refs", []))
        + list(autobiographical_stack.get("anchor_refs", []))
        + list(autobiographical_stack.get("turn_refs", []))
        + list(autobiographical_stack.get("narrative_refs", []))
        + ["runtime/state/self/autobiographical_stack.json"]
    )
    updated["relationship_memory_refs"] = _dedupe(
        list(updated.get("relationship_memory_refs", []))
        + list(relationship_memory.get("shared_memory_refs", []))
        + list(relationship_memory.get("timeline_refs", []))
        + ["runtime/state/memory/relationship_memory.json"]
    )
    updated["relationship_timeline_refs"] = _dedupe(
        list(updated.get("relationship_timeline_refs", []))
        + ["runtime/state/relationship/relationship_timeline.json"]
        + [
            f"runtime/state/relationship/relationship_timeline.json#{item.get('relationship_continuity_report_id')}"
            for item in relationship_timeline.get("relationship_continuity_reports", [])
            if isinstance(item, dict) and item.get("relationship_continuity_report_id")
        ]
    )
    updated["responsibility_memory_refs"] = _dedupe(
        list(updated.get("responsibility_memory_refs", []))
        + list(commitment_truth_state.get("responsibility_event_refs", []))
        + list(responsibility_ledger.get("responsibility_event_refs", []))
        + list(relationship_memory.get("responsibility_event_refs", []))
    )

    offline_learning_refs = [
        ref
        for ref in [
            nightmare_risk_ref,
            belief_learning_plan_ref,
            language_learning_plan_ref,
            relationship_learning_plan_ref,
        ]
        if ref
    ]
    updated["offline_learning_refs"] = _dedupe(
        list(updated.get("offline_learning_refs", []))
        + list(relationship_memory.get("offline_learning_refs", []))
        + offline_learning_refs
    )
    if nightmare_risk_ref:
        updated["dream_memory_refs"] = _dedupe(
            list(updated.get("dream_memory_refs", [])) + [nightmare_risk_ref]
        )
    cumulative_profile = normalize_offline_learning_cumulative_profile(
        offline_learning_cumulative_profile
    )
    if cumulative_profile:
        cumulative_refs = list(cumulative_profile.get("ref_set", []))
        updated["offline_learning_refs"] = _dedupe(
            list(updated.get("offline_learning_refs", [])) + cumulative_refs
        )
        updated["offline_learning_cumulative_refs"] = cumulative_refs
        updated["offline_learning_cumulative_projection"] = {
            "schema_version": cumulative_profile["schema_version"],
            "generation": cumulative_profile["generation"],
            "pressure_level": cumulative_profile["pressure_level"],
            "attention_target": cumulative_profile["attention_target"],
            "priority_profile": dict(cumulative_profile.get("priority_profile", {})),
            "ref_set": cumulative_refs,
        }

    queue_e_repair_refs = list(relationship_memory.get("queue_e_repair_refs", []))
    if queue_e_repair_refs:
        updated["queue_e_repair_refs"] = _dedupe(
            list(updated.get("queue_e_repair_refs", [])) + queue_e_repair_refs
        )
        updated["queue_e_repair_pressure_level"] = relationship_memory.get(
            "queue_e_repair_pressure_level"
        )
        updated["queue_e_repair_attention_target"] = relationship_memory.get(
            "queue_e_repair_attention_target"
        )

    if state_merge_guard:
        state_merge_ref = "runtime/state/memory/state_merge_guard.json"
        updated["state_merge_guard_refs"] = _dedupe(
            list(updated.get("state_merge_guard_refs", [])) + [state_merge_ref]
        )
        updated["state_merge_change_source_refs"] = _dedupe(
            list(updated.get("state_merge_change_source_refs", []))
            + _flatten_change_sources(
                state_merge_guard.get("long_term_change_sources", {})
            )
        )
    updated["replay_cue_refs"] = _dedupe(
        list(updated.get("replay_cue_refs", []))
        + ["runtime/state/life_state.json#memory_index.replay_cues"]
    )
    updated["anti_forgetting_anchor_refs"] = _dedupe(
        list(updated.get("anti_forgetting_anchor_refs", []))
        + list(updated.get("autobiographical_memory_refs", []))
        + list(updated.get("live_dialogue_turn_refs", []))[-4:]
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    return updated


def _seed_missing_engram_index(
    engram_index: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if engram_index:
        return json.loads(json.dumps(engram_index))
    resolved_run_id = run_id or "resident-turn-writeback"
    return {
        "schema_version": "engram_index_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "engram_index_id": f"engram-index-{resolved_run_id}",
        "autobiographical_memory_refs": [
            "runtime/state/self/autobiographical_stack.json#anchor_refs"
        ],
        "relationship_memory_refs": [
            "runtime/state/memory/relationship_memory.json#shared_memory_refs"
        ],
        "dream_memory_refs": [],
        "responsibility_memory_refs": [
            "runtime/state/responsibility/responsibility_ledger.json#responsibility_events"
        ],
        "replay_cue_refs": [
            "runtime/state/replay/replay_cue_bundle.json",
            "runtime/state/life_state.json#memory_index.replay_cues",
        ],
        "anti_forgetting_anchor_refs": [
            "runtime/state/self/autobiographical_stack.json#anchor_refs"
        ],
        "quarantine_refs": [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _flatten_change_sources(change_sources: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for value in change_sources.values():
        if isinstance(value, list):
            refs.extend(str(item) for item in value if item)
        elif isinstance(value, str) and value:
            refs.append(value)
    return refs


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
