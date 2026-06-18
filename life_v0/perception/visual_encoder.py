from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Mapping

VISUAL_OBSERVATION_REF = "runtime/state/observation/visual_observation.json"
SOURCE_DOC_REFS = [
    "docs/v0/动力学升级/10_用户上下文与感知视觉.md",
    "docs/real—live0/09_prediction_perception_world_contact.md",
]


def is_visual_encoder_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_VISUAL_ENCODER"), False)


def encode_visual_observation(
    *,
    image_ref: str | None = None,
    generated_at: str,
    run_id: str = "visual-encode",
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    if not is_visual_encoder_enabled(environ):
        return _degraded_visual_observation(
            generated_at=generated_at,
            run_id=run_id,
            reason="visual_encoder_disabled",
        )

    normalized_ref = str(image_ref or "").strip()
    if not normalized_ref:
        return _degraded_visual_observation(
            generated_at=generated_at,
            run_id=run_id,
            reason="no_visual_input",
        )

    path = Path(normalized_ref)
    if not path.exists():
        return _degraded_visual_observation(
            generated_at=generated_at,
            run_id=run_id,
            reason="visual_input_missing",
            image_ref=normalized_ref,
        )

    try:
        payload = path.read_bytes()
    except OSError:
        return _degraded_visual_observation(
            generated_at=generated_at,
            run_id=run_id,
            reason="visual_input_unreadable",
            image_ref=normalized_ref,
        )

    if not payload:
        return _degraded_visual_observation(
            generated_at=generated_at,
            run_id=run_id,
            reason="visual_input_empty",
            image_ref=normalized_ref,
        )

    fingerprint = hashlib.sha256(payload).hexdigest()[:16]
    return {
        "schema_version": "visual_observation_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "encoded_ref_only",
        "encoder_available": True,
        "encoder_kind": "ref_fingerprint_v0",
        "image_ref": normalized_ref,
        "visual_embedding_ref": f"{VISUAL_OBSERVATION_REF}#embedding:{fingerprint}",
        "visual_caption_candidate": None,
        "visual_feature_encoding": {
            "encoding_kind": "content_fingerprint",
            "layout_fingerprint": fingerprint,
            "byte_length": len(payload),
        },
        "truth_gate_required": True,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_visual_observation_event(
    *,
    image_ref: str | None = None,
    generated_at: str,
    run_id: str = "visual-event",
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    encoded = encode_visual_observation(
        image_ref=image_ref,
        generated_at=generated_at,
        run_id=run_id,
        environ=environ,
    )
    return {
        "schema_version": "visual_observation_event_v1",
        "event_kind": "VisualObservationEvent",
        "generated_at": generated_at,
        "observation_ref": VISUAL_OBSERVATION_REF,
        "observation_status": encoded.get("status"),
        "encoder_available": encoded.get("encoder_available"),
        "degrade_reason": encoded.get("degrade_reason"),
        "visual_observation": encoded,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _degraded_visual_observation(
    *,
    generated_at: str,
    run_id: str,
    reason: str,
    image_ref: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "visual_observation_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "degraded",
        "encoder_available": False,
        "encoder_kind": None,
        "image_ref": image_ref,
        "visual_embedding_ref": None,
        "visual_caption_candidate": None,
        "visual_feature_encoding": None,
        "degrade_reason": reason,
        "truth_gate_required": True,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _parse_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default