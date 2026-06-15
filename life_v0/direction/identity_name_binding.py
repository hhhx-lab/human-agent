from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from life_v0.digital_life_identity import (
    LIFE_NAME_REGISTRY_REF,
    LIFE_NAME_REGISTRY_SCHEMA,
    life_name_registry_path,
    read_life_name_registry,
)

IDENTITY_ROOT_REF = "runtime/state/direction/identity_root.json"
CONTINUITY_REFS_REF = "runtime/state/direction/continuity_refs.json"
IDENTITY_NAME_BINDING_BOUNDARY = (
    "structured_identity_name_binding_not_spoken_language"
)


def project_identity_root_with_life_name_registry(
    *,
    identity_root: dict[str, Any],
    life_name_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not identity_root:
        return {}
    if not life_name_registry:
        return identity_root
    if life_name_registry.get("schema_version") != LIFE_NAME_REGISTRY_SCHEMA:
        return identity_root

    updated = json.loads(json.dumps(identity_root))
    anchor_refs = list(updated.get("anchor_refs", []))
    if LIFE_NAME_REGISTRY_REF not in anchor_refs:
        anchor_refs.append(LIFE_NAME_REGISTRY_REF)
    updated["anchor_refs"] = anchor_refs
    updated["life_name_registry_ref"] = LIFE_NAME_REGISTRY_REF
    updated["life_name_id"] = life_name_registry.get("life_name_id")
    updated["life_name_binding_status"] = life_name_registry.get("status")
    updated["identity_name_binding_boundary"] = IDENTITY_NAME_BINDING_BOUNDARY
    return updated


def project_life_name_registry_with_identity_root(
    *,
    life_name_registry: dict[str, Any],
    identity_root: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not life_name_registry:
        return {}
    if life_name_registry.get("schema_version") != LIFE_NAME_REGISTRY_SCHEMA:
        return life_name_registry

    updated = json.loads(json.dumps(life_name_registry))
    updated["identity_root_ref"] = IDENTITY_ROOT_REF
    updated["continuity_refs_ref"] = CONTINUITY_REFS_REF
    updated["identity_name_binding_boundary"] = IDENTITY_NAME_BINDING_BOUNDARY
    if identity_root:
        updated["identity_root_schema_version"] = identity_root.get("schema_version")
        updated["identity_continuity_mode"] = identity_root.get("continuity_mode")
    return updated


def project_continuity_refs_with_life_name_registry(
    *,
    continuity_refs: dict[str, Any],
    life_name_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not continuity_refs:
        return {}
    if not life_name_registry:
        return continuity_refs
    if life_name_registry.get("schema_version") != LIFE_NAME_REGISTRY_SCHEMA:
        return continuity_refs

    updated = json.loads(json.dumps(continuity_refs))
    registry_refs = list(updated.get("life_name_registry_refs", []))
    if LIFE_NAME_REGISTRY_REF not in registry_refs:
        registry_refs.append(LIFE_NAME_REGISTRY_REF)
    updated["life_name_registry_refs"] = registry_refs
    updated["identity_name_binding_boundary"] = IDENTITY_NAME_BINDING_BOUNDARY
    return updated


def identity_name_binding_inspection_snapshot(
    *,
    identity_root: dict[str, Any] | None = None,
    life_name_registry: dict[str, Any] | None = None,
    continuity_refs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity_root = identity_root or {}
    life_name_registry = life_name_registry or {}
    continuity_refs = continuity_refs or {}
    identity_has_registry_ref = bool(
        identity_root.get("life_name_registry_ref") == LIFE_NAME_REGISTRY_REF
        or LIFE_NAME_REGISTRY_REF in identity_root.get("anchor_refs", [])
    )
    registry_has_identity_ref = bool(
        life_name_registry.get("identity_root_ref") == IDENTITY_ROOT_REF
    )
    continuity_has_registry_ref = bool(
        LIFE_NAME_REGISTRY_REF in continuity_refs.get("life_name_registry_refs", [])
    )
    return {
        "identity_name_binding_present": bool(
            identity_has_registry_ref and registry_has_identity_ref
        ),
        "identity_root_life_name_registry_ref": identity_root.get(
            "life_name_registry_ref"
        ),
        "life_name_registry_identity_root_ref": life_name_registry.get(
            "identity_root_ref"
        ),
        "continuity_refs_life_name_registry_ref_count": len(
            continuity_refs.get("life_name_registry_refs", [])
        ),
        "identity_name_binding_bidirectional": bool(
            identity_has_registry_ref
            and registry_has_identity_ref
            and continuity_has_registry_ref
        ),
        "identity_name_binding_boundary": IDENTITY_NAME_BINDING_BOUNDARY,
    }


def sync_identity_name_binding_refs(state_dir: Path) -> dict[str, Any]:
    state_dir = state_dir.resolve()
    direction_dir = state_dir / "direction"
    identity_root_path = direction_dir / "identity_root.json"
    continuity_refs_path = direction_dir / "continuity_refs.json"
    registry_path = life_name_registry_path(state_dir)

    life_name_registry = read_life_name_registry(state_dir)
    if not life_name_registry:
        return identity_name_binding_inspection_snapshot()

    identity_root = _read_json_if_exists(identity_root_path)
    continuity_refs = _read_json_if_exists(continuity_refs_path)

    refreshed_identity_root = project_identity_root_with_life_name_registry(
        identity_root=identity_root,
        life_name_registry=life_name_registry,
    )
    refreshed_registry = project_life_name_registry_with_identity_root(
        life_name_registry=life_name_registry,
        identity_root=refreshed_identity_root,
    )
    refreshed_continuity_refs = project_continuity_refs_with_life_name_registry(
        continuity_refs=continuity_refs,
        life_name_registry=life_name_registry,
    )

    if refreshed_identity_root:
        _write_json(identity_root_path, refreshed_identity_root)
    _write_json(registry_path, refreshed_registry)
    if refreshed_continuity_refs:
        _write_json(continuity_refs_path, refreshed_continuity_refs)

    return identity_name_binding_inspection_snapshot(
        identity_root=refreshed_identity_root,
        life_name_registry=refreshed_registry,
        continuity_refs=refreshed_continuity_refs,
    )


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )