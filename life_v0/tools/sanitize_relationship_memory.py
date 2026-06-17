from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from life_v0.state_store.relation_identity_hygiene import sanitize_observed_names


MEMORY_FILES = (
    "memory/relationship_memory.json",
    "memory/dialogue_memory_summary.json",
)


def sanitize_runtime_memory_files(*, state_dir: Path) -> dict[str, Any]:
    sanitized_files: list[dict[str, Any]] = []
    for relative_path in MEMORY_FILES:
        path = state_dir / relative_path
        payload = _read_json(path)
        if not payload:
            continue
        profile = payload.get("relation_person_profile")
        if not isinstance(profile, dict):
            continue
        before = list(profile.get("observed_names", []))
        after = sanitize_observed_names(before)
        if before == after:
            continue
        profile["observed_names"] = after
        _write_json(path, payload)
        sanitized_files.append(
            {
                "path": str(path),
                "before_count": len(before),
                "after_count": len(after),
                "removed_count": max(0, len(before) - len(after)),
            }
        )
    return {
        "schema_version": "sanitize_relationship_memory_report_v0",
        "state_dir": str(state_dir),
        "sanitized_file_count": len(sanitized_files),
        "sanitized_files": sanitized_files,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state",
        type=Path,
        default=Path("runtime/state"),
        help="Runtime state directory containing memory/*.json.",
    )
    args = parser.parse_args(argv)
    report = sanitize_runtime_memory_files(state_dir=args.state)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _read_json(path: Path) -> dict[str, Any]:
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
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
