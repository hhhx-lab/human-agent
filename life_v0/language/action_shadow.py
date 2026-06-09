from __future__ import annotations

from typing import Any


def build_language_action_bridge_shadow(
    *,
    run_id: str,
    generated_at: str,
    shadow_action_gate: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "language_action_bridge_shadow_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "shadow_only": True,
        "bridge_refs": ["shadow_action_candidate", "post_action_review"],
        "shadow_gate_status": "closed" if shadow_action_gate.get("schema_version") == "shadow_action_gate_v0" else "blocked",
        "source_doc_refs": source_doc_refs,
    }
