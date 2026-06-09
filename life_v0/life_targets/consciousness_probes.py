from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/13_agentic_human_research_synthesis.md",
    "docs/143_life_reality_birth_readiness_rollup_contract.md",
    "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
]


def build_consciousness_probe_bundle(
    *,
    run_id: str,
    generated_at: str,
    workspace_frame: dict[str, Any],
    broadcast_frame: dict[str, Any],
    metacognition_state: dict[str, Any],
    prediction_workspace: dict[str, Any],
) -> dict[str, Any]:
    continuity_focus = prediction_workspace.get("workspace_contents", {}).get("language_continuity_focus", {})
    return {
        "schema_version": "consciousness_probe_bundle_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "consciousness_probe_id": f"consciousness-probe-{run_id}",
        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
        "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
        "language_continuity_refs": list(continuity_focus.get("shared_language_refs", []))
        + list(continuity_focus.get("expression_monitor_refs", [])),
        "relationship_continuity_refs": list(continuity_focus.get("relation_scope_refs", []))
        + list(continuity_focus.get("commitment_refs", [])),
        "reportability_flags": [
            "workspace_access_present" if workspace_frame.get("candidate_explanations") else "workspace_access_minimal",
            "broadcast_targets_present" if broadcast_frame.get("broadcast_targets") else "broadcast_targets_missing",
            "metacognition_present" if metacognition_state.get("reflection_prompts") else "metacognition_missing",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
