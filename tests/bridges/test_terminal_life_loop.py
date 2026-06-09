import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TerminalLifeLoopTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_cli_terminal_life_loop_returns_zero_and_writes_loop_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-contracts", "--strict"],
                ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-preflight", "--strict"],
                ["run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-replay", "--strict"],
                ["write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-archive", "--strict"],
                ["emit-report", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-emit", "--strict"],
                ["explain-stage", "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-stage", "--strict"],
                ["digital-life", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-birth", "--strict"],
                ["first-terminal-turn", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli-turn", "--strict"],
                ["terminal-life-loop", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "loop-cli", "--strict"],
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

            loop_packet = self._read_json(paths["reports"] / "terminal_life_loop_packet.json")
            loop_report = self._read_json(paths["reports"] / "terminal_life_loop_report.json")
            loop_digest = self._read_json(paths["reports"] / "terminal_life_loop_digest.json")
            dialogue_packet = self._read_json(paths["reports"] / "resumed_external_dialogue_packet.json")
            loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            context_accumulation = self._read_json(paths["terminal_state"] / "context_accumulation_window.json")
            turn_transition = self._read_json(paths["terminal_state"] / "turn_transition_trace.json")
            dialogue_writeback = self._read_json(paths["reports"] / "dialogue_writeback_bundle.json")
            receipt = self._read_json(paths["receipts"] / "terminal_life_loop_loop-cli.json")

        self.assertEqual(loop_packet["schema_version"], "terminal_life_loop_packet_v0")
        self.assertEqual(loop_packet["status"], "closed")
        self.assertEqual(loop_packet["loop_stage"], "restored_loop_waiting_next_external_turn")
        self.assertEqual(loop_packet["next_required_action"], "await_next_external_relation_turn")

        self.assertEqual(loop_report["schema_version"], "terminal_life_loop_report_v0")
        self.assertEqual(loop_report["status"], "closed")
        self.assertEqual(loop_report["current_terminal_mode"], "resumed_external_dialogue_loop")
        self.assertEqual(loop_report["next_required_action"], "await_next_external_relation_turn")

        self.assertEqual(loop_digest["schema_version"], "terminal_life_loop_digest_v0")
        self.assertEqual(loop_digest["status"], "closed")

        self.assertEqual(dialogue_packet["schema_version"], "resumed_external_dialogue_packet_v0")
        self.assertEqual(dialogue_packet["status"], "closed")
        self.assertEqual(dialogue_packet["dialogue_mode"], "restored_relation_continuation")
        self.assertTrue(dialogue_packet["expression_monitor_restore_refs"])
        self.assertTrue(dialogue_packet["relation_scope_restore_refs"])
        self.assertTrue(dialogue_packet["self_narrative_restore_refs"])
        self.assertEqual(
            dialogue_packet["waiting_heartbeat_ref"],
            "runtime/reports/latest/digital_life_waiting_heartbeat.json",
        )
        self.assertEqual(
            dialogue_packet["context_accumulation_ref"],
            "runtime/state/terminal/context_accumulation_window.json",
        )
        self.assertEqual(
            dialogue_packet["turn_transition_ref"],
            "runtime/state/terminal/turn_transition_trace.json",
        )
        self.assertEqual(
            dialogue_packet["dialogue_writeback_bundle_ref"],
            "runtime/reports/latest/dialogue_writeback_bundle.json",
        )

        self.assertEqual(loop_state["schema_version"], "terminal_life_loop_state_v0")
        self.assertEqual(loop_state["current_mode"], "restored_waiting_for_external_turn")
        self.assertEqual(loop_state["last_turn_status"], "closed")
        self.assertEqual(
            loop_state["context_accumulation_ref"],
            "runtime/state/terminal/context_accumulation_window.json",
        )
        self.assertEqual(
            loop_state["turn_transition_ref"],
            "runtime/state/terminal/turn_transition_trace.json",
        )
        self.assertEqual(
            loop_state["dialogue_writeback_bundle_ref"],
            "runtime/reports/latest/dialogue_writeback_bundle.json",
        )

        self.assertEqual(safe_terminal_loop["schema_version"], "safe_terminal_loop_state_v0")
        self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
        self.assertEqual(safe_terminal_loop["last_completed_turn_mode"], "resumed_external_dialogue_loop")

        self.assertEqual(context_accumulation["schema_version"], "context_accumulation_window_v0")
        self.assertTrue(context_accumulation["language_percept_restore_refs"])
        self.assertTrue(context_accumulation["semantic_map_restore_refs"])
        self.assertEqual(context_accumulation["semantic_focus"], "repair_commitment_shared_language")
        self.assertEqual(
            context_accumulation["waiting_heartbeat_ref"],
            "runtime/reports/latest/digital_life_waiting_heartbeat.json",
        )
        self.assertEqual(turn_transition["schema_version"], "turn_transition_trace_v0")
        self.assertIn("waiting_heartbeat", turn_transition["turn_transition_chain"])
        self.assertTrue(turn_transition["language_percept_restore_refs"])
        self.assertTrue(turn_transition["semantic_map_restore_refs"])

        self.assertEqual(dialogue_writeback["schema_version"], "dialogue_writeback_bundle_v0")
        self.assertEqual(dialogue_writeback["status"], "closed")
        self.assertTrue(dialogue_writeback["dialogue_event_refs"])
        self.assertTrue(dialogue_writeback["self_narrative_writeback_refs"])
        self.assertTrue(dialogue_writeback["relationship_writeback_refs"])
        self.assertTrue(dialogue_writeback["commitment_writeback_refs"])
        self.assertTrue(dialogue_writeback["replay_cue_refs"])
        self.assertTrue(dialogue_writeback["terminal_state_refs"])

        self.assertEqual(receipt["schema_version"], "terminal_life_loop_receipt_v0")
        self.assertEqual(receipt["command"], "terminal-life-loop")

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
            "terminal_state": state_root / "terminal",
        }

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
