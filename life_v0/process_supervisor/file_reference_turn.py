from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REFERENCE_PATTERN = re.compile(r"@([^\s]+)")
MAX_FILE_CHARS = 4000


@dataclass(frozen=True)
class ExpandedRelationTurn:
    utterance: str
    references: list[dict[str, str]]


def expand_file_references_for_relation_turn(
    utterance: str,
    *,
    repo_root: Path,
) -> ExpandedRelationTurn:
    text = str(utterance or "")
    references: list[dict[str, str]] = []
    blocks: list[str] = []
    for match in REFERENCE_PATTERN.finditer(text):
        raw_ref = match.group(1).strip().rstrip(".,;，。；")
        if not raw_ref:
            continue
        status, resolved, reason = _resolve_reference(raw_ref, repo_root=repo_root)
        item = {"path": raw_ref, "status": status}
        if reason:
            item["reason"] = reason
        references.append(item)
        if status != "included" or resolved is None:
            continue
        if resolved.is_dir():
            entries = _directory_preview(resolved, repo_root=repo_root)
            blocks.append(f"引用文件夹: {raw_ref}\n{entries}")
            continue
        content = _read_text_preview(resolved)
        blocks.append(f"引用文件: {raw_ref}\n{content}")
    if not blocks:
        return ExpandedRelationTurn(utterance=text, references=references)
    expanded = text + "\n\n" + "\n\n".join(blocks)
    return ExpandedRelationTurn(utterance=expanded, references=references)


def _resolve_reference(
    raw_ref: str,
    *,
    repo_root: Path,
) -> tuple[str, Path | None, str]:
    clean = raw_ref.replace("\\", "/").lstrip("/")
    if not clean or clean.startswith("~"):
        return "blocked", None, "invalid_reference"
    first = clean.split("/", 1)[0]
    if first in {".git", ".venv", "runtime", "node_modules", ".pytest_cache", ".codex"}:
        return "blocked", None, "blocked_root"
    if clean == ".env" or clean.startswith(".env."):
        if clean != ".env.example":
            return "blocked", None, "secret_env_file"
    path = (repo_root / clean).resolve()
    try:
        path.relative_to(repo_root.resolve())
    except ValueError:
        return "blocked", None, "outside_repo"
    if not path.exists():
        return "missing", None, "not_found"
    if path.is_file() and path.stat().st_size > 512_000:
        return "blocked", None, "file_too_large"
    return "included", path, ""


def _read_text_preview(path: Path) -> str:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "<unreadable>"
    return raw[:MAX_FILE_CHARS]


def _directory_preview(path: Path, *, repo_root: Path) -> str:
    entries: list[str] = []
    for child in sorted(path.iterdir(), key=lambda item: item.name.lower())[:40]:
        try:
            rel = child.relative_to(repo_root).as_posix()
        except ValueError:
            rel = child.name
        suffix = "/" if child.is_dir() else ""
        entries.append(rel + suffix)
    return "\n".join(entries)

