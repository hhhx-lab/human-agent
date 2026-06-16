from __future__ import annotations

from typing import Any

LANGUAGE_EVENT_BUNDLE_REF = "runtime/state/language/language_event_bundle.json"

FIXTURE_EVENT_KINDS = (
    "commit",
    "apologize",
    "refuse",
    "dream_report",
    "shared_term_development",
)


def build_language_event_bundle(
    *,
    run_id: str,
    generated_at: str,
    language_event_kind: str,
    inner_speech_ref: str | None = None,
    expression_plan_ref: str | None = None,
    turn_transition_trace_ref: str | None = None,
    future_probe_refs: list[str] | None = None,
    language_percept_ref: str | None = None,
    semantic_map_ref: str | None = None,
    expression_monitor_ref: str | None = None,
    source_doc_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "language_event_bundle_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "language_event_kind": language_event_kind,
        "fixture_event_kinds_covered": list(FIXTURE_EVENT_KINDS),
        "inner_speech_ref": inner_speech_ref
        or "runtime/state/language/inner_speech_frame.json",
        "expression_plan_ref": expression_plan_ref
        or "runtime/state/language/expression_plan.json",
        "turn_transition_trace_ref": turn_transition_trace_ref
        or "runtime/state/terminal/turn_transition_trace.json",
        "future_probe": list(future_probe_refs or [])[:8],
        "language_percept_ref": language_percept_ref
        or "runtime/state/language/language_percept_frame.json",
        "semantic_map_ref": semantic_map_ref
        or "runtime/state/language/semantic_map_frame.json",
        "expression_monitor_ref": expression_monitor_ref
        or "runtime/state/language/expression_monitor_state.json",
        "source_doc_refs": list(source_doc_refs or []),
        "bundle_ref": LANGUAGE_EVENT_BUNDLE_REF,
    }


def infer_language_event_kind(
    *,
    semantic_focus: str | None = None,
    speech_act: str | None = None,
    dream_signal_candidates: list[str] | None = None,
    shared_term_hits: list[str] | None = None,
) -> str:
    focus = str(semantic_focus or "").lower()
    act = str(speech_act or "").lower()
    if dream_signal_candidates:
        return "dream_report"
    if shared_term_hits:
        return "shared_term_development"
    if "apolog" in focus or "repair" in focus or act == "apology":
        return "apologize"
    if "refus" in focus or "boundar" in focus or act == "refusal":
        return "refuse"
    if "commit" in focus or act in {"commitment_request", "commitment"}:
        return "commit"
    return "commit"