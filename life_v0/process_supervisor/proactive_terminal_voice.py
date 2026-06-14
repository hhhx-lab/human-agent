from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PROACTIVE_TERMINAL_EVENTS_REF = (
    "runtime/state/terminal/resident_terminal_proactive_events.jsonl"
)
PROACTIVE_TERMINAL_STATE_REF = (
    "runtime/state/terminal/resident_terminal_proactive_state.json"
)


def build_resident_proactive_terminal_event(
    *,
    terminal_dir: Path,
    life_name: str | None,
    now_iso: Callable[[], str],
) -> dict[str, Any]:
    state_root = terminal_dir.parent
    relationship_memory = _read_json(
        state_root / "memory" / "relationship_memory.json"
    )
    dialogue_memory_summary = _read_json(
        state_root / "memory" / "dialogue_memory_summary.json"
    )
    exit_dream_summary = _read_json(
        state_root / "dream" / "exit_dream_consolidation_summary.json"
    )
    web_dream_learning = _read_json(
        state_root / "dream" / "web_dream_learning_state.json"
    )
    autonomous_activity = _read_json(
        terminal_dir / "resident_autonomous_activity_state.json"
    )
    idle_strategy = _read_json(terminal_dir / "idle_strategy_state.json")
    governance = _read_json(terminal_dir / "resident_governance_state.json")

    memory_profile = _memory_profile(
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    dream_profile = _dream_profile(exit_dream_summary)
    memory_tier_profile = _memory_tier_profile(
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
        exit_dream_summary=exit_dream_summary,
    )
    web_learning_profile = _web_learning_profile(web_dream_learning)
    activity_profile = _activity_profile(autonomous_activity)
    idle_profile = _idle_profile(idle_strategy=idle_strategy, governance=governance)
    focus = _select_focus(
        memory_profile=memory_profile,
        memory_tier_profile=memory_tier_profile,
        dream_profile=dream_profile,
        web_learning_profile=web_learning_profile,
        activity_profile=activity_profile,
        idle_profile=idle_profile,
    )
    source_refs = _source_refs(
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
        memory_tier_profile=memory_tier_profile,
        exit_dream_summary=exit_dream_summary,
        web_dream_learning=web_dream_learning,
        autonomous_activity=autonomous_activity,
        idle_strategy=idle_strategy,
        governance=governance,
    )
    fingerprint = _fingerprint(
        {
            "focus": focus,
            "memory": memory_profile,
            "memory_tier": memory_tier_profile,
            "dream": dream_profile,
            "web_learning": web_learning_profile,
            "activity": activity_profile,
            "idle": idle_profile,
            "source_refs": source_refs,
        }
    )
    proactive_voice_profile = _build_proactive_voice_profile(
        focus=focus,
        memory_profile=memory_profile,
        dream_profile=dream_profile,
        web_learning_profile=web_learning_profile,
        activity_profile=activity_profile,
        idle_profile=idle_profile,
        memory_tier_profile=memory_tier_profile,
        source_refs=source_refs,
        fingerprint=fingerprint,
    )
    utterance = ""
    return {
        "schema_version": "resident_proactive_terminal_event_v0",
        "status": "held_internal",
        "release_scope": "open_terminal_idle_hidden",
        "generated_at": now_iso(),
        "life_name": life_name,
        "focus": focus,
        "utterance": utterance,
        "proactive_voice_profile": proactive_voice_profile,
        "memory_tier_profile": memory_tier_profile,
        "composition_fingerprint": fingerprint,
        "source_refs": source_refs,
        "resident_terminal_proactive_events_ref": PROACTIVE_TERMINAL_EVENTS_REF,
        "resident_terminal_proactive_state_ref": PROACTIVE_TERMINAL_STATE_REF,
    }


def write_resident_proactive_terminal_event(
    *,
    terminal_dir: Path,
    event: dict[str, Any],
) -> dict[str, Any]:
    events_path = terminal_dir / "resident_terminal_proactive_events.jsonl"
    sequence = _jsonl_count(events_path) + 1
    written = dict(event)
    written["sequence"] = sequence
    release_profile = _release_profile(written)
    written.update(release_profile)
    _append_jsonl(events_path, written)
    natural_language_release_count = _jsonl_release_count(events_path)
    state = {
        "schema_version": "resident_terminal_proactive_state_v0",
        "status": release_profile["status"],
        "last_release_scope": release_profile["release_scope"],
        "last_natural_language_released": release_profile[
            "natural_language_released"
        ],
        "last_sequence": sequence,
        "last_generated_at": written.get("generated_at"),
        "last_focus": written.get("focus"),
        "last_utterance": written.get("utterance"),
        "last_proactive_voice_profile": written.get("proactive_voice_profile"),
        "last_proactive_voice_surface_kind": (
            written.get("proactive_voice_profile", {}) or {}
        ).get("surface_kind"),
        "last_model_expression_status": written.get("model_expression_status"),
        "last_model_expression_state_ref": written.get("model_expression_state_ref"),
        "last_model_expression_report_ref": written.get("model_expression_report_ref"),
        "last_post_expression_gate_status": written.get("post_expression_gate_status"),
        "last_composition_fingerprint": written.get("composition_fingerprint"),
        "event_count": sequence,
        "release_count": natural_language_release_count,
        "resident_terminal_proactive_events_ref": PROACTIVE_TERMINAL_EVENTS_REF,
    }
    _write_json(terminal_dir / "resident_terminal_proactive_state.json", state)
    return written


def _release_profile(event: dict[str, Any]) -> dict[str, Any]:
    utterance = str(event.get("utterance") or "").strip()
    model_status = str(event.get("model_expression_status") or "")
    gate_status = str(event.get("post_expression_gate_status") or "")
    released = bool(
        utterance
        and model_status == "model_expression_applied"
        and gate_status == "accepted"
    )
    if released:
        return {
            "status": "released_model_expression",
            "release_scope": "open_terminal_idle_model_expression",
            "natural_language_released": True,
        }
    return {
        "status": "held_internal",
        "release_scope": "open_terminal_idle_hidden",
        "natural_language_released": False,
    }


def _memory_profile(
    *,
    relationship_memory: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
) -> dict[str, Any]:
    relation_profile = relationship_memory.get("relation_person_profile")
    if not isinstance(relation_profile, dict):
        relation_profile = {}
    dialogue_profile = dialogue_memory_summary.get("relation_person_profile")
    if not isinstance(dialogue_profile, dict):
        dialogue_profile = {}
    names = _dedupe(
        _string_list(relation_profile.get("observed_names"))
        + _string_list(dialogue_profile.get("observed_names"))
    )
    preferences = _dedupe(
        _string_list(relation_profile.get("preference_hypotheses"))
        + _string_list(dialogue_profile.get("preference_hypotheses"))
    )
    themes = _dedupe(
        _string_list(relationship_memory.get("relationship_theme_tags"))
        + _string_list(dialogue_memory_summary.get("relationship_theme_tags"))
    )
    return {
        "observed_names": names,
        "preference_cues": preferences,
        "theme_cues": themes,
        "source_dialogue_turn_count": dialogue_memory_summary.get(
            "source_dialogue_turn_count"
        ),
        "next_wake_cues": _dedupe(
            _string_list(relationship_memory.get("next_wake_cues"))
            + _string_list(dialogue_memory_summary.get("next_wake_cues"))
        ),
    }


def _memory_tier_profile(
    *,
    relationship_memory: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
    exit_dream_summary: dict[str, Any],
) -> dict[str, Any]:
    relationship_projection = relationship_memory.get("memory_tier_projection")
    if not isinstance(relationship_projection, dict):
        relationship_projection = {}
    dream_tiering = exit_dream_summary.get("memory_tiering")
    if not isinstance(dream_tiering, dict):
        dream_tiering = {}
    dialogue_tiering = dialogue_memory_summary.get("memory_tiering")
    if not isinstance(dialogue_tiering, dict):
        dialogue_tiering = {}
    return {
        "relationship_memory_tier_projection_ref": (
            "runtime/state/memory/relationship_memory.json#memory_tier_projection"
            if relationship_projection
            else None
        ),
        "dialogue_memory_tiering_ref": (
            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering"
            if dream_tiering
            else None
        ),
        "dialogue_memory_tier_refs": _dedupe(
            _string_list(dialogue_tiering.get("salient_core_episode_refs"))
            + _string_list(dialogue_tiering.get("retrievable_context_episode_refs"))
            + _string_list(dialogue_tiering.get("deep_sediment_episode_refs"))
        ),
        "relationship_memory_tier_refs": _dedupe(
            _string_list(relationship_projection.get("salient_core_episode_refs"))
            + _string_list(
                relationship_projection.get("retrievable_context_episode_refs")
            )
            + _string_list(relationship_projection.get("deep_sediment_episode_refs"))
        ),
        "next_wake_cues": _dedupe(
            _string_list(relationship_memory.get("next_wake_cues"))
            + _string_list(dialogue_memory_summary.get("next_wake_cues"))
            + _string_list(exit_dream_summary.get("next_wake_cues"))
        ),
        "relationship_profile_name_refs": _dedupe(
            _string_list(
                (relationship_memory.get("relation_person_profile") or {}).get(
                    "observed_names"
                )
            )
            + _string_list(
                (dialogue_memory_summary.get("relation_person_profile") or {}).get(
                    "observed_names"
                )
            )
        ),
    }


def _dream_profile(exit_dream_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "entry_state": exit_dream_summary.get("entry_state"),
        "theme_cues": _string_list(exit_dream_summary.get("relationship_theme_tags")),
    }


def _web_learning_profile(web_dream_learning: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": web_dream_learning.get("status"),
        "topic_phrases": _dedupe(
            _string_list(web_dream_learning.get("topic_candidates"))
        ),
        "wake_question_candidates": _dedupe(
            _string_list(web_dream_learning.get("wake_question_candidates"))
        ),
    }


def _activity_profile(autonomous_activity: dict[str, Any]) -> dict[str, Any]:
    return {
        "activity_count": autonomous_activity.get("activity_count"),
        "last_activity_kind": autonomous_activity.get("last_activity_kind"),
        "next_activity_kind": autonomous_activity.get("next_activity_kind"),
        "cycle_completion_count": autonomous_activity.get("cycle_completion_count"),
    }


def _idle_profile(
    *,
    idle_strategy: dict[str, Any],
    governance: dict[str, Any],
) -> dict[str, Any]:
    return {
        "attention_target": idle_strategy.get("governance_attention_target")
        or governance.get("governance_attention_target"),
        "next_idle_action": idle_strategy.get("next_idle_action")
        or governance.get("next_required_action"),
        "waiting_posture": idle_strategy.get("body_waiting_posture")
        or governance.get("governance_phase"),
    }


def _select_focus(
    *,
    memory_profile: dict[str, Any],
    memory_tier_profile: dict[str, Any],
    dream_profile: dict[str, Any],
    web_learning_profile: dict[str, Any],
    activity_profile: dict[str, Any],
    idle_profile: dict[str, Any],
) -> str:
    if memory_tier_profile.get("next_wake_cues"):
        return "memory_tiered_wake_cue"
    if memory_profile.get("preference_cues") or memory_profile.get("observed_names"):
        return "relationship_memory"
    if web_learning_profile.get("topic_phrases"):
        return "web_dream_learning"
    if dream_profile.get("entry_state") or dream_profile.get("theme_cues"):
        return "dream_residue"
    if activity_profile.get("activity_count"):
        return "resident_autonomous_activity"
    if idle_profile.get("attention_target"):
        return "waiting_attention"
    return "open_terminal_presence"


def _build_proactive_voice_profile(
    *,
    focus: str,
    memory_profile: dict[str, Any],
    dream_profile: dict[str, Any],
    web_learning_profile: dict[str, Any],
    activity_profile: dict[str, Any],
    idle_profile: dict[str, Any],
    memory_tier_profile: dict[str, Any],
    source_refs: list[str],
    fingerprint: str,
) -> dict[str, Any]:
    question_candidates = _build_question_candidates(
        focus=focus,
        memory_profile=memory_profile,
        dream_profile=dream_profile,
        web_learning_profile=web_learning_profile,
        activity_profile=activity_profile,
        idle_profile=idle_profile,
        memory_tier_profile=memory_tier_profile,
    )
    surface_kind = _surface_kind_for_focus(
        focus=focus,
        memory_profile=memory_profile,
        dream_profile=dream_profile,
        web_learning_profile=web_learning_profile,
        activity_profile=activity_profile,
        idle_profile=idle_profile,
    )
    return {
        "schema_version": "resident_proactive_voice_profile_v0",
        "focus": focus,
        "surface_kind": surface_kind,
        "question_candidate_count": len(question_candidates),
        "question_candidates": question_candidates,
        "memory_cues": _dedupe(
            _string_list(memory_profile.get("next_wake_cues"))[:5]
        ),
        "memory_names": _dedupe(
            _string_list(memory_tier_profile.get("relationship_profile_name_refs"))[:5]
        ),
        "dream_cues": _dedupe(_string_list(dream_profile.get("theme_cues"))[:5]),
        "web_learning_cues": _dedupe(
            _string_list(web_learning_profile.get("topic_phrases"))[:5]
        ),
        "activity_cues": _activity_cues(activity_profile),
        "idle_cues": _idle_cues(idle_profile),
        "speaking_constraints": [
            "state_driven",
            "model_expression_only",
            "no_precomposed_surface",
            "state_cues_not_sentences",
        ],
        "composition_fingerprint": fingerprint,
        "source_refs": list(source_refs),
    }


def _build_question_candidates(
    *,
    focus: str,
    memory_profile: dict[str, Any],
    dream_profile: dict[str, Any],
    web_learning_profile: dict[str, Any],
    activity_profile: dict[str, Any],
    idle_profile: dict[str, Any],
    memory_tier_profile: dict[str, Any],
) -> list[str]:
    candidates: list[str] = []
    candidates.extend(
        f"wake_cue:{cue}"
        for cue in _string_list(memory_tier_profile.get("next_wake_cues"))[:3]
    )
    candidates.extend(
        f"name:{name}" for name in _string_list(memory_profile.get("observed_names"))[:3]
    )
    candidates.extend(
        f"preference_cue:{cue}"
        for cue in _string_list(memory_profile.get("preference_cues"))[:3]
    )
    candidates.extend(
        f"dream_theme_cue:{cue}"
        for cue in _string_list(dream_profile.get("theme_cues"))[:3]
    )
    candidates.extend(
        f"web_topic:{topic}"
        for topic in _string_list(web_learning_profile.get("topic_phrases"))[:3]
    )
    if activity_profile.get("last_activity_kind"):
        candidates.append(f"activity:{activity_profile['last_activity_kind']}")
    if activity_profile.get("next_activity_kind"):
        candidates.append(f"next_activity:{activity_profile['next_activity_kind']}")
    if idle_profile.get("attention_target"):
        candidates.append(f"idle_attention:{idle_profile['attention_target']}")
    if idle_profile.get("next_idle_action"):
        candidates.append(f"idle_next_action:{idle_profile['next_idle_action']}")
    if not candidates:
        candidates.append(f"presence:{focus}")
    return _dedupe(candidates)[:8]


def _surface_kind_for_focus(
    *,
    focus: str,
    memory_profile: dict[str, Any],
    dream_profile: dict[str, Any],
    web_learning_profile: dict[str, Any],
    activity_profile: dict[str, Any],
    idle_profile: dict[str, Any],
) -> str:
    if focus == "memory_tiered_wake_cue":
        return "wake_question"
    if focus == "relationship_memory":
        return "relationship_checkin"
    if focus == "web_dream_learning":
        return "learning_probe"
    if focus == "dream_residue":
        return "dream_probe"
    if focus == "resident_autonomous_activity":
        return "self_continuity_checkin"
    if focus == "waiting_attention":
        return "attention_probe"
    if memory_profile.get("observed_names"):
        return "memory_probe"
    if dream_profile.get("theme_cues"):
        return "dream_probe"
    if web_learning_profile.get("topic_phrases"):
        return "learning_probe"
    if activity_profile.get("activity_count"):
        return "self_continuity_checkin"
    if idle_profile.get("attention_target"):
        return "attention_probe"
    return "presence_checkin"


def _activity_cues(activity_profile: dict[str, Any]) -> list[str]:
    cues = []
    if activity_profile.get("last_activity_kind"):
        cues.append(f"last_activity:{activity_profile['last_activity_kind']}")
    if activity_profile.get("next_activity_kind"):
        cues.append(f"next_activity:{activity_profile['next_activity_kind']}")
    if activity_profile.get("activity_count") is not None:
        cues.append(f"activity_count:{activity_profile['activity_count']}")
    return _dedupe(cues)


def _idle_cues(idle_profile: dict[str, Any]) -> list[str]:
    cues = []
    if idle_profile.get("attention_target"):
        cues.append(f"attention_target:{idle_profile['attention_target']}")
    if idle_profile.get("next_idle_action"):
        cues.append(f"next_idle_action:{idle_profile['next_idle_action']}")
    if idle_profile.get("waiting_posture"):
        cues.append(f"waiting_posture:{idle_profile['waiting_posture']}")
    return _dedupe(cues)


def _source_refs(
    *,
    relationship_memory: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
    memory_tier_profile: dict[str, Any],
    exit_dream_summary: dict[str, Any],
    web_dream_learning: dict[str, Any],
    autonomous_activity: dict[str, Any],
    idle_strategy: dict[str, Any],
    governance: dict[str, Any],
) -> list[str]:
    refs: list[str] = []
    if relationship_memory:
        refs.append("runtime/state/memory/relationship_memory.json")
    if dialogue_memory_summary:
        refs.append("runtime/state/memory/dialogue_memory_summary.json")
    if memory_tier_profile.get("relationship_memory_tier_projection_ref"):
        refs.append(memory_tier_profile["relationship_memory_tier_projection_ref"])
    if memory_tier_profile.get("dialogue_memory_tiering_ref"):
        refs.append(memory_tier_profile["dialogue_memory_tiering_ref"])
    if exit_dream_summary:
        refs.append("runtime/state/dream/exit_dream_consolidation_summary.json")
    if web_dream_learning:
        refs.append("runtime/state/dream/web_dream_learning_state.json")
    if autonomous_activity:
        refs.append("runtime/state/terminal/resident_autonomous_activity_state.json")
    if idle_strategy:
        refs.append("runtime/state/terminal/idle_strategy_state.json")
    if governance:
        refs.append("runtime/state/terminal/resident_governance_state.json")
    return refs


def _fingerprint(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _read_json(path: Path) -> dict[str, Any]:
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
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _jsonl_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line])


def _jsonl_release_count(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except ValueError:
            continue
        if isinstance(payload, dict) and payload.get("natural_language_released") is True:
            count += 1
    return count


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _first(value: Any) -> str:
    values = _string_list(value)
    return values[0] if values else ""


def _join_cn(values: list[str]) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return ""
    return "、".join(cleaned)
