from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


PERSISTENT_PROCESS_STATE_REF = "runtime/state/terminal/persistent_process_state.json"
PERSISTENT_PROCESS_REPORT_REF = "runtime/reports/latest/digital_life_persistent_process_report.json"


@dataclass(frozen=True)
class PersistentProcessArtifactsResult:
    state: dict[str, Any]
    report: dict[str, Any]


def write_persistent_process_artifacts(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    heartbeat_counter: int,
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
    waiting_mode: str,
    idle_strategy_ref: str | None,
    last_heartbeat_packet_ref: str | None,
    last_dialogue_packet_ref: str | None,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> PersistentProcessArtifactsResult:
    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "schema_version": "persistent_process_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "foreground_terminal_residency",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "next_required_action": "await_process_relaunch_or_new_terminal_wake",
    }
    report = {
        "schema_version": "digital_life_persistent_process_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "foreground_terminal_residency",
        "persistent_process_state_ref": PERSISTENT_PROCESS_STATE_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }

    write_json(terminal_dir / "persistent_process_state.json", state)
    write_json(reports_dir / "digital_life_persistent_process_report.json", report)
    return PersistentProcessArtifactsResult(state=state, report=report)
