from __future__ import annotations

import json
import os
import re
import shutil
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .terminal_input import iter_slash_command_entries
from .terminal_markdown import format_markdown_body_fragments
from .terminal_session_transcript import (
    load_current_terminal_session_lines,
    render_resume_transcript,
)

REFERENCE_PREVIEW_PATTERN = re.compile(r"@([^\s]+)")

ITR09_FLAGS: tuple[tuple[str, str], ...] = (
    ("DIGITAL_LIFE_BODY_INTEGRATE", "A"),
    ("DIGITAL_LIFE_PREDICTION_REFRESH", "B"),
    ("DIGITAL_LIFE_MEMORY_SALIENCE_TICK", "C"),
    ("DIGITAL_LIFE_WORKSPACE_TOPK", "D"),
    ("DIGITAL_LIFE_EXPRESSION_SLOTS", "E"),
    ("DIGITAL_LIFE_INTEGRATOR_PARAMETER_PATCH", "F"),
    ("DIGITAL_LIFE_VISUAL_ENCODER", "V"),
)

IMAGE_SUFFIXES = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic", ".tif", ".tiff"}
)

SIDEBAR_PANE_WIDTH = 28
CODE_FENCE_PATTERN = re.compile(r"```(\w*)?\n?")


@dataclass
class TerminalLayoutState:
    sidebar_visible: bool = False
    terminal_width: int = 88
    terminal_height: int = 28
    theme_id: str = "groknight"
    markdown_enabled: bool = True


@dataclass(frozen=True)
class MessageRenderSpec:
    speaker: str
    text: str
    life_name: str = "Digital Life"
    timestamp: str | None = None
    release_badge: str | None = None
    event_kind: str = "message"


@dataclass(frozen=True)
class SidebarSnapshot:
    body_integrator: dict[str, Any] = field(default_factory=dict)
    expression_plan: dict[str, Any] = field(default_factory=dict)
    workspace_frame: dict[str, Any] = field(default_factory=dict)
    model_expression: dict[str, Any] = field(default_factory=dict)
    itr_flags: str = ""


def resolve_terminal_layout_state(
    *,
    theme_id: str | None = None,
) -> TerminalLayoutState:
    import os

    size = shutil.get_terminal_size((88, 28))
    resolved_theme = str(
        theme_id or os.environ.get("DIGITAL_LIFE_TUI_THEME") or "groknight"
    ).strip().lower()
    return TerminalLayoutState(
        terminal_width=max(56, int(size.columns)),
        terminal_height=max(20, int(size.lines)),
        theme_id=resolved_theme or "groknight",
    )


def resolve_sidebar_pane_width(layout_state: TerminalLayoutState) -> int:
    if layout_state.terminal_width >= 120:
        return 32
    if layout_state.terminal_width >= 96:
        return SIDEBAR_PANE_WIDTH
    return max(22, SIDEBAR_PANE_WIDTH - 6)


def build_itr09_flag_summary(environ: dict[str, str] | None = None) -> str:
    env = dict(os.environ if environ is None else environ)
    parts: list[str] = []
    for key, label in ITR09_FLAGS:
        if _parse_bool(env.get(key), False):
            parts.append(f"{label}✓")
        else:
            parts.append(f"{label}·")
    return "ITR " + "".join(parts)


def load_resident_status(*, terminal_dir: Path) -> str:
    lifecycle = _read_json(terminal_dir / "resident_lifecycle_state.json")
    status = str(lifecycle.get("status") or lifecycle.get("lifecycle_status") or "").strip()
    if status:
        return status
    loop = _read_json(terminal_dir / "terminal_life_loop_state.json")
    return str(loop.get("status") or "active").strip() or "active"


def load_sidebar_snapshot(*, terminal_dir: Path) -> SidebarSnapshot:
    state_root = terminal_dir.parent
    body = _read_json(state_root / "body" / "body_integrator_state.json")
    expression = _read_json(state_root / "language" / "expression_plan.json")
    workspace = _read_json(state_root / "consciousness" / "workspace_frame.json")
    model_expression = _read_json(state_root / "language" / "model_expression_state.json")
    return SidebarSnapshot(
        body_integrator=body,
        expression_plan=expression,
        workspace_frame=workspace,
        model_expression=model_expression,
        itr_flags=build_itr09_flag_summary(),
    )


