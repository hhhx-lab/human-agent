from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from life_v0.runtime_config import load_digital_life_runtime_config

from life_v0.dream.web_dream_browser import (
    WEB_DREAM_BROWSER_SESSION_REF,
    read_only_fetch_page,
    run_readonly_browse_session,
    url_digest,
)
from life_v0.dream.web_dream_discovery import (
    WEB_DREAM_TOPIC_HISTORY_REF,
    append_topic_history_entry,
    build_structured_wake_question_candidates,
    read_topic_history,
    resolve_seed_urls,
    select_topic_candidate,
    topic_candidates_from_page,
    write_topic_history,
)

WEB_DREAM_LEARNING_STATE_REF = "runtime/state/dream/web_dream_learning_state.json"
WEB_DREAM_LEARNING_LOG_REF = "runtime/state/dream/web_dream_learning_log.jsonl"
WEB_DREAM_LEARNING_SEEDS_REF = "runtime/state/dream/web_dream_learning_seeds.json"

SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
]

FetchUrl = Callable[[str, float], Mapping[str, Any] | str]


def web_dream_learning_env_enabled(
    environ: Mapping[str, str] | None = None,
) -> bool:
    effective_environ = _effective_environ(environ)
    env_enabled = _optional_env_bool(
        effective_environ.get("DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED")
    )
    env_urls_present = bool(
        str(effective_environ.get("DIGITAL_LIFE_WEB_DREAM_URLS") or "").strip()
    )
    return bool(env_urls_present or env_enabled)


