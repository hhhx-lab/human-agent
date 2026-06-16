from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from life_v0.dream.web_dream_browser import topic_cluster_id, url_digest

WEB_DREAM_TOPIC_HISTORY_REF = "runtime/state/dream/web_dream_topic_history.json"

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/real—live0/08_dream_sleep_offline_life.md",
]


def build_structured_wake_question_candidates(
    *,
    topic_cluster_id_value: str,
    source_refs: list[str],
    intent: str = "continue_learning",
) -> list[dict[str, Any]]:
    return [
        {
            "schema_version": "structured_wake_question_candidate_v1",
            "candidate_id": f"wake-q-{topic_cluster_id_value}",
            "topic_cluster_id": topic_cluster_id_value,
            "intent": intent,
            "source_refs": list(source_refs),
            "expression_policy": "model_generated_only_no_fixed_sentence",
            "literal_text": None,
        }
    ]


def select_topic_candidate(
    *,
    candidates: list[dict[str, Any]],
    topic_history: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    topic_history = topic_history or {}
    policy = policy or {}
    no_repeat_window = int(policy.get("no_repeat_cluster_window", 3) or 3)
    url_cooldown = int(policy.get("url_digest_cooldown_sessions", 5) or 5)
    entries = [
        item for item in topic_history.get("entries", []) if isinstance(item, dict)
    ]
    recent_clusters = {
        str(item.get("topic_cluster_id") or "")
        for item in entries[-no_repeat_window:]
    }
    recent_url_digests = {
        str(item.get("url_digest") or "") for item in entries[-url_cooldown:]
    }

    scored: list[tuple[float, dict[str, Any]]] = []
    for candidate in candidates:
        cluster = str(candidate.get("topic_cluster_id") or "")
        digest = str(candidate.get("url_digest") or "")
        if cluster and cluster in recent_clusters:
            continue
        if digest and digest in recent_url_digests:
            continue
        score = float(candidate.get("selection_score", 0.0) or 0.0)
        scored.append((score, candidate))
    scored.sort(key=lambda item: -item[0])
    if not scored:
        return {
            "selected": None,
            "selection_rationale": {
                "reason": "all_candidates_filtered_by_cooldown",
                "candidate_count": len(candidates),
            },
        }
    selected = scored[0][1]
    return {
        "selected": selected,
        "selection_rationale": {
            "selection_score": scored[0][0],
            "topic_cluster_id": selected.get("topic_cluster_id"),
            "url_digest": selected.get("url_digest"),
            "forbid_fixed_topic_table": True,
        },
    }


def append_topic_history_entry(
    *,
    topic_history: dict[str, Any],
    session_id: str,
    topic_cluster_id_value: str,
    url_digest_value: str,
    generated_at: str,
    discovery_mode: str,
) -> dict[str, Any]:
    updated = dict(topic_history or {})
    updated.setdefault("schema_version", "web_dream_topic_history_v1")
    entries = list(updated.get("entries", []))
    entries.append(
        {
            "session_id": session_id,
            "topic_cluster_id": topic_cluster_id_value,
            "url_digest": url_digest_value,
            "generated_at": generated_at,
            "discovery_mode": discovery_mode,
        }
    )
    updated["entries"] = entries[-200:]
    updated["web_dream_topic_history_ref"] = WEB_DREAM_TOPIC_HISTORY_REF
    return updated


def topic_candidates_from_page(
    *,
    page: dict[str, Any],
    relation_theme_tags: list[str] | None = None,
    dream_residue_weight: float = 0.0,
) -> list[dict[str, Any]]:
    title = str(page.get("page_title") or "")
    headings = [str(item) for item in page.get("headings", []) if item]
    text_sample = str(page.get("text_sample") or "")
    final_url = str(page.get("final_url") or page.get("url") or "")
    domain = urlparse(final_url).netloc
    cluster = topic_cluster_id(
        title=title,
        headings=headings,
        text_sample=text_sample,
        domain=domain,
    )
    digest = str(page.get("url_digest") or url_digest(final_url))
    base_score = 0.35
    if title:
        base_score += 0.2
    if headings:
        base_score += 0.1
    base_score += min(len(relation_theme_tags or []) * 0.05, 0.2)
    base_score += min(dream_residue_weight, 0.25)
    candidates = []
    labels = [title] + headings[:3]
    for label in labels:
        if not label:
            continue
        candidates.append(
            {
                "topic_label": label,
                "topic_cluster_id": cluster,
                "url_digest": digest,
                "source_url": final_url,
                "selection_score": base_score,
            }
        )
    return candidates


def read_topic_history(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": "web_dream_topic_history_v1", "entries": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {"schema_version": "web_dream_topic_history_v1", "entries": []}
    return payload if isinstance(payload, dict) else {"entries": []}


def write_topic_history(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def default_world_seed_catalog() -> list[dict[str, Any]]:
    return [
        {
            "name": "GitHub Trending",
            "url": "https://github.com/trending",
            "category": "code_and_open_source",
            "priority": 100,
        },
        {
            "name": "GitHub Explore",
            "url": "https://github.com/explore",
            "category": "code_and_open_source",
            "priority": 98,
        },
        {
            "name": "Hugging Face Models",
            "url": "https://huggingface.co/models",
            "category": "ai_models",
            "priority": 95,
        },
        {
            "name": "Hugging Face Papers",
            "url": "https://huggingface.co/papers",
            "category": "ai_research",
            "priority": 94,
        },
        {
            "name": "Nature",
            "url": "https://www.nature.com/",
            "category": "authority_science_journal",
            "priority": 92,
        },
        {
            "name": "Nature Neuroscience",
            "url": "https://www.nature.com/neuro/",
            "category": "authority_neuroscience_journal",
            "priority": 93,
        },
        {
            "name": "Science",
            "url": "https://www.science.org/",
            "category": "authority_science_journal",
            "priority": 92,
        },
        {
            "name": "PubMed",
            "url": "https://pubmed.ncbi.nlm.nih.gov/",
            "category": "biomedical_index",
            "priority": 90,
        },
        {
            "name": "Cell",
            "url": "https://www.cell.com/",
            "category": "authority_life_science_journal",
            "priority": 88,
        },
        {
            "name": "PNAS",
            "url": "https://www.pnas.org/",
            "category": "authority_science_journal",
            "priority": 86,
        },
        {
            "name": "Papers with Code",
            "url": "https://paperswithcode.com/",
            "category": "ai_research_code_bridge",
            "priority": 86,
        },
        {
            "name": "arXiv cs.AI",
            "url": "https://arxiv.org/list/cs.AI/recent",
            "category": "ai_research_preprint",
            "priority": 84,
        },
        {
            "name": "AI Hot Daily",
            "url": "https://aihot.virxact.com/daily",
            "category": "ai_daily_digest",
            "priority": 84,
        },
        {
            "name": "Linux.do",
            "url": "https://linux.do/",
            "category": "developer_community",
            "priority": 80,
        },
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com/",
            "category": "developer_community",
            "priority": 78,
        },
        {
            "name": "Bilibili",
            "url": "https://www.bilibili.com/",
            "category": "chinese_video_culture",
            "priority": 72,
        },
        {
            "name": "X / Twitter Explore",
            "url": "https://x.com/explore",
            "category": "social_signal",
            "priority": 70,
        },
        {
            "name": "今日头条",
            "url": "https://www.toutiao.com/",
            "category": "chinese_news_and_social_signal",
            "priority": 68,
        },
        {
            "name": "Reddit Machine Learning",
            "url": "https://www.reddit.com/r/MachineLearning/",
            "category": "research_community_signal",
            "priority": 66,
        },
    ]


def resolve_seed_urls(
    *,
    seed_payload: Mapping[str, Any],
    environ: Mapping[str, str] | None = None,
) -> list[str]:
    urls: list[str] = []
    relation_seeds = seed_payload.get("relation_curated_seeds") or seed_payload.get(
        "user_curated_seeds"
    )
    if isinstance(relation_seeds, list):
        for item in relation_seeds:
            if isinstance(item, dict) and item.get("url"):
                urls.append(str(item["url"]))
            elif isinstance(item, str):
                urls.append(item)
    for item in seed_payload.get("seed_urls", []) or []:
        urls.append(str(item))
    catalog = seed_payload.get("default_world_seed_catalog")
    if isinstance(catalog, list):
        for item in sorted(
            [entry for entry in catalog if isinstance(entry, dict)],
            key=lambda entry: -int(entry.get("priority", 0) or 0),
        ):
            if item.get("url"):
                urls.append(str(item["url"]))
    if not urls and seed_payload.get("autonomous_discovery", {}).get("enabled", True):
        urls.extend(item["url"] for item in default_world_seed_catalog())
    if environ:
        raw = str(environ.get("DIGITAL_LIFE_WEB_DREAM_URLS") or "")
        urls.extend(item.strip() for item in raw.split(",") if item.strip())
    deduped: list[str] = []
    for url in urls:
        if url and url not in deduped:
            deduped.append(url)
    return deduped
