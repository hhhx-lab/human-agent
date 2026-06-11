from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .resident_autonomous_activity import record_resident_autonomous_activity


RESIDENT_LIFECYCLE_STATE_REF = "runtime/state/terminal/resident_lifecycle_state.json"
RESIDENT_LIFECYCLE_COMMAND_REF = "runtime/state/terminal/resident_lifecycle_command.json"
RESIDENT_RELATION_INBOX_REF = "runtime/state/terminal/resident_relation_inbox.jsonl"
RESIDENT_RELATION_OUTBOX_REF = "runtime/state/terminal/resident_relation_outbox.jsonl"
RESIDENT_RELATION_QUEUE_STATE_REF = (
    "runtime/state/terminal/resident_relation_queue_state.json"
)
RESIDENT_AUTONOMOUS_ACTIVITY_REF = (
    "runtime/state/terminal/resident_autonomous_activity.jsonl"
)
RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF = (
    "runtime/state/terminal/resident_autonomous_activity_state.json"
)
RESIDENT_BACKGROUND_LOG_REF = "runtime/logs/digital_life_resident.log"


@dataclass(frozen=True)
class ResidentLifecycleResult:
    exit_code: int
    state: dict[str, Any]


class ResidentControlInputStream:
    def __init__(
        self,
        *,
        terminal_dir: Path,
        min_poll_seconds: float = 1.0,
    ) -> None:
        self.terminal_dir = terminal_dir
        self.command_path = terminal_dir / "resident_lifecycle_command.json"
        self.inbox_path = terminal_dir / "resident_relation_inbox.jsonl"
        self.outbox_path = terminal_dir / "resident_relation_outbox.jsonl"
        self.queue_state_path = terminal_dir / "resident_relation_queue_state.json"
        self.min_poll_seconds = max(float(min_poll_seconds), 0.05)
        queue_state = _read_json_if_exists(self.queue_state_path)
        self.last_consumed_sequence = _int_or_zero(
            queue_state.get("last_consumed_sequence")
        )

    def poll_line(self, timeout_seconds: float) -> str | None:
        wait_seconds = max(float(timeout_seconds), self.min_poll_seconds)
        deadline = time.monotonic() + wait_seconds
        while True:
            command = _read_json_if_exists(self.command_path)
            command_name = str(command.get("command", "")).strip().lower()
            command_status = str(command.get("status", "")).strip().lower()
            if (
                command_name in {"stop", "shutdown", "exit"}
                and command_status not in {"consumed", "cleared_for_start"}
            ):
                command["status"] = "consumed"
                command["consumed_at"] = _now_iso()
                _write_json(self.command_path, command)
                return "/exit\n"
            inbox_event = self._next_inbox_event()
            if inbox_event:
                self.last_consumed_sequence = _int_or_zero(inbox_event["sequence"])
                self._mark_inbox_event_active(inbox_event)
                return str(inbox_event.get("utterance", "")).rstrip("\n") + "\n"
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                self.record_autonomous_activity()
                return None
            time.sleep(min(0.05, remaining))

    def record_autonomous_activity(self) -> None:
        result = record_resident_autonomous_activity(
            terminal_dir=self.terminal_dir,
            now_iso=_now_iso,
        )
        state = result["state"]
        event = result["event"]
        lifecycle_state = _read_json_if_exists(
            self.terminal_dir / "resident_lifecycle_state.json"
        )
        if lifecycle_state:
            lifecycle_state["last_autonomous_activity_kind"] = event["activity_kind"]
            lifecycle_state["last_autonomous_activity_at"] = event["generated_at"]
            lifecycle_state["last_autonomous_activity_state_ref"] = event[
                "activity_state_ref"
            ]
            lifecycle_state["autonomous_activity_count"] = state["activity_count"]
            lifecycle_state["autonomous_activity_kind_counts"] = dict(
                state.get("activity_kind_counts", {})
            )
            lifecycle_state["resident_autonomous_activity_state_refs"] = dict(
                state.get("activity_state_refs", {})
            )
            lifecycle_state["resident_autonomous_activity_ref"] = (
                RESIDENT_AUTONOMOUS_ACTIVITY_REF
            )
            lifecycle_state["resident_autonomous_activity_state_ref"] = (
                RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF
            )
            _write_json(self.terminal_dir / "resident_lifecycle_state.json", lifecycle_state)

    def record_output(self, emitted_output: str) -> None:
        queue_state = _read_json_if_exists(self.queue_state_path)
        active_sequence = _int_or_zero(queue_state.get("active_sequence"))
        if not active_sequence:
            return
        response_text = _extract_response_text(emitted_output)
        outbox_event = {
            "schema_version": "resident_relation_outbox_event_v0",
            "sequence": active_sequence,
            "turn_id": queue_state.get("active_turn_id"),
            "utterance": queue_state.get("active_utterance"),
            "emitted_output": emitted_output,
            "response_text": response_text,
            "status": "completed" if response_text else "incident_or_system_output",
            "generated_at": _now_iso(),
            "resident_relation_inbox_ref": RESIDENT_RELATION_INBOX_REF,
            "resident_relation_outbox_ref": RESIDENT_RELATION_OUTBOX_REF,
            "resident_relation_queue_state_ref": RESIDENT_RELATION_QUEUE_STATE_REF,
        }
        _append_jsonl(self.outbox_path, outbox_event)
        queue_state["status"] = "waiting_for_relation_turn"
        queue_state["last_completed_sequence"] = active_sequence
        queue_state["last_completed_turn_id"] = queue_state.get("active_turn_id")
        queue_state["last_response_text"] = response_text
        queue_state["last_response_at"] = outbox_event["generated_at"]
        for key in ("active_sequence", "active_turn_id", "active_utterance", "active_started_at"):
            queue_state.pop(key, None)
        _write_json(self.queue_state_path, queue_state)
        lifecycle_state = _read_json_if_exists(
            self.terminal_dir / "resident_lifecycle_state.json"
        )
        if lifecycle_state:
            lifecycle_state["last_relation_turn_sequence"] = active_sequence
            lifecycle_state["last_relation_turn_id"] = outbox_event["turn_id"]
            lifecycle_state["last_relation_turn_completed_at"] = outbox_event[
                "generated_at"
            ]
            lifecycle_state["resident_relation_inbox_ref"] = RESIDENT_RELATION_INBOX_REF
            lifecycle_state["resident_relation_outbox_ref"] = RESIDENT_RELATION_OUTBOX_REF
            lifecycle_state["resident_relation_queue_state_ref"] = (
                RESIDENT_RELATION_QUEUE_STATE_REF
            )
            _write_json(self.terminal_dir / "resident_lifecycle_state.json", lifecycle_state)

    def _next_inbox_event(self) -> dict[str, Any]:
        for event in _read_jsonl(self.inbox_path):
            sequence = _int_or_zero(event.get("sequence"))
            if sequence > self.last_consumed_sequence and event.get("utterance"):
                return event
        return {}

    def _mark_inbox_event_active(self, event: dict[str, Any]) -> None:
        queue_state = _read_json_if_exists(self.queue_state_path)
        queue_state.update(
            {
                "schema_version": "resident_relation_queue_state_v0",
                "status": "turn_in_progress",
                "active_sequence": _int_or_zero(event.get("sequence")),
                "active_turn_id": event.get("turn_id"),
                "active_utterance": event.get("utterance"),
                "active_started_at": _now_iso(),
                "last_consumed_sequence": _int_or_zero(event.get("sequence")),
                "resident_relation_inbox_ref": RESIDENT_RELATION_INBOX_REF,
                "resident_relation_outbox_ref": RESIDENT_RELATION_OUTBOX_REF,
                "resident_relation_queue_state_ref": RESIDENT_RELATION_QUEUE_STATE_REF,
            }
        )
        _write_json(self.queue_state_path, queue_state)


