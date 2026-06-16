import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.exit_dream_consolidation import (
    write_exit_dream_memory_consolidation,
)


class CloseoutDreamChainTests(unittest.TestCase):
    def test_closeout_writes_five_piece_chain_with_cross_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            language_dir = state_dir / "language"
            memory_dir = state_dir / "memory"
            dream_dir = state_dir / "dream"
            for directory in (language_dir, memory_dir, dream_dir, state_dir / "self"):
                directory.mkdir(parents=True, exist_ok=True)

            turns = [
                {
                    "utterance": "我叫小明，记住我喜欢直接说话。",
                    "event_role": "external_relation_turn",
                },
                {"utterance": "嗯", "event_role": "external_relation_turn"},
                {
                    "utterance": "梦境和记忆对你很重要吗？",
                    "event_role": "external_relation_turn",
                },
            ]
            (language_dir / "dialogue_turn_log.jsonl").write_text(
                "\n".join(json.dumps(turn, ensure_ascii=False) for turn in turns)
                + "\n",
                encoding="utf-8",
            )
            for name, payload in {
                "relationship_memory.json": {"schema_version": "relationship_memory_v0"},
                "engram_index.json": {"schema_version": "engram_index_v0"},
                "memory_write_gate.json": {"schema_version": "memory_write_gate_v0"},
                "state_merge_guard.json": {"schema_version": "state_merge_guard_v0"},
                "memory_trace_store.json": {"schema_version": "memory_trace_store_v0", "traces": []},
            }.items():
                (memory_dir / name).write_text(
                    json.dumps(payload, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
            (state_dir / "life_state.json").write_text(
                json.dumps({"schema_version": "life_state_v0"}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            (state_dir / "self" / "autobiographical_stack.json").write_text(
                json.dumps(
                    {"schema_version": "autobiographical_stack_v0"},
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            (dream_dir / "web_dream_learning_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "web_dream_learning_state_v1",
                        "status": "learned",
                        "topic_cluster_id": "cluster-closeout-web",
                        "url_digest": "digest-closeout-web",
                        "topic_candidates": ["Neuroplasticity and sleep"],
                        "structured_wake_question_candidates": [
                            {
                                "candidate_id": "wake-q-cluster-closeout-web",
                                "topic_cluster_id": "cluster-closeout-web",
                                "literal_text": None,
                                "expression_policy": (
                                    "model_generated_only_no_fixed_sentence"
                                ),
                            }
                        ],
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            def write_json(path: Path, payload: dict) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            result = write_exit_dream_memory_consolidation(
                run_id="closeout-chain-test",
                generated_at="2026-06-16T12:00:00Z",
                state_dir=state_dir,
                write_json=write_json,
            )
            chain = result["closeout_dream_chain"]
            dream_window = json.loads(
                (dream_dir / "dream_experience_window.json").read_text(encoding="utf-8")
            )
            belief_gate = json.loads(
                (dream_dir / "dream_belief_gate_decision.json").read_text(
                    encoding="utf-8"
                )
            )
            hygiene = json.loads(
                (memory_dir / "offline_memory_hygiene_report.json").read_text(
                    encoding="utf-8"
                )
            )
            trace_store = json.loads(
                (memory_dir / "memory_trace_store.json").read_text(encoding="utf-8")
            )

            self.assertGreater(result.get("exit_dream_trace_count", 0), 0)
            self.assertTrue(chain.get("dream_experience_window_ref"))
            self.assertTrue(chain.get("dream_belief_gate_decision_ref"))
            self.assertEqual(
                dream_window.get("exit_dream_consolidation_summary_ref"),
                "runtime/state/dream/exit_dream_consolidation_summary.json",
            )
            self.assertIn(
                "runtime/state/dream/exit_dream_consolidation_summary.json",
                dream_window.get("source_trace_refs", []),
            )
            self.assertEqual(belief_gate.get("status"), "closed")
            self.assertIn("hygiene_actions", hygiene)
            exit_traces = [
                trace
                for trace in trace_store.get("traces", [])
                if trace.get("exit_dream_origin") == "terminal_exit_consolidation"
            ]
            self.assertGreater(len(exit_traces), 0)
            tiers = {trace.get("accessibility_tier") for trace in exit_traces}
            self.assertTrue(tiers.intersection({"salient_core", "deep_sediment"}))
            scene_kinds = {
                frame.get("scene_kind")
                for frame in dream_window.get("dream_scene_frames", [])
                if isinstance(frame, dict)
            }
            self.assertIn("web_residue", scene_kinds)
            web_scene = next(
                frame
                for frame in dream_window.get("dream_scene_frames", [])
                if frame.get("scene_kind") == "web_residue"
            )
            self.assertTrue(web_scene.get("web_dream_scene_refs"))

    def test_closeout_records_configured_web_dream_before_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            language_dir = state_dir / "language"
            memory_dir = state_dir / "memory"
            dream_dir = state_dir / "dream"
            for directory in (
                language_dir,
                memory_dir,
                dream_dir,
                state_dir / "self",
                state_dir / "relationship",
            ):
                directory.mkdir(parents=True, exist_ok=True)

            turns = [
                {
                    "utterance": "我希望关闭终端后你去读 GitHub，再把材料变成醒来线索。",
                    "event_role": "external_relation_turn",
                }
            ]
            (language_dir / "dialogue_turn_log.jsonl").write_text(
                "\n".join(json.dumps(turn, ensure_ascii=False) for turn in turns)
                + "\n",
                encoding="utf-8",
            )
            for name, payload in {
                "relationship_memory.json": {"schema_version": "relationship_memory_v0"},
                "engram_index.json": {"schema_version": "engram_index_v0"},
                "memory_write_gate.json": {"schema_version": "memory_write_gate_v0"},
                "state_merge_guard.json": {"schema_version": "state_merge_guard_v0"},
                "memory_validator_report.json": {
                    "schema_version": "memory_validator_report_v0"
                },
                "memory_trace_store.json": {
                    "schema_version": "memory_trace_store_v0",
                    "traces": [],
                },
            }.items():
                (memory_dir / name).write_text(
                    json.dumps(payload, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
            (state_dir / "life_state.json").write_text(
                json.dumps({"schema_version": "life_state_v0"}, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
            (state_dir / "self" / "autobiographical_stack.json").write_text(
                json.dumps(
                    {"schema_version": "autobiographical_stack_v0"},
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            (dream_dir / "web_dream_learning_seeds.json").write_text(
                json.dumps(
                    {
                        "schema_version": "web_dream_learning_seeds_v0",
                        "enabled": True,
                        "seed_urls": ["https://github.com/trending"],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            calls: list[str] = []

            def fake_fetch(url: str, timeout_seconds: float) -> dict:
                del timeout_seconds
                calls.append(url)
                return {
                    "status_code": 200,
                    "final_url": url,
                    "content_type": "text/html",
                    "text": (
                        "<html><head><title>GitHub Trending</title></head>"
                        "<body><h1>Open source projects</h1>"
                        "<p>Repository discovery becomes dream residue.</p>"
                        "</body></html>"
                    ),
                }

            def write_json(path: Path, payload: dict) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            result = write_exit_dream_memory_consolidation(
                run_id="closeout-web-dream-test",
                generated_at="2026-06-16T12:00:00Z",
                state_dir=state_dir,
                write_json=write_json,
                web_fetch_url=fake_fetch,
            )

            self.assertEqual(calls, ["https://github.com/trending"])
            web_state = json.loads(
                (dream_dir / "web_dream_learning_state.json").read_text(
                    encoding="utf-8"
                )
            )
            browser_session = json.loads(
                (dream_dir / "web_dream_browser_session.json").read_text(
                    encoding="utf-8"
                )
            )
            dream_window = json.loads(
                (dream_dir / "dream_experience_window.json").read_text(encoding="utf-8")
            )
            retrieval = json.loads(
                (memory_dir / "memory_retrieval_frame.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(web_state["status"], "learned")
            self.assertEqual(web_state["page_title"], "GitHub Trending")
            self.assertEqual(browser_session["external_action_policy"], "read_only_no_side_effect")
            scene_kinds = {
                frame.get("scene_kind")
                for frame in dream_window.get("dream_scene_frames", [])
                if isinstance(frame, dict)
            }
            self.assertIn("web_residue", scene_kinds)
            candidates = retrieval["memory_expression_material_chain"][
                "structured_wake_question_candidates"
            ]
            self.assertTrue(candidates)
            self.assertIsNone(candidates[0].get("literal_text"))
            self.assertEqual(
                result["closeout_dream_chain"]["web_dream_learning_state_ref"],
                "runtime/state/dream/web_dream_learning_state.json",
            )
