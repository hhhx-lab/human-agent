from __future__ import annotations

import re
from typing import Iterable

CODE_FENCE_RE = re.compile(r"```(\w+)?\n?")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s+(.+)$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def format_markdown_body_fragments(text: str) -> list[tuple[str, str]]:
    normalized = str(text or "")
    if not normalized.strip():
        return [("class:message-body", "\n")]

    fragments: list[tuple[str, str]] = []
    cursor = 0
    for match in CODE_FENCE_RE.finditer(normalized):
        fragments.extend(
            _format_plain_markdown_block(normalized[cursor : match.start()])
        )
        cursor = match.end()
        language = str(match.group(1) or "").strip()
        end = normalized.find("```", cursor)
        if end == -1:
            code = normalized[cursor:]
            cursor = len(normalized)
        else:
            code = normalized[cursor:end]
            cursor = end + 3
        fragments.extend(_format_code_block(code, language=language))
    fragments.extend(_format_plain_markdown_block(normalized[cursor:]))
    return fragments


def _format_plain_markdown_block(text: str) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = []
    for line in str(text or "").splitlines() or [""]:
        if not line:
            fragments.append(("", "\n"))
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            style = f"class:md-h{min(level, 3)}"
            fragments.append((style, f"  {heading.group(2)}\n"))
            continue
        bullet = LIST_RE.match(line)
        if bullet:
            marker = bullet.group(2)
            body = bullet.group(3)
            fragments.extend(
                [
                    ("class:md-list", f"  {marker} "),
                    *_format_inline_markdown(body),
                    ("", "\n"),
                ]
            )
            continue
        fragments.append(("class:message-body", "  "))
        fragments.extend(_format_inline_markdown(line))
        fragments.append(("", "\n"))
    return fragments


def _format_inline_markdown(text: str) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = []
    cursor = 0
    for match in LINK_RE.finditer(text):
        if match.start() > cursor:
            fragments.extend(
                _format_inline_code_spans(text[cursor : match.start()])
            )
        fragments.append(("class:md-link", match.group(1)))
        fragments.append(("class:hint", f" ({match.group(2)})"))
        cursor = match.end()
    fragments.extend(_format_inline_code_spans(text[cursor:]))
    return fragments


def _format_inline_code_spans(text: str) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = []
    cursor = 0
    for match in INLINE_CODE_RE.finditer(text):
        if match.start() > cursor:
            fragments.append(("class:message-body", text[cursor : match.start()]))
        fragments.append(("class:md-code-inline", match.group(1)))
        cursor = match.end()
    if cursor < len(text):
        fragments.append(("class:message-body", text[cursor:]))
    return fragments


def _format_code_block(text: str, *, language: str) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = []
    if language:
        fragments.append(("class:md-code-lang", f"  {language}\n"))
    for line in str(text or "").splitlines() or [""]:
        fragments.append(("class:code-block", f"  {line}\n" if line else "\n"))
    return fragments


def highlight_code_language(language: str, lines: Iterable[str]) -> list[tuple[str, str]]:
    normalized = str(language or "").strip().lower()
    fragments: list[tuple[str, str]] = []
    for line in lines:
        if normalized in {"py", "python"}:
            fragments.extend(_highlight_python_line(line))
        else:
            fragments.append(("class:code-block", f"  {line}\n" if line else "\n"))
    return fragments


def _highlight_python_line(line: str) -> list[tuple[str, str]]:
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return [("class:md-comment", f"  {line}\n")]
    if stripped.startswith(("def ", "class ", "return ", "import ", "from ")):
        return [("class:md-keyword", f"  {line}\n")]
    if '"' in line or "'" in line:
        return [("class:md-string", f"  {line}\n")]
    return [("class:code-block", f"  {line}\n" if line else "\n")]