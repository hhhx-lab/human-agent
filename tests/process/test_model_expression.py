import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.model_expression import compose_model_expression


class ModelExpressionTests(unittest.TestCase):
    def test_openai_compatible_expression_uses_transport_and_redacts_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            language_dir = root / "state" / "language"
            reports_dir = root / "reports"
            captured = {}

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                captured["endpoint"] = endpoint
                captured["headers"] = dict(headers)
                captured["payload"] = payload
                captured["timeout_seconds"] = timeout_seconds
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {
                                "content": "我会带着刚形成的关系记忆回应你，而不是把这句话当成任务。"
                            },
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你现在怎么理解我们？",
                deterministic_response="确定性脚手：我记得关系阶段和修复压力。",
                language_dir=language_dir,
                reports_dir=reports_dir,
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                language_percept={
                    "speaker_role": "friend",
                    "shared_term_hits": ["知识宝座"],
                    "ambiguity_flags": ["待确认关系语义细节"],
                    "repair_trigger_candidates": ["repair-language-v0-0001"],
                    "prediction_focus": {
                        "belief_scope": "relationship",
                        "active_sampling_route": "clarify",
                    },
                },
                semantic_map={
                    "semantic_focus": "repair_relational_trace",
                    "ambiguity_queue": ["shared_term_unresolved"],
                    "shared_meaning_bindings": [{"surface": "知识宝座"}],
                    "semantic_prediction_trace": {
                        "relationship_pressure": "elevated",
                        "repair_drive": "active",
                    },
                },
                inner_speech={
                    "attention_focus": "relationship_subject_and_responsibility_trace",
                    "affective_modulation": "guarded_but_expressive",
                    "responsibility_constraint": "no_untraced_commitment",
                    "drive_resolution_order": ["hold", "repair"],
                    "internal_drive_sources": {
                        "repair": {"drive": "active"},
                        "confirm": {"drive": "low"},
                    },
                },
                expression_monitor={
                    "monitor_dimensions": ["semantic_coherence", "commitment_trace"],
                    "blocked_language": ["service_object"],
                    "write_gate_pressure": {
                        "stage_policy": "guarded_append",
                        "responsibility_event_count": 2,
                    },
                    "affect_expression_modulation": {
                        "arousal": 0.71,
                        "repair_drive": "active",
                    },
                },
                expression_plan={"semantic_goal": "relational_checkin"},
                brain_graph={
                    "region_nodes": [{"node_id": "LanguageRelationshipRuntime"}],
                    "functional_edges": [{"edge_id": "edge-language-memory"}],
                    "live_turn_focus": {
                        "relationship_stage": "repair_guarded_continuity",
                        "trait_names": ["continuity_drive"],
                    },
                },
                network_state={
                    "active_networks": [
                        {
                            "network_id": "executive_workspace_network",
                            "mode": "live_relation_focus",
                        }
                    ],
                    "switch_events": [{"event_id": "network-switch-live-1"}],
                    "workspace_priority": "language_relationship_and_memory_retrieval",
                },
                prediction_workspace={
                    "workspace_contents": {
                        "precision_state": "semantic_handoff_seeded",
                        "active_sampling_mode": "clarify_ambiguity",
                        "belief_scope": "relationship",
                        "candidate_explanations": [
                            {
                                "explanation_id": "semantic-focus-v0-0001",
                                "focus": "repair_relational_trace",
                            }
                        ],
                    }
                },
                workspace_frame={
                    "live_turn_focus": "repair_relational_trace",
                    "broadcast_targets": ["LanguageRelationshipRuntime"],
                    "candidate_explanations": [
                        {"focus": "repair_relational_trace"}
                    ],
                    "live_language_turn_refs": [
                        "runtime/state/language/semantic_map_frame.json"
                    ],
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                    "DIGITAL_LIFE_MODEL_TEMPERATURE": "0.2",
                    "DIGITAL_LIFE_MODEL_MAX_OUTPUT_TOKENS": "128",
                    "DIGITAL_LIFE_MODEL_TIMEOUT_SECONDS": "9",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertTrue(result.applied)
            self.assertIn("关系记忆", result.response_text)
            self.assertEqual(
                captured["endpoint"],
                "https://model.example/v1/chat/completions",
            )
            self.assertEqual(captured["headers"]["Authorization"], "Bearer secret-token")
            self.assertEqual(captured["payload"]["model"], "gpt-5.5")
            self.assertEqual(captured["payload"]["temperature"], 0.2)
            self.assertEqual(captured["payload"]["max_tokens"], 128)
            self.assertEqual(captured["timeout_seconds"], 9.0)
            expression_context = json.loads(
                captured["payload"]["messages"][1]["content"]
            )
            self.assertEqual(
                expression_context["live_language"]["semantic_focus"],
                "repair_relational_trace",
            )
            self.assertEqual(
                expression_context["live_language"]["inner_drive_states"]["repair"],
                "active",
            )
            self.assertEqual(
                expression_context["prediction_conscious_workspace"][
                    "prediction_active_sampling_mode"
                ],
                "clarify_ambiguity",
            )
            self.assertEqual(
                expression_context["prediction_conscious_workspace"][
                    "active_network_modes"
                ][0]["mode"],
                "live_relation_focus",
            )

            state_text = (language_dir / "model_expression_state.json").read_text(
                encoding="utf-8"
            )
            report_text = (
                reports_dir / "digital_life_model_expression_report.json"
            ).read_text(encoding="utf-8")
            self.assertNotIn("secret-token", state_text)
            self.assertNotIn("secret-token", report_text)

            state = json.loads(state_text)
            report = json.loads(report_text)
            self.assertEqual(state["model_expression_status"], "model_expression_applied")
            self.assertEqual(report["model_expression_state_ref"], result.state_ref)
            self.assertEqual(
                state["model_expression_context_summary"]["language_percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                state["model_expression_context_summary"]["prediction_workspace_ref"],
                "runtime/state/prediction/prediction_workspace_frame.json",
            )

    def test_local_provider_keeps_deterministic_expression_without_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def failing_transport(endpoint, headers, payload, timeout_seconds):
                self.fail("local provider should not call model transport")

            result = compose_model_expression(
                run_id="model-expression-local",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你好",
                deterministic_response="确定性回应仍然在场。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                environ={"DIGITAL_LIFE_MODEL_PROVIDER": "local"},
                transport=failing_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(result.response_text, "确定性回应仍然在场。")
            self.assertEqual(
                result.state["fallback_reason"],
                "provider_local_or_disabled",
            )

    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
