import unittest

from life_v0.neural_core.network_state import (
    build_network_state,
    network_conflict_monitoring_inspection_snapshot,
    project_network_state_from_live_turn,
)


class NetworkStateConflictTests(unittest.TestCase):
    def test_seed_includes_conflict_monitoring_network(self):
        network_state = build_network_state(
            run_id="network-conflict-seed",
            generated_at="2026-06-15T05:00:00+00:00",
            bus_payload={"edges": [{"edge_id": "signal_media_bus"}]},
            brain_graph={"brain_graph_id": "brain-graph-network-conflict-seed"},
        )

        network_ids = [
            item["network_id"] for item in network_state["active_networks"]
        ]
        self.assertIn("conflict_monitoring_network", network_ids)
        self.assertEqual(network_state["conflict_monitor"]["status"], "standby")

    def test_live_projection_activates_conflict_monitoring(self):
        seeded = build_network_state(
            run_id="network-conflict-live",
            generated_at="2026-06-15T05:00:00+00:00",
            bus_payload={"edges": [{"edge_id": "signal_media_bus"}]},
            brain_graph={"brain_graph_id": "brain-graph-network-conflict-live"},
        )
        projected = project_network_state_from_live_turn(
            network_state=seeded,
            generated_at="2026-06-15T06:00:00+00:00",
            run_id="network-conflict-live-turn",
            live_turn_focus="repair_guarded_continuity",
            signal_media_runtime={
                "modulation_vector": {"repair_drive": 0.72, "inhibition": 0.65}
            },
            metacognition_state={"uncertainty_flags": ["semantic_ambiguity"]},
            broadcast_frame={"suppressed_content_refs": ["ref-a", "ref-b"]},
            go_nogo_state={"release_posture": "confirmation_blocked"},
        )

        self.assertEqual(projected["dominant_network"], "conflict_monitoring_network")
        self.assertEqual(projected["conflict_monitor"]["status"], "active")
        self.assertGreaterEqual(projected["conflict_monitor"]["conflict_signal_count"], 1)
        conflict_switch = [
            event
            for event in projected["switch_events"]
            if event.get("to_network") == "conflict_monitoring_network"
        ]
        self.assertTrue(conflict_switch)

    def test_inspection_snapshot_fields(self):
        snapshot = network_conflict_monitoring_inspection_snapshot(
            network_state={
                "dominant_network": "conflict_monitoring_network",
                "transition_cost": 0.56,
                "active_networks": [
                    {
                        "network_id": "conflict_monitoring_network",
                        "mode": "active_conflict_resolution",
                    }
                ],
                "conflict_monitor": {
                    "status": "active",
                    "conflict_signal_count": 3,
                },
            }
        )
        self.assertTrue(snapshot["network_conflict_monitoring_present"])
        self.assertTrue(snapshot["network_conflict_monitoring_active"])
        self.assertEqual(snapshot["network_conflict_signal_count"], 3)