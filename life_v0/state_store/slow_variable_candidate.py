from __future__ import annotations

import json
from typing import Any

SLOW_VARIABLE_CANDIDATE_SCHEMA = "self_model_slow_variable_candidate_queue_v0"
SLOW_VARIABLE_CANDIDATE_BOUNDARY = (
    "structured_slow_variable_candidate_not_spoken_personality"
)
DRAMATIC_DELTA_THRESHOLD = 0.12
MIN_EXPOSURE_WINDOWS_FOR_PROMOTION = 2
MAX_INCREMENTAL_COMMIT_PER_TURN = 0.04


def project_trait_slow_variables_with_candidate_gate(
    *,
    previous_variables: dict[str, Any],
    proposed_variables: dict[str, Any],
    previous_candidates: dict[str, Any] | None = None,
    generated_at: str,
    relationship_stage: str,
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    previous_candidates = previous_candidates or {}
    evidence_refs = list(evidence_refs or [])
    committed: dict[str, Any] = {}
    candidate_entries: list[dict[str, Any]] = []
    blocked_refs: list[str] = []

    existing_by_name = _candidate_index(previous_candidates)

    for name, proposed_payload in proposed_variables.items():
        if not isinstance(proposed_payload, dict):
            continue
        previous_payload = previous_variables.get(name, {})
        if not isinstance(previous_payload, dict):
            previous_payload = {}
        previous_value = _numeric_value(previous_payload.get("value"))
        proposed_value = _numeric_value(proposed_payload.get("value"))
        if proposed_value is None:
            committed[name] = proposed_payload
            continue

        delta = 0.0 if previous_value is None else abs(proposed_value - previous_value)
        existing_candidate = existing_by_name.get(name)
        exposure_count = int((existing_candidate or {}).get("exposure_count", 0))

        if delta >= DRAMATIC_DELTA_THRESHOLD:
            exposure_count += 1
            candidate_id = str(
                (existing_candidate or {}).get("candidate_id")
                or f"slow-variable-candidate-{name}"
            )
            gate_status = (
                "promoted_multi_window"
                if exposure_count >= MIN_EXPOSURE_WINDOWS_FOR_PROMOTION
                else "blocked_dramatic_single_turn"
            )
            if exposure_count >= MIN_EXPOSURE_WINDOWS_FOR_PROMOTION:
                committed[name] = _committed_payload(
                    proposed_payload,
                    promotion_gate_status=gate_status,
                    candidate_id=candidate_id,
                )
            else:
                committed[name] = _incremental_commit_payload(
                    previous_payload=previous_payload,
                    proposed_payload=proposed_payload,
                    previous_value=previous_value,
                    proposed_value=proposed_value,
                    generated_at=generated_at,
                    relationship_stage=relationship_stage,
                    promotion_gate_status=gate_status,
                    candidate_id=candidate_id,
                )
                candidate_entries.append(
                    {
                        "candidate_id": candidate_id,
                        "variable_name": name,
                        "proposed_value": proposed_value,
                        "previous_value": previous_value,
                        "delta": round(delta, 3),
                        "exposure_count": exposure_count,
                        "first_seen_at": (existing_candidate or {}).get(
                            "first_seen_at", generated_at
                        ),
                        "last_seen_at": generated_at,
                        "last_relationship_stage": relationship_stage,
                        "promotion_gate_status": gate_status,
                        "evidence_refs": _dedupe(evidence_refs),
                        "slow_variable_candidate_boundary": SLOW_VARIABLE_CANDIDATE_BOUNDARY,
                    }
                )
                blocked_refs.append(
                    f"runtime/state/self/self_model.json#{candidate_id}"
                )
        else:
            committed[name] = _committed_payload(
                proposed_payload,
                promotion_gate_status="direct_commit_within_threshold",
            )

    return {
        "trait_slow_variables": committed,
        "trait_slow_variable_candidates": {
            "schema_version": SLOW_VARIABLE_CANDIDATE_SCHEMA,
            "generated_at": generated_at,
            "status": "closed",
            "candidates": candidate_entries,
            "blocked_update_refs": blocked_refs,
            "dramatic_delta_threshold": DRAMATIC_DELTA_THRESHOLD,
            "min_exposure_windows_for_promotion": MIN_EXPOSURE_WINDOWS_FOR_PROMOTION,
            "slow_variable_candidate_boundary": SLOW_VARIABLE_CANDIDATE_BOUNDARY,
        },
        "blocked_update_refs": blocked_refs,
    }


def slow_variable_candidate_inspection_snapshot(
    *,
    self_model_state: dict[str, Any] | None = None,
    trait_drift_monitor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    self_model_state = self_model_state or {}
    trait_drift_monitor = trait_drift_monitor or {}
    candidate_queue = self_model_state.get("trait_slow_variable_candidates", {})
    if not isinstance(candidate_queue, dict):
        candidate_queue = {}
    candidates = [
        item for item in candidate_queue.get("candidates", []) if isinstance(item, dict)
    ]
    blocked_refs = _dedupe(
        list(candidate_queue.get("blocked_update_refs", []))
        + list(trait_drift_monitor.get("blocked_update_refs", []))
    )
    return {
        "slow_variable_candidate_present": bool(candidates),
        "slow_variable_candidate_count": len(candidates),
        "slow_variable_candidate_blocked_ref_count": len(blocked_refs),
        "slow_variable_candidate_variable_names": [
            str(item.get("variable_name"))
            for item in candidates
            if item.get("variable_name")
        ][:12],
        "slow_variable_candidate_boundary": (
            candidate_queue.get("slow_variable_candidate_boundary")
            or SLOW_VARIABLE_CANDIDATE_BOUNDARY
        ),
    }


def _incremental_commit_payload(
    *,
    previous_payload: dict[str, Any],
    proposed_payload: dict[str, Any],
    previous_value: float | None,
    proposed_value: float,
    generated_at: str,
    relationship_stage: str,
    promotion_gate_status: str,
    candidate_id: str,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(proposed_payload))
    if previous_value is None:
        updated["value"] = proposed_value
    else:
        step = min(abs(proposed_value - previous_value), MAX_INCREMENTAL_COMMIT_PER_TURN)
        direction = 1.0 if proposed_value >= previous_value else -1.0
        updated["value"] = round(previous_value + step * direction, 3)
    updated["trend"] = _trend(previous_value, updated["value"])
    updated["last_generated_at"] = generated_at
    updated["last_relationship_stage"] = relationship_stage
    updated["slow_variable_update_mode"] = "candidate_gated_incremental_commit"
    updated["promotion_gate_status"] = promotion_gate_status
    updated["slow_variable_candidate_ref"] = (
        f"runtime/state/self/self_model.json#{candidate_id}"
    )
    updated["update_count"] = _int_or_zero(previous_payload.get("update_count")) + 1
    return updated


def _committed_payload(
    proposed_payload: dict[str, Any],
    *,
    promotion_gate_status: str,
    candidate_id: str | None = None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(proposed_payload))
    updated["promotion_gate_status"] = promotion_gate_status
    if candidate_id:
        updated["slow_variable_candidate_ref"] = (
            f"runtime/state/self/self_model.json#{candidate_id}"
        )
    if promotion_gate_status == "direct_commit_within_threshold":
        updated.setdefault("slow_variable_update_mode", "direct_commit_within_threshold")
    elif promotion_gate_status == "promoted_multi_window":
        updated["slow_variable_update_mode"] = "candidate_promoted_multi_window"
    return updated


def _candidate_index(previous_candidates: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for item in previous_candidates.get("candidates", []):
        if isinstance(item, dict) and item.get("variable_name"):
            index[str(item["variable_name"])] = item
    return index


def _numeric_value(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _trend(previous_value: float | None, current_value: float) -> str:
    if previous_value is None:
        return "seeded"
    if current_value > previous_value + 0.01:
        return "rising"
    if current_value < previous_value - 0.01:
        return "falling"
    return "stable"


def _int_or_zero(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return 0


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result