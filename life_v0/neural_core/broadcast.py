from __future__ import annotations

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
