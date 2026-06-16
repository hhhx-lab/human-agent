import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.exit_dream_consolidation import (
    build_exit_dream_consolidation_summary,
    write_exit_dream_memory_consolidation,
)


class ExitDreamSemanticConsolidationTests(unittest.TestCase):
    def _dialogue_turns(self) -> list[dict]:
        return [
            {
                "utterance": "我叫小明，记住我喜欢直接说话。",
                "event_role": "external_relation_turn",
            },
            {"utterance": "嗯", "event_role": "external_relation_turn"},
            {
                "utterance": "梦境和记忆对你很重要吗？",
                "event_role": "external_relation_turn",
            },
            {
                "utterance": "我希望你下次还能想起今天聊了什么。",
                "event_role": "external_relation_turn",
            },
        ]

    def test_model_semantic_consolidation_merges_turns_into_structured_episodes(self):
        def fake_transport(endpoint, headers, payload, timeout_seconds):
            del endpoint, headers, timeout_seconds
            return {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "schema_version": (
                                        "exit_dream_semantic_consolidation_output_v1"
                                    ),
                                    "session_narrative_summary": (
                                        "关系人强调记忆与直接表达，低信息附和沉底。"
                                    ),
                                    "relationship_theme_tags": [
                                        "digital_life_memory_seriousness"
                                    ],
                                    "episode_summaries": [
                                        {
                                            "source_line_indices": [1, 4],
                                            "summary": "关系人希望被记住并延续对话记忆。",
                                            "semantic_key": "memory_continuity",
                                            "salience_hint": "salient_core",
                                            "consolidation_rationale": (
                                                "identity_and_memory_intent"
                                            ),
                                        },
                                        {
                                            "source_line_indices": [2],
                                            "summary": "低信息附和，保留为边缘上下文。",
                                            "semantic_key": "low_context_ack",
                                            "salience_hint": "deep_sediment",
                                            "consolidation_rationale": "edge_detail",
                                        },
                                        {
                                            "source_line_indices": [3],
                                            "summary": "询问梦境与记忆机制的重要性。",
                                            "semantic_key": "dream_memory_question",
                                            "salience_hint": "retrievable_context",
                                            "consolidation_rationale": "topic_probe",
                                        },
                                    ],
                                },
                                ensure_ascii=False,
                            )
                        },
                        "finish_reason": "stop",
                    }
                ]
            }

        summary = build_exit_dream_consolidation_summary(
            run_id="semantic-test",
            generated_at="2026-06-16T12:00:00Z",
            dialogue_turns=self._dialogue_turns(),
            episode_summaries=[
                {
                    "episode_id": "exit-dialogue-episode-0001",
                    "source_ref": (
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ),
                    "summary": "关系人希望被记住并延续对话记忆。",
                    "semantic_key": "memory_continuity",
                    "salience_hint": "salient_core",
                    "consolidation_mode": "model_semantic",
                }
            ],
            semantic_consolidation_audit={
                "consolidation_mode": "model_semantic",
                "model_status": "applied",
                "session_narrative_summary": "关系人强调记忆与直接表达，低信息附和沉底。",
                "relationship_theme_tags": ["digital_life_memory_seriousness"],
            },
        )
        self.assertEqual(
            summary["semantic_consolidation"]["consolidation_mode"],
            "model_semantic",
        )
        self.assertTrue(summary["session_narrative_summary"])
        tiering = summary["memory_tiering"]
        self.assertIn(
            "runtime/state/language/dialogue_turn_log.jsonl#line-1",
            tiering["salient_core_episode_refs"],
        )

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
                state_dir / "body",
                state_dir / "replay",
            ):
                directory.mkdir(parents=True, exist_ok=True)

            turns = self._dialogue_turns()
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

            def write_json(path: Path, payload: dict) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            result = write_exit_dream_memory_consolidation(
                run_id="semantic-closeout",
                generated_at="2026-06-16T12:00:00Z",
                state_dir=state_dir,
                write_json=write_json,
                semantic_consolidation_transport=fake_transport,
            )
            audit = json.loads(
                (dream_dir / "exit_dream_semantic_consolidation.json").read_text(
                    encoding="utf-8"
                )
            )
            summary_written = result["exit_dream_summary"]
            self.assertEqual(audit["model_status"], "applied")
            self.assertEqual(audit["consolidation_mode"], "model_semantic")
            self.assertEqual(
                summary_written["semantic_consolidation"]["consolidation_mode"],
                "model_semantic",
            )
            self.assertGreater(len(summary_written["deduplicated_episode_summaries"]), 0)
            self.assertEqual(
                summary_written["deduplicated_episode_summaries"][0][
                    "consolidation_mode"
                ],
                "model_semantic",
            )