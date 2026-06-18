from __future__ import annotations

import math
from typing import Any

from life_v0.body.body_integrator import build_body_integrator_state, integrate_body_state

SOURCE_DOC_REFS = [
    "docs/v0/动力学升级/12_神经振荡扩散与Tick引擎.md",
    "docs/v0/动力学升级/13_实施波次_测试与Gate.md",
]

CONTINUOUS_FIELDS = (
    "sleep_pressure",
    "allostatic_load",
    "body_state_debt",
    "cognitive_bandwidth",
    "recovery_rate",
    "stress_pulse",
)


def run_accelerated_dynamics_audit(
    *,
    run_id: str,
    generated_at: str,
    tick_hours: int = 72,
    ticks_per_hour: int = 1,
    dt_ms: int = 3_600_000,
    dialogue_turn_every: int = 0,
    recovery_every: int = 0,
) -> dict[str, Any]:
    integrator = build_body_integrator_state(run_id=run_id, generated_at=generated_at)
    total_ticks = max(1, int(tick_hours) * max(1, int(ticks_per_hour)))
    anomalies: list[str] = []
    samples: list[dict[str, Any]] = []

    for tick in range(1, total_ticks + 1):
        tick_at = f"{generated_at}+tick{tick:04d}"
        integrator = integrate_body_state(
            integrator=integrator,
            generated_at=tick_at,
            mode="background",
            dt_ms=dt_ms,
            dialogue_turn=bool(dialogue_turn_every and tick % dialogue_turn_every == 0),
            recovery_event=bool(recovery_every and tick % recovery_every == 0),
        )
        continuous = integrator.get("continuous") or {}
        for field in CONTINUOUS_FIELDS:
            value = continuous.get(field)
            if value is None:
                continue
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                anomalies.append(f"non_finite:{field}:tick{tick}")
            if isinstance(value, (int, float)) and not 0.0 <= float(value) <= 1.0:
                if field != "cognitive_bandwidth" or float(value) < 0.05:
                    anomalies.append(f"out_of_range:{field}:tick{tick}")
        if tick in {1, total_ticks // 2, total_ticks}:
            samples.append(
                {
                    "tick": tick,
                    "tick_counter": (integrator.get("phase") or {}).get("tick_counter"),
                    "continuous": dict(continuous),
                }
            )

    phase = integrator.get("phase") or {}
    tick_counter = int(phase.get("tick_counter", 0) or 0)
    if tick_counter < total_ticks:
        anomalies.append("tick_counter_below_expected")

    return {
        "schema_version": "accelerated_dynamics_audit_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "passed" if not anomalies else "anomaly_detected",
        "audit_kind": "non_merge_gate_fixture",
        "simulated_hours": tick_hours,
        "simulated_ticks": total_ticks,
        "dt_ms": dt_ms,
        "final_tick_counter": tick_counter,
        "final_continuous": integrator.get("continuous") or {},
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:24],
        "samples": samples,
        "source_doc_refs": SOURCE_DOC_REFS,
    }