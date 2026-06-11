from __future__ import annotations

import json
from typing import Any


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/13_agentic_human_research_synthesis.md",
    "docs/143_life_reality_birth_readiness_rollup_contract.md",
    "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
]


def build_workspace_frame(
    *,
    run_id: str,
    generated_at: str,
    prediction_workspace: dict[str, Any],
    network_state: dict[str, Any] | None,
    engram_index: dict[str, Any] | None,
) -> dict[str, Any]:
    workspace_contents = prediction_workspace.get("workspace_contents", {})
    return {
        "schema_version": "workspace_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "workspace_frame_id": f"workspace-frame-{run_id}",
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "candidate_explanations": list(workspace_contents.get("candidate_explanations", [])),
        "broadcast_targets": [
            "LanguageRelationshipRuntime",
            "ActionResponsibilityRuntime",
            "AffectiveSelfRuntime",
        ],
        "metacognitive_probe_refs": [
            "runtime/reports/latest/identity_birth_readiness_probe.json",
            "runtime/state/consciousness/workspace_frame.json#candidate_explanations",
        ],
        "engram_retrieval_refs": list((engram_index or {}).get("autobiographical_memory_refs", []))
        + list((engram_index or {}).get("relationship_memory_refs", []))
        or [
            "runtime/state/memory/engram_index.json#autobiographical_memory_refs",
            "runtime/state/memory/engram_index.json#relationship_memory_refs",
        ],
        "network_state_ref": (
            "runtime/state/neural_life_core/network_state.json"
            if network_state
            else None
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_workspace_frame_from_live_turn(
    *,
    workspace_frame: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_workspace_frame(workspace_frame, generated_at, run_id)
    prediction_workspace = prediction_workspace or {}
    network_state = network_state or {}
    engram_index = engram_index or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["prediction_workspace_ref"] = "runtime/state/prediction/prediction_workspace_frame.json"
    updated["network_state_ref"] = "runtime/state/neural_life_core/network_state.json"
    updated["engram_retrieval_refs"] = _dedupe(
        list(updated.get("engram_retrieval_refs", []))
        + list((engram_index or {}).get("autobiographical_memory_refs", []))
        + list((engram_index or {}).get("relationship_memory_refs", []))
        + list((engram_index or {}).get("replay_cue_refs", []))
    )
    if prediction_workspace:
        updated["candidate_explanations"] = _dedupe_dict_list(
            list(updated.get("candidate_explanations", []))
            + list(prediction_workspace.get("workspace_contents", {}).get("candidate_explanations", []))
        )
        updated["broadcast_targets"] = _dedupe(
            list(updated.get("broadcast_targets", []))
            + list(prediction_workspace.get("downstream_systems", []))
        )
        updated["prediction_workspace_contents"] = dict(
            prediction_workspace.get("workspace_contents", {})
        )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", [])) + list(live_dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    if network_state:
        updated["network_state_mode"] = list(network_state.get("active_networks", []))
    updated["metacognitive_probe_refs"] = _dedupe(
        list(updated.get("metacognitive_probe_refs", []))
        + [
            "runtime/reports/latest/identity_birth_readiness_probe.json",
            "runtime/state/consciousness/workspace_frame.json#candidate_explanations",
        ]
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _seed_missing_workspace_frame(
    workspace_frame: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if workspace_frame:
        return json.loads(json.dumps(workspace_frame))
    resolved_run_id = run_id or "resident-turn-writeback"
    return {
        "schema_version": "workspace_frame_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "workspace_frame_id": f"workspace-frame-{resolved_run_id}",
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "candidate_explanations": [],
        "broadcast_targets": [
            "LanguageRelationshipRuntime",
            "ActionResponsibilityRuntime",
            "AffectiveSelfRuntime",
        ],
        "metacognitive_probe_refs": [],
        "engram_retrieval_refs": [],
        "network_state_ref": "runtime/state/neural_life_core/network_state.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _dedupe_dict_list(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if marker not in seen:
            seen.add(marker)
            result.append(item)
    return result


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