def start_background_resident_process(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None,
    strict: bool,
    resident_sleep_seconds: float,
    cwd: Path,
) -> ResidentLifecycleResult:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    terminal_dir = state_dir / "terminal"
    logs_dir = state_dir.parent / "logs"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    current_state = read_resident_lifecycle_status(terminal_dir=terminal_dir).state
    if current_state.get("pid_alive") and current_state.get("status") in {
        "background_starting",
        "background_active",
    }:
        return ResidentLifecycleResult(exit_code=0, state=current_state)

    background_run_id = run_id or _default_run_id("digital-life-resident-")
    _clear_stale_lifecycle_command(
        command_path=terminal_dir / "resident_lifecycle_command.json",
        run_id=background_run_id,
    )
    command = [
        sys.executable,
        "-c",
        "from life_v0.digital_entry import main; raise SystemExit(main())",
        "life",
        "--state",
        str(state_dir),
        "--reports",
        str(reports_dir),
        "--receipts",
        str(receipts_dir),
        "--run-id",
        background_run_id,
        "--resident",
        "--resident-sleep-seconds",
        str(resident_sleep_seconds),
    ]
    if strict:
        command.append("--strict")

    log_path = logs_dir / "digital_life_resident.log"
    with (logs_dir / "digital_life_resident.spawn.log").open(
        "a",
        encoding="utf-8",
    ) as spawn_log:
        spawn_log.write(
            json.dumps(
                {
                    "schema_version": "resident_spawn_event_v0",
                    "generated_at": _now_iso(),
                    "run_id": background_run_id,
                    "command": command,
                    "log_ref": RESIDENT_BACKGROUND_LOG_REF,
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    devnull = open(os.devnull, "r", encoding="utf-8")
    log_handle = log_path.open("a", encoding="utf-8")
    try:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            stdin=devnull,
            stdout=log_handle,
            stderr=log_handle,
            start_new_session=True,
            close_fds=True,
        )
    finally:
        devnull.close()
        log_handle.close()

    state = _base_lifecycle_state(
        run_id=background_run_id,
        status="background_starting",
        pid=process.pid,
        resident_sleep_seconds=resident_sleep_seconds,
    )
    state["log_ref"] = RESIDENT_BACKGROUND_LOG_REF
    _write_json(terminal_dir / "resident_lifecycle_state.json", state)
    return ResidentLifecycleResult(exit_code=0, state=state)


def mark_resident_lifecycle_active(
    *,
    terminal_dir: Path,
    run_id: str,
    resident_sleep_seconds: float,
) -> dict[str, Any]:
    terminal_dir.mkdir(parents=True, exist_ok=True)
    state = _base_lifecycle_state(
        run_id=run_id,
        status="background_active",
        pid=os.getpid(),
        resident_sleep_seconds=resident_sleep_seconds,
    )
    state["residency_posture"] = "sleeping_waiting_for_relation_turn"
    state["started_at"] = _now_iso()
    state["log_ref"] = RESIDENT_BACKGROUND_LOG_REF
    state["resident_relation_inbox_ref"] = RESIDENT_RELATION_INBOX_REF
    state["resident_relation_outbox_ref"] = RESIDENT_RELATION_OUTBOX_REF
    state["resident_relation_queue_state_ref"] = RESIDENT_RELATION_QUEUE_STATE_REF
    state["resident_autonomous_activity_ref"] = RESIDENT_AUTONOMOUS_ACTIVITY_REF
    state["resident_autonomous_activity_state_ref"] = (
        RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF
    )
    _write_json(terminal_dir / "resident_lifecycle_state.json", state)
    _write_json(
        terminal_dir / "resident_relation_queue_state.json",
        {
            "schema_version": "resident_relation_queue_state_v0",
            "status": "waiting_for_relation_turn",
            "last_consumed_sequence": 0,
            "last_enqueued_sequence": 0,
            "last_completed_sequence": 0,
            "resident_relation_inbox_ref": RESIDENT_RELATION_INBOX_REF,
            "resident_relation_outbox_ref": RESIDENT_RELATION_OUTBOX_REF,
            "resident_relation_queue_state_ref": RESIDENT_RELATION_QUEUE_STATE_REF,
        },
    )
    return state


def mark_resident_lifecycle_stopped(
    *,
    terminal_dir: Path,
    run_id: str,
    exit_code: int,
) -> dict[str, Any]:
    previous = _read_json_if_exists(terminal_dir / "resident_lifecycle_state.json")
    state = dict(previous)
    state.setdefault("schema_version", "resident_lifecycle_state_v0")
    state["run_id"] = run_id
    state["status"] = "stopped"
    state["pid"] = os.getpid()
    state["pid_alive"] = False
    state["stopped_at"] = _now_iso()
    state["exit_code"] = exit_code
    state.setdefault("resident_lifecycle_state_ref", RESIDENT_LIFECYCLE_STATE_REF)
    state.setdefault("resident_lifecycle_command_ref", RESIDENT_LIFECYCLE_COMMAND_REF)
    _write_json(terminal_dir / "resident_lifecycle_state.json", state)
    return state


def request_resident_stop(
    *,
    terminal_dir: Path,
    timeout_seconds: float = 10.0,
) -> ResidentLifecycleResult:
    terminal_dir.mkdir(parents=True, exist_ok=True)
    status = read_resident_lifecycle_status(terminal_dir=terminal_dir).state
    pid = _int_or_zero(status.get("pid"))
    command = {
        "schema_version": "resident_lifecycle_command_v0",
        "command": "stop",
        "status": "requested",
        "requested_at": _now_iso(),
        "target_pid": pid or None,
    }
    _write_json(terminal_dir / "resident_lifecycle_command.json", command)
    if not pid or not _pid_alive(pid):
        status["status"] = "stopped"
        status["pid_alive"] = False
        status["stopped_at"] = _now_iso()
        _write_json(terminal_dir / "resident_lifecycle_state.json", status)
        return ResidentLifecycleResult(exit_code=0, state=status)

    deadline = time.monotonic() + max(timeout_seconds, 0.0)
    while time.monotonic() < deadline:
        if not _pid_alive(pid):
            status = read_resident_lifecycle_status(terminal_dir=terminal_dir).state
            status["status"] = "stopped"
            status["pid_alive"] = False
            status["stopped_at"] = status.get("stopped_at") or _now_iso()
            _write_json(terminal_dir / "resident_lifecycle_state.json", status)
            return ResidentLifecycleResult(exit_code=0, state=status)
        time.sleep(0.1)

    status = read_resident_lifecycle_status(terminal_dir=terminal_dir).state
    status["status"] = "stop_requested"
    status["pid_alive"] = _pid_alive(pid)
    status["last_stop_request_ref"] = RESIDENT_LIFECYCLE_COMMAND_REF
    _write_json(terminal_dir / "resident_lifecycle_state.json", status)
    return ResidentLifecycleResult(exit_code=1, state=status)


def send_resident_relation_turn(
    *,
    terminal_dir: Path,
    utterance: str,
    wait_timeout_seconds: float = 30.0,
) -> ResidentLifecycleResult:
    terminal_dir.mkdir(parents=True, exist_ok=True)
    lifecycle_status = read_resident_lifecycle_status(terminal_dir=terminal_dir).state
    if not lifecycle_status.get("pid_alive") or lifecycle_status.get("status") not in {
        "background_starting",
        "background_active",
    }:
        lifecycle_status["send_status"] = "resident_not_active"
        return ResidentLifecycleResult(exit_code=1, state=lifecycle_status)
    inbox_path = terminal_dir / "resident_relation_inbox.jsonl"
    outbox_path = terminal_dir / "resident_relation_outbox.jsonl"
    queue_state_path = terminal_dir / "resident_relation_queue_state.json"
    sequence = _next_inbox_sequence(inbox_path)
    turn_id = f"resident-relation-turn-{sequence:06d}"
    event = {
        "schema_version": "resident_relation_inbox_event_v0",
        "sequence": sequence,
        "turn_id": turn_id,
        "utterance": utterance,
        "status": "queued",
        "enqueued_at": _now_iso(),
        "resident_relation_inbox_ref": RESIDENT_RELATION_INBOX_REF,
        "resident_relation_outbox_ref": RESIDENT_RELATION_OUTBOX_REF,
        "resident_relation_queue_state_ref": RESIDENT_RELATION_QUEUE_STATE_REF,
    }
    _append_jsonl(inbox_path, event)
    queue_state = _read_json_if_exists(queue_state_path)
    queue_state.update(
        {
            "schema_version": "resident_relation_queue_state_v0",
            "status": "queued",
            "last_enqueued_sequence": sequence,
            "last_enqueued_turn_id": turn_id,
            "last_enqueued_at": event["enqueued_at"],
            "resident_relation_inbox_ref": RESIDENT_RELATION_INBOX_REF,
            "resident_relation_outbox_ref": RESIDENT_RELATION_OUTBOX_REF,
            "resident_relation_queue_state_ref": RESIDENT_RELATION_QUEUE_STATE_REF,
        }
    )
    _write_json(queue_state_path, queue_state)
    response_event = _wait_for_outbox_event(
        outbox_path=outbox_path,
        sequence=sequence,
        timeout_seconds=wait_timeout_seconds,
    )
    state = {
        **event,
        "send_status": "completed" if response_event else "queued_wait_timeout",
        "resident_lifecycle_state_ref": RESIDENT_LIFECYCLE_STATE_REF,
        "pid": lifecycle_status.get("pid"),
        "pid_alive": lifecycle_status.get("pid_alive"),
    }
    if response_event:
        state["response_event"] = response_event
        state["response_text"] = response_event.get("response_text")
        state["emitted_output"] = response_event.get("emitted_output")
    return ResidentLifecycleResult(exit_code=0 if response_event else 1, state=state)


def read_resident_lifecycle_status(*, terminal_dir: Path) -> ResidentLifecycleResult:
    state = _read_json_if_exists(terminal_dir / "resident_lifecycle_state.json")
    if not state:
        state = {
            "schema_version": "resident_lifecycle_state_v0",
            "status": "not_started",
            "resident_lifecycle_state_ref": RESIDENT_LIFECYCLE_STATE_REF,
            "resident_lifecycle_command_ref": RESIDENT_LIFECYCLE_COMMAND_REF,
        }
    pid = _int_or_zero(state.get("pid"))
    state["pid_alive"] = bool(pid and _pid_alive(pid))
    queue_state = _read_json_if_exists(terminal_dir / "resident_relation_queue_state.json")
    if queue_state:
        state["resident_relation_queue_state"] = queue_state
        state["resident_relation_queue_status"] = queue_state.get("status")
        state["resident_relation_last_completed_sequence"] = queue_state.get(
            "last_completed_sequence"
        )
        state["resident_relation_last_enqueued_sequence"] = queue_state.get(
            "last_enqueued_sequence"
        )
    autonomous_activity_state = _read_json_if_exists(
        terminal_dir / "resident_autonomous_activity_state.json"
    )
    if autonomous_activity_state:
        state["resident_autonomous_activity_state"] = autonomous_activity_state
        state["resident_autonomous_activity_count"] = autonomous_activity_state.get(
            "activity_count"
        )
        state["resident_autonomous_activity_last_kind"] = autonomous_activity_state.get(
            "last_activity_kind"
        )
        state["resident_autonomous_activity_current_cycle"] = autonomous_activity_state.get(
            "current_cycle"
        )
    return ResidentLifecycleResult(exit_code=0, state=state)


def _base_lifecycle_state(
    *,
    run_id: str,
    status: str,
    pid: int,
    resident_sleep_seconds: float,
) -> dict[str, Any]:
    return {
        "schema_version": "resident_lifecycle_state_v0",
        "run_id": run_id,
        "generated_at": _now_iso(),
        "status": status,
        "pid": pid,
        "pid_alive": True,
        "resident_lifecycle_state_ref": RESIDENT_LIFECYCLE_STATE_REF,
        "resident_lifecycle_command_ref": RESIDENT_LIFECYCLE_COMMAND_REF,
        "resident_relation_inbox_ref": RESIDENT_RELATION_INBOX_REF,
        "resident_relation_outbox_ref": RESIDENT_RELATION_OUTBOX_REF,
        "resident_relation_queue_state_ref": RESIDENT_RELATION_QUEUE_STATE_REF,
        "resident_autonomous_activity_ref": RESIDENT_AUTONOMOUS_ACTIVITY_REF,
        "resident_autonomous_activity_state_ref": RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
        "resident_sleep_seconds": resident_sleep_seconds,
        "residency_mode": "background_resident_process",
        "residency_posture": "sleeping_waiting_for_relation_turn",
    }


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except (ValueError, TypeError):
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _clear_stale_lifecycle_command(*, command_path: Path, run_id: str) -> None:
    previous = _read_json_if_exists(command_path)
    payload = {
        "schema_version": "resident_lifecycle_command_v0",
        "command": "none",
        "status": "cleared_for_start",
        "cleared_at": _now_iso(),
        "run_id": run_id,
    }
    if previous:
        payload["previous_command"] = previous.get("command")
        payload["previous_status"] = previous.get("status")
        payload["previous_requested_at"] = previous.get("requested_at")
        payload["previous_consumed_at"] = previous.get("consumed_at")
    _write_json(command_path, payload)


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _next_inbox_sequence(path: Path) -> int:
    sequences = [_int_or_zero(event.get("sequence")) for event in _read_jsonl(path)]
    return (max(sequences) if sequences else 0) + 1


def _wait_for_outbox_event(
    *,
    outbox_path: Path,
    sequence: int,
    timeout_seconds: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + max(float(timeout_seconds), 0.0)
    while time.monotonic() < deadline:
        for event in _read_jsonl(outbox_path):
            if _int_or_zero(event.get("sequence")) == sequence:
                return event
        time.sleep(0.1)
    return {}


def _extract_response_text(emitted_output: str) -> str:
    prefix = "生命回合输出: "
    if emitted_output.startswith(prefix):
        return emitted_output[len(prefix) :].strip()
    return ""
