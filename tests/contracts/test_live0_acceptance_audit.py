import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from life_v0.live0_audit import run_live0_acceptance_audit


class Live0AcceptanceAuditTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_live0_acceptance_audit_closes_all_seven_criteria(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state = runtime_root / "state"
            reports = runtime_root / "reports" / "latest"
            receipts = runtime_root / "receipts"
            self._write_live0_fixture(runtime_root)

            result = run_live0_acceptance_audit(
                docs_dir=self.docs_dir,
                state_dir=state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="live0-audit-test",
                strict=True,
            )

            report = self._read_json(reports / "live0_acceptance_audit_report.json")
            digest = self._read_json(reports / "live0_acceptance_audit_digest.json")
            receipt = self._read_json(
                receipts / "live0_acceptance_audit_live0-audit-test.json"
            )

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(report["schema_version"], "live0_acceptance_audit_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertTrue(report["live0_acceptance_closed"])
        self.assertEqual(report["summary"]["criteria_total"], 7)
        self.assertEqual(report["summary"]["criteria_closed"], 7)
        self.assertEqual(report["summary"]["failed_criteria"], [])
        self.assertEqual(report["next_required_action"], "live0_v0_closure_allowed")
        self.assertIn(
            "runtime/state/schema_runner/run_manifest.json",
            report["evidence_refs"],
        )
        relationship_criterion = self._criterion(
            report, "f_equal_relationship_dialogue_growth"
        )
        self.assertTrue(
            any(
                probe["probe_id"] == "queue_e_world_contact_repair_hold_validated"
                and probe["status"] == "passed"
                for probe in relationship_criterion["probes"]
            )
        )
        mechanism_criterion = self._criterion(
            report, "g_initial_life_mechanism_coverage"
        )
        language_criterion = self._criterion(
            report, "b_conscious_emotion_thought_language"
        )
        self.assertTrue(
            any(
                probe["probe_id"] == "resident_proactive_terminal_voice_audited"
                and probe["status"] == "passed"
                for probe in language_criterion["probes"]
            )
        )
        self.assertTrue(
            any(
                probe["probe_id"]
                == "queue_e_world_contact_repair_hold_schema_handoff"
                and probe["status"] == "passed"
                for probe in mechanism_criterion["probes"]
            )
        )
        self.assertEqual(digest["status"], "closed")
        self.assertEqual(receipt["schema_version"], "live0_acceptance_audit_receipt_v0")
        self.assertIn(
            "runtime/reports/latest/live0_acceptance_audit_report.json",
            receipt["report_refs"],
        )

    def test_live0_acceptance_audit_blocks_without_direct_name_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state = runtime_root / "state"
            reports = runtime_root / "reports" / "latest"
            receipts = runtime_root / "receipts"
            self._write_live0_fixture(runtime_root)
            (state / "identity" / "life_name_command_manifest.json").unlink()

            result = run_live0_acceptance_audit(
                docs_dir=self.docs_dir,
                state_dir=state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="live0-audit-missing-name-command",
                strict=True,
            )

            report = self._read_json(reports / "live0_acceptance_audit_report.json")

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report["status"], "blocked")
        self.assertIn(
            "a_terminal_wake_and_named_residency",
            report["summary"]["failed_criteria"],
        )
        self.assertTrue(
            any("direct_life_name_command_bound" in reason for reason in report["blocked_reasons"])
        )

    def test_live0_acceptance_audit_blocks_when_direct_name_command_file_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state = runtime_root / "state"
            reports = runtime_root / "reports" / "latest"
            receipts = runtime_root / "receipts"
            self._write_live0_fixture(runtime_root)
            manifest = self._read_json(
                state / "identity" / "life_name_command_manifest.json"
            )
            Path(manifest["command_path"]).unlink()

            result = run_live0_acceptance_audit(
                docs_dir=self.docs_dir,
                state_dir=state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="live0-audit-missing-name-command-file",
                strict=True,
            )

            report = self._read_json(reports / "live0_acceptance_audit_report.json")

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report["status"], "blocked")
        self.assertIn(
            "a_terminal_wake_and_named_residency",
            report["summary"]["failed_criteria"],
        )
        self.assertTrue(
            any(
                "direct_life_name_command_bound" in reason
                for reason in report["blocked_reasons"]
            )
        )

    def test_live0_acceptance_audit_blocks_without_queue_e_world_contact_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state = runtime_root / "state"
            reports = runtime_root / "reports" / "latest"
            receipts = runtime_root / "receipts"
            self._write_live0_fixture(runtime_root)
            self._write_json_ref(
                runtime_root,
                "runtime/state/schema_runner/run_manifest.json",
                {
                    "schema_version": "schema_runner_run_manifest_v0",
                    "run_status": "closed",
                    "queue_e_world_contact_repair_hold_required": False,
                    "queue_e_world_contact_confirmation_threshold_bias": "baseline",
                    "queue_e_world_contact_future_no_go_profile_ref": "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                    "queue_e_world_contact_blocked_future_routes": [],
                    "queue_e_world_contact_allowed_repair_routes": [],
                    "queue_e_world_contact_repair_governance_refs": [],
                },
            )

            result = run_live0_acceptance_audit(
                docs_dir=self.docs_dir,
                state_dir=state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="live0-audit-missing-queue-e-world-contact",
                strict=True,
            )

            report = self._read_json(reports / "live0_acceptance_audit_report.json")

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report["status"], "blocked")
        self.assertIn(
            "g_initial_life_mechanism_coverage",
            report["summary"]["failed_criteria"],
        )
        self.assertTrue(
            any(
                "queue_e_world_contact_repair_hold_schema_handoff" in reason
                for reason in report["blocked_reasons"]
            )
        )

    def test_live0_acceptance_audit_blocks_without_proactive_terminal_voice(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state = runtime_root / "state"
            reports = runtime_root / "reports" / "latest"
            receipts = runtime_root / "receipts"
            self._write_live0_fixture(runtime_root)
            (state / "terminal" / "resident_terminal_proactive_state.json").unlink()

            result = run_live0_acceptance_audit(
                docs_dir=self.docs_dir,
                state_dir=state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="live0-audit-missing-proactive-terminal-voice",
                strict=True,
            )

            report = self._read_json(reports / "live0_acceptance_audit_report.json")

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report["status"], "blocked")
        self.assertIn(
            "b_conscious_emotion_thought_language",
            report["summary"]["failed_criteria"],
        )
        self.assertTrue(
            any(
                "resident_proactive_terminal_voice_audited" in reason
                for reason in report["blocked_reasons"]
            )
        )

    def test_cli_audit_live0_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state = runtime_root / "state"
            reports = runtime_root / "reports" / "latest"
            receipts = runtime_root / "receipts"
            self._write_live0_fixture(runtime_root)

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0",
                    "audit-live0",
                    "--docs",
                    str(self.docs_dir),
                    "--state",
                    str(state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "live0-audit-cli",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )

            report = self._read_json(reports / "live0_acceptance_audit_report.json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["run_id"], "live0-audit-cli")
        self.assertEqual(report["status"], "closed")

    def _write_live0_fixture(self, runtime_root: Path) -> None:
        closed_reports = [
            "direction_lock_report",
            "source_authority_report",
            "neural_life_core_report",
            "state_store_report",
            "life_membrane_report",
            "language_relationship_report",
            "validation_membrane_report",
            "schema_runner_report",
            "life_support_development_report",
            "first_activation_preflight_report",
            "replay_shadow_report",
            "growth_archive_report",
            "report_bundle",
            "stage_explanation_report",
            "digital_life_birth_packet",
        ]
        for name in closed_reports:
            self._write_json_ref(
                runtime_root,
                f"runtime/reports/latest/{name}.json",
                {"schema_version": f"{name}_v0", "status": "closed"},
            )
        self._write_json_ref(
            runtime_root,
            "runtime/reports/latest/birth_readiness_report.json",
            {
                "schema_version": "s08_life_target_runtimes_report_v0",
                "overall_status": "open",
                "blocked_reasons": [],
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/reports/latest/growth_reconsolidation_report.json",
            {
                "schema_version": "s10_runtime_growth_reconsolidation_report_v0",
                "status": "safe_idle",
                "blocked_reasons": [],
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/reports/latest/v0_contract_coverage_report.json",
            {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
                "activation_preflight_allowed": True,
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/reports/latest/digital_life_model_expression_report.json",
            {
                "schema_version": "model_expression_report_v0",
                "status": "closed",
                "model_expression_status": "model_expression_applied",
                "post_expression_gate_status": "accepted",
                "audited_expression_material_release_disabled": True,
                "model_provider": "openai-compatible",
                "model_name": "gpt-5.5",
                "model_api_key_present": True,
                "model_api_key_redacted": "<redacted>",
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/reports/latest/digital_life_process_report.json",
            {
                "schema_version": "digital_life_process_report_v0",
                "status": "closed",
                "completed_dialogue_turns": 2,
                "last_life_turn": {
                    "relation_role": "friend",
                    "resident_background_lineage_autonomous_activity_refs": [
                        "runtime/state/terminal/resident_autonomous_activity_state.json"
                    ],
                    "resident_background_lineage_dream_wake_refs": [
                        "runtime/state/dream/dream_experience_window.json",
                        "runtime/state/dream/wake_integration_frame.json",
                    ],
                    "resident_background_lineage_offline_learning_refs": [
                        "runtime/state/growth/belief_learning_plan.json"
                    ],
                    "offline_learning_cumulative_profile": {
                        "schema_version": "offline_learning_cumulative_profile_v0",
                        "generation": 3,
                        "ref_set": ["runtime/state/growth/belief_learning_plan.json"],
                    },
                },
            },
        )
        queue_e_governance_refs = [
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/world_contact_summary.json",
            "runtime/reports/latest/pain_regret_repair_report.json",
        ]
        queue_e_blocked_routes = [
            "external_release_without_repair_review",
            "direct_world_contact_without_confirmation",
        ]
        queue_e_allowed_routes = [
            "repair_followup",
            "shadow_review",
        ]
        self._write_json_ref(
            runtime_root,
            "runtime/state/action/go_nogo_state.json",
            {
                "schema_version": "go_nogo_state_v0",
                "status": "closed",
                "future_no_go_profile": {
                    "schema_version": "future_no_go_profile_v0",
                    "repair_hold_required": True,
                    "confirmation_threshold_bias": "raised",
                    "repair_governance_refs": queue_e_governance_refs,
                },
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/validation/world_contact_validation.json",
            {
                "schema_version": "world_contact_validation_v0",
                "status": "closed",
                "future_no_go_profile_ref": "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                "repair_hold_required": True,
                "confirmation_threshold_bias": "raised",
                "blocked_future_routes": queue_e_blocked_routes,
                "allowed_repair_routes": queue_e_allowed_routes,
                "repair_governance_refs": queue_e_governance_refs,
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/validation/validation_rollup.json",
            {
                "schema_version": "validation_rollup_v0",
                "overall_status": "closed",
                "queue_e_world_contact_future_no_go_profile_ref": "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                "queue_e_world_contact_repair_hold_required": True,
                "queue_e_world_contact_confirmation_threshold_bias": "raised",
                "queue_e_world_contact_future_release_posture": "repair_before_release",
                "queue_e_world_contact_blocked_future_routes": queue_e_blocked_routes,
                "queue_e_world_contact_allowed_repair_routes": queue_e_allowed_routes,
                "queue_e_world_contact_repair_governance_refs": queue_e_governance_refs,
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/schema_runner/run_manifest.json",
            {
                "schema_version": "schema_runner_run_manifest_v0",
                "run_status": "closed",
                "queue_e_world_contact_future_no_go_profile_ref": "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                "queue_e_world_contact_repair_hold_required": True,
                "queue_e_world_contact_confirmation_threshold_bias": "raised",
                "queue_e_world_contact_future_release_posture": "repair_before_release",
                "queue_e_world_contact_blocked_future_routes": queue_e_blocked_routes,
                "queue_e_world_contact_allowed_repair_routes": queue_e_allowed_routes,
                "queue_e_world_contact_repair_governance_refs": queue_e_governance_refs,
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/identity/life_name_registry.json",
            {
                "schema_version": "digital_life_name_registry_v0",
                "status": "loaded_existing_name",
                "canonical_name": "星火",
                "normalized_name": "星火",
                "life_name_id": "test-life-name",
                "name_lock_state": "permanent_for_runtime",
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/identity/life_name_command_manifest.json",
            {
                "schema_version": "life_name_direct_command_manifest_v0",
                "status": "active",
                "direct_command_enabled": True,
                "command_on_path": True,
                "command_name": "星火",
                "command_path": str(
                    self._write_direct_life_name_command(runtime_root, "星火")
                ),
                "state_dir": str((runtime_root / "state").resolve()),
                "reports_dir": str((runtime_root / "reports" / "latest").resolve()),
                "receipts_dir": str((runtime_root / "receipts").resolve()),
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/terminal/resident_lifecycle_state.json",
            {
                "schema_version": "resident_lifecycle_state_v0",
                "status": "background_active",
                "pid": os.getpid(),
                "resident_lifecycle_state_ref": "runtime/state/terminal/resident_lifecycle_state.json",
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/terminal/resident_relation_queue_state.json",
            {
                "schema_version": "resident_relation_queue_state_v0",
                "status": "waiting_for_relation_turn",
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/terminal/resident_process_lease.json",
            {
                "schema_version": "resident_process_lease_v0",
                "lease_state": "active",
                "resident_process_id": "resident-process-test",
            },
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/terminal/resident_process_lease_history_profile.json",
            {
                "schema_version": "resident_process_lease_history_profile_v0",
                "history_event_count": 1,
                "current_identity_continuity_state": "active_residency",
                "identity_pressure_level": "present",
            },
        )
        self._write_jsonl_ref(
            runtime_root,
            "runtime/state/terminal/resident_process_lease_history.jsonl",
            [{"schema_version": "resident_process_lease_history_event_v0"}],
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/terminal/resident_autonomous_activity_state.json",
            {
                "schema_version": "resident_autonomous_activity_state_v0",
                "status": "active",
                "activity_count": 5,
                "cycle_coverage_complete": True,
                "cycle_completion_count": 1,
                "covered_activity_kinds": [
                    "sleep",
                    "memory_recall",
                    "self_thinking",
                    "growth_rehearsal",
                    "learning_consolidation",
                ],
                "missing_activity_kinds": [],
            },
        )
        self._write_jsonl_ref(
            runtime_root,
            "runtime/state/terminal/resident_terminal_proactive_events.jsonl",
            [
                {
                    "schema_version": "resident_proactive_terminal_event_v0",
                    "status": "held_internal",
                    "release_scope": "open_terminal_idle_hidden",
                    "natural_language_released": False,
                    "focus": "memory_wake_question",
                    "proactive_voice_profile": {
                        "schema_version": "resident_proactive_voice_profile_v0",
                        "surface_kind": "wake_question_candidate",
                    },
                }
            ],
        )
        self._write_json_ref(
            runtime_root,
            "runtime/state/terminal/resident_terminal_proactive_state.json",
            {
                "schema_version": "resident_terminal_proactive_state_v0",
                "status": "held_internal",
                "last_release_scope": "open_terminal_idle_hidden",
                "last_natural_language_released": False,
                "last_sequence": 1,
                "last_focus": "memory_wake_question",
                "last_proactive_voice_profile": {
                    "schema_version": "resident_proactive_voice_profile_v0",
                    "surface_kind": "wake_question_candidate",
                },
                "last_proactive_voice_surface_kind": "wake_question_candidate",
                "event_count": 1,
                "release_count": 0,
                "resident_terminal_proactive_events_ref": "runtime/state/terminal/resident_terminal_proactive_events.jsonl",
            },
        )
        for ref, schema in {
            "runtime/state/prediction/prediction_workspace_frame.json": "prediction_workspace_frame_v0",
            "runtime/state/signal/signal_media_runtime.json": "signal_media_runtime_v0",
            "runtime/state/prediction/active_sampling_plan.json": "active_sampling_plan_v0",
            "runtime/state/body/core_affect_vector.json": "core_affect_vector_v0",
            "runtime/state/self/resident_self_thinking_state.json": "resident_self_thinking_state_v0",
            "runtime/state/language/language_percept_frame.json": "language_percept_frame_v0",
            "runtime/state/language/semantic_map_frame.json": "semantic_map_frame_v0",
            "runtime/state/language/inner_speech_frame.json": "inner_speech_frame_v0",
            "runtime/state/language/expression_monitor_state.json": "expression_monitor_state_v0",
            "runtime/state/language/expression_plan.json": "expression_plan_v0",
            "runtime/state/life_state.json": "life_state_v0",
            "runtime/state/memory/engram_index.json": "engram_index_v0",
            "runtime/state/memory/relationship_memory.json": "relationship_memory_v0",
            "runtime/state/self/autobiographical_stack.json": "autobiographical_stack_v0",
            "runtime/state/memory/resident_memory_recall_state.json": "resident_memory_recall_state_v0",
            "runtime/state/memory/memory_write_gate.json": "memory_write_gate_v0",
            "runtime/state/growth/growth_patch_candidate_queue.json": "growth_patch_candidate_queue_v0",
            "runtime/state/growth/self_read_report.json": "self_read_report_v0",
            "runtime/state/growth/resident_growth_rehearsal_state.json": "resident_growth_rehearsal_state_v0",
            "runtime/state/growth/resident_learning_consolidation_state.json": "resident_learning_consolidation_state_v0",
            "runtime/state/dream/dream_experience_window.json": "dream_experience_window_v0",
            "runtime/state/dream/wake_integration_frame.json": "wake_integration_frame_v0",
            "runtime/state/terminal/resident_sleep_cycle_state.json": "resident_sleep_state_v0",
            "runtime/state/relationship/relationship_timeline.json": "relationship_timeline_v0",
            "runtime/state/relationship/commitment_truth_state.json": "commitment_truth_state_v0",
            "runtime/reports/latest/dialogue_writeback_bundle.json": "dialogue_writeback_bundle_v0",
            "runtime/state/life_targets/queue_e_birth_repair_profile.json": "queue_e_repair_modulation_profile_v0",
            "runtime/state/growth/belief_learning_plan.json": "belief_learning_plan_v0",
        }.items():
            payload = {"schema_version": schema, "status": "closed"}
            if ref.endswith("life_state.json"):
                payload = {"schema_version": schema}
            if ref.endswith("queue_e_birth_repair_profile.json"):
                payload["pressure_level"] = "elevated"
            self._write_json_ref(runtime_root, ref, payload)
        self._write_json_ref(
            runtime_root,
            "runtime/state/dream/dream_fact_gate_decision.json",
            {
                "schema_version": "dream_fact_gate_decision_v0",
                "gate_result": "passed",
            },
        )
        self._write_jsonl_ref(
            runtime_root,
            "runtime/state/language/dialogue_turn_log.jsonl",
            [{"schema_version": "dialogue_turn_event_v0", "relation_role": "friend"}],
        )

    def _write_json_ref(self, runtime_root: Path, ref: str, payload: dict) -> None:
        path = runtime_root / ref.removeprefix("runtime/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_jsonl_ref(self, runtime_root: Path, ref: str, events: list[dict]) -> None:
        path = runtime_root / ref.removeprefix("runtime/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
            encoding="utf-8",
        )

    def _write_direct_life_name_command(
        self,
        runtime_root: Path,
        command_name: str,
    ) -> Path:
        command_dir = runtime_root / "command-bin"
        command_dir.mkdir(parents=True, exist_ok=True)
        command_path = command_dir / command_name
        command_path.write_text(
            "\n".join(
                [
                    "#!/bin/sh",
                    "# human-agent-life-name-direct-command-v0",
                    f"# state_dir={(runtime_root / 'state').resolve()}",
                    f"# reports_dir={(runtime_root / 'reports' / 'latest').resolve()}",
                    f"# receipts_dir={(runtime_root / 'receipts').resolve()}",
                    "exit 0",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        command_path.chmod(0o755)
        return command_path

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _criterion(self, report: dict, criterion_id: str) -> dict:
        for criterion in report["criteria"]:
            if criterion["criterion_id"] == criterion_id:
                return criterion
        self.fail(f"criterion not found: {criterion_id}")
