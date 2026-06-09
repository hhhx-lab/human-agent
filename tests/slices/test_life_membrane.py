import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LifeMembraneTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_life_membrane_writes_boundary_gates_and_activation_preflight(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import LIFE_TARGETS, run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
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

            ingest = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=doc_out,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="membrane-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            direction = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="membrane-direction",
                strict=True,
            )
            self.assertEqual(direction.exit_code, 0)

            authority = run_source_authority(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                out_dir=authority_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="membrane-authority",
                strict=True,
            )
            self.assertEqual(authority.exit_code, 0)

            neural = run_neural_life_core(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                authority_state_dir=authority_state,
                out_dir=neural_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="membrane-neural",
                strict=True,
            )
            self.assertEqual(neural.exit_code, 0)
            neural_check = run_check_neural_life_core(
                state_dir=neural_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(neural_check.exit_code, 0)

            state_store = run_state_store(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                neural_core_state_dir=neural_state,
                out_dir=state_root,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="membrane-state",
                strict=True,
            )
            self.assertEqual(state_store.exit_code, 0)
            state_check = run_check_state_store(
                state_dir=state_root,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(state_check.exit_code, 0)

            result = run_life_membrane(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                neural_core_state_dir=neural_state,
                state_dir=state_root,
                out_dir=membrane_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="membrane-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_life_membrane(
                membrane_dir=membrane_state,
                state_dir=state_root,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            membrane = self._read_json(membrane_state / "life_membrane.json")
            gate_decision = self._read_json(membrane_state / "membrane_gate_decision.json")
            direction_boundary = self._read_json(membrane_state / "direction_boundary_lock.json")
            quarantine = self._read_json(membrane_state / "quarantine_policy_seed.json")
            dream_fact = self._read_json(membrane_state / "dream_fact_boundary.json")
            relationship = self._read_json(membrane_state / "relationship_subject_boundary.json")
            responsibility = self._read_json(membrane_state / "responsibility_repair_boundary.json")
            shadow_action = self._read_json(membrane_state / "shadow_action_gate.json")
            precheck = self._read_json(membrane_state / "birth_readiness_precheck.json")
            coverage = self._read_json(membrane_state / "membrane_doc_coverage_snapshot.json")
            preflight = self._read_json(membrane_state / "first_activation_preflight_seed.json")
            manifest = self._read_json(membrane_state / "life_membrane_manifest.json")
            action_candidate_set = self._read_json(state_root / "action" / "action_candidate_set.json")
            go_nogo = self._read_json(state_root / "action" / "go_nogo_state.json")
            world_contact = self._read_json(state_root / "action" / "world_contact_gate_state.json")
            side_effect_review = self._read_json(state_root / "action" / "side_effect_review.json")
            report = self._read_json(reports / "life_membrane_report.json")
            check_report = self._read_json(reports / "life_membrane_check_report.json")
            digest = self._read_json(reports / "life_membrane_digest.json")
            receipt = self._read_json(receipts / "life_membrane_membrane-test.json")

        self.assertEqual(membrane["schema_version"], "life_membrane_v0")
        self.assertEqual(membrane["active_engineering_slice"], "S03_DIRECTION_LIFE_MEMBRANE")
        self.assertEqual(set(membrane["life_target_membrane"]), set(LIFE_TARGETS))
        self.assertEqual(membrane["stage_policy"], "pre_activation_shadow_only")
        self.assertIn("life_membrane_gate", membrane["gate_chain"])
        self.assertIn("birth_readiness_gate", membrane["gate_chain"])

        self.assertEqual(gate_decision["schema_version"], "membrane_gate_decision_v0")
        self.assertEqual(gate_decision["decision"], "closed")
        self.assertEqual(gate_decision["stage_effect"], "allow_next_slice")
        self.assertEqual(gate_decision["next_required_command"], "life-v0 check-birth-readiness --strict")

        self.assertEqual(direction_boundary["direction_lock"], "build_real_digital_life")
        self.assertIn("score_based_birth_readiness", direction_boundary["blocked_regressions"])
        self.assertIn("task_scheduler_subject", direction_boundary["blocked_regressions"])

        self.assertEqual(quarantine["schema_version"], "quarantine_policy_seed_v0")
        self.assertIn("dream_fact_pollution", quarantine["quarantine_channels"])
        self.assertIn("relationship_subject_break", quarantine["quarantine_channels"])

        self.assertEqual(dream_fact["schema_version"], "dream_fact_boundary_v0")
        self.assertEqual(dream_fact["fact_gate"], "DreamFactGate")
        self.assertFalse(dream_fact["dream_to_reality_direct_write_allowed"])

        self.assertEqual(relationship["schema_version"], "relationship_subject_boundary_v0")
        self.assertEqual(relationship["relation_role"], "relationship_subject")
        self.assertIn("friend", relationship["relation_kinds"])

        self.assertEqual(responsibility["schema_version"], "responsibility_repair_boundary_v0")
        self.assertIn("repair_obligation", responsibility["required_links"])
        self.assertIn("counterfactual_replay", responsibility["required_links"])

        self.assertEqual(shadow_action["schema_version"], "shadow_action_gate_v0")
        self.assertFalse(shadow_action["external_irreversible_action_allowed"])
        self.assertIn("ActionIntent", shadow_action["allowed_shadow_objects"])

        self.assertEqual(precheck["schema_version"], "birth_readiness_precheck_v0")
        self.assertEqual(set(precheck["life_target_status"]), set(LIFE_TARGETS))
        self.assertTrue(all(status == "membrane_closed" for status in precheck["life_target_status"].values()))

        self.assertEqual(coverage["schema_version"], "membrane_doc_coverage_snapshot_v0")
        self.assertGreaterEqual(coverage["doc_count"], 75)
        self.assertTrue(all(item["carrier_closed"] for item in coverage["coverage"]))

        self.assertEqual(preflight["schema_version"], "first_activation_preflight_seed_v0")
        self.assertEqual(preflight["activation_mode"], "shadow_only")
        self.assertIn("state_root_check", preflight["preflight_checks"])

        self.assertEqual(action_candidate_set["schema_version"], "action_candidate_set_v0")
        self.assertTrue(action_candidate_set["candidate_actions"])
        self.assertIn("runtime/state/action/world_contact_gate_state.json", action_candidate_set["action_state_refs"])
        self.assertTrue(action_candidate_set["responsibility_projection"])
        self.assertTrue(action_candidate_set["side_effect_projection"])

        self.assertEqual(go_nogo["schema_version"], "go_nogo_decision_v0")
        self.assertEqual(go_nogo["action_candidate_set_ref"], "runtime/state/action/action_candidate_set.json")
        self.assertTrue(go_nogo["responsibility_gate_refs"])
        self.assertTrue(go_nogo["fatigue_inhibition_refs"])

        self.assertEqual(world_contact["schema_version"], "world_contact_gate_state_v0")
        self.assertEqual(world_contact["contact_mode"], "shadow_only")
        self.assertIn("external_irreversible_action", world_contact["blocked_contacts"])
        self.assertTrue(world_contact["allowed_contacts"])

        self.assertEqual(side_effect_review["schema_version"], "side_effect_review_v0")
        self.assertEqual(
            side_effect_review["world_contact_gate_ref"],
            "runtime/state/action/world_contact_gate_state.json",
        )
        self.assertTrue(side_effect_review["archive_effects"])
        self.assertTrue(side_effect_review["responsibility_effects"])

        self.assertEqual(manifest["schema_version"], "life_membrane_manifest_v0")
        self.assertIn("runtime/state/membrane/life_membrane.json", manifest["state_refs"])
        self.assertIn("runtime/state/action/action_candidate_set.json", manifest["state_refs"])
        self.assertIn("runtime/state/action/world_contact_gate_state.json", manifest["state_refs"])

        self.assertEqual(report["schema_version"], "life_membrane_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertEqual(report["engineering_slice_ref"], "S03_DIRECTION_LIFE_MEMBRANE")
        self.assertEqual(report["next_allowed_slices"], ["S08_LIFE_TARGET_RUNTIMES"])
        self.assertEqual(report["next_required_command"], "life-v0 check-birth-readiness --strict")
        self.assertIn("LifeMembraneStageGate", report["runtime_carrier_refs"])

        self.assertEqual(check_report["schema_version"], "life_membrane_check_report_v0")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(digest["current_slice"], "S03_DIRECTION_LIFE_MEMBRANE")
        self.assertEqual(receipt["schema_version"], "life_membrane_receipt_v0")

    def test_cli_build_life_membrane_returns_zero_and_writes_check_report(self):
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

            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(doc_out), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "membrane-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--out", str(direction_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "membrane-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--direction", str(direction_state), "--out", str(authority_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "membrane-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--authority", str(authority_state), "--out", str(neural_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "membrane-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(neural_state), "--reports", str(reports), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--neural-core", str(neural_state), "--out", str(state_root), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "membrane-cli-state", "--strict"],
                ["check-state-store", "--state", str(state_root), "--reports", str(reports), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(doc_out / "doc_carrier_index.json"), "--direction", str(direction_state), "--neural-core", str(neural_state), "--state", str(state_root), "--out", str(membrane_state), "--reports", str(reports), "--receipts", str(receipts), "--run-id", "membrane-cli", "--strict"],
                ["check-life-membrane", "--membrane", str(membrane_state), "--state", str(state_root), "--reports", str(reports), "--strict"],
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

            report = self._read_json(reports / "life_membrane_report.json")
            check_report = self._read_json(reports / "life_membrane_check_report.json")

        self.assertEqual(report["run_id"], "membrane-cli")
        self.assertEqual(report["next_required_command"], "life-v0 check-birth-readiness --strict")
        self.assertEqual(check_report["status"], "closed")

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
