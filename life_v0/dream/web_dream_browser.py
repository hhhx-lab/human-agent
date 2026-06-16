from __future__ import annotations

import hashlib
import re
import urllib.error
import urllib.request
from html.parser import HTMLParser
from typing import Any, Callable, Mapping, Protocol
from urllib.parse import urljoin, urlparse

WEB_DREAM_BROWSER_SESSION_REF = "runtime/state/dream/web_dream_browser_session.json"

FetchPage = Callable[[str, float], dict[str, Any]]


class ReadOnlyBrowser(Protocol):
    def read_page(self, url: str, *, timeout_seconds: float) -> dict[str, Any]: ...


def read_only_fetch_page(url: str, timeout_seconds: float) -> dict[str, Any]:
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("web dream browser only reads http/https urls")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "human-agent-live0-web-dream-browser/0.1",
            "Accept": "text/html,text/plain;q=0.9,*/*;q=0.5",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read(512_000)
            charset = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
            status_code = getattr(response, "status", None)
            final_url = response.geturl()
            content_type = response.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        raw = exc.read(64_000)
        text = raw.decode("utf-8", errors="replace")
        status_code = exc.code
        final_url = url
        content_type = exc.headers.get("content-type", "") if exc.headers else ""
    profile = extract_page_profile(text)
    outbound = extract_outbound_links(text, base_url=final_url)
    return {
        "status_code": status_code,
        "final_url": final_url,
        "content_type": content_type,
        "text": text,
        "page_profile": profile,
        "outbound_links": outbound,
        "browser_policy": "read_only_no_side_effect",
        "action_inhibition_seal": "closed",
    }


def run_readonly_browse_session(
    *,
    start_url: str,
    generated_at: str,
    session_id: str,
    max_hops: int = 2,
    timeout_seconds: float = 8.0,
    fetch_page: FetchPage | None = None,
    visited_url_digests: set[str] | None = None,
) -> dict[str, Any]:
    fetch_page = fetch_page or read_only_fetch_page
    visited = set(visited_url_digests or [])
    pages: list[dict[str, Any]] = []
    current_url = start_url
    hops = 0
    while current_url and hops <= max_hops:
        digest = url_digest(current_url)
        if digest in visited:
            break
        visited.add(digest)
        try:
            fetched = fetch_page(current_url, timeout_seconds)
        except Exception as exc:
            pages.append(
                {
                    "url": current_url,
                    "url_digest": digest,
                    "status": "fetch_failed",
                    "failure_message": str(exc)[:200],
                }
            )
            break
        profile = fetched.get("page_profile") or extract_page_profile(
            str(fetched.get("text") or "")
        )
        pages.append(
            {
                "url": current_url,
                "final_url": fetched.get("final_url") or current_url,
                "url_digest": digest,
                "status": "read",
                "http_status": fetched.get("status_code"),
                "page_title": profile.get("title", ""),
                "headings": list(profile.get("headings", []))[:8],
                "text_sample": str(profile.get("text_sample", ""))[:800],
                "outbound_link_count": len(fetched.get("outbound_links", [])),
                "browser_policy": fetched.get("browser_policy"),
            }
        )
        hops += 1
        if hops > max_hops:
            break
        outbound = list(fetched.get("outbound_links", []))
        next_url = ""
        for link in outbound:
            candidate_digest = url_digest(link)
            if candidate_digest not in visited:
                next_url = link
                break
        current_url = next_url

    return {
        "schema_version": "web_dream_browser_session_v1",
        "generated_at": generated_at,
        "session_id": session_id,
        "start_url": start_url,
        "visited_urls": [page.get("final_url") or page.get("url") for page in pages],
        "page_count": len(pages),
        "pages": pages,
        "external_action_policy": "read_only_no_side_effect",
        "allow_click": False,
        "allow_form_fill": False,
        "allow_download": False,
        "action_inhibition_seal": "closed",
        "web_dream_browser_session_ref": WEB_DREAM_BROWSER_SESSION_REF,
    }


def extract_page_profile(raw_text: str) -> dict[str, Any]:
    parser = _HtmlParser()
    parser.feed(raw_text[:512_000])
    text = _clean_text(" ".join(parser.text_chunks))
    return {
        "title": _clean_text(parser.title)[:160],
        "headings": _dedupe([_clean_text(item)[:160] for item in parser.headings])[:8],
        "text_sample": text[:1200],
    }


def extract_outbound_links(raw_text: str, *, base_url: str) -> list[str]:
    hrefs = re.findall(r"""href=["']([^"'#]+)["']""", raw_text[:256_000], flags=re.I)
    base_host = urlparse(base_url).netloc
    result: list[str] = []
    for href in hrefs:
        absolute = urljoin(base_url, href.strip())
        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"}:
            continue
        if not parsed.netloc:
            continue
        if parsed.netloc != base_host and len(result) >= 12:
            continue
        if absolute not in result:
            result.append(absolute)
        if len(result) >= 16:
            break
    return result


def url_digest(url: str) -> str:
    normalized = urlparse(url)._replace(fragment="", query="").geturl()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def topic_cluster_id(*, title: str, headings: list[str], text_sample: str, domain: str) -> str:
    payload = "|".join(
        [
            _clean_text(title)[:80],
            _clean_text(" ".join(headings[:2]))[:80],
            _clean_text(text_sample)[:120],
            domain,
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


class _HtmlParser(HTMLParser):
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


def _clean_text(text: str) -> str:
    return " ".join(str(text or "").split())


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result