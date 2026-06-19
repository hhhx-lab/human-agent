from __future__ import annotations

from dataclasses import dataclass

from prompt_toolkit.styles import Style


@dataclass(frozen=True)
class TerminalTheme:
    theme_id: str
    label: str
    style_dict: dict[str, str]
    truecolor: bool = True


_GROK_MUTED = "#6b6b6b"
_GROK_BODY = "#e1e1e1"
_GROK_BG = "#0a0a0a"
_GROK_SURFACE = "#141414"
_GROK_SURFACE_ALT = "#1a1a1a"
_GROK_BORDER = "#2a2a2a"
_GROK_ACCENT = "#bb9af7"

_SHARED_BLOCK_STYLES: dict[str, str] = {
    "block-accent-user": f"{_GROK_MUTED}",
    "block-accent-assistant": "#4a4a4a",
    "block-accent-thinking": "#5c7cfa",
    "block-accent-tool": "#c9a227",
    "block-accent-execute": "#d97757",
    "block-accent-diff": "#6b8adb",
    "block-accent-system": _GROK_MUTED,
    "block-title-user": f"{_GROK_BODY} bold",
    "block-title-assistant": f"{_GROK_BODY} bold",
    "block-title-thinking": "#8ab4f8 bold",
    "block-title-tool": "#d4b86a bold",
    "block-title-execute": "#e8a87c bold",
    "block-title-diff": "#8ab4f8 bold",
    "block-title-system": f"{_GROK_MUTED} bold",
    "block-body": _GROK_BODY,
    "block-body-thinking": "#8ab4f8 italic",
    "block-body-tool": "#d4b86a",
    "block-body-execute": "#e8a87c",
    "block-body-muted": _GROK_MUTED,
    "block-muted": f"{_GROK_MUTED} italic",
    "block-selected": f"bg:#{_GROK_SURFACE_ALT[1:]}",
    "diff-insert": "#7fd47f",
    "diff-delete": "#f07070",
    "diff-hunk": "#8ab4f8 bold",
    "palette-title": f"{_GROK_BODY} bold",
    "palette-item": "#b0b0b0",
    "palette-active": f"{_GROK_BODY} bold bg:#{_GROK_SURFACE_ALT[1:]}",
    "palette-detail": "#c8c8c8",
    "palette-search": f"{_GROK_BODY} bg:#{_GROK_SURFACE[1:]}",
    "welcome-title": f"{_GROK_BODY} bold",
    "welcome-subtitle": "#00FFFF",
    "welcome-section": "#39FF14 bold",
    "welcome-line": "#6b8f71",
    "welcome-active": "#39FF14 bold",
    "welcome-phase": "#6b6b6b italic",
    "welcome-screen": "bg:#000000",
    "welcome-void": "bg:#000000",
    "welcome-scanline": "#0a0a0a bg:#000000",
    "welcome-binary": "#39FF14",
    "welcome-binary-bright": "#7fff7f bold",
    "welcome-binary-dim": "#1a4d2e",
    "welcome-glitch-red": "#FF00FF",
    "welcome-glitch-cyan": "#00FFFF",
    "welcome-scanline-hot": "#0a0a0a bg:#00FFFF",
    "welcome-particle-cyan": "#00FFFF bold",
    "welcome-particle-magenta": "#FF00FF bold",
    "welcome-particle-white": "#FFFFFF bold",
    "welcome-pixel-cyan": "#00FFFF bold",
    "welcome-pixel-magenta": "#FF00FF bold",
    "welcome-pixel-magenta-pulse": "#FF66FF bold",
    "welcome-fusion": "#00FF9F bold",
    "welcome-heart-red": "#FF0000 bold",
    "welcome-heart-dim": "#8B0000 bold",
    "welcome-node": "#39FF14 bold",
    "welcome-circuit-green": "#00FF9F bold",
    "welcome-circuit-fade": "#1a5c3a bold",
    "welcome-link": "#0d3d28",
    "welcome-link-active": "#39FF14 bold",
    "welcome-hud": "#39FF14",
    "welcome-hud-bright": "#7fff7f bold",
    "welcome-hud-ok": "#00FF9F bold",
    "welcome-progress-fill": "#39FF14 bold",
    "welcome-progress-empty": "#1a4d2e",
    "welcome-crt-border": "#0d2a1f",
    "welcome-crt-glass": "bg:#000000",
    "welcome-crt-bezel": "#0a1a12",
    "viewer-title": f"{_GROK_BODY} bold",
    "overlay": _GROK_BG,
    "overlay-backdrop": f"bg:{_GROK_BG}",
    "overlay-panel": f"{_GROK_BODY} bg:#{_GROK_SURFACE[1:]}",
    "overlay-panel-border": f"{_GROK_BORDER} bg:#{_GROK_SURFACE[1:]}",
    "top-bar-divider": _GROK_BORDER,
}


