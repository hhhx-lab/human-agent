import unittest

from life_v0.language.pragmatic_inference import detect_memory_feedback_from_utterance
from life_v0.state_store.cross_modal_evidence import collect_cross_modal_source_evidence
from life_v0.state_store.engram_cluster import build_engram_like_trace_cluster
from life_v0.state_store.life_schema_map import project_life_schema_map_from_live_turn
from life_v0.state_store.hippocampal_cue_index import build_hippocampal_cue_index
from life_v0.state_store.memory_capability_scorecard import (
    build_memory_capability_scorecard,
)
from life_v0.state_store.memory_engineering_completion_gate import (
    build_memory_engineering_completion_gate,
)
from life_v0.state_store.pattern_completion import build_pattern_completion_frame
from life_v0.state_store.memory_longitudinal_profile import (
    project_memory_longitudinal_profile_from_live_turn,
)
from life_v0.state_store.memory_retrieval import (
    build_memory_retrieval_frame,
    project_memory_retrieval_from_live_turn,
)
from life_v0.state_store.memory_trace_store import (
    apply_post_expression_reconsolidation,
    build_memory_trace_store,
)
from life_v0.state_store.offline_memory_consolidation import (
    apply_offline_memory_consolidation,
)
from life_v0.state_store.pattern_separation import build_pattern_separation_index
from life_v0.state_store.relationship_memory import project_relationship_memory


