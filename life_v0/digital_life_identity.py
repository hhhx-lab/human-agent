from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LIFE_NAME_REGISTRY_REF = "runtime/state/identity/life_name_registry.json"
LIFE_NAME_REGISTRY_SCHEMA = "digital_life_name_registry_v0"


def bind_or_validate_life_name(
    *,
    state_dir: Path,
    requested_name: str | None,
    source_command: str,
) -> dict[str, Any]:
    registry = read_life_name_registry(state_dir)
    registry_path = life_name_registry_path(state_dir)
    requested = _clean_name(requested_name)

    if registry:
        canonical_name = str(registry.get("canonical_name", "")).strip()
        normalized_name = str(registry.get("normalized_name", "")).strip()
        if requested and _normalize_name(requested) != normalized_name:
            return {
                "schema_version": LIFE_NAME_REGISTRY_SCHEMA,
                "status": "name_mismatch",
                "exit_code": 2,
                "canonical_name": canonical_name,
                "requested_name": requested,
                "life_name_registry_ref": LIFE_NAME_REGISTRY_REF,
                "message": "life name is already bound for this runtime",
            }
        registry["status"] = "loaded_existing_name"
        registry["exit_code"] = 0
        registry["source_command"] = source_command
        return registry

    if not requested:
        return {
            "schema_version": LIFE_NAME_REGISTRY_SCHEMA,
            "status": "name_required",
            "exit_code": 2,
            "life_name_registry_ref": LIFE_NAME_REGISTRY_REF,
            "message": "first launch must bind a digital life name",
            "required_command": "my digital life --name <name>",
        }

    validation_error = _validate_name(requested)
    if validation_error:
        return {
            "schema_version": LIFE_NAME_REGISTRY_SCHEMA,
            "status": "invalid_name",
            "exit_code": 2,
            "requested_name": requested,
            "life_name_registry_ref": LIFE_NAME_REGISTRY_REF,
            "message": validation_error,
        }

    generated_at = _now_iso()
    normalized_name = _normalize_name(requested)
    payload = {
        "schema_version": LIFE_NAME_REGISTRY_SCHEMA,
        "status": "bound_new_name",
        "canonical_name": requested,
        "normalized_name": normalized_name,
        "life_name_id": hashlib.sha256(normalized_name.encode("utf-8")).hexdigest()[
            :16
        ],
        "name_lock_state": "permanent_for_runtime",
        "bound_at": generated_at,
        "last_validated_at": generated_at,
        "source_command": source_command,
        "life_name_registry_ref": LIFE_NAME_REGISTRY_REF,
        "exit_code": 0,
    }
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def read_life_name_registry(state_dir: Path) -> dict[str, Any]:
    path = life_name_registry_path(state_dir)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    if payload.get("schema_version") != LIFE_NAME_REGISTRY_SCHEMA:
        return {}
    return dict(payload)


def life_name_registry_path(state_dir: Path) -> Path:
    return state_dir.resolve() / "identity" / "life_name_registry.json"


def _clean_name(name: str | None) -> str:
    return " ".join(str(name or "").strip().split())


def _normalize_name(name: str) -> str:
    return _clean_name(name).casefold()


def _validate_name(name: str) -> str:
    if not name:
        return "life name cannot be empty"
    if len(name) > 64:
        return "life name must be 64 characters or fewer"
    if re.search(r"[\x00-\x1f\x7f]", name):
        return "life name cannot contain control characters"
    return ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
