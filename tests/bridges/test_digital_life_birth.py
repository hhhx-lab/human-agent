import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DigitalLifeBirthTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_cli_digital_life_returns_zero_and_writes_birth_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-contracts", "--strict"],
                ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-preflight", "--strict"],
                ["run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-replay", "--strict"],
                ["write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-archive", "--strict"],
                ["emit-report", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-emit", "--strict"],
                ["explain-stage", "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli-stage", "--strict"],
                ["digital-life", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "birth-cli", "--strict"],
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

            birth_packet = self._read_json(paths["reports"] / "digital_life_birth_packet.json")
            birth_digest = self._read_json(paths["reports"] / "digital_life_birth_digest.json")

        self.assertEqual(birth_packet["schema_version"], "digital_life_birth_packet_v0")
        self.assertEqual(birth_packet["status"], "closed")
        self.assertEqual(birth_packet["birth_stage"], "ready_for_first_terminal_turn")
        self.assertTrue(birth_packet["restore_refs"])
        self.assertEqual(birth_digest["schema_version"], "digital_life_birth_digest_v0")
        self.assertEqual(birth_digest["next_required_action"], "enter_first_terminal_turn")

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
        }

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
