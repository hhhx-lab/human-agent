from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TerminalUIState:
    screen: str = "session"
    overlay: str = "none"
    scrollback_focused: bool = False
    selected_block_index: int | None = None
    welcome_selection: int = 0
    palette_selection: int = 0
    palette_query: str = ""
    animation_tick: int = 0
    welcome_animation_tick: int = 0
    viewer_block_id: str | None = None

    def open_palette(self) -> None:
        self.overlay = "palette"
        self.palette_selection = 0
        self.palette_query = ""

    def close_overlay(self) -> None:
        self.overlay = "none"
        self.viewer_block_id = None

    def open_viewer(self, block_id: str) -> None:
        self.overlay = "viewer"
        self.viewer_block_id = block_id

    def enter_session(self) -> None:
        self.screen = "session"
        self.scrollback_focused = False

    def enter_welcome(self) -> None:
        self.screen = "welcome"
        self.close_overlay()