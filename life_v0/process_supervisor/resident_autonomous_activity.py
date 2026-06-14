from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

from life_v0.dream.web_dream_learning import (
    WEB_DREAM_LEARNING_LOG_REF,
    WEB_DREAM_LEARNING_STATE_REF,
    FetchUrl,
    record_web_dream_learning,
)


RESIDENT_AUTONOMOUS_ACTIVITY_REF = (
    "runtime/state/terminal/resident_autonomous_activity.jsonl"
)
RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF = (
    "runtime/state/terminal/resident_autonomous_activity_state.json"
)
RESIDENT_SLEEP_CYCLE_STATE_REF = (
    "runtime/state/terminal/resident_sleep_cycle_state.json"
)
RESIDENT_MEMORY_RECALL_STATE_REF = (
    "runtime/state/memory/resident_memory_recall_state.json"
)
RESIDENT_SELF_THINKING_STATE_REF = (
    "runtime/state/self/resident_self_thinking_state.json"
)
RESIDENT_GROWTH_REHEARSAL_STATE_REF = (
    "runtime/state/growth/resident_growth_rehearsal_state.json"
)
RESIDENT_LEARNING_CONSOLIDATION_STATE_REF = (
    "runtime/state/growth/resident_learning_consolidation_state.json"
)

AUTONOMOUS_ACTIVITY_CYCLE = [
    "sleep",
    "memory_recall",
    "self_thinking",
    "growth_rehearsal",
    "learning_consolidation",
]

ACTIVITY_STATE_REFS = {
    "sleep": RESIDENT_SLEEP_CYCLE_STATE_REF,
    "memory_recall": RESIDENT_MEMORY_RECALL_STATE_REF,
    "self_thinking": RESIDENT_SELF_THINKING_STATE_REF,
    "growth_rehearsal": RESIDENT_GROWTH_REHEARSAL_STATE_REF,
    "learning_consolidation": RESIDENT_LEARNING_CONSOLIDATION_STATE_REF,
}

SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/17_memory_trace_object_model.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
    "docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md",
]


