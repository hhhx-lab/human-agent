from __future__ import annotations

import unittest

from life_v0.language.pragmatic_inference import (
    _build_pragmatic_inference_profile,
    detect_memory_feedback_from_utterance,
)
from life_v0.process_supervisor.model_expression import audit_model_expression_response
from life_v0.process_supervisor.response_surface import (
    compose_recall_bounded_spoken_response,
    recall_expression_grounded,
)


class RecallBoundedExpressionTests(unittest.TestCase):
    def test_recall_bounded_spoken_response_for_memory_question(self):
        text = compose_recall_bounded_spoken_response(
            external_utterance="你还记得我是谁吗？",
            memory_retrieval_frame={
                "activated_engram_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
                "memory_phenomenology_profile": {
                    "uncertain_boundary_active": True,
                    "closure_hint": "uncertain",
                },
            },
            expression_plan={
                "memory_grounding_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ]
            },
            relationship_memory={
                "relationship_theme_tags": ["relationship_formation"],
            },
        )
        self.assertEqual(text, "")
        self.assertTrue(
            recall_expression_grounded(
                memory_retrieval_frame={
                    "activated_engram_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ],
                    "memory_phenomenology_profile": {
                        "uncertain_boundary_active": True,
                        "closure_hint": "uncertain",
                    },
                },
                expression_plan={
                    "memory_grounding_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ]
                },
            )
        )

    def test_presence_question_does_not_emit_fixed_reply(self):
        text = compose_recall_bounded_spoken_response(
            external_utterance="Adam，你现在醒着吗？",
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
        )
        self.assertEqual(text, "")

    def test_repair_focus_decays_without_current_repair_surface(self):
        profile = _build_pragmatic_inference_profile(
            language_percept={
                "incoming_surface": "你还记得我们上次聊什么吗？",
                "utterance_signal_profile": {
                    "repair_request": False,
                    "apology": False,
                },
                "repair_trigger_candidates": ["repair-language-v0-0001"],
            },
            relationship_timeline={
                "relationship_continuity_reports": [
                    {"continuity_state": "repair_guarded_continuity"}
                ]
            },
            commitment_truth_state={"repair_required_refs": ["repair-1"]},
            context_accumulation={},
            relation_scope_index={},
            shared_term_registry={},
            relationship_stage="friend_repair_guarded",
            generated_at="2026-06-17T00:00:00Z",
        )
        self.assertEqual(profile["dominant_pragmatic_intent"], "relational_checkin")

    def test_memory_confirmation_feedback_detected(self):
        event = detect_memory_feedback_from_utterance("你说得对，就是这样。")
        self.assertEqual(event.get("event_type"), "confirmation")

    def test_positive_evidence_waives_background_flags(self):
        context = {
            "external_relation_utterance": "我们接着聊。",
            "relationship": {
                "relation_role": "friend",
                "relationship_stage": "relationship_formation",
                "continuity_state": "stable",
                "trust_state": "calibrated",
            },
            "shared_language": {"shared_terms": ["朋友"]},
            "language_plasticity": {
                "expression_tempo_mode": "guarded_deliberate",
                "promoted_shared_term_count": 1,
            },
            "self_slow_variables": {"continuity_drive": 0.7},
            "memory_retrieval": {
                "memory_retrieval_frame_ref": "runtime/state/memory/memory_retrieval_frame.json",
                "activated_engram_ref_count": 2,
                "memory_retrieval_recall_to_expression_closure_status": "closed",
            },
            "live_language": {
                "memory_grounding_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
            },
            "resident_background": {
                "autonomous_activity_presence": True,
                "identity_consciousness_birth_presence": True,
                "birth_repair_presence": True,
                "life_constraint_presence": True,
                "world_contact_handoff_presence": True,
            },
            "life_context": {},
            "body_affect": {},
            "responsibility_regret_repair": {},
            "prediction_conscious_workspace": {},
        }
        gate = audit_model_expression_response(
            model_response_text="我在。我们继续聊，我记得一些之前的事。",
            audited_expression_material="{}",
            expression_context=context,
        )
        self.assertEqual(gate["gate_status"], "accepted")
        self.assertIn("recall_expression_grounded", gate["positive_evidence_flags"])
        self.assertIn(
            "resident_autonomous_activity",
            gate["waived_required_evidence_flags"],
        )

    def test_recall_expression_grounded_helper(self):
        self.assertTrue(
            recall_expression_grounded(
                memory_retrieval_frame={
                    "activated_engram_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"]
                },
                expression_plan={
                    "memory_grounding_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ]
                },
            )
        )

    def test_non_recall_utterance_with_observed_name_stays_unreleased(self):
        text = compose_recall_bounded_spoken_response(
            external_utterance="今天天气不错。",
            relationship_memory={
                "relation_person_profile": {"observed_names": ["阿宝"]},
            },
        )
        self.assertEqual(text, "")


if __name__ == "__main__":
    unittest.main()
