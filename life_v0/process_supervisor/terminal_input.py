from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO


TERMINAL_INPUT_PROFILE_REF = "runtime/state/terminal/terminal_input_profile.json"


@dataclass(frozen=True)
class TerminalCompletionItem:
    label: str
    detail: str = ""
    kind: str = "command"


@dataclass(frozen=True)
class TerminalCompletionState:
    trigger: str
    query: str
    start_index: int
    end_index: int
    items: tuple[TerminalCompletionItem, ...]


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
            "input_box": "bottom_composer_with_prompt_prefix_and_cursor_index",
            "mouse_support": True,
            "enable_history_search": True,
            "show_frame": True,
            "complete_style": "MULTI_COLUMN",
            "reserve_space_for_menu": 8,
            "cursor_shape": "BLINKING_BEAM",
            "placeholder": "输入一句话，或 / 查看状态命令，@ 引用文件",
            "internal_life_signal_visibility": "hidden_until_slash_command",
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


def build_slash_completion_items(
    text: str,
    *,
    slash_commands: list[tuple[str, str]] | tuple[tuple[str, str], ...],
    limit: int = 10,
) -> tuple[TerminalCompletionItem, ...]:
    token = str(text or "").strip()
    if not token.startswith("/"):
        return tuple()
    query = token[1:].lower()
    items: list[TerminalCompletionItem] = []
    for label, detail in slash_commands:
        normalized_label = str(label or "").strip()
        if not normalized_label.startswith("/"):
            continue
        search = normalized_label[1:].lower()
        if query and not search.startswith(query):
            continue
        items.append(
            TerminalCompletionItem(
                label=normalized_label,
                detail=str(detail or "").strip(),
                kind="command",
            )
        )
        if len(items) >= limit:
            break
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
        return TerminalCompletionState(
            trigger="@",
            query=token[1:],
            start_index=token_start,
            end_index=cursor,
            items=items,
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
        return TerminalCompletionState(
            trigger="/",
            query=token[1:],
            start_index=token_start,
            end_index=cursor,
            items=items,
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
    lines = [f"  {header}"]
    for item in state.items:
        detail = item.detail
        if detail:
            line = f"  {item.label.ljust(label_width)} {detail}"
        else:
            line = f"  {item.label}"
        lines.append(line[:width])
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
