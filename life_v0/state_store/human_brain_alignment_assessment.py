from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "temp/14_memory_module_rebuild_audit.md",
]

HUMAN_BRAIN_ALIGNMENT_ASSESSMENT_REF = (
    "runtime/reports/latest/human_brain_alignment_assessment.json"
)

TIER_CEILINGS = {
    "fixture_simulation": 78.0,
    "process_live_turn": 82.0,
    "calendar_months_unverified": 88.0,
}


def build_human_brain_alignment_assessment(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    pattern_completion_frame: dict[str, Any] | None = None,
    hippocampal_cue_index: dict[str, Any] | None = None,
    memory_longitudinal_profile: dict[str, Any] | None = None,
    memory_consolidation_report: dict[str, Any] | None = None,
    process_long_run_evidence: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    life_schema_map: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evidence_tier = _resolve_evidence_quality_tier(
        memory_longitudinal_profile=memory_longitudinal_profile,
        process_long_run_evidence=process_long_run_evidence,
    )
    dimensions = [
        _assess_cue_reconstructive_recall(
            pattern_completion_frame=pattern_completion_frame,
            hippocampal_cue_index=hippocampal_cue_index,
            memory_retrieval_frame=memory_retrieval_frame,
        ),
        _assess_phenomenology_grounding(memory_retrieval_frame=memory_retrieval_frame),
        _assess_cross_modal_encoding(memory_trace_store=memory_trace_store),
        _assess_sleep_replay_selection(memory_consolidation_report=memory_consolidation_report),
        _assess_schema_multiweek_evolution(
            memory_trace_store=memory_trace_store,
            memory_longitudinal_profile=memory_longitudinal_profile,
            life_schema_map=life_schema_map,
        ),
        _assess_relationship_self_rewrite(
            memory_trace_store=memory_trace_store,
            memory_longitudinal_profile=memory_longitudinal_profile,
            relationship_memory=relationship_memory,
            autobiographical_stack=autobiographical_stack,
        ),
        _assess_long_term_copresence(
            memory_longitudinal_profile=memory_longitudinal_profile,
            process_long_run_evidence=process_long_run_evidence,
            evidence_quality_tier=evidence_tier,
        ),
    ]
    raw_overall = round(
        sum(float(item["score_pct"]) for item in dimensions) / len(dimensions),
        1,
    ) if dimensions else 0.0
    tier_ceiling = TIER_CEILINGS.get(evidence_tier, 82.0)
    overall = round(min(raw_overall, tier_ceiling), 1)
    gap_closure = round(
        sum(min(100.0, float(item["score_pct"]) / 0.8) for item in dimensions)
        / len(dimensions),
        1,
    ) if dimensions else 0.0
    return {
        "schema_version": "human_brain_alignment_assessment_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "assessment_ref": HUMAN_BRAIN_ALIGNMENT_ASSESSMENT_REF,
        "overall_brain_alignment_pct": overall,
        "raw_brain_alignment_pct": raw_overall,
        "honest_estimate_band": _honest_estimate_band(overall),
        "evidence_quality_tier": evidence_tier,
        "evidence_tier_ceiling_pct": tier_ceiling,
        "gap_closure_pct": gap_closure,
        "at_biological_human_parity": False,
        "assessment_boundary": (
            "honest_multi_dimension_estimate_not_engineering_rubric_full_marks"
        ),
        "dimensions": dimensions,
        "remaining_gap_summary": [
            item["primary_gap"]
            for item in dimensions
            if float(item["score_pct"]) < 80.0
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _resolve_evidence_quality_tier(
    *,
    memory_longitudinal_profile: dict[str, Any] | None,
    process_long_run_evidence: dict[str, Any] | None,
) -> str:
    evidence = process_long_run_evidence or (
        (memory_longitudinal_profile or {}).get("process_long_run_evidence") or {}
    )
    boundary = str(evidence.get("acceptance_boundary") or "")
    if any(
        marker in boundary
        for marker in (
            "fixture",
            "simulation",
            "unit_test",
            "turn_counter_not_calendar",
            "not_calendar_months",
        )
    ):
        return "fixture_simulation"
    if "calendar_months_verified" in boundary:
        return "calendar_months_unverified"
    if evidence.get("process_id") or evidence.get("process_run_id"):
        return "process_live_turn"
    turn_count = int((memory_longitudinal_profile or {}).get("turn_count") or 0)
    if turn_count >= 1:
        return "process_live_turn"
    return "fixture_simulation"


def _honest_estimate_band(overall: float) -> str:
    if overall < 45.0:
        return "emerging"
    if overall < 60.0:
        return "developing"
    if overall < 75.0:
        return "maturing"
    return "advanced"


def _assess_cue_reconstructive_recall(
    *,
    pattern_completion_frame: dict[str, Any] | None,
    hippocampal_cue_index: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
) -> dict[str, Any]:
    fragments = _reconstruction_fragments(pattern_completion_frame)
    bindings = len((hippocampal_cue_index or {}).get("cue_bindings") or [])
    reconstructive_profile = (memory_retrieval_frame or {}).get(
        "reconstructive_recall_profile"
    ) or {}
    reconstructive = (pattern_completion_frame or {}).get("reconstructive_completion") or {}
    completion_mode = (
        reconstructive_profile.get("completion_mode")
        or reconstructive.get("completion_mode")
        or ("reconstructive_fragment_assembly" if fragments else "ref_only_fallback")
    )
    score = 15.0
    if bindings >= 4:
        score += 15.0
    if bindings >= 12:
        score += 5.0
    if fragments:
        score += 20.0
    if len(fragments) >= 3:
        score += 5.0
    if any(float(fragment.get("activation_score") or 0) >= 2.5 for fragment in fragments):
        score += 15.0
    if completion_mode == "reconstructive_fragment_assembly":
        score += 20.0
    if reconstructive_profile.get("reconstruction_fragment_count"):
        score += 5.0
    return {
        "dimension_id": "cue_reconstructive_recall",
        "score_pct": round(min(100.0, score), 1),
        "primary_gap": "召回需海马 cue 绑定 + 片段补全，不是 ref 拼接",
        "evidence": {
            "hippocampal_binding_count": bindings,
            "reconstruction_fragment_count": len(fragments),
            "completion_mode": completion_mode,
            "retrieval_profile_mode": reconstructive_profile.get("completion_mode"),
        },
    }


def _assess_phenomenology_grounding(
    *, memory_retrieval_frame: dict[str, Any] | None
) -> dict[str, Any]:
    phenomenology = (memory_retrieval_frame or {}).get("memory_phenomenology_profile") or {}
    material_chain = (memory_retrieval_frame or {}).get(
        "memory_expression_material_chain"
    ) or {}
    tip_gate = material_chain.get("tip_of_tongue_gate") or {}
    chain_steps = material_chain.get("chain_steps") or []
    passed_steps = sum(
        1 for step in chain_steps if isinstance(step, dict) and step.get("passed")
    )
    score = 10.0
    recall_phenomenology = phenomenology.get("recall_phenomenology")
    if recall_phenomenology:
        score += 10.0
    if recall_phenomenology in {"vivid", "partial"}:
        score += 10.0
    if phenomenology.get("recall_strength_score") is not None:
        score += 5.0
    if float(phenomenology.get("recall_strength_score") or 0) >= 0.55:
        score += 10.0
    if phenomenology.get("tip_of_tongue_risk"):
        score += 5.0
    if phenomenology.get("expression_material_grounded"):
        score += 15.0
    if material_chain.get("chain_steps"):
        score += 10.0
    if passed_steps >= 4:
        score += 10.0
    if material_chain.get("tip_of_tongue_gate"):
        score += 5.0
    if material_chain.get("chain_closed"):
        score += 15.0
    if tip_gate.get("gate_status") == "blocked":
        score += 5.0
    return {
        "dimension_id": "phenomenology_like_remembered",
        "score_pct": round(min(100.0, score), 1),
        "primary_gap": "现象层需表达材料链落地，不是 JSON 标签",
        "evidence": {
            "recall_phenomenology": recall_phenomenology,
            "expression_material_grounded": phenomenology.get("expression_material_grounded"),
            "expression_material_chain_closed": material_chain.get("chain_closed"),
            "material_chain_passed_steps": passed_steps,
            "tip_of_tongue_gate_status": tip_gate.get("gate_status"),
        },
    }


def _assess_cross_modal_encoding(
    *, memory_trace_store: dict[str, Any] | None
) -> dict[str, Any]:
    live_traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    with_cross_modal = sum(1 for trace in live_traces if trace.get("cross_modal_evidence_refs"))
    with_encoded_features = sum(
        1 for trace in live_traces if trace.get("cross_modal_feature_bundle")
    )
    with_visual_encoding = sum(
        1
        for trace in live_traces
        if (trace.get("cross_modal_feature_bundle") or {}).get(
            "visual_feature_encoding_present"
        )
    )
    modality_counts = [
        int((trace.get("cross_modal_feature_bundle") or {}).get("modality_feature_count") or 0)
        for trace in live_traces
    ]
    mean_modalities = (
        round(sum(modality_counts) / len(modality_counts), 2) if modality_counts else 0.0
    )
    visual_ratio = (with_visual_encoding / len(live_traces)) if live_traces else 0.0
    score = 10.0
    if with_cross_modal:
        score += 15.0
    if with_encoded_features:
        score += 25.0
    if with_visual_encoding:
        score += 15.0
    if visual_ratio >= 0.5:
        score += 10.0
    if visual_ratio >= 0.8:
        score += 10.0
    if mean_modalities >= 2.0:
        score += 10.0
    if mean_modalities >= 3.0:
        score += 5.0
    return {
        "dimension_id": "cross_modal_encoding",
        "score_pct": round(min(100.0, score), 1),
        "primary_gap": "跨模态需特征束进 engram，不是路径 ref",
        "evidence": {
            "live_trace_count": len(live_traces),
            "cross_modal_ref_traces": with_cross_modal,
            "cross_modal_feature_traces": with_encoded_features,
            "visual_feature_encoding_traces": with_visual_encoding,
            "visual_feature_encoding_ratio": round(visual_ratio, 3),
            "mean_modality_feature_count": mean_modalities,
        },
    }


def _assess_sleep_replay_selection(
    *, memory_consolidation_report: dict[str, Any] | None
) -> dict[str, Any]:
    diff = (memory_consolidation_report or {}).get("consolidation_diff") or {}
    salience_updates = diff.get("trace_salience_updates") or []
    cortical_diff = diff.get("cortical_transfer_diff") or []
    cortical_linked = sum(
        1
        for item in cortical_diff
        if isinstance(item, dict)
        and item.get("to_state") == "cortical_linked"
    )
    score = 15.0
    if salience_updates:
        score += 20.0
    if (memory_consolidation_report or {}).get("replay_selection_policy") == "swr_weighted":
        score += 20.0
    if cortical_diff:
        score += 20.0
    if cortical_linked:
        score += 15.0
    if (memory_consolidation_report or {}).get("cortical_transfer_policy"):
        score += 10.0
    return {
        "dimension_id": "sleep_replay_selection",
        "score_pct": round(min(100.0, score), 1),
        "primary_gap": "离线 replay 需 SWR 加权选择，不是浅层 salience bump",
        "evidence": {
            "salience_update_count": len(salience_updates),
            "replay_selection_policy": (memory_consolidation_report or {}).get(
                "replay_selection_policy"
            ),
            "cortical_transfer_count": len(cortical_diff),
            "cortical_linked_count": cortical_linked,
        },
    }


def _assess_schema_multiweek_evolution(
    *,
    memory_trace_store: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
    life_schema_map: dict[str, Any] | None,
) -> dict[str, Any]:
    turn_count = int((memory_longitudinal_profile or {}).get("turn_count") or 0)
    live_count = sum(
        1
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("live_trace_origin") == "live_dialogue_turn"
    )
    promoted_schema_count = sum(
        1
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("schema_promotion_refs")
    )
    cortical_linked_traces = sum(
        1
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("cortical_transfer_state")
    )
    schema_map = life_schema_map or {}
    score = 10.0
    if turn_count >= 21:
        score += 15.0
    if turn_count >= 30 or live_count >= 24:
        score += 10.0
    if turn_count >= 90:
        score += 15.0
    if promoted_schema_count:
        score += 15.0
    if cortical_linked_traces:
        score += 10.0
    if schema_map.get("schema_promotion_policy") == "multi_week_evidence_not_count_only":
        score += 10.0
    if schema_map.get("cortical_integration_refs"):
        score += 10.0
    if schema_map.get("last_promoted_schema_ids"):
        score += 5.0
    return {
        "dimension_id": "fast_to_slow_schema",
        "score_pct": round(min(100.0, score), 1),
        "primary_gap": "schema 化需多周真实演化，不是计数到 3 即 promotion",
        "evidence": {
            "turn_count": turn_count,
            "live_trace_count": live_count,
            "schema_linked_trace_count": promoted_schema_count,
            "cortical_linked_trace_count": cortical_linked_traces,
            "schema_promotion_policy": schema_map.get("schema_promotion_policy"),
        },
    }


def _assess_relationship_self_rewrite(
    *,
    memory_trace_store: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
) -> dict[str, Any]:
    score = 10.0
    summary = (memory_longitudinal_profile or {}).get("slow_variable_summary") or {}
    if summary.get("relationship_depth_trend") in {"rising", "stable"}:
        score += 15.0
    if summary.get("self_continuity_trend") in {"rising", "stable"}:
        score += 15.0
    narrative_rewrite_refs = [
        trace.get("relationship_narrative_rewrite_ref")
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("relationship_narrative_rewrite_ref")
    ]
    if narrative_rewrite_refs:
        score += 25.0
    shared_narratives = (relationship_memory or {}).get("shared_narrative_memory") or []
    if isinstance(shared_narratives, list) and shared_narratives:
        score += 15.0
    self_threads = (autobiographical_stack or {}).get("general_event_threads") or []
    if isinstance(self_threads, list) and self_threads:
        score += 10.0
    if (relationship_memory or {}).get("relationship_narrative_last_rewrite_at"):
        score += 5.0
    if (autobiographical_stack or {}).get("self_narrative_last_rewrite_at"):
        score += 5.0
    return {
        "dimension_id": "relationship_self_slow_variables",
        "score_pct": round(min(100.0, score), 1),
        "primary_gap": "关系/自我需叙事重写证据，不是统计曲线",
        "evidence": {
            "relationship_depth_trend": summary.get("relationship_depth_trend"),
            "self_continuity_trend": summary.get("self_continuity_trend"),
            "narrative_rewrite_ref_count": len(narrative_rewrite_refs),
            "shared_narrative_entry_count": len(shared_narratives)
            if isinstance(shared_narratives, list)
            else 0,
            "self_narrative_thread_count": len(self_threads)
            if isinstance(self_threads, list)
            else 0,
        },
    }


def _assess_long_term_copresence(
    *,
    memory_longitudinal_profile: dict[str, Any] | None,
    process_long_run_evidence: dict[str, Any] | None,
    evidence_quality_tier: str,
) -> dict[str, Any]:
    longitudinal = memory_longitudinal_profile or {}
    turn_count = int(longitudinal.get("turn_count") or 0)
    process_turns = int((process_long_run_evidence or {}).get("process_turn_count") or 0)
    relation_curves = len(longitudinal.get("relation_subject_curves") or {})
    offline_cycles = int(longitudinal.get("offline_cycle_count") or 0)
    score = 10.0
    if turn_count >= 30:
        score += 15.0
    if process_turns >= 30:
        score += 10.0
    if process_turns >= 90:
        score += 15.0
    if process_turns >= 120:
        score += 15.0
    if relation_curves >= 2:
        score += 15.0
    if offline_cycles >= 1:
        score += 10.0
    if longitudinal.get("offline_consolidation_curve"):
        score += 10.0
    raw = round(min(100.0, score), 1)
    if evidence_quality_tier == "fixture_simulation":
        capped = min(raw, 58.0)
    elif evidence_quality_tier == "process_live_turn":
        capped = min(raw, 72.0)
    else:
        capped = min(raw, 85.0)
    return {
        "dimension_id": "long_term_copresence",
        "score_pct": capped,
        "raw_score_pct": raw,
        "primary_gap": "需数月真实共在 process 长跑，不是单测夹具",
        "evidence": {
            "longitudinal_turn_count": turn_count,
            "process_turn_count": process_turns,
            "relation_subject_curve_count": relation_curves,
            "offline_cycle_count": offline_cycles,
            "evidence_quality_tier": evidence_quality_tier,
        },
    }


def _reconstruction_fragments(pattern_completion_frame: dict[str, Any] | None) -> list[dict[str, Any]]:
    fragments: list[dict[str, Any]] = []
    for candidate in (pattern_completion_frame or {}).get("completion_candidates", []):
        if not isinstance(candidate, dict):
            continue
        for fragment in candidate.get("reconstruction_fragments", []):
            if isinstance(fragment, dict):
                fragments.append(fragment)
    reconstructive = (pattern_completion_frame or {}).get("reconstructive_completion") or {}
    if isinstance(reconstructive, dict):
        for fragment in reconstructive.get("reconstruction_fragments", []):
            if isinstance(fragment, dict):
                fragments.append(fragment)
    return fragments