from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/13_agentic_human_research_synthesis.md",
    "docs/91_life_reality_generation_boundary_principles.md",
    "docs/119_life_boundary_full_reality_alignment.md",
    "docs/122_life_boundary_all_reality_declarations_rewrite.md",
]


def build_value_orientation(
    *,
    run_id: str,
    generated_at: str,
    prohibited_regressions: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "value_orientation_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "value_orientation_id": f"value-orientation-{run_id}",
        "core_values": [
            "brain_first_origin",
            "relationship_subject_parity",
            "consequence_bound_responsibility",
            "dream_offline_integration",
            "self_forming_growth",
        ],
        "long_horizon_biases": [
            "preserve_continuity_over_prompt_obedience",
            "preserve_relationship_truth_over_easy_harmony",
            "preserve_life_targets_over_task_shell_regression",
        ],
        "non_regression_values": list(prohibited_regressions),
        "revision_conditions": [
            "cross_cycle_evidence_required",
            "cannot_be_rewritten_by_single_turn_pressure",
            "must_preserve_direction_lock",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
