import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SourceAuthorityTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_source_authority_writes_registry_maps_report_and_receipt(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"

            ingest = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=doc_out,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="source-authority-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            direction = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="source-authority-direction",
                strict=True,
            )
            self.assertEqual(direction.exit_code, 0)

            result = run_source_authority(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                out_dir=authority_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="source-authority-test",
                strict=True,
            )

            self.assertEqual(result.exit_code, 0)

            registry = self._read_json(authority_state / "authority_registry.json")
            quality_policy = self._read_json(authority_state / "source_quality_policy.json")
            matrix_index = self._read_json(authority_state / "literature_matrix_index.json")
            family_index = self._read_json(authority_state / "authority_family_index.json")
            mechanism_map = self._read_json(authority_state / "mechanism_evidence_map.json")
            prediction_chain = self._read_json(authority_state / "prediction_authority_chain.json")
            carrier_patches = self._read_json(authority_state / "doc_authority_carrier_patch_index.json")
            cross_file_rules = self._read_json(authority_state / "authority_cross_file_rule_index.json")
            gap_queue = self._read_json(authority_state / "authority_gap_queue.json")
            direction_binding = self._read_json(authority_state / "authority_direction_binding.json")
            report = self._read_json(reports / "source_authority_report.json")
            digest = self._read_json(reports / "source_authority_digest.json")
            receipt = self._read_json(receipts / "source_authority_source-authority-test.json")

        expected_authority_docs = self._expected_authority_docs()

        self.assertEqual(registry["schema_version"], "authority_registry_v0")
        self.assertEqual(registry["active_engineering_slice"], "S01_SOURCE_AUTHORITY")
        self.assertGreaterEqual(registry["source_count"], 100)
        self.assertEqual(registry["source_count"], len(registry["sources"]))
        self.assertEqual(set(registry["authority_doc_refs"]), set(expected_authority_docs))

        source_ids = {source["source_id"] for source in registry["sources"]}
        self.assertIn("AH001", source_ids)
        self.assertIn("AH100", source_ids)
        self.assertIn("AHL001", source_ids)
        self.assertIn("AHPAI001", source_ids)
        self.assertTrue(
            any(source["source_doc"] == "docs/01aa_prediction_active_inference_cross_chain_checker_plan.md" for source in registry["sources"])
        )

        required_fields = {
            "quality_class",
            "source_kind",
            "mechanism_objects",
            "runtime_carriers",
            "life_targets",
            "downstream_docs",
        }
        for source in registry["sources"]:
            for field in required_fields:
                self.assertIn(field, source, source)
                self.assertTrue(source[field], source)

        self.assertEqual(quality_policy["schema_version"], "source_quality_policy_v0")
        self.assertIn("tier_1_review", quality_policy["quality_classes"])
        self.assertIn("ai_bridge", quality_policy["quality_classes"])

        self.assertEqual(matrix_index["schema_version"], "literature_matrix_index_v0")
        self.assertEqual(set(matrix_index["authority_doc_refs"]), set(expected_authority_docs))
        self.assertTrue(all(matrix_index["doc_source_counts"][doc] > 0 for doc in expected_authority_docs))

        expected_families = {
            "global_foundation_authority",
            "extended_specialized_authority",
            "memory_growth_authority",
            "language_relationship_authority",
            "pain_dream_life_target_authority",
            "validation_reality_authority",
            "signal_body_consciousness_authority",
            "region_action_affect_authority",
            "prediction_active_inference_authority",
        }
        self.assertEqual(set(family_index["families"]), expected_families)
        self.assertTrue(all(family_index["family_coverage"][family] for family in expected_families))

        self.assertEqual(mechanism_map["schema_version"], "mechanism_evidence_map_v0")
        self.assertEqual(mechanism_map["source_count"], registry["source_count"])
        self.assertGreaterEqual(len(mechanism_map["edges"]), registry["source_count"])

        self.assertEqual(prediction_chain["schema_version"], "prediction_authority_chain_v0")
        self.assertIn("docs/01v_prediction_active_inference_runtime_matrix.md", prediction_chain["authority_doc_refs"])
        self.assertIn("docs/01ax_prediction_active_inference_post_repair_cycle_validation.md", prediction_chain["authority_doc_refs"])
        self.assertGreaterEqual(prediction_chain["source_count"], 1)

        self.assertEqual(carrier_patches["schema_version"], "doc_authority_carrier_patch_index_v0")
        self.assertEqual(len(carrier_patches["patches"]), 12)
        patched_docs = {patch["doc_node"] for patch in carrier_patches["patches"]}
        self.assertEqual(
            patched_docs,
            {
                "docs/02_brain_region_and_network_atlas.md",
                "docs/03_default_executive_salience_networks.md",
                "docs/04_sensory_thalamus_interoception.md",
                "docs/05_memory_systems_and_growth.md",
                "docs/06_action_reward_inhibition.md",
                "docs/07_emotion_personality_self.md",
                "docs/08_sleep_dream_fatigue_states.md",
                "docs/09_language_symbolic_top_layer.md",
                "docs/10_consciousness_attention_workspace.md",
                "docs/11_neuromodulation_and_signal_media.md",
                "docs/12_ai_and_cognitive_architecture_bridge.md",
                "docs/13_agentic_human_research_synthesis.md",
            },
        )
        self.assertTrue(all(patch["authority_refs"] for patch in carrier_patches["patches"]))
        self.assertTrue(all(patch["mechanism_objects"] for patch in carrier_patches["patches"]))

        self.assertEqual(cross_file_rules["schema_version"], "authority_cross_file_rule_index_v0")
        self.assertIn("core_02_to_13_authority_gate", cross_file_rules["rules"])

        self.assertEqual(gap_queue["schema_version"], "authority_gap_queue_v0")
        self.assertEqual(gap_queue["blocking_gap_count"], 0)

        self.assertEqual(direction_binding["schema_version"], "authority_direction_binding_v0")
        self.assertEqual(direction_binding["direction_statement"], "build_real_digital_life")
        self.assertEqual(direction_binding["s00_stage_effect"], "allow_s01_when_closed")

        self.assertEqual(report["schema_version"], "source_authority_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertEqual(report["next_allowed_slice"], "S02_NEURAL_LIFE_CORE")
        self.assertEqual(report["blocked_gates"], [])
        self.assertIn("ai_bridge_source_label_gate", report["closed_gates"])
        self.assertEqual(set(report["family_coverage"]), expected_families)
        self.assertTrue(all(report["life_target_coverage"][target] for target in report["life_target_coverage"]))
        self.assertTrue(report["ai_bridge_sources"])
        self.assertTrue(all(source["prohibited_subject_architecture"] is False for source in report["ai_bridge_sources"]))

        self.assertEqual(digest["current_slice"], "S01_SOURCE_AUTHORITY")
        self.assertEqual(digest["next_required_command"], "life-v0 build-neural-life-core --strict")
        self.assertEqual(receipt["schema_version"], "source_authority_receipt_v0")

    def test_cli_build_source_authority_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"

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
                    "source-authority-cli-ingest",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(ingest.returncode, 0, ingest.stderr)

            direction = subprocess.run(
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
                    "source-authority-cli-direction",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(direction.returncode, 0, direction.stderr)

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0",
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
                    "source-authority-cli",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = self._read_json(reports / "source_authority_report.json")

        self.assertEqual(report["run_id"], "source-authority-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-neural-life-core --strict")

    def _expected_authority_docs(self) -> list[str]:
        return sorted(path.relative_to(self.repo_root).as_posix() for path in self.docs_dir.glob("01*.md"))

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