def build_web_dream_learning_effective_seed_preview(
    *,
    state_dir: Path,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    dream_dir = state_dir / "dream"
    seed_path = dream_dir / "web_dream_learning_seeds.json"
    effective_environ = _effective_environ(environ)
    seed_payload = _read_json(seed_path)
    source = "seed_file" if seed_payload else "env_default"
    if not seed_payload:
        seed_payload = _seed_payload_from_env_defaults(effective_environ)
    else:
        seed_payload = _apply_env_defaults_to_seed_payload(
            seed_payload=seed_payload,
            environ=effective_environ,
        )
    seed_urls = resolve_seed_urls(
        seed_payload=seed_payload,
        environ=effective_environ,
    )
    return {
        "schema_version": "web_dream_learning_effective_seed_preview_v1",
        "source": source,
        "enabled": _seed_enabled(seed_payload=seed_payload, seed_urls=seed_urls),
        "configured_enabled": bool(seed_payload.get("enabled")),
        "seed_count": len(seed_urls),
        "seed_urls": seed_urls,
        "web_dream_learning_seeds_ref": WEB_DREAM_LEARNING_SEEDS_REF,
    }


def record_web_dream_learning(
    *,
    state_dir: Path,
    generated_at: str,
    fetch_url: FetchUrl | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    dream_dir = state_dir / "dream"
    memory_dir = state_dir / "memory"
    state_path = dream_dir / "web_dream_learning_state.json"
    log_path = dream_dir / "web_dream_learning_log.jsonl"
    seed_path = dream_dir / "web_dream_learning_seeds.json"
    browser_session_path = dream_dir / "web_dream_browser_session.json"
    topic_history_path = dream_dir / "web_dream_topic_history.json"

    previous_state = _read_json(state_path)
    effective_environ = _effective_environ(environ)
    seed_payload = _read_json(seed_path)
    if not seed_payload:
        seed_payload = _seed_payload_from_env_defaults(effective_environ)
    else:
        seed_payload = _apply_env_defaults_to_seed_payload(
            seed_payload=seed_payload,
            environ=effective_environ,
        )
    seed_urls = resolve_seed_urls(
        seed_payload=seed_payload,
        environ=effective_environ,
    )
    enabled = _seed_enabled(seed_payload=seed_payload, seed_urls=seed_urls)
    timeout_seconds = _timeout_seconds(seed_payload)
    sequence = _jsonl_count(log_path) + 1
    session_id = f"web-dream-session-{sequence:04d}"
    topic_history = read_topic_history(topic_history_path)
    relationship_memory = _read_json(memory_dir / "relationship_memory.json")
    relation_tags = list(relationship_memory.get("relationship_theme_tags", []))
    policy = seed_payload.get("topic_selection_policy") or {}

    base_state: dict[str, Any] = {
        "schema_version": "web_dream_learning_state_v1",
        "status": "disabled" if not enabled else "no_seed_urls",
        "generated_at": generated_at,
        "sequence": sequence,
        "session_id": session_id,
        "external_action_policy": "read_only_no_side_effect",
        "browser_backend": seed_payload.get("browser_backend", "playwright_readonly"),
        "fallback_backend": seed_payload.get("fallback_backend", "urllib_mock_or_ci_fallback"),
        "discovery_mode": None,
        "seed_count": len(seed_urls),
        "selected_seed_index": None,
        "selected_url": None,
        "page_title": "",
        "content_digest": "",
        "url_digest": "",
        "topic_cluster_id": "",
        "topic_candidates": [],
        "structured_wake_question_candidates": [],
        "wake_question_candidates": [],
        "topic_selection_rationale": {},
        "web_dream_browser_session_ref": WEB_DREAM_BROWSER_SESSION_REF,
        "web_dream_topic_history_ref": WEB_DREAM_TOPIC_HISTORY_REF,
        "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
        "web_dream_learning_log_ref": WEB_DREAM_LEARNING_LOG_REF,
        "web_dream_learning_seeds_ref": WEB_DREAM_LEARNING_SEEDS_REF,
        "ref_set": _dedupe(
            [
                WEB_DREAM_LEARNING_STATE_REF,
                WEB_DREAM_LEARNING_LOG_REF,
                WEB_DREAM_LEARNING_SEEDS_REF,
            ]
        ),
        "claim_status": "hypothesis_or_residue",
        "source_doc_refs": SOURCE_DOC_REFS,
    }
    if not enabled or not seed_urls:
        _write_json(state_path, base_state)
        _append_jsonl(log_path, _event_from_state(base_state))
        return {"state": base_state, "event": _event_from_state(base_state)}

    selected_index = _next_seed_index(previous_state, len(seed_urls))
    selected_url = seed_urls[selected_index]
    discovery_mode = _discovery_mode(seed_payload, selected_index)
    learned_state = dict(base_state)
    learned_state.update(
        {
            "status": "fetching",
            "discovery_mode": discovery_mode,
            "selected_seed_index": selected_index,
            "selected_url": selected_url,
        }
    )
    fetch_page = _fetch_page_adapter(fetch_url)
    max_hops = int(
        (seed_payload.get("playwright_readonly") or {}).get("max_hops_per_seed", 2)
    )
    try:
        browser_session = run_readonly_browse_session(
            start_url=selected_url,
            generated_at=generated_at,
            session_id=session_id,
            max_hops=max_hops,
            timeout_seconds=timeout_seconds,
            fetch_page=fetch_page,
            visited_url_digests=_visited_digests(topic_history),
        )
        pages = [
            page for page in browser_session.get("pages", []) if isinstance(page, dict)
        ]
        page = pages[-1] if pages else {}
        candidates = []
        for item in pages:
            candidates.extend(
                topic_candidates_from_page(
                    page=item,
                    relation_theme_tags=relation_tags,
                    dream_residue_weight=0.1,
                )
            )
        selection = select_topic_candidate(
            candidates=candidates,
            topic_history=topic_history,
            policy=policy,
        )
        selected_topic = selection.get("selected") or {}
        topic_cluster = str(
            selected_topic.get("topic_cluster_id")
            or page.get("topic_cluster_id")
            or ""
        )
        final_url = str(
            selected_topic.get("source_url")
            or page.get("final_url")
            or page.get("url")
            or selected_url
        )
        digest = str(
            selected_topic.get("url_digest") or page.get("url_digest") or url_digest(final_url)
        )
        topic_labels = _topic_labels(candidates, selected_topic)
        wake_structured = build_structured_wake_question_candidates(
            topic_cluster_id_value=topic_cluster or digest,
            source_refs=[
                WEB_DREAM_LEARNING_STATE_REF,
                WEB_DREAM_BROWSER_SESSION_REF,
            ],
        )
        learned_state.update(
            {
                "status": "learned" if topic_labels else "learned_sparse",
                "final_url": final_url,
                "http_status": page.get("http_status"),
                "page_title": page.get("page_title", ""),
                "content_digest": _digest(str(page.get("text_sample") or "")),
                "url_digest": digest,
                "topic_cluster_id": topic_cluster,
                "topic_candidates": topic_labels,
                "structured_wake_question_candidates": wake_structured,
                "wake_question_candidates": wake_structured,
                "topic_selection_rationale": selection.get("selection_rationale", {}),
                "extracted_text_sample": page.get("text_sample", ""),
                "heading_candidates": list(page.get("headings", [])),
                "visited_urls": list(browser_session.get("visited_urls", [])),
                "page_count": browser_session.get("page_count", 0),
                "ref_set": _dedupe(
                    list(learned_state.get("ref_set", []))
                    + [
                        WEB_DREAM_BROWSER_SESSION_REF,
                        WEB_DREAM_TOPIC_HISTORY_REF,
                    ]
                ),
            }
        )
        _write_json(browser_session_path, browser_session)
        if topic_cluster and digest:
            topic_history = append_topic_history_entry(
                topic_history=topic_history,
                session_id=session_id,
                topic_cluster_id_value=topic_cluster,
                url_digest_value=digest,
                generated_at=generated_at,
                discovery_mode=discovery_mode,
            )
            write_topic_history(topic_history_path, topic_history)
    except Exception as exc:
        learned_state.update(
            {
                "status": "fetch_failed",
                "failure_type": exc.__class__.__name__,
                "failure_message": str(exc)[:240],
            }
        )

    _write_json(state_path, learned_state)
    event = _event_from_state(learned_state)
    _append_jsonl(log_path, event)
    return {"state": learned_state, "event": event}


def write_web_dream_learning_toggle(
    *,
    state_dir: Path,
    enabled: bool,
    generated_at: str,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    dream_dir = state_dir / "dream"
    seed_path = dream_dir / "web_dream_learning_seeds.json"
    state_path = dream_dir / "web_dream_learning_state.json"
    effective_environ = _effective_environ(environ)
    seed_payload = _read_json(seed_path)
    if not seed_payload:
        seed_payload = _seed_payload_from_env_defaults(effective_environ)
    seed_payload = _apply_env_defaults_to_seed_payload(
        seed_payload=seed_payload,
        environ=effective_environ,
    )
    if enabled:
        seed_payload["autonomous_discovery"] = {
            **dict(seed_payload.get("autonomous_discovery") or {}),
            "enabled": True,
            "open_web_read": True,
        }
    seed_urls = resolve_seed_urls(
        seed_payload=seed_payload,
        environ=effective_environ,
    )
    seed_payload.update(
        {
            "schema_version": "web_dream_learning_config_v1",
            "enabled": bool(enabled),
            "seed_urls": seed_urls,
            "manual_toggle_state": "enabled" if enabled else "disabled",
            "toggle_source": "terminal_slash_command",
            "updated_at": generated_at,
            "web_dream_learning_seeds_ref": WEB_DREAM_LEARNING_SEEDS_REF,
            "source_doc_refs": SOURCE_DOC_REFS,
        }
    )
    _write_json(seed_path, seed_payload)

    state_payload = _read_json(state_path)
    state_payload.update(
        {
            "schema_version": "web_dream_learning_state_v1",
            "status": "enabled_waiting_for_dream_cycle" if enabled else "disabled",
            "generated_at": generated_at,
            "manual_toggle_state": seed_payload["manual_toggle_state"],
            "toggle_source": "terminal_slash_command",
            "seed_count": len(seed_urls),
            "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
            "web_dream_learning_seeds_ref": WEB_DREAM_LEARNING_SEEDS_REF,
            "source_doc_refs": SOURCE_DOC_REFS,
        }
    )
    _write_json(state_path, state_payload)
    return {
        "schema_version": "web_dream_learning_toggle_result_v1",
        "status": state_payload["status"],
        "enabled": bool(enabled),
        "manual_toggle_state": seed_payload["manual_toggle_state"],
        "seed_count": len(seed_urls),
        "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
        "web_dream_learning_seeds_ref": WEB_DREAM_LEARNING_SEEDS_REF,
    }


def _default_seed_config() -> dict[str, Any]:
    return {
        "schema_version": "web_dream_learning_config_v1",
        "enabled": True,
        "external_action_policy": "read_only_no_side_effect",
        "browser_backend": "playwright_readonly",
        "fallback_backend": "urllib_mock_or_ci_fallback",
        "autonomous_discovery": {"enabled": True, "open_web_read": True},
        "topic_selection_policy": {
            "no_repeat_cluster_window": 3,
            "url_digest_cooldown_sessions": 5,
            "forbid_fixed_topic_table": True,
        },
    }


def _seed_payload_from_env_defaults(environ: Mapping[str, str]) -> dict[str, Any]:
    env_urls_present = bool(str(environ.get("DIGITAL_LIFE_WEB_DREAM_URLS") or "").strip())
    env_enabled = _optional_env_bool(
        environ.get("DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED")
    )
    enabled = env_urls_present if env_enabled is None else env_enabled
    payload = _default_seed_config()
    payload["enabled"] = enabled
    payload["autonomous_discovery"] = {
        "enabled": bool(enabled and not env_urls_present),
        "open_web_read": bool(enabled),
    }
    payload["env_default_applied"] = True
    return _apply_env_defaults_to_seed_payload(
        seed_payload=payload,
        environ=environ,
    )


def _apply_env_defaults_to_seed_payload(
    *,
    seed_payload: Mapping[str, Any],
    environ: Mapping[str, str],
) -> dict[str, Any]:
    payload = dict(seed_payload or {})
    env_enabled = _optional_env_bool(
        environ.get("DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED")
    )
    if "enabled" not in payload and env_enabled is not None:
        payload["enabled"] = env_enabled
    readonly = dict(payload.get("playwright_readonly") or {})
    max_hops = _optional_env_int(environ.get("DIGITAL_LIFE_WEB_DREAM_MAX_HOPS_PER_SEED"))
    if max_hops is not None and "max_hops_per_seed" not in readonly:
        readonly["max_hops_per_seed"] = max(0, min(max_hops, 8))
    timeout = _optional_env_float(
        environ.get("DIGITAL_LIFE_WEB_DREAM_MAX_SECONDS_PER_PAGE")
    )
    if timeout is not None and "max_seconds_per_page" not in readonly:
        readonly["max_seconds_per_page"] = max(0.5, min(timeout, 20.0))
    if readonly:
        payload["playwright_readonly"] = readonly
    return payload


def _discovery_mode(seed_payload: Mapping[str, Any], selected_index: int) -> str:
    relation_seeds = seed_payload.get("relation_curated_seeds") or []
    if isinstance(relation_seeds, list) and selected_index < len(relation_seeds):
        return "curated"
    if seed_payload.get("autonomous_discovery", {}).get("enabled", True):
        return "autonomous"
    return "curated"


def _fetch_page_adapter(fetch_url: FetchUrl | None):
    if fetch_url is None:
        return read_only_fetch_page

    def _adapter(url: str, timeout_seconds: float) -> dict[str, Any]:
        fetched = fetch_url(url, timeout_seconds)
        if isinstance(fetched, str):
            return read_only_fetch_page(url, timeout_seconds)
        text = str(fetched.get("text") or "")
        from life_v0.dream.web_dream_browser import extract_outbound_links, extract_page_profile

        profile = extract_page_profile(text)
        return {
            "status_code": fetched.get("status_code"),
            "final_url": fetched.get("final_url") or url,
            "content_type": fetched.get("content_type", ""),
            "text": text,
            "page_profile": profile,
            "outbound_links": extract_outbound_links(text, base_url=str(fetched.get("final_url") or url)),
            "browser_policy": "read_only_no_side_effect",
            "action_inhibition_seal": "closed",
        }

    return _adapter


def _visited_digests(topic_history: dict[str, Any]) -> set[str]:
    return {
        str(item.get("url_digest") or "")
        for item in topic_history.get("entries", [])
        if isinstance(item, dict) and item.get("url_digest")
    }


def _topic_labels(
    candidates: list[dict[str, Any]],
    selected: dict[str, Any],
) -> list[str]:
    labels: list[str] = []
    selected_label = str(selected.get("topic_label") or "")
    if selected_label:
        labels.append(selected_label)
    for candidate in candidates:
        label = str(candidate.get("topic_label") or "")
        if label and label not in labels:
            labels.append(label)
        if len(labels) >= 8:
            break
    return labels


def _event_from_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "web_dream_learning_event_v1",
        "sequence": state.get("sequence"),
        "session_id": state.get("session_id"),
        "generated_at": state.get("generated_at"),
        "status": state.get("status"),
        "discovery_mode": state.get("discovery_mode"),
        "selected_url": state.get("selected_url"),
        "topic_cluster_id": state.get("topic_cluster_id"),
        "url_digest": state.get("url_digest"),
        "page_title": state.get("page_title"),
        "topic_candidates": list(state.get("topic_candidates", [])),
        "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
    }


def _seed_enabled(*, seed_payload: dict[str, Any], seed_urls: list[str]) -> bool:
    if not seed_urls:
        return False
    if "enabled" not in seed_payload:
        return True
    return bool(seed_payload.get("enabled"))


def _timeout_seconds(seed_payload: dict[str, Any]) -> float:
    readonly = seed_payload.get("playwright_readonly") or {}
    try:
        value = float(readonly.get("max_seconds_per_page", seed_payload.get("timeout_seconds", 4.0)))
    except (TypeError, ValueError):
        value = 4.0
    return max(0.5, min(value, 20.0))


def _next_seed_index(previous_state: dict[str, Any], seed_count: int) -> int:
    previous = previous_state.get("selected_seed_index")
    try:
        previous_index = int(previous)
    except (TypeError, ValueError):
        previous_index = -1
    return (previous_index + 1) % max(seed_count, 1)


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


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


def _effective_environ(environ: Mapping[str, str] | None) -> Mapping[str, str]:
    if environ is not None:
        return environ
    try:
        runtime_config = load_digital_life_runtime_config()
        env_file = runtime_config.env_file
        if env_file and env_file.exists():
            file_env = _read_env_file(env_file)
            return {**file_env, **os.environ}
    except Exception:
        return os.environ
    return os.environ


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return values
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        values[key] = _unquote(value.strip())
    return values


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _optional_env_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if not normalized:
        return None
    if normalized in {"1", "true", "yes", "on", "enabled", "enable"}:
        return True
    if normalized in {"0", "false", "no", "off", "disabled", "disable"}:
        return False
    return None


def _optional_env_int(value: str | None) -> int | None:
    if value is None or not value.strip():
        return None
    try:
        return int(value.strip())
    except ValueError:
        return None


def _optional_env_float(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    try:
        return float(value.strip())
    except ValueError:
        return None


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
