from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.perception.live_visual_hook import (
    extract_visual_image_ref_from_utterance,
    maybe_run_visual_encoder_hook,
)
from life_v0.state_store.cross_modal_evidence import collect_cross_modal_source_evidence


class LiveVisualHookTests(unittest.TestCase):
    def test_extracts_image_reference_from_utterance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "assets" / "scene.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"png-bytes")
            ref = extract_visual_image_ref_from_utterance(
                "看看这张图 @assets/scene.png 有什么",
                repo_root=root,
            )
            self.assertEqual(ref, str(image.resolve()))

    def test_hook_writes_degraded_observation_when_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            observation_dir = Path(tmp)
            writes: list[tuple[Path, dict]] = []

            def write_json(path: Path, payload: dict) -> None:
                writes.append((path, payload))

            result = maybe_run_visual_encoder_hook(
                observation_dir=observation_dir,
                run_id="visual-hook",
                generated_at="2026-06-18T08:00:00Z",
                external_utterance="没有图片",
                write_json=write_json,
                environ={},
            )
            self.assertFalse(result.applied)
            self.assertEqual(result.visual_observation["status"], "degraded")
            self.assertEqual(len(writes), 0)

    def test_hook_encodes_image_and_feeds_cross_modal_when_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "photo.jpg"
            image.write_bytes(b"jpeg-bytes")
            observation_dir = root / "observation"
            observation_dir.mkdir(parents=True)

            def write_json(path: Path, payload: dict) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(payload, ensure_ascii=False),
                    encoding="utf-8",
                )

            result = maybe_run_visual_encoder_hook(
                observation_dir=observation_dir,
                run_id="visual-hook",
                generated_at="2026-06-18T08:00:00Z",
                external_utterance=f"请看 @photo.jpg",
                repo_root=root,
                write_json=write_json,
                environ={"DIGITAL_LIFE_VISUAL_ENCODER": "true"},
            )
            self.assertTrue(result.applied)
            self.assertEqual(result.visual_observation["status"], "encoded_ref_only")
            written = json.loads(
                (observation_dir / "visual_observation.json").read_text(encoding="utf-8")
            )
            evidence = collect_cross_modal_source_evidence(
                visual_observation=written,
            )
            self.assertIn("visual_percept", evidence["evidence_modalities"])
            self.assertIn(
                "runtime/state/observation/visual_observation.json",
                evidence["cross_modal_evidence_refs"],
            )


if __name__ == "__main__":
    unittest.main()