import unittest


class EvidenceRankerTests(unittest.TestCase):
    def test_build_evidence_ranking_emits_density_suspicion_and_priority_budget(self):
        from life_v0.schema_runner.evidence_ranker import build_evidence_ranking, check_evidence_ranking

        ranking = build_evidence_ranking(
            run_id="evidence-test",
            generated_at="2026-06-09T00:00:00+00:00",
            observation_truth_review={
                "missing_fields": ["prediction_workspace"],
                "truth_review_required": True,
            },
            boundary_audit={"audit_findings": ["world_contact_blocked"]},
            consistency_logic={"inconsistency_findings": ["candidate_action_missing"]},
            counterfactual_trace={"counterfactual_branches": [{"branch_id": "cf-1"}]},
            comparison_trace={"suppressed_branch_refs": ["cf-2"]},
        )

        self.assertEqual(ranking["schema_version"], "evidence_ranking_v0")
        self.assertEqual(ranking["evidence_ranking_id"], "evidence-ranking-evidence-test")
        self.assertLess(ranking["evidence_density_score"], 1.0)
        self.assertTrue(ranking["ranked_evidence"])
        self.assertIn("missing:prediction_workspace", ranking["suspicious_points"])
        self.assertIn("observation_truth_review_pending", ranking["pending_confirmation_points"])
        self.assertEqual(ranking["priority_budget"]["truth_review"], "high")
        self.assertEqual(check_evidence_ranking(ranking), [])

    def test_check_evidence_ranking_requires_core_fields(self):
        from life_v0.schema_runner.evidence_ranker import check_evidence_ranking

        reasons = check_evidence_ranking({"schema_version": "evidence_ranking_v0"})

        self.assertIn("evidence_ranking_gate missing evidence_ranking_id", reasons)
        self.assertIn("evidence_ranking_gate density score missing", reasons)


if __name__ == "__main__":
    unittest.main()