def resolve_release_badge(*, terminal_dir: Path, speaker: str, text: str) -> str | None:
    normalized = str(speaker or "").strip().lower()
    if normalized not in {"life", "proactive"}:
        return None
    state_root = terminal_dir.parent
    model_state = _read_json(state_root / "language" / "model_expression_state.json")
    gate = model_state.get("post_expression_gate") or {}
    gate_status = str(
        gate.get("gate_status")
        or gate.get("status")
        or model_state.get("post_expression_gate_status")
        or ""
    ).strip()
    model_status = str(model_state.get("model_expression_status") or "").strip()
    if gate_status == "accepted" and model_status == "model_expression_applied":
        return "released"
    if gate_status in {"blocked", "rejected"} or model_status == "completed_unreleased":
        return "unreleased"
    if str(text or "").strip().startswith("{"):
        return "unreleased"
    return None


def format_top_bar_fragments(
    *,
    life_name: str,
    resident_status: str,
    itr_flags: str,
    width: int,
    mode_label: str = "chat",
    theme_label: str = "groknight",
) -> list[tuple[str, str]]:
    status_dot = "●" if resident_status in {
        "background_active",
        "background_starting",
        "active",
    } else "○"
    left = f" {life_name}  ·  {resident_status}  ·  {mode_label}  ·  {theme_label} "
    right = f" {itr_flags} "
    inner = max(20, width)
    if len(left) + len(right) > inner:
        right = ""
    pad = max(0, inner - len(left) - len(right))
    dot_style = "class:status-dot" if status_dot == "●" else "class:hint"
    return [
        (dot_style, f" {status_dot}"),
        ("class:top-bar", left),
        ("class:hint", right),
        ("class:top-bar", " " * pad + "\n"),
        ("class:top-bar-divider", " " + "─" * max(10, inner - 1) + "\n"),
    ]


def format_sidebar_pane_fragments(
    *,
    snapshot: SidebarSnapshot,
    width: int = SIDEBAR_PANE_WIDTH,
    collapsed: bool,
) -> list[tuple[str, str]]:
    if collapsed:
        return [
            ("class:sidebar-title", " live\n"),
            ("class:hint", "侧栏关闭\n"),
            ("class:hint", "Ctrl-B 展开\n"),
        ]
    continuous = snapshot.body_integrator.get("continuous") or {}
    bandwidth = continuous.get("cognitive_bandwidth")
    allostatic = continuous.get("allostatic_load")
    sleep = continuous.get("sleep_pressure")
    topk = snapshot.expression_plan.get("workspace_topk_k") or (
        (snapshot.workspace_frame.get("workspace_topk") or {}).get("k")
    )
    focus = snapshot.expression_plan.get("workspace_primary_focus") or snapshot.workspace_frame.get(
        "primary_focus"
    )
    drive = snapshot.expression_plan.get("proactive_drive_scalar")
    lines: list[tuple[str, str]] = [("class:sidebar-title", " live\n")]
    for label, value in (
        ("band", _fmt_scalar(bandwidth)),
        ("load", _fmt_scalar(allostatic)),
        ("sleep", _fmt_scalar(sleep)),
        ("topk", str(topk) if topk is not None else "·"),
        ("focus", _truncate(str(focus or "·"), max(8, width - 8))),
        ("drive", _fmt_scalar(drive)),
    ):
        lines.append(("class:sidebar", f"{label}\n"))
        lines.append(("class:sidebar", f" {value}\n"))
    lines.append(("class:hint", f"{snapshot.itr_flags}\n"))
    return lines


def format_footer_fragments(
    *,
    life_name: str,
    buffer=None,
    completion_hint: str = "",
) -> list[tuple[str, str]]:
    cursor_index = 0
    text_length = 0
    if buffer is not None:
        cursor_index = int(getattr(buffer, "cursor_position", 0) or 0)
        text_length = len(str(getattr(buffer, "text", "") or ""))
    return [
        ("class:status", f" {life_name} "),
        ("class:input-box", " ┃ "),
        ("class:cursor-index", f"pos {cursor_index}/{text_length}"),
        (
            "class:hint",
            "  Enter发送  双指滑对话区  ⌃↑↓滚  ⌃G最新  Ctrl+P命令  Ctrl+O浏览  Ctrl-B侧栏  Ctrl-Q离开",
        ),
        ("class:hint", completion_hint),
    ]