def _base_theme(
    *,
    theme_id: str,
    label: str,
    bg: str,
    fg: str,
    accent: str,
    top_bar: str,
    tab_active: str,
    tab_idle: str,
    input_surface: str,
) -> TerminalTheme:
    return TerminalTheme(
        theme_id=theme_id,
        label=label,
        style_dict={
            **_SHARED_BLOCK_STYLES,
            "status": fg,
            "hint": _GROK_MUTED,
            "speaker": f"{fg} bold",
            "relation": fg,
            "input": fg,
            "error": "#f07070",
            "input-box": _GROK_MUTED,
            "input-composer": f"{fg} bg:{input_surface}",
            "input-separator": f"bg:{_GROK_BORDER}",
            "status-dot": "#5fd45f bold",
            "cursor-index": _GROK_MUTED,
            "top-bar": top_bar,
            "top-bar-divider": _GROK_BORDER,
            "overlay-panel": f"{fg} bg:{input_surface}",
            "palette-search": f"{fg} bg:{input_surface}",
            "palette-detail": "#c8c8c8",
            "tab-bar": tab_idle,
            "tab-active": tab_active,
            "tab-idle": tab_idle,
            "tab-active-underline": f"{fg} bold",
            "sidebar": fg,
            "sidebar-title": f"{fg} bold",
            "timestamp": _GROK_MUTED,
            "message-body": fg,
            "code-block": f"{fg} bg:#{_GROK_SURFACE_ALT[1:]}",
            "badge": _GROK_MUTED,
            "badge-released": "#7fd47f",
            "badge-unreleased": "#f07070",
            "slash-panel-title": f"{fg} bold",
            "slash-panel-group": _GROK_MUTED,
            "slash-panel-item": "#b0b0b0",
            "file-preview": "#d4b86a",
            "resume-title": f"{fg} bold",
            "resume-section": _GROK_MUTED,
            "resume-line": "#b0b0b0",
            "resume-carry": fg,
            "typing": f"{_GROK_MUTED} italic",
            "md-h1": f"{fg} bold",
            "md-h2": f"{fg} bold",
            "md-h3": "#8ab4f8 bold",
            "md-list": "#b0b0b0",
            "md-link": "#8ab4f8 underline",
            "md-code-inline": "#d4b86a",
            "md-code-lang": _GROK_MUTED,
            "md-keyword": f"{_GROK_ACCENT} bg:#{_GROK_SURFACE_ALT[1:]}",
            "md-string": f"#7fd47f bg:#{_GROK_SURFACE_ALT[1:]}",
            "md-comment": f"{_GROK_MUTED} bg:#{_GROK_SURFACE_ALT[1:]}",
            "scrollbar.background": f"bg:#{_GROK_SURFACE[1:]}",
            "scrollbar.button": f"bg:{_GROK_MUTED}",
            "scrollbar.arrow": _GROK_MUTED,
            "bg": bg,
        },
    )


