from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/22_state_transition_and_threshold_model.md",
]


def build_metacognition_state(
    *,
    run_id: str,
    generated_at: str,
    broadcast_frame: dict[str, Any],
    workspace_frame: dict[str, Any],
) -> dict[str, Any]:
    retrieval_refs = list(workspace_frame.get("engram_retrieval_refs", []))
    return {
        "schema_version": "metacognition_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "metacognition_id": f"metacognition-{run_id}",
        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
        "uncertainty_flags": ["semantic-ambiguity-monitoring"] if retrieval_refs else [],
        "expression_risk_refs": ["runtime/state/language/expression_monitor_state.json"],
        "relationship_tension_refs": ["runtime/state/relationship/commitment_truth_state.json#repair_required_refs"],
        "reflection_prompts": [
            "当前工作区内容是否足以形成可报告意识证据",
            "当前表达是否会损伤关系连续体",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
        "broadcast_targets": list(broadcast_frame.get("broadcast_targets", [])),
    }
