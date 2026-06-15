from __future__ import annotations

import json
from typing import Any


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/13_agentic_human_research_synthesis.md",
    "docs/143_life_reality_birth_readiness_rollup_contract.md",
    "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
    "docs/real—live0/02_brain_network_and_workspace.md",
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


def project_consciousness_probe_bundle_from_live_turn(
    *,
    consciousness_probe_bundle: dict[str, Any],
    generated_at: str,
    workspace_frame: dict[str, Any],
    broadcast_frame: dict[str, Any],
    metacognition_state: dict[str, Any],
    prediction_workspace: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    run_id: str | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_consciousness_probe_bundle(
        consciousness_probe_bundle,
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        metacognition_state=metacognition_state,
        prediction_workspace=prediction_workspace or {},
        generated_at=generated_at,
        run_id=run_id,
    )
    prediction_workspace = prediction_workspace or {}
    expression_plan = expression_plan or {}
    commitment_truth_state = commitment_truth_state or {}
    continuity_focus = prediction_workspace.get("workspace_contents", {}).get(
        "language_continuity_focus", {}
    )
    if not isinstance(continuity_focus, dict):
        continuity_focus = {}

    language_continuity_refs = _dedupe(
        list(continuity_focus.get("shared_language_refs", []))
        + list(continuity_focus.get("expression_monitor_refs", []))
        + list(live_language_turn_refs or [])
        + (
            ["runtime/state/language/expression_plan.json"]
            if expression_plan
            else []
        )
    )
    relationship_continuity_refs = _dedupe(
        list(continuity_focus.get("relation_scope_refs", []))
        + list(continuity_focus.get("commitment_refs", []))
        + list(commitment_truth_state.get("open_commitment_refs", []))
        + list(commitment_truth_state.get("repair_required_refs", []))
    )
    reportability_flags = [
        (
            "workspace_access_present"
            if workspace_frame.get("candidate_explanations")
            else "workspace_access_minimal"
        ),
        (
            "broadcast_targets_present"
            if broadcast_frame.get("broadcast_targets")
            else "broadcast_targets_missing"
        ),
        (
            "metacognition_present"
            if metacognition_state.get("reflection_prompts")
            or metacognition_state.get("uncertainty_flags")
            else "metacognition_missing"
        ),
    ]
    if metacognition_state.get("uncertainty_flags"):
        reportability_flags.append("metacognitive_uncertainty_monitoring")
    if broadcast_frame.get("live_turn_focus") or live_turn_focus:
        reportability_flags.append("live_turn_broadcast_context_present")

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["workspace_frame_ref"] = "runtime/state/consciousness/workspace_frame.json"
    updated["broadcast_frame_ref"] = "runtime/state/consciousness/broadcast_frame.json"
    updated["metacognition_ref"] = "runtime/state/consciousness/metacognition_state.json"
    updated["language_continuity_refs"] = language_continuity_refs
    updated["relationship_continuity_refs"] = relationship_continuity_refs
    updated["reportability_flags"] = _dedupe(reportability_flags)
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", [])) + list(live_language_turn_refs or [])
    )
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", [])) + list(live_dialogue_turn_refs or [])
    )
    updated["metacognition_uncertainty_flags"] = _dedupe(
        list(metacognition_state.get("uncertainty_flags", []))
    )
    updated["broadcast_target_count"] = len(
        list(broadcast_frame.get("broadcast_targets", []))
    )
    updated["source_doc_refs"] = _dedupe(list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS)
    updated["last_projected_from_live_turn_ref"] = broadcast_frame.get(
        "last_projected_from_live_turn_ref"
    )
    updated["probe_boundary"] = "consciousness_probe_live_turn_evidence_not_spoken_language"
    return updated


def _seed_missing_consciousness_probe_bundle(
    consciousness_probe_bundle: dict[str, Any],
    *,
    workspace_frame: dict[str, Any],
    broadcast_frame: dict[str, Any],
    metacognition_state: dict[str, Any],
    prediction_workspace: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if consciousness_probe_bundle:
        return json.loads(json.dumps(consciousness_probe_bundle))
    resolved_run_id = run_id or "resident-turn-writeback"
    return build_consciousness_probe_bundle(
        run_id=resolved_run_id,
        generated_at=generated_at,
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        metacognition_state=metacognition_state,
        prediction_workspace=prediction_workspace,
    )


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(str(item))
    return result
