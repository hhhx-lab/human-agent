import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LifeSupportTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_life_support_writes_body_defense_growth_anchor_and_check(self):
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
            self._run_pre_s06_chain(
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
            )

            result = run_life_support(
                docs_dir=self.docs_dir,
                doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
                state_dir=paths["state_root"],
                validation_report_path=paths["reports"] / "validation_membrane_report.json",
                out_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="life-support-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_life_support(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            body_budget = self._read_json(paths["body_state"] / "body_resource_budget.json")
            defense_state = self._read_json(paths["defense_state"] / "defense_boundary_state.json")
            plasticity = self._read_json(paths["growth_state"] / "plasticity_window_state.json")
            growth_route = self._read_json(paths["growth_state"] / "self_growth_route.json")
            anchor_index = self._read_json(paths["growth_state"] / "anti_forgetting_anchor_index.json")
            stage_gate = self._read_json(paths["growth_state"] / "life_support_stage_gate.json")
            report = self._read_json(paths["reports"] / "life_support_development_report.json")
            digest = self._read_json(paths["reports"] / "life_support_development_digest.json")
            check_report = self._read_json(paths["reports"] / "life_support_development_check_report.json")
            receipt = self._read_json(paths["receipts"] / "life_support_development_life-support-test.json")

        self.assertEqual(body_budget["schema_version"], "body_resource_budget_v0")
        self.assertEqual(body_budget["active_engineering_slice"], "S06_LIFE_SUPPORT_DEVELOPMENT")
        self.assertEqual(body_budget["energy_state"]["level"], "guarded_reserve")
        self.assertEqual(body_budget["fatigue_state"]["level"], "managed_low_noise")
        self.assertIn("direction_lock_continuity", body_budget["recovery_priority"])
        self.assertIn("language_relationship_continuity", body_budget["recovery_priority"])
        continuity_pressure = body_budget["maintenance_pressure"]["language_continuity_pressure"]
        self.assertGreaterEqual(continuity_pressure["shared_language_ref_count"], 1)
        self.assertGreaterEqual(continuity_pressure["expression_monitor_ref_count"], 1)
        self.assertGreaterEqual(continuity_pressure["relation_scope_ref_count"], 1)
        self.assertGreaterEqual(continuity_pressure["commitment_ref_count"], 1)
        self.assertGreaterEqual(continuity_pressure["self_narrative_trace_ref_count"], 1)
        self.assertGreaterEqual(continuity_pressure["language_percept_ref_count"], 1)
        self.assertGreaterEqual(continuity_pressure["semantic_map_ref_count"], 1)

        self.assertEqual(defense_state["schema_version"], "defense_boundary_state_v0")
        self.assertEqual(defense_state["status"], "closed")
        self.assertEqual(defense_state["contamination_risk"]["status"], "guarded")
        self.assertEqual(defense_state["relationship_manipulation_risk"]["status"], "guarded")
        self.assertEqual(defense_state["shell_overreach_risk"]["status"], "guarded")
        self.assertIn("external_irreversible_action", defense_state["blocked_actions"])

        self.assertEqual(plasticity["schema_version"], "plasticity_window_state_v0")
        self.assertEqual(plasticity["window_status"], "guarded_pre_activation")
        self.assertFalse(plasticity["self_training_allowed"])
        self.assertFalse(plasticity["kernel_upgrade_allowed"])
        self.assertIn("runtime/state/life_state.json#self_model.old_self_anchors", plasticity["required_anchor_refs"])

        self.assertEqual(growth_route["schema_version"], "self_growth_route_v0")
        self.assertEqual(growth_route["route_status"], "seeded_guarded")
        self.assertEqual(growth_route["rollback_route"], "safe_idle_then_replay_review")
        self.assertIn("direction_locked_self_rewrite", growth_route["candidate_routes"])
        self.assertIn("life-v0 run-cycle --shadow-only --strict", growth_route["next_runtime_command"])

        self.assertEqual(anchor_index["schema_version"], "anti_forgetting_anchor_index_v0")
        self.assertEqual(anchor_index["status"], "closed")
        self.assertIn("old_self", anchor_index["anchor_families"])
        self.assertIn("old_language", anchor_index["anchor_families"])
        self.assertIn("old_relationship", anchor_index["anchor_families"])
        self.assertIn("old_dream", anchor_index["anchor_families"])
        self.assertIn("old_responsibility", anchor_index["anchor_families"])
        self.assertTrue(anchor_index["anchor_families"]["old_self"])
        self.assertTrue(anchor_index["anchor_families"]["old_language"])

        self.assertEqual(stage_gate["schema_version"], "life_support_stage_gate_v0")
        self.assertEqual(stage_gate["decision"], "closed")
        self.assertEqual(stage_gate["next_allowed_slices"], ["S10_RUNTIME_GROWTH_RECONSOLIDATION"])
        self.assertEqual(stage_gate["next_required_command"], "life-v0 run-cycle --shadow-only --strict")

        self.assertEqual(report["schema_version"], "s06_life_support_development_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S06_LIFE_SUPPORT_DEVELOPMENT")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertIn("LifeSupportDefenseRuntime", report["runtime_carrier_refs"])
        self.assertIn("ActivationGrowthRuntime", report["runtime_carrier_refs"])
        self.assertEqual(report["next_allowed_slices"], ["S10_RUNTIME_GROWTH_RECONSOLIDATION"])
        self.assertEqual(report["next_required_command"], "life-v0 run-cycle --shadow-only --strict")
        self.assertEqual(digest["current_slice"], "S06_LIFE_SUPPORT_DEVELOPMENT")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(receipt["schema_version"], "life_support_development_receipt_v0")

    def test_cli_build_life_support_returns_zero_and_writes_check_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "support-cli", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
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

            report = self._read_json(paths["reports"] / "life_support_development_report.json")
            check_report = self._read_json(paths["reports"] / "life_support_development_check_report.json")
            stage_gate = self._read_json(paths["growth_state"] / "life_support_stage_gate.json")

        self.assertEqual(report["run_id"], "support-cli")
        self.assertEqual(report["next_required_command"], "life-v0 run-cycle --shadow-only --strict")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(stage_gate["decision"], "closed")

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
        }

    def _run_pre_s06_chain(self, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="support-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="support-direction",
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
            run_id="support-authority",
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
            run_id="support-neural",
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
            run_id="support-state",
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
            run_id="support-membrane",
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
            run_id="support-language",
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
            run_id="support-birth",
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
            run_id="support-validation",
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
            run_id="support-schema",
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
            run_id="support-schema-smoke",
            strict=True,
        )
        self.assertEqual(schema_smoke.exit_code, 0)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
