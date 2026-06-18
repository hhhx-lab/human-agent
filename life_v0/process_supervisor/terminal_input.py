from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, TextIO


TERMINAL_INPUT_PROFILE_REF = "runtime/state/terminal/terminal_input_profile.json"


@dataclass(frozen=True)
class TerminalCompletionItem:
    label: str
    detail: str = ""
    kind: str = "command"
    group: str = ""
    show_on_empty_query: bool = True


@dataclass(frozen=True)
class TerminalCompletionState:
    trigger: str
    query: str
    start_index: int
    end_index: int
    items: tuple[TerminalCompletionItem, ...]
    visible_limit: int = 10
    remaining_count: int = 0
    total_count: int = 0
    hint: str = ""


def build_terminal_input_profile(
    *,
    input_stream: TextIO,
    idle_voice_interval_seconds: float,
    mode_override: str | None = None,
) -> dict[str, Any]:
    is_tty = bool(getattr(input_stream, "isatty", lambda: False)())
    return {
        "schema_version": "terminal_input_profile_v0",
        "terminal_input_profile_ref": TERMINAL_INPUT_PROFILE_REF,
        "input_mode": mode_override or "prompt_toolkit_mature_terminal",
        "is_tty": is_tty,
        "terminal_framework": "prompt_toolkit",
        "self_built_input_reader": "removed",
        "prompt_toolkit_experience": {
            "layout_profile": "product_split_pane_v4_grok_visual",
            "input_box": "split_pane_bottom_composer",
            "mouse_support": True,
            "scrollback_policy": "in_app_conversation_pane",
            "session_replay_line_limit": 400,
            "enable_history_search": True,
            "show_frame": True,
            "complete_style": "COLUMN",
            "reserve_space_for_menu": 14,
            "cursor_shape": "BLINKING_BEAM",
            "placeholder": "输入对话，/ 命令面板，@ 引用文件，Ctrl-B 侧栏",
            "sidebar_toggle": "ctrl_b",
            "slash_panel": "inline_on_empty_slash_query",
            "file_reference_preview": "inline_on_at_reference",
            "message_blocks": "timestamp_speaker_badge_body",
            "session_resume": "startup_carry_and_transcript",
            "internal_life_signal_visibility": "sidebar_opt_in_ctrl_b",
        },
        "line_editing": {
            "backspace": "prompt_toolkit_native_delete_previous_character",
            "delete": "prompt_toolkit_native_delete_character_under_cursor",
            "left_right_arrows": "prompt_toolkit_native_cursor_navigation",
            "up_down_arrows": "completion_selection_when_menu_open_else_history",
            "home_end": "prompt_toolkit_native_line_boundaries",
            "ctrl_u": "prompt_toolkit_native_clear_before_cursor",
            "ctrl_w": "prompt_toolkit_native_delete_previous_word",
            "ctrl_k": "prompt_toolkit_native_clear_after_cursor",
            "ctrl_a_ctrl_e": "prompt_toolkit_native_line_boundaries",
            "ctrl_l": "prompt_toolkit_native_clear_screen",
            "ctrl_d": "prompt_toolkit_native_eof",
            "ctrl_c": "prompt_toolkit_native_interrupt",
            "redraw_strategy": "prompt_toolkit_layout_renderer",
        },
        "idle_voice_policy": {
            "enabled": idle_voice_interval_seconds > 0,
            "interval_seconds": idle_voice_interval_seconds,
            "release_only_when_prompt_submits_empty_line": True,
            "do_not_interrupt_active_completion_menu": True,
        },
        "slash_command_completion": {
            "enabled": True,
            "trigger": "/",
            "surface": "prompt_toolkit_completion_menu",
            "selection": "up_down_arrows",
            "confirm": "enter",
            "empty_query_surface": "grouped_core_command_panel",
            "candidate_policy": "full_match_list_with_visible_hint",
            "groups": ["常用", "状态", "生命机制", "控制", "梦境网页"],
            "relation_inbox_policy": "completion_preview_only_until_submitted",
        },
        "file_reference_completion": {
            "enabled": True,
            "trigger": "@",
            "surface": "prompt_toolkit_completion_menu",
            "selection": "up_down_arrows",
            "confirm": "enter",
            "excluded_roots": [
                ".git",
                ".venv",
                ".pytest_cache",
                "__pycache__",
                "runtime",
                "node_modules",
            ],
            "relation_inbox_policy": "reference_text_only_when_submitted",
        },
        "default_state_visibility": "hidden_until_slash_command",
        "relation_turn_boundary": {
            "slash_commands_bypass_relation_inbox": True,
            "input_profile_is_terminal_periphery": True,
        },
    }


