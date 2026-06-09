import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from life_v0.dream.nightmare_risk import build_nightmare_loop_risk
from life_v0.growth.belief_learning import build_belief_learning_plan
from life_v0.growth.language_learning import build_language_learning_plan
from life_v0.growth.relationship_learning import build_relationship_learning_plan


class RuntimeGrowthTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_cli_run_cycle_shadow_only_writes_s10_runtime_bundle(self):
        from life_v0.authority import run_source_authority
        from life_v0.body import run_check_life_support, run_life_support
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
        from life_v0.state_store import run_check_state_store, run_state_store
        from life_v0.validators import run_check_validation_membrane, run_validation_membrane

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            self._run_pre_s10_chain(
                paths,
                run_doc_ingestion=run_doc_ingestion,
                run_direction_lock=run_direction_lock,
                run_source_authority=run_source_authority,
                run_neural_life_core=run_neural_life_core,
                run_check_neural_life_core=run_check_neural_life_core,
                run_state_store=run_state_store,
                run_check_state_store=run_check_state_store,
                run_life_membrane=run_life_membrane,
                run_check_life_membrane=run_check_life_membrane,
                run_build_language_relationship=run_build_language_relationship,
                run_check_language_relationship=run_check_language_relationship,
                run_birth_readiness=run_birth_readiness,
                run_validation_membrane=run_validation_membrane,
                run_check_validation_membrane=run_check_validation_membrane,
                run_schema_runner=run_schema_runner,
                run_check_schema_runner=run_check_schema_runner,
                run_schema_smoke=run_schema_smoke,
                run_life_support=run_life_support,
                run_check_life_support=run_check_life_support,
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0",
                    "run-cycle",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--run-id",
                    "runtime-growth-cli",
                    "--shadow-only",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

            runtime_mount = self._read_json(paths["growth_state"] / "runtime_mount_state.json")
            shadow_trace = self._read_json(paths["replay_state"] / "shadow_cycle_trace.json")
            replay_cue_bundle = self._read_json(paths["replay_state"] / "replay_cue_bundle.json")
            dream_frame = self._read_json(paths["dream_state"] / "dream_consolidation_frame.json")
            offline_entry = self._read_json(paths["dream_state"] / "offline_entry_gate.json")
            offline_consolidation = self._read_json(paths["dream_state"] / "offline_consolidation_frame.json")
            dream_fact_gate = self._read_json(paths["dream_state"] / "dream_fact_gate_decision.json")
            nightmare_risk = self._read_json(paths["dream_state"] / "nightmare_loop_risk.json")
            pain_replay = self._read_json(paths["replay_state"] / "pain_regret_responsibility_replay.json")
            self_read = self._read_json(paths["growth_state"] / "self_read_report.json")
            growth_queue = self._read_json(paths["growth_state"] / "growth_patch_queue.json")
            growth_patch_candidate = self._read_json(paths["growth_state"] / "growth_patch_candidate_queue.json")
            anti_forgetting_plan = self._read_json(paths["growth_state"] / "anti_forgetting_replay_plan.json")
            belief_learning = self._read_json(paths["growth_state"] / "belief_learning_plan.json")
            language_learning = self._read_json(paths["growth_state"] / "language_learning_plan.json")
            relationship_learning = self._read_json(paths["growth_state"] / "relationship_learning_plan.json")
            archive_graph = self._read_json(paths["archive_state"] / "reconsolidation_archive_graph.json")
            next_seed = self._read_json(paths["growth_state"] / "next_feedback_seed.json")
            growth_report = self._read_json(paths["reports"] / "growth_reconsolidation_report.json")
            run_report = self._read_json(paths["reports"] / "run_report.json")
            digest = self._read_json(paths["reports"] / "digest.json")
            stage_gate = self._read_json(paths["reports"] / "stage_gate.json")
            quarantine = self._read_json(paths["reports"] / "quarantine.json")
            replay_needed = self._read_json(paths["reports"] / "replay_needed.json")
            receipt = self._read_json(paths["receipts"] / "run_cycle_runtime-growth-cli.json")

        self.assertEqual(runtime_mount["schema_version"], "runtime_mount_state_v0")
        self.assertEqual(runtime_mount["status"], "closed")
        self.assertEqual(runtime_mount["life_support_gate"]["status"], "closed")
        self.assertEqual(runtime_mount["schema_mount_gate"]["status"], "closed")
        self.assertEqual(runtime_mount["birth_readiness_gate"]["status"], "open")

        self.assertEqual(shadow_trace["schema_version"], "shadow_cycle_trace_v0")
        self.assertTrue(shadow_trace["shadow_only"])
        self.assertIn("old_self", shadow_trace["replayed_anchor_families"])
        self.assertIn("old_language", shadow_trace["replayed_anchor_families"])
        self.assertIn("old_relationship", shadow_trace["replayed_anchor_families"])

        self.assertEqual(replay_cue_bundle["schema_version"], "replay_cue_bundle_v0")
        self.assertEqual(replay_cue_bundle["status"], "closed")
        self.assertTrue(replay_cue_bundle["turn_residue_refs"])
        self.assertTrue(replay_cue_bundle["relationship_residue_refs"])
        self.assertTrue(replay_cue_bundle["pain_regret_residue_refs"])
        self.assertTrue(replay_cue_bundle["dream_entry_candidates"])
        self.assertTrue(replay_cue_bundle["anti_forgetting_targets"])
        self.assertEqual(replay_cue_bundle["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(replay_cue_bundle["repair_followup_required"])
        self.assertEqual(replay_cue_bundle["queue_e_priority_band"], "repair_guarded")
        self.assertGreaterEqual(replay_cue_bundle["repair_obligation_count"], 1)
        self.assertGreaterEqual(replay_cue_bundle["regret_pressure_count"], 1)

        self.assertEqual(dream_frame["schema_version"], "dream_consolidation_frame_v0")
        self.assertEqual(dream_frame["dream_fact_gate"], "closed")
        self.assertEqual(dream_frame["status"], "closed")

        self.assertEqual(offline_entry["schema_version"], "offline_entry_gate_v0")
        self.assertEqual(offline_entry["entry_decision"], "offline_allowed")
        self.assertEqual(offline_entry["external_action_policy"], "blocked")
        self.assertTrue(offline_entry["offline_modes"])
        self.assertTrue(offline_entry["entry_pressure"])

        self.assertEqual(offline_consolidation["schema_version"], "offline_consolidation_frame_v0")
        self.assertEqual(offline_consolidation["status"], "closed")
        self.assertTrue(offline_consolidation["replay_cue_refs"])
        self.assertTrue(offline_consolidation["dream_window_refs"])
        self.assertTrue(offline_consolidation["dream_fact_gate_refs"])
        self.assertTrue(offline_consolidation["wake_integration_targets"])
        self.assertTrue(offline_consolidation["growth_patch_seed_refs"])

        self.assertEqual(dream_fact_gate["schema_version"], "dream_fact_gate_decision_v0")
        self.assertEqual(dream_fact_gate["object_kind"], "DreamFactGateDecision")
        self.assertEqual(dream_fact_gate["gate_result"], "passed")
        self.assertTrue(dream_fact_gate["decision_items"])
        self.assertTrue(dream_fact_gate["allowed_writes"])
        self.assertTrue(dream_fact_gate["blocked_writes"])

        self.assertEqual(nightmare_risk["schema_version"], "nightmare_loop_risk_v0")
        self.assertEqual(nightmare_risk["object_kind"], "NightmareLoopRisk")
        self.assertIn(nightmare_risk["risk_status"], {"guarded", "elevated"})
        self.assertTrue(nightmare_risk["source_residue_refs"])
        self.assertTrue(nightmare_risk["recovery_targets"])
        self.assertEqual(nightmare_risk["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(nightmare_risk["repair_followup_required"])
        self.assertEqual(nightmare_risk["queue_e_priority_band"], "repair_guarded")
        self.assertIn("guarded_repair_followup", nightmare_risk["loop_indicators"])

        self.assertEqual(pain_replay["schema_version"], "pain_regret_responsibility_replay_v0")
        self.assertEqual(pain_replay["status"], "closed")
        self.assertTrue(pain_replay["repair_obligation_refs"])

        self.assertEqual(self_read["schema_version"], "self_read_report_v0")
        self.assertEqual(self_read["event_kind"], "SelfReadReport")
        self.assertTrue(self_read["read_scope"])
        self.assertTrue(self_read["growth_pressures"])
        self.assertTrue(self_read["protected_core_refs"])
        self.assertTrue(self_read["recommended_growth_paths"])

        self.assertEqual(growth_queue["schema_version"], "growth_patch_queue_v0")
        self.assertEqual(growth_queue["status"], "queued_guarded")
        self.assertIn("anti_forgetting_replay_patch", growth_queue["queued_patch_families"])

        self.assertEqual(growth_patch_candidate["schema_version"], "growth_patch_candidate_queue_v0")
        self.assertEqual(growth_patch_candidate["status"], "closed")
        self.assertTrue(growth_patch_candidate["candidates"])
        first_candidate = growth_patch_candidate["candidates"][0]
        self.assertTrue(first_candidate["source_residue_refs"])
        self.assertEqual(first_candidate["plasticity_window_ref"], "runtime/state/growth/plasticity_window_state.json")
        self.assertTrue(first_candidate["risk_flags"])
        self.assertTrue(first_candidate["anti_forgetting_requirements"])
        self.assertTrue(first_candidate["core_continuity_requirements"])
        self.assertEqual(first_candidate["archive_requirement"], "required_before_activation")

        self.assertEqual(anti_forgetting_plan["schema_version"], "anti_forgetting_replay_plan_v0")
        self.assertEqual(anti_forgetting_plan["event_kind"], "AntiForgettingReplayPlan")
        self.assertIn("core_self_replay", anti_forgetting_plan["replay_sets"])
        self.assertIn("relationship_replay", anti_forgetting_plan["replay_sets"])
        self.assertIn("memory_integrity_replay", anti_forgetting_plan["replay_sets"])
        self.assertIn("capability_replay", anti_forgetting_plan["replay_sets"])
        self.assertIn("pain_regret_replay", anti_forgetting_plan["replay_sets"])
        self.assertIn("dream_replay", anti_forgetting_plan["replay_sets"])

        self.assertEqual(belief_learning["schema_version"], "belief_learning_plan_v0")
        self.assertEqual(belief_learning["object_kind"], "BeliefLearningPlan")
        self.assertEqual(belief_learning["window_status"], "guarded_pre_activation")
        self.assertTrue(belief_learning["belief_targets"])
        self.assertTrue(belief_learning["evidence_inputs"])
        self.assertEqual(belief_learning["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(belief_learning["repair_followup_required"])
        self.assertEqual(belief_learning["queue_e_priority_band"], "repair_guarded")
        self.assertIn("repair_accountability_belief_revision", belief_learning["belief_targets"])

        self.assertEqual(language_learning["schema_version"], "language_learning_plan_v0")
        self.assertEqual(language_learning["object_kind"], "LanguageLearningPlan")
        self.assertEqual(language_learning["window_status"], "guarded_pre_activation")
        self.assertTrue(language_learning["language_targets"])
        self.assertTrue(language_learning["continuity_inputs"])
        self.assertEqual(language_learning["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(language_learning["repair_followup_required"])
        self.assertEqual(language_learning["queue_e_priority_band"], "repair_guarded")
        self.assertIn("apology_repair_expression_refinement", language_learning["language_targets"])

        self.assertEqual(relationship_learning["schema_version"], "relationship_learning_plan_v0")
        self.assertEqual(relationship_learning["object_kind"], "RelationshipLearningPlan")
        self.assertEqual(relationship_learning["window_status"], "guarded_pre_activation")
        self.assertTrue(relationship_learning["relationship_targets"])
        self.assertTrue(relationship_learning["repair_inputs"])
        self.assertEqual(relationship_learning["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(relationship_learning["repair_followup_required"])
        self.assertEqual(relationship_learning["queue_e_priority_band"], "repair_guarded")
        self.assertIn("repair_reentry_timing_adjustment", relationship_learning["relationship_targets"])

        self.assertEqual(archive_graph["schema_version"], "reconsolidation_archive_graph_v0")
        self.assertEqual(archive_graph["status"], "closed")
        self.assertTrue(archive_graph["archive_edges"])

        self.assertEqual(next_seed["schema_version"], "next_feedback_seed_v0")
        self.assertEqual(next_seed["status"], "seeded")
        self.assertIn("replay_shadow", next_seed["seed_families"])

        self.assertEqual(growth_report["schema_version"], "s10_runtime_growth_reconsolidation_report_v0")
        self.assertEqual(growth_report["engineering_slice_ref"], "S10_RUNTIME_GROWTH_RECONSOLIDATION")
        self.assertEqual(growth_report["status"], "safe_idle")
        self.assertEqual(growth_report["next_allowed_slices"], ["S11_V0_ENGINEERING_CONTRACTS"])
        self.assertEqual(growth_report["next_required_command"], "life-v0 check-v0-contracts --strict")

        self.assertEqual(run_report["schema_version"], "run_cycle_report_v0")
        self.assertEqual(run_report["command"], "run-cycle")
        self.assertEqual(run_report["status"], "safe_idle")
        self.assertTrue(run_report["cycle_trace"])
        self.assertEqual(run_report["archive_receipt_ref"], "runtime/receipts/run_cycle_runtime-growth-cli.json")

        self.assertEqual(digest["schema_version"], "runtime_growth_digest_v0")
        self.assertEqual(digest["current_slice"], "S10_RUNTIME_GROWTH_RECONSOLIDATION")
        self.assertEqual(digest["status"], "safe_idle")

        self.assertEqual(stage_gate["schema_version"], "runtime_growth_stage_gate_v0")
        self.assertEqual(stage_gate["decision"], "safe_idle")
        self.assertEqual(stage_gate["next_allowed_slices"], ["S11_V0_ENGINEERING_CONTRACTS"])
        self.assertEqual(stage_gate["next_required_command"], "life-v0 check-v0-contracts --strict")

        self.assertEqual(quarantine["schema_version"], "runtime_growth_quarantine_v0")
        self.assertEqual(quarantine["status"], "closed")
        self.assertEqual(replay_needed["schema_version"], "runtime_growth_replay_needed_v0")
        self.assertEqual(replay_needed["status"], "closed")
        self.assertEqual(receipt["schema_version"], "run_cycle_receipt_v0")

    def test_queue_e_priority_band_modulates_dream_and_growth_learning_organs(self):
        replay_cue_bundle = {
            "relationship_residue_refs": ["runtime/state/relationship/relationship_memory.json#r1"],
            "turn_residue_refs": ["runtime/state/replay/shadow_cycle_trace.json"],
            "pain_regret_residue_refs": ["runtime/state/life_state.json#regret_events"],
            "world_contact_release_posture": "confirmation_blocked",
            "repair_followup_required": True,
            "repair_obligation_refs": ["runtime/state/action/responsibility_loop_state.json#repair"],
            "repair_obligation_count": 2,
            "regret_pressure_refs": ["runtime/state/life_state.json#regret_events"],
            "regret_pressure_count": 1,
            "queue_e_priority_band": "locked_repair_urgent",
        }
        learning_window = {
            "window_status": "guarded_pre_activation",
            "blocked_learning_modes": ["self_training"],
        }
        self_read_report = {"growth_pressures": ["pain_recovery_gap"]}
        dream_window = {
            "pain_residue_refs": ["runtime/state/life_state.json#pain_events"],
            "relationship_simulation_refs": ["runtime/state/relationship/relationship_memory.json#r1"],
        }
        pain_replay = {
            "repair_obligation_refs": ["runtime/state/membrane/responsibility_repair_boundary.json"],
        }
        wake_integration = {
            "relationship_repair_candidates": ["runtime/state/relationship/relationship_memory.json#repair"],
        }

        nightmare_risk = build_nightmare_loop_risk(
            run_id="queue-e-growth",
            generated_at="2026-06-10T00:00:00Z",
            dream_window=dream_window,
            pain_replay=pain_replay,
            wake_integration=wake_integration,
            replay_cue_bundle=replay_cue_bundle,
        )
        belief_learning = build_belief_learning_plan(
            run_id="queue-e-growth",
            generated_at="2026-06-10T00:00:00Z",
            learning_window=learning_window,
            replay_cue_bundle=replay_cue_bundle,
            self_read_report=self_read_report,
        )
        language_learning = build_language_learning_plan(
            run_id="queue-e-growth",
            generated_at="2026-06-10T00:00:00Z",
            learning_window=learning_window,
            replay_cue_bundle=replay_cue_bundle,
            self_read_report=self_read_report,
        )
        relationship_learning = build_relationship_learning_plan(
            run_id="queue-e-growth",
            generated_at="2026-06-10T00:00:00Z",
            learning_window=learning_window,
            replay_cue_bundle=replay_cue_bundle,
            self_read_report=self_read_report,
            wake_integration=wake_integration,
        )

        self.assertEqual(nightmare_risk["queue_e_priority_band"], "locked_repair_urgent")
        self.assertIn("confirmation_blocked_repair_lock", nightmare_risk["loop_indicators"])
        self.assertEqual(belief_learning["queue_e_priority_band"], "locked_repair_urgent")
        self.assertIn("confirmation_locked_contact_model_revision", belief_learning["belief_targets"])
        self.assertEqual(language_learning["queue_e_priority_band"], "locked_repair_urgent")
        self.assertIn("confirmation_locked_expression_restraint", language_learning["language_targets"])
        self.assertEqual(relationship_learning["queue_e_priority_band"], "locked_repair_urgent")
        self.assertIn("contact_boundary_respect_rehearsal", relationship_learning["relationship_targets"])

    def _runtime_paths(self, tmp_path: Path) -> dict[str, Path]:
        state_root = tmp_path / "runtime" / "state"
        return {
            "doc_out": tmp_path / "runtime" / "docs",
            "reports": tmp_path / "runtime" / "reports" / "latest",
            "receipts": tmp_path / "runtime" / "receipts",
            "direction_state": state_root / "direction",
            "authority_state": state_root / "authority",
            "neural_state": state_root / "neural_life_core",
            "state_root": state_root,
            "membrane_state": state_root / "membrane",
            "life_targets_state": state_root / "life_targets",
            "validation_state": state_root / "validation",
            "observation_state": state_root / "observation",
            "schema_runner_state": state_root / "schema_runner",
            "body_state": state_root / "body",
            "growth_state": state_root / "growth",
            "defense_state": state_root / "defense",
            "dream_state": state_root / "dream",
            "replay_state": state_root / "replay",
            "archive_state": state_root / "archive",
        }

    def _run_pre_s10_chain(self, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-direction",
            strict=True,
        )
        self.assertEqual(direction.exit_code, 0)

        authority = kwargs["run_source_authority"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=paths["direction_state"],
            out_dir=paths["authority_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-authority",
            strict=True,
        )
        self.assertEqual(authority.exit_code, 0)

        neural = kwargs["run_neural_life_core"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            authority_state_dir=paths["authority_state"],
            out_dir=paths["neural_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-neural",
            strict=True,
        )
        self.assertEqual(neural.exit_code, 0)
        neural_check = kwargs["run_check_neural_life_core"](
            state_dir=paths["neural_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(neural_check.exit_code, 0)

        state_store = kwargs["run_state_store"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            neural_core_state_dir=paths["neural_state"],
            out_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-state",
            strict=True,
        )
        self.assertEqual(state_store.exit_code, 0)
        state_check = kwargs["run_check_state_store"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(state_check.exit_code, 0)

        membrane = kwargs["run_life_membrane"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=paths["direction_state"],
            neural_core_state_dir=paths["neural_state"],
            state_dir=paths["state_root"],
            out_dir=paths["membrane_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-membrane",
            strict=True,
        )
        self.assertEqual(membrane.exit_code, 0)
        membrane_check = kwargs["run_check_life_membrane"](
            membrane_dir=paths["membrane_state"],
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(membrane_check.exit_code, 0)

        language = kwargs["run_build_language_relationship"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            neural_core_state_dir=paths["neural_state"],
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            out_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-language",
            strict=True,
        )
        self.assertEqual(language.exit_code, 0)
        language_check = kwargs["run_check_language_relationship"](
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(language_check.exit_code, 0)

        birth = kwargs["run_birth_readiness"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=paths["direction_state"],
            neural_core_state_dir=paths["neural_state"],
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            out_dir=paths["life_targets_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-birth",
            strict=True,
        )
        self.assertEqual(birth.exit_code, 0)

        validation = kwargs["run_validation_membrane"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            life_targets_dir=paths["life_targets_state"],
            validation_dir=paths["validation_state"],
            observation_dir=paths["observation_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-validation",
            strict=True,
        )
        self.assertEqual(validation.exit_code, 0)
        validation_check = kwargs["run_check_validation_membrane"](
            state_dir=paths["state_root"],
            validation_dir=paths["validation_state"],
            observation_dir=paths["observation_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(validation_check.exit_code, 0)

        schema_runner = kwargs["run_schema_runner"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-schema",
            strict=True,
        )
        self.assertEqual(schema_runner.exit_code, 0)
        schema_check = kwargs["run_check_schema_runner"](
            state_dir=paths["schema_runner_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(schema_check.exit_code, 0)
        schema_smoke = kwargs["run_schema_smoke"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-schema-smoke",
            strict=True,
        )
        self.assertEqual(schema_smoke.exit_code, 0)

        life_support = kwargs["run_life_support"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            validation_report_path=paths["reports"] / "validation_membrane_report.json",
            out_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="growth-life-support",
            strict=True,
        )
        self.assertEqual(life_support.exit_code, 0)
        life_support_check = kwargs["run_check_life_support"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(life_support_check.exit_code, 0)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