def record_resident_autonomous_activity(
    *,
    terminal_dir: Path,
    now_iso: Callable[[], str],
    web_fetch_url: FetchUrl | None = None,
) -> dict[str, Any]:
    state_dir = terminal_dir.parent
    activity_path = terminal_dir / "resident_autonomous_activity.jsonl"
    aggregate_state_path = terminal_dir / "resident_autonomous_activity_state.json"
    aggregate_state = _read_json_if_exists(aggregate_state_path)
    previous_activity_count = _int_or_zero(aggregate_state.get("activity_count"))
    activity_count = previous_activity_count + 1
    activity_kind = autonomous_activity_kind(activity_count)
    generated_at = now_iso()
    activity_ref = ACTIVITY_STATE_REFS[activity_kind]
    activity_state = _build_activity_state(
        state_dir=state_dir,
        activity_sequence=activity_count,
        activity_kind=activity_kind,
        generated_at=generated_at,
        web_fetch_url=web_fetch_url,
    )
    _write_json(_path_for_ref(state_dir=state_dir, ref=activity_ref), activity_state)

    event = {
        "schema_version": "resident_autonomous_activity_event_v0",
        "activity_sequence": activity_count,
        "activity_kind": activity_kind,
        "generated_at": generated_at,
        "residency_posture": "sleeping_waiting_for_relation_turn",
        "autonomous_activity_ref": RESIDENT_AUTONOMOUS_ACTIVITY_REF,
        "autonomous_activity_state_ref": RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
        "activity_state_ref": activity_ref,
        "activity_evidence_refs": activity_state["evidence_refs"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }

    kind_counts = dict(aggregate_state.get("activity_kind_counts", {}))
    if _activity_kind_count_total(kind_counts) < previous_activity_count:
        kind_counts = _cycle_kind_counts(previous_activity_count)
    kind_counts[activity_kind] = _int_or_zero(kind_counts.get(activity_kind)) + 1
    coverage_profile = _cycle_coverage_profile(
        activity_count=activity_count,
        kind_counts=kind_counts,
    )
    event.update(
        {
            "cycle_phase_index": coverage_profile["cycle_phase_index"],
            "cycle_phase_count": coverage_profile["cycle_phase_count"],
            "cycle_completion_count": coverage_profile["cycle_completion_count"],
            "cycle_coverage_complete": coverage_profile["cycle_coverage_complete"],
            "covered_activity_kinds": coverage_profile["covered_activity_kinds"],
            "missing_activity_kinds": coverage_profile["missing_activity_kinds"],
            "next_activity_kind": coverage_profile["next_activity_kind"],
        }
    )
    _append_jsonl(activity_path, event)
    aggregate_state.update(
        {
            "schema_version": "resident_autonomous_activity_state_v0",
            "status": "active",
            "activity_count": activity_count,
            "activity_kind_counts": kind_counts,
            "last_activity_kind": activity_kind,
            "last_activity_at": generated_at,
            "last_activity_state_ref": activity_ref,
            "resident_autonomous_activity_ref": RESIDENT_AUTONOMOUS_ACTIVITY_REF,
            "resident_autonomous_activity_state_ref": (
                RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF
            ),
            "activity_state_refs": dict(ACTIVITY_STATE_REFS),
            "current_cycle": list(AUTONOMOUS_ACTIVITY_CYCLE),
            "last_activity_evidence_refs": activity_state["evidence_refs"],
            "last_web_dream_learning_state_ref": activity_state.get(
                "web_dream_learning_state_ref"
            ),
            "last_web_dream_learning_status": activity_state.get(
                "web_dream_learning_status"
            ),
            "last_web_dream_learning_topic_candidates": list(
                activity_state.get("web_dream_learning_topic_candidates", [])
            ),
            "last_web_dream_learning_wake_question_candidates": list(
                activity_state.get("web_dream_learning_wake_question_candidates", [])
            ),
            "source_doc_refs": SOURCE_DOC_REFS,
            **coverage_profile,
        }
    )
    _write_json(aggregate_state_path, aggregate_state)
    return {"event": event, "state": aggregate_state, "activity_state": activity_state}


def autonomous_activity_kind(activity_count: int) -> str:
    return AUTONOMOUS_ACTIVITY_CYCLE[
        (max(int(activity_count), 1) - 1) % len(AUTONOMOUS_ACTIVITY_CYCLE)
    ]


def _build_activity_state(
    *,
    state_dir: Path,
    activity_sequence: int,
    activity_kind: str,
    generated_at: str,
    web_fetch_url: FetchUrl | None = None,
) -> dict[str, Any]:
    evidence_refs = _evidence_refs_for_kind(activity_kind)
    web_learning_state: dict[str, Any] = {}
    if activity_kind == "learning_consolidation":
        web_learning = record_web_dream_learning(
            state_dir=state_dir,
            generated_at=generated_at,
            fetch_url=web_fetch_url,
        )
        web_learning_state = web_learning["state"]
        evidence_refs = _dedupe(
            evidence_refs
            + list(web_learning_state.get("ref_set", []))
            + [WEB_DREAM_LEARNING_STATE_REF]
        )
    existing_refs = [
        ref for ref in evidence_refs if _path_for_ref(state_dir=state_dir, ref=ref).exists()
    ]
    payload: dict[str, Any] = {
        "schema_version": f"resident_{activity_kind}_state_v0",
        "status": "closed",
        "activity_sequence": activity_sequence,
        "activity_kind": activity_kind,
        "generated_at": generated_at,
        "residency_posture": "sleeping_waiting_for_relation_turn",
        "evidence_refs": evidence_refs,
        "existing_evidence_refs": existing_refs,
        "existing_evidence_ref_count": len(existing_refs),
        "source_doc_refs": SOURCE_DOC_REFS,
    }
    if activity_kind == "sleep":
        payload.update(
            {
                "sleep_phase": "resident_background_sleep_cycle",
                "sleep_function": "restore_budget_and_open_offline_consolidation",
                "offline_consolidation_frame_ref": (
                    "runtime/state/dream/offline_consolidation_frame.json"
                ),
                "dream_experience_window_ref": (
                    "runtime/state/dream/dream_experience_window.json"
                ),
            }
        )
    elif activity_kind == "memory_recall":
        payload.update(
            {
                "recall_mode": "cue_driven_progressive_disclosure",
                "recall_targets": [
                    "relationship_memory",
                    "autobiographical_stack",
                    "dialogue_turn_log",
                    "replay_cue_bundle",
                ],
                "memory_trace_policy": "recall_without_overwriting_source_memory",
            }
        )
    elif activity_kind == "self_thinking":
        payload.update(
            {
                "thinking_mode": "self_model_and_resident_governance_reflection",
                "reflection_targets": [
                    "trait_slow_variables",
                    "background_convergence_history",
                    "consciousness_probe",
                    "inner_speech",
                ],
                "self_continuity_policy": "reflect_then_wait_for_relation_turn",
            }
        )
    elif activity_kind == "growth_rehearsal":
        payload.update(
            {
                "rehearsal_mode": "growth_patch_candidate_rehearsal",
                "growth_targets": [
                    "belief_learning_plan",
                    "language_learning_plan",
                    "relationship_learning_plan",
                    "plasticity_window",
                ],
                "patch_policy": "rehearse_candidate_before_long_term_merge",
            }
        )
    elif activity_kind == "learning_consolidation":
        payload.update(
            {
                "consolidation_mode": "long_term_change_source_integration",
                "learning_targets": [
                    "state_merge_guard",
                    "relationship_memory",
                    "commitment_expression_plan",
                    "apology_repair_language_trace",
                    "offline_learning_cumulative_profile",
                    "web_dream_learning_state",
                ],
                "learning_policy": "consolidate_without_erasing_relation_history",
                "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
                "web_dream_learning_log_ref": WEB_DREAM_LEARNING_LOG_REF,
                "web_dream_learning_status": web_learning_state.get("status"),
                "web_dream_learning_selected_url": web_learning_state.get(
                    "selected_url"
                ),
                "web_dream_learning_topic_candidates": list(
                    web_learning_state.get("topic_candidates", [])
                ),
                "web_dream_learning_wake_question_candidates": list(
                    web_learning_state.get("wake_question_candidates", [])
                ),
                "web_dream_learning_policy": web_learning_state.get(
                    "external_action_policy"
                ),
            }
        )
    return payload


def _evidence_refs_for_kind(activity_kind: str) -> list[str]:
    common_refs = [
        "runtime/state/terminal/resident_lifecycle_state.json",
        "runtime/state/terminal/resident_governance_state.json",
        "runtime/state/terminal/idle_strategy_state.json",
        "runtime/state/terminal/idle_continuity_frame.json",
        "runtime/state/replay/replay_cue_bundle.json",
    ]
    specific_refs = {
        "sleep": [
            "runtime/state/body/body_rhythm_pulse.json",
            "runtime/state/body/need_state.json",
            "runtime/state/dream/offline_consolidation_frame.json",
            "runtime/state/dream/dream_experience_window.json",
            "runtime/state/dream/wake_integration_frame.json",
        ],
        "memory_recall": [
            "runtime/state/memory/engram_index.json",
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/self/autobiographical_stack.json",
            "runtime/state/language/dialogue_turn_log.jsonl",
        ],
        "self_thinking": [
            "runtime/state/self/self_model.json",
            "runtime/state/language/inner_speech_frame.json",
            "runtime/state/consciousness/consciousness_probe_bundle.json",
            "runtime/state/terminal/background_convergence_history.json",
        ],
        "growth_rehearsal": [
            "runtime/state/growth/growth_patch_candidate_queue.json",
            "runtime/state/growth/plasticity_window.json",
            "runtime/state/growth/belief_learning_plan.json",
            "runtime/state/growth/language_learning_plan.json",
            "runtime/state/growth/relationship_learning_plan.json",
        ],
        "learning_consolidation": [
            "runtime/state/memory/state_merge_guard.json",
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/relationship/relationship_timeline.json",
            "runtime/state/language/commitment_expression_plan.json",
            "runtime/state/language/apology_repair_language_trace.json",
            "runtime/state/growth/learning_window.json",
            WEB_DREAM_LEARNING_STATE_REF,
        ],
    }
    return _dedupe(common_refs + specific_refs.get(activity_kind, []))


def _path_for_ref(*, state_dir: Path, ref: str) -> Path:
    prefix = "runtime/state/"
    if ref.startswith(prefix):
        return state_dir / ref[len(prefix) :]
    return state_dir.parent / ref.removeprefix("runtime/")


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
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _activity_kind_count_total(kind_counts: dict[str, Any]) -> int:
    return sum(_int_or_zero(value) for value in kind_counts.values())


def _cycle_kind_counts(activity_count: int) -> dict[str, int]:
    count = max(_int_or_zero(activity_count), 0)
    cycle_size = len(AUTONOMOUS_ACTIVITY_CYCLE)
    full_cycles = count // cycle_size
    remainder = count % cycle_size
    return {
        kind: full_cycles + (1 if index < remainder else 0)
        for index, kind in enumerate(AUTONOMOUS_ACTIVITY_CYCLE)
    }


def _cycle_coverage_profile(
    *,
    activity_count: int,
    kind_counts: dict[str, Any],
) -> dict[str, Any]:
    count = max(_int_or_zero(activity_count), 0)
    cycle_size = len(AUTONOMOUS_ACTIVITY_CYCLE)
    covered_kinds = [
        kind
        for kind in AUTONOMOUS_ACTIVITY_CYCLE
        if _int_or_zero(kind_counts.get(kind)) > 0
    ]
    missing_kinds = [
        kind
        for kind in AUTONOMOUS_ACTIVITY_CYCLE
        if _int_or_zero(kind_counts.get(kind)) <= 0
    ]
    cycle_phase_index = ((count - 1) % cycle_size) if count else 0
    next_activity_count = count + 1 if count else 1
    return {
        "cycle_phase_index": cycle_phase_index,
        "cycle_phase_count": cycle_size,
        "cycle_completion_count": min(
            [_int_or_zero(kind_counts.get(kind)) for kind in AUTONOMOUS_ACTIVITY_CYCLE]
            or [0]
        ),
        "cycle_coverage_complete": not missing_kinds,
        "covered_activity_kinds": covered_kinds,
        "missing_activity_kinds": missing_kinds,
        "next_activity_kind": autonomous_activity_kind(next_activity_count),
    }
