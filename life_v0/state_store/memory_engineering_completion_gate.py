from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "temp/14_memory_module_rebuild_audit.md",
]

MEMORY_ENGINEERING_COMPLETION_GATE_REF = (
    "runtime/reports/latest/memory_engineering_completion_gate.json"
)

U_STAGE_IDS = (
    "U1_live_projection_single_pass",
    "U2_trace_contentization",
    "U3_reconsolidation_feedback",
    "U4_cue_provider_bridge",
    "U5_fast_slow_channel",
    "U6_expression_consumption",
    "U7_longitudinal_acceptance",
    "U8_deepening",
    "U9_phenomenology_offline_longitudinal",
    "U10_u12_engineering_rubric",
    "U13_reconstructive_recall",
    "U14_expression_material_chain",
    "U15_cross_modal_feature_bundle",
    "U16_swr_weighted_replay",
    "U17_multiweek_schema_promotion",
    "U18_relationship_self_narrative_rewrite",
    "U19_process_long_run_fixture",
    "U20_visual_feature_encoding",
    "U21_cortical_slow_transfer",
    "U22_process_long_run_wiring",
    "U23_engineering_scorecard_extended",
    "U24_engineering_completion_gate",
)


def build_memory_engineering_completion_gate(
    *,
    run_id: str,
    generated_at: str,
    memory_capability_scorecard: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    memory_consolidation_report: dict[str, Any] | None = None,
    memory_longitudinal_profile: dict[str, Any] | None = None,
    hippocampal_cue_index: dict[str, Any] | None = None,
    pattern_completion_frame: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scorecard = memory_capability_scorecard or {}
    stage_checks = _u_stage_checks(
        memory_trace_store=memory_trace_store,
        memory_retrieval_frame=memory_retrieval_frame,
        memory_consolidation_report=memory_consolidation_report,
        memory_longitudinal_profile=memory_longitudinal_profile,
        hippocampal_cue_index=hippocampal_cue_index,
        pattern_completion_frame=pattern_completion_frame,
        scorecard=scorecard,
    )
    passed_stages = sum(1 for item in stage_checks if item.get("passed"))
    engineering_completion_pct = round(
        100.0 * passed_stages / len(stage_checks),
        1,
    )
    rubric_satisfied = bool(scorecard.get("engineering_rubric_satisfied"))
    all_stages_passed = passed_stages == len(stage_checks)
    engineering_complete = rubric_satisfied and all_stages_passed
    return {
        "schema_version": "memory_engineering_completion_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "gate_ref": MEMORY_ENGINEERING_COMPLETION_GATE_REF,
        "engineering_completion_pct": engineering_completion_pct,
        "engineering_rubric_satisfied": rubric_satisfied,
        "all_u_stages_passed": all_stages_passed,
        "engineering_complete": engineering_complete,
        "at_biological_human_parity": False,
        "completion_boundary": (
            "engineering_100_percent_means_rubric_plus_u_stage_artifacts_landed"
        ),
        "u_stage_checks": stage_checks,
        "failed_stage_ids": [
            item["stage_id"] for item in stage_checks if not item.get("passed")
        ],
        "scorecard_overall_alignment_pct": scorecard.get("overall_alignment_pct"),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _u_stage_checks(
    *,
    memory_trace_store: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
    memory_consolidation_report: dict[str, Any] | None,
    memory_longitudinal_profile: dict[str, Any] | None,
    hippocampal_cue_index: dict[str, Any] | None,
    pattern_completion_frame: dict[str, Any] | None,
    scorecard: dict[str, Any],
) -> list[dict[str, Any]]:
    store = memory_trace_store or {}
    frame = memory_retrieval_frame or {}
    report = memory_consolidation_report or {}
    longitudinal = memory_longitudinal_profile or {}
    live_traces = [
        trace
        for trace in store.get("traces", [])
        if isinstance(trace, dict) and trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    diff = report.get("consolidation_diff") or {}
    reconstructive = (pattern_completion_frame or {}).get("reconstructive_completion") or {}
    return [
        _stage("U1_live_projection_single_pass", bool(live_traces)),
        _stage(
            "U2_trace_contentization",
            any(trace.get("content_summary") for trace in live_traces),
        ),
        _stage(
            "U3_reconsolidation_feedback",
            any(trace.get("contradiction_links") for trace in store.get("traces", [])),
        ),
        _stage(
            "U4_cue_provider_bridge",
            bool((frame.get("cue_provider_audit") or {}).get("provider_status")),
        ),
        _stage("U5_fast_slow_channel", bool(store.get("fast_episodic_buffer"))),
        _stage(
            "U6_expression_consumption",
            bool(frame.get("recall_to_expression_profile")),
        ),
        _stage(
            "U7_longitudinal_acceptance",
            int(longitudinal.get("turn_count") or 0) >= 1,
        ),
        _stage(
            "U8_deepening",
            bool(longitudinal.get("relationship_depth_curve")),
        ),
        _stage(
            "U9_phenomenology_offline_longitudinal",
            bool(frame.get("memory_phenomenology_profile"))
            and bool(diff.get("trace_salience_updates")),
        ),
        _stage(
            "U10_u12_engineering_rubric",
            bool(scorecard.get("engineering_rubric_satisfied")),
        ),
        _stage(
            "U13_reconstructive_recall",
            bool((hippocampal_cue_index or {}).get("cue_bindings"))
            or bool(reconstructive.get("reconstruction_fragments")),
        ),
        _stage(
            "U14_expression_material_chain",
            bool(frame.get("memory_expression_material_chain")),
        ),
        _stage(
            "U15_cross_modal_feature_bundle",
            any(trace.get("cross_modal_feature_bundle") for trace in live_traces),
        ),
        _stage(
            "U16_swr_weighted_replay",
            report.get("replay_selection_policy") == "swr_weighted",
        ),
        _stage(
            "U17_multiweek_schema_promotion",
            bool((frame.get("schema_memory_hits") or []))
            or any(trace.get("schema_promotion_refs") for trace in live_traces),
        ),
        _stage(
            "U18_relationship_self_narrative_rewrite",
            bool(diff.get("relationship_self_narrative_rewrite_diff"))
            or any(
                trace.get("relationship_narrative_rewrite_ref")
                for trace in store.get("traces", [])
                if isinstance(trace, dict)
            ),
        ),
        _stage(
            "U19_process_long_run_fixture",
            int((longitudinal.get("process_long_run_evidence") or {}).get(
                "process_turn_count"
            ) or 0)
            >= 30
            or int(longitudinal.get("turn_count") or 0) >= 30,
        ),
        _stage(
            "U20_visual_feature_encoding",
            any(
                (trace.get("cross_modal_feature_bundle") or {}).get(
                    "visual_feature_encoding_present"
                )
                for trace in live_traces
            ),
        ),
        _stage(
            "U21_cortical_slow_transfer",
            bool(diff.get("cortical_transfer_diff"))
            or any(trace.get("cortical_transfer_state") for trace in live_traces),
        ),
        _stage(
            "U22_process_long_run_wiring",
            bool(longitudinal.get("process_long_run_evidence")),
        ),
        _stage(
            "U23_engineering_scorecard_extended",
            bool(scorecard.get("extended_checks")),
        ),
        _stage("U24_engineering_completion_gate", True),
    ]


def _stage(stage_id: str, passed: bool) -> dict[str, Any]:
    return {"stage_id": stage_id, "passed": passed}