def format_auxiliary_fragments(
    *,
    active_text: str,
    slash_commands: Iterable[tuple[str, str]] | None,
    repo_root: Path | None,
    width: int,
    slash_panel_limit: int = 6,
) -> list[tuple[str, str]]:
    from .terminal_input import build_slash_completion_items

    fragments: list[tuple[str, str]] = []
    if active_text.lstrip().startswith("/") and slash_commands is not None:
        query = active_text.lstrip()[1:]
        if not query:
            fragments.extend(
                format_slash_panel_fragments(
                    slash_commands,
                    width=width,
                    limit=slash_panel_limit,
                )
            )
        else:
            matches = build_slash_completion_items(
                active_text,
                slash_commands=tuple(slash_commands),
            )
            fragments.append(("class:slash-panel-title", "命令匹配\n"))
            if not matches:
                fragments.append(("class:slash-panel-item", "  (无匹配)\n"))
            else:
                for item in matches[:18]:
                    line = f"  {item.label} {item.detail}".strip()
                    fragments.append(
                        (
                            "class:slash-panel-item",
                            _truncate(line, max(8, width - 2)) + "\n",
                        )
                    )
                remaining = max(0, len(matches) - 18)
                if remaining:
                    fragments.append(
                        ("class:slash-panel-group", f"  … +{remaining}\n")
                    )
    if "@" in active_text and repo_root is not None:
        file_preview = format_file_reference_preview_fragments(
            active_text,
            repo_root=repo_root,
        )
        if file_preview:
            if fragments:
                fragments.append(("", "\n"))
            fragments.extend(file_preview)
    return fragments


def build_startup_conversation_fragments(
    *,
    terminal_dir: Path,
    life_name: str,
    width: int,
) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = []
    fragments.extend(
        render_resume_startup_fragments(
            terminal_dir=terminal_dir,
            life_name=life_name,
            width=width,
        )
    )
    fragments.append(("", "\n"))
    fragments.extend(
        render_session_history_fragments(
            terminal_dir=terminal_dir,
            life_name=life_name,
            width=width,
        )
    )
    return fragments


def format_sidebar_fragments(
    *,
    snapshot: SidebarSnapshot,
    width: int,
    collapsed: bool,
) -> list[tuple[str, str]]:
    if collapsed:
        return [
            ("class:hint", "侧栏关闭"),
            ("class:hint", " · Ctrl-B 展开"),
        ]
    continuous = snapshot.body_integrator.get("continuous") or {}
    bandwidth = continuous.get("cognitive_bandwidth")
    allostatic = continuous.get("allostatic_load")
    sleep = continuous.get("sleep_pressure")
    topk = snapshot.expression_plan.get("workspace_topk_k") or (
        (snapshot.workspace_frame.get("workspace_topk") or {}).get("k")
    )
    focus = snapshot.expression_plan.get("workspace_primary_focus") or snapshot.workspace_frame.get(
        "primary_focus"
    )
    drive = snapshot.expression_plan.get("proactive_drive_scalar")
    lines = [
        ("class:sidebar-title", " live "),
        ("class:sidebar", f"band { _fmt_scalar(bandwidth)}"),
        ("class:sidebar", f" load {_fmt_scalar(allostatic)}"),
        ("class:sidebar", f" sleep {_fmt_scalar(sleep)}"),
    ]
    if topk is not None:
        lines.append(("class:sidebar", f" topk {topk}"))
    if focus:
        lines.append(("class:sidebar", f" focus {str(focus)[:12]}"))
    if drive is not None:
        lines.append(("class:sidebar", f" drive {_fmt_scalar(drive)}"))
    if width >= 100:
        lines.append(("class:hint", f" {snapshot.itr_flags}"))
    return lines


def format_message_body_fragments(
    text: str,
    *,
    markdown: bool = True,
) -> list[tuple[str, str]]:
    if markdown:
        return format_markdown_body_fragments(text)
    normalized = str(text or "")
    if "```" not in normalized:
        body: list[tuple[str, str]] = []
        for line in normalized.splitlines() or [""]:
            body.append(("class:message-body", f"  {line}\n" if line else "\n"))
        return body

    body: list[tuple[str, str]] = []
    cursor = 0
    for match in CODE_FENCE_PATTERN.finditer(normalized):
        body.extend(_format_plain_body_lines(normalized[cursor : match.start()]))
        cursor = match.end()
        end = normalized.find("```", cursor)
        if end == -1:
            code = normalized[cursor:]
            cursor = len(normalized)
        else:
            code = normalized[cursor:end]
            cursor = end + 3
        body.extend(_format_code_body_lines(code))
    body.extend(_format_plain_body_lines(normalized[cursor:]))
    return body


