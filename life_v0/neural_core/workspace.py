from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from typing import Any, Mapping


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/13_agentic_human_research_synthesis.md",
    "docs/143_life_reality_birth_readiness_rollup_contract.md",
    "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
    "docs/v0/动力学升级/03_意识工作区与广播.md",
]

WORKSPACE_K_MAX = 5


def is_workspace_topk_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_WORKSPACE_TOPK"), False)


@dataclass(frozen=True)
class WorkspaceTopKResult:
    winners: list[dict[str, Any]]
    evicted: list[dict[str, Any]]
    k: int
    applied: bool


def resolve_workspace_k(
    *,
    k_max: int = WORKSPACE_K_MAX,
    cognitive_bandwidth: float = 0.82,
    fatigue_load: float = 0.0,
) -> int:
    bandwidth = max(0.05, min(1.0, float(cognitive_bandwidth or 0.82)))
    fatigue = max(0.0, min(1.0, float(fatigue_load or 0.0)))
    resolved = int(math.floor(k_max * bandwidth * (1.0 - fatigue * 0.35)))
    return max(1, min(k_max, resolved))


def apply_workspace_topk(
    candidates: list[dict[str, Any]],
    *,
    k: int,
    allostatic_load: float = 0.0,
    live_turn_focus: str | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
) -> WorkspaceTopKResult:
    normalized = [
        dict(candidate)
        for candidate in candidates
        if isinstance(candidate, dict) and candidate.get("explanation_id")
    ]
    if not normalized:
        return WorkspaceTopKResult(winners=[], evicted=[], k=max(1, k), applied=False)

    scored: list[tuple[float, dict[str, Any]]] = []
    for candidate in normalized:
        score = score_workspace_candidate(
            candidate,
            allostatic_load=allostatic_load,
            live_turn_focus=live_turn_focus,
            memory_retrieval_frame=memory_retrieval_frame,
        )
        payload = dict(candidate)
        payload["salience_score"] = score
        scored.append((score, payload))

    scored.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("explanation_id") or ""),
        )
    )
    limit = max(1, min(int(k), len(scored)))
    winners = [item[1] for item in scored[:limit]]
    evicted = [item[1] for item in scored[limit:]]
    return WorkspaceTopKResult(
        winners=winners,
        evicted=evicted,
        k=limit,
        applied=len(evicted) > 0 or len(winners) < len(normalized),
    )


def score_workspace_candidate(
    candidate: dict[str, Any],
    *,
    allostatic_load: float = 0.0,
    live_turn_focus: str | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
) -> float:
    base = float(candidate.get("salience_score") or 0.5)
    focus = str(candidate.get("focus") or "")
    family = str(candidate.get("explanation_family") or "")
    lowered = focus.lower()
    if any(token in lowered for token in ("repair", "clarif", "commitment")):
        base += 0.14
    if any(token in lowered for token in ("relationship", "continuity")):
        base += 0.08
    if family == "language_semantic_handoff":
        base += 0.06
    if live_turn_focus and focus and focus == live_turn_focus:
        base += 0.12

    retrieval = memory_retrieval_frame or {}
    reconstructive = retrieval.get("reconstructive_recall_profile") or {}
    mean_activation = float(reconstructive.get("mean_activation_score") or 0.0)
    if mean_activation > 0:
        base += min(0.1, mean_activation * 0.12)

    base -= float(allostatic_load or 0.0) * 0.18
    return round(max(0.0, min(1.0, base)), 3)


