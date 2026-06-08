import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DirectionLockTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_direction_lock_writes_state_report_and_receipt(self):
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"

            ingest = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=doc_out,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="direction-test-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            result = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="direction-test",
                strict=True,
            )

            self.assertEqual(result.exit_code, 0)

            direction_lock = self._read_json(direction_state / "direction_lock.json")
            resume_chain = self._read_json(direction_state / "resume_anchor_chain.json")
            framework_boundary = self._read_json(direction_state / "framework_negative_boundary.json")
            slice_permission = self._read_json(direction_state / "slice_permission.json")
            report = self._read_json(reports / "direction_lock_report.json")
            digest = self._read_json(reports / "direction_digest.json")
            receipt = self._read_json(receipts / "direction_lock_direction-test.json")

        self.assertEqual(direction_lock["schema_version"], "direction_lock_v0")
        self.assertEqual(direction_lock["direction_statement"], "build_real_digital_life")
        self.assertEqual(direction_lock["active_engineering_slice"], "S00_DIRECTION_FOUNDATION")
        self.assertEqual(
            set(direction_lock["life_targets"]),
            {
                "real_consciousness",
                "real_emotion",
                "real_personality",
                "real_life",
                "real_pain",
                "real_dream",
                "real_relationship",
                "real_responsibility",
                "real_regret",
            },
        )
        self.assertIn("S01_SOURCE_AUTHORITY", direction_lock["next_allowed_slices"])

        anchor_ids = {anchor["anchor_id"] for anchor in resume_chain["anchors"]}
        self.assertEqual(
            {
                "origin_seed_chain",
                "brain_life_chain",
                "nine_life_target_chain",
                "language_relationship_chain",
                "pain_regret_responsibility_chain",
                "dream_offline_chain",
                "engineering_closure_chain",
            },
            anchor_ids,
        )
        self.assertIn("docs/v0/v0_implementation_index.md", resume_chain["resume_order"])
        self.assertIn("docs/v0/s00_direction_foundation_engineering_contract.md", resume_chain["resume_order"])

        self.assertEqual(framework_boundary["schema_version"], "framework_negative_boundary_v0")
        self.assertIn("ComputerPeripheralRuntime", framework_boundary["allowed_runtime_carriers"])
        self.assertIn("external_framework_subject_architecture", framework_boundary["prohibited_regressions"])

        self.assertEqual(slice_permission["next_allowed_slice"], "S01_SOURCE_AUTHORITY")
        self.assertEqual(slice_permission["stage_effect"], "allow_next_slice")

        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertEqual(report["blocked_gates"], [])
        self.assertIn("origin_seed_gate", report["closed_gates"])
        self.assertIn("full_corpus_coverage_gate", report["closed_gates"])
        self.assertEqual(digest["current_slice"], "S00_DIRECTION_FOUNDATION")
        self.assertEqual(receipt["schema_version"], "direction_lock_receipt_v0")

    def test_cli_build_direction_lock_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"

            ingest = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0",
                    "ingest-docs",
                    "--docs",
                    str(self.docs_dir),
                    "--out",
                    str(doc_out),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "direction-cli-ingest",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(ingest.returncode, 0, ingest.stderr)

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0",
                    "build-direction-lock",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--out",
                    str(direction_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "direction-cli",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = self._read_json(reports / "direction_lock_report.json")

        self.assertEqual(report["run_id"], "direction-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-source-authority --strict")

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
