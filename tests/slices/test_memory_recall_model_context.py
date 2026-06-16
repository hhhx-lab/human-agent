import unittest

from life_v0.process_supervisor.model_expression import build_model_expression_context


class MemoryRecallModelContextTests(unittest.TestCase):
    def test_model_context_carries_memory_recall_and_restore_refs(self):
        context = build_model_expression_context(
            external_utterance="你还记得我们上次说的语言系统吗？",
            audited_expression_material="{}",
            runtime_config=type(
                "Cfg",
                (),
                {
                    "response_language": "zh-CN",
                    "dialogue_style": "equal_relation",
                },
            )(),
            semantic_map={
                "semantic_focus": "memory_grounded_relational_recall",
                "memory_recall_refs": ["engram-a", "engram-b"],
                "memory_reconstruction_focus": "relationship_memory",
            },
            expression_plan={
                "memory_grounding_refs": ["engram-a"],
                "memory_reconstruction_focus": "relationship_memory",
                "expression_tempo_mode": "steady",
                "release_caution_level": "baseline",
            },
            relationship_timeline={
                "relationship_language_events": ["timeline-event-1"],
            },
            commitment_expression_plan={
                "restore_refs": [
                    "runtime/state/language/commitment_expression_plan.json"
                ],
            },
            apology_repair_language_trace={
                "restore_refs": [
                    "runtime/state/language/apology_repair_language_trace.json"
                ],
                "future_probe_refs": ["future-probe-1"],
            },
        )
        live_language = context["live_language"]
        relationship = context["relationship"]
        plasticity = context["language_plasticity"]

        self.assertEqual(
            live_language["memory_recall_refs"],
            ["engram-a", "engram-b"],
        )
        self.assertEqual(
            live_language["memory_grounding_refs"],
            ["engram-a"],
        )
        self.assertEqual(
            live_language["memory_reconstruction_focus"],
            "relationship_memory",
        )
        self.assertEqual(
            relationship["relationship_language_events"],
            ["timeline-event-1"],
        )
        self.assertTrue(relationship["commitment_restore_refs"])
        self.assertEqual(relationship["future_probe_refs"], ["future-probe-1"])
        self.assertEqual(plasticity["expression_tempo_mode"], "steady")