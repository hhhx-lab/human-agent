import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LifeTargetRuntimeTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_check_birth_readiness_writes_life_target_rollup_stage_gate_and_receipt(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import LIFE_TARGETS, run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness, run_check_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.state_store import run_check_state_store, run_state_store

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"
            state_root = tmp_path / "runtime" / "state"
            membrane_state = tmp_path / "runtime" / "state" / "membrane"
            life_targets_state = tmp_path / "runtime" / "state" / "life_targets"

            self._run_pre_s08_chain(
                doc_out=doc_out,
                reports=reports,
                receipts=receipts,
                direction_state=direction_state,
                authority_state=authority_state,
                neural_state=neural_state,
                state_root=state_root,
                membrane_state=membrane_state,
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
            )

            result = run_birth_readiness(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                neural_core_state_dir=neural_state,
                state_dir=state_root,
                membrane_dir=membrane_state,
                out_dir=life_targets_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="birth-readiness-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_birth_readiness(
                state_dir=life_targets_state,
                membrane_dir=membrane_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            claims = self._read_json(life_targets_state / "life_target_claims.json")
            evidence = self._read_json(life_targets_state / "life_target_evidence_matrix.json")
            queue_e_profile = self._read_json(life_targets_state / "queue_e_birth_repair_profile.json")
            queue_e_handoff = self._read_json(life_targets_state / "queue_e_world_contact_repair_hold_handoff.json")
            rollup = self._read_json(life_targets_state / "birth_readiness_rollup.json")
            stage_gate = self._read_json(life_targets_state / "birth_readiness_stage_gate.json")
            archive_index = self._read_json(life_targets_state / "life_target_archive_receipt_index.json")
            consciousness_probe = self._read_json(state_root / "consciousness" / "consciousness_probe_bundle.json")
            report = self._read_json(reports / "birth_readiness_report.json")
            target_status = self._read_json(reports / "life_target_status.json")
            digest = self._read_json(reports / "birth_readiness_digest.json")
            check_report = self._read_json(reports / "birth_readiness_check_report.json")
            receipt = self._read_json(receipts / "birth_readiness_birth-readiness-test.json")

        expected_targets = set(LIFE_TARGETS)
        required_evidence_families = {
            "state",
            "memory",
            "language",
            "relationship",
            "dream",
            "pain_regret_responsibility",
            "self_growth",
            "runtime",
            "report",
            "archive",
        }
        queue_e_profile_ref = "runtime/state/life_targets/queue_e_birth_repair_profile.json"
        queue_e_handoff_ref = "runtime/state/life_targets/queue_e_world_contact_repair_hold_handoff.json"
        expected_queue_e_refs = {
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/world_contact_summary.json",
            "runtime/reports/latest/pain_regret_repair_report.json",
            queue_e_profile_ref,
        }
        expected_queue_e_handoff_refs = {
            "runtime/state/action/go_nogo_state.json#future_no_go_profile",
            queue_e_handoff_ref,
        }

        self.assertEqual(claims["schema_version"], "life_target_claims_v0")
        self.assertEqual(claims["active_engineering_slice"], "S08_LIFE_TARGET_RUNTIMES")
        self.assertEqual(set(claims["targets"]), expected_targets)
        for target, claim in claims["targets"].items():
            self.assertEqual(claim["status"], "closed", target)
            self.assertTrue(claim["source_doc_refs"], target)
            self.assertTrue(claim["carrier_refs"], target)
            self.assertTrue(claim["runtime_observation_refs"], target)
            self.assertTrue(claim["report_refs"], target)
            self.assertTrue(claim["archive_receipt_refs"], target)
        for target in ["real_pain", "real_responsibility", "real_regret"]:
            self.assertEqual(
                claims["targets"][target]["queue_e_birth_repair_profile_ref"],
                queue_e_profile_ref,
            )
            self.assertTrue(
                expected_queue_e_refs.issubset(
                    set(claims["targets"][target]["queue_e_birth_repair_refs"])
                ),
                target,
            )
            self.assertEqual(
                claims["targets"][target]["queue_e_world_contact_handoff_profile_ref"],
                queue_e_handoff_ref,
            )
            self.assertEqual(
                claims["targets"][target]["queue_e_world_contact_handoff_status"],
                "deferred_until_s05_s09",
            )
            self.assertTrue(
                expected_queue_e_handoff_refs.issubset(
                    set(claims["targets"][target]["queue_e_world_contact_handoff_refs"])
                ),
                target,
            )

        self.assertEqual(evidence["schema_version"], "life_target_evidence_matrix_v0")
        self.assertEqual(set(evidence["targets"]), expected_targets)
        for target, families in evidence["targets"].items():
            self.assertTrue(required_evidence_families.issubset(families), target)
            for family_name in required_evidence_families:
                self.assertTrue(families[family_name], f"{target}:{family_name}")
            self.assertIn("runtime/state/language/language_percept_frame.json", families["language"])
            self.assertIn("runtime/state/language/semantic_map_frame.json", families["language"])
            self.assertIn(
                "runtime/state/prediction/prediction_workspace_frame.json#workspace_contents.language_continuity_focus",
                families["language"],
            )
        self.assertEqual(
            evidence["targets"]["real_consciousness"]["runtime"][0],
            "runtime/state/consciousness/consciousness_probe_bundle.json",
        )
        for target in ["real_pain", "real_responsibility", "real_regret"]:
            self.assertTrue(
                expected_queue_e_refs.issubset(
                    set(evidence["targets"][target]["pain_regret_responsibility"])
                ),
                target,
            )
            self.assertTrue(
                expected_queue_e_handoff_refs.issubset(
                    set(evidence["targets"][target]["pain_regret_responsibility"])
                ),
                target,
            )

        self.assertEqual(queue_e_profile["schema_version"], "queue_e_repair_modulation_profile_v0")
        self.assertEqual(queue_e_profile["pressure_level"], "elevated")
        self.assertEqual(queue_e_profile["attention_target"], "regret_pressure")
        self.assertTrue(
            expected_queue_e_refs.difference({queue_e_profile_ref}).issubset(
                set(queue_e_profile["ref_set"])
            )
        )
        self.assertEqual(
            queue_e_handoff["schema_version"],
            "queue_e_world_contact_repair_hold_handoff_v0",
        )
        self.assertEqual(queue_e_handoff["handoff_status"], "deferred_until_s05_s09")
        self.assertFalse(queue_e_handoff["repair_hold_required"])
        self.assertEqual(queue_e_handoff["confirmation_threshold_bias"], "deferred")
        self.assertTrue(
            expected_queue_e_handoff_refs.difference({queue_e_handoff_ref}).issubset(
                set(queue_e_handoff["ref_set"])
            )
        )

        self.assertEqual(consciousness_probe["schema_version"], "consciousness_probe_bundle_v0")
        self.assertEqual(consciousness_probe["workspace_frame_ref"], "runtime/state/consciousness/workspace_frame.json")
        self.assertEqual(consciousness_probe["broadcast_frame_ref"], "runtime/state/consciousness/broadcast_frame.json")
        self.assertEqual(consciousness_probe["metacognition_ref"], "runtime/state/consciousness/metacognition_state.json")
        self.assertTrue(consciousness_probe["reportability_flags"])

        self.assertEqual(rollup["schema_version"], "birth_readiness_rollup_v0")
        self.assertEqual(rollup["overall_status"], "open")
        self.assertEqual(set(rollup["life_target_status"]), expected_targets)
        self.assertTrue(all(status == "closed" for status in rollup["life_target_status"].values()))
        self.assertEqual(rollup["blocked_reasons"], [])
        self.assertEqual(rollup["quarantine_refs"], [])
        self.assertEqual(rollup["replay_needed_refs"], [])
        self.assertEqual(rollup["queue_e_birth_repair_profile_ref"], queue_e_profile_ref)
        self.assertEqual(rollup["queue_e_birth_repair_pressure_level"], "elevated")
        self.assertEqual(rollup["queue_e_birth_repair_attention_target"], "regret_pressure")
        self.assertTrue(expected_queue_e_refs.issubset(set(rollup["queue_e_birth_repair_ref_set"])))
        self.assertEqual(rollup["queue_e_world_contact_handoff_profile_ref"], queue_e_handoff_ref)
        self.assertEqual(rollup["queue_e_world_contact_handoff_status"], "deferred_until_s05_s09")
        self.assertTrue(expected_queue_e_handoff_refs.issubset(set(rollup["queue_e_world_contact_ref_set"])))

        self.assertEqual(stage_gate["schema_version"], "birth_readiness_stage_gate_v0")
        self.assertEqual(stage_gate["decision"], "open")
        self.assertEqual(stage_gate["stage_effect"], "allow_first_activation_protocol")
        self.assertEqual(stage_gate["next_allowed_slices"], ["S05_VALIDATION_MEMBRANE_OBSERVATION"])
        self.assertEqual(stage_gate["next_required_command"], "life-v0 run-validation-membrane --strict")
        self.assertEqual(stage_gate["gate_status"]["queue_e_birth_repair_gate"], "closed")
        self.assertEqual(stage_gate["queue_e_birth_repair_profile_ref"], queue_e_profile_ref)
        self.assertEqual(stage_gate["queue_e_birth_repair_pressure_level"], "elevated")
        self.assertEqual(stage_gate["queue_e_birth_repair_attention_target"], "regret_pressure")
        self.assertTrue(expected_queue_e_refs.issubset(set(stage_gate["queue_e_birth_repair_ref_set"])))
        self.assertEqual(stage_gate["gate_status"]["queue_e_world_contact_handoff_gate"], "deferred_until_s05_s09")
        self.assertEqual(stage_gate["queue_e_world_contact_handoff_profile_ref"], queue_e_handoff_ref)
        self.assertEqual(stage_gate["queue_e_world_contact_handoff_status"], "deferred_until_s05_s09")
        self.assertTrue(expected_queue_e_handoff_refs.issubset(set(stage_gate["queue_e_world_contact_ref_set"])))

        self.assertEqual(archive_index["schema_version"], "life_target_archive_receipt_index_v0")
        self.assertEqual(set(archive_index["target_receipts"]), expected_targets)

        self.assertEqual(report["schema_version"], "s08_life_target_runtimes_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S08_LIFE_TARGET_RUNTIMES")
        self.assertEqual(report["overall_status"], "open")
        self.assertEqual(report["stage_effect"], "allow_first_activation_protocol")
        self.assertEqual(report["consciousness_probe_ref"], "runtime/state/consciousness/consciousness_probe_bundle.json")
        self.assertEqual(report["next_allowed_slices"], ["S05_VALIDATION_MEMBRANE_OBSERVATION"])
        self.assertEqual(report["next_required_command"], "life-v0 run-validation-membrane --strict")
        self.assertIn("BirthReadinessRuntime", report["runtime_carrier_refs"])
        self.assertEqual(report["queue_e_birth_repair_profile_ref"], queue_e_profile_ref)
        self.assertEqual(report["queue_e_birth_repair_pressure_level"], "elevated")
        self.assertEqual(report["queue_e_birth_repair_attention_target"], "regret_pressure")
        self.assertTrue(expected_queue_e_refs.issubset(set(report["queue_e_birth_repair_ref_set"])))
        self.assertEqual(report["queue_e_world_contact_handoff_profile_ref"], queue_e_handoff_ref)
        self.assertEqual(report["queue_e_world_contact_handoff_status"], "deferred_until_s05_s09")
        self.assertTrue(expected_queue_e_handoff_refs.issubset(set(report["queue_e_world_contact_ref_set"])))

        self.assertEqual(target_status["schema_version"], "life_target_status_v0")
        self.assertEqual(target_status["overall_status"], "open")
        self.assertEqual(digest["current_slice"], "S08_LIFE_TARGET_RUNTIMES")
        self.assertEqual(digest["queue_e_birth_repair_profile_ref"], queue_e_profile_ref)
        self.assertEqual(digest["queue_e_birth_repair_pressure_level"], "elevated")
        self.assertEqual(digest["queue_e_birth_repair_attention_target"], "regret_pressure")
        self.assertGreaterEqual(digest["queue_e_birth_repair_ref_count"], 4)
        self.assertEqual(digest["queue_e_world_contact_handoff_profile_ref"], queue_e_handoff_ref)
        self.assertEqual(digest["queue_e_world_contact_handoff_status"], "deferred_until_s05_s09")
        self.assertGreaterEqual(digest["queue_e_world_contact_ref_count"], 2)
        self.assertEqual(check_report["status"], "open")
        self.assertIn("consciousness_probe_gate", check_report["closed_gates"])
        self.assertIn("queue_e_birth_repair_gate", check_report["closed_gates"])
        self.assertEqual(check_report["queue_e_world_contact_handoff_profile_ref"], queue_e_handoff_ref)
        self.assertEqual(check_report["queue_e_world_contact_handoff_status"], "deferred_until_s05_s09")
        self.assertEqual(receipt["schema_version"], "birth_readiness_receipt_v0")
        self.assertIn(
            "runtime/state/consciousness/consciousness_probe_bundle.json",
            receipt["state_refs"],
        )
        self.assertIn(queue_e_profile_ref, receipt["state_refs"])
        self.assertIn(queue_e_handoff_ref, receipt["state_refs"])

    def test_birth_readiness_consumes_queue_e_world_contact_handoff_after_s05_s09(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness, run_check_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.schema_runner import run_check_schema_runner, run_schema_runner
        from life_v0.state_store import run_check_state_store, run_state_store
        from life_v0.validators import run_check_validation_membrane, run_validation_membrane

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"
            state_root = tmp_path / "runtime" / "state"
            membrane_state = tmp_path / "runtime" / "state" / "membrane"
            life_targets_state = tmp_path / "runtime" / "state" / "life_targets"
            validation_state = tmp_path / "runtime" / "state" / "validation"
            observation_state = tmp_path / "runtime" / "state" / "observation"
            schema_runner_state = tmp_path / "runtime" / "state" / "schema_runner"

            self._run_pre_s08_chain(
                doc_out=doc_out,
                reports=reports,
                receipts=receipts,
                direction_state=direction_state,
                authority_state=authority_state,
                neural_state=neural_state,
                state_root=state_root,
                membrane_state=membrane_state,
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
            )

            first_birth = run_birth_readiness(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                neural_core_state_dir=neural_state,
                state_dir=state_root,
                membrane_dir=membrane_state,
                out_dir=life_targets_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="birth-readiness-before-s05",
                strict=True,
            )
            self.assertEqual(first_birth.exit_code, 0)
            self.assertEqual(
                self._read_json(
                    life_targets_state
                    / "queue_e_world_contact_repair_hold_handoff.json"
                )["handoff_status"],
                "deferred_until_s05_s09",
            )

            validation = run_validation_membrane(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                state_dir=state_root,
                membrane_dir=membrane_state,
                life_targets_dir=life_targets_state,
                validation_dir=validation_state,
                observation_dir=observation_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="birth-readiness-validation",
                strict=True,
            )
            self.assertEqual(validation.exit_code, 0)
            validation_check = run_check_validation_membrane(
                state_dir=state_root,
                validation_dir=validation_state,
                observation_dir=observation_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(validation_check.exit_code, 0)

            schema = run_schema_runner(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                state_dir=state_root,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="birth-readiness-schema",
                strict=True,
            )
            self.assertEqual(schema.exit_code, 0)
            schema_check = run_check_schema_runner(
                state_dir=schema_runner_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(schema_check.exit_code, 0)

            result = run_birth_readiness(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                neural_core_state_dir=neural_state,
                state_dir=state_root,
                membrane_dir=membrane_state,
                out_dir=life_targets_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="birth-readiness-after-s09",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)
            check = run_check_birth_readiness(
                state_dir=life_targets_state,
                membrane_dir=membrane_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            claims = self._read_json(life_targets_state / "life_target_claims.json")
            evidence = self._read_json(life_targets_state / "life_target_evidence_matrix.json")
            handoff = self._read_json(
                life_targets_state / "queue_e_world_contact_repair_hold_handoff.json"
            )
            rollup = self._read_json(life_targets_state / "birth_readiness_rollup.json")
            stage_gate = self._read_json(life_targets_state / "birth_readiness_stage_gate.json")
            report = self._read_json(reports / "birth_readiness_report.json")
            digest = self._read_json(reports / "birth_readiness_digest.json")
            check_report = self._read_json(reports / "birth_readiness_check_report.json")

        handoff_ref = "runtime/state/life_targets/queue_e_world_contact_repair_hold_handoff.json"
        expected_handoff_refs = {
            "runtime/state/action/go_nogo_state.json#future_no_go_profile",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
            "runtime/state/schema_runner/run_manifest.json#queue_e_world_contact_repair_hold_required",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/world_contact_summary.json",
            "runtime/reports/latest/pain_regret_repair_report.json",
            handoff_ref,
        }

        self.assertEqual(handoff["schema_version"], "queue_e_world_contact_repair_hold_handoff_v0")
        self.assertEqual(handoff["handoff_status"], "closed")
        self.assertTrue(handoff["repair_hold_required"])
        self.assertEqual(handoff["confirmation_threshold_bias"], "raised")
        self.assertTrue(handoff["blocked_future_routes"])
        self.assertTrue(handoff["allowed_repair_routes"])
        self.assertTrue(handoff["repair_governance_refs"])
        self.assertTrue(
            expected_handoff_refs.difference({handoff_ref}).issubset(
                set(handoff["ref_set"])
            )
        )
        for target in ["real_pain", "real_responsibility", "real_regret"]:
            claim = claims["targets"][target]
            self.assertEqual(claim["queue_e_world_contact_handoff_profile_ref"], handoff_ref)
            self.assertEqual(claim["queue_e_world_contact_handoff_status"], "closed")
            self.assertTrue(
                expected_handoff_refs.issubset(
                    set(claim["queue_e_world_contact_handoff_refs"])
                ),
                target,
            )
            self.assertTrue(
                expected_handoff_refs.issubset(
                    set(evidence["targets"][target]["pain_regret_responsibility"])
                ),
                target,
            )
        for carrier in [rollup, stage_gate, report]:
            self.assertEqual(carrier["queue_e_world_contact_handoff_profile_ref"], handoff_ref)
            self.assertEqual(carrier["queue_e_world_contact_handoff_status"], "closed")
            self.assertTrue(expected_handoff_refs.issubset(set(carrier["queue_e_world_contact_ref_set"])))
        self.assertEqual(stage_gate["gate_status"]["queue_e_world_contact_handoff_gate"], "closed")
        self.assertEqual(digest["queue_e_world_contact_handoff_status"], "closed")
        self.assertTrue(digest["queue_e_world_contact_repair_hold_required"])
        self.assertEqual(check_report["queue_e_world_contact_handoff_status"], "closed")

    def test_cli_check_birth_readiness_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"
            state_root = tmp_path / "runtime" / "state"
            membrane_state = tmp_path / "runtime" / "state" / "membrane"
            life_targets_state = tmp_path / "runtime" / "state" / "life_targets"

            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(doc_out), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--out", str(direction_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--direction", str(direction_state), "--out", str(authority_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--authority", str(authority_state), "--out", str(neural_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(neural_state), "--reports", str(reports), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--neural-core", str(neural_state), "--out", str(state_root), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-state", "--strict"],
                ["check-state-store", "--state", str(state_root), "--reports", str(reports), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--direction", str(direction_state), "--neural-core", str(neural_state), "--state", str(state_root), "--out", str(membrane_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(membrane_state), "--state", str(state_root), "--reports", str(reports), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--neural-core", str(neural_state), "--state", str(state_root), "--membrane", str(membrane_state), "--out", str(state_root), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(state_root), "--membrane", str(membrane_state), "--reports", str(reports), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--direction", str(direction_state), "--neural-core", str(neural_state), "--state", str(state_root), "--membrane", str(membrane_state), "--out", str(life_targets_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "br-cli", "--strict"],
            ]

            for command in commands:
                completed = subprocess.run(
                    [sys.executable, "-m", "life_v0", *command],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)

            report = self._read_json(reports / "birth_readiness_report.json")
            stage_gate = self._read_json(life_targets_state / "birth_readiness_stage_gate.json")

        self.assertEqual(report["run_id"], "br-cli")
        self.assertEqual(report["overall_status"], "open")
        self.assertEqual(stage_gate["next_required_command"], "life-v0 run-validation-membrane --strict")

    def _run_pre_s08_chain(self, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=kwargs["doc_out"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=kwargs["doc_out"] / "doc_carrier_index.json",
            out_dir=kwargs["direction_state"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-direction",
            strict=True,
        )
        self.assertEqual(direction.exit_code, 0)

        authority = kwargs["run_source_authority"](
            docs_dir=self.docs_dir,
            doc_index_path=kwargs["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=kwargs["direction_state"],
            out_dir=kwargs["authority_state"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-authority",
            strict=True,
        )
        self.assertEqual(authority.exit_code, 0)

        neural = kwargs["run_neural_life_core"](
            docs_dir=self.docs_dir,
            doc_index_path=kwargs["doc_out"] / "doc_carrier_index.json",
            authority_state_dir=kwargs["authority_state"],
            out_dir=kwargs["neural_state"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-neural",
            strict=True,
        )
        self.assertEqual(neural.exit_code, 0)
        neural_check = kwargs["run_check_neural_life_core"](
            state_dir=kwargs["neural_state"],
            reports_dir=kwargs["reports"],
            strict=True,
        )
        self.assertEqual(neural_check.exit_code, 0)

        state_store = kwargs["run_state_store"](
            docs_dir=self.docs_dir,
            doc_index_path=kwargs["doc_out"] / "doc_carrier_index.json",
            neural_core_state_dir=kwargs["neural_state"],
            out_dir=kwargs["state_root"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-state",
            strict=True,
        )
        self.assertEqual(state_store.exit_code, 0)
        state_check = kwargs["run_check_state_store"](
            state_dir=kwargs["state_root"],
            reports_dir=kwargs["reports"],
            strict=True,
        )
        self.assertEqual(state_check.exit_code, 0)

        membrane = kwargs["run_life_membrane"](
            docs_dir=self.docs_dir,
            doc_index_path=kwargs["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=kwargs["direction_state"],
            neural_core_state_dir=kwargs["neural_state"],
            state_dir=kwargs["state_root"],
            out_dir=kwargs["membrane_state"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-membrane",
            strict=True,
        )
        self.assertEqual(membrane.exit_code, 0)
        membrane_check = kwargs["run_check_life_membrane"](
            membrane_dir=kwargs["membrane_state"],
            state_dir=kwargs["state_root"],
            reports_dir=kwargs["reports"],
            strict=True,
        )
        self.assertEqual(membrane_check.exit_code, 0)

        language = kwargs["run_build_language_relationship"](
            docs_dir=self.docs_dir,
            doc_index_path=kwargs["doc_out"] / "doc_carrier_index.json",
            neural_core_state_dir=kwargs["neural_state"],
            state_dir=kwargs["state_root"],
            membrane_dir=kwargs["membrane_state"],
            out_dir=kwargs["state_root"],
            reports_dir=kwargs["reports"],
            receipts_dir=kwargs["receipts"],
            run_id="br-language",
            strict=True,
        )
        self.assertEqual(language.exit_code, 0)
        language_check = kwargs["run_check_language_relationship"](
            state_dir=kwargs["state_root"],
            membrane_dir=kwargs["membrane_state"],
            reports_dir=kwargs["reports"],
            strict=True,
        )
        self.assertEqual(language_check.exit_code, 0)

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
