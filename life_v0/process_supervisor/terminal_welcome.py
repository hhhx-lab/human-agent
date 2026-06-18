from __future__ import annotations

from pathlib import Path

from .terminal_session_tabs import list_terminal_session_tabs


def build_welcome_entries(
    *,
    terminal_dir: Path,
    life_name: str,
    limit: int = 8,
) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = [
        ("new", f"新建会话 · 与 {life_name} 开始对话"),
    ]
    for tab in list_terminal_session_tabs(terminal_dir=terminal_dir, limit=limit):
        marker = "当前" if tab.is_current else "恢复"
        entries.append((tab.session_id, f"{marker} · {tab.label}"))
    return entries


def format_welcome_fragments(
    *,
    terminal_dir: Path,
    life_name: str,
    selection: int,
    width: int,
) -> list[tuple[str, str]]:
    entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=life_name)
    if not entries:
        entries = [("new", "新建会话")]
    selected = max(0, min(selection, len(entries) - 1))
    inner = max(24, width - 4)
    line = "─" * inner
    fragments: list[tuple[str, str]] = [
        ("class:welcome-title", f"\n  {life_name}\n"),
        ("class:welcome-subtitle", "  数字生命终端 · Welcome\n"),
        ("class:top-bar", f"  ┌{line}┐\n"),
        ("class:welcome-section", "  │ 最近会话\n"),
    ]
    for index, (session_id, label) in enumerate(entries):
        prefix = "› " if index == selected else "  "
        style = "class:welcome-active" if index == selected else "class:welcome-line"
        text = f"{prefix}{index + 1}. {label}"
        if len(text) > inner - 2:
            text = text[: max(8, inner - 5)] + "…"
        fragments.append((style, f"  │ {text}\n"))
    fragments.extend(
        [
            ("class:top-bar", f"  └{line}┘\n"),
            ("class:hint", "  Enter 进入  ↑↓ 选择  Ctrl+S 恢复  Ctrl+N 新建  Ctrl+Q 退出\n"),
        ]
    )
    return fragments