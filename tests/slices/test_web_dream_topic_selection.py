import unittest

from life_v0.dream.web_dream_discovery import (
    append_topic_history_entry,
    select_topic_candidate,
    topic_cluster_id,
)


class WebDreamTopicSelectionTests(unittest.TestCase):
    def test_five_rounds_yield_distinct_topic_clusters(self):
        history = {"entries": []}
        clusters: list[str] = []
        for index in range(5):
            cluster = topic_cluster_id(
                title=f"Topic {index}",
                headings=[f"Heading {index}"],
                text_sample=f"sample {index}",
                domain=f"example-{index}.org",
            )
            candidates = [
                {
                    "topic_label": f"Topic {index}",
                    "topic_cluster_id": cluster,
                    "url_digest": f"digest-{index}",
                    "selection_score": 0.8,
                }
            ]
            selection = select_topic_candidate(
                candidates=candidates,
                topic_history=history,
            )
            selected = selection["selected"]
            self.assertIsNotNone(selected)
            clusters.append(str(selected["topic_cluster_id"]))
            history = append_topic_history_entry(
                topic_history=history,
                session_id=f"session-{index}",
                topic_cluster_id_value=cluster,
                url_digest_value=f"digest-{index}",
                generated_at="2026-06-16T12:00:00Z",
                discovery_mode="autonomous",
            )
        self.assertEqual(len(set(clusters)), 5)

    def test_recent_cluster_filtered_by_cooldown(self):
        cluster = topic_cluster_id(
            title="Repeat",
            headings=["A"],
            text_sample="repeat",
            domain="example.org",
        )
        history = {
            "entries": [
                {
                    "topic_cluster_id": cluster,
                    "url_digest": "digest-1",
                }
                for _ in range(3)
            ]
        }
        selection = select_topic_candidate(
            candidates=[
                {
                    "topic_cluster_id": cluster,
                    "url_digest": "digest-2",
                    "selection_score": 0.9,
                }
            ],
            topic_history=history,
            policy={"no_repeat_cluster_window": 3},
        )
        self.assertIsNone(selection["selected"])
        self.assertEqual(
            selection["selection_rationale"]["reason"],
            "all_candidates_filtered_by_cooldown",
        )