def format_message_fragments(
    spec: MessageRenderSpec,
    *,
    width: int = 88,
    block_mode: bool = True,
) -> list[tuple[str, str]]:
    if block_mode:
        from .terminal_blocks import format_message_block_fragments

        return format_message_block_fragments(
            MessageRenderSpec(
                speaker=spec.speaker,
                text=spec.text,
                life_name=spec.life_name,
                timestamp=spec.timestamp or _now_hms(),
                release_badge=spec.release_badge,
                event_kind=spec.event_kind,
            ),
            width=width,
        )
    speaker = _display_speaker(spec.speaker, spec.life_name)
    timestamp = spec.timestamp or _now_hms()
    badge = spec.release_badge
    badge_text = ""
    badge_style = "class:badge"
    if badge == "released":
        badge_text = " released "
        badge_style = "class:badge-released"
    elif badge == "unreleased":
        badge_text = " unreleased "
        badge_style = "class:badge-unreleased"
    header = [
        ("class:timestamp", f"[{timestamp}] "),
        ("class:speaker", speaker),
    ]
    if badge_text:
        header.append((badge_style, badge_text))
    header.append(("", "\n"))
    return header + format_message_body_fragments(spec.text)


def format_message_plain(spec: MessageRenderSpec) -> str:
    return "".join(
        fragment for _, fragment in format_message_fragments(spec, block_mode=False)
    )


