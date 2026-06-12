from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LIFE_NAME_REGISTRY_REF = "runtime/state/identity/life_name_registry.json"
LIFE_NAME_REGISTRY_SCHEMA = "digital_life_name_registry_v0"
LIFE_NAME_COMMAND_MANIFEST_REF = "runtime/state/identity/life_name_command_manifest.json"
LIFE_NAME_COMMAND_MANIFEST_SCHEMA = "life_name_direct_command_manifest_v0"
LIFE_NAME_COMMAND_DIR_ENV = "DIGITAL_LIFE_COMMAND_DIR"


def bind_or_validate_life_name(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
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
        command_manifest = ensure_life_name_command(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            canonical_name=canonical_name,
            source_command=source_command,
        )
        if command_manifest.get("status") != "active":
            return {
                **registry,
                "status": "direct_command_binding_failed",
                "exit_code": 2,
                "life_name_command_manifest_ref": LIFE_NAME_COMMAND_MANIFEST_REF,
                "life_name_command_manifest": command_manifest,
                "message": command_manifest.get(
                    "message",
                    "life name direct command could not be bound",
                ),
            }
        registry["status"] = "loaded_existing_name"
        registry["exit_code"] = 0
        registry["source_command"] = source_command
        registry["life_name_command_manifest_ref"] = LIFE_NAME_COMMAND_MANIFEST_REF
        registry["life_name_command_manifest"] = command_manifest
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
    command_manifest = ensure_life_name_command(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        canonical_name=requested,
        source_command=source_command,
    )
    payload["life_name_command_manifest_ref"] = LIFE_NAME_COMMAND_MANIFEST_REF
    payload["life_name_command_manifest"] = command_manifest
    if command_manifest.get("status") != "active":
        payload["status"] = "direct_command_binding_failed"
        payload["exit_code"] = 2
        payload["message"] = command_manifest.get(
            "message",
            "life name direct command could not be bound",
        )
        registry_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return payload
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


def ensure_life_name_command(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    canonical_name: str,
    source_command: str,
) -> dict[str, Any]:
    generated_at = _now_iso()
    command_name = _clean_name(canonical_name)
    command_error = _validate_command_name(command_name)
    command_dir = _command_dir()
    command_path = command_dir / command_name if not command_error else command_dir
    manifest_path = life_name_command_manifest_path(state_dir)
    manifest: dict[str, Any] = {
        "schema_version": LIFE_NAME_COMMAND_MANIFEST_SCHEMA,
        "status": "active" if not command_error else "blocked",
        "direct_command_enabled": not bool(command_error),
        "command_name": command_name,
        "command_dir": str(command_dir),
        "command_path": str(command_path),
        "command_on_path": _path_contains(command_dir),
        "state_dir": str(state_dir.resolve()),
        "reports_dir": str(reports_dir.resolve()),
        "receipts_dir": str(receipts_dir.resolve()),
        "source_command": source_command,
        "generated_at": generated_at,
        "life_name_command_manifest_ref": LIFE_NAME_COMMAND_MANIFEST_REF,
    }
    if command_error:
        manifest["message"] = command_error
        _write_manifest(manifest_path, manifest)
        return manifest

    try:
        command_dir.mkdir(parents=True, exist_ok=True)
        command_path.write_text(
            _direct_command_script(
                state_dir=state_dir.resolve(),
                reports_dir=reports_dir.resolve(),
                receipts_dir=receipts_dir.resolve(),
            ),
            encoding="utf-8",
        )
        command_path.chmod(0o755)
        manifest["direct_command_enabled"] = command_path.exists()
        manifest["status"] = "active" if command_path.exists() else "blocked"
        if manifest["status"] != "active":
            manifest["message"] = "life name direct command file was not created"
    except OSError as exc:
        manifest["status"] = "blocked"
        manifest["direct_command_enabled"] = False
        manifest["message"] = f"life name direct command write failed: {exc}"
    _write_manifest(manifest_path, manifest)
    return manifest


def read_life_name_command_manifest(state_dir: Path) -> dict[str, Any]:
    path = life_name_command_manifest_path(state_dir)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    if payload.get("schema_version") != LIFE_NAME_COMMAND_MANIFEST_SCHEMA:
        return {}
    return dict(payload)


def life_name_registry_path(state_dir: Path) -> Path:
    return state_dir.resolve() / "identity" / "life_name_registry.json"


def life_name_command_manifest_path(state_dir: Path) -> Path:
    return state_dir.resolve() / "identity" / "life_name_command_manifest.json"


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
    if "/" in name:
        return "life name cannot contain path separators"
    return ""


def _validate_command_name(command_name: str) -> str:
    if not command_name:
        return "life name direct command cannot be empty"
    if any(char.isspace() for char in command_name):
        return "life name direct command cannot contain whitespace"
    if command_name in {"my", "digital", "life-v0", "python", "python3"}:
        return "life name direct command cannot replace a reserved command"
    if command_name in {".", ".."}:
        return "life name direct command cannot be a relative directory marker"
    if "/" in command_name:
        return "life name direct command cannot contain path separators"
    return ""


def _command_dir() -> Path:
    configured = os.environ.get(LIFE_NAME_COMMAND_DIR_ENV, "").strip()
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".local" / "bin"


def _path_contains(command_dir: Path) -> bool:
    resolved = str(command_dir.expanduser().resolve())
    return any(
        str(Path(item).expanduser().resolve()) == resolved
        for item in os.environ.get("PATH", "").split(os.pathsep)
        if item
    )


def _direct_command_script(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
) -> str:
    return "\n".join(
        [
            "#!/bin/sh",
            "exec "
            + _shell_quote(sys.executable)
            + " -m life_v0.my_entry digital life --state "
            + _shell_quote(str(state_dir))
            + " --reports "
            + _shell_quote(str(reports_dir))
            + " --receipts "
            + _shell_quote(str(receipts_dir))
            + ' "$@"',
            "",
        ]
    )


def _shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def _write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
