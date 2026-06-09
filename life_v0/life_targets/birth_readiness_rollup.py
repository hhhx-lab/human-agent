from __future__ import annotations

from typing import Any


def build_birth_readiness_rollup(
    *,
    run_id: str,
    generated_at: str,
    overall_status: str,
    target_status: dict[str, str],
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "birth_readiness_rollup_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "overall_status": overall_status,
        "life_target_status": target_status,
        "blocked_reasons": list(blocked_reasons),
        "quarantine_refs": [],
        "replay_needed_refs": [],
        "archive_receipt_ref": receipt_ref,
    }
