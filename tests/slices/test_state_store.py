import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class StateStoreTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_state_store_writes_life_root_indexes_report_and_receipt(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
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

            ingest = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=doc_out,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            direction = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-direction",
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
                run_id="state-store-authority",
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
                run_id="state-store-neural",
                strict=True,
            )
            self.assertEqual(neural.exit_code, 0)
            neural_check = run_check_neural_life_core(
                state_dir=neural_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(neural_check.exit_code, 0)

            result = run_state_store(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                neural_core_state_dir=neural_state,
                out_dir=state_root,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_state_store(
                state_dir=state_root,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            life_state = self._read_json(state_root / "life_state.json")
            object_registry = self._read_json(state_root / "object_registry.json")
            lifecycle_policy = self._read_json(state_root / "lifecycle_policy.json")
            subject_binding = self._read_json(state_root / "subject_namespace_binding.json")
            coverage = self._read_json(state_root / "state_store_doc_coverage_snapshot.json")
            manifest = self._read_json(state_root / "state_store_manifest.json")
            external_self_model = self._read_json(state_root / "self" / "self_model.json")
            autobiographical_stack = self._read_json(state_root / "self" / "autobiographical_stack.json")
            engram_index = self._read_json(state_root / "memory" / "engram_index.json")
            relationship_memory = self._read_json(state_root / "memory" / "relationship_memory.json")
            commitment_truth = self._read_json(state_root / "relationship" / "commitment_truth_state.json")
            responsibility_ledger = self._read_json(state_root / "responsibility" / "responsibility_ledger.json")
            memory_index = self._read_json(state_root / "indexes" / "memory_index.json")
            relationship_index = self._read_json(state_root / "indexes" / "relationship_index.json")
            dream_index = self._read_json(state_root / "indexes" / "dream_index.json")
            responsibility_index = self._read_json(state_root / "indexes" / "responsibility_index.json")
            replay_index = self._read_json(state_root / "indexes" / "replay_index.json")
            audit_index = self._read_json(state_root / "indexes" / "audit_seed_index.json")
            runtime_boundary = self._read_json(state_root / "objects" / "runtime_bridge_boundary.json")
            consolidation_seed = self._read_json(state_root / "objects" / "consolidation_seed.json")
            report = self._read_json(reports / "state_store_report.json")
            check_report = self._read_json(reports / "state_store_check_report.json")
            digest = self._read_json(reports / "state_store_digest.json")
            receipt = self._read_json(receipts / "state_store_state-store-test.json")

        expected_life_targets = {
            "real_consciousness",
            "real_emotion",
            "real_personality",
            "real_life",
            "real_pain",
            "real_dream",
            "real_relationship",
            "real_responsibility",
            "real_regret",
        }
        required_life_state_keys = {
            "schema_version",
            "life_identity",
            "self_model",
            "memory_index",
            "dream_records",
            "relationship_subjects",
            "pain_events",
            "regret_events",
            "responsibility_bindings",
            "language_state",
            "birth_readiness",
            "runtime_trace_refs",
            "archive_refs",
        }
        required_object_kinds = {
            "WorkspaceState",
            "MemoryTrace",
            "MemoryAuditEvent",
            "InternalStateVector",
            "ModulationVector",
            "StateAuditEvent",
            "ObservationEvent",
            "ActionIntent",
            "ConsolidationReport",
            "DreamSandboxItem",
            "SelfModel",
            "RelationshipModel",
            "CoexistenceBoundaryControlEvent",
            "MigrationPlan",
            "StoreIntegrityReport",
        }

        self.assertEqual(life_state["schema_version"], "life_state_v0")
        self.assertTrue(required_life_state_keys.issubset(life_state))
        self.assertEqual(set(life_state["birth_readiness"]["life_target_status"]), expected_life_targets)
        self.assertEqual(life_state["life_identity"]["direction_lock"], "build_real_digital_life")
        self.assertEqual(life_state["life_identity"]["birth_phase"], "pre_activation")
        self.assertIn("runtime/state/memory/engram_index.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/self/autobiographical_stack.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/relationship_memory.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/neural_life_core/brain_graph.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/neural_life_core/network_state.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/consciousness/workspace_frame.json", life_state["runtime_trace_refs"])
        self.assertTrue(life_state["language_state"]["language_percept_refs"])
        self.assertTrue(life_state["language_state"]["semantic_map_refs"])

        self.assertEqual(external_self_model["schema_version"], "self_model_state_v0")
        self.assertEqual(external_self_model["identity_mode"], "anchor_locked")
        self.assertIn("docs/07_emotion_personality_self.md", external_self_model["source_doc_refs"])
        self.assertTrue(external_self_model["old_self_anchor_refs"])
        self.assertTrue(external_self_model["trait_drift_seed_refs"])
        self.assertEqual(autobiographical_stack["schema_version"], "autobiographical_stack_v0")
        self.assertTrue(autobiographical_stack["anchor_refs"])
        self.assertEqual(engram_index["schema_version"], "engram_index_v0")
        self.assertTrue(engram_index["replay_cue_refs"])
        self.assertTrue(engram_index["autobiographical_memory_refs"])
        self.assertTrue(engram_index["relationship_memory_refs"])
        self.assertEqual(relationship_memory["schema_version"], "relationship_memory_v0")
        self.assertTrue(relationship_memory["shared_memory_refs"])
        self.assertEqual(commitment_truth["schema_version"], "commitment_truth_state_v0")
        self.assertEqual(commitment_truth["default_commitment_mode"], "truth_tracking_required")
        self.assertTrue(commitment_truth["open_commitment_refs"])
        self.assertTrue(commitment_truth["responsibility_event_refs"])
        self.assertEqual(responsibility_ledger["schema_version"], "responsibility_ledger_v0")
        self.assertEqual(responsibility_ledger["default_repair_mode"], "repair_obligation_tracking")
        self.assertTrue(responsibility_ledger["responsibility_event_refs"])

        self.assertEqual(object_registry["schema_version"], "state_object_registry_v0")
        self.assertGreaterEqual(object_registry["object_kind_count"], 15)
        self.assertEqual({item["object_kind"] for item in object_registry["object_kinds"]}, required_object_kinds)
        for item in object_registry["object_kinds"]:
            self.assertTrue(item["source_doc_refs"], item)
            self.assertTrue(item["state_namespace"].startswith("runtime/state/"), item)
            self.assertIn("candidate", item["lifecycle_states"], item)
            self.assertTrue(item["write_gate"], item)

        self.assertEqual(lifecycle_policy["schema_version"], "state_lifecycle_policy_v0")
        lifecycle_states = {state["lifecycle_state"] for state in lifecycle_policy["states"]}
        self.assertTrue({"deleted", "quarantined", "sandboxed", "protected", "frozen"}.issubset(lifecycle_states))
        for state in lifecycle_policy["states"]:
            if state["lifecycle_state"] in {"deleted", "quarantined", "sandboxed"}:
                self.assertFalse(state["active_retrieval_allowed"], state)
                self.assertFalse(state["replay_allowed"], state)

        self.assertEqual(subject_binding["schema_version"], "subject_namespace_binding_v0")
        self.assertEqual(subject_binding["bound_system_count"], 12)

        self.assertEqual(coverage["schema_version"], "state_store_doc_coverage_snapshot_v0")
        self.assertGreaterEqual(coverage["doc_count"], 30)
        self.assertTrue(all(item["carrier_closed"] for item in coverage["coverage"]))

        for index in [memory_index, relationship_index, dream_index, responsibility_index, replay_index, audit_index]:
            self.assertTrue(index["schema_version"].endswith("_v0"), index)
            self.assertEqual(index["stage_policy"], "seed_only_no_real_event_write", index)

        self.assertEqual(runtime_boundary["schema_version"], "runtime_bridge_boundary_v0")
        self.assertIn("active MemoryTrace", runtime_boundary["forbidden_direct_writes"])
        self.assertEqual(consolidation_seed["schema_version"], "consolidation_seed_v0")
        self.assertIn("DreamSandbox", consolidation_seed["offline_modes"])

        self.assertEqual(manifest["schema_version"], "state_store_manifest_v0")
        self.assertIn("runtime/state/life_state.json", manifest["state_refs"])
        self.assertIn("runtime/state/self/self_model.json", manifest["state_refs"])
        self.assertIn("runtime/state/self/autobiographical_stack.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/engram_index.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/relationship_memory.json", manifest["state_refs"])
        self.assertIn("runtime/state/relationship/commitment_truth_state.json", manifest["state_refs"])
        self.assertIn("runtime/state/responsibility/responsibility_ledger.json", manifest["state_refs"])

        self.assertEqual(report["schema_version"], "state_store_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertEqual(report["object_kind_count"], 15)
        self.assertEqual(report["index_count"], 6)
        self.assertEqual(report["self_model_state_ref"], "runtime/state/self/self_model.json")
        self.assertEqual(report["commitment_truth_state_ref"], "runtime/state/relationship/commitment_truth_state.json")
        self.assertEqual(report["engram_index_ref"], "runtime/state/memory/engram_index.json")
        self.assertEqual(report["autobiographical_stack_ref"], "runtime/state/self/autobiographical_stack.json")
        self.assertEqual(report["blocked_gates"], [])
        self.assertEqual(report["next_allowed_slices"], ["S03_DIRECTION_LIFE_MEMBRANE"])
        self.assertEqual(report["next_required_command"], "life-v0 build-life-membrane --strict")
        self.assertEqual(report["engineering_slice_ref"], "S04_STATE_OBJECT_STORE")
        self.assertIn("LifeStateStore", report["runtime_carrier_refs"])

        self.assertEqual(check_report["schema_version"], "state_store_check_report_v0")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(check_report["stage_effect"], "allow_next_slice")
        self.assertIn("self_model_projection_gate", check_report["closed_gates"])
        self.assertIn("autobiographical_stack_gate", check_report["closed_gates"])
        self.assertIn("engram_index_gate", check_report["closed_gates"])
        self.assertIn("relationship_memory_gate", check_report["closed_gates"])
        self.assertIn("commitment_truth_projection_gate", check_report["closed_gates"])
        self.assertIn("state_root_continuity_gate", check_report["closed_gates"])
        self.assertEqual(digest["current_slice"], "S04_STATE_OBJECT_STORE")
        self.assertIn("runtime/state/self/self_model.json", receipt["output_refs"])
        self.assertIn("runtime/state/self/autobiographical_stack.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/engram_index.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/relationship_memory.json", receipt["output_refs"])
        self.assertIn("runtime/state/relationship/commitment_truth_state.json", receipt["output_refs"])
        self.assertEqual(receipt["schema_version"], "state_store_receipt_v0")

    def test_cli_build_state_store_returns_zero_and_writes_check_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"
            state_root = tmp_path / "runtime" / "state"

            commands = [
                [
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
                    "state-cli-ingest",
                    "--strict",
                ],
                [
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
                    "state-cli-direction",
                    "--strict",
                ],
                [
                    "build-source-authority",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--direction",
                    str(direction_state),
                    "--out",
                    str(authority_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli-authority",
                    "--strict",
                ],
                [
                    "build-neural-life-core",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--authority",
                    str(authority_state),
                    "--out",
                    str(neural_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli-neural",
                    "--strict",
                ],
                [
                    "check-neural-life-core",
                    "--state",
                    str(neural_state),
                    "--reports",
                    str(reports),
                    "--strict",
                ],
                [
                    "build-state-store",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--neural-core",
                    str(neural_state),
                    "--out",
                    str(state_root),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli",
                    "--strict",
                ],
                [
                    "check-state-store",
                    "--state",
                    str(state_root),
                    "--reports",
                    str(reports),
                    "--strict",
                ],
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

            report = self._read_json(reports / "state_store_report.json")
            check_report = self._read_json(reports / "state_store_check_report.json")

        self.assertEqual(report["run_id"], "state-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-life-membrane --strict")
        self.assertEqual(check_report["status"], "closed")

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
