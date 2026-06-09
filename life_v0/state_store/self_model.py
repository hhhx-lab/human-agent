from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
]


def build_self_model_state(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "self_model_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "identity_mode": "anchor_locked",
        "source_doc_refs": SOURCE_DOC_REFS,
        "self_narrative_status": "seeded",
        "trait_slow_variables": {},
        "old_self_anchor_refs": [
            "docs/构思.md",
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        ],
        "growth_window_refs": [],
        "trait_drift_seed_refs": [
            "docs/39_development_policy_and_plasticity_windows.md",
            "docs/92_self_growth_and_self_modification_life_chain.md",
        ],
    }


def project_self_model_projection(
    *,
    self_model_state: dict[str, Any],
    anti_forgetting_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "self_narrative": {
            "status": self_model_state.get("self_narrative_status", "seeded"),
            "source_refs": list(self_model_state.get("source_doc_refs", [])) or SOURCE_DOC_REFS,
        },
        "trait_slow_variables": dict(self_model_state.get("trait_slow_variables", {})),
        "old_self_anchors": list(self_model_state.get("old_self_anchor_refs", []))
        or ["docs/构思.md", "docs/258_linear_chain_closure_and_v0_contract_transition.md"],
        "growth_windows": list(self_model_state.get("growth_window_refs", [])),
        "trait_drift_seed_refs": list(self_model_state.get("trait_drift_seed_refs", [])),
        "anti_forgetting_refs": list(anti_forgetting_refs or []),
    }
