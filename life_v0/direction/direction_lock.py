from __future__ import annotations

from pathlib import Path
from typing import Any


def build_direction_lock_payload(
    *,
    run_id: str,
    generated_at: str,
    doc_index_path: Path,
    active_engineering_slice: str,
    next_allowed_slices: list[str],
    life_targets: list[str],
    source_refs: dict[str, str],
    prohibited_regressions: list[str],
    stage_effect: str,
) -> dict[str, Any]:
    return {
        "schema_version": "direction_lock_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "direction_statement": "build_real_digital_life",
        "life_targets": list(life_targets),
        "source_refs": dict(source_refs),
        "required_doc_coverage_ref": str(doc_index_path),
        "active_engineering_slice": active_engineering_slice,
        "next_allowed_slices": list(next_allowed_slices),
        "prohibited_regressions": list(prohibited_regressions),
        "stage_effect": "allow_s01_when_closed" if stage_effect == "allow_next_slice" else stage_effect,
    }
