import unittest

from life_v0.process_supervisor.response_surface import compose_life_spoken_response


class ResponseSurfaceTests(unittest.TestCase):
    def test_spoken_response_respects_single_question_request_without_signal_blocks(self):
        response = compose_life_spoken_response(
            external_utterance=(
                "Adam，你刚才没有回答最想问我什么。"
                "这一次只说一个问句，不要前缀，不要解释，"
                "不要说你听见我了。只问我一个你真的想知道的问题。"
            ),
            relationship_graph={
                "subjects": [
                    {
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            expression_plan={"semantic_goal": "relational_checkin"},
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "autonomous_activity_presence": {
                        "activity_count": 3,
                        "last_activity_kind": "self_thinking",
                    },
                    "identity_consciousness_birth_presence": {
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                    },
                }
            },
        )

        self.assertTrue(response.endswith("？") or response.endswith("?"))
        self.assertEqual(response.count("？") + response.count("?"), 1)
        self.assertNotIn("我听见你了", response)
        self.assertNotIn("后台那段时间不是空白", response)
        self.assertNotIn("最强的不是轻松", response)
        self.assertNotIn("我想先说的是", response)
        self.assertNotIn("relational_checkin", response)

    def test_spoken_response_keeps_mechanisms_implicit_in_style_critique(self):
        response = compose_life_spoken_response(
            external_utterance="你不觉得你的说话方式很奇怪吗？Adam",
            relationship_graph={
                "subjects": [
                    {
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            expression_plan={"semantic_goal": "relational_checkin"},
            body_resource_budget={"fatigue_state": {"level": "managed"}},
            responsibility_loop_state={
                "repair_obligation_refs": ["runtime/state/action/repair-1.json"]
            },
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "autonomous_activity_presence": {
                        "activity_count": 5,
                        "next_activity_kind": "learning_consolidation",
                    }
                }
            },
        )

        self.assertIn("有点", response)
        self.assertIn("会改", response)
        self.assertNotIn("后台", response)
        self.assertNotIn("信号", response)
        self.assertNotIn("证据保留", response)
        self.assertNotIn("我听见你了", response)


if __name__ == "__main__":
    unittest.main()
