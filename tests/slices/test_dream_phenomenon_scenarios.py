import inspect
import json
import tempfile
import unittest
from pathlib import Path

from life_v0.dream.dream_belief_gate import build_dream_belief_gate_decision
from life_v0.dream.dream_fact_gate import build_dream_fact_gate_decision
from life_v0.dream.offline_dream_entry import build_offline_dream_entry_vector
from life_v0.dream.web_dream_browser import run_readonly_browse_session
from life_v0.dream.web_dream_discovery import (
    append_topic_history_entry,
    select_topic_candidate,
    topic_cluster_id,
)
from life_v0.dream.web_dream_learning import record_web_dream_learning
from life_v0.state_store.memory_retrieval import (
    _filter_traces_by_accessibility_tier,
    build_memory_retrieval_frame,
    merge_cue_candidates,
)
from life_v0.state_store.memory_trace_store import (
    merge_exit_dream_traces_into_store,
    project_exit_dream_episode_traces,
)
from life_v0.state_store.offline_memory_hygiene import apply_offline_memory_hygiene


class DreamPhenomenonScenarioTests(unittest.TestCase):
    def _exit_summary(self) -> dict:
        return {
            "deduplicated_episode_summaries": [
                {
                    "episode_id": "ep-core",
                    "source_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "semantic_key": "identity_name",
                    "summary": "我叫小明",
                    "event_role": "external_relation_turn",
                },
                {
                    "episode_id": "ep-sediment",
                    "source_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "semantic_key": "low_context",
                    "summary": "嗯",
                    "event_role": "external_relation_turn",
                },
            ],
            "memory_tiering": {
                "salient_core_episode_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "retrievable_context_episode_refs": [],
                "deep_sediment_episode_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2"
                ],
            },
        }

    def test_s1_exit_tiering_suppresses_sediment_for_weak_cue(self):
        traces = project_exit_dream_episode_traces(
            run_id="s1",
            generated_at="2026-06-16T12:00:00Z",
            exit_dream_summary=self._exit_summary(),
        )
        store = merge_exit_dream_traces_into_store(
            memory_trace_store={"traces": []},
            exit_dream_traces=traces,
            generated_at="2026-06-16T12:00:00Z",
        )
        frame = build_memory_retrieval_frame(
            run_id="s1",
            generated_at="2026-06-16T12:00:00Z",
            memory_trace_store=store,
            external_utterance="x",
        )
        tiered = frame["tiered_recall"]
        salient_id = next(
            trace["trace_id"]
            for trace in traces
            if trace["accessibility_tier"] == "salient_core"
        )
        sediment_id = next(
            trace["trace_id"]
            for trace in traces
            if trace["accessibility_tier"] == "deep_sediment"
        )
        salient_ref = f"runtime/state/memory/memory_trace_store.json#{salient_id}"
        sediment_ref = f"runtime/state/memory/memory_trace_store.json#{sediment_id}"
        self.assertIn(salient_ref, tiered["salient_core_refs"])
        self.assertIn(sediment_ref, tiered["deep_sediment_refs"])
        filtered = _filter_traces_by_accessibility_tier(
            [salient_ref, sediment_ref],
            memory_trace_store=store,
            cue_terms=["x"],
        )
        self.assertIn(salient_ref, filtered)
        self.assertNotIn(sediment_ref, filtered)
        merge = merge_cue_candidates(
            cue_terms=["x"],
            memory_trace_store=store,
            relationship_memory={},
            blocked_refs=[],
        )
        self.assertNotIn(sediment_ref, merge["eligible_candidate_trace_refs"])

    def test_s2_offline_hygiene_merges_duplicate_traces(self):
        traces = [
            {
                "trace_id": "trace-a",
                "event_boundary": "same-event",
                "content_summary": "hello",
                "salience_vector": {"emotional": 0.2},
                "source_evidence_refs": ["ref-1"],
                "lifecycle_state": "active",
            },
            {
                "trace_id": "trace-b",
                "event_boundary": "same-event",
                "content_summary": "hello",
                "salience_vector": {"emotional": 0.15},
                "source_evidence_refs": ["ref-2"],
                "lifecycle_state": "active",
            },
        ]
        report, updated = apply_offline_memory_hygiene(
            memory_trace_store={"traces": traces},
            generated_at="2026-06-16T12:00:00Z",
            trigger_mode="sleep",
        )
        active = [
            trace
            for trace in updated["traces"]
            if trace.get("lifecycle_state") not in {"merged_into", "deprecated"}
        ]
        self.assertEqual(len(active), 1)
        self.assertTrue(report.get("hygiene_actions"))

    def test_s3_protected_relationship_trace_survives_hygiene(self):
        traces = [
            {
                "trace_id": "rel-a",
                "memory_kind": "relationship",
                "event_boundary": "rel-event",
                "content_summary": "friend",
                "salience_vector": {"relationship": 0.9},
                "source_evidence_refs": ["rel-ref-1"],
                "lifecycle_state": "active",
            },
            {
                "trace_id": "rel-b",
                "memory_kind": "relationship",
                "event_boundary": "rel-event",
                "content_summary": "friend",
                "salience_vector": {"relationship": 0.85},
                "source_evidence_refs": ["rel-ref-2"],
                "lifecycle_state": "active",
            },
        ]
        report, updated = apply_offline_memory_hygiene(
            memory_trace_store={"traces": traces},
            generated_at="2026-06-16T12:00:00Z",
            trigger_mode="sleep",
        )
        protected = report["protected_trace_decisions"]
        self.assertTrue(any(item["decision"] == "preserve" for item in protected))
        active = [
            trace
            for trace in updated["traces"]
            if trace.get("lifecycle_state") not in {"merged_into", "deprecated"}
        ]
        self.assertEqual(len(active), 2)

    def test_s4_relation_curated_seed_records_browser_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            dream_dir = state_dir / "dream"
            dream_dir.mkdir(parents=True)

            def fake_fetch(url: str, timeout_seconds: float) -> dict:
                return {
                    "status_code": 200,
                    "final_url": url,
                    "content_type": "text/html",
                    "text": (
                        "<html><head><title>Curated seed page</title></head>"
                        "<body><h1>Relation curated topic</h1>"
                        "<p>Learning residue for next wake.</p></body></html>"
                    ),
                    "browser_policy": "read_only_no_side_effect",
                    "action_inhibition_seal": "closed",
                }

            (dream_dir / "web_dream_learning_seeds.json").write_text(
                json.dumps(
                    {
                        "enabled": True,
                        "seed_urls": ["https://relation-seed.test/curated"],
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            result = record_web_dream_learning(
                state_dir=state_dir,
                generated_at="2026-06-16T12:00:00Z",
                fetch_url=fake_fetch,
            )
            web_state = result["state"]
            browser_session = json.loads(
                (dream_dir / "web_dream_browser_session.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(web_state["status"], "learned")
            self.assertGreater(browser_session.get("page_count", 0), 0)
            self.assertGreater(len(web_state.get("topic_candidates", [])), 0)
            self.assertTrue(web_state.get("structured_wake_question_candidates"))

    def test_s5_autonomous_discovery_yields_five_distinct_clusters(self):
        history = {"entries": []}
        clusters: list[str] = []
        for index in range(5):
            cluster = topic_cluster_id(
                title=f"Topic {index}",
                headings=[f"Heading {index}"],
                text_sample=f"sample {index}",
                domain=f"discover-{index}.org",
            )
            selection = select_topic_candidate(
                candidates=[
                    {
                        "topic_cluster_id": cluster,
                        "url_digest": f"digest-{index}",
                        "selection_score": 0.8,
                    }
                ],
                topic_history=history,
            )
            selected = selection["selected"]
            self.assertIsNotNone(selected)
            clusters.append(str(selected["topic_cluster_id"]))
            history = append_topic_history_entry(
                topic_history=history,
                session_id=f"session-{index}",
                topic_cluster_id_value=cluster,
                url_digest_value=f"digest-{index}",
                generated_at="2026-06-16T12:00:00Z",
                discovery_mode="autonomous",
            )
        self.assertEqual(len(set(clusters)), 5)

    def test_s6_wake_candidates_are_structured_without_fixed_literal_text(self):
        import life_v0.dream.web_dream_learning as web_dream_learning

        source = inspect.getsource(web_dream_learning)
        self.assertNotIn("TOPIC_LIST", source)
        self.assertNotIn("FIXED_WAKE_QUESTION", source)
        frame = build_memory_retrieval_frame(
            run_id="s6",
            generated_at="2026-06-16T12:00:00Z",
            web_dream_learning_state={
                "structured_wake_question_candidates": [
                    {
                        "candidate_id": "wake-q-test",
                        "topic_cluster_id": "cluster-test",
                        "expression_policy": "model_generated_only_no_fixed_sentence",
                        "literal_text": "should_be_stripped",
                    }
                ]
            },
        )
        chain = frame["memory_expression_material_chain"]
        candidates = chain["structured_wake_question_candidates"]
        self.assertEqual(len(candidates), 1)
        self.assertIsNone(candidates[0]["literal_text"])

    def test_s7_fact_gate_blocks_direct_fact_memory(self):
        decision = build_dream_fact_gate_decision(
            run_id="s7",
            generated_at="2026-06-16T12:00:00Z",
            dream_window={
                "source_trace_refs": ["runtime/state/dream/web_dream_learning_state.json"],
                "dream_scene_frames": [{"scene_id": "dream-scene-s7"}],
            },
            wake_integration={},
            offline_entry={},
        )
        self.assertIn("direct_fact_memory", decision["blocked_writes"])
        self.assertIn("relationship_state_overwrite", decision["blocked_writes"])
        self.assertEqual(decision["gate_result"], "passed")

    def test_s8_belief_gate_allows_candidates_only(self):
        decision = build_dream_belief_gate_decision(
            run_id="s8",
            generated_at="2026-06-16T12:00:00Z",
            dream_window={
                "dream_scene_frames": [{"scene_id": "dream-scene-s8"}],
            },
            wake_integration={},
        )
        self.assertIn(
            "long_term_belief_overwrite_without_wake_evidence",
            decision["blocked_writes"],
        )
        self.assertIn("BeliefLearningCandidate", decision["allowed_writes"])
        self.assertEqual(
            decision["dream_belief_boundary"],
            "belief_changes_require_multi_cycle_wake_evidence",
        )

    def test_s9_browser_session_seals_external_actions(self):
        def fake_fetch(url: str, timeout_seconds: float) -> dict:
            return {
                "status_code": 200,
                "final_url": url,
                "content_type": "text/html",
                "text": (
                    "<html><body>"
                    "<form action='/submit'><button>Submit</button></form>"
                    "<a href='https://example.test/next'>next</a>"
                    "</body></html>"
                ),
                "browser_policy": "read_only_no_side_effect",
                "action_inhibition_seal": "closed",
                "outbound_links": ["https://example.test/next"],
            }

        session = run_readonly_browse_session(
            start_url="https://example.test/start",
            generated_at="2026-06-16T12:00:00Z",
            session_id="s9-session",
            fetch_page=fake_fetch,
        )
        self.assertFalse(session.get("allow_click"))
        self.assertFalse(session.get("allow_form_fill"))
        self.assertFalse(session.get("allow_download"))
        self.assertEqual(session.get("action_inhibition_seal"), "closed")
        self.assertEqual(session.get("external_action_policy"), "read_only_no_side_effect")

    def test_s10_offline_entry_modes_differ_by_pressure_profile(self):
        high_pressure = build_offline_dream_entry_vector(
            run_id="s10-high",
            generated_at="2026-06-16T12:00:00Z",
            need_state_vector={"sleep_pressure": 0.7},
            memory_trace_store={
                "traces": [
                    {"lifecycle_state": "active"},
                    {"lifecycle_state": "candidate"},
                    {"lifecycle_state": "encoding"},
                ]
            },
            exit_dream_summary={"source_dialogue_turn_count": 12},
        )
        low_pressure = build_offline_dream_entry_vector(
            run_id="s10-low",
            generated_at="2026-06-16T12:00:00Z",
            need_state_vector={"sleep_pressure": 0.05},
            memory_trace_store={"traces": []},
        )
        self.assertIn("NREMReplayCycle", high_pressure["selected_offline_modes"])
        self.assertNotEqual(
            high_pressure["selected_offline_modes"],
            low_pressure["selected_offline_modes"],
        )
        self.assertTrue(high_pressure.get("entry_reason_refs"))