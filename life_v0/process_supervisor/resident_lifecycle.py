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


RESIDENT_LIFECYCLE_STATE_REF = "runtime/state/terminal/resident_lifecycle_state.json"
RESIDENT_LIFECYCLE_COMMAND_REF = "runtime/state/terminal/resident_lifecycle_command.json"
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
        self.min_poll_seconds = max(float(min_poll_seconds), 0.05)

    def poll_line(self, timeout_seconds: float) -> str | None:
        wait_seconds = max(float(timeout_seconds), self.min_poll_seconds)
        deadline = time.monotonic() + wait_seconds
        while True:
            command = _read_json_if_exists(self.command_path)
            command_name = str(command.get("command", "")).strip().lower()
            if command_name in {"stop", "shutdown", "exit"}:
                command["status"] = "consumed"
                command["consumed_at"] = _now_iso()
                _write_json(self.command_path, command)
                return "/exit\n"
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            time.sleep(min(0.05, remaining))


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
    _write_json(terminal_dir / "resident_lifecycle_state.json", state)
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


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
