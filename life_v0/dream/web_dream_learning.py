from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Mapping


WEB_DREAM_LEARNING_STATE_REF = "runtime/state/dream/web_dream_learning_state.json"
WEB_DREAM_LEARNING_LOG_REF = "runtime/state/dream/web_dream_learning_log.jsonl"
WEB_DREAM_LEARNING_SEEDS_REF = "runtime/state/dream/web_dream_learning_seeds.json"

SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
]

FetchUrl = Callable[[str, float], Mapping[str, Any] | str]


def record_web_dream_learning(
    *,
    state_dir: Path,
    generated_at: str,
    fetch_url: FetchUrl | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    dream_dir = state_dir / "dream"
    state_path = dream_dir / "web_dream_learning_state.json"
    log_path = dream_dir / "web_dream_learning_log.jsonl"
    seed_path = dream_dir / "web_dream_learning_seeds.json"

    previous_state = _read_json(state_path)
    seed_payload = _read_json(seed_path)
    seed_urls = _seed_urls(seed_payload) or _env_seed_urls(environ or os.environ)
    enabled = _seed_enabled(seed_payload=seed_payload, seed_urls=seed_urls)
    timeout_seconds = _timeout_seconds(seed_payload)
    sequence = _jsonl_count(log_path) + 1

    base_state: dict[str, Any] = {
        "schema_version": "web_dream_learning_state_v0",
        "status": "disabled" if not enabled else "no_seed_urls",
        "generated_at": generated_at,
        "sequence": sequence,
        "external_action_policy": "read_configured_seed_url_only_no_side_effect",
        "seed_count": len(seed_urls),
        "selected_seed_index": None,
        "selected_url": None,
        "page_title": "",
        "content_digest": "",
        "topic_candidates": [],
        "wake_question_candidates": [],
        "dream_learning_summary": "",
        "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
        "web_dream_learning_log_ref": WEB_DREAM_LEARNING_LOG_REF,
        "web_dream_learning_seeds_ref": (
            WEB_DREAM_LEARNING_SEEDS_REF if seed_payload else None
        ),
        "ref_set": _dedupe(
            [
                WEB_DREAM_LEARNING_STATE_REF,
                WEB_DREAM_LEARNING_LOG_REF,
                WEB_DREAM_LEARNING_SEEDS_REF if seed_payload else "",
            ]
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }
    if not enabled or not seed_urls:
        _write_json(state_path, base_state)
        _append_jsonl(log_path, _event_from_state(base_state))
        return {"state": base_state, "event": _event_from_state(base_state)}

    selected_index = _next_seed_index(previous_state, len(seed_urls))
    selected_url = seed_urls[selected_index]
    learned_state = dict(base_state)
    learned_state.update(
        {
            "status": "fetching",
            "selected_seed_index": selected_index,
            "selected_url": selected_url,
        }
    )
    try:
        fetched = (fetch_url or _fetch_url)(selected_url, timeout_seconds)
        fetched_payload = _normalize_fetch_result(fetched, selected_url)
        extracted = _extract_page_profile(fetched_payload.get("text", ""))
        topic_candidates = _topic_candidates(extracted)
        learned_state.update(
            {
                "status": "learned" if topic_candidates else "learned_sparse",
                "final_url": fetched_payload.get("final_url") or selected_url,
                "http_status": fetched_payload.get("status_code"),
                "content_type": fetched_payload.get("content_type", ""),
                "page_title": extracted["title"],
                "content_digest": _digest(fetched_payload.get("text", "")),
                "topic_candidates": topic_candidates,
                "wake_question_candidates": _wake_question_candidates(
                    topic_candidates
                ),
                "dream_learning_summary": _learning_summary(
                    selected_url=selected_url,
                    extracted=extracted,
                    topic_candidates=topic_candidates,
                ),
                "extracted_text_sample": extracted["text_sample"],
                "heading_candidates": extracted["headings"],
            }
        )
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


def _fetch_url(url: str, timeout_seconds: float) -> dict[str, Any]:
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("web_dream_learning only reads http/https seed urls")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "human-agent-live0-web-dream-learning/0.1",
            "Accept": "text/html,text/plain;q=0.9,*/*;q=0.5",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read(512_000)
            content_type = response.headers.get("content-type", "")
            charset = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
            status_code = getattr(response, "status", None)
            final_url = response.geturl()
    except urllib.error.HTTPError as exc:
        raw = exc.read(64_000)
        text = raw.decode("utf-8", errors="replace")
        status_code = exc.code
        content_type = exc.headers.get("content-type", "") if exc.headers else ""
        final_url = url
    return {
        "status_code": status_code,
        "final_url": final_url,
        "content_type": content_type,
        "text": text,
    }


def _normalize_fetch_result(fetched: Mapping[str, Any] | str, url: str) -> dict[str, Any]:
    if isinstance(fetched, str):
        return {
            "status_code": None,
            "final_url": url,
            "content_type": "",
            "text": fetched,
        }
    return {
        "status_code": fetched.get("status_code"),
        "final_url": str(fetched.get("final_url") or url),
        "content_type": str(fetched.get("content_type") or ""),
        "text": str(fetched.get("text") or ""),
    }


def _extract_page_profile(raw_text: str) -> dict[str, Any]:
    parser = _HtmlLearningParser()
    parser.feed(raw_text[:512_000])
    text = _clean_text(" ".join(parser.text_chunks))
    return {
        "title": _clean_text(parser.title)[:160],
        "headings": _dedupe([_clean_text(item)[:160] for item in parser.headings])[:8],
        "text_sample": text[:1200],
    }


def _topic_candidates(extracted: dict[str, Any]) -> list[str]:
    candidates: list[str] = []
    title = str(extracted.get("title") or "").strip()
    if title:
        candidates.append(title)
    candidates.extend(str(item).strip() for item in extracted.get("headings", []))
    text_sample = str(extracted.get("text_sample") or "")
    candidates.extend(_keyword_candidates(text_sample))
    return _dedupe([item for item in candidates if item])[:8]


def _keyword_candidates(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}|[\u4e00-\u9fff]{2,8}", text)
    stopwords = {
        "about",
        "after",
        "also",
        "from",
        "have",
        "this",
        "that",
        "with",
        "your",
        "更多",
        "登录",
        "注册",
        "首页",
        "关于",
    }
    result: list[str] = []
    for word in words:
        lowered = word.lower()
        if lowered in stopwords or word in stopwords:
            continue
        if word not in result:
            result.append(word)
        if len(result) >= 6:
            break
    return result


def _wake_question_candidates(topic_candidates: list[str]) -> list[str]:
    return [f"wake_question_about:{topic}" for topic in topic_candidates[:3]]


def _learning_summary(
    *,
    selected_url: str,
    extracted: dict[str, Any],
    topic_candidates: list[str],
) -> str:
    title = str(extracted.get("title") or "").strip()
    topics = "、".join(topic_candidates[:3])
    if title and topics:
        return f"{title} -> {topics}"
    if topics:
        return topics
    return selected_url


def _event_from_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "web_dream_learning_event_v0",
        "sequence": state.get("sequence"),
        "generated_at": state.get("generated_at"),
        "status": state.get("status"),
        "selected_url": state.get("selected_url"),
        "page_title": state.get("page_title"),
        "topic_candidates": list(state.get("topic_candidates", [])),
        "web_dream_learning_state_ref": WEB_DREAM_LEARNING_STATE_REF,
    }


class _HtmlLearningParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._tag_stack: list[str] = []
        self.title = ""
        self.headings: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._tag_stack.append(tag.lower())

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        for index in range(len(self._tag_stack) - 1, -1, -1):
            if self._tag_stack[index] == lowered:
                del self._tag_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        current = self._tag_stack[-1] if self._tag_stack else ""
        text = _clean_text(data)
        if not text:
            return
        if current == "title":
            self.title = _clean_text(f"{self.title} {text}")
        elif current in {"h1", "h2", "h3"}:
            self.headings.append(text)
        elif current not in {"script", "style", "noscript"}:
            self.text_chunks.append(text)


def _seed_urls(seed_payload: dict[str, Any]) -> list[str]:
    urls = seed_payload.get("seed_urls")
    if not isinstance(urls, list):
        return []
    return _dedupe([str(url).strip() for url in urls if str(url).strip()])


def _env_seed_urls(environ: Mapping[str, str]) -> list[str]:
    raw = str(environ.get("DIGITAL_LIFE_WEB_DREAM_URLS") or "")
    return _dedupe([item.strip() for item in raw.split(",") if item.strip()])


def _seed_enabled(*, seed_payload: dict[str, Any], seed_urls: list[str]) -> bool:
    if not seed_urls:
        return False
    if "enabled" not in seed_payload:
        return True
    return bool(seed_payload.get("enabled"))


def _timeout_seconds(seed_payload: dict[str, Any]) -> float:
    try:
        value = float(seed_payload.get("timeout_seconds", 4.0))
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


def _clean_text(text: str) -> str:
    return " ".join(str(text or "").split())


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


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
