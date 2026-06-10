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
    queue_e_birth_repair_profile: dict[str, Any] | None = None,
    queue_e_birth_repair_profile_ref: str | None = None,
    queue_e_birth_repair_refs: list[str] | None = None,
) -> dict[str, Any]:
    queue_e_birth_repair_profile = queue_e_birth_repair_profile or {}
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
        "queue_e_birth_repair_profile_ref": queue_e_birth_repair_profile_ref,
        "queue_e_birth_repair_pressure_level": queue_e_birth_repair_profile.get("pressure_level"),
        "queue_e_birth_repair_attention_target": queue_e_birth_repair_profile.get("attention_target"),
        "queue_e_birth_repair_ref_set": list(queue_e_birth_repair_refs or []),
    }