def _month_scale_memory_fixture() -> dict[str, object]:
    relationship_memory = project_relationship_memory(
        relationship_memory={"relation_person_profile": {}},
        relationship_graph={
            "subjects": [
                {"relationship_id": "person-a", "preference_hypotheses": ["tea"]},
                {"relationship_id": "person-b", "preference_hypotheses": ["coffee"]},
            ]
        },
    )
    autobiographical_stack = {
        "memory_hierarchy": {"specific_episode_refs": [], "general_event_threads": []},
    }
    trace_store = None
    longitudinal = None
    cross_modal = collect_cross_modal_source_evidence(
        language_percept={"percept_cue_refs": ["runtime/state/language/language_percept_frame.json#cue-visual"]},
        world_contact_summary={
            "contact_event_refs": ["runtime/state/membrane/world_contact_summary.json#event-visual"],
            "active_sampling_expected_observation_refs": [
                "runtime/state/observation/world_observation_route.json#visual-scene-1"
            ],
        },
        responsibility_loop_state={
            "repair_obligation_refs": ["runtime/state/action/responsibility_loop_state.json#repair-1"],
            "action_outcome_refs": ["runtime/state/action/responsibility_loop_state.json#action-1"],
        },
        signal_media_runtime={
            "body_signal_profile": {
                "visual_channel_refs": [
                    "runtime/state/observation/world_observation_route.json#visual-scene-1"
                ]
            }
        },
        world_observation_route={"visual_scene_refs": ["runtime/state/observation/world_observation_route.json#scene-a"]},
        periphery_normalization_trace={"promoted_channels": ["visual_channel_live"]},
        percept_frame_present=True,
        world_contact_present=True,
        visual_percept_present=True,
    )

    for turn in range(30):
        subject_id = "person-a" if turn % 2 == 0 else "person-b"
        beverage = "tea" if subject_id == "person-a" else "coffee"
        trace_store = build_memory_trace_store(
            run_id=f"u12-month-{turn}",
            generated_at=f"2026-06-{1 + turn // 28:02d}T{turn % 24:02d}:00:00+00:00",
            relationship_memory=relationship_memory,
            autobiographical_stack=autobiographical_stack,
            live_turn_context={
                "dialogue_turn_refs": [
                    f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 1}",
                    f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 2}",
                ],
                "external_utterance": f"{subject_id} likes {beverage} at turn {turn}",
                "semantic_focus": "relationship_continuity_and_repair",
                "relationship_scope": f"relation_subject:{subject_id}",
                "relation_subject_id": subject_id,
                **cross_modal,
            },
            existing_memory_trace_store=trace_store,
        )
        frame = build_memory_retrieval_frame(
            run_id=f"u12-month-{turn}",
            generated_at=f"2026-06-{1 + turn // 28:02d}T{turn % 24:02d}:00:00+00:00",
            external_utterance=f"你还记得我喜欢什么？ turn {turn}",
            engram_index={
                "live_memory_trace_refs": [
                    f"runtime/state/memory/memory_trace_store.json#{trace['trace_id']}"
                    for trace in trace_store.get("traces", [])
                    if trace.get("live_trace_origin") == "live_dialogue_turn"
                ][-2:]
            },
            relationship_memory={
                **relationship_memory,
                "relationship_scope": f"relation_subject:{subject_id}",
                "active_relation_subject_id": subject_id,
            },
            memory_trace_store=trace_store,
        )
        longitudinal = project_memory_longitudinal_profile_from_live_turn(
            profile=longitudinal,
            run_id=f"u12-month-{turn}",
            generated_at=f"2026-06-{1 + turn // 28:02d}T{turn % 24:02d}:00:00+00:00",
            memory_trace_store=trace_store,
            relationship_memory=relationship_memory,
            autobiographical_stack=autobiographical_stack,
            memory_phenomenology_profile=frame.get("memory_phenomenology_profile"),
            cross_modal_evidence=cross_modal,
        )

    correction_feedback = detect_memory_feedback_from_utterance(
        "你记错了，是咖啡。",
        dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-61",
    )
    reconsolidation = apply_post_expression_reconsolidation(
        trace_store,
        feedback_event=correction_feedback,
        run_id="u12-correct",
        generated_at="2026-06-16T12:00:00+00:00",
        relationship_memory=relationship_memory,
        state_merge_guard={},
        exclude_dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-61",
    )
    trace_store = reconsolidation["memory_trace_store"]

    confirm_feedback = detect_memory_feedback_from_utterance(
        "没错，你记得对。",
        dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-62",
    )
    reconsolidation = apply_post_expression_reconsolidation(
        trace_store,
        feedback_event=confirm_feedback,
        run_id="u12-confirm",
        generated_at="2026-06-16T13:00:00+00:00",
        relationship_memory=relationship_memory,
        state_merge_guard={},
        exclude_dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-62",
    )
    trace_store = reconsolidation["memory_trace_store"]

    life_schema_map = project_life_schema_map_from_live_turn(
        life_schema_map=None,
        run_id="u12-schema",
        generated_at="2026-06-16T14:00:00+00:00",
        memory_trace_store=trace_store,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        memory_longitudinal_profile=longitudinal,
    )
    engram_cluster = build_engram_like_trace_cluster(
        run_id="u12-cluster",
        generated_at="2026-06-16T14:00:00+00:00",
        memory_trace_store=trace_store,
        engram_index={
            "live_memory_trace_refs": [
                f"runtime/state/memory/memory_trace_store.json#{trace['trace_id']}"
                for trace in trace_store.get("traces", [])
                if trace.get("live_trace_origin") == "live_dialogue_turn"
            ][:8]
        },
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
    )
    pattern_separation_index = build_pattern_separation_index(
        run_id="u12-sep",
        generated_at="2026-06-16T14:00:00+00:00",
        engram_cluster=engram_cluster,
        memory_trace_store=trace_store,
        relationship_memory=relationship_memory,
    )
    live_refs = [
        f"runtime/state/memory/memory_trace_store.json#{trace['trace_id']}"
        for trace in trace_store.get("traces", [])
        if trace.get("live_trace_origin") == "live_dialogue_turn"
    ][-4:]
    memory_retrieval_frame = project_memory_retrieval_from_live_turn(
        memory_retrieval_frame=None,
        run_id="u12-recall",
        generated_at="2026-06-16T14:00:00+00:00",
        external_utterance="你还记得我们上次聊的饮料偏好吗？",
        semantic_map={"semantic_focus": "shared_beverage_preference"},
        language_percept={},
        engram_index={"live_memory_trace_refs": live_refs},
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        dialogue_memory_summary={},
        life_state={},
        responsibility_loop_state={},
        state_merge_guard={},
        memory_trace_store=trace_store,
        life_schema_map=life_schema_map,
    )
    consolidation = apply_offline_memory_consolidation(
        run_id="u12-offline",
        generated_at="2026-06-16T15:00:00+00:00",
        memory_trace_store=trace_store,
        life_schema_map=life_schema_map,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        memory_longitudinal_profile=longitudinal,
        dream_window={
            "dream_window_id": "dream-window-u12",
            "memory_consolidation_trace_refs": live_refs,
            "relationship_deep_dream_refs": [
                "runtime/state/memory/relationship_memory.json#we_memory_traces"
            ],
            "source_trace_refs": live_refs,
        },
        replay_cue_bundle={
            "memory_consolidation_bridge": {
                "trace_store_refs": ["runtime/state/memory/memory_trace_store.json"]
            }
        },
    )
    hippocampal_cue_index = build_hippocampal_cue_index(
        run_id="u12-hippo",
        generated_at="2026-06-16T14:30:00+00:00",
        memory_trace_store=consolidation["memory_trace_store"],
    )
    pattern_completion_frame = build_pattern_completion_frame(
        run_id="u12-complete",
        generated_at="2026-06-16T14:30:00+00:00",
        memory_retrieval_frame=memory_retrieval_frame,
        memory_trace_store=consolidation["memory_trace_store"],
        hippocampal_cue_index=hippocampal_cue_index,
    )
    memory_retrieval_frame = project_memory_retrieval_from_live_turn(
        memory_retrieval_frame=memory_retrieval_frame,
        run_id="u12-recall-final",
        generated_at="2026-06-16T14:45:00+00:00",
        external_utterance="你还记得我们上次聊的饮料偏好吗？",
        semantic_map={"semantic_focus": "relationship_continuity_and_repair"},
        language_percept={},
        engram_index={"live_memory_trace_refs": live_refs},
        relationship_memory=consolidation["relationship_memory"],
        autobiographical_stack=consolidation["autobiographical_stack"],
        dialogue_memory_summary={},
        life_state={},
        responsibility_loop_state={},
        state_merge_guard={},
        memory_trace_store=consolidation["memory_trace_store"],
        life_schema_map=consolidation["life_schema_map"],
        pattern_completion_frame=pattern_completion_frame,
    )
    return {
        "trace_store": consolidation["memory_trace_store"],
        "relationship_memory": consolidation["relationship_memory"],
        "autobiographical_stack": consolidation["autobiographical_stack"],
        "life_schema_map": consolidation["life_schema_map"],
        "memory_longitudinal_profile": consolidation["memory_longitudinal_profile"],
        "memory_consolidation_report": consolidation["memory_consolidation_report"],
        "memory_retrieval_frame": memory_retrieval_frame,
        "fast_episodic_buffer": trace_store.get("fast_episodic_buffer"),
        "engram_cluster": engram_cluster,
        "pattern_separation_index": pattern_separation_index,
        "hippocampal_cue_index": hippocampal_cue_index,
        "pattern_completion_frame": pattern_completion_frame,
    }


