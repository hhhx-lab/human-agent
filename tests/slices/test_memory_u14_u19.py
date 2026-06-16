import unittest

from life_v0.state_store.cross_modal_evidence import collect_cross_modal_source_evidence
from life_v0.state_store.human_brain_alignment_assessment import (
    build_human_brain_alignment_assessment,
)
from life_v0.state_store.life_schema_map import project_life_schema_map_from_live_turn
from life_v0.state_store.memory_expression_material_chain import (
    build_memory_expression_material_chain,
)
from life_v0.state_store.memory_longitudinal_profile import (
    project_memory_longitudinal_profile_from_live_turn,
)
from life_v0.state_store.memory_retrieval import (
    build_memory_retrieval_frame,
    memory_retrieval_context_summary,
)
from life_v0.state_store.memory_trace_store import build_memory_trace_store
from life_v0.state_store.offline_memory_consolidation import (
    apply_offline_memory_consolidation,
)


class MemoryU14U19BrainAlignmentTests(unittest.TestCase):
    def test_u14_expression_material_chain_blocks_tip_of_tongue_without_fragments(self):
        frame = build_memory_retrieval_frame(
            run_id="u14-tot",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得我们上次聊过什么吗？",
        )
        chain = frame.get("memory_expression_material_chain") or {}
        tip_gate = chain.get("tip_of_tongue_gate") or {}
        profile = frame.get("recall_to_expression_profile") or {}
        summary = memory_retrieval_context_summary(frame)

        self.assertTrue(chain.get("chain_steps"))
        self.assertEqual(tip_gate.get("gate_status"), "blocked")
        self.assertEqual(
            chain.get("expression_release_posture"),
            "withhold_pending_reconstruction",
        )
        self.assertEqual(profile.get("closure_status"), "withhold_pending_reconstruction")
        self.assertEqual(
            summary.get("expression_release_posture"),
            "withhold_pending_reconstruction",
        )

    def test_u14_material_chain_builder_audits_chain_steps(self):
        chain = build_memory_expression_material_chain(
            memory_retrieval_frame={
                "cue_terms": ["tea"],
                "memory_phenomenology_profile": {
                    "expression_material_grounded": True,
                    "recall_phenomenology": "partial",
                    "recall_strength_score": 0.62,
                    "tip_of_tongue_risk": "low",
                },
                "reconstructive_recall_profile": {
                    "hippocampal_activation_count": 2,
                    "reconstruction_fragment_refs": ["trace-a"],
                },
                "recall_to_expression_profile": {
                    "expression_source_refs": ["runtime/state/memory/memory_trace_store.json#trace-a"],
                },
            },
            pattern_completion_frame={
                "reconstructive_completion": {
                    "reconstruction_fragments": [
                        {"trace_ref": "trace-a", "episode_digest": "tea chat"}
                    ]
                }
            },
        )
        self.assertTrue(chain.get("chain_closed"))
        self.assertGreaterEqual(chain.get("reconstruction_fragment_count"), 1)

    def test_u15_cross_modal_feature_bundle_persists_on_live_trace(self):
        evidence = collect_cross_modal_source_evidence(
            language_percept={"shared_term_hits": ["茶", "tea"]},
            world_contact_summary={"contact_event_refs": ["event-1"]},
            percept_frame_present=True,
            world_contact_present=True,
        )
        store = build_memory_trace_store(
            run_id="u15-cross-modal",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "茶很好喝",
                "semantic_focus": "tea_preference",
                "cross_modal_evidence_refs": evidence.get("cross_modal_evidence_refs"),
                "cross_modal_feature_bundle": evidence.get("cross_modal_feature_bundle"),
            },
        )
        live_trace = next(
            trace
            for trace in store.get("traces", [])
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        )
        bundle = live_trace.get("cross_modal_feature_bundle") or {}
        self.assertEqual(bundle.get("schema_version"), "cross_modal_feature_bundle_v0")
        self.assertGreaterEqual(bundle.get("modality_feature_count"), 1)

    def test_u16_offline_consolidation_uses_swr_weighted_replay_policy(self):
        store = build_memory_trace_store(
            run_id="u16-swr",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-4",
                ],
                "external_utterance": "repair topic",
                "semantic_focus": "repair_topic",
                "replay_salience": 0.82,
                "accessibility_score": 0.77,
            },
        )
        result = apply_offline_memory_consolidation(
            run_id="u16-swr",
            generated_at="2026-06-16T01:00:00+00:00",
            memory_trace_store=store,
        )
        report = result.get("memory_consolidation_report") or {}
        self.assertEqual(report.get("replay_selection_policy"), "swr_weighted")
        self.assertTrue(report.get("swr_replay_weights"))
        self.assertTrue(report.get("replay_trace_ids"))

    def test_u17_schema_promotion_requires_multiweek_turn_span(self):
        traces = [
            {
                "trace_id": f"memory-trace-live-{index}",
                "live_trace_origin": "live_dialogue_turn",
                "lifecycle_state": "active",
                "semantic_focus": "relationship_continuity_and_repair",
                "content_summary": (
                    "Live relation episode centered on relationship_continuity_and_repair"
                ),
            }
            for index in range(3)
        ]
        early = project_life_schema_map_from_live_turn(
            life_schema_map=None,
            run_id="u17-schema",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_trace_store={"traces": traces},
            memory_longitudinal_profile={"turn_count": 5},
        )
        self.assertFalse(early.get("last_promoted_schema_ids"))
        late = project_life_schema_map_from_live_turn(
            life_schema_map=early,
            run_id="u17-schema",
            generated_at="2026-06-16T00:30:00+00:00",
            memory_trace_store={"traces": traces},
            memory_longitudinal_profile={"turn_count": 21},
        )
        self.assertTrue(late.get("last_promoted_schema_ids"))

    def test_u18_offline_consolidation_writes_relationship_self_narrative_rewrite(self):
        store = build_memory_trace_store(
            run_id="u18-narrative",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-5",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-6",
                ],
                "external_utterance": "我们是一起长大的",
                "semantic_focus": "shared_history",
                "relation_subject_id": "relation-subject-a",
            },
        )
        result = apply_offline_memory_consolidation(
            run_id="u18-narrative",
            generated_at="2026-06-16T02:00:00+00:00",
            memory_trace_store=store,
            relationship_memory={"shared_narrative_memory": []},
            autobiographical_stack={"general_event_threads": []},
        )
        relationship = result.get("relationship_memory") or {}
        autobiographical = result.get("autobiographical_stack") or {}
        updated_store = result.get("memory_trace_store") or {}
        rewrite_refs = [
            trace.get("relationship_narrative_rewrite_ref")
            for trace in updated_store.get("traces", [])
            if trace.get("relationship_narrative_rewrite_ref")
        ]
        self.assertTrue(relationship.get("shared_narrative_memory"))
        self.assertTrue(autobiographical.get("general_event_threads"))
        self.assertTrue(rewrite_refs)
        diff = (result.get("memory_consolidation_report") or {}).get(
            "consolidation_diff", {}
        ).get("relationship_self_narrative_rewrite_diff")
        self.assertTrue(diff)

    def test_u19_long_run_process_evidence_feeds_human_alignment_assessment(self):
        profile = {"turn_count": 0, "offline_cycle_count": 0}
        store = {"traces": []}
        for turn in range(120):
            profile = project_memory_longitudinal_profile_from_live_turn(
                profile=profile,
                run_id="u19-long-run",
                generated_at=f"2026-06-{turn + 1:02d}T00:00:00+00:00",
                memory_trace_store=store,
            )
            store = build_memory_trace_store(
                run_id="u19-long-run",
                generated_at=f"2026-06-{turn + 1:02d}T00:00:00+00:00",
                live_turn_context={
                    "dialogue_turn_refs": [
                        f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 1}",
                        f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 2}",
                    ],
                    "external_utterance": f"turn {turn}",
                    "semantic_focus": "copresence_thread",
                },
                existing_memory_trace_store=store if store.get("traces") else None,
            )
        process_long_run_evidence = {
            "process_turn_count": profile["turn_count"],
            "process_id": "u19-long-run",
            "acceptance_boundary": "unit_test_turn_simulation_not_real_months",
        }
        assessment = build_human_brain_alignment_assessment(
            run_id="u19-long-run",
            generated_at="2026-06-16T12:00:00+00:00",
            memory_trace_store=store,
            memory_longitudinal_profile=profile,
            process_long_run_evidence=process_long_run_evidence,
        )
        copresence = next(
            item
            for item in assessment.get("dimensions", [])
            if item.get("dimension_id") == "long_term_copresence"
        )
        self.assertEqual(profile["turn_count"], 120)
        self.assertGreaterEqual(float(copresence.get("score_pct")), 55.0)
        self.assertFalse(assessment.get("at_biological_human_parity"))


if __name__ == "__main__":
    unittest.main()