import unittest


class BodyTraitDriftTests(unittest.TestCase):
    def test_trait_drift_monitor_observes_background_history_update_modes(self):
        from life_v0.body.trait_drift import build_trait_drift_monitor_from_self_model

        monitor = build_trait_drift_monitor_from_self_model(
            run_id="trait-history-monitor",
            generated_at="2026-06-10T00:00:00+00:00",
            self_model_state={
                "growth_window_refs": [
                    "runtime/state/terminal/background_convergence_history.json"
                ],
                "trait_slow_variables": {
                    "continuity_drive": {
                        "value": 0.78,
                        "trend": "rising",
                        "update_count": 3,
                        "last_relationship_stage": "background_continuity_waiting",
                        "slow_variable_update_mode": "background_history_recalibration",
                        "background_trait_convergence_history_focus": "trait_recalibration_required",
                        "background_trait_convergence_history_role": "unstable",
                        "background_trait_convergence_history_latest_band": "recalibrating",
                        "background_trait_convergence_history_trend_state": "recent_trait_recalibration",
                        "evidence_refs": [
                            "runtime/state/terminal/background_convergence_history.json",
                            "runtime/state/body/trait_drift_monitor.json",
                        ],
                    },
                    "repair_seriousness": {
                        "value": 0.82,
                        "trend": "steady",
                        "update_count": 2,
                        "last_relationship_stage": "background_continuity_waiting",
                        "slow_variable_update_mode": "background_history_stabilized",
                        "background_trait_convergence_history_focus": "trait_recalibration_required",
                        "background_trait_convergence_history_role": "stable",
                        "background_trait_convergence_history_latest_band": "stabilized",
                        "background_trait_convergence_history_trend_state": "stable_trait_convergence",
                        "evidence_refs": [
                            "runtime/state/terminal/background_convergence_summary.json"
                        ],
                    },
                },
            },
            relationship_graph={
                "subjects": [
                    {
                        "relationship_stage": "background_continuity_waiting",
                        "relationship_stage_evidence_refs": [
                            "runtime/state/terminal/resident_governance_state.json"
                        ],
                    }
                ]
            },
            trigger_ref="runtime/state/terminal/resident_governance_state.json#bootstrap_continuity_refresh",
        )

        slow_variables = monitor["slow_variable_summary"]
        self.assertEqual(
            slow_variables["continuity_drive"]["slow_variable_update_mode"],
            "background_history_recalibration",
        )
        self.assertEqual(
            slow_variables["continuity_drive"][
                "background_trait_convergence_history_role"
            ],
            "unstable",
        )
        self.assertEqual(
            slow_variables["repair_seriousness"]["slow_variable_update_mode"],
            "background_history_stabilized",
        )
        self.assertEqual(
            monitor["slow_variable_update_mode_summary"][
                "background_history_recalibration"
            ],
            ["continuity_drive"],
        )
        self.assertEqual(
            monitor["slow_variable_update_mode_summary"][
                "background_history_stabilized"
            ],
            ["repair_seriousness"],
        )
        self.assertEqual(
            monitor["background_history_recalibration_names"],
            ["continuity_drive"],
        )
        self.assertEqual(
            monitor["background_history_stabilized_names"],
            ["repair_seriousness"],
        )
        self.assertEqual(
            monitor["drift_direction"],
            "background_history_recalibration_needed",
        )
        self.assertIn(
            "runtime/state/terminal/background_convergence_history.json",
            monitor["drift_observation_refs"],
        )

    def test_trait_drift_monitor_observes_growth_self_modification_slow_variable_evidence(self):
        from life_v0.body.trait_drift import build_trait_drift_monitor_from_self_model

        growth_refs = [
            "runtime/state/growth/self_read_report.json",
            "runtime/state/growth/plasticity_window_state.json",
            "runtime/state/archive/growth_archive_receipt_batch.json",
        ]

        monitor = build_trait_drift_monitor_from_self_model(
            run_id="trait-growth-monitor",
            generated_at="2026-06-14T00:00:00+08:00",
            self_model_state={
                "growth_window_refs": list(growth_refs),
                "trait_slow_variables": {
                    "continuity_drive": {
                        "value": 0.84,
                        "trend": "rising",
                        "update_count": 4,
                        "last_relationship_stage": (
                            "growth_self_modification_reconsolidation_waiting"
                        ),
                        "growth_self_modification_update_mode": (
                            "growth_self_modification_rehearsal_hold"
                        ),
                        "background_growth_self_modification_pressure_level": "present",
                        "background_growth_self_modification_attention_target": (
                            "growth_self_modification_archive_replay"
                        ),
                        "background_growth_self_modification_waiting_posture": (
                            "growth_self_modification_shadow_archive_waiting"
                        ),
                        "background_growth_self_modification_boundary": (
                            "structured_growth_evidence_not_spoken_language_or_autonomous_code_rewrite"
                        ),
                        "background_growth_self_modification_active_domain_count": 7,
                        "background_growth_self_modification_growth_pressure_count": 2,
                        "background_growth_self_modification_patch_candidate_count": 1,
                        "background_growth_self_modification_archive_receipt_count": 1,
                        "evidence_refs": list(growth_refs),
                    }
                },
            },
            relationship_graph={
                "subjects": [
                    {
                        "relationship_stage": (
                            "growth_self_modification_reconsolidation_waiting"
                        ),
                        "relationship_stage_evidence_refs": list(growth_refs),
                    }
                ]
            },
            trigger_ref="runtime/reports/latest/resumed_external_dialogue_packet.json",
        )

        profile = monitor["growth_self_modification_observation_profile"]
        self.assertEqual(
            profile["schema_version"],
            "growth_self_modification_trait_observation_v0",
        )
        self.assertEqual(profile["trait_names"], ["continuity_drive"])
        self.assertEqual(profile["growth_ref_count"], 3)
        self.assertEqual(profile["pressure_level"], "present")
        self.assertEqual(
            profile["boundary"],
            "structured_growth_evidence_not_spoken_language_or_autonomous_code_rewrite",
        )
        self.assertEqual(
            monitor["growth_self_modification_trait_names"],
            ["continuity_drive"],
        )
        self.assertEqual(monitor["growth_self_modification_ref_count"], 3)
        self.assertEqual(
            monitor["drift_direction"],
            "growth_self_modification_reconsolidation_observed",
        )


if __name__ == "__main__":
    unittest.main()
