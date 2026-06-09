from __future__ import annotations

from typing import Any

from .dream_window import (
    SOURCE_DOC_REFS as DREAM_WINDOW_SOURCE_DOC_REFS,
    build_dream_experience_window,
    check_dream_experience_window,
)
from .dream_fact_gate import (
    SOURCE_DOC_REFS as DREAM_FACT_GATE_SOURCE_DOC_REFS,
    build_dream_fact_gate_decision,
    check_dream_fact_gate_decision,
)
from .offline_entry import (
    SOURCE_DOC_REFS as OFFLINE_ENTRY_SOURCE_DOC_REFS,
    build_offline_entry_gate,
    check_offline_entry_gate,
)
from .wake_integration import (
    SOURCE_DOC_REFS as WAKE_INTEGRATION_SOURCE_DOC_REFS,
    build_wake_integration_frame,
    check_wake_integration_frame,
)


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/220_life_reality_first_runner_schema_runtime_growth_fourth_cycle_reconsolidation_plan.md",
    "docs/223_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_archive_plan.md",
    "docs/228_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_activation_consolidation_plan.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]
SOURCE_DOC_REFS = sorted(
    set(
        SOURCE_DOC_REFS
        + OFFLINE_ENTRY_SOURCE_DOC_REFS
        + DREAM_WINDOW_SOURCE_DOC_REFS
        + WAKE_INTEGRATION_SOURCE_DOC_REFS
        + DREAM_FACT_GATE_SOURCE_DOC_REFS
    )
)


def build_dream_consolidation_frame(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    dream_fact_boundary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dream_consolidation_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "dream_fact_gate": "closed" if dream_fact_boundary.get("fact_gate") == "DreamFactGate" else "blocked",
        "dream_record_refs": list(life_state.get("dream_records", [])),
        "wake_integration_mode": "deferred_to_next_feedback_seed",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_offline_consolidation_frame(
    *,
    run_id: str,
    generated_at: str,
    replay_cue_bundle: dict[str, Any],
    dream_frame: dict[str, Any],
    offline_entry: dict[str, Any] | None = None,
    dream_window: dict[str, Any] | None = None,
    wake_integration: dict[str, Any] | None = None,
    dream_fact_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "offline_consolidation_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "offline_consolidation_id": f"offline-consolidation-{run_id}",
        "offline_entry_refs": ["runtime/state/dream/offline_entry_gate.json"] if offline_entry else [],
        "replay_cue_refs": ["runtime/state/replay/replay_cue_bundle.json"],
        "dream_window_refs": [
            "runtime/state/dream/dream_consolidation_frame.json",
            "runtime/state/dream/dream_experience_window.json",
        ]
        if dream_window
        else ["runtime/state/dream/dream_consolidation_frame.json"],
        "dream_fact_gate_refs": [
            "runtime/state/membrane/dream_fact_boundary.json",
            f"runtime/state/dream/dream_consolidation_frame.json#dream_fact_gate.{dream_frame.get('dream_fact_gate', 'closed')}",
        ]
        + (["runtime/state/dream/dream_fact_gate_decision.json"] if dream_fact_gate else []),
        "wake_integration_targets": [
            "runtime/state/growth/next_feedback_seed.json",
            "runtime/state/life_state.json#dream_records",
            "runtime/state/body/core_affect_vector.json",
        ],
        "wake_integration_refs": ["runtime/state/dream/wake_integration_frame.json"] if wake_integration else [],
        "growth_patch_seed_refs": list(replay_cue_bundle.get("anti_forgetting_targets", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }
