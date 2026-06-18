from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from life_v0.perception.visual_encoder import (
    VISUAL_OBSERVATION_REF,
    encode_visual_observation,
    is_visual_encoder_enabled,
)

REFERENCE_PATTERN = re.compile(r"@([^\s]+)")
VISUAL_IMAGE_SUFFIXES = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic", ".tif", ".tiff"}
)
BLOCKED_REFERENCE_ROOTS = frozenset(
    {".git", ".venv", "runtime", "node_modules", ".pytest_cache", ".codex"}
)


@dataclass(frozen=True)
class VisualEncoderHookResult:
    visual_observation: dict[str, Any]
    image_ref: str | None
    applied: bool


def extract_visual_image_ref_from_utterance(
    utterance: str,
    *,
    repo_root: Path | None = None,
) -> str | None:
    text = str(utterance or "")
    for match in REFERENCE_PATTERN.finditer(text):
        raw_ref = match.group(1).strip().rstrip(".,;，。；")
        if not raw_ref:
            continue
        resolved = _resolve_visual_reference(raw_ref, repo_root=repo_root)
        if resolved is not None:
            return str(resolved)
    return None


def maybe_run_visual_encoder_hook(
    *,
    observation_dir: Path,
    run_id: str,
    generated_at: str,
    external_utterance: str,
    repo_root: Path | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
    environ: Mapping[str, str] | None = None,
) -> VisualEncoderHookResult:
    observation_path = observation_dir / "visual_observation.json"
    image_ref = extract_visual_image_ref_from_utterance(
        external_utterance,
        repo_root=repo_root,
    )
    encoded = encode_visual_observation(
        image_ref=image_ref,
        generated_at=generated_at,
        run_id=run_id,
        environ=environ,
    )
    if is_visual_encoder_enabled(environ) or image_ref:
        write_json(observation_path, encoded)
        return VisualEncoderHookResult(
            visual_observation=encoded,
            image_ref=image_ref,
            applied=True,
        )

    existing = _read_json(observation_path)
    if existing:
        return VisualEncoderHookResult(
            visual_observation=existing,
            image_ref=image_ref,
            applied=False,
        )
    return VisualEncoderHookResult(
        visual_observation=encoded,
        image_ref=image_ref,
        applied=False,
    )


def _resolve_visual_reference(
    raw_ref: str,
    *,
    repo_root: Path | None,
) -> Path | None:
    clean = raw_ref.replace("\\", "/").lstrip("/")
    if not clean or clean.startswith("~"):
        return None
    suffix = Path(clean).suffix.lower()
    if suffix not in VISUAL_IMAGE_SUFFIXES:
        return None
    first = clean.split("/", 1)[0]
    if first in BLOCKED_REFERENCE_ROOTS:
        return None
    if clean == ".env" or clean.startswith(".env."):
        if clean != ".env.example":
            return None
    if repo_root is None:
        candidate = Path(clean)
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()
        return None
    path = (repo_root / clean).resolve()
    try:
        path.relative_to(repo_root.resolve())
    except ValueError:
        return None
    if not path.exists() or not path.is_file():
        return None
    if path.stat().st_size > 512_000:
        return None
    return path


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import json

        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


__all__ = [
    "VISUAL_OBSERVATION_REF",
    "VisualEncoderHookResult",
    "extract_visual_image_ref_from_utterance",
    "maybe_run_visual_encoder_hook",
]