def iter_slash_command_entries(
    slash_commands: Iterable[tuple[Any, ...]],
) -> Iterable[tuple[str, str]]:
    for command in slash_commands:
        if len(command) < 2:
            continue
        yield str(command[0]), str(command[1])


def build_slash_completion_items(
    text: str,
    *,
    slash_commands: list[tuple[Any, ...]] | tuple[tuple[Any, ...], ...],
    limit: int = 10,
) -> tuple[TerminalCompletionItem, ...]:
    del limit
    token = str(text or "").strip()
    if not token.startswith("/"):
        return tuple()
    query = token[1:].lower()
    items: list[TerminalCompletionItem] = []
    for command in slash_commands:
        if len(command) < 2:
            continue
        label, detail = command[0], command[1]
        metadata = command[2] if len(command) >= 3 and isinstance(command[2], dict) else {}
        show_on_empty_query = bool(metadata.get("show_on_empty_query", True))
        normalized_label = str(label or "").strip()
        if not normalized_label.startswith("/"):
            continue
        search = normalized_label[1:].lower()
        if not query and not show_on_empty_query:
            continue
        if query and not search.startswith(query):
            continue
        group, clean_detail = _split_completion_group_and_detail(str(detail or ""))
        items.append(
            TerminalCompletionItem(
                label=normalized_label,
                detail=clean_detail,
                kind="command",
                group=group,
                show_on_empty_query=show_on_empty_query,
            )
        )
    return tuple(items)


def build_file_reference_completion_items(
    text: str,
    *,
    repo_root: Path,
    limit: int = 10,
) -> tuple[TerminalCompletionItem, ...]:
    token = str(text or "").strip()
    if not token.startswith("@"):
        return tuple()
    query = token[1:].replace("\\", "/").lstrip("/")
    root = Path(repo_root)
    if not root.exists():
        return tuple()

    excluded_dirs = {
        ".git",
        ".venv",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "__pycache__",
        "node_modules",
        "runtime",
        ".codex",
    }
    candidates: list[tuple[int, str, TerminalCompletionItem]] = []
    query_lower = query.lower()
    max_candidates = max(limit * 4, 24)

    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in excluded_dirs and not dirname.startswith(".DS_")
        ]
        rel_parent = _relative_posix(current_path, root)
        depth = 0 if not rel_parent else rel_parent.count("/") + 1
        if depth > 6:
            dirnames[:] = []
            continue

        for dirname in dirnames:
            rel = _join_posix(rel_parent, dirname) + "/"
            score = _file_completion_score(rel, query_lower)
            if score is not None:
                candidates.append(
                    (
                        score,
                        rel,
                        TerminalCompletionItem(
                            label=rel,
                            detail="folder",
                            kind="folder",
                        ),
                    )
                )
        for filename in filenames:
            if _is_ignored_reference_file(filename):
                continue
            rel = _join_posix(rel_parent, filename)
            score = _file_completion_score(rel, query_lower)
            if score is not None:
                candidates.append(
                    (
                        score + 1,
                        rel,
                        TerminalCompletionItem(
                            label=rel,
                            detail="file",
                            kind="file",
                        ),
                    )
                )
        if len(candidates) >= max_candidates:
            break

    candidates.sort(key=lambda item: (item[0], item[1].lower()))
    return tuple(item for _, _, item in candidates[:limit])


