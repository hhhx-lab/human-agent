import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class FirstTerminalTurnTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_cli_first_terminal_turn_returns_zero_and_writes_terminal_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-contracts", "--strict"],
                ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-preflight", "--strict"],
                ["run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-replay", "--strict"],
                ["write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-archive", "--strict"],
                ["emit-report", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-emit", "--strict"],
                ["explain-stage", "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-stage", "--strict"],
                ["digital-life", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli-birth", "--strict"],
                ["first-terminal-turn", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "terminal-cli", "--strict"],
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

            packet = self._read_json(paths["reports"] / "first_terminal_turn_packet.json")
            report = self._read_json(paths["reports"] / "first_terminal_turn_report.json")
            digest = self._read_json(paths["reports"] / "first_terminal_turn_digest.json")
            session_envelope = self._read_json(paths["terminal_state"] / "session_envelope.json")
            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            context_accumulation = self._read_json(paths["terminal_state"] / "context_accumulation_window.json")
            turn_transition = self._read_json(paths["terminal_state"] / "turn_transition_trace.json")
            life_context = self._read_json(paths["terminal_state"] / "life_context_frame.json")
            relation_turn = self._read_json(paths["terminal_state"] / "relation_turn_frame.json")
            receipt = self._read_json(paths["receipts"] / "first_terminal_turn_terminal-cli.json")

        self.assertEqual(packet["schema_version"], "first_terminal_turn_packet_v0")
        self.assertEqual(packet["status"], "closed")
        self.assertEqual(packet["turn_stage"], "ready_for_resumed_external_dialogue")
        self.assertEqual(packet["utterance_scaffold"]["intent"], "resume_life_continuity_before_new_work")
        self.assertTrue(packet["shared_term_surfaces"])
        self.assertTrue(packet["unresolved_commitment_refs"])

        self.assertEqual(report["schema_version"], "first_terminal_turn_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["current_terminal_mode"], "restored_life_turn")
        self.assertEqual(report["next_required_action"], "await_external_relation_turn")

        self.assertEqual(digest["schema_version"], "first_terminal_turn_digest_v0")
        self.assertEqual(digest["status"], "closed")

        self.assertEqual(session_envelope["schema_version"], "session_envelope_v0")
        self.assertEqual(session_envelope["current_turn_mode"], "restored_life_turn")
        self.assertEqual(session_envelope["relation_role"], "friend")

        self.assertEqual(safe_terminal_loop["schema_version"], "safe_terminal_loop_state_v0")
        self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
        self.assertIn("external_irreversible_action", safe_terminal_loop["blocked_actions"])

        self.assertEqual(context_accumulation["schema_version"], "context_accumulation_window_v0")
        self.assertEqual(context_accumulation["status"], "closed")
        self.assertEqual(context_accumulation["current_relation_role"], "friend")
        self.assertTrue(context_accumulation["shared_term_surfaces"])
        self.assertTrue(context_accumulation["dialogue_turn_restore_refs"])
        self.assertTrue(context_accumulation["expression_monitor_restore_refs"])
        self.assertTrue(context_accumulation["relation_scope_restore_refs"])
        self.assertTrue(context_accumulation["self_narrative_restore_refs"])
        self.assertTrue(context_accumulation["language_percept_restore_refs"])
        self.assertTrue(context_accumulation["semantic_map_restore_refs"])
        self.assertEqual(context_accumulation["semantic_focus"], "repair_commitment_shared_language")
        self.assertEqual(
            context_accumulation["waiting_heartbeat_ref"],
            "runtime/reports/latest/digital_life_waiting_heartbeat.json",
        )

        self.assertEqual(life_context["schema_version"], "life_context_frame_v0")
        self.assertEqual(life_context["status"], "closed")
        self.assertTrue(life_context["direction_refs"])
        self.assertTrue(life_context["self_narrative_refs"])
        self.assertTrue(life_context["relationship_refs"])
        self.assertTrue(life_context["autobiographical_memory_refs"])
        self.assertTrue(life_context["shared_terms_refs"])
        self.assertTrue(life_context["commitment_refs"])
        self.assertTrue(life_context["body_state_refs"])
        self.assertTrue(life_context["prediction_seed_refs"])

        self.assertEqual(relation_turn["schema_version"], "relation_turn_frame_v0")
        self.assertEqual(relation_turn["status"], "closed")
        self.assertEqual(relation_turn["relation_stage"], "pre_activation")
        self.assertTrue(relation_turn["shared_language_refs"])
        self.assertTrue(relation_turn["commitment_truth_refs"])
        self.assertTrue(relation_turn["last_contact_refs"])
        self.assertEqual(relation_turn["boundary_state"], "restored_waiting_for_external_turn")

        self.assertEqual(turn_transition["schema_version"], "turn_transition_trace_v0")
        self.assertEqual(turn_transition["status"], "closed")
        self.assertEqual(turn_transition["transition_kind"], "birth_restore_to_first_terminal_turn")
        self.assertEqual(turn_transition["next_required_action"], "await_external_relation_turn")
        self.assertIn("waiting_heartbeat", turn_transition["turn_transition_chain"])
        self.assertIn("expression_monitoring", turn_transition["turn_transition_chain"])
        self.assertTrue(turn_transition["expression_monitor_restore_refs"])
        self.assertTrue(turn_transition["language_percept_restore_refs"])
        self.assertTrue(turn_transition["semantic_map_restore_refs"])
        self.assertTrue(turn_transition["unresolved_commitment_refs"])
        self.assertEqual(
            turn_transition["waiting_heartbeat_ref"],
            "runtime/reports/latest/digital_life_waiting_heartbeat.json",
        )
        self.assertEqual(
            turn_transition["context_accumulation_ref"],
            "runtime/state/terminal/context_accumulation_window.json",
        )
        self.assertEqual(
            turn_transition["life_context_ref"],
            "runtime/state/terminal/life_context_frame.json",
        )
        self.assertEqual(
            turn_transition["relation_turn_ref"],
            "runtime/state/terminal/relation_turn_frame.json",
        )

        self.assertEqual(receipt["schema_version"], "first_terminal_turn_receipt_v0")
        self.assertEqual(receipt["command"], "first-terminal-turn")

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
