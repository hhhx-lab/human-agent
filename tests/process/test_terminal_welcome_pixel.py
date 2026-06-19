import unittest
from pathlib import Path

from life_v0.process_supervisor.terminal_theme import build_terminal_style
from life_v0.process_supervisor.terminal_welcome_pixel import (
    _progress_percent,
    format_pixel_welcome_screen,
    render_welcome_preview_frames,
)
from life_v0.process_supervisor.terminal_ui import resolve_relation_turn_display_text
from life_v0.process_supervisor.resident_lifecycle import send_resident_relation_turn


class TerminalWelcomePixelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terminal_dir = Path("runtime/state/terminal")

    def test_progress_reaches_one_hundred(self):
        self.assertEqual(_progress_percent(64), 100.0)
        self.assertEqual(_progress_percent(200), 100.0)

    def test_welcome_screen_renders_terminal_humanoid_hud(self):
        rendered = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=self.terminal_dir,
                life_name="Adam",
                selection=0,
                width=128,
                height=52,
                animation_tick=64,
            )
        )
        self.assertIn("╭", rendered)
        self.assertIn("╰", rendered)
        self.assertIn("Digital Life", rendered)
        self.assertIn("Adam", rendered)
        self.assertIn("INITIATE: SOUL_GEN.EXE", rendered)
        self.assertIn("PHASE: BIRTH", rendered)
        self.assertIn("SOUL INTEGRITY: 100.0%", rendered)
        self.assertIn("●", rendered)
        self.assertIn("◈", rendered)
        self.assertNotIn("◈ CORE ◈", rendered)
        self.assertGreaterEqual(rendered.count("0") + rendered.count("1"), 90)
        self.assertIn("██  ██", rendered)
        self.assertIn("██████", rendered)
        self.assertIn("╭─", rendered)
        self.assertIn("├", rendered)
        self.assertIn("╰●╯", rendered)
        self.assertIn("01001001", rendered)
        self.assertIn("10110100", rendered)
        self.assertIn("01011010", rendered)
        self.assertIn("10100101", rendered)
        self.assertIn("01101001", rendered)
        self.assertIn("STREAMING", rendered)
        self.assertIn("[", rendered)
        self.assertIn("]", rendered)
        self.assertIn("POST-HUMAN SYMBIOSIS", rendered)
        self.assertIn("PROTOCOL: LINKED", rendered)
        self.assertIn("[ OK ]", rendered)
        self.assertNotIn("POST-HUMAN SYMBIOSIS PROTOCOL: LINKED", rendered)
        self.assertIn("█", rendered)

    def test_welcome_uses_red_heart_and_fast_particle_styles(self):
        fragments = format_pixel_welcome_screen(
            terminal_dir=self.terminal_dir,
            life_name="Adam",
            selection=0,
            width=128,
            height=52,
            animation_tick=64,
        )
        styles = [style for style, _ in fragments]
        self.assertIn("class:welcome-heart-red", styles)
        self.assertIn("class:welcome-particle-white", styles)
        self.assertIn("class:welcome-circuit-green", styles)
        self.assertIn("class:welcome-pixel-magenta", styles)

    def test_welcome_zero_frame_starts_as_particle_convergence(self):
        rendered = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=self.terminal_dir,
                life_name="Adam",
                selection=0,
                width=128,
                height=52,
                animation_tick=0,
            )
        )
        flow_count = sum(rendered.count(char) for char in ("·", "∙", "•", "✦"))
        self.assertGreaterEqual(flow_count, 30)
        self.assertNotIn("INITIATE: SOUL_GEN.EXE", rendered)
        self.assertNotIn("SOUL INTEGRITY", rendered)
        self.assertNotIn("01001001", rendered)
        self.assertNotIn("██  ██", rendered)

    def test_welcome_animation_fades_in(self):
        early = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=self.terminal_dir,
                life_name="Adam",
                selection=0,
                width=128,
                height=52,
                animation_tick=4,
            )
        )
        late = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=self.terminal_dir,
                life_name="Adam",
                selection=0,
                width=128,
                height=52,
                animation_tick=64,
            )
        )
        self.assertIn("PHASE: BIRTH", early)
        self.assertLess(early.count("█"), late.count("█"))
        self.assertIn("POST-HUMAN SYMBIOSIS", late)
        self.assertIn("PROTOCOL: LINKED", late)
        self.assertIn("PHASE: BIRTH", late)
        self.assertNotEqual(early, late)

    def test_welcome_progress_holds_after_full_load_while_flow_moves(self):
        full_a = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=self.terminal_dir,
                life_name="Adam",
                selection=0,
                width=128,
                height=52,
                animation_tick=64,
            )
        )
        full_b = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=self.terminal_dir,
                life_name="Adam",
                selection=0,
                width=128,
                height=52,
                animation_tick=96,
            )
        )
        self.assertIn("加载 100.0%", full_a)
        self.assertIn("加载 100.0%", full_b)
        self.assertNotEqual(full_a, full_b)

    def test_preview_frames_cover_full_cycle(self):
        frames = render_welcome_preview_frames(ticks=range(0, 16, 8))
        self.assertEqual(len(frames), 2)

    def test_welcome_theme_styles_compile(self):
        build_terminal_style("groknight")

    def test_dialogue_still_works_after_welcome_pipeline(self):
        turn_result = send_resident_relation_turn(
            terminal_dir=self.terminal_dir,
            utterance="欢迎页之后还能对话吗？",
            wait_timeout_seconds=90.0,
        )
        response_event = turn_result.state.get("response_event") or {}
        response = resolve_relation_turn_display_text(
            utterance="欢迎页之后还能对话吗？",
            response_text=str(turn_result.state.get("response_text") or ""),
            send_status=str(turn_result.state.get("send_status") or ""),
            output_status=str(response_event.get("status") or ""),
        )
        self.assertTrue(response.strip())


if __name__ == "__main__":
    unittest.main()
