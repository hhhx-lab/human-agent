from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .terminal_input import iter_slash_command_entries


@dataclass(frozen=True)
class PaletteItem:
    label: str
    detail: str
    action: str
    group: str = "命令"


def build_palette_items(
    *,
    slash_commands: tuple[tuple[Any, ...], ...] | list[tuple[Any, ...]],
) -> list[PaletteItem]:
    items: list[PaletteItem] = [
        PaletteItem("Ctrl+B", "切换 Live 侧栏", "hint:sidebar", group="快捷键"),
        PaletteItem("Ctrl+P", "命令面板", "hint:palette", group="快捷键"),
        PaletteItem("Ctrl+Y", "轮换主题", "hint:theme", group="快捷键"),
        PaletteItem("Ctrl+T", "新建 session", "hint:new_session", group="快捷键"),
        PaletteItem("Ctrl+O", "块浏览模式", "hint:scrollback", group="滚动"),
        PaletteItem("h / l", "折叠 / 展开块", "hint:fold", group="滚动"),
        PaletteItem("Enter", "全屏查看选中块", "hint:viewer", group="滚动"),
    ]
    for command, detail in iter_slash_command_entries(slash_commands):
        group, _, rest = str(detail).partition("｜")
        items.append(
            PaletteItem(
                command,
                rest or detail or command,
                f"slash:{command}",
                group=group or "命令",
            )
        )
    return items


def resolve_palette_visible_items(
    items: list[PaletteItem],
    *,
    query: str,
) -> list[PaletteItem]:
    return filter_palette_items(items, query=query) or list(items)


def filter_palette_items(
    items: list[PaletteItem],
    *,
    query: str,
) -> list[PaletteItem]:
    normalized = str(query or "").strip().lower()
    if not normalized:
        return list(items)
    if normalized.startswith("/"):
        normalized = normalized[1:]
    filtered: list[PaletteItem] = []
    for item in items:
        label = str(item.label or "").lower()
        command_key = label[1:] if label.startswith("/") else label
        detail = str(item.detail or "").lower()
        group = str(item.group or "").lower()
        haystack = f"{label} {command_key} {detail} {group}"
        if (
            normalized in haystack
            or command_key.startswith(normalized)
            or label.startswith(f"/{normalized}")
        ):
            filtered.append(item)
    return filtered


def _truncate_line(text: str, *, width: int) -> str:
    if len(text) <= width:
        return text
    return text[: max(8, width - 1)] + "…"


def _wrap_detail_lines(detail: str, *, width: int, max_lines: int = 3) -> list[str]:
    normalized = " ".join(str(detail or "").split())
    if not normalized:
        return ["(无简介)"]
    if len(normalized) <= max(12, width - 4):
        return [normalized]
    words = normalized.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max(12, width - 4):
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    if len(words) > len(" ".join(lines).split()) and lines:
        lines[-1] = _truncate_line(lines[-1], width=width - 4) + " …"
    return lines or [normalized[: max(12, width - 4)]]


def palette_list_line_count(
    *,
    items: list[PaletteItem],
    query: str,
) -> int:
    visible = resolve_palette_visible_items(items, query=query)
    lines = 0
    current_group = ""
    for item in visible:
        if item.group and item.group != current_group:
            current_group = item.group
            lines += 1
        lines += 1
    return max(lines, 1)


def palette_list_line_offset(
    *,
    items: list[PaletteItem],
    query: str,
    selection: int,
) -> int:
    visible = resolve_palette_visible_items(items, query=query)
    if not visible:
        return 0
    active = selection % len(visible)
    offset = 0
    current_group = ""
    for index, item in enumerate(visible):
        if item.group and item.group != current_group:
            current_group = item.group
            offset += 1
        if index == active:
            return offset
        offset += 1
    return offset


def apply_palette_list_scroll_policy(
    *,
    pane,
    items: list[PaletteItem],
    query: str,
    selection: int,
    visible_height: int,
) -> None:
    line_offset = palette_list_line_offset(
        items=items,
        query=query,
        selection=selection,
    )
    total_lines = palette_list_line_count(items=items, query=query)
    viewport = max(4, int(visible_height))
    max_scroll = max(0, total_lines - viewport)
    target = max(0, min(max_scroll, line_offset - max(1, viewport // 3)))
    pane.vertical_scroll = target


def format_palette_list_fragments(
    *,
    items: list[PaletteItem],
    selection: int,
    query: str,
    width: int,
) -> list[tuple[str, str]]:
    visible = resolve_palette_visible_items(items, query=query)
    active_index = selection % max(1, len(visible))
    fragments: list[tuple[str, str]] = [
        ("class:hint", f" {len(visible)} 项")
    ]
    if query.strip():
        fragments.append(("class:hint", f" · 筛选「{query.strip()}」"))
    fragments.append(("class:hint", "\n"))
    current_group = ""
    for index, item in enumerate(visible):
        if item.group and item.group != current_group:
            current_group = item.group
            fragments.append(("class:slash-panel-group", f" [{current_group}]\n"))
        prefix = "› " if index == active_index else "  "
        style = "class:palette-active" if index == active_index else "class:palette-item"
        line = f"{prefix}{item.label}"
        fragments.append((style, _truncate_line(line, width=width - 2) + "\n"))
    return fragments


def format_palette_detail_fragments(
    *,
    items: list[PaletteItem],
    selection: int,
    query: str,
    width: int,
) -> list[tuple[str, str]]:
    visible = resolve_palette_visible_items(items, query=query)
    if not visible:
        return [
            ("class:palette-title", " 命令简介\n"),
            ("class:palette-detail", " 输入关键词筛选 / 命令。\n"),
        ]
    item = visible[selection % len(visible)]
    fragments: list[tuple[str, str]] = [
        ("class:palette-title", f" {item.label}\n"),
        ("class:slash-panel-group", f" [{item.group}]\n"),
    ]
    for line in _wrap_detail_lines(item.detail, width=width, max_lines=4):
        fragments.append(("class:palette-detail", f" {line}\n"))
    return fragments


def format_palette_footer_fragments() -> list[tuple[str, str]]:
    return [
        (
            "class:hint",
            " ↑↓选择  Enter执行  Esc关闭  ·  搜索框输入 / 或命令名筛选\n",
        )
    ]


def format_palette_fragments(
    *,
    items: list[PaletteItem],
    selection: int,
    query: str,
    width: int,
) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = [("class:palette-title", " 命令面板\n")]
    fragments.extend(
        format_palette_list_fragments(
            items=items,
            selection=selection,
            query=query,
            width=width,
        )
    )
    fragments.append(("", "\n"))
    fragments.extend(
        format_palette_detail_fragments(
            items=items,
            selection=selection,
            query=query,
            width=width,
        )
    )
    fragments.extend(format_palette_footer_fragments())
    return fragments


def resolve_palette_action(item: PaletteItem) -> tuple[str, str]:
    action = str(item.action or "")
    if action.startswith("slash:"):
        return "slash", action.split(":", 1)[1]
    if action.startswith("action:"):
        return "action", action.split(":", 1)[1]
    return "hint", action.split(":", 1)[-1]