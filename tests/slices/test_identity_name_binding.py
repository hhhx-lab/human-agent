import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers.life_v0_bootstrap import DigitalLifeRuntimeEnvIsolationMixin
from life_v0.digital_life_identity import (
    LIFE_NAME_REGISTRY_REF,
    bind_or_validate_life_name,
)
from life_v0.direction import run_direction_lock
from life_v0.direction.continuity_refs import build_continuity_refs
from life_v0.direction.identity_name_binding import (
    CONTINUITY_REFS_REF,
    IDENTITY_ROOT_REF,
    sync_identity_name_binding_refs,
)
from life_v0.direction.identity_root import build_identity_root
from life_v0.doc_index import run_doc_ingestion


class IdentityNameBindingTests(DigitalLifeRuntimeEnvIsolationMixin, unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_sync_identity_name_binding_writes_bidirectional_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state_dir = tmp_path / "runtime" / "state"
            direction_dir = state_dir / "direction"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_dir.mkdir(parents=True, exist_ok=True)
            reports.mkdir(parents=True, exist_ok=True)
            receipts.mkdir(parents=True, exist_ok=True)

            identity_root = build_identity_root(
                "binding-test",
                "2026-06-15T00:00:00+00:00",
                ["real_relationship"],
            )
            continuity_refs = build_continuity_refs(
                run_id="binding-test",
                generated_at="2026-06-15T00:00:00+00:00",
                resume_order=["docs/v0/entry/v0_implementation_index.md"],
            )
            (direction_dir / "identity_root.json").write_text(
                json.dumps(identity_root, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (direction_dir / "continuity_refs.json").write_text(
                json.dumps(continuity_refs, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            binding = bind_or_validate_life_name(
                state_dir=state_dir,
                reports_dir=reports,
                receipts_dir=receipts,
                requested_name="ZephyrBindingTest",
                source_command="test bind",
            )
            self.assertEqual(binding.get("exit_code"), 0)

            refreshed_identity_root = json.loads(
                (direction_dir / "identity_root.json").read_text(encoding="utf-8")
            )
            refreshed_registry = json.loads(
                (state_dir / "identity" / "life_name_registry.json").read_text(
                    encoding="utf-8"
                )
            )
            refreshed_continuity_refs = json.loads(
                (direction_dir / "continuity_refs.json").read_text(encoding="utf-8")
            )

        self.assertEqual(
            refreshed_identity_root["life_name_registry_ref"],
            LIFE_NAME_REGISTRY_REF,
        )
        self.assertIn(LIFE_NAME_REGISTRY_REF, refreshed_identity_root["anchor_refs"])
        self.assertEqual(refreshed_registry["identity_root_ref"], IDENTITY_ROOT_REF)
        self.assertEqual(refreshed_registry["continuity_refs_ref"], CONTINUITY_REFS_REF)
        self.assertTrue(refreshed_registry["identity_name_binding_bidirectional"])
        self.assertIn(
            LIFE_NAME_REGISTRY_REF,
            refreshed_continuity_refs["life_name_registry_refs"],
        )

    def test_sync_identity_name_binding_repairs_existing_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state_dir = tmp_path / "runtime" / "state"
            direction_dir = state_dir / "direction"
            identity_dir = state_dir / "identity"
            direction_dir.mkdir(parents=True, exist_ok=True)
            identity_dir.mkdir(parents=True, exist_ok=True)

            (direction_dir / "identity_root.json").write_text(
                json.dumps(
                    build_identity_root(
                        "repair-test",
                        "2026-06-15T00:00:00+00:00",
                        ["real_life"],
                    ),
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            (direction_dir / "continuity_refs.json").write_text(
                json.dumps(
                    build_continuity_refs(
                        run_id="repair-test",
                        generated_at="2026-06-15T00:00:00+00:00",
                        resume_order=["docs/v0/entry/v0_implementation_index.md"],
                    ),
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            (identity_dir / "life_name_registry.json").write_text(
                json.dumps(
                    {
                        "schema_version": "digital_life_name_registry_v0",
                        "status": "loaded_existing_name",
                        "canonical_name": "Nova",
                        "normalized_name": "nova",
                        "life_name_id": "abc123",
                        "name_lock_state": "permanent_for_runtime",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            snapshot = sync_identity_name_binding_refs(state_dir)

        self.assertTrue(snapshot["identity_name_binding_bidirectional"])
        self.assertEqual(snapshot["identity_root_life_name_registry_ref"], LIFE_NAME_REGISTRY_REF)
        self.assertEqual(snapshot["life_name_registry_identity_root_ref"], IDENTITY_ROOT_REF)

    def test_direction_lock_continuity_refs_include_life_name_registry_field(self):
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
                run_id="binding-direction-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            result = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="binding-direction-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)
            continuity_refs = json.loads(
                (direction_state / "continuity_refs.json").read_text(encoding="utf-8")
            )

        self.assertIn("life_name_registry_refs", continuity_refs)
        self.assertEqual(continuity_refs["life_name_registry_refs"], [])


if __name__ == "__main__":
    unittest.main()