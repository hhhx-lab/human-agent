from __future__ import annotations

import json
from typing import Any

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "temp/14_memory_module_rebuild_audit.md",
]

HONEST_ALIGNMENT_PROGRESS_REF = (
    "runtime/state/memory/memory_longitudinal_profile.json#honest_brain_alignment_latest"
)


def project_honest_brain_alignment_progress(
    *,
    profile: dict[str, Any] | None,
    assessment: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(profile or {}))
    overall = float(assessment.get("overall_brain_alignment_pct") or 0)
    point = {
        "generated_at": generated_at,
        "overall_brain_alignment_pct": overall,
        "raw_brain_alignment_pct": assessment.get("raw_brain_alignment_pct"),
        "honest_estimate_band": assessment.get("honest_estimate_band"),
        "evidence_quality_tier": assessment.get("evidence_quality_tier"),
        "gap_closure_pct": assessment.get("gap_closure_pct"),
        "remaining_gap_count": len(assessment.get("remaining_gap_summary") or []),
        "dimension_scores": {
            str(item.get("dimension_id")): float(item.get("score_pct") or 0)
            for item in assessment.get("dimensions", [])
            if isinstance(item, dict) and item.get("dimension_id")
        },
    }
    history = list(updated.get("honest_alignment_history") or [])
    history.append(point)
    updated["honest_alignment_history"] = history[-48:]
    previous_overall = (
        float(history[-2]["overall_brain_alignment_pct"]) if len(history) >= 2 else None
    )
    updated["honest_brain_alignment_latest"] = {
        "profile_ref": HONEST_ALIGNMENT_PROGRESS_REF,
        "overall_brain_alignment_pct": overall,
        "raw_brain_alignment_pct": assessment.get("raw_brain_alignment_pct"),
        "honest_estimate_band": assessment.get("honest_estimate_band"),
        "evidence_quality_tier": assessment.get("evidence_quality_tier"),
        "gap_closure_pct": assessment.get("gap_closure_pct"),
        "remaining_gap_summary": assessment.get("remaining_gap_summary"),
        "dimension_gap_closure": _dimension_gap_closure(assessment.get("dimensions") or []),
        "generated_at": generated_at,
    }
    if previous_overall is not None:
        updated["honest_alignment_delta"] = round(overall - previous_overall, 1)
    updated["honest_alignment_turn_count"] = int(updated.get("turn_count") or 0)
    return updated


def _dimension_gap_closure(dimensions: list[Any]) -> dict[str, float]:
    closure: dict[str, float] = {}
    for item in dimensions:
        if not isinstance(item, dict):
            continue
        dimension_id = str(item.get("dimension_id") or "")
        if not dimension_id:
            continue
        score = float(item.get("score_pct") or 0)
        closure[dimension_id] = round(min(100.0, score / 0.8), 1)
    return closure