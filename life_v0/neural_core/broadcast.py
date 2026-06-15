from __future__ import annotations

import json
from typing import Any


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/13_agentic_human_research_synthesis.md",
]


def build_broadcast_frame(
    *,
    run_id: str,
    generated_at: str,
    workspace_frame: dict[str, Any],
) -> dict[str, Any]:
    candidate_explanations = list(workspace_frame.get("candidate_explanations", []))
    return {
        "schema_version": "broadcast_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "broadcast_frame_id": f"broadcast-frame-{run_id}",
        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
        "broadcast_targets": list(workspace_frame.get("broadcast_targets", []))
        or ["LanguageRelationshipRuntime", "ActionResponsibilityRuntime", "AffectiveSelfRuntime"],
        "salience_ranking": [
            {
                "rank": index + 1,
                "candidate_ref": explanation.get("explanation_id"),
            }
            for index, explanation in enumerate(candidate_explanations)
        ],
        "suppressed_content_refs": [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_broadcast_frame_from_live_turn(
    *,
    broadcast_frame: dict[str, Any],
    generated_at: str,
    workspace_frame: dict[str, Any],
    run_id: str | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_broadcast_frame(
        broadcast_frame,
        workspace_frame=workspace_frame,
        generated_at=generated_at,
        run_id=run_id,
    )
    candidate_explanations = list(workspace_frame.get("candidate_explanations", []))
    broadcast_targets = list(workspace_frame.get("broadcast_targets", [])) or list(
        updated.get("broadcast_targets", [])
    )

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["workspace_frame_ref"] = "runtime/state/consciousness/workspace_frame.json"
    updated["broadcast_targets"] = _dedupe(broadcast_targets)
    updated["salience_ranking"] = [
        {
            "rank": index + 1,
            "candidate_ref": explanation.get("explanation_id"),
            "focus": explanation.get("focus"),
        }
        for index, explanation in enumerate(candidate_explanations)
        if isinstance(explanation, dict)
    ]
    updated["suppressed_content_refs"] = _suppressed_explanation_refs(candidate_explanations)
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", [])) + list(live_dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    updated["source_doc_refs"] = _dedupe(list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS)
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _seed_missing_broadcast_frame(
    broadcast_frame: dict[str, Any],
    *,
    workspace_frame: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if broadcast_frame:
        return json.loads(json.dumps(broadcast_frame))
    resolved_run_id = run_id or "resident-turn-writeback"
    return build_broadcast_frame(
        run_id=resolved_run_id,
        generated_at=generated_at,
        workspace_frame=workspace_frame,
    )


def _suppressed_explanation_refs(candidate_explanations: list[dict[str, Any]]) -> list[str]:
    if len(candidate_explanations) <= 2:
        return []
    suppressed: list[str] = []
    for explanation in candidate_explanations[2:]:
        if not isinstance(explanation, dict):
            continue
        explanation_id = explanation.get("explanation_id")
        if explanation_id:
            suppressed.append(str(explanation_id))
    return suppressed


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
