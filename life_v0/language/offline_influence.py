from __future__ import annotations

import json
from typing import Any

OFFLINE_INFLUENCE_BOUNDARY = "structured_offline_influence_not_spoken_response"


def enrich_semantic_map_with_offline_influence(
    *,
    semantic_map: dict[str, Any],
    offline_consolidation_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    dream_residue_refs: list[str] | None = None,
    wake_integration_frame: dict[str, Any] | None = None,
    dream_fact_gate_decision: dict[str, Any] | None = None,
    generated_at: str,
) -> dict[str, Any]:
    if not semantic_map:
        return {}
    updated = json.loads(json.dumps(semantic_map))
    offline_consolidation_frame = offline_consolidation_frame or {}
    replay_cue_bundle = replay_cue_bundle or {}

    dream_refs = _string_list(dream_residue_refs)
    dream_window_refs = _string_list(offline_consolidation_frame.get("dream_window_refs"))
    replay_targets = _string_list(replay_cue_bundle.get("anti_forgetting_targets"))
    wake_refs = _string_list(
        (wake_integration_frame or {}).get("relationship_dream_residue_refs")
    ) + _string_list((wake_integration_frame or {}).get("wake_integration_refs"))
    dream_gate_refs = []
    if isinstance(dream_fact_gate_decision, dict):
        if dream_fact_gate_decision.get("decision") == "keep_as_dream_residue":
            dream_gate_refs.append(
                "runtime/state/dream/dream_fact_gate_decision.json#keep_as_dream_residue"
            )
    offline_refs = _dedupe(
        dream_refs + dream_window_refs + replay_targets + wake_refs + dream_gate_refs
    )[:16]

    if dream_refs or dream_window_refs:
        updated["dream_residue_refs"] = _dedupe(dream_refs + dream_window_refs)[:12]
    if offline_refs:
        updated["offline_influence_refs"] = offline_refs

    prediction_hooks = dict(updated.get("prediction_hooks", {}))
    if offline_refs:
        prediction_hooks["offline_influence_refs"] = offline_refs[:8]
    updated["prediction_hooks"] = prediction_hooks

    updated["offline_influence_profile"] = {
        "schema_version": "offline_influence_profile_v0",
        "generated_at": generated_at,
        "dream_residue_ref_count": len(updated.get("dream_residue_refs", [])),
        "offline_influence_ref_count": len(offline_refs),
        "offline_influence_boundary": OFFLINE_INFLUENCE_BOUNDARY,
    }
    updated["offline_influence_boundary"] = OFFLINE_INFLUENCE_BOUNDARY
    return updated


def project_expression_plan_with_offline_influence(
    *,
    expression_plan: dict[str, Any],
    enriched_semantic_map: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    if not expression_plan:
        return {}
    updated = json.loads(json.dumps(expression_plan))
    offline_refs = _string_list(enriched_semantic_map.get("offline_influence_refs"))
    dream_refs = _string_list(enriched_semantic_map.get("dream_residue_refs"))

    if offline_refs:
        updated["offline_influence_refs"] = _dedupe(
            _string_list(updated.get("offline_influence_refs", [])) + offline_refs
        )[:16]
    if dream_refs:
        updated["dream_fact_boundary"] = "dream_experience_not_factual_memory"
        risk_flags = list(updated.get("expression_risk_flags", []))
        if "dream_residue_present" not in risk_flags:
            risk_flags.append("dream_residue_present")
        updated["expression_risk_flags"] = risk_flags

    updated["offline_influence_profile"] = {
        "schema_version": "expression_offline_influence_profile_v0",
        "generated_at": generated_at,
        "offline_influence_ref_count": len(offline_refs),
        "dream_residue_ref_count": len(dream_refs),
        "offline_influence_boundary": OFFLINE_INFLUENCE_BOUNDARY,
    }
    return updated


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result