def build_terminal_completion_state(
    text: str,
    *,
    cursor_index: int | None = None,
    slash_commands: list[tuple[str, str]] | tuple[tuple[str, str], ...] = (),
    repo_root: Path | None = None,
    limit: int = 10,
) -> TerminalCompletionState | None:
    buffer_text = str(text or "")
    cursor = len(buffer_text) if cursor_index is None else max(0, min(cursor_index, len(buffer_text)))
    before_cursor = buffer_text[:cursor]
    token_start = _current_token_start(before_cursor)
    token = before_cursor[token_start:]

    if token.startswith("@"):
        items = build_file_reference_completion_items(
            token,
            repo_root=repo_root or Path.cwd(),
            limit=limit,
        )
        if not items:
            return None
        total_count = len(items)
        remaining_count = max(0, total_count - max(0, limit))
        return TerminalCompletionState(
            trigger="@",
            query=token[1:],
            start_index=token_start,
            end_index=cursor,
            items=items,
            visible_limit=limit,
            remaining_count=remaining_count,
            total_count=total_count,
            hint=_completion_hint(
                remaining_count=remaining_count,
                trigger="@",
            ),
        )

    stripped_before = before_cursor.lstrip()
    leading_offset = len(before_cursor) - len(stripped_before)
    if leading_offset == token_start and token.startswith("/") and " " not in token:
        items = build_slash_completion_items(
            token,
            slash_commands=slash_commands,
            limit=limit,
        )
        if not items:
            return None
        total_count = len(items)
        remaining_count = max(0, total_count - max(0, limit))
        return TerminalCompletionState(
            trigger="/",
            query=token[1:],
            start_index=token_start,
            end_index=cursor,
            items=items,
            visible_limit=limit,
            remaining_count=remaining_count,
            total_count=total_count,
            hint=_completion_hint(
                remaining_count=remaining_count,
                trigger="/",
            ),
        )

    return None


def render_terminal_completion_popup(
    state: TerminalCompletionState | None,
    *,
    max_width: int = 88,
) -> str:
    if state is None or not state.items:
        return ""
    header = "/ command" if state.trigger == "/" else "@ file"
    width = max(32, min(max_width, 100))
    label_width = min(
        max(len(item.label) for item in state.items) + 2,
        max(12, width // 2),
    )
    visible_limit = max(0, state.visible_limit)
    visible_items = state.items[:visible_limit] if visible_limit else state.items
    lines = [f"  {header}"]
    current_group = ""
    for item in visible_items:
        if state.trigger == "/" and item.group and item.group != current_group:
            current_group = item.group
            lines.append(f"  {current_group}")
        detail = item.detail
        if detail:
            line = f"  {item.label.ljust(label_width)} {detail}"
        else:
            line = f"  {item.label}"
        lines.append(line[:width])
    if state.hint:
        lines.append(f"  {state.hint}"[:width])
    return "\n".join(lines)


def write_terminal_input_profile(
    *,
    terminal_dir: Path,
    profile: dict[str, Any],
) -> dict[str, Any]:
    terminal_dir.mkdir(parents=True, exist_ok=True)
    path = terminal_dir / "terminal_input_profile.json"
    path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return profile


def _current_token_start(text: str) -> int:
    index = len(text)
    while index > 0 and not text[index - 1].isspace():
        index -= 1
    return index


def _split_completion_group_and_detail(detail: str) -> tuple[str, str]:
    value = str(detail or "").strip()
    for separator in ("｜", "|"):
        if separator in value:
            group, clean_detail = value.split(separator, 1)
            return group.strip(), clean_detail.strip()
    return "", value


def _completion_hint(*, remaining_count: int, trigger: str) -> str:
    if remaining_count <= 0:
        return ""
    if trigger == "/":
        return f"还有 {remaining_count} 个，继续输入筛选"
    return f"还有 {remaining_count} 个，继续输入筛选"


def _relative_posix(path: Path, root: Path) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return ""
    value = relative.as_posix()
    return "" if value == "." else value


def _join_posix(parent: str, child: str) -> str:
    return f"{parent}/{child}" if parent else child


def _file_completion_score(candidate: str, query_lower: str) -> int | None:
    candidate_lower = candidate.lower()
    if not query_lower:
        return 20 + candidate_lower.count("/")
    if candidate_lower.startswith(query_lower):
        return candidate_lower.count("/")
    basename = candidate_lower.rstrip("/").rsplit("/", 1)[-1]
    if basename.startswith(query_lower):
        return 10 + candidate_lower.count("/")
    if query_lower in candidate_lower:
        return 30 + candidate_lower.index(query_lower)
    return None


def _is_ignored_reference_file(filename: str) -> bool:
    if filename.startswith(".DS_") or filename.endswith((".pyc", ".pyo")):
        return True
    if filename == ".env" or filename.startswith(".env."):
        return filename == ".env" or not filename.endswith(".example")
    return False
