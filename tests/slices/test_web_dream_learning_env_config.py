import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from life_v0.dream.web_dream_learning import (
    record_web_dream_learning,
    write_web_dream_learning_toggle,
)


class WebDreamLearningEnvConfigTests(unittest.TestCase):
    def test_env_urls_enable_learning_without_seed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            calls: list[str] = []

            def fake_fetch(url: str, timeout_seconds: float) -> dict:
                del timeout_seconds
                calls.append(url)
                return {
                    "status_code": 200,
                    "final_url": url,
                    "content_type": "text/html",
                    "text": (
                        "<html><head><title>Env Dream Learning</title></head>"
                        "<body><h1>Dream learning from env</h1>"
                        "<p>Configured web residue should become wake material.</p>"
                        "</body></html>"
                    ),
                }

            result = record_web_dream_learning(
                state_dir=state_dir,
                generated_at="2026-06-17T00:00:00Z",
                fetch_url=fake_fetch,
                environ={
                    "DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED": "true",
                    "DIGITAL_LIFE_WEB_DREAM_URLS": "https://example.test/env-dream",
                },
            )

            self.assertEqual(calls, ["https://example.test/env-dream"])
            state = result["state"]
            self.assertEqual(state["status"], "learned")
            self.assertEqual(state["seed_count"], 1)
            self.assertEqual(state["selected_url"], "https://example.test/env-dream")
            self.assertEqual(state["page_title"], "Env Dream Learning")

            written_state = json.loads(
                (state_dir / "dream" / "web_dream_learning_state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(written_state["status"], "learned")

    def test_env_file_urls_enable_learning_without_exported_process_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "runtime" / "state"
            env_path = root / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED=true",
                        "DIGITAL_LIFE_WEB_DREAM_URLS=https://example.test/file-env-dream",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            calls: list[str] = []

            def fake_fetch(url: str, timeout_seconds: float) -> dict:
                del timeout_seconds
                calls.append(url)
                return {
                    "status_code": 200,
                    "final_url": url,
                    "content_type": "text/html",
                    "text": (
                        "<html><head><title>File Env Dream Learning</title></head>"
                        "<body><h1>Dream learning from env file</h1>"
                        "<p>The local env file should feed web dream seeds.</p>"
                        "</body></html>"
                    ),
                }

            patched_env = {
                key: value
                for key, value in os.environ.items()
                if not key.startswith("DIGITAL_LIFE_WEB_DREAM")
            }
            patched_env["DIGITAL_LIFE_ENV_FILE"] = str(env_path)

            with patch.dict(os.environ, patched_env, clear=True):
                result = record_web_dream_learning(
                    state_dir=state_dir,
                    generated_at="2026-06-17T00:00:01Z",
                    fetch_url=fake_fetch,
                )

            self.assertEqual(calls, ["https://example.test/file-env-dream"])
            self.assertEqual(result["state"]["status"], "learned")
            self.assertEqual(result["state"]["page_title"], "File Env Dream Learning")

    def test_manual_off_keeps_learning_disabled_even_when_env_file_default_is_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "runtime" / "state"
            env_path = root / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED=true",
                        "DIGITAL_LIFE_WEB_DREAM_URLS=https://example.test/manual-off-should-not-fetch",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            patched_env = {
                key: value
                for key, value in os.environ.items()
                if not key.startswith("DIGITAL_LIFE_WEB_DREAM")
            }
            patched_env["DIGITAL_LIFE_ENV_FILE"] = str(env_path)
            calls: list[str] = []

            def fake_fetch(url: str, timeout_seconds: float) -> dict:
                del timeout_seconds
                calls.append(url)
                return {
                    "status_code": 200,
                    "final_url": url,
                    "content_type": "text/html",
                    "text": "<html><title>Should Not Fetch</title></html>",
                }

            with patch.dict(os.environ, patched_env, clear=True):
                toggle = write_web_dream_learning_toggle(
                    state_dir=state_dir,
                    enabled=False,
                    generated_at="2026-06-17T00:00:03Z",
                )
                result = record_web_dream_learning(
                    state_dir=state_dir,
                    generated_at="2026-06-17T00:00:04Z",
                    fetch_url=fake_fetch,
                )

            self.assertEqual(toggle["manual_toggle_state"], "disabled")
            self.assertEqual(calls, [])
            state = result["state"]
            self.assertEqual(state["status"], "disabled")
            self.assertEqual(state["seed_count"], 1)
            self.assertEqual(state["selected_url"], None)