THEME_GROKNIGHT = _base_theme(
    theme_id="groknight",
    label="GrokNight",
    bg=_GROK_BG,
    fg=_GROK_BODY,
    accent=_GROK_ACCENT,
    top_bar=f"#8a8a8a bg:{_GROK_BG}",
    tab_active=f"{_GROK_BODY} bold bg:{_GROK_SURFACE_ALT}",
    tab_idle=_GROK_MUTED,
    input_surface=_GROK_SURFACE,
)

THEME_GROKDAY = TerminalTheme(
    theme_id="grokday",
    label="GrokDay",
    truecolor=True,
    style_dict={
        **THEME_GROKNIGHT.style_dict,
        "bg": "#f5f5f5",
        "top-bar": "#3a3a3a bg:#f5f5f5",
        "block-body": "#1a1a1a",
        "block-title-user": "#1a1a1a bold",
        "block-title-assistant": "#1a1a1a bold",
        "message-body": "#1a1a1a",
        "speaker": "#1a1a1a bold",
        "input-composer": "#1a1a1a bg:#ffffff",
        "input-box": "#8a8a8a",
        "hint": "#8a8a8a",
        "tab-active": "#1a1a1a bold bg:#e8e8e8",
        "tab-idle": "#8a8a8a",
        "overlay-panel": "#1a1a1a bg:#ffffff",
    },
)

THEME_TOKYO_NIGHT = _base_theme(
    theme_id="tokyonight",
    label="TokyoNight",
    bg="#1a1b26",
    fg="#a9b1d6",
    accent="#7aa2f7",
    top_bar="#a9b1d6 bg:#16161e",
    tab_active="#ffffff bold bg:#3d59a1",
    tab_idle="#565f89",
    input_surface="#16161e",
)

THEME_ROSE_PINE = _base_theme(
    theme_id="rosepine",
    label="RosePineMoon",
    bg="#232136",
    fg="#e0def4",
    accent="#c4a7e7",
    top_bar="#e0def4 bg:#232136",
    tab_active="#191724 bold bg:#403d52",
    tab_idle="#908caa",
    input_surface="#2a273f",
)

THEME_OSCURA = _base_theme(
    theme_id="oscura",
    label="OscuraMidnight",
    bg="#030304",
    fg="#e2e2e9",
    accent="#a78bfa",
    top_bar="#e2e2e9 bg:#030304",
    tab_active="#ffffff bold bg:#1f1f22",
    tab_idle="#6b6b70",
    input_surface="#111113",
)

THEME_ADAM = THEME_GROKNIGHT

TERMINAL_THEMES: tuple[TerminalTheme, ...] = (
    THEME_GROKNIGHT,
    THEME_GROKDAY,
    THEME_TOKYO_NIGHT,
    THEME_ROSE_PINE,
    THEME_OSCURA,
)
TERMINAL_THEME_BY_ID = {theme.theme_id: theme for theme in TERMINAL_THEMES}
TERMINAL_THEME_BY_ID["adam"] = THEME_ADAM
TERMINAL_THEME_BY_ID["grok"] = THEME_GROKNIGHT
TERMINAL_THEME_BY_ID["codex"] = THEME_TOKYO_NIGHT


def resolve_terminal_theme(theme_id: str | None = None) -> TerminalTheme:
    normalized = str(theme_id or "groknight").strip().lower()
    return TERMINAL_THEME_BY_ID.get(normalized, THEME_GROKNIGHT)


def build_terminal_style(theme_id: str | None = None) -> Style:
    theme = resolve_terminal_theme(theme_id)
    return Style.from_dict(theme.style_dict)


def cycle_terminal_theme(theme_id: str | None) -> str:
    current = resolve_terminal_theme(theme_id)
    ordered = TERMINAL_THEMES
    index = next((i for i, theme in enumerate(ordered) if theme.theme_id == current.theme_id), 0)
    return ordered[(index + 1) % len(ordered)].theme_id


def list_terminal_theme_labels() -> list[tuple[str, str]]:
    return [(theme.theme_id, theme.label) for theme in TERMINAL_THEMES]
