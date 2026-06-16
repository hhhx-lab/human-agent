from __future__ import annotations

import json
from typing import Any

MEMORY_RECALL_ENRICHMENT_BOUNDARY = (
    "structured_memory_recall_enrichment_not_spoken_response"
)


def enrich_semantic_map_with_memory_recall(
    *,
    semantic_map: dict[str, Any],
    memory_retrieval_frame: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    if not semantic_map:
        return {}
    updated = json.loads(json.dumps(semantic_map))
    activated_refs = _string_list(memory_retrieval_frame.get("activated_engram_refs"))
    cue_terms = _string_list(memory_retrieval_frame.get("cue_terms"))
    reconstruction_focus = _reconstruction_focus(memory_retrieval_frame)

    updated["memory_recall_refs"] = activated_refs[:16]
    updated["memory_reconstruction_focus"] = reconstruction_focus
    if cue_terms:
        updated["memory_cue_terms"] = cue_terms[:12]

    prediction_hooks = dict(updated.get("prediction_hooks", {}))
    if activated_refs:
        prediction_hooks["memory_recall_refs"] = [
            MEMORY_RETRIEVAL_FRAME_REF + "#activated_engram_refs"
        ]
    if reconstruction_focus:
        prediction_hooks["memory_reconstruction_focus"] = reconstruction_focus
    updated["prediction_hooks"] = prediction_hooks

    if activated_refs and updated.get("semantic_focus") == "relational_checkin":
        updated["semantic_focus"] = "memory_grounded_relational_recall"

    updated["memory_recall_enrichment_profile"] = {
        "schema_version": "memory_recall_enrichment_profile_v0",
        "generated_at": generated_at,
        "activated_engram_ref_count": len(activated_refs),
        "cue_term_count": len(cue_terms),
        "reconstruction_focus": reconstruction_focus,
        "memory_retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "memory_recall_enrichment_boundary": MEMORY_RECALL_ENRICHMENT_BOUNDARY,
    }
    updated["memory_recall_enrichment_boundary"] = MEMORY_RECALL_ENRICHMENT_BOUNDARY
    return updated


def project_expression_plan_with_memory_grounding(
    *,
    expression_plan: dict[str, Any],
    memory_retrieval_frame: dict[str, Any],
    enriched_semantic_map: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    if not expression_plan:
        return {}
    updated = json.loads(json.dumps(expression_plan))
    activated_refs = _string_list(memory_retrieval_frame.get("activated_engram_refs"))
    recall_refs = _string_list(enriched_semantic_map.get("memory_recall_refs"))
    grounding_refs = _dedupe(activated_refs + recall_refs)[:16]

    updated["memory_grounding_refs"] = grounding_refs
    updated["memory_reconstruction_focus"] = enriched_semantic_map.get(
        "memory_reconstruction_focus"
    )
    updated["semantic_goal"] = enriched_semantic_map.get(
        "semantic_focus", updated.get("semantic_goal")
    )

    risk_flags = list(updated.get("expression_risk_flags", []))
    if grounding_refs and "memory_grounding_present" not in risk_flags:
        risk_flags.append("memory_grounding_present")
    updated["expression_risk_flags"] = risk_flags

    recall_profile = memory_retrieval_frame.get("recall_to_expression_profile")
    if isinstance(recall_profile, dict):
        updated["memory_recall_to_expression_profile_ref"] = recall_profile.get(
            "profile_ref"
        )

    updated["memory_grounding_profile"] = {
        "schema_version": "memory_grounding_profile_v0",
        "generated_at": generated_at,
        "grounding_ref_count": len(grounding_refs),
        "memory_retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "memory_grounding_boundary": MEMORY_RECALL_ENRICHMENT_BOUNDARY,
    }
    return updated


MEMORY_RETRIEVAL_FRAME_REF = "runtime/state/memory/memory_retrieval_frame.json"


def _reconstruction_focus(memory_retrieval_frame: dict[str, Any]) -> str | None:
    recall_profile = memory_retrieval_frame.get("recall_to_expression_profile")
    if isinstance(recall_profile, dict):
        families = _string_list(recall_profile.get("expression_influence_families"))
        if families:
            return families[0]
    reconstruction = memory_retrieval_frame.get("reconstruction_inputs")
    if isinstance(reconstruction, dict):
        focus = reconstruction.get("reconstruction_focus")
        if focus:
            return str(focus)
    cue_terms = _string_list(memory_retrieval_frame.get("cue_terms"))
    if cue_terms:
        return f"cue:{cue_terms[0]}"
    return None


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