def maybe_apply_workspace_topk_to_frame(
    workspace_frame: dict[str, Any],
    *,
    body_integrator: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    live_turn_focus: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    updated = dict(workspace_frame or {})
    if not is_workspace_topk_enabled(environ):
        return updated

    continuous = (body_integrator or {}).get("continuous") or {}
    modulation = (signal_media_runtime or {}).get("modulation_vector") or {}
    cognitive_bandwidth = float(continuous.get("cognitive_bandwidth", 0.82) or 0.82)
    fatigue_load = float(modulation.get("fatigue_load", 0.0) or 0.0)
    allostatic_load = float(continuous.get("allostatic_load", 0.0) or 0.0)

    candidates = _collect_workspace_candidates(
        workspace_frame=updated,
        prediction_error_field=prediction_error_field,
        memory_retrieval_frame=memory_retrieval_frame,
    )
    k = resolve_workspace_k(
        cognitive_bandwidth=cognitive_bandwidth,
        fatigue_load=fatigue_load,
    )
    topk = apply_workspace_topk(
        candidates,
        k=k,
        allostatic_load=allostatic_load,
        live_turn_focus=live_turn_focus or updated.get("live_turn_focus"),
        memory_retrieval_frame=memory_retrieval_frame,
    )
    updated["candidate_explanations"] = topk.winners
    updated["workspace_topk_applied"] = topk.applied
    updated["workspace_topk"] = {
        "schema_version": "workspace_topk_v1",
        "k": topk.k,
        "k_max": WORKSPACE_K_MAX,
        "cognitive_bandwidth": round(cognitive_bandwidth, 3),
        "fatigue_load": round(fatigue_load, 3),
        "allostatic_load": round(allostatic_load, 3),
        "winner_count": len(topk.winners),
        "evicted_count": len(topk.evicted),
        "evicted_candidate_refs": [
            str(item.get("explanation_id"))
            for item in topk.evicted
            if item.get("explanation_id")
        ],
        "suppressed_candidates": topk.evicted,
    }
    return updated


def _collect_workspace_candidates(
    *,
    workspace_frame: dict[str, Any],
    prediction_error_field: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    candidates = [
        dict(item)
        for item in workspace_frame.get("candidate_explanations", [])
        if isinstance(item, dict)
    ]
    for event in (prediction_error_field or {}).get("error_events", []):
        if not isinstance(event, dict):
            continue
        error_id = str(event.get("error_id") or "")
        if not error_id:
            continue
        candidates.append(
            {
                "explanation_id": f"prediction-error-{error_id}",
                "explanation_family": "prediction_error",
                "focus": str(event.get("delta") or event.get("error_kind") or "prediction_error"),
                "salience_score": float(event.get("magnitude") or 0.45),
            }
        )
    reconstructive = (memory_retrieval_frame or {}).get("reconstructive_recall_profile") or {}
    for index, ref in enumerate(_string_list(reconstructive.get("reconstruction_fragment_refs"))[:6]):
        candidates.append(
            {
                "explanation_id": f"reconstruction-fragment-{index + 1:02d}",
                "explanation_family": "memory_reconstruction",
                "focus": ref.rsplit("#", 1)[-1] if "#" in ref else ref,
                "salience_score": float(reconstructive.get("mean_activation_score") or 0.4),
            }
        )
    return _dedupe_dict_list(candidates)


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


def project_workspace_frame_from_live_turn(
    *,
    workspace_frame: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_workspace_frame(workspace_frame, generated_at, run_id)
    prediction_workspace = prediction_workspace or {}
    network_state = network_state or {}
    engram_index = engram_index or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["prediction_workspace_ref"] = "runtime/state/prediction/prediction_workspace_frame.json"
    updated["network_state_ref"] = "runtime/state/neural_life_core/network_state.json"
    updated["engram_retrieval_refs"] = _dedupe(
        list(updated.get("engram_retrieval_refs", []))
        + list((engram_index or {}).get("autobiographical_memory_refs", []))
        + list((engram_index or {}).get("relationship_memory_refs", []))
        + list((engram_index or {}).get("replay_cue_refs", []))
    )
    if prediction_workspace:
        updated["candidate_explanations"] = _dedupe_dict_list(
            list(updated.get("candidate_explanations", []))
            + list(prediction_workspace.get("workspace_contents", {}).get("candidate_explanations", []))
        )
        updated["broadcast_targets"] = _dedupe(
            list(updated.get("broadcast_targets", []))
            + list(prediction_workspace.get("downstream_systems", []))
        )
        updated["prediction_workspace_contents"] = dict(
            prediction_workspace.get("workspace_contents", {})
        )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", [])) + list(live_dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    if network_state:
        updated["network_state_mode"] = list(network_state.get("active_networks", []))
    updated["metacognitive_probe_refs"] = _dedupe(
        list(updated.get("metacognitive_probe_refs", []))
        + [
            "runtime/reports/latest/identity_birth_readiness_probe.json",
            "runtime/state/consciousness/workspace_frame.json#candidate_explanations",
        ]
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _seed_missing_workspace_frame(
    workspace_frame: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if workspace_frame:
        return json.loads(json.dumps(workspace_frame))
    resolved_run_id = run_id or "resident-turn-writeback"
    return {
        "schema_version": "workspace_frame_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "workspace_frame_id": f"workspace-frame-{resolved_run_id}",
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "candidate_explanations": [],
        "broadcast_targets": [
            "LanguageRelationshipRuntime",
            "ActionResponsibilityRuntime",
            "AffectiveSelfRuntime",
        ],
        "metacognitive_probe_refs": [],
        "engram_retrieval_refs": [],
        "network_state_ref": "runtime/state/neural_life_core/network_state.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _dedupe_dict_list(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if marker not in seen:
            seen.add(marker)
            result.append(item)
    return result


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str) and value:
        return [value]
    return []


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
