import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.file_reference_turn import (
    expand_file_references_for_relation_turn,
)


class FileReferenceTurnTests(unittest.TestCase):
    def test_file_reference_is_injected_as_readable_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            docs = repo / "docs"
            docs.mkdir()
            (docs / "sample.md").write_text(
                "# 记忆设计\n\n这里写了海马索引、长期记忆和醒后召回。",
                encoding="utf-8",
            )

            expanded = expand_file_references_for_relation_turn(
                "看一下 @docs/sample.md 然后说说记忆",
                repo_root=repo,
            )

            self.assertIn("看一下 @docs/sample.md 然后说说记忆", expanded.utterance)
            self.assertIn("引用文件: docs/sample.md", expanded.utterance)
            self.assertIn("海马索引", expanded.utterance)
            self.assertEqual(expanded.references[0]["path"], "docs/sample.md")
            self.assertEqual(expanded.references[0]["status"], "included")

    def test_env_and_runtime_references_are_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".env").write_text("SECRET=1", encoding="utf-8")
            (repo / "runtime" / "state").mkdir(parents=True)
            (repo / "runtime" / "state" / "x.json").write_text("{}", encoding="utf-8")

            expanded = expand_file_references_for_relation_turn(
                "看 @.env 和 @runtime/state/x.json",
                repo_root=repo,
            )

            self.assertNotIn("SECRET", expanded.utterance)
            statuses = {item["path"]: item["status"] for item in expanded.references}
            self.assertEqual(statuses[".env"], "blocked")
            self.assertEqual(statuses["runtime/state/x.json"], "blocked")

