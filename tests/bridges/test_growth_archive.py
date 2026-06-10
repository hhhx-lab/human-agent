import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GrowthArchiveTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_write_growth_archive_writes_archive_bundle(self):
        from life_v0.activation import run_first_activation_preflight
        from life_v0.archive import run_write_growth_archive
        from life_v0.authority import run_source_authority
        from life_v0.body import run_check_life_support, run_life_support
        from life_v0.contracts import run_check_v0_contracts
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.growth import run_cycle
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.replay import run_replay_shadow
        from life_v0.schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
        from life_v0.state_store import run_check_state_store, run_state_store
        from life_v0.validators import run_check_validation_membrane, run_validation_membrane

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            self._run_pre_growth_archive_chain(
                paths=paths,
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
                run_cycle=run_cycle,
                run_check_v0_contracts=run_check_v0_contracts,
                run_first_activation_preflight=run_first_activation_preflight,
                run_replay_shadow=run_replay_shadow,
            )

            result = run_write_growth_archive(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="growth-archive-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            batch = self._read_json(paths["archive_state"] / "growth_archive_receipt_batch.json")
            preconditions = self._read_json(paths["archive_state"] / "shadow_run_preconditions.json")
            handoff = self._read_json(paths["archive_state"] / "growth_archive_to_shadow_handoff.json")
            archive_graph = self._read_json(paths["archive_state"] / "reconsolidation_archive_graph.json")
            report = self._read_json(paths["reports"] / "growth_archive_report.json")
            digest = self._read_json(paths["reports"] / "growth_archive_digest.json")
            stage_gate = self._read_json(paths["reports"] / "growth_archive_stage_gate.json")
            receipt = self._read_json(paths["receipts"] / "write_growth_archive_growth-archive-test.json")
            history_path = paths["runtime_root"] / "archive" / "growth_archive_events.jsonl"
            history_lines = history_path.read_text(encoding="utf-8").strip().splitlines()
            archive_event = json.loads(history_lines[-1])
            life_state = self._read_json(paths["state_root"] / "life_state.json")

        self.assertEqual(batch["schema_version"], "growth_archive_receipt_batch_v0")
        self.assertEqual(batch["status"], "closed")
        self.assertTrue(batch["growth_patch_receipt_refs"])
        self.assertTrue(batch["language_action_archive_receipt_refs"])
        self.assertTrue(batch["shadow_run_seed_archive_receipt_refs"])
        self.assertTrue(batch["responsibility_archive_receipt_refs"])
        self.assertEqual(batch["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(batch["repair_followup_required"])
        self.assertTrue(batch["repair_obligation_refs"])
        self.assertEqual(
            batch["queue_e_repair_modulation_profile"]["schema_version"],
            "queue_e_repair_modulation_profile_v0",
        )
        self.assertEqual(batch["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(batch["queue_e_repair_attention_target"], "regret_pressure")
        self.assertIn(
            "runtime/reports/latest/pain_regret_repair_report.json",
            batch["queue_e_repair_ref_set"],
        )

        self.assertEqual(preconditions["schema_version"], "shadow_run_preconditions_v0")
        self.assertEqual(preconditions["status"], "closed")
        self.assertTrue(preconditions["preconditions_ready"])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", preconditions["required_refs"])
        self.assertIn("runtime/reports/latest/pain_regret_repair_report.json", preconditions["required_refs"])

        self.assertEqual(handoff["schema_version"], "growth_archive_to_shadow_handoff_v0")
        self.assertEqual(handoff["status"], "closed")
        self.assertTrue(handoff["shadow_run_handoff_ready"])
        self.assertTrue(handoff["responsibility_archive_receipt_refs"])
        self.assertEqual(handoff["world_contact_release_posture"], "shadow_only_guarded")
        self.assertTrue(handoff["repair_followup_required"])
        self.assertEqual(handoff["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(handoff["queue_e_repair_attention_target"], "regret_pressure")
        self.assertIn(
            "runtime/state/action/responsibility_loop_state.json",
            handoff["queue_e_repair_ref_set"],
        )

        self.assertEqual(archive_graph["schema_version"], "reconsolidation_archive_graph_v0")
        self.assertEqual(archive_graph["status"], "closed")
        self.assertTrue(archive_graph["archive_edges"])
        self.assertIn(
            {"source": "pain_regret_repair_report", "target": "growth_archive_report", "edge_kind": "repair_to_archive"},
            archive_graph["archive_edges"],
        )

        self.assertEqual(report["schema_version"], "growth_archive_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S10_RUNTIME_GROWTH_RECONSOLIDATION")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "archive_written")
        self.assertEqual(report["next_required_command"], "life-v0 emit-report --strict")
        self.assertIn("B30_RECONSOLIDATION_REPLAY_GROWTH", report["readme_block_refs"])
        self.assertEqual(report["queue_e_state_refs"][0], "runtime/state/action/responsibility_loop_state.json")
        self.assertEqual(report["queue_e_report_refs"], ["runtime/reports/latest/pain_regret_repair_report.json"])
        self.assertEqual(report["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(report["queue_e_repair_attention_target"], "regret_pressure")

        self.assertEqual(digest["schema_version"], "growth_archive_digest_v0")
        self.assertEqual(digest["current_phase"], "growth_archive")
        self.assertEqual(digest["status"], "closed")
        self.assertEqual(digest["queue_e_ref_count"], 3)
        self.assertEqual(digest["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(digest["queue_e_repair_attention_target"], "regret_pressure")
        self.assertGreaterEqual(digest["queue_e_repair_ref_count"], 3)

        self.assertEqual(stage_gate["schema_version"], "growth_archive_stage_gate_v0")
        self.assertEqual(stage_gate["decision"], "closed")
        self.assertEqual(stage_gate["next_required_command"], "life-v0 emit-report --strict")
        self.assertEqual(stage_gate["gates"]["responsibility_archive_gate"], "closed")

        self.assertEqual(receipt["schema_version"], "write_growth_archive_receipt_v0")
        self.assertEqual(receipt["command"], "write-growth-archive")
        self.assertGreaterEqual(len(history_lines), 1)
        self.assertEqual(archive_event["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(archive_event["queue_e_repair_attention_target"], "regret_pressure")
        self.assertTrue(life_state["archive_refs"])
        self.assertIn("runtime/archive/growth_archive_events.jsonl", life_state["archive_refs"])
        self.assertEqual(life_state["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(life_state["queue_e_repair_attention_target"], "regret_pressure")

    def test_cli_write_growth_archive_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-contracts", "--strict"],
                ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-preflight", "--strict"],
                ["run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli-replay", "--strict"],
                ["write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "archive-cli", "--strict"],
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

            report = self._read_json(paths["reports"] / "growth_archive_report.json")
            digest = self._read_json(paths["reports"] / "growth_archive_digest.json")
            stage_gate = self._read_json(paths["reports"] / "growth_archive_stage_gate.json")
            batch = self._read_json(paths["archive_state"] / "growth_archive_receipt_batch.json")

        self.assertEqual(report["run_id"], "archive-cli")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["next_required_command"], "life-v0 emit-report --strict")
        self.assertEqual(digest["current_phase"], "growth_archive")
        self.assertEqual(stage_gate["decision"], "closed")
        self.assertEqual(batch["status"], "closed")
        self.assertEqual(report["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(digest["queue_e_repair_attention_target"], "regret_pressure")
        self.assertEqual(batch["queue_e_repair_pressure_level"], "elevated")

    def _runtime_paths(self, tmp_path: Path) -> dict[str, Path]:
        state_root = tmp_path / "runtime" / "state"
        runtime_root = tmp_path / "runtime"
        return {
            "runtime_root": runtime_root,
            "doc_out": runtime_root / "docs",
            "reports": runtime_root / "reports" / "latest",
            "receipts": runtime_root / "receipts",
            "direction_state": state_root / "direction",
            "authority_state": state_root / "authority",
            "neural_state": state_root / "neural_life_core",
            "state_root": state_root,
            "membrane_state": state_root / "membrane",
            "life_targets_state": state_root / "life_targets",
            "validation_state": state_root / "validation",
            "observation_state": state_root / "observation",
            "schema_runner_state": state_root / "schema_runner",
            "archive_state": state_root / "archive",
        }

    def _run_pre_growth_archive_chain(self, *, paths, **kwargs):
        from tests.bridges.test_replay_shadow import ReplayShadowTests

        helper = ReplayShadowTests()
        helper._run_pre_replay_shadow_chain(paths=paths, **kwargs)

        replay = kwargs["run_replay_shadow"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="archive-replay",
            strict=True,
        )
        self.assertEqual(replay.exit_code, 0)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
