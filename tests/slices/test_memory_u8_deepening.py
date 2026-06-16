import unittest

from life_v0.state_store.memory_retrieval import (
    build_memory_retrieval_frame,
    merge_cue_candidates,
)
from life_v0.state_store.memory_trace_store import (
    apply_post_expression_reconsolidation,
    build_memory_trace_store,
    guard_offline_trace_mutations,
    project_live_dialogue_episode_traces,
)
from life_v0.state_store.pattern_separation import build_pattern_separation_index
from life_v0.state_store.relationship_memory import project_relationship_memory


class MemoryU8DeepeningTests(unittest.TestCase):
    def test_twenty_round_live_trace_accumulation(self):
        store = None
        for turn in range(20):
            store = build_memory_trace_store(
                run_id="u8-20round",
                generated_at=f"2026-06-16T00:{turn:02d}:00+00:00",
                live_turn_context={
                    "dialogue_turn_refs": [
                        f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 1}",
                        f"runtime/state/language/dialogue_turn_log.jsonl#line-{turn * 2 + 2}",
                    ],
                    "external_utterance": f"turn-{turn}",
                    "semantic_focus": f"topic_{turn % 4}",
                },
                existing_memory_trace_store=store,
            )
        live_traces = [
            trace
            for trace in store.get("traces", [])
            if trace.get("live_trace_origin") == "live_dialogue_turn"
            and trace.get("lifecycle_state") != "deprecated"
        ]
        self.assertGreaterEqual(len(live_traces), int(20 * 0.8))
        self.assertEqual(store.get("stage_policy"), "live_trace_accumulation_on_existing_store")

    def test_reconsolidation_passes_mem_cor_002_validator(self):
        store = build_memory_trace_store(
            run_id="u8-validator",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "你喜欢茶",
                "semantic_focus": "tea_preference",
            },
        )
        result = apply_post_expression_reconsolidation(
            store,
            feedback_event={
                "event_type": "correction",
                "trigger_event_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-3",
            },
            run_id="u8-validator",
            generated_at="2026-06-16T01:00:00+00:00",
            relationship_memory={},
            state_merge_guard={},
            exclude_dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        report = result["memory_reconsolidation_report"]
        self.assertTrue(report.get("mem_cor_002_satisfied"))
        self.assertIn(
            report.get("validator_result"),
            {"pass_with_guarded_partitions", "fail_with_quarantine"},
        )

    def test_multi_relation_scope_blocks_cross_person_provider_hits(self):
        trace_store = {
            "traces": [
                {
                    "trace_id": "memory-trace-person-a-tea",
                    "lifecycle_state": "active",
                    "relationship_scope": "relation_subject:person-a",
                    "relation_subject_id": "person-a",
                    "content_summary": "person a likes tea",
                    "live_trace_origin": "live_dialogue_turn",
                },
                {
                    "trace_id": "memory-trace-person-b-tea",
                    "lifecycle_state": "active",
                    "relationship_scope": "relation_subject:person-b",
                    "relation_subject_id": "person-b",
                    "content_summary": "person b likes tea",
                    "live_trace_origin": "live_dialogue_turn",
                },
            ]
        }
        merge = merge_cue_candidates(
            cue_terms=["tea"],
            memory_trace_store=trace_store,
            relationship_memory={
                "relationship_scope": "relation_subject:person-a",
                "active_relation_subject_id": "person-a",
            },
            blocked_refs=[],
            provider_name="local_full_text",
        )
        eligible = merge["eligible_candidate_trace_refs"]
        self.assertEqual(len(eligible), 1)
        self.assertIn("memory-trace-person-a-tea", eligible[0])
        self.assertNotIn("memory-trace-person-b-tea", " ".join(eligible))

    def test_pattern_separation_emits_multi_relation_routes(self):
        trace_store = build_memory_trace_store(
            run_id="u8-sep",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "hello",
                "semantic_focus": "greeting",
                "relationship_scope": "relation_subject:person-a",
                "relation_subject_id": "person-a",
            },
        )
        relationship_memory = project_relationship_memory(
            relationship_memory={},
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "person-a",
                        "relation_role": "friend",
                        "preference_hypotheses": ["tea"],
                    },
                    {
                        "relationship_id": "person-b",
                        "relation_role": "family",
                        "preference_hypotheses": ["coffee"],
                    },
                ]
            },
        )
        separation = build_pattern_separation_index(
            run_id="u8-sep",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_trace_store=trace_store,
            relationship_memory=relationship_memory,
        )
        route_kinds = [
            route.get("route_kind")
            for route in separation.get("separation_routes", [])
            if isinstance(route, dict)
        ]
        self.assertIn("multi_relation_subject_scope", route_kinds)
        self.assertGreaterEqual(separation.get("multi_relation_subject_scope_count", 0), 2)

    def test_protected_trace_offline_mutation_guard(self):
        protected_trace = {
            "trace_id": "memory-trace-protected-self",
            "lifecycle_state": "protected",
            "content_summary": "core self continuity",
            "claim_type": "self_update",
            "source_evidence_refs": ["runtime/state/self/self_model.json"],
            "contradiction_links": [],
        }
        mutated = {
            **protected_trace,
            "content_summary": "dream rewritten self",
            "lifecycle_state": "active",
        }
        guard = guard_offline_trace_mutations(
            before_traces=[protected_trace],
            after_traces=[mutated],
        )
        self.assertTrue(guard["protected_mutation_blocked"])
        self.assertEqual(guard["blocked_mutations"][0]["rule_id"], "MEM-PRO-001")

    def test_live_trace_includes_cross_modal_evidence_refs(self):
        traces = project_live_dialogue_episode_traces(
            run_id="u8-cross-modal",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "你看到了什么？",
                "semantic_focus": "shared_observation",
                "cross_modal_evidence_refs": [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/membrane/world_contact_summary.json",
                ],
            },
        )
        self.assertEqual(len(traces), 1)
        evidence = traces[0].get("source_evidence_refs", [])
        self.assertIn("runtime/state/language/language_percept_frame.json", evidence)
        self.assertIn("runtime/state/membrane/world_contact_summary.json", evidence)
        self.assertTrue(traces[0].get("cross_modal_evidence_refs"))

    def test_build_memory_retrieval_respects_active_relation_scope(self):
        frame = build_memory_retrieval_frame(
            run_id="u8-retrieval-scope",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="tea preference check",
            relationship_memory={
                "relationship_scope": "relation_subject:person-a",
                "active_relation_subject_id": "person-a",
                "shared_memory_refs": [
                    "runtime/state/memory/relationship_memory.json#person-a"
                ],
            },
            memory_trace_store={
                "traces": [
                    {
                        "trace_id": "memory-trace-person-a-tea",
                        "lifecycle_state": "active",
                        "relationship_scope": "relation_subject:person-a",
                        "relation_subject_id": "person-a",
                        "content_summary": "tea preference for person a",
                        "live_trace_origin": "live_dialogue_turn",
                    },
                    {
                        "trace_id": "memory-trace-person-b-coffee",
                        "lifecycle_state": "active",
                        "relationship_scope": "relation_subject:person-b",
                        "relation_subject_id": "person-b",
                        "content_summary": "coffee preference for person b",
                        "live_trace_origin": "live_dialogue_turn",
                    },
                ]
            },
            cue_provider_name="local_full_text",
        )
        provider_refs = frame.get("cue_provider_candidate_trace_refs") or []
        joined = " ".join(provider_refs)
        self.assertIn("person-a", joined)
        self.assertNotIn("person-b-coffee", joined)


if __name__ == "__main__":
    unittest.main()