def sanitize_terminal_message_text(text: str) -> str:
    normalized = str(text or "")
    if not normalized.strip():
        return ""
    cleaned: list[str] = []
    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        while line.startswith(("▌", "│", "◆", "›")):
            line = line[1:].strip()
        if line in {"▾", "▸"}:
            continue
        if line.startswith("› expand"):
            continue
        if " · " in line and line.endswith("▾"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def build_slash_panel_lines(
    slash_commands: Iterable[tuple[object, ...]],
    *,
    width: int = 88,
    limit: int = 8,
) -> list[str]:
    groups: dict[str, list[str]] = {}
    for command, detail in iter_slash_command_entries(slash_commands):
        group, _, rest = str(detail).partition("｜")
        label = rest or detail or command
        groups.setdefault(group or "命令", []).append(f"{command} {label}".strip())
    lines = ["slash panel"]
    for group_name in ("常用", "状态", "生命机制", "梦境网页", "控制"):
        entries = groups.get(group_name)
        if not entries:
            continue
        lines.append(f"[{group_name}]")
        for entry in entries[:limit]:
            lines.append("  " + _truncate(entry, max(8, width - 6)))
        if len(entries) > limit:
            lines.append(f"  … +{len(entries) - limit}")
    if len(lines) == 1:
        for group_name, entries in sorted(groups.items()):
            lines.append(f"[{group_name}]")
            for entry in entries[:limit]:
                lines.append("  " + _truncate(entry, max(8, width - 6)))
    return lines


def format_slash_panel_fragments(
    slash_commands: Iterable[tuple[str, str]],
    *,
    width: int = 88,
    limit: int = 8,
) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = [("class:slash-panel-title", "命令面板\n")]
    for line in build_slash_panel_lines(slash_commands, width=width, limit=limit):
        if line == "slash panel":
            continue
        if line.startswith("["):
            fragments.append(("class:slash-panel-group", line + "\n"))
        else:
            fragments.append(("class:slash-panel-item", line + "\n"))
    return fragments


def build_file_reference_preview(
    text: str,
    *,
    repo_root: Path,
    max_chars: int = 48,
) -> str | None:
    refs = list(_iter_reference_paths(text))
    if not refs:
        return None
    previews: list[str] = []
    for raw_ref in refs[:2]:
        preview = _preview_reference(raw_ref, repo_root=repo_root, max_chars=max_chars)
        if preview:
            previews.append(preview)
    if not previews:
        return None
    return "引用预览: " + " | ".join(previews)


def format_file_reference_preview_fragments(
    text: str,
    *,
    repo_root: Path,
) -> list[tuple[str, str]]:
    preview = build_file_reference_preview(text, repo_root=repo_root)
    if not preview:
        return []
    return [("class:file-preview", preview)]


def render_resume_startup_fragments(
    *,
    terminal_dir: Path,
    life_name: str,
    width: int,
) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = [
        ("class:resume-title", "会话恢复\n"),
    ]
    carry = _load_resume_carry_summary(terminal_dir=terminal_dir)
    if carry:
        for line in textwrap.wrap(carry, width=max(20, width - 4)):
            fragments.append(("class:resume-carry", f"  {line}\n"))
    resume = render_resume_transcript(
        terminal_dir=terminal_dir,
        session_count=2,
        event_limit=12,
    )
    for line in resume.splitlines()[:18]:
        if not line.strip():
            fragments.append(("", "\n"))
            continue
        if line.startswith("最近会话") or line.startswith("最近内容"):
            fragments.append(("class:resume-section", line + "\n"))
        else:
            fragments.append(("class:resume-line", _truncate(line, width) + "\n"))
    return fragments


def render_session_history_fragments(
    *,
    terminal_dir: Path,
    life_name: str,
    width: int,
    limit: int = 400,
) -> list[tuple[str, str]]:
    lines = load_current_terminal_session_lines(
        terminal_dir=terminal_dir,
        limit=max(limit, shutil.get_terminal_size((100, 28)).lines * 4),
    )
    if not lines:
        return format_message_fragments(
            MessageRenderSpec(
                speaker="system",
                text="/ 打开状态命令，/resume 查看历史，@ 引用项目文件。",
                life_name=life_name,
            )
        )
    fragments: list[tuple[str, str]] = []
    for line in lines:
        speaker, text = split_history_line(line, life_name)
        fragments.extend(
            format_message_fragments(
                MessageRenderSpec(
                    speaker=speaker,
                    text=text,
                    life_name=life_name,
                    timestamp="··",
                )
            )
        )
        fragments.append(("", "\n"))
    return fragments


def format_layout_toolbar_fragments(
    *,
    life_name: str,
    terminal_dir: Path,
    layout_state: TerminalLayoutState,
    buffer=None,
    slash_commands: Iterable[tuple[str, str]] | None = None,
    repo_root: Path | None = None,
) -> list[tuple[str, str]]:
    snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
    resident_status = load_resident_status(terminal_dir=terminal_dir)
    top = format_top_bar_fragments(
        life_name=life_name,
        resident_status=resident_status,
        itr_flags=snapshot.itr_flags,
        width=layout_state.terminal_width,
    )
    sidebar = format_sidebar_fragments(
        snapshot=snapshot,
        width=layout_state.terminal_width,
        collapsed=not layout_state.sidebar_visible,
    )
    cursor_index = 0
    text_length = 0
    active_text = ""
    completion_hint = ""
    slash_hint: list[tuple[str, str]] = []
    file_preview: list[tuple[str, str]] = []
    if buffer is not None:
        cursor_index = int(getattr(buffer, "cursor_position", 0) or 0)
        text_length = len(str(getattr(buffer, "text", "") or ""))
        active_text = str(getattr(buffer, "text", "") or "")
        if getattr(buffer, "complete_state", None):
            completion_hint = "  ↑↓ 选择  Enter 确认"
            overflow_hint = _completion_overflow_hint(
                complete_state=getattr(buffer, "complete_state", None),
            )
            if overflow_hint:
                completion_hint = f"{completion_hint}  {overflow_hint}"
        if active_text.lstrip().startswith("/") and slash_commands is not None:
            query = active_text.lstrip()[1:]
            if not query:
                slash_hint = format_slash_panel_fragments(
                    slash_commands,
                    width=layout_state.terminal_width,
                )[:12]
        if "@" in active_text and repo_root is not None:
            file_preview = format_file_reference_preview_fragments(
                active_text,
                repo_root=repo_root,
            )

    footer = [
        ("class:status", f" {life_name} "),
        ("class:input-box", " ┃ "),
        ("class:cursor-index", f"pos {cursor_index}/{text_length}"),
        (
            "class:hint",
            "  Enter发送  双指滑对话区  ⌃↑↓滚  ⌃G最新  Ctrl+P命令  Ctrl+O浏览  Ctrl-B侧栏  Ctrl-Q离开",
        ),
        ("class:hint", completion_hint),
    ]
    if layout_state.sidebar_visible and layout_state.terminal_width >= 96:
        footer.extend([("class:input-box", " ┃ ")])
        footer.extend(sidebar)
    fragments = top + [("", "\n")]
    if slash_hint:
        fragments.extend(slash_hint)
    if file_preview:
        fragments.extend(file_preview)
        fragments.append(("", "\n"))
    fragments.extend(footer)
    return fragments


def _load_resume_carry_summary(*, terminal_dir: Path) -> str:
    state_root = terminal_dir.parent
    relationship = _read_json(state_root / "relationship" / "relationship_timeline.json")
    memory = _read_json(state_root / "memory" / "memory_retrieval_frame.json")
    parts: list[str] = []
    stage = relationship.get("relationship_stage") or relationship.get("stage")
    if stage:
        parts.append(f"关系阶段 {stage}")
    focus = memory.get("reconstruction_focus") or memory.get("semantic_focus")
    if focus:
        parts.append(f"召回焦点 {focus}")
    return " · ".join(str(part) for part in parts if part)


def split_history_line(line: str, life_name: str) -> tuple[str, str]:
    normalized = str(line or "")
    if normalized.startswith("你: "):
        return "relation", normalized[3:]
    prefix = f"{life_name}: "
    if normalized.startswith(prefix):
        return "life", normalized[len(prefix) :]
    if normalized.startswith("command result: "):
        return "command_result", normalized[len("command result: ") :]
    if normalized.startswith("command: "):
        return "command", normalized[len("command: ") :]
    if normalized.startswith("session "):
        return "system", normalized
    return "system", normalized


def _format_plain_body_lines(text: str) -> list[tuple[str, str]]:
    lines: list[tuple[str, str]] = []
    for line in str(text or "").splitlines() or [""]:
        lines.append(("class:message-body", f"  {line}\n" if line else "\n"))
    return lines


def _format_code_body_lines(text: str) -> list[tuple[str, str]]:
    lines: list[tuple[str, str]] = []
    for line in str(text or "").splitlines() or [""]:
        lines.append(("class:code-block", f"  {line}\n" if line else "\n"))
    return lines


def _display_speaker(speaker: str, life_name: str) -> str:
    normalized = str(speaker or "").strip().lower()
    if normalized == "relation":
        return "你"
    if normalized in {"life", "proactive"}:
        return life_name
    if normalized == "command":
        return "command"
    if normalized == "command_result":
        return "result"
    if normalized == "system":
        return "·"
    return speaker or "·"


def _preview_reference(raw_ref: str, *, repo_root: Path, max_chars: int) -> str:
    clean = raw_ref.replace("\\", "/").lstrip("/")
    path = (repo_root / clean).resolve()
    try:
        path.relative_to(repo_root.resolve())
    except ValueError:
        return f"@{clean} (blocked)"
    if not path.exists():
        return f"@{clean} (missing)"
    if path.is_dir():
        count = sum(1 for _ in path.iterdir())
        return f"@{clean}/ ({count} entries)"
    suffix = path.suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        size = path.stat().st_size
        return f"@{clean} (image {size}B)"
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return f"@{clean} (unreadable)"
    snippet = " ".join(content.split())
    if not snippet:
        return f"@{clean} (empty)"
    return f"@{clean} ({_truncate(snippet, max_chars)})"


def _iter_reference_paths(text: str) -> Iterable[str]:
    for match in REFERENCE_PREVIEW_PATTERN.finditer(str(text or "")):
        raw_ref = match.group(1).strip().rstrip(".,;，。；")
        if raw_ref:
            yield raw_ref


def _completion_overflow_hint(*, complete_state) -> str:
    completions = getattr(complete_state, "completions", None) or []
    total = len(completions)
    visible_rows = 14
    remaining = max(0, total - visible_rows)
    if remaining <= 0:
        return ""
    return f"还有 {remaining} 个，继续输入筛选"


def _fmt_scalar(value: Any) -> str:
    if value is None:
        return "·"
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)[:6]


def _truncate(text: str, width: int) -> str:
    normalized = str(text or "")
    if len(normalized) <= width:
        return normalized
    return normalized[: max(0, width - 1)] + "…"


def _now_hms() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M")


def _parse_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}