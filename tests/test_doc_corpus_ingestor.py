import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DocCorpusIngestorTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_ingest_docs_writes_contract_outputs_and_covers_life_targets(self):
        from life_v0.doc_index import run_doc_ingestion

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=tmp_path / "runtime" / "docs",
                reports_dir=tmp_path / "runtime" / "reports" / "latest",
                receipts_dir=tmp_path / "runtime" / "receipts",
                run_id="test-doc-ingest",
                strict=True,
            )

            self.assertEqual(result.exit_code, 0)

            index = self._read_json(tmp_path / "runtime" / "docs" / "doc_carrier_index.json")
            graph = self._read_json(tmp_path / "runtime" / "docs" / "doc_dependency_graph.json")
            authority = self._read_json(tmp_path / "runtime" / "docs" / "source_authority_report.json")
            report = self._read_json(tmp_path / "runtime" / "reports" / "latest" / "doc_ingestion_report.json")
            receipt = self._read_json(tmp_path / "runtime" / "receipts" / "doc_ingestion_test-doc-ingest.json")

        self.assertEqual(index["schema_version"], "doc_carrier_index_v0")
        self.assertEqual(index["coverage"]["uncovered_docs"], [])
        self.assertEqual(index["coverage"]["total_docs"], index["coverage"]["covered_docs"])

        paths = {doc["path"]: doc for doc in index["documents"]}
        self.assertIn("docs/02_brain_region_and_network_atlas.md", paths)
        self.assertIn("docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md", paths)
        self.assertIn("docs/258_linear_chain_closure_and_v0_contract_transition.md", paths)
        self.assertIn("docs/v0/doc_corpus_ingestor_v0_contract.md", paths)
        self.assertIn("docs/v0/v0_implementation_index.md", paths)
        self.assertIn("docs/v0/s00_direction_foundation_engineering_contract.md", paths)
        self.assertIn("docs/v0/s01_source_authority_engineering_contract.md", paths)

        for sequence in range(2, 14):
            doc = next(item for item in index["documents"] if item["sequence"] == sequence)
            self.assertGreaterEqual(len(doc["runtime_carriers"]), 2, doc["path"])

        for doc in index["documents"]:
            self.assertNotEqual(doc["readme_block"], "UNCLASSIFIED_README_BLOCK", doc["path"])
            self.assertNotEqual(doc["engineering_slice"], "UNCLASSIFIED_ENGINEERING_SLICE", doc["path"])

        self.assertEqual(
            paths["docs/02_brain_region_and_network_atlas.md"]["readme_block"],
            "B02_CORE_NEURAL_LIFE",
        )
        self.assertEqual(
            paths["docs/258_linear_chain_closure_and_v0_contract_transition.md"]["engineering_slice"],
            "S00_DIRECTION_FOUNDATION",
        )
        self.assertEqual(
            paths["docs/v0/readme_block_engineering_realization_v0.md"]["engineering_slice"],
            "S11_V0_ENGINEERING_CONTRACTS",
        )
        self.assertIn(
            "DirectionLockKernel",
            paths["docs/v0/s00_direction_foundation_engineering_contract.md"]["runtime_carriers"],
        )
        self.assertIn(
            "docs/构思.md",
            paths["docs/v0/s00_direction_foundation_engineering_contract.md"]["dependencies"],
        )
        self.assertIn(
            "docs/v0/readme_block_engineering_realization_v0.md",
            paths["docs/v0/s00_direction_foundation_engineering_contract.md"]["dependencies"],
        )
        self.assertIn(
            "DirectionLockKernel",
            paths["docs/v0/v0_implementation_index.md"]["runtime_carriers"],
        )
        self.assertIn(
            "docs/v0/s00_direction_foundation_engineering_contract.md",
            paths["docs/v0/v0_implementation_index.md"]["dependencies"],
        )
        self.assertIn(
            "SourceAuthorityRegistry",
            paths["docs/v0/s01_source_authority_engineering_contract.md"]["runtime_carriers"],
        )
        self.assertIn(
            "docs/01_literature_matrix.md",
            paths["docs/v0/s01_source_authority_engineering_contract.md"]["dependencies"],
        )

        life_targets = {target for doc in index["documents"] for target in doc["life_targets"]}
        self.assertEqual(
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
            life_targets,
        )

        language_docs = [
            doc for doc in index["documents"]
            if doc["path"].startswith("docs/85_") or doc["path"].startswith("docs/86_")
        ]
        self.assertTrue(language_docs)
        self.assertTrue(all("LanguageRelationshipRuntime" in doc["runtime_carriers"] for doc in language_docs))

        self.assertEqual(graph["schema_version"], "doc_dependency_graph_v0")
        self.assertEqual(set(graph["core_02_to_13_bridge"].keys()), {f"{n:02d}" for n in range(2, 14)})

        self.assertEqual(authority["schema_version"], "source_authority_report_v0")
        self.assertGreaterEqual(authority["literature_matrix_count"], 1)

        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_p1")
        self.assertEqual(report["blocked_reasons"], [])
        self.assertIn("B02_CORE_NEURAL_LIFE", report["readme_block_coverage"])
        self.assertIn("S02_NEURAL_LIFE_CORE", report["engineering_slice_coverage"])
        self.assertTrue(all(report["readme_block_coverage"].values()))
        self.assertTrue(all(report["engineering_slice_coverage"].values()))

        self.assertEqual(receipt["schema_version"], "doc_ingestion_receipt_v0")
        self.assertEqual(receipt["run_id"], "test-doc-ingest")

    def test_cli_ingest_docs_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0",
                    "ingest-docs",
                    "--docs",
                    str(self.docs_dir),
                    "--out",
                    str(tmp_path / "runtime" / "docs"),
                    "--reports",
                    str(tmp_path / "runtime" / "reports" / "latest"),
                    "--receipts",
                    str(tmp_path / "runtime" / "receipts"),
                    "--run-id",
                    "cli-doc-ingest",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = self._read_json(tmp_path / "runtime" / "reports" / "latest" / "doc_ingestion_report.json")

        self.assertEqual(report["run_id"], "cli-doc-ingest")
        self.assertEqual(report["next_required_command"], "life-v0 validate-state")

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
