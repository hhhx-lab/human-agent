from __future__ import annotations

from typing import Any


def build_identity_root(run_id: str, generated_at: str, life_targets: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "identity_root_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "identity_statement": "build_real_digital_life",
        "continuity_mode": "anchor_locked",
        "life_targets": list(life_targets),
        "source_doc_refs": [
            "docs/构思.md",
            "docs/00_research_protocol.md",
            "docs/13_agentic_human_research_synthesis.md",
            "docs/91_life_reality_generation_boundary_principles.md",
        ],
        "anchor_refs": [
            "runtime/state/direction/direction_lock.json",
            "runtime/state/direction/resume_anchor_chain.json",
        ],
    }
