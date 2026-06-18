from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from life_v0.perception.visual_encoder import (
    encode_visual_observation,
    is_visual_encoder_enabled,
)
from life_v0.state_store.cross_modal_evidence import collect_cross_modal_source_evidence


class VisualEncoderTests(unittest.TestCase):
    def test_disabled_by_default(self):
        self.assertFalse(is_visual_encoder_enabled({}))

    def test_graceful_degrade_when_disabled(self):
        encoded = encode_visual_observation(
            image_ref="/tmp/example.png",
            generated_at="2026-06-17T07:00:00Z",
            environ={},
        )
        self.assertEqual(encoded["status"], "degraded")
        self.assertFalse(encoded["encoder_available"])
        self.assertEqual(encoded["degrade_reason"], "visual_encoder_disabled")

    def test_graceful_degrade_without_input_when_enabled(self):
        encoded = encode_visual_observation(
            image_ref=None,
            generated_at="2026-06-17T07:00:00Z",
            environ={"DIGITAL_LIFE_VISUAL_ENCODER": "true"},
        )
        self.assertEqual(encoded["status"], "degraded")
        self.assertFalse(encoded["encoder_available"])
        self.assertEqual(encoded["degrade_reason"], "no_visual_input")

    def test_encodes_existing_image_ref_when_enabled(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
            handle.write(b"fake-image-bytes")
            image_path = handle.name
        try:
            encoded = encode_visual_observation(
                image_ref=image_path,
                generated_at="2026-06-17T07:00:00Z",
                environ={"DIGITAL_LIFE_VISUAL_ENCODER": "true"},
            )
            self.assertEqual(encoded["status"], "encoded_ref_only")
            self.assertTrue(encoded["encoder_available"])
            self.assertIsNotNone(encoded["visual_embedding_ref"])
            self.assertIsNotNone(encoded["visual_feature_encoding"])
        finally:
            Path(image_path).unlink(missing_ok=True)

    def test_cross_modal_collects_degraded_visual_observation(self):
        evidence = collect_cross_modal_source_evidence(
            visual_observation={
                "status": "degraded",
                "encoder_available": False,
                "degrade_reason": "no_visual_input",
            }
        )
        self.assertIn(
            "runtime/state/observation/visual_observation.json#degraded",
            evidence["cross_modal_evidence_refs"],
        )


if __name__ == "__main__":
    unittest.main()