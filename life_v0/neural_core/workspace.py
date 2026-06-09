from __future__ import annotations

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
