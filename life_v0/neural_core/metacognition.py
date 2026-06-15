from __future__ import annotations

import json
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


def project_metacognition_state_from_live_turn(
    *,
    metacognition_state: dict[str, Any],
    generated_at: str,
    broadcast_frame: dict[str, Any],
    workspace_frame: dict[str, Any],
    run_id: str | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    expression_monitor_state: dict[str, Any] | None = None,
    live_turn_focus: str | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_metacognition_state(
        metacognition_state,
        broadcast_frame=broadcast_frame,
        workspace_frame=workspace_frame,
        generated_at=generated_at,
        run_id=run_id,
    )
    memory_retrieval_frame = memory_retrieval_frame or {}
    expression_monitor_state = expression_monitor_state or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["broadcast_frame_ref"] = "runtime/state/consciousness/broadcast_frame.json"
    updated["workspace_frame_ref"] = "runtime/state/consciousness/workspace_frame.json"
    updated["broadcast_targets"] = _dedupe(
        list(broadcast_frame.get("broadcast_targets", []))
        + list(workspace_frame.get("broadcast_targets", []))
    )
    updated["uncertainty_flags"] = _uncertainty_flags(
        workspace_frame=workspace_frame,
        memory_retrieval_frame=memory_retrieval_frame,
        expression_monitor_state=expression_monitor_state,
    )
    updated["expression_risk_refs"] = _dedupe(
        list(updated.get("expression_risk_refs", []))
        + ["runtime/state/language/expression_monitor_state.json"]
    )
    if expression_monitor_state.get("release_caution_level"):
        updated["expression_release_caution_level"] = expression_monitor_state.get(
            "release_caution_level"
        )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    if memory_retrieval_frame.get("reconstruction_focus"):
        updated["memory_reconstruction_focus"] = memory_retrieval_frame.get(
            "reconstruction_focus"
        )
    updated["memory_retrieval_frame_ref"] = (
        "runtime/state/memory/memory_retrieval_frame.json"
        if memory_retrieval_frame
        else updated.get("memory_retrieval_frame_ref")
    )
    updated["source_doc_refs"] = _dedupe(list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS)
    updated["last_projected_from_live_turn_ref"] = broadcast_frame.get(
        "last_projected_from_live_turn_ref"
    )
    return updated


def _seed_missing_metacognition_state(
    metacognition_state: dict[str, Any],
    *,
    broadcast_frame: dict[str, Any],
    workspace_frame: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if metacognition_state:
        return json.loads(json.dumps(metacognition_state))
    resolved_run_id = run_id or "resident-turn-writeback"
    return build_metacognition_state(
        run_id=resolved_run_id,
        generated_at=generated_at,
        broadcast_frame=broadcast_frame,
        workspace_frame=workspace_frame,
    )


def _uncertainty_flags(
    *,
    workspace_frame: dict[str, Any],
    memory_retrieval_frame: dict[str, Any],
    expression_monitor_state: dict[str, Any],
) -> list[str]:
    flags: list[str] = []
    retrieval_refs = list(workspace_frame.get("engram_retrieval_refs", []))
    if retrieval_refs:
        flags.append("semantic-ambiguity-monitoring")
    if memory_retrieval_frame.get("blocked_or_quarantined_refs"):
        flags.append("memory-quarantine-monitoring")
    if memory_retrieval_frame.get("reconstruction_focus"):
        flags.append("reconstructive-recall-monitoring")
    if expression_monitor_state.get("delay_or_release_decision") == "delay_for_clarification":
        flags.append("expression-clarification-monitoring")
    return _dedupe(flags)


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
