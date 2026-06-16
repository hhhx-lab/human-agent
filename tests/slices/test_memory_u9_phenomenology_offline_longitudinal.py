import unittest

from life_v0.state_store.cross_modal_evidence import collect_cross_modal_source_evidence
from life_v0.state_store.memory_retrieval import (
    build_memory_retrieval_frame,
    merge_cue_candidates,
    project_memory_retrieval_from_live_turn,
)
from life_v0.state_store.memory_trace_store import (
    build_memory_trace_store,
    guard_offline_trace_mutations,
)
from life_v0.state_store.offline_memory_consolidation import (
    apply_offline_memory_consolidation,
)
from life_v0.state_store.pattern_separation import build_pattern_separation_index
from life_v0.state_store.relationship_memory import project_relationship_memory


class MemoryU9PhenomenologyOfflineLongitudinalTests(unittest.TestCase):
    def test_recall_without_source_sets_uncertain_phenomenology(self):
        frame = build_memory_retrieval_frame(
            run_id="u9-uncertain",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得我们上次聊的 X 吗？",
        )
        phenomenology = frame.get("memory_phenomenology_profile") or {}
        profile = frame.get("recall_to_expression_profile") or {}
        self.assertEqual(phenomenology.get("recall_phenomenology"), "uncertain")
        self.assertTrue(phenomenology.get("uncertain_boundary_active"))
        self.assertEqual(
            profile.get("closure_status"),
            "withhold_pending_reconstruction",
        )

    def test_confirmation_marks_strengthening_eligible(self):
        frame = build_memory_retrieval_frame(
            run_id="u9-confirm",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="没错，你记得对。",
            engram_index={
                "live_memory_trace_refs": [
                    "runtime/state/memory/memory_trace_store.json#memory-trace-live"
                ]
            },
        )
        phenomenology = frame.get("memory_phenomenology_profile") or {}
        self.assertTrue(phenomenology.get("strengthening_eligible"))

    def test_cross_modal_evidence_collects_action_and_percept_modalities(self):
        evidence = collect_cross_modal_source_evidence(
            language_percept={"percept_cue_refs": ["runtime/state/language/language_percept_frame.json#cue-1"]},
            world_contact_summary={
                "contact_event_refs": ["runtime/state/membrane/world_contact_summary.json#event-1"]
            },
            responsibility_loop_state={
                "repair_obligation_refs": ["runtime/state/action/responsibility_loop_state.json#repair-1"],
                "action_outcome_refs": ["runtime/state/action/responsibility_loop_state.json#action-1"],
            },
            percept_frame_present=True,
            world_contact_present=True,
        )
        self.assertIn("language_percept", evidence.get("evidence_modalities"))
        self.assertIn("world_contact", evidence.get("evidence_modalities"))
        self.assertIn("action_responsibility", evidence.get("evidence_modalities"))
        self.assertGreaterEqual(evidence.get("evidence_modal_count"), 3)

    def test_offline_consolidation_applies_trace_salience_and_dream_hypothesis(self):
        store = build_memory_trace_store(
            run_id="u9-offline",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "repair topic",
                "semantic_focus": "repair_topic",
            },
        )
        live_trace_id = next(
            trace["trace_id"]
            for trace in store.get("traces", [])
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        )
        schema_map = {
            "schemas": [
                {
                    "schema_id": "life-schema-relationship_schema-abc",
                    "schema_kind": "relationship_schema",
                    "trace_refs": [
                        f"runtime/state/memory/memory_trace_store.json#{live_trace_id}"
                    ],
                }
            ],
            "last_promoted_schema_ids": ["life-schema-relationship_schema-abc"],
            "schema_evidence_counts": {"life-schema-relationship_schema-abc": 3},
        }
        dream_window = {
            "dream_window_id": "dream-window-u9-offline",
            "memory_consolidation_trace_refs": [
                f"runtime/state/memory/memory_trace_store.json#{live_trace_id}"
            ],
            "relationship_deep_dream_refs": [
                "runtime/state/memory/relationship_memory.json#we_memory_traces"
            ],
            "source_trace_refs": [
                f"runtime/state/memory/memory_trace_store.json#{live_trace_id}"
            ],
        }
        result = apply_offline_memory_consolidation(
            run_id="u9-offline",
            generated_at="2026-06-16T02:00:00+00:00",
            memory_trace_store=store,
            life_schema_map=schema_map,
            relationship_memory={"we_memory_traces": []},
            autobiographical_stack={"memory_hierarchy": {"specific_episode_refs": []}},
            replay_cue_bundle={
                "memory_consolidation_bridge": {
                    "trace_store_refs": ["runtime/state/memory/memory_trace_store.json"]
                }
            },
            dream_window=dream_window,
            offline_consolidation_frame={"consolidation_route": "dream_replay_test"},
        )
        updated_store = result["memory_trace_store"]
        updated_trace = next(
            trace
            for trace in updated_store.get("traces", [])
            if trace.get("trace_id") == live_trace_id
        )
        self.assertGreaterEqual(updated_trace.get("offline_replay_count"), 1)
        self.assertGreater(updated_trace.get("replay_salience", 0), 0.5)
        hypothesis_traces = [
            trace
            for trace in updated_store.get("traces", [])
            if trace.get("claim_type") == "hypothesis"
            and trace.get("live_trace_origin") == "offline_dream_replay"
        ]
        self.assertEqual(len(hypothesis_traces), 1)
        report = result["memory_consolidation_report"]
        diff = report.get("consolidation_diff") or {}
        self.assertTrue(diff.get("trace_salience_updates"))
        self.assertTrue(diff.get("dream_hypothesis_residue_diff"))
        self.assertTrue(diff.get("relationship_deepening_diff"))
        self.assertFalse(report["offline_mutation_guard"]["protected_mutation_blocked"])

    def test_protected_trace_blocks_offline_consolidation_mutation(self):
        store = {
            "traces": [
                {
                    "trace_id": "memory-trace-protected",
                    "lifecycle_state": "protected",
                    "claim_type": "fact",
                    "content_summary": "protected fact",
                    "live_trace_origin": "live_dialogue_turn",
                    "consolidation_state": "episodic",
                    "replay_salience": 0.5,
                    "offline_replay_count": 0,
                }
            ]
        }
        result = apply_offline_memory_consolidation(
            run_id="u9-protected",
            generated_at="2026-06-16T02:00:00+00:00",
            memory_trace_store=store,
            dream_window={"dream_window_id": "dream-window-u9-protected"},
        )
        trace = result["memory_trace_store"]["traces"][0]
        self.assertEqual(trace.get("offline_replay_count"), 0)
        guard = guard_offline_trace_mutations(
            before_traces=store["traces"],
            after_traces=[{**trace, "content_summary": "mutated"}],
        )
        self.assertTrue(guard.get("protected_mutation_blocked"))

    def test_multi_relation_longitudinal_isolation_over_turns(self):
        relationship_graph = {
            "subjects": [
                {
                    "relationship_id": "person-a",
                    "preference_hypotheses": ["tea"],
                },
                {
                    "relationship_id": "person-b",
                    "preference_hypotheses": ["coffee"],
                },
            ]
        }
        relationship_memory = project_relationship_memory(
            relationship_memory={"relation_person_profile": {}},
            relationship_graph=relationship_graph,
        )
        trace_store = {"traces": []}
        for turn in range(10):
            subject_id = "person-a" if turn % 2 == 0 else "person-b"
            beverage = "tea" if subject_id == "person-a" else "coffee"
            turn_store = build_memory_trace_store(
                run_id=f"u9-long-{turn}",
                generated_at=f"2026-06-16T00:{turn:02d}:00+00:00",
                live_turn_context={
                    "dialogue_turn_refs": [
                        f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 1}",
                        f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 2}",
                    ],
                    "external_utterance": f"{subject_id} likes {beverage} turn {turn}",
                    "semantic_focus": f"{subject_id}_{beverage}_preference",
                    "relationship_scope": f"relation_subject:{subject_id}",
                    "relation_subject_id": subject_id,
                },
                existing_memory_trace_store=trace_store,
            )
            trace_store = turn_store

        for subject_id, beverage in (("person-a", "tea"), ("person-b", "coffee")):
            merge = merge_cue_candidates(
                cue_terms=[beverage],
                memory_trace_store=trace_store,
                relationship_memory={
                    **relationship_memory,
                    "relationship_scope": f"relation_subject:{subject_id}",
                    "active_relation_subject_id": subject_id,
                },
                blocked_refs=[],
                provider_name="local_full_text",
            )
            eligible = merge.get("eligible_candidate_trace_refs") or []
            self.assertTrue(eligible)
            for ref in eligible:
                trace_id = ref.rsplit("#", 1)[-1]
                trace = next(
                    t for t in trace_store["traces"] if t.get("trace_id") == trace_id
                )
                self.assertEqual(trace.get("relation_subject_id"), subject_id)

            separation = build_pattern_separation_index(
                run_id=f"u9-sep-{subject_id}",
                generated_at="2026-06-16T01:00:00+00:00",
                memory_trace_store=trace_store,
                relationship_memory={
                    **relationship_memory,
                    "relationship_scope": f"relation_subject:{subject_id}",
                    "active_relation_subject_id": subject_id,
                },
            )
            self.assertGreaterEqual(
                separation.get("multi_relation_subject_scope_count", 0), 2
            )

            frame = project_memory_retrieval_from_live_turn(
                memory_retrieval_frame=None,
                run_id=f"u9-recall-{subject_id}",
                generated_at="2026-06-16T01:00:00+00:00",
                external_utterance=f"你还记得我喜欢什么？",
                semantic_map={"semantic_focus": f"{subject_id}_preference"},
                language_percept={},
                engram_index={
                    "live_memory_trace_refs": eligible,
                },
                relationship_memory={
                    **relationship_memory,
                    "relationship_scope": f"relation_subject:{subject_id}",
                    "active_relation_subject_id": subject_id,
                },
                autobiographical_stack={},
                dialogue_memory_summary={},
                life_state={},
                responsibility_loop_state={},
                state_merge_guard={},
                memory_trace_store=trace_store,
            )
            phenomenology = frame.get("memory_phenomenology_profile") or {}
            self.assertIn(
                phenomenology.get("recall_phenomenology"),
                {"vivid", "partial", "uncertain"},
            )
            self.assertNotEqual(
                frame["recall_to_expression_profile"].get("closure_status"),
                "open_no_retrievable_expression_material",
            )


if __name__ == "__main__":
    unittest.main()