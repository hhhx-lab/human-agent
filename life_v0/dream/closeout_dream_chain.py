from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from life_v0.dream.dream_belief_gate import (
    DREAM_BELIEF_GATE_DECISION_REF,
    build_dream_belief_gate_decision,
)
from life_v0.dream.dream_fact_gate import build_dream_fact_gate_decision
from life_v0.dream.dream_window import build_exit_closeout_dream_experience_window
from life_v0.dream.offline_dream_entry import (
    DREAM_CUE_POLICY_STATE_REF,
    OFFLINE_DREAM_ENTRY_VECTOR_REF,
    build_dream_cue_policy_state,
    build_offline_dream_entry_vector,
)
from life_v0.dream.wake_integration import build_wake_integration_frame

DREAM_EXPERIENCE_WINDOW_REF = "runtime/state/dream/dream_experience_window.json"
WAKE_INTEGRATION_FRAME_REF = "runtime/state/dream/wake_integration_frame.json"
DREAM_FACT_GATE_DECISION_REF = "runtime/state/dream/dream_fact_gate_decision.json"
WEB_DREAM_LEARNING_STATE_REF = "runtime/state/dream/web_dream_learning_state.json"
WEB_DREAM_BROWSER_SESSION_REF = "runtime/state/dream/web_dream_browser_session.json"
WEB_DREAM_TOPIC_HISTORY_REF = "runtime/state/dream/web_dream_topic_history.json"

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/real—live0/08_dream_sleep_offline_life.md",
]


def write_closeout_dream_chain(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    write_json: Callable[[Path, dict[str, Any]], None],
    exit_dream_summary: dict[str, Any],
    hygiene_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    dream_dir = state_dir / "dream"
    memory_dir = state_dir / "memory"
    replay_dir = state_dir / "replay"
    body_dir = state_dir / "body"
    dream_dir.mkdir(parents=True, exist_ok=True)

    life_state = _read_json(state_dir / "life_state.json")
    relationship_memory = _read_json(memory_dir / "relationship_memory.json")
    memory_trace_store = _read_json(memory_dir / "memory_trace_store.json")
    need_state_vector = _read_json(body_dir / "need_state.json")
    body_resource_budget = _read_json(body_dir / "body_resource_budget.json")
    replay_cue_bundle = _read_json(replay_dir / "replay_cue_bundle.json")
    web_dream_state = _read_json(dream_dir / "web_dream_learning_state.json")
    topic_history = _read_json(dream_dir / "web_dream_topic_history.json")

    entry_vector = build_offline_dream_entry_vector(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        replay_cue_bundle=replay_cue_bundle,
        memory_trace_store=memory_trace_store,
        need_state_vector=need_state_vector,
        body_resource_budget=body_resource_budget,
        relationship_memory=relationship_memory,
        exit_dream_summary=exit_dream_summary,
    )
    cue_policy = build_dream_cue_policy_state(
        run_id=run_id,
        generated_at=generated_at,
        entry_vector=entry_vector,
        exit_dream_summary=exit_dream_summary,
        relationship_memory=relationship_memory,
        replay_cue_bundle=replay_cue_bundle,
        web_dream_learning_state=web_dream_state,
        topic_history=topic_history,
    )
    dream_window = build_exit_closeout_dream_experience_window(
        run_id=run_id,
        generated_at=generated_at,
        exit_dream_summary=exit_dream_summary,
        entry_vector=entry_vector,
        cue_policy=cue_policy,
        hygiene_report=hygiene_report,
        memory_trace_store=memory_trace_store,
        web_dream_learning_state=web_dream_state,
    )
    wake_integration = build_wake_integration_frame(
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        replay_cue_bundle=replay_cue_bundle or {"turn_residue_refs": []},
    )
    offline_entry_stub = {
        "offline_modes": entry_vector.get("selected_offline_modes", []),
        "entry_decision": "offline_allowed",
        "external_action_policy": "blocked",
    }
    dream_fact_gate = build_dream_fact_gate_decision(
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        wake_integration=wake_integration,
        offline_entry=offline_entry_stub,
    )
    dream_belief_gate = build_dream_belief_gate_decision(
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        wake_integration=wake_integration,
    )

    write_json(dream_dir / "offline_dream_entry_vector.json", entry_vector)
    write_json(dream_dir / "dream_cue_policy_state.json", cue_policy)
    write_json(dream_dir / "dream_experience_window.json", dream_window)
    write_json(dream_dir / "wake_integration_frame.json", wake_integration)
    write_json(dream_dir / "dream_fact_gate_decision.json", dream_fact_gate)
    write_json(dream_dir / "dream_belief_gate_decision.json", dream_belief_gate)

    return {
        "offline_dream_entry_vector": entry_vector,
        "dream_cue_policy_state": cue_policy,
        "dream_experience_window": dream_window,
        "wake_integration_frame": wake_integration,
        "dream_fact_gate_decision": dream_fact_gate,
        "dream_belief_gate_decision": dream_belief_gate,
        "offline_dream_entry_vector_ref": OFFLINE_DREAM_ENTRY_VECTOR_REF,
        "dream_cue_policy_state_ref": DREAM_CUE_POLICY_STATE_REF,
        "dream_experience_window_ref": DREAM_EXPERIENCE_WINDOW_REF,
        "wake_integration_frame_ref": WAKE_INTEGRATION_FRAME_REF,
        "dream_fact_gate_decision_ref": DREAM_FACT_GATE_DECISION_REF,
        "dream_belief_gate_decision_ref": DREAM_BELIEF_GATE_DECISION_REF,
        "web_dream_learning_state_ref": (
            WEB_DREAM_LEARNING_STATE_REF if web_dream_state else None
        ),
        "web_dream_browser_session_ref": (
            WEB_DREAM_BROWSER_SESSION_REF
            if (dream_dir / "web_dream_browser_session.json").exists()
            else None
        ),
        "web_dream_topic_history_ref": (
            WEB_DREAM_TOPIC_HISTORY_REF if topic_history else None
        ),
        "web_dream_learning_status": web_dream_state.get("status"),
        "web_dream_topic_candidate_count": len(
            web_dream_state.get("topic_candidates", [])
        )
        if isinstance(web_dream_state.get("topic_candidates"), list)
        else 0,
        "web_dream_wake_candidate_count": len(
            web_dream_state.get("structured_wake_question_candidates", [])
        )
        if isinstance(
            web_dream_state.get("structured_wake_question_candidates"), list
        )
        else 0,
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}
