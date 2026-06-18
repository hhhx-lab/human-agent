from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .terminal_blocks import (
    BlockRecord,
    format_block_fragments,
    format_block_viewer_fragments,
    format_message_block_fragments,
    format_thinking_block_fragments,
    resolve_block_kind,
)
from .terminal_layout import (
    MessageRenderSpec,
    resolve_release_badge,
    sanitize_terminal_message_text,
    split_history_line,
)
from .terminal_session_transcript import load_current_terminal_session_lines
from .terminal_session_tabs import load_session_conversation_lines


@dataclass
class ConversationModel:
    blocks: list[BlockRecord] = field(default_factory=list)
    width: int = 88
    scroll_to_end: bool = True
    selected_index: int | None = None
    stream_block_id: str | None = None
    stream_text: str = ""
    use_markdown: bool = True

    @property
    def fragments(self) -> list[tuple[str, str]]:
        return self.render_fragments(animation_tick=0)

    def render_fragments(self, *, animation_tick: int = 0) -> list[tuple[str, str]]:
        rendered: list[tuple[str, str]] = []
        for index, record in enumerate(self.blocks):
            if index > 0:
                rendered.append(("", "\n"))
            rendered.extend(
                format_message_block_fragments(
                    record.spec,
                    width=self.width,
                    collapsed=record.collapsed,
                    selected=index == self.selected_index,
                    running=record.running,
                    animation_tick=animation_tick,
                )
            )
        return rendered

    def viewer_fragments(self, block_id: str, *, animation_tick: int = 0) -> list[tuple[str, str]]:
        record = self.find_block(block_id)
        if record is None:
            return [("class:hint", " 块不存在\n")]
        return format_block_viewer_fragments(
            record,
            width=self.width,
            animation_tick=animation_tick,
        )

    def find_block(self, block_id: str) -> BlockRecord | None:
        for record in self.blocks:
            if record.block_id == block_id:
                return record
        return None

    def load_startup(
        self,
        *,
        terminal_dir: Path,
        life_name: str,
        width: int,
    ) -> None:
        self.width = width
        lines = load_current_terminal_session_lines(
            terminal_dir=terminal_dir,
            limit=400,
        )
        self.blocks = []
        if not lines:
            self.blocks.append(
                BlockRecord.create(
                    MessageRenderSpec(
                        speaker="system",
                        text="/ 打开状态命令，/resume 查看历史，@ 引用项目文件。",
                        life_name=life_name,
                    )
                )
            )
        else:
            for line in lines:
                speaker, text = split_history_line(line, life_name)
                if speaker == "system" and str(text).startswith("session "):
                    continue
                cleaned = sanitize_terminal_message_text(text)
                if not cleaned:
                    continue
                self.blocks.append(
                    BlockRecord.create(
                        MessageRenderSpec(
                            speaker=speaker,
                            text=cleaned,
                            life_name=life_name,
                            timestamp="··",
                        )
                    )
                )
        self.selected_index = None
        self.scroll_to_end = True

    def load_session(
        self,
        *,
        terminal_dir: Path,
        session_id: str,
        life_name: str,
        width: int,
    ) -> None:
        self.width = width
        lines = load_session_conversation_lines(
            terminal_dir=terminal_dir,
            session_id=session_id,
        )
        self.blocks = []
        if not lines:
            self.blocks.append(
                BlockRecord.create(
                    MessageRenderSpec(
                        speaker="system",
                        text=f"会话 {session_id} 还没有内容。",
                        life_name=life_name,
                    )
                )
            )
            return
        for line in lines:
            speaker, text = split_history_line(line, life_name)
            if speaker == "system" and str(text).startswith("session "):
                continue
            cleaned = sanitize_terminal_message_text(text)
            if not cleaned:
                continue
            self.blocks.append(
                BlockRecord.create(
                    MessageRenderSpec(
                        speaker=speaker,
                        text=cleaned,
                        life_name=life_name,
                        timestamp="··",
                    )
                )
            )
        self.selected_index = None
        self.scroll_to_end = True

    def append_message(self, spec: MessageRenderSpec) -> None:
        self._clear_ephemeral()
        cleaned = sanitize_terminal_message_text(spec.text)
        self.blocks.append(
            BlockRecord.create(
                MessageRenderSpec(
                    speaker=spec.speaker,
                    text=cleaned,
                    life_name=spec.life_name,
                    timestamp=spec.timestamp,
                    release_badge=spec.release_badge,
                    event_kind=spec.event_kind,
                )
            )
        )
        self.scroll_to_end = True

    def show_typing(self, *, life_name: str) -> None:
        self._clear_ephemeral()
        record = BlockRecord.create(
            MessageRenderSpec(
                speaker="life",
                text="正在组织表达…",
                life_name=life_name,
                event_kind="thinking",
            ),
            ephemeral=True,
        )
        record.running = True
        self.blocks.append(record)
        self.stream_block_id = record.block_id
        self.stream_text = ""
        self.scroll_to_end = True

    def start_stream_message(self, spec: MessageRenderSpec) -> None:
        self._clear_ephemeral()
        record = BlockRecord.create(spec, ephemeral=True)
        record.running = True
        self.blocks.append(record)
        self.stream_block_id = record.block_id
        self.stream_text = ""
        self.scroll_to_end = True

    def append_stream_delta(self, chunk: str) -> None:
        if not chunk:
            return
        self._clear_ephemeral(keep_stream=True)
        if self.stream_block_id is None:
            self.start_stream_message(
                MessageRenderSpec(
                    speaker="life",
                    text="",
                    life_name="Digital Life",
                )
            )
        self.stream_text += chunk
        record = self.find_block(self.stream_block_id or "")
        if record is None:
            return
        record.spec = MessageRenderSpec(
            speaker=record.spec.speaker,
            text=self.stream_text,
            life_name=record.spec.life_name,
            timestamp=record.spec.timestamp,
            release_badge=record.spec.release_badge,
            event_kind=record.spec.event_kind,
        )
        record.running = True
        self.scroll_to_end = True

    def finalize_stream_message(self, spec: MessageRenderSpec) -> None:
        record = self.find_block(self.stream_block_id or "")
        if record is not None:
            record.ephemeral = False
            record.running = False
            record.spec = spec
            record.block_kind = resolve_block_kind(
                speaker=spec.speaker,
                event_kind=spec.event_kind,
                text=spec.text,
            )
            self.stream_block_id = None
            self.stream_text = ""
            self.scroll_to_end = True
            return
        self._clear_ephemeral()
        if spec.text:
            self.append_message(spec)

    def clear_typing(self) -> None:
        self._clear_ephemeral()

    def clear_stream(self) -> None:
        self._clear_ephemeral()

    def select_block(self, index: int | None) -> None:
        if index is None or not self.blocks:
            self.selected_index = None
            return
        self.selected_index = max(0, min(index, len(self.blocks) - 1))

    def move_selection(self, delta: int) -> None:
        if not self.blocks:
            self.selected_index = None
            return
        if self.selected_index is None:
            self.selected_index = 0 if delta >= 0 else len(self.blocks) - 1
            return
        self.selected_index = max(0, min(self.selected_index + delta, len(self.blocks) - 1))

    def collapse_selected(self) -> None:
        if self.selected_index is None:
            return
        self.blocks[self.selected_index].collapsed = True

    def expand_selected(self) -> None:
        if self.selected_index is None:
            return
        self.blocks[self.selected_index].collapsed = False

    def toggle_selected_fold(self) -> None:
        if self.selected_index is None:
            return
        record = self.blocks[self.selected_index]
        record.collapsed = not record.collapsed

    def selected_block_id(self) -> str | None:
        if self.selected_index is None or not self.blocks:
            return None
        return self.blocks[self.selected_index].block_id

    def _clear_ephemeral(self, *, keep_stream: bool = False) -> None:
        retained: list[BlockRecord] = []
        for record in self.blocks:
            if record.ephemeral and (not keep_stream or record.block_id != self.stream_block_id):
                continue
            retained.append(record)
        if not keep_stream:
            self.stream_block_id = None
            self.stream_text = ""
        self.blocks = retained


def build_turn_hooks(
    *,
    conversation: ConversationModel,
    life_name: str,
    schedule_ui: Callable[[Callable[[], None]], None],
    on_exit: Callable[[int | None], None],
) -> tuple[Callable[[], None], Callable[[str], None], Callable[[str], None]]:
    def on_start() -> None:
        schedule_ui(lambda: conversation.show_typing(life_name=life_name))

    def on_delta(chunk: str) -> None:
        schedule_ui(lambda: conversation.append_stream_delta(chunk))

    def on_complete(full_text: str) -> None:
        del full_text

    return on_start, on_delta, on_complete


def resolve_streaming_life_spec(
    *,
    terminal_dir: Path,
    life_name: str,
    text: str,
    speaker: str = "life",
    event_kind: str = "life_response",
) -> MessageRenderSpec:
    return MessageRenderSpec(
        speaker=speaker,
        text=text,
        life_name=life_name,
        release_badge=resolve_release_badge(
            terminal_dir=terminal_dir,
            speaker=speaker,
            text=text,
        ),
        event_kind=event_kind,
    )