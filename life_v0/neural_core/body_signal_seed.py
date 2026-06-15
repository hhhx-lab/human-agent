from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BODY_RESOURCE_BUDGET_REF = "runtime/state/body/body_resource_budget.json"
CORE_AFFECT_VECTOR_REF = "runtime/state/body/core_affect_vector.json"
NEURAL_CORE_BODY_SIGNAL_SEED_BOUNDARY = (
    "neural_core_pre_activation_body_signal_seed_not_spoken_language"
)

SOURCE_DOC_REFS = [
    "docs/real—live0/03_body_affect_homeostasis.md",
    "docs/real—live0/12_neuromodulation_signal_media.md",
    "docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md",
]


def build_neural_core_body_resource_budget_seed(
    *,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": "body_resource_budget_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": "S02_NEURAL_LIFE_CORE",
        "body_mode": "pre_activation_guarded_body",
        "need_state_ref": "runtime/state/body/need_state_vector.json",
        "rhythm_ref": "runtime/state/body/body_rhythm_pulse.json",
        "recovery_path_ref": "runtime/state/body/recovery_path.json",
        "energy_state": {
            "level": "guarded_reserve",
            "reserve_fraction": 0.72,
            "direction_lock_mode": "preserve_core_continuity_before_activation",
        },
        "fatigue_state": {"level": "managed_pre_dream"},
        "maintenance_pressure": {
            "repair_drive": "low",
            "resource_deficit": "guarded_maintenance",
        },
        "body_signal_seed_mode": "neural_core_pre_activation_seed",
        "body_signal_seed_boundary": NEURAL_CORE_BODY_SIGNAL_SEED_BOUNDARY,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_neural_core_core_affect_seed(
    *,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": "core_affect_vector_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "core_affect_id": f"core-affect-{run_id}",
        "valence": -0.05,
        "arousal": 0.28,
        "dominance": 0.52,
        "pain_pressure": 0.12,
        "relationship_tension": 0.18,
        "dream_residue_load": 0.14,
        "responsibility_weight": 0.16,
        "repair_drive": "low",
        "body_signal_seed_mode": "neural_core_pre_activation_seed",
        "body_signal_seed_boundary": NEURAL_CORE_BODY_SIGNAL_SEED_BOUNDARY,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def resolve_body_signal_inputs_for_neural_core(
    *,
    state_root: Path,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    state_root = state_root.resolve()
    body_dir = state_root / "body"
    budget_path = body_dir / "body_resource_budget.json"
    affect_path = body_dir / "core_affect_vector.json"

    body_resource_budget = _read_json_if_exists(budget_path)
    core_affect_vector = _read_json_if_exists(affect_path)
    seeded = False

    if not body_resource_budget:
        body_resource_budget = build_neural_core_body_resource_budget_seed(
            run_id=run_id,
            generated_at=generated_at,
        )
        seeded = True
    if not core_affect_vector:
        core_affect_vector = build_neural_core_core_affect_seed(
            run_id=run_id,
            generated_at=generated_at,
        )
        seeded = True

    return {
        "body_resource_budget": body_resource_budget,
        "core_affect_vector": core_affect_vector,
        "body_resource_budget_ref": BODY_RESOURCE_BUDGET_REF,
        "core_affect_vector_ref": CORE_AFFECT_VECTOR_REF,
        "body_signal_seed_applied": seeded,
        "body_signal_seed_boundary": NEURAL_CORE_BODY_SIGNAL_SEED_BOUNDARY,
    }


def write_neural_core_body_signal_seed_artifacts(
    *,
    state_root: Path,
    body_resource_budget: dict[str, Any],
    core_affect_vector: dict[str, Any],
    only_if_missing: bool = True,
) -> list[str]:
    state_root = state_root.resolve()
    body_dir = state_root / "body"
    body_dir.mkdir(parents=True, exist_ok=True)
    written_refs: list[str] = []
    budget_path = body_dir / "body_resource_budget.json"
    affect_path = body_dir / "core_affect_vector.json"

    if body_resource_budget and (not only_if_missing or not budget_path.exists()):
        _write_json(budget_path, body_resource_budget)
        written_refs.append(BODY_RESOURCE_BUDGET_REF)
    if core_affect_vector and (not only_if_missing or not affect_path.exists()):
        _write_json(affect_path, core_affect_vector)
        written_refs.append(CORE_AFFECT_VECTOR_REF)
    return written_refs


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )