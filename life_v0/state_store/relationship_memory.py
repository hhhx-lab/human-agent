from __future__ import annotations

from typing import Any

from life_v0.growth.offline_learning_profile import (
    normalize_offline_learning_cumulative_profile,
)
from life_v0.membrane.queue_e_signals import (
    build_queue_e_repair_modulation_profile,
)


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
    shared_memory_refs = _dedupe(
        [
            "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
            "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs",
        ]
        + list(commitment_truth_state.get("open_commitment_refs", []))
    )
    initial_profile = {
        "schema_version": "relationship_person_profile_v0",
        "observed_names": [],
        "preference_hypotheses": [],
        "personality_hypotheses": [],
        "relationship_stage_hint": "pre_activation",
        "profile_source_refs": [
            "runtime/state/relationship/commitment_truth_state.json",
            "runtime/state/responsibility/responsibility_ledger.json",
        ],
    }
    relationship_depth = _build_relationship_depth_profile(
        shared_memory_refs=shared_memory_refs,
        repair_refs=repair_refs,
        responsibility_refs=list(responsibility_ledger.get("responsibility_event_refs", []))
        or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
    )
    return {
        "schema_version": "relationship_memory_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "relationship_memory_id": f"relationship-memory-{run_id}",
        "subject_refs": ["runtime/state/relationship/relationship_subject_graph.json#rel-v0-0001"],
        "shared_memory_refs": shared_memory_refs,
        "repair_history_refs": repair_refs,
        "last_contact_refs": ["runtime/state/language/inner_speech_frame.json"],
        "dialogue_summary_refs": [],
        "exit_dream_consolidation_refs": [],
        "memory_tier_projection": {
            "schema_version": "relationship_memory_tier_projection_v0",
            "salient_core_episode_refs": [],
            "retrievable_context_episode_refs": [],
            "deep_sediment_episode_refs": [],
            "projection_source_ref": "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering",
        },
        "salient_core_memory_refs": [],
        "retrievable_context_memory_refs": [],
        "deep_sediment_memory_refs": [],
        "relation_person_profile": initial_profile,
        "relationship_memory_depth_profile": relationship_depth["relationship_memory_depth_profile"],
        "shared_narrative_memory": relationship_depth["shared_narrative_memory"],
        "we_memory_traces": relationship_depth["we_memory_traces"],
        "relationship_damage_and_repair_chain": relationship_depth["relationship_damage_and_repair_chain"],
        "commitment_fulfillment_threads": relationship_depth["commitment_fulfillment_threads"],
        "relationship_theme_tags": [],
        "next_wake_cues": [],
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
            "relationship_memory_offline_refs": [],
            "relationship_memory_repair_refs": repair_refs,
            "relationship_memory_deepening_refs": [
                "runtime/state/memory/relationship_memory.json#we_memory_traces",
                "runtime/state/memory/relationship_memory.json#shared_narrative_memory",
                "runtime/state/memory/relationship_memory.json#relationship_damage_and_repair_chain",
            ],
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
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
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
        "we_memory_traces": list(relationship_memory.get("we_memory_traces", [])),
        "relationship_damage_and_repair_chain": list(
            relationship_memory.get("relationship_damage_and_repair_chain", [])
        ),
        "commitment_fulfillment_threads": list(
            relationship_memory.get("commitment_fulfillment_threads", [])
        ),
    }

    subject_refs = [
        f"runtime/state/relationship/relationship_subject_graph.json#{subject.get('relationship_id')}"
        for subject in relationship_graph.get("subjects", [])
        if isinstance(subject, dict) and subject.get("relationship_id")
    ]
    if subject_refs:
        updated["subject_refs"] = _dedupe(subject_refs)

    relation_subject_scopes: list[dict[str, Any]] = []
    scoped_preference_traces: list[dict[str, Any]] = []
    for subject in relationship_graph.get("subjects", []):
        if not isinstance(subject, dict):
            continue
        subject_id = str(
            subject.get("relationship_id")
            or subject.get("subject_id")
            or subject.get("relation_id")
            or ""
        )
        if not subject_id:
            continue
        relationship_scope = f"relation_subject:{subject_id}"
        relation_subject_scopes.append(
            {
                "relation_subject_id": subject_id,
                "relationship_scope": relationship_scope,
                "relation_role": subject.get("relation_role"),
                "subject_ref": (
                    f"runtime/state/relationship/relationship_subject_graph.json#{subject_id}"
                ),
            }
        )
        for preference in _string_list(subject.get("preference_hypotheses")):
            scoped_preference_traces.append(
                {
                    "relation_subject_id": subject_id,
                    "relationship_scope": relationship_scope,
                    "preference_hypothesis": preference,
                    "trace_kind": "relation_scoped_preference_hypothesis",
                }
            )
    if relation_subject_scopes:
        updated["relation_subject_scopes"] = relation_subject_scopes
        updated.setdefault("relationship_scope", relation_subject_scopes[0]["relationship_scope"])
        updated.setdefault(
            "active_relation_subject_id",
            relation_subject_scopes[0]["relation_subject_id"],
        )
    if scoped_preference_traces:
        updated["scoped_preference_traces"] = _dedupe_dict_list(
            list(updated.get("scoped_preference_traces", [])) + scoped_preference_traces
        )

    updated["shared_memory_refs"] = _dedupe(
        updated["shared_memory_refs"]
        + ["runtime/state/language/language_relationship_state.json#shared_language_refs"]
        + list(commitment_truth_state.get("open_commitment_refs", []))
    )
    relation_person_profile = dict(updated.get("relation_person_profile", {}))
    relation_person_profile["schema_version"] = relation_person_profile.get(
        "schema_version", "relationship_person_profile_v0"
    )
    relation_person_profile["observed_names"] = _dedupe(
        _valid_observed_names(
            list(relation_person_profile.get("observed_names", []))
            + list((commitment_truth_state.get("observed_names", [])))
        )
    )
    relation_person_profile["preference_hypotheses"] = _dedupe(
        list(relation_person_profile.get("preference_hypotheses", []))
        + list((commitment_truth_state.get("preference_hypotheses", [])))
    )
    relation_person_profile["personality_hypotheses"] = _dedupe(
        list(relation_person_profile.get("personality_hypotheses", []))
        + list((commitment_truth_state.get("personality_hypotheses", [])))
    )
    if relationship_timeline.get("relationship_continuity_reports"):
        first_report = relationship_timeline.get("relationship_continuity_reports", [])
        first_report = first_report[0] if first_report and isinstance(first_report[0], dict) else {}
        if first_report.get("relationship_stage_hint"):
            relation_person_profile["relationship_stage_hint"] = first_report["relationship_stage_hint"]
    updated["relation_person_profile"] = relation_person_profile
    updated["repair_history_refs"] = _dedupe(
        updated["repair_history_refs"]
        + list(commitment_truth_state.get("repair_required_refs", []))
        + list(commitment_repair_index.get("regret_trace_refs", []))
        + list(commitment_repair_index.get("repair_language_refs", []))
    )
    updated["shared_narrative_memory"] = _merge_shared_narrative_memory(
        updated.get("shared_narrative_memory"),
        shared_memory_refs=updated["shared_memory_refs"],
        timeline_refs=updated.get("timeline_refs", []),
        repair_refs=updated["repair_history_refs"],
    )
    updated["we_memory_traces"] = _merge_we_memory_traces(
        updated.get("we_memory_traces", []),
        shared_memory_refs=updated["shared_memory_refs"],
        timeline_refs=updated.get("timeline_refs", []),
        repair_refs=updated["repair_history_refs"],
    )
    updated["relationship_damage_and_repair_chain"] = (
        _merge_relationship_damage_and_repair_chain(
            updated.get("relationship_damage_and_repair_chain", []),
            repair_refs=updated["repair_history_refs"],
            responsibility_refs=updated["responsibility_event_refs"],
        )
    )
    updated["commitment_fulfillment_threads"] = _merge_commitment_threads(
        updated.get("commitment_fulfillment_threads", []),
        commitment_truth_state=commitment_truth_state,
        responsibility_refs=updated["responsibility_event_refs"],
    )
    updated["relationship_memory_depth_profile"] = _relationship_depth_profile_from_updated(updated)
    updated.setdefault("long_term_change_sources", {})
    updated["long_term_change_sources"]["relationship_memory_deepening_refs"] = _dedupe(
        list(updated["long_term_change_sources"].get("relationship_memory_deepening_refs", []))
        + [
            "runtime/state/memory/relationship_memory.json#we_memory_traces",
            "runtime/state/memory/relationship_memory.json#shared_narrative_memory",
            "runtime/state/memory/relationship_memory.json#relationship_damage_and_repair_chain",
        ]
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
    cumulative_profile = normalize_offline_learning_cumulative_profile(
        offline_learning_cumulative_profile
    )
    if cumulative_profile:
        cumulative_refs = list(cumulative_profile.get("ref_set", []))
        updated["offline_learning_refs"] = _dedupe(
            updated["offline_learning_refs"] + cumulative_refs
        )
        updated["offline_learning_cumulative_projection"] = {
            "schema_version": cumulative_profile["schema_version"],
            "generation": cumulative_profile["generation"],
            "pressure_level": cumulative_profile["pressure_level"],
            "attention_target": cumulative_profile["attention_target"],
            "priority_profile": dict(cumulative_profile.get("priority_profile", {})),
            "ref_set": cumulative_refs,
        }
        updated["offline_learning_cumulative_refs"] = cumulative_refs
        updated.setdefault("long_term_change_sources", {})
        updated["long_term_change_sources"]["offline_learning_cumulative_refs"] = (
            cumulative_refs
        )
        updated["long_term_change_sources"]["relationship_memory_offline_refs"] = _dedupe(
            list(updated["long_term_change_sources"].get("relationship_memory_offline_refs", []))
            + cumulative_refs
        )
    repair_profile = build_queue_e_repair_modulation_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    if repair_profile["pressure_level"] != "quiet" or repair_profile["ref_set"]:
        repair_refs = list(repair_profile.get("ref_set", []))
        updated["repair_history_refs"] = _dedupe(
            updated["repair_history_refs"] + repair_refs
        )
        updated["queue_e_repair_modulation_profile"] = repair_profile
        updated["queue_e_repair_pressure_level"] = repair_profile["pressure_level"]
        updated["queue_e_repair_attention_target"] = repair_profile["attention_target"]
        updated["queue_e_repair_refs"] = repair_refs
        updated.setdefault("long_term_change_sources", {})
        updated["long_term_change_sources"]["queue_e_repair_modulation_refs"] = (
            repair_refs
        )
        updated["long_term_change_sources"]["relationship_memory_repair_refs"] = _dedupe(
            list(updated["long_term_change_sources"].get("relationship_memory_repair_refs", []))
            + repair_refs
        )
    return updated


def _build_relationship_depth_profile(
    *,
    shared_memory_refs: list[str],
    repair_refs: list[str],
    responsibility_refs: list[str],
) -> dict[str, Any]:
    shared_narrative_memory = _merge_shared_narrative_memory(
        None,
        shared_memory_refs=shared_memory_refs,
        timeline_refs=[],
        repair_refs=repair_refs,
    )
    we_memory_traces = _merge_we_memory_traces(
        [],
        shared_memory_refs=shared_memory_refs,
        timeline_refs=[],
        repair_refs=repair_refs,
    )
    repair_chain = _merge_relationship_damage_and_repair_chain(
        [],
        repair_refs=repair_refs,
        responsibility_refs=responsibility_refs,
    )
    commitment_threads = _merge_commitment_threads(
        [],
        commitment_truth_state={},
        responsibility_refs=responsibility_refs,
    )
    seed = {
        "shared_narrative_memory": shared_narrative_memory,
        "we_memory_traces": we_memory_traces,
        "relationship_damage_and_repair_chain": repair_chain,
        "commitment_fulfillment_threads": commitment_threads,
    }
    return {
        **seed,
        "relationship_memory_depth_profile": _relationship_depth_profile_from_updated(seed),
    }


def _merge_shared_narrative_memory(
    current: Any,
    *,
    shared_memory_refs: list[str],
    timeline_refs: list[str],
    repair_refs: list[str],
) -> dict[str, Any]:
    current = current if isinstance(current, dict) else {}
    return {
        "schema_version": "shared_narrative_memory_v0",
        "narrative_ref": "runtime/state/memory/relationship_memory.json#shared_narrative_memory",
        "source_refs": _dedupe(
            list(current.get("source_refs", []))
            + shared_memory_refs
            + timeline_refs
            + repair_refs
        ),
        "shared_term_refs": _dedupe(
            list(current.get("shared_term_refs", []))
            + [
                ref
                for ref in shared_memory_refs
                if "language_relationship_state" in ref or "shared_language" in ref
            ]
        ),
        "commitment_refs": _dedupe(
            list(current.get("commitment_refs", []))
            + [ref for ref in shared_memory_refs if "commitment" in ref]
        ),
        "repair_refs": _dedupe(list(current.get("repair_refs", [])) + repair_refs),
        "narrative_boundary": "shared_narrative_is_relation_scoped_not_global_personality",
    }


def _merge_we_memory_traces(
    current: list[Any],
    *,
    shared_memory_refs: list[str],
    timeline_refs: list[str],
    repair_refs: list[str],
) -> list[dict[str, Any]]:
    traces = [item for item in current if isinstance(item, dict)]
    seed = {
        "we_memory_id": "we-memory-v0-0001",
        "we_memory_ref": "runtime/state/memory/relationship_memory.json#we_memory_traces.0",
        "event_refs": _dedupe(shared_memory_refs + timeline_refs + repair_refs),
        "participants": ["digital_life", "relation_subject"],
        "ownership": "shared_seed",
        "correction_refs": [],
        "dream_residue_refs": [
            "runtime/state/dream/wake_integration_frame.json#relationship_dream_residue"
        ],
        "boundary": "we_memory_requires_relation_scope_and_correction_history",
    }
    if not traces:
        return [seed]
    first = dict(traces[0])
    first["event_refs"] = _dedupe(list(first.get("event_refs", [])) + seed["event_refs"])
    first.setdefault("participants", seed["participants"])
    first.setdefault("ownership", seed["ownership"])
    first.setdefault("dream_residue_refs", seed["dream_residue_refs"])
    first.setdefault("boundary", seed["boundary"])
    return [first] + traces[1:]


def _merge_relationship_damage_and_repair_chain(
    current: list[Any],
    *,
    repair_refs: list[str],
    responsibility_refs: list[str],
) -> list[dict[str, Any]]:
    chain = [item for item in current if isinstance(item, dict)]
    seed = {
        "chain_id": "relationship-repair-chain-v0-0001",
        "chain_ref": "runtime/state/memory/relationship_memory.json#relationship_damage_and_repair_chain.0",
        "injury_refs": [],
        "repair_refs": _dedupe(repair_refs),
        "responsibility_refs": _dedupe(responsibility_refs),
        "repair_route": "commitment_truth_then_responsibility_ledger_then_state_merge_guard",
        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
    }
    if not chain:
        return [seed]
    first = dict(chain[0])
    first["repair_refs"] = _dedupe(list(first.get("repair_refs", [])) + seed["repair_refs"])
    first["responsibility_refs"] = _dedupe(
        list(first.get("responsibility_refs", [])) + seed["responsibility_refs"]
    )
    first.setdefault("repair_route", seed["repair_route"])
    first.setdefault("state_merge_guard_ref", seed["state_merge_guard_ref"])
    return [first] + chain[1:]


def _merge_commitment_threads(
    current: list[Any],
    *,
    commitment_truth_state: dict[str, Any],
    responsibility_refs: list[str],
) -> list[dict[str, Any]]:
    threads = [item for item in current if isinstance(item, dict)]
    open_refs = list(commitment_truth_state.get("open_commitment_refs", [])) or [
        "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs"
    ]
    seed = {
        "thread_id": "commitment-thread-v0-0001",
        "thread_ref": "runtime/state/memory/relationship_memory.json#commitment_fulfillment_threads.0",
        "open_commitment_refs": _dedupe(open_refs),
        "responsibility_refs": _dedupe(responsibility_refs),
        "fulfillment_status": "open_seed",
        "future_probe_ref": "runtime/state/relationship/commitment_truth_state.json#future_probe",
    }
    if not threads:
        return [seed]
    first = dict(threads[0])
    first["open_commitment_refs"] = _dedupe(
        list(first.get("open_commitment_refs", [])) + seed["open_commitment_refs"]
    )
    first["responsibility_refs"] = _dedupe(
        list(first.get("responsibility_refs", [])) + seed["responsibility_refs"]
    )
    first.setdefault("fulfillment_status", seed["fulfillment_status"])
    first.setdefault("future_probe_ref", seed["future_probe_ref"])
    return [first] + threads[1:]


def _relationship_depth_profile_from_updated(updated: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "relationship_memory_depth_profile_v0",
        "profile_ref": "runtime/state/memory/relationship_memory.json#relationship_memory_depth_profile",
        "shared_narrative_ref": "runtime/state/memory/relationship_memory.json#shared_narrative_memory",
        "we_memory_trace_refs": [
            trace.get("we_memory_ref")
            for trace in updated.get("we_memory_traces", [])
            if isinstance(trace, dict) and trace.get("we_memory_ref")
        ],
        "damage_repair_chain_refs": [
            chain.get("chain_ref")
            for chain in updated.get("relationship_damage_and_repair_chain", [])
            if isinstance(chain, dict) and chain.get("chain_ref")
        ],
        "commitment_thread_refs": [
            thread.get("thread_ref")
            for thread in updated.get("commitment_fulfillment_threads", [])
            if isinstance(thread, dict) and thread.get("thread_ref")
        ],
        "separation_keys": [
            "relation_subject_id",
            "shared_language",
            "boundary_history",
            "repair_history",
            "commitment_fulfillment",
        ],
        "consumer_refs": [
            "runtime/state/memory/pattern_separation_index.json#relationship_subject_scope",
            "runtime/state/memory/pattern_completion_frame.json#relationship_episode_completion",
            "runtime/state/memory/memory_retrieval_frame.json#relationship_memory_hits",
            "runtime/state/life_state.json#memory_index.relationship_deep_memory_refs",
        ],
    }


def _valid_observed_names(values: list[Any]) -> list[str]:
    from .relation_identity_hygiene import sanitize_observed_names

    return sanitize_observed_names(values)


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


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _dedupe_dict_list(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        key = "|".join(
            [
                str(item.get("relation_subject_id") or ""),
                str(item.get("relationship_scope") or ""),
                str(item.get("preference_hypothesis") or ""),
            ]
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
