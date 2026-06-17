from __future__ import annotations

import json
import os
import gzip
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_HOT_JSONL_MAX_BYTES = 64 * 1024 * 1024
DEFAULT_HOT_JSONL_TAIL_EVENTS = 512
DEFAULT_ARCHIVE_DIR_REF = "runtime/archive/resource_budget"


def append_jsonl_with_hot_budget(
    path: Path,
    payload: dict[str, Any],
    *,
    max_bytes: int = DEFAULT_HOT_JSONL_MAX_BYTES,
    tail_events: int = DEFAULT_HOT_JSONL_TAIL_EVENTS,
    archive_dir: Path | None = None,
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    rotation = rotate_hot_jsonl_if_needed(
        path,
        max_bytes=max_bytes,
        tail_events=tail_events,
        archive_dir=archive_dir,
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return {
        "schema_version": "hot_jsonl_append_budget_result_v0",
        "path": str(path),
        "rotated": bool(rotation),
        "rotation": rotation,
    }


def rotate_hot_jsonl_if_needed(
    path: Path,
    *,
    max_bytes: int = DEFAULT_HOT_JSONL_MAX_BYTES,
    tail_events: int = DEFAULT_HOT_JSONL_TAIL_EVENTS,
    archive_dir: Path | None = None,
) -> dict[str, Any]:
    if max_bytes <= 0 or not path.exists():
        return {}
    try:
        current_size = path.stat().st_size
    except OSError:
        return {}
    if current_size <= max_bytes:
        return {}

    archive_root = archive_dir or _default_archive_dir(path)
    archive_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    archive_path = archive_root / f"{path.stem}.{stamp}.{os.getpid()}.jsonl.gz"
    summary_path = archive_root / f"{path.stem}.{stamp}.{os.getpid()}.summary.json"

    tail, observed_count, latest_counter = _read_tail_lines(
        path,
        tail_events=max(tail_events, 0),
    )
    with path.open("rb") as source, gzip.open(archive_path, "wb", compresslevel=6) as target:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            target.write(chunk)
    path.unlink(missing_ok=True)
    if tail:
        path.write_text("".join(tail), encoding="utf-8")
    else:
        path.write_text("", encoding="utf-8")

    summary = {
        "schema_version": "hot_jsonl_rotation_summary_v0",
        "rotated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hot_path": str(path),
        "archive_path": str(archive_path),
        "previous_size_bytes": current_size,
        "observed_event_count": observed_count,
        "preserved_tail_event_count": len(tail),
        "latest_counter": latest_counter,
        "max_hot_bytes": max_bytes,
        "tail_event_budget": tail_events,
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def count_jsonl_events(path: Path) -> int:
    count = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    count += 1
    except OSError:
        return 0
    return count


def count_jsonl_events_or_latest_counter(path: Path, *, counter_key: str) -> int:
    line_count = 0
    latest_counter = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                line_count += 1
                try:
                    event = json.loads(line)
                except (TypeError, ValueError):
                    continue
                if isinstance(event, dict):
                    latest_counter = max(latest_counter, _int_or_zero(event.get(counter_key)))
    except OSError:
        return 0
    return max(line_count, latest_counter)


def max_jsonl_int_field(path: Path, *, field_name: str) -> int:
    max_value = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except (TypeError, ValueError):
                    continue
                if isinstance(event, dict):
                    max_value = max(max_value, _int_or_zero(event.get(field_name)))
    except OSError:
        return 0
    return max_value


def _read_tail_lines(
    path: Path,
    *,
    tail_events: int,
) -> tuple[list[str], int, int]:
    tail: deque[str] = deque(maxlen=tail_events)
    observed_count = 0
    latest_counter = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                observed_count += 1
                tail.append(line)
                try:
                    event = json.loads(line)
                except (TypeError, ValueError):
                    continue
                if isinstance(event, dict):
                    latest_counter = max(
                        latest_counter,
                        _int_or_zero(event.get("heartbeat_counter")),
                        _int_or_zero(event.get("activity_sequence")),
                    )
    except OSError:
        return [], observed_count, latest_counter

    return list(tail), observed_count, latest_counter


def _default_archive_dir(path: Path) -> Path:
    parts = list(path.parts)
    if "runtime" in parts:
        runtime_index = parts.index("runtime")
        runtime_root = Path(*parts[: runtime_index + 1])
        return runtime_root / "archive" / "resource_budget"
    return path.parent / "resource_budget_archive"


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
