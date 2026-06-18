from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Literal, Mapping


BODY_INTEGRATOR_STATE_REF = "runtime/state/body/body_integrator_state.json"
BODY_INTEGRATOR_SCHEMA = "body_integrator_state_v1"
MAX_DT_MS = 300_000
DEFAULT_BACKGROUND_DT_MS = 30_000

SOURCE_DOC_REFS = [
    "docs/01n_body_interoception_allostasis_matrix.md",
    "docs/v0/动力学升级/01_硅基身体内环境.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def is_body_integrate_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_BODY_INTEGRATE"), False)


def build_body_integrator_state(
    *,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": BODY_INTEGRATOR_SCHEMA,
        "run_id": run_id,
        "generated_at": generated_at,
        "integrator_id": f"body-integrator-{run_id}",
        "status": "closed",
        "continuous": {
            "sleep_pressure": 0.12,
            "allostatic_load": 0.18,
            "body_state_debt": 0.0,
            "cognitive_bandwidth": 0.82,
            "recovery_rate": 0.08,
            "stress_pulse": 0.05,
        },
        "phase": {
            "tick_counter": 0,
            "last_integrate_at": generated_at,
            "last_integrate_mode": "seed",
        },
        "integrator_events": [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def integrate_body_state(
    *,
    integrator: dict[str, Any],
    generated_at: str,
    mode: Literal["foreground", "background", "seed"],
    dt_ms: int | None = None,
    dialogue_turn: bool = False,
    recovery_event: bool = False,
    unmerged_trace_count: int = 0,
    fatigue_level: str | None = None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(integrator or {}))
    if not updated:
        updated = build_body_integrator_state(run_id="integrator-live", generated_at=generated_at)

    continuous = dict(updated.get("continuous") or {})
    phase = dict(updated.get("phase") or {})
    last_at = str(phase.get("last_integrate_at") or "")
    resolved_dt = _resolve_dt_ms(
        last_integrate_at=last_at,
        generated_at=generated_at,
        explicit_dt_ms=dt_ms,
        mode=mode,
    )
    dt_h = resolved_dt / 3_600_000.0

    sleep_pressure = float(continuous.get("sleep_pressure", 0.0) or 0.0)
    allostatic_load = float(continuous.get("allostatic_load", 0.0) or 0.0)
    body_state_debt = float(continuous.get("body_state_debt", 0.0) or 0.0)
    cognitive_bandwidth = float(continuous.get("cognitive_bandwidth", 0.82) or 0.82)
    recovery_rate = float(continuous.get("recovery_rate", 0.08) or 0.08)
    stress_pulse = float(continuous.get("stress_pulse", 0.05) or 0.05)

    fatigue_load = _fatigue_scalar(fatigue_level)
    trace_pressure = min(1.0, unmerged_trace_count * 0.04)

    if dialogue_turn:
        stress_pulse = _clamp(stress_pulse + 0.12, 0.0, 1.0)

    sleep_pressure = _clamp(
        sleep_pressure
        + dt_h * (0.35 + trace_pressure * 0.5 + fatigue_load * 0.2)
        + (0.04 if dialogue_turn else 0.0),
        0.0,
        1.0,
    )
    recovery_quality = 0.0
    if recovery_event:
        recovery_quality = _clamp(0.25 + recovery_rate, 0.0, 0.6)
        sleep_pressure = _clamp(sleep_pressure - recovery_quality * 0.35, 0.0, 1.0)
        allostatic_load = _clamp(allostatic_load - recovery_quality * 0.2, 0.0, 1.0)
        body_state_debt = _clamp(body_state_debt - recovery_quality * 0.15, 0.0, 1.0)

    allostatic_load = _clamp(
        allostatic_load + stress_pulse * dt_h * 1.2 - recovery_rate * dt_h * 0.8,
        0.0,
        1.0,
    )
    if not recovery_event:
        body_state_debt = _clamp(
            body_state_debt + max(0.0, stress_pulse - recovery_rate) * dt_h * 0.9,
            0.0,
            1.0,
        )
    cognitive_bandwidth = _clamp(
        1.0 - allostatic_load * 0.45 - body_state_debt * 0.25 - fatigue_load * 0.2,
        0.05,
        1.0,
    )
    stress_pulse = _clamp(stress_pulse * 0.92 + (0.08 if dialogue_turn else 0.02), 0.0, 1.0)

    tick_counter = int(phase.get("tick_counter", 0) or 0) + 1
    events = list(updated.get("integrator_events") or [])
    events.append(
        {
            "event_id": f"body-integrate-{tick_counter:06d}",
            "generated_at": generated_at,
            "mode": mode,
            "dt_ms": resolved_dt,
            "dialogue_turn": dialogue_turn,
            "recovery_event": recovery_event,
            "sleep_pressure": round(sleep_pressure, 4),
            "allostatic_load": round(allostatic_load, 4),
            "body_state_debt": round(body_state_debt, 4),
        }
    )
    events = events[-32:]

    updated["schema_version"] = BODY_INTEGRATOR_SCHEMA
    updated["generated_at"] = generated_at
    updated["status"] = "closed"
    updated["continuous"] = {
        "sleep_pressure": round(sleep_pressure, 4),
        "allostatic_load": round(allostatic_load, 4),
        "body_state_debt": round(body_state_debt, 4),
        "cognitive_bandwidth": round(cognitive_bandwidth, 4),
        "recovery_rate": round(recovery_rate, 4),
        "stress_pulse": round(stress_pulse, 4),
    }
    updated["phase"] = {
        "tick_counter": tick_counter,
        "last_integrate_at": generated_at,
        "last_integrate_mode": mode,
        "last_dt_ms": resolved_dt,
    }
    updated["integrator_events"] = events
    updated.setdefault("source_doc_refs", SOURCE_DOC_REFS)
    return updated


def project_core_affect_from_integrator(
    *,
    core_affect_vector: dict[str, Any] | None,
    integrator: dict[str, Any],
    life_state: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    life_state = life_state or {}
    continuous = integrator.get("continuous") or {}
    updated = json.loads(json.dumps(core_affect_vector or {}))
    if not updated:
        updated = {
            "schema_version": "core_affect_vector_v0",
            "core_affect_id": f"core-affect-{run_id}",
        }

    pain_events = life_state.get("pain_events", [])
    dream_records = life_state.get("dream_records", [])
    relationship_subjects = life_state.get("relationship_subjects", [])
    responsibility_bindings = life_state.get("responsibility_bindings", [])

    base_pain = min(1.0, 0.1 + 0.06 * len(pain_events))
    base_relationship = min(1.0, 0.15 + 0.05 * len(relationship_subjects))
    base_dream = min(1.0, 0.12 + 0.08 * len(dream_records))
    base_responsibility = min(1.0, 0.15 + 0.07 * len(responsibility_bindings))

    allostatic_load = float(continuous.get("allostatic_load", 0.0) or 0.0)
    body_state_debt = float(continuous.get("body_state_debt", 0.0) or 0.0)
    sleep_pressure = float(continuous.get("sleep_pressure", 0.0) or 0.0)
    cognitive_bandwidth = float(continuous.get("cognitive_bandwidth", 0.82) or 0.82)

    pain_pressure = _clamp(base_pain + allostatic_load * 0.25, 0.0, 1.0)
    relationship_tension = _clamp(base_relationship + body_state_debt * 0.2, 0.0, 1.0)
    dream_residue_load = _clamp(base_dream + sleep_pressure * 0.35, 0.0, 1.0)
    responsibility_weight = _clamp(base_responsibility + allostatic_load * 0.15, 0.0, 1.0)

    valence = round(-0.08 - pain_pressure * 0.22 - body_state_debt * 0.12, 3)
    arousal = round(
        0.2
        + relationship_tension * 0.35
        + dream_residue_load * 0.18
        + allostatic_load * 0.2,
        3,
    )
    dominance = round(max(0.0, 0.58 - responsibility_weight * 0.22 - body_state_debt * 0.1), 3)

    updated.update(
        {
            "schema_version": "core_affect_vector_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "core_affect_id": updated.get("core_affect_id") or f"core-affect-{run_id}",
            "valence": valence,
            "arousal": arousal,
            "dominance": dominance,
            "pain_pressure": round(pain_pressure, 3),
            "relationship_tension": round(relationship_tension, 3),
            "dream_residue_load": round(dream_residue_load, 3),
            "responsibility_weight": round(responsibility_weight, 3),
            "repair_drive": "active" if body_state_debt > 0.25 or pain_pressure > 0.35 else "low",
            "body_integrator_ref": BODY_INTEGRATOR_STATE_REF,
            "cognitive_bandwidth_scalar": round(cognitive_bandwidth, 3),
            "source_doc_refs": list(updated.get("source_doc_refs") or SOURCE_DOC_REFS),
        }
    )
    return updated


def project_need_state_from_integrator(
    *,
    need_state_vector: dict[str, Any] | None,
    integrator: dict[str, Any],
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    continuous = integrator.get("continuous") or {}
    updated = json.loads(json.dumps(need_state_vector or {}))
    if not updated:
        updated = {
            "schema_version": "need_state_vector_v0",
            "need_vector_id": f"need-state-{run_id}",
        }

    sleep_pressure = float(continuous.get("sleep_pressure", 0.0) or 0.0)
    cognitive_bandwidth = float(continuous.get("cognitive_bandwidth", 0.82) or 0.82)
    body_state_debt = float(continuous.get("body_state_debt", 0.0) or 0.0)

    if sleep_pressure >= 0.65:
        sleep_label = "offline_ready"
    elif sleep_pressure >= 0.35:
        sleep_label = "elevated_pre_dream"
    else:
        sleep_label = "managed_pre_dream"

    if cognitive_bandwidth >= 0.7:
        bandwidth_label = "live_dialogic"
    elif cognitive_bandwidth >= 0.45:
        bandwidth_label = "guarded_dialogic"
    else:
        bandwidth_label = "narrow_guarded"

    if body_state_debt >= 0.45:
        resource_deficit = "elevated_guard"
    elif body_state_debt >= 0.2:
        resource_deficit = "guarded_maintenance"
    else:
        resource_deficit = updated.get("resource_deficit") or "guarded_maintenance"

    updated.update(
        {
            "schema_version": "need_state_vector_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "need_vector_id": updated.get("need_vector_id") or f"need-state-{run_id}",
            "sleep_pressure": sleep_label,
            "sleep_pressure_scalar": round(sleep_pressure, 4),
            "cognitive_bandwidth": bandwidth_label,
            "cognitive_bandwidth_scalar": round(cognitive_bandwidth, 4),
            "resource_deficit": resource_deficit,
            "body_state_debt_scalar": round(body_state_debt, 4),
            "body_integrator_ref": BODY_INTEGRATOR_STATE_REF,
            "source_doc_refs": list(updated.get("source_doc_refs") or []),
        }
    )
    return updated


def project_body_rhythm_from_integrator(
    *,
    body_rhythm_pulse: dict[str, Any] | None,
    integrator: dict[str, Any],
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    continuous = integrator.get("continuous") or {}
    phase = integrator.get("phase") or {}
    updated = json.loads(json.dumps(body_rhythm_pulse or {}))
    if not updated:
        updated = {
            "schema_version": "body_rhythm_pulse_v0",
            "pulse_id": f"body-rhythm-pulse-{run_id}",
        }
    updated.update(
        {
            "schema_version": "body_rhythm_pulse_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "heartbeat_counter": int(phase.get("tick_counter", 0) or 0),
            "allostatic_load": round(float(continuous.get("allostatic_load", 0.0) or 0.0), 4),
            "body_state_debt_scalar": round(float(continuous.get("body_state_debt", 0.0) or 0.0), 4),
            "body_integrator_ref": BODY_INTEGRATOR_STATE_REF,
        }
    )
    return updated


@dataclass(frozen=True)
class BodyIntegrateHookResult:
    integrator: dict[str, Any]
    core_affect_vector: dict[str, Any]
    need_state_vector: dict[str, Any]
    body_rhythm_pulse: dict[str, Any]
    applied: bool


def maybe_run_body_integrate_hook(
    *,
    body_dir: Path,
    run_id: str,
    generated_at: str,
    mode: Literal["foreground", "background"],
    write_json: Callable[[Path, dict[str, Any]], None],
    life_state: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    dialogue_turn: bool = False,
    recovery_event: bool = False,
    unmerged_trace_count: int = 0,
    fatigue_level: str | None = None,
    dt_ms: int | None = None,
    environ: Mapping[str, str] | None = None,
) -> BodyIntegrateHookResult:
    core_affect_vector = core_affect_vector or {}
    need_state_vector = need_state_vector or {}
    body_rhythm_pulse = body_rhythm_pulse or {}
    if not is_body_integrate_enabled(environ):
        integrator = _read_json(body_dir / "body_integrator_state.json")
        return BodyIntegrateHookResult(
            integrator=integrator,
            core_affect_vector=core_affect_vector,
            need_state_vector=need_state_vector,
            body_rhythm_pulse=body_rhythm_pulse,
            applied=False,
        )

    integrator = _read_json(body_dir / "body_integrator_state.json")
    if not integrator:
        integrator = build_body_integrator_state(run_id=run_id, generated_at=generated_at)

    integrator = integrate_body_state(
        integrator=integrator,
        generated_at=generated_at,
        mode=mode,
        dt_ms=dt_ms,
        dialogue_turn=dialogue_turn,
        recovery_event=recovery_event,
        unmerged_trace_count=unmerged_trace_count,
        fatigue_level=fatigue_level,
    )
    core_affect_vector = project_core_affect_from_integrator(
        core_affect_vector=core_affect_vector,
        integrator=integrator,
        life_state=life_state,
        run_id=run_id,
        generated_at=generated_at,
    )
    need_state_vector = project_need_state_from_integrator(
        need_state_vector=need_state_vector,
        integrator=integrator,
        run_id=run_id,
        generated_at=generated_at,
    )
    body_rhythm_pulse = project_body_rhythm_from_integrator(
        body_rhythm_pulse=body_rhythm_pulse,
        integrator=integrator,
        run_id=run_id,
        generated_at=generated_at,
    )

    write_json(body_dir / "body_integrator_state.json", integrator)
    write_json(body_dir / "core_affect_vector.json", core_affect_vector)
    write_json(body_dir / "need_state_vector.json", need_state_vector)
    write_json(body_dir / "body_rhythm_pulse.json", body_rhythm_pulse)

    return BodyIntegrateHookResult(
        integrator=integrator,
        core_affect_vector=core_affect_vector,
        need_state_vector=need_state_vector,
        body_rhythm_pulse=body_rhythm_pulse,
        applied=True,
    )


def check_body_integrator_state(integrator: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if integrator.get("schema_version") != BODY_INTEGRATOR_SCHEMA:
        reasons.append("body_integrator schema mismatch")
    continuous = integrator.get("continuous") or {}
    for field in (
        "sleep_pressure",
        "allostatic_load",
        "body_state_debt",
        "cognitive_bandwidth",
    ):
        if field not in continuous:
            reasons.append(f"body_integrator missing continuous.{field}")
    phase = integrator.get("phase") or {}
    if "tick_counter" not in phase:
        reasons.append("body_integrator missing phase.tick_counter")
    return reasons


def _resolve_dt_ms(
    *,
    last_integrate_at: str,
    generated_at: str,
    explicit_dt_ms: int | None,
    mode: str,
) -> int:
    if explicit_dt_ms is not None:
        return max(0, min(int(explicit_dt_ms), MAX_DT_MS))
    last_ms = _parse_iso_ms(last_integrate_at)
    now_ms = _parse_iso_ms(generated_at)
    if last_ms is not None and now_ms is not None and now_ms >= last_ms:
        return max(0, min(now_ms - last_ms, MAX_DT_MS))
    if mode == "background":
        return DEFAULT_BACKGROUND_DT_MS
    return 1_000


def _parse_iso_ms(value: str) -> int | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp() * 1000)


def _fatigue_scalar(level: str | None) -> float:
    normalized = str(level or "").strip().lower()
    if normalized in {"critical", "high"}:
        return 0.55
    if normalized in {"elevated", "managed_low_noise"}:
        return 0.3
    return 0.1


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _parse_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}