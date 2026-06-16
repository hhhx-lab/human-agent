from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "temp/14_memory_module_rebuild_audit.md",
]

MEMORY_CAPABILITY_SCORECARD_REF = (
    "runtime/reports/latest/memory_capability_scorecard.json"
)


def build_memory_capability_scorecard(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    life_schema_map: dict[str, Any] | None = None,
    memory_longitudinal_profile: dict[str, Any] | None = None,
    memory_consolidation_report: dict[str, Any] | None = None,
    fast_episodic_buffer: dict[str, Any] | None = None,
    engram_cluster: dict[str, Any] | None = None,
    pattern_separation_index: dict[str, Any] | None = None,
    hippocampal_cue_index: dict[str, Any] | None = None,
    pattern_completion_frame: dict[str, Any] | None = None,
) -> dict[str, Any]:
    structure_checks = _structure_checks(
        memory_trace_store=memory_trace_store,
        life_schema_map=life_schema_map,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        fast_episodic_buffer=fast_episodic_buffer,
        engram_cluster=engram_cluster,
        pattern_separation_index=pattern_separation_index,
        memory_longitudinal_profile=memory_longitudinal_profile,
        memory_consolidation_report=memory_consolidation_report,
    )
    function_checks = _function_checks(
        memory_trace_store=memory_trace_store,
        memory_retrieval_frame=memory_retrieval_frame,
        relationship_memory=relationship_memory,
        life_schema_map=life_schema_map,
        memory_longitudinal_profile=memory_longitudinal_profile,
        memory_consolidation_report=memory_consolidation_report,
    )
    phenomenology_checks = _phenomenology_checks(
        memory_retrieval_frame=memory_retrieval_frame,
        memory_trace_store=memory_trace_store,
        memory_longitudinal_profile=memory_longitudinal_profile,
    )
    extended_checks = _extended_checks(
        memory_trace_store=memory_trace_store,
        memory_retrieval_frame=memory_retrieval_frame,
        memory_consolidation_report=memory_consolidation_report,
        memory_longitudinal_profile=memory_longitudinal_profile,
        hippocampal_cue_index=hippocampal_cue_index,
        pattern_completion_frame=pattern_completion_frame,
    )
    all_checks = structure_checks + function_checks + phenomenology_checks + extended_checks
    structure_score = _score_from_checks(structure_checks)
    function_score = _score_from_checks(function_checks)
    phenomenology_score = _score_from_checks(phenomenology_checks)
    extended_score = _score_from_checks(extended_checks)
    overall = round(_score_from_checks(all_checks), 1)
    return {
        "schema_version": "memory_capability_scorecard_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "scorecard_ref": MEMORY_CAPABILITY_SCORECARD_REF,
        "structure_completeness_pct": structure_score,
        "functional_memory_ability_pct": function_score,
        "phenomenology_like_remembered_pct": phenomenology_score,
        "extended_capability_pct": extended_score,
        "overall_alignment_pct": overall,
        "engineering_rubric_satisfied": overall >= 100.0,
        "extended_checks": extended_checks,
        "at_human_parity_target": False,
        "human_parity_note": (
            "engineering_rubric_only; see human_brain_alignment_assessment.json"
        ),
        "structure_checks": structure_checks,
        "function_checks": function_checks,
        "phenomenology_checks": phenomenology_checks,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _structure_checks(
    *,
    memory_trace_store: dict[str, Any] | None,
    life_schema_map: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    fast_episodic_buffer: dict[str, Any] | None,
    engram_cluster: dict[str, Any] | None,
    pattern_separation_index: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
    memory_consolidation_report: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    store = memory_trace_store or {}
    live_traces = [
        trace
        for trace in store.get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    return [
        _check("live_trace_store", bool(store.get("traces"))),
        _check("live_trace_accumulation", len(live_traces) >= 1),
        _check("fast_episodic_buffer", bool(fast_episodic_buffer)),
        _check("engram_cluster", bool(engram_cluster)),
        _check(
            "pattern_separation_multi_relation",
            int((pattern_separation_index or {}).get("multi_relation_subject_scope_count") or 0)
            >= 1
            or bool((pattern_separation_index or {}).get("separation_routes")),
        ),
        _check(
            "life_schema_evidence_counts",
            bool((life_schema_map or {}).get("schema_evidence_counts")),
        ),
        _check(
            "relationship_subject_scopes",
            bool((relationship_memory or {}).get("relation_subject_scopes")),
        ),
        _check(
            "autobiographical_hierarchy",
            bool((autobiographical_stack or {}).get("memory_hierarchy")),
        ),
        _check(
            "offline_consolidation_diff",
            bool((memory_consolidation_report or {}).get("consolidation_diff")),
        ),
        _check(
            "memory_longitudinal_profile",
            bool(memory_longitudinal_profile),
        ),
        _check(
            "cross_modal_on_traces",
            any(
                trace.get("cross_modal_evidence_refs")
                for trace in live_traces
            ),
        ),
        _check(
            "visual_modality_refs",
            _has_visual_modality(live_traces),
        ),
    ]


def _function_checks(
    *,
    memory_trace_store: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    life_schema_map: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
    memory_consolidation_report: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    frame = memory_retrieval_frame or {}
    profile = frame.get("recall_to_expression_profile") or {}
    phenomenology = frame.get("memory_phenomenology_profile") or {}
    store = memory_trace_store or {}
    live_traces = [
        trace
        for trace in store.get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    longitudinal = memory_longitudinal_profile or {}
    summary = longitudinal.get("slow_variable_summary") or {}
    diff = (memory_consolidation_report or {}).get("consolidation_diff") or {}
    return [
        _check(
            "cue_driven_retrieval",
            bool(frame.get("cue_terms")) or bool(profile.get("expression_source_refs")),
        ),
        _check(
            "reconsolidation_contradiction_links",
            any(trace.get("contradiction_links") for trace in store.get("traces", [])),
        ),
        _check(
            "multi_relation_scope_isolation",
            len((relationship_memory or {}).get("relation_subject_scopes") or []) >= 2
            or len(longitudinal.get("relation_subject_curves") or {}) >= 2,
        ),
        _check(
            "schema_promotion_path",
            bool((life_schema_map or {}).get("last_promoted_schema_ids"))
            or any(
                trace.get("schema_promotion_refs")
                for trace in store.get("traces", [])
                if isinstance(trace, dict)
            ),
        ),
        _check(
            "offline_replay_salience_updates",
            bool(diff.get("trace_salience_updates")),
        ),
        _check(
            "dream_hypothesis_not_fact",
            all(
                trace.get("claim_type") != "fact"
                for trace in store.get("traces", [])
                if isinstance(trace, dict)
                and trace.get("live_trace_origin") == "offline_dream_replay"
            ),
        ),
        _check(
            "confirmation_accessibility_strengthening",
            any(
                float(trace.get("accessibility_score") or 0) > 0.6
                for trace in live_traces
            ),
        ),
        _check(
            "month_scale_turn_accumulation",
            int(longitudinal.get("turn_count") or 0) >= 30
            or len(live_traces) >= 24,
        ),
        _check(
            "relationship_depth_curve_rising",
            summary.get("relationship_depth_trend") in {"rising", "stable"},
        ),
        _check(
            "self_continuity_curve_present",
            bool(longitudinal.get("self_continuity_curve")),
        ),
    ]


def _phenomenology_checks(
    *,
    memory_retrieval_frame: dict[str, Any] | None,
    memory_trace_store: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    frame = memory_retrieval_frame or {}
    phenomenology = frame.get("memory_phenomenology_profile") or {}
    profile = frame.get("recall_to_expression_profile") or {}
    longitudinal = memory_longitudinal_profile or {}
    return [
        _check(
            "uncertain_boundary_supported",
            phenomenology.get("recall_phenomenology") in {
                "uncertain",
                "partial",
                "vivid",
                "absent",
            },
        ),
        _check(
            "recall_strength_score",
            phenomenology.get("recall_strength_score") is not None,
        ),
        _check(
            "familiarity_score",
            phenomenology.get("familiarity_score") is not None,
        ),
        _check(
            "tip_of_tongue_risk",
            phenomenology.get("tip_of_tongue_risk") is not None,
        ),
        _check(
            "dream_residue_modulation",
            phenomenology.get("dream_residue_modulation") is not None,
        ),
        _check(
            "strengthening_eligible_path",
            "strengthening_eligible" in phenomenology,
        ),
        _check(
            "closure_status_wired",
            bool(profile.get("closure_status")),
        ),
        _check(
            "cross_modal_grounding",
            int(phenomenology.get("cross_modal_evidence_ref_count") or 0) >= 1
            or bool(phenomenology.get("cross_modal_evidence_refs")),
        ),
        _check(
            "accessibility_curve_observable",
            bool(longitudinal.get("accessibility_curve")),
        ),
        _check(
            "recall_strength_curve_observable",
            bool(longitudinal.get("recall_strength_curve")),
        ),
    ]


def _extended_checks(
    *,
    memory_trace_store: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
    memory_consolidation_report: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
    hippocampal_cue_index: dict[str, Any] | None,
    pattern_completion_frame: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    frame = memory_retrieval_frame or {}
    report = memory_consolidation_report or {}
    longitudinal = memory_longitudinal_profile or {}
    diff = report.get("consolidation_diff") or {}
    live_traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    reconstructive = (pattern_completion_frame or {}).get("reconstructive_completion") or {}
    return [
        _check(
            "hippocampal_cue_index_bindings",
            bool((hippocampal_cue_index or {}).get("cue_bindings")),
        ),
        _check(
            "reconstructive_recall_profile",
            bool(frame.get("reconstructive_recall_profile"))
            or bool(reconstructive.get("reconstruction_fragments")),
        ),
        _check(
            "expression_material_chain",
            bool(frame.get("memory_expression_material_chain")),
        ),
        _check(
            "cross_modal_feature_bundle_encoded",
            any(trace.get("cross_modal_feature_bundle") for trace in live_traces),
        ),
        _check(
            "visual_feature_encoding_present",
            any(
                (trace.get("cross_modal_feature_bundle") or {}).get(
                    "visual_feature_encoding_present"
                )
                for trace in live_traces
            ),
        ),
        _check(
            "swr_weighted_replay_policy",
            report.get("replay_selection_policy") == "swr_weighted",
        ),
        _check(
            "relationship_narrative_rewrite",
            bool(diff.get("relationship_self_narrative_rewrite_diff"))
            or any(
                trace.get("relationship_narrative_rewrite_ref")
                for trace in (memory_trace_store or {}).get("traces", [])
                if isinstance(trace, dict)
            ),
        ),
        _check(
            "cortical_transfer_diff",
            bool(diff.get("cortical_transfer_diff"))
            or any(trace.get("cortical_transfer_state") for trace in live_traces),
        ),
        _check(
            "process_long_run_evidence",
            bool(longitudinal.get("process_long_run_evidence")),
        ),
        _check(
            "multiweek_schema_promotion_policy",
            bool((frame.get("schema_memory_hits") or []))
            or bool(
                (memory_trace_store or {})
                and any(trace.get("schema_promotion_refs") for trace in live_traces)
            ),
        ),
    ]


def _has_visual_modality(live_traces: list[dict[str, Any]]) -> bool:
    visual_markers = (
        "visual_percept",
        "observation/visual",
        "periphery_normalization",
        "world_observation_route",
    )
    for trace in live_traces:
        bundle = trace.get("cross_modal_feature_bundle") or {}
        if bundle.get("visual_feature_encoding_present"):
            return True
        refs = _string_list(trace.get("cross_modal_evidence_refs")) + _string_list(
            trace.get("source_evidence_refs")
        )
        if any(any(marker in ref for marker in visual_markers) for ref in refs):
            return True
    return False


def _check(check_id: str, passed: bool) -> dict[str, Any]:
    return {"check_id": check_id, "passed": passed}


def _score_from_checks(checks: list[dict[str, Any]]) -> float:
    if not checks:
        return 0.0
    passed = sum(1 for item in checks if item.get("passed"))
    return round(100.0 * passed / len(checks), 1)


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []