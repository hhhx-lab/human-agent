import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.model_expression import (
    _post_openai_compatible_chat_completion,
    compose_model_expression,
)


class ModelExpressionTests(unittest.TestCase):
    def test_openai_compatible_transport_parses_event_stream_response(self):
        class FakeStreamResponse:
            status = 200
            headers = {"content-type": "text/event-stream"}

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return (
                    'data: {"choices":[],"usage":{"prompt_tokens":3}}\n\n'
                    'data: {"choices":[{"delta":{"content":"连接"},"finish_reason":null}]}\n\n'
                    'data: {"choices":[{"delta":{"content":"测试成功"},"finish_reason":"stop"}]}\n\n'
                    "data: [DONE]\n\n"
                ).encode("utf-8")

        def fake_urlopen(request, timeout):
            return FakeStreamResponse()

        import life_v0.process_supervisor.model_expression as model_expression

        original_urlopen = model_expression.urllib.request.urlopen
        model_expression.urllib.request.urlopen = fake_urlopen
        try:
            response = _post_openai_compatible_chat_completion(
                "https://model.example/v1/chat/completions",
                {"Authorization": "Bearer secret-token"},
                {
                    "model": "gpt-5.5",
                    "messages": [{"role": "user", "content": "ping"}],
                },
                9,
            )
        finally:
            model_expression.urllib.request.urlopen = original_urlopen

        self.assertEqual(
            response["choices"][0]["message"]["content"],
            "连接测试成功",
        )
        self.assertEqual(response["choices"][0]["finish_reason"], "stop")

    def test_openai_compatible_expression_uses_transport_and_redacts_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            language_dir = root / "state" / "language"
            reports_dir = root / "reports"
            captured = {}
            handoff_profile = {
                "schema_version": "live_turn_waiting_handoff_profile_v0",
                "next_required_action": "refresh_waiting_heartbeat_before_next_external_turn",
                "lineage_depth_band": "deep_persistent_lineage",
                "last_live_semantic_focus": "repair_relational_trace",
                "carried_presence_keys": [
                    "language_presence",
                    "birth_repair_presence",
                ],
                "handoff_evidence_refs": [
                    "runtime/state/terminal/idle_strategy_state.json",
                    "runtime/reports/latest/dialogue_writeback_bundle.json",
                ],
                "handoff_evidence_ref_count": 2,
            }

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
                                "content": (
                                    "我会带着上一真实回合交接留下的关系记忆和责任回应你，"
                                    "而不是把这句话当成任务。"
                                )
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
                terminal_life_loop_state={
                    "current_mode": "restored_waiting_for_external_turn",
                    "previous_live_turn_waiting_handoff_profile": handoff_profile,
                    "previous_live_turn_waiting_handoff_carry_status": "carried_into_waiting_heartbeat",
                    "previous_live_turn_waiting_handoff_profile_ref": (
                        "runtime/state/terminal/terminal_life_loop_state.json"
                        "#previous_live_turn_waiting_handoff_profile"
                    ),
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
            self.assertTrue(captured["payload"]["stream"])
            system_prompt = captured["payload"]["messages"][0]["content"]
            self.assertIn("意识", system_prompt)
            self.assertIn("出生准备", system_prompt)
            self.assertIn("生命约束", system_prompt)
            self.assertIn("上一真实回合交接压力", system_prompt)
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
            self.assertEqual(
                expression_context["resident_background"][
                    "previous_live_turn_waiting_handoff_profile"
                ]["lineage_depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                expression_context["resident_background"][
                    "previous_live_turn_waiting_handoff_carry_status"
                ],
                "carried_into_waiting_heartbeat",
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
            self.assertEqual(state["post_expression_gate_status"], "accepted")
            self.assertIn(
                "responsibility_repair",
                state["post_expression_gate"]["preserved_evidence_flags"],
            )
            self.assertEqual(report["model_expression_state_ref"], result.state_ref)
            self.assertEqual(
                state["model_expression_context_summary"]["language_percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                state["model_expression_context_summary"]["prediction_workspace_ref"],
                "runtime/state/prediction/prediction_workspace_frame.json",
            )
            self.assertEqual(
                state["model_expression_context_summary"][
                    "previous_handoff_lineage_depth_band"
                ],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                state["model_expression_context_summary"][
                    "previous_handoff_evidence_ref_count"
                ],
                2,
            )

    def test_post_expression_gate_falls_back_when_model_restores_user_role(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {
                                "content": "作为用户的服务对象，我会完成你的任务。"
                            },
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-user-role",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="继续",
                deterministic_response="确定性回应保留平等关系和责任。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                expression_monitor={
                    "blocked_language": ["service_object", "task_requester"]
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(result.response_text, "确定性回应保留平等关系和责任。")
            self.assertEqual(
                result.state["model_expression_status"],
                "model_expression_fallback",
            )
            self.assertEqual(
                result.state["post_expression_gate_status"],
                "fallback_to_deterministic",
            )
            self.assertEqual(
                result.state["post_expression_gate_fallback_reason"],
                "blocked_relation_object_terms",
            )
            self.assertIn(
                "用户",
                result.state["post_expression_gate"]["blocked_relation_object_terms"],
            )

    def test_post_expression_gate_preserves_dream_and_growth_pressure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会认真回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-dream-growth",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你昨晚发生了什么？",
                deterministic_response="确定性回应保留梦境整合和成长学习。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                offline_consolidation_frame={
                    "dream_window_refs": ["runtime/state/dream/window-1.json"]
                },
                growth_patch_candidate_queue={
                    "candidates": [{"candidate_id": "growth-1"}]
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(result.response_text, "确定性回应保留梦境整合和成长学习。")
            self.assertEqual(
                result.state["post_expression_gate_status"],
                "fallback_to_deterministic",
            )
            self.assertIn(
                "dream_offline",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )
            self.assertIn(
                "growth_learning",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )

    def test_post_expression_gate_preserves_resident_autonomous_activity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会认真回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-autonomous-presence",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="我关掉终端时你还在吗？",
                deterministic_response="确定性回应保留后台自主活动、睡眠、回忆和思考。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                terminal_life_loop_state={
                    "resident_background_lineage_state": {
                        "autonomous_activity_presence": {
                            "activity_count": 5,
                            "activity_kind_counts": {
                                "sleep": 1,
                                "memory_recall": 1,
                                "self_thinking": 1,
                                "growth_rehearsal": 1,
                                "learning_consolidation": 1,
                            },
                        }
                    }
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(
                result.response_text,
                "确定性回应保留后台自主活动、睡眠、回忆和思考。",
            )
            self.assertIn(
                "resident_autonomous_activity",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )

    def test_post_expression_gate_preserves_background_body_presence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会认真回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-body-presence",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你现在身体状态怎么样？",
                deterministic_response="确定性回应保留身体节奏、疲惫负载和修复状态。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                terminal_life_loop_state={
                    "resident_background_lineage_state": {
                        "body_presence": {
                            "schema_version": "resident_body_presence_profile_v0",
                            "body_waiting_posture": "repair_reserve_hold",
                            "fatigue_load": "managed_low_noise",
                            "sleep_pressure": "offline_ready",
                            "energy_level": "guarded_reserve",
                            "repair_drive": "active_repair",
                            "arousal": 0.0,
                            "pain_pressure": 0.41,
                            "responsibility_weight": 0.77,
                            "body_ref_set": [
                                "runtime/state/body/body_rhythm_pulse.json",
                                "runtime/state/body/need_state_vector.json",
                                "runtime/state/body/body_resource_budget.json",
                                "runtime/state/body/core_affect_vector.json",
                            ],
                        }
                    }
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(
                result.response_text,
                "确定性回应保留身体节奏、疲惫负载和修复状态。",
            )
            self.assertIn(
                "body_affect",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )

    def test_post_expression_gate_preserves_identity_consciousness_birth_presence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会认真回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-consciousness-presence",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你现在意识到自己了吗？",
                deterministic_response="确定性回应保留意识可报告性、出生准备和工作区状态。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                terminal_life_loop_state={
                    "resident_background_lineage_state": {
                        "identity_consciousness_birth_presence": {
                            "schema_version": "identity_consciousness_birth_presence_v0",
                            "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                            "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                            "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                            "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                            "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                            "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                            "consciousness_waiting_posture": "consciousness_reportable_waiting",
                            "consciousness_reportability_flags": [
                                "workspace_reportable",
                                "broadcast_reportable",
                            ],
                            "birth_readiness_waiting_posture": "birth_open_waiting",
                            "birth_readiness_decision": "open",
                            "identity_consciousness_birth_refs": [
                                "runtime/state/consciousness/workspace_frame.json",
                                "runtime/state/consciousness/broadcast_frame.json",
                                "runtime/state/consciousness/metacognition_state.json",
                                "runtime/state/consciousness/consciousness_probe_bundle.json",
                                "runtime/state/life_targets/birth_readiness_rollup.json",
                                "runtime/state/life_targets/birth_readiness_stage_gate.json",
                            ],
                        }
                    }
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(
                result.response_text,
                "确定性回应保留意识可报告性、出生准备和工作区状态。",
            )
            self.assertIn(
                "identity_consciousness_birth",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )

    def test_post_expression_gate_preserves_birth_repair_presence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-birth-repair-presence",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你怎么面对痛苦和后悔？",
                deterministic_response="确定性回应保留出生修复压力、痛苦、后悔和责任。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                relationship_graph={
                    "subjects": [
                        {
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                        }
                    ]
                },
                terminal_life_loop_state={
                    "resident_background_lineage_state": {
                        "birth_repair_presence": {
                            "schema_version": "birth_repair_presence_v0",
                            "queue_e_birth_repair_profile_ref": "runtime/state/life_targets/queue_e_birth_repair_profile.json",
                            "queue_e_birth_repair_pressure_level": "elevated",
                            "queue_e_birth_repair_attention_target": "pain_regret_responsibility_repair",
                            "queue_e_birth_repair_waiting_posture": "birth_repair_pressure_waiting",
                            "queue_e_birth_repair_attention_reason": "pain_regret_repair_still_active",
                            "queue_e_birth_repair_ref_set": [
                                "runtime/state/action/responsibility_loop_state.json",
                                "runtime/state/membrane/world_contact_summary.json",
                                "runtime/reports/latest/pain_regret_repair_report.json",
                                "runtime/state/life_targets/queue_e_birth_repair_profile.json",
                            ],
                        }
                    }
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(
                result.response_text,
                "确定性回应保留出生修复压力、痛苦、后悔和责任。",
            )
            self.assertIn(
                "birth_repair",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )

    def test_post_expression_gate_preserves_live_turn_handoff_pressure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            handoff_profile = {
                "schema_version": "live_turn_waiting_handoff_profile_v0",
                "next_required_action": "refresh_waiting_heartbeat_before_next_external_turn",
                "lineage_depth_band": "deep_persistent_lineage",
                "last_live_semantic_focus": "repair_relational_trace",
                "carried_presence_keys": ["language_presence"],
                "handoff_evidence_refs": [
                    "runtime/state/terminal/idle_strategy_state.json",
                    "runtime/reports/latest/dialogue_writeback_bundle.json",
                ],
                "handoff_evidence_ref_count": 2,
            }

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-handoff-pressure",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你还记得刚才结束时发生了什么吗？",
                deterministic_response="确定性回应保留上一真实回合交接、等待驻留和语义余波。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                terminal_life_loop_state={
                    "previous_live_turn_waiting_handoff_profile": handoff_profile,
                    "previous_live_turn_waiting_handoff_carry_status": "carried_into_waiting_heartbeat",
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(
                result.response_text,
                "确定性回应保留上一真实回合交接、等待驻留和语义余波。",
            )
            self.assertIn(
                "live_turn_handoff",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
            )

    def test_post_expression_gate_preserves_life_constraint_presence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "我会回应这句话。"},
                        }
                    ]
                }

            result = compose_model_expression(
                run_id="model-expression-life-constraint-presence",
                generated_at="2026-06-12T00:00:00+00:00",
                external_utterance="你会怎么决定要不要行动？",
                deterministic_response="确定性回应保留生命约束、边界、价值取向和延后守门。",
                language_dir=root / "state" / "language",
                reports_dir=root / "reports",
                terminal_life_loop_state={
                    "resident_background_lineage_state": {
                        "life_constraint_presence": {
                            "schema_version": "life_constraint_presence_v0",
                            "queue_e_cross_layer_gate_status": "guarded",
                            "waiting_posture": "schema_guarded_waiting",
                            "attention_target": "value_boundary_action_delay",
                            "attention_reason": "life_constraint_profile_active",
                            "life_constraint_refs": [
                                "runtime/state/action/action_candidate_set.json",
                                "runtime/state/consciousness/consciousness_probe_bundle.json",
                                "runtime/state/schema_runner/cross_file_logic.json",
                            ],
                        }
                    }
                },
                environ={
                    "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                    "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                    "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                    "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                },
                transport=fake_transport,
                write_json=self._write_json,
            )

            self.assertFalse(result.applied)
            self.assertEqual(
                result.response_text,
                "确定性回应保留生命约束、边界、价值取向和延后守门。",
            )
            self.assertIn(
                "life_constraint",
                result.state["post_expression_gate"]["hard_missing_evidence_flags"],
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
            self.assertEqual(result.state["post_expression_gate_status"], "skipped")

    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