class MemoryU10U12HumanParityScorecardTests(unittest.TestCase):
    def test_visual_cross_modal_collects_visual_modality(self):
        evidence = collect_cross_modal_source_evidence(
            signal_media_runtime={
                "body_signal_profile": {
                    "visual_channel_refs": [
                        "runtime/state/observation/world_observation_route.json#scene"
                    ]
                }
            },
            world_observation_route={
                "visual_scene_refs": [
                    "runtime/state/observation/world_observation_route.json#scene"
                ]
            },
            periphery_normalization_trace={"promoted_channels": ["visual_channel"]},
            visual_percept_present=True,
        )
        self.assertIn("visual_percept", evidence.get("evidence_modalities"))
        self.assertTrue(
            any(
                "world_observation_route" in ref
                for ref in evidence.get("cross_modal_evidence_refs", [])
            )
        )

    def test_phenomenology_scores_present(self):
        fixture = _month_scale_memory_fixture()
        phenomenology = fixture["memory_retrieval_frame"].get(
            "memory_phenomenology_profile"
        ) or {}
        self.assertIsNotNone(phenomenology.get("recall_strength_score"))
        self.assertIsNotNone(phenomenology.get("familiarity_score"))
        self.assertIsNotNone(phenomenology.get("tip_of_tongue_risk"))

    def test_longitudinal_curves_accumulate_over_month_scale_turns(self):
        fixture = _month_scale_memory_fixture()
        profile = fixture["memory_longitudinal_profile"]
        self.assertGreaterEqual(profile.get("turn_count"), 30)
        self.assertTrue(profile.get("accessibility_curve"))
        self.assertTrue(profile.get("relationship_depth_curve"))
        self.assertTrue(profile.get("self_continuity_curve"))
        self.assertGreaterEqual(len(profile.get("relation_subject_curves") or {}), 2)

    def test_capability_scorecard_reaches_human_parity_target(self):
        fixture = _month_scale_memory_fixture()
        scorecard = build_memory_capability_scorecard(
            run_id="u12-scorecard",
            generated_at="2026-06-16T16:00:00+00:00",
            memory_trace_store=fixture["trace_store"],
            memory_retrieval_frame=fixture["memory_retrieval_frame"],
            relationship_memory=fixture["relationship_memory"],
            autobiographical_stack=fixture["autobiographical_stack"],
            life_schema_map=fixture["life_schema_map"],
            memory_longitudinal_profile=fixture["memory_longitudinal_profile"],
            memory_consolidation_report=fixture["memory_consolidation_report"],
            fast_episodic_buffer=fixture["fast_episodic_buffer"],
            engram_cluster=fixture["engram_cluster"],
            pattern_separation_index=fixture["pattern_separation_index"],
            hippocampal_cue_index=fixture["hippocampal_cue_index"],
            pattern_completion_frame=fixture["pattern_completion_frame"],
        )
        completion_gate = build_memory_engineering_completion_gate(
            run_id="u24-gate",
            generated_at="2026-06-16T16:00:00+00:00",
            memory_capability_scorecard=scorecard,
            memory_trace_store=fixture["trace_store"],
            memory_retrieval_frame=fixture["memory_retrieval_frame"],
            memory_consolidation_report=fixture["memory_consolidation_report"],
            memory_longitudinal_profile=fixture["memory_longitudinal_profile"],
            hippocampal_cue_index=fixture["hippocampal_cue_index"],
            pattern_completion_frame=fixture["pattern_completion_frame"],
        )
        self.assertEqual(scorecard["structure_completeness_pct"], 100.0)
        self.assertEqual(scorecard["functional_memory_ability_pct"], 100.0)
        self.assertEqual(scorecard["phenomenology_like_remembered_pct"], 100.0)
        self.assertEqual(scorecard["extended_capability_pct"], 100.0)
        self.assertEqual(scorecard["overall_alignment_pct"], 100.0)
        self.assertTrue(scorecard["engineering_rubric_satisfied"])
        self.assertFalse(scorecard["at_human_parity_target"])
        self.assertTrue(completion_gate["engineering_complete"])
        self.assertEqual(completion_gate["engineering_completion_pct"], 100.0)
        failed = [
            check
            for group in (
                scorecard["structure_checks"],
                scorecard["function_checks"],
                scorecard["phenomenology_checks"],
                scorecard["extended_checks"],
            )
            for check in group
            if not check.get("passed")
        ]
        self.assertEqual(failed, [], msg=str(failed))
        self.assertEqual(completion_gate["failed_stage_ids"], [])


if __name__ == "__main__":
    unittest.main()