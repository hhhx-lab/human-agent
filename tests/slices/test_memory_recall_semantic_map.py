import unittest

from life_v0.language.memory_recall_enrichment import (
    enrich_semantic_map_with_memory_recall,
    project_expression_plan_with_memory_grounding,
)


class MemoryRecallSemanticMapTests(unittest.TestCase):
    def test_enriches_semantic_map_with_activated_engrams(self):
        semantic_map = {
            "schema_version": "semantic_map_frame_v0",
            "semantic_focus": "relational_checkin",
            "prediction_hooks": {},
        }
        memory_retrieval_frame = {
            "activated_engram_refs": ["engram-a", "engram-b"],
            "cue_terms": ["语言系统"],
            "recall_to_expression_profile": {
                "expression_influence_families": ["relationship_memory"],
            },
        }
        result = enrich_semantic_map_with_memory_recall(
            semantic_map=semantic_map,
            memory_retrieval_frame=memory_retrieval_frame,
            generated_at="2026-06-16T01:00:00+00:00",
        )
        self.assertEqual(result["memory_recall_refs"], ["engram-a", "engram-b"])
        self.assertEqual(result["semantic_focus"], "memory_grounded_relational_recall")
        self.assertTrue(result["prediction_hooks"]["memory_recall_refs"])

    def test_projects_expression_plan_memory_grounding(self):
        expression_plan = {
            "schema_version": "expression_plan_v0",
            "semantic_goal": "relational_checkin",
            "expression_risk_flags": [],
        }
        enriched_semantic_map = {
            "semantic_focus": "memory_grounded_relational_recall",
            "memory_recall_refs": ["engram-a"],
            "memory_reconstruction_focus": "relationship_memory",
        }
        result = project_expression_plan_with_memory_grounding(
            expression_plan=expression_plan,
            memory_retrieval_frame={"activated_engram_refs": ["engram-a"]},
            enriched_semantic_map=enriched_semantic_map,
            generated_at="2026-06-16T01:00:00+00:00",
        )
        self.assertEqual(result["memory_grounding_refs"], ["engram-a"])
        self.assertEqual(
            result["semantic_goal"], "memory_grounded_relational_recall"
        )
        self.assertIn("memory_grounding_present", result["expression_risk_flags"])