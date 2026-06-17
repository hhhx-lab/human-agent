from __future__ import annotations

import unittest

from life_v0.state_store.relation_identity_hygiene import (
    extract_observed_names_from_utterances,
    is_valid_observed_name,
    sanitize_observed_names,
)


class RelationIdentityHygieneTests(unittest.TestCase):
    def test_valid_chinese_name(self):
        self.assertTrue(is_valid_observed_name("何剑宝"))

    def test_rejects_question_fragment_and_provider_name(self):
        self.assertFalse(is_valid_observed_name("哪一种吗"))
        self.assertFalse(is_valid_observed_name("ChatGPT"))

    def test_extract_only_from_explicit_introduction_patterns(self):
        names = extract_observed_names_from_utterances(
            ["我叫何剑宝，以后叫我阿宝。", "你是哪一种吗？"]
        )
        self.assertEqual(names, ["何剑宝", "阿宝"])

    def test_exit_dream_style_inputs_do_not_leak_identity_noise(self):
        names = extract_observed_names_from_utterances(
            [
                "我是 ChatGPT 吗？",
                "你是哪一种吗？",
                "我是一个语言模型这种说法不对。",
                "之后你可以叫我阿宝。",
            ]
        )
        self.assertEqual(names, ["阿宝"])

    def test_sanitize_prunes_polluted_list(self):
        self.assertEqual(
            sanitize_observed_names(["何剑宝", "哪一种吗", "GPT", "阿宝"]),
            ["何剑宝", "阿宝"],
        )


if __name__ == "__main__":
    unittest.main()
