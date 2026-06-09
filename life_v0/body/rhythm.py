from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/37_life_support_layer_policy.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_body_rhythm_pulse(
    *,
    run_id: str,
    generated_at: str,
    need_state: dict[str, Any],
    resource_budget: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "body_rhythm_pulse_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "pulse_id": f"body-rhythm-pulse-{run_id}",
        "heartbeat_counter": 0,
        "rhythm_state": "pre_activation_guarded",
        "fatigue_load": resource_budget.get("fatigue_state", {}).get("level", "managed_low_noise"),
        "allostatic_load": need_state.get("resource_deficit", "guarded_maintenance"),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_body_rhythm_pulse(pulse: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if pulse.get("schema_version") != "body_rhythm_pulse_v0":
        reasons.append("body_rhythm_gate schema mismatch")
    for field in ["pulse_id", "rhythm_state", "fatigue_load", "allostatic_load"]:
        if not pulse.get(field):
            reasons.append(f"body_rhythm_gate missing {field}")
    return reasons
