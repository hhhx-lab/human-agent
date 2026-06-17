from __future__ import annotations

import argparse
import json
import sys
from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Callable

from .activation import run_first_activation_preflight
from .archive import run_write_growth_archive
from .authority import run_source_authority
from .body import run_check_life_support, run_life_support
from .contracts import run_check_v0_contracts
from .direction import run_direction_lock
from .dream.web_dream_learning import (
    build_web_dream_learning_effective_seed_preview,
    write_web_dream_learning_toggle,
)
from .process_supervisor.file_reference_turn import (
    expand_file_references_for_relation_turn,
)
from .process_supervisor.life_feature_audit import build_life_feature_audit
from .process_supervisor.prompt_toolkit_terminal_app import (
    prompt_toolkit_available,
    run_prompt_toolkit_terminal_app,
)
from .doc_index import run_doc_ingestion
from .growth import run_cycle
from .language import run_build_language_relationship, run_check_language_relationship
from .life_targets import run_birth_readiness
from .membrane import run_check_life_membrane, run_life_membrane
from .neural_core import run_check_neural_life_core, run_neural_life_core
from .process_supervisor import run_digital_life_process
from .process_supervisor.resident_lifecycle import (
    ResidentControlInputStream,
    mark_resident_lifecycle_active,
    mark_resident_lifecycle_stopped,
    read_resident_lifecycle_status,
    request_resident_stop,
    send_resident_relation_turn,
    start_background_resident_process,
)
from .process_supervisor.state_inspection import (
    STATE_INSPECTION_CATEGORIES,
    build_resident_state_inspection,
)
from .process_supervisor.terminal_inspection_compose import (
    COMPOSITE_CATEGORIES,
    build_composite_state_inspection,
)
from .process_supervisor.terminal_input import (
    build_terminal_completion_state,
    build_terminal_input_profile,
    write_terminal_input_profile,
)
from .process_supervisor.terminal_session_transcript import (
    append_terminal_session_event,
    render_resume_transcript,
    start_terminal_session_transcript,
)
from .process_supervisor.proactive_terminal_voice import (
    build_resident_proactive_terminal_event,
    write_resident_proactive_terminal_event,
)
from .process_supervisor.model_expression import (
    ModelExpressionTransport,
    compose_model_expression,
)
from .process_supervisor.terminal_ui import (
    render_dialogue_box,
    render_digital_life_banner,
    render_input_prompt,
    render_life_opening,
)
from .reporting import run_emit_report
from .replay import run_replay_shadow
from .schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
from .stage_explain import run_explain_stage
from .state_store import run_check_state_store, run_state_store
from .validators import run_check_validation_membrane, run_validation_membrane


SLASH_COMPOSITE_COMMANDS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("me", "我是谁：生命名、等待姿态、关系阶段、表达与记忆摘要", ("/me", "/我是谁")),
    ("turn", "上一关系回合：语义焦点、召回引用、表达门与模型状态", ("/turn", "/回合", "/last-turn")),
    ("recall", "记忆召回链路：检索帧→语义地图→表达计划接地", ("/recall", "/唤回", "/召回链")),
    ("express", "表达释放链路：计划、监视器、模型门、能否自然说话", ("/express", "/表达", "/release")),
    ("carry", "跨唤醒携带：关系角色、共享词、时间线恢复引用", ("/carry", "/携带", "/resume-carry")),
    ("background", "后台活动：自主循环、思考记账、主动发话、网页梦境", ("/background", "/后台", "/idle")),
    ("converge", "慢收敛：性格慢变量、语言节奏、共享词晋升", ("/converge", "/收敛", "/slow-change")),
)

SLASH_STATE_COMMANDS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("state", "常驻状态、生命周期、等待心跳、终端输入", ("/state", "/status", "/terminal", "/lifecycle", "/heartbeat", "/queue")),
    ("context", "关系上下文、语义焦点、回合累积", ("/context", "/上下文")),
    ("memory", "短期/长期记忆、召回、写门、沉淀层", ("/memory", "/记忆", "/short-memory", "/long-memory", "/stm", "/ltm")),
    ("dream", "梦境、离线整合、醒后整合、网页梦境学习", ("/dream", "/梦境")),
    ("growth", "成长、学习、自我修改候选、反遗忘回放", ("/growth", "/成长", "/learning")),
    ("body", "身体节律、资源预算、需要状态", ("/body", "/身体")),
    ("emotion", "情绪、痛苦压力、调节循环", ("/emotion", "/情绪", "/affect")),
    ("inner_environment", "内环境、稳态、资源和调制压力", ("/inner", "/内环境", "/homeostasis")),
    ("signal", "信号介质、调质、预测误差与释放偏置", ("/signal", "/调质", "/modulation")),
    ("membrane", "生命膜、事实门、边界与验证膜", ("/membrane", "/生命膜", "/boundary")),
    ("relationship", "关系时间线、承诺、共同语言、关系阶段", ("/relationship", "/relation", "/关系")),
    ("responsibility", "责任、痛苦、后悔、修复链", ("/responsibility", "/责任", "/痛苦", "/后悔", "/repair")),
    ("language", "语言感知、语义地图、内言语、表达计划", ("/language", "/语言")),
    ("cognition", "工作区、预测、采样、写门", ("/cognition", "/认知")),
    ("consciousness", "意识工作区、广播、元认知、可报告性", ("/consciousness", "/意识", "/workspace")),
    ("thinking", "自我思考、内言语、等待反思", ("/thinking", "/思考", "/inner-speech")),
    ("personality", "人格慢变量、性格收敛、自传栈", ("/personality", "/性格", "/人格", "/self")),
    ("ability", "能力面、出生准备、验收证据", ("/ability", "/能力")),
    ("perception", "视觉/感知、外周观察、世界接触", ("/vision", "/visual", "/perception", "/感知", "/视觉")),
    ("prediction", "预测、主动采样、世界接触和确认绑定", ("/prediction", "/预测", "/active-inference", "/world")),
    ("proactive_voice", "主动发话画像、释放状态、候选来源覆盖", ("/proactive", "/主动", "/voice")),
    ("features", "生命能力启用审计、disabled/缺证据检查", ("/features", "/功能", "/启用", "/audit-features")),
)

SLASH_INSPECTION_ALIASES = {
    alias.lower().lstrip("/"): category
    for category, _, aliases in (*SLASH_COMPOSITE_COMMANDS, *SLASH_STATE_COMMANDS)
    for alias in aliases
}
EMPTY_PREVIEW_TEXT = "暂无"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="digital")
    subparsers = parser.add_subparsers(dest="command", required=True)

    life = subparsers.add_parser(
        "life",
        help="Restore the digital life birth shell, first terminal turn, and terminal life loop.",
    )
    life.add_argument("--state", default="runtime/state")
    life.add_argument("--reports", default="runtime/reports/latest")
    life.add_argument("--receipts", default="runtime/receipts")
    life.add_argument("--run-id", default=None)
    life.add_argument("--strict", action="store_true")
    life.add_argument(
        "--background",
        action="store_true",
        help="Start the digital life process as a detached resident process.",
    )
    life.add_argument(
        "--resident",
        action="store_true",
        help="Run the resident process loop without treating stdin EOF as death.",
    )
    life.add_argument(
        "--status",
        action="store_true",
        help="Print a compact resident lifecycle status for the terminal.",
    )
    life.add_argument(
        "--stop",
        action="store_true",
        help="Ask the resident process to close itself through its lifecycle command file.",
    )
    life.add_argument(
        "--say",
        default=None,
        help="Send one relation turn to the resident process and print its response.",
    )
    life.add_argument(
        "--attach",
        action="store_true",
        help="Attach this terminal to the resident process, starting it first if needed.",
    )
    life.add_argument(
        "--foreground",
        action="store_true",
        help="Run the foreground process loop even when stdin is an interactive terminal.",
    )
    life.add_argument(
        "--json",
        action="store_true",
        help="Print the full machine-readable lifecycle JSON for --status or --stop.",
    )
    life.add_argument("--say-timeout-seconds", type=float, default=30.0)
    life.add_argument("--resident-sleep-seconds", type=float, default=5.0)
    life.add_argument("--stop-timeout-seconds", type=float, default=10.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "life":
        state_dir = Path(args.state)
        reports_dir = Path(args.reports)
        receipts_dir = Path(args.receipts)
        terminal_dir = state_dir / "terminal"
        if args.status:
            result = read_resident_lifecycle_status(
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
            )
            print(_format_lifecycle_output(result.state, action="status", full=args.json))
            return result.exit_code
        if args.stop:
            result = request_resident_stop(
                terminal_dir=terminal_dir,
                timeout_seconds=args.stop_timeout_seconds,
            )
            print(_format_lifecycle_output(result.state, action="stop", full=args.json))
            return result.exit_code
        if args.say is not None:
            expanded_say = expand_file_references_for_relation_turn(
                args.say,
                repo_root=Path.cwd(),
            )
            result = send_resident_relation_turn(
                terminal_dir=terminal_dir,
                utterance=expanded_say.utterance,
                wait_timeout_seconds=args.say_timeout_seconds,
            )
            if result.state.get("send_status") == "resident_not_active":
                start_result = start_background_resident_process(
                    state_dir=state_dir,
                    reports_dir=reports_dir,
                    receipts_dir=receipts_dir,
                    run_id=args.run_id,
                    strict=args.strict,
                    resident_sleep_seconds=args.resident_sleep_seconds,
                    cwd=Path.cwd(),
                )
                if start_result.exit_code == 0:
                    result = send_resident_relation_turn(
                        terminal_dir=terminal_dir,
                        utterance=expanded_say.utterance,
                        wait_timeout_seconds=args.say_timeout_seconds,
                    )
            response_text = result.state.get("response_text")
            if response_text:
                print(response_text)
            elif args.json:
                print(
                    json.dumps(
                        _format_relation_send_unreleased_output(result.state),
                        ensure_ascii=False,
                        indent=2,
                    )
                )
            return result.exit_code

        if args.background:
            result = start_background_resident_process(
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                run_id=args.run_id,
                strict=args.strict,
                resident_sleep_seconds=args.resident_sleep_seconds,
                cwd=Path.cwd(),
            )
            print(json.dumps(result.state, ensure_ascii=False, indent=2))
            return result.exit_code
        if _should_attach_resident(args):
            return run_resident_terminal_client(
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                run_id=args.run_id,
                strict=args.strict,
                resident_sleep_seconds=args.resident_sleep_seconds,
                say_timeout_seconds=args.say_timeout_seconds,
            )

        bootstrap_exit = ensure_minimal_digital_life_runtime(
            docs_dir=Path("docs"),
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=args.run_id,
            strict=args.strict,
        )
        if bootstrap_exit != 0:
            return bootstrap_exit
        resident_lifecycle_run_id = args.run_id or _bootstrap_run_id(None, "resident")
        input_stream = None
        if args.resident:
            mark_resident_lifecycle_active(
                terminal_dir=terminal_dir,
                run_id=resident_lifecycle_run_id,
                resident_sleep_seconds=args.resident_sleep_seconds,
            )
            input_stream = ResidentControlInputStream(
                terminal_dir=terminal_dir,
                min_poll_seconds=args.resident_sleep_seconds,
            )
        result = run_digital_life_process(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=resident_lifecycle_run_id if args.resident else args.run_id,
            strict=args.strict,
            input_stream=input_stream,
        )
        if args.resident:
            mark_resident_lifecycle_stopped(
                terminal_dir=terminal_dir,
                run_id=resident_lifecycle_run_id,
                exit_code=result.exit_code,
            )
        return result.exit_code

    parser.error(f"unsupported command: {args.command}")
    return 5


def run_resident_terminal_client(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None,
    strict: bool,
    resident_sleep_seconds: float,
    say_timeout_seconds: float,
) -> int:
    terminal_dir = state_dir / "terminal"
    start_result = start_background_resident_process(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=run_id,
        strict=strict,
        resident_sleep_seconds=resident_sleep_seconds,
        cwd=Path.cwd(),
    )
    if start_result.exit_code != 0:
        print(json.dumps(start_result.state, ensure_ascii=False, indent=2))
        return start_result.exit_code

    life_name = str(start_result.state.get("life_name") or "").strip() or None
    if sys.stdin.isatty():
        write_terminal_input_profile(
            terminal_dir=terminal_dir,
            profile=build_terminal_input_profile(
                input_stream=sys.stdin,
                idle_voice_interval_seconds=90.0,
            ),
        )
        return _run_interactive_resident_terminal_client(
            terminal_dir=terminal_dir,
            life_name=life_name,
            say_timeout_seconds=say_timeout_seconds,
        )

    print(
        render_digital_life_banner(
            life_name=life_name,
            status=str(start_result.state.get("status") or "resident"),
        )
    )
    print(render_life_opening(start_result.state, life_name=life_name))

    pipe_terminal_session_id = _ensure_pipe_terminal_session(
        terminal_dir=terminal_dir,
        life_name=life_name,
    )
    for raw_line in sys.stdin:
        utterance = raw_line.rstrip("\n")
        exit_code = _handle_resident_terminal_utterance(
            terminal_dir=terminal_dir,
            utterance=utterance,
            life_name=life_name,
            say_timeout_seconds=say_timeout_seconds,
            terminal_session_id=pipe_terminal_session_id,
        )
        if exit_code is not None:
            return exit_code
    return 0


def _run_interactive_resident_terminal_client(
    *,
    terminal_dir: Path,
    life_name: str | None,
    say_timeout_seconds: float,
    read_line_fn: Callable[..., str] | None = None,
    idle_voice_interval_seconds: float = 90.0,
) -> int:
    def idle_voice_fn() -> bool:
        return _emit_resident_proactive_terminal_voice(
            terminal_dir=terminal_dir,
            life_name=life_name,
        )

    terminal_history: list[str] = []
    slash_completion_items = _build_terminal_slash_completion_items()

    def completion_provider(text: str, cursor_index: int):
        return build_terminal_completion_state(
            text,
            cursor_index=cursor_index,
            slash_commands=slash_completion_items,
            repo_root=Path.cwd(),
        )

    if read_line_fn is None and sys.stdin.isatty():
        def handle_utterance_for_tui(utterance: str) -> tuple[int | None, str]:
            output = StringIO()
            with redirect_stdout(output):
                exit_code = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance=utterance,
                    life_name=life_name,
                    say_timeout_seconds=say_timeout_seconds,
                    record_terminal_transcript=False,
                )
            rendered = output.getvalue()
            response = _plain_text_from_terminal_output(rendered)
            _append_terminal_history(terminal_history, utterance)
            return exit_code, response

        def idle_voice_for_tui() -> str | None:
            output = StringIO()
            with redirect_stdout(output):
                emitted = _emit_resident_proactive_terminal_voice(
                    terminal_dir=terminal_dir,
                    life_name=life_name,
                )
            if not emitted:
                return None
            return _plain_text_from_terminal_output(output.getvalue())

        if not prompt_toolkit_available():
            print(
                "prompt_toolkit is required for the interactive terminal. "
                "Run `uv sync` in this project and start Adam again.",
                file=sys.stderr,
            )
            return 5
        return run_prompt_toolkit_terminal_app(
            terminal_dir=terminal_dir,
            life_name=life_name,
            handle_utterance=handle_utterance_for_tui,
            slash_commands=slash_completion_items,
            idle_voice_fn=idle_voice_for_tui,
            repo_root=Path.cwd(),
        )

    session_event = start_terminal_session_transcript(
        terminal_dir=terminal_dir,
        life_name=life_name,
    )
    terminal_session_id = str(session_event.get("session_id") or "")
    while True:
        try:
            prompt = render_input_prompt(life_name=life_name)
            if read_line_fn is None:
                print(
                    "prompt_toolkit interactive terminal is required for TTY input.",
                    file=sys.stderr,
                )
                return 5
            utterance = read_line_fn(
                prompt=prompt,
                idle_voice_fn=idle_voice_fn,
                completion_provider=completion_provider,
            )
        except KeyboardInterrupt:
            print()
            return 130
        except EOFError:
            print()
            return 0
        exit_code = _handle_resident_terminal_utterance(
            terminal_dir=terminal_dir,
            utterance=utterance,
            life_name=life_name,
            say_timeout_seconds=say_timeout_seconds,
            terminal_session_id=terminal_session_id,
        )
        _append_terminal_history(terminal_history, utterance)
        if exit_code is not None:
            return exit_code


def _handle_resident_terminal_utterance(
    *,
    terminal_dir: Path,
    utterance: str,
    life_name: str | None,
    say_timeout_seconds: float,
    terminal_session_id: str | None = None,
    record_terminal_transcript: bool = True,
) -> int | None:
    command = utterance.strip().lower()
    if not utterance.strip():
        return None
    session_id = terminal_session_id or ""
    if record_terminal_transcript:
        session_id = _ensure_pipe_terminal_session(
            terminal_dir=terminal_dir,
            life_name=life_name,
            existing_session_id=session_id,
        )
        append_terminal_session_event(
            terminal_dir=terminal_dir,
            session_id=session_id,
            event_kind="command" if command.startswith("/") else "relation_utterance",
            speaker="command" if command.startswith("/") else "relation",
            text=utterance,
            life_name=life_name,
        )
    if command in {"/help", "/commands"}:
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="终端命令",
            text=_render_slash_help_text(),
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    if command.startswith("/resume"):
        resume_text = render_resume_transcript(
            terminal_dir=terminal_dir,
            session_count=_resume_session_count(command),
            event_limit=160,
        )
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="会话恢复",
            text=resume_text,
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    if command in {"/all", "/snapshot", "/inspect-all", "/全部", "/总览"}:
        inspection = _build_resident_state_inspection_bundle(
            terminal_dir=terminal_dir,
        )
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="状态总览",
            text=_render_state_inspection_bundle_for_terminal(inspection),
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    if command in {"/features", "/feature", "/启用", "/功能", "/audit-features"}:
        audit = build_life_feature_audit(
            state_dir=terminal_dir.parent,
            reports_dir=terminal_dir.parent.parent / "reports" / "latest",
        )
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="功能启用审计",
            text=_render_generic_mapping_for_terminal(audit),
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    if _is_web_dream_toggle_command(command):
        result = _handle_web_dream_toggle_command(
            terminal_dir=terminal_dir,
            command=command,
        )
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="网页梦境学习",
            text=_render_web_dream_toggle_for_terminal(result),
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    if command in {"/clear", "/cls"}:
        print("\033[2J\033[H", end="")
        return None
    if _is_state_inspection_command(command):
        slash_command, want_json = _parse_slash_command(command)
        inspection = _build_state_inspection_for_command(
            terminal_dir=terminal_dir,
            command=slash_command,
        )
        rendered = (
            json.dumps(inspection, ensure_ascii=False, indent=2)
            if want_json
            else _render_state_inspection_for_terminal(inspection)
        )
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="状态查看",
            text=rendered,
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    if command in {"/exit", "/quit"}:
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="终端连接",
            text=(
                "终端连接已离开。\n"
                "常驻过程保持存在；记忆、会话记录和状态继续保存在 runtime/state。\n"
                "以后可以直接输入 Adam 重新连接。"
            ),
            record_terminal_transcript=record_terminal_transcript,
        )
        return 0
    if command in {"/stop", "/shutdown"}:
        stop_result = request_resident_stop(
            terminal_dir=terminal_dir,
            timeout_seconds=30.0,
        )
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="Digital Life",
            text=_render_lifecycle_summary_for_terminal(
                _lifecycle_terminal_summary(stop_result.state, action="stop")
            ),
            record_terminal_transcript=record_terminal_transcript,
        )
        return stop_result.exit_code
    if command.startswith("/"):
        _print_command_result(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            title="终端命令",
            text="未识别这个 / 命令。输入 /help 查看当前终端可用的状态查看和控制命令。",
            record_terminal_transcript=record_terminal_transcript,
        )
        return None
    expanded = expand_file_references_for_relation_turn(
        utterance,
        repo_root=Path.cwd(),
    )
    turn_result = send_resident_relation_turn(
        terminal_dir=terminal_dir,
        utterance=expanded.utterance,
        wait_timeout_seconds=say_timeout_seconds,
    )
    response_text = turn_result.state.get("response_text")
    if response_text:
        print(render_dialogue_box(life_name or "Digital Life", str(response_text)))
        if record_terminal_transcript:
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=session_id,
                event_kind="life_response",
                speaker="life",
                text=str(response_text),
                life_name=life_name,
            )
    elif turn_result.exit_code != 0:
        return turn_result.exit_code
    return None


def _emit_resident_proactive_terminal_voice(
    *,
    terminal_dir: Path,
    life_name: str | None,
    now_iso=None,
    model_transport: ModelExpressionTransport | None = None,
    environ: dict[str, str] | None = None,
) -> bool:
    event = build_resident_proactive_terminal_event(
        terminal_dir=terminal_dir,
        life_name=life_name,
        now_iso=now_iso or _now_iso,
    )
    proactive_profile = event.get("proactive_voice_profile") or {}
    release_constraints = list(proactive_profile.get("release_constraints", []))
    if (
        event.get("proactive_release_threshold") == "elevated"
        and "hold_proactive_voice_until_body_recovery" in release_constraints
    ):
        written = write_resident_proactive_terminal_event(
            terminal_dir=terminal_dir,
            event=event,
        )
        return False
    state_root = terminal_dir.parent
    generated_at = str(event.get("generated_at") or _now_iso())
    model_result = compose_model_expression(
        run_id="resident-proactive-" + str(event.get("composition_fingerprint") or "event"),
        generated_at=generated_at,
        external_utterance="open_terminal_idle",
        audited_expression_material=json.dumps(
            {
                key: value
                for key, value in event.items()
                if key not in {"utterance"}
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        language_dir=state_root / "language",
        reports_dir=state_root.parent / "reports" / "latest",
        terminal_life_loop_state=_read_runtime_json(
            terminal_dir / "terminal_life_loop_state.json"
        ),
        relationship_memory=_read_runtime_json(
            state_root / "memory" / "relationship_memory.json"
        ),
        dialogue_memory_summary=_read_runtime_json(
            state_root / "memory" / "dialogue_memory_summary.json"
        ),
        memory_retrieval_frame=_read_runtime_json(
            state_root / "memory" / "memory_retrieval_frame.json"
        ),
        repo_root=Path.cwd(),
        environ=environ,
        transport=model_transport,
        write_json=_write_runtime_json,
    )
    release_path = str(model_result.state.get("expression_release_path") or "")
    post_gate_status = str(model_result.state.get("post_expression_gate_status") or "")
    model_status = str(model_result.state.get("model_expression_status") or "")
    proactive_utterance = ""
    if (
        release_path == "model_expression"
        and post_gate_status == "accepted"
        and model_status == "model_expression_applied"
    ):
        proactive_utterance = model_result.response_text
    event["utterance"] = proactive_utterance
    event["model_expression_status"] = (
        "model_expression_applied"
        if proactive_utterance
        else "model_expression_unreleased"
    )
    event["source_model_expression_status"] = model_result.state.get(
        "model_expression_status"
    )
    event["model_expression_state_ref"] = model_result.state_ref
    event["model_expression_report_ref"] = model_result.report_ref
    event["post_expression_gate_status"] = (
        "blocked"
        if not proactive_utterance
        and release_path != "model_expression"
        and model_result.state.get("pre_fallback_candidate_text")
        else model_result.state.get("post_expression_gate_status")
    )
    event["expression_release_path"] = model_result.state.get("expression_release_path")
    event["expression_release_tier"] = model_result.state.get("expression_release_tier")
    written = write_resident_proactive_terminal_event(
        terminal_dir=terminal_dir,
        event=event,
    )
    utterance = str(written.get("utterance") or "").strip()
    if not utterance:
        return False
    print(render_dialogue_box(life_name or "Digital Life", utterance))
    return True


def _render_slash_help_text() -> str:
    lines = [
        "/help /commands 查看这张命令表",
        "/all /snapshot 查看所有生命状态检查面",
        "/resume [数量] 查看过往终端会话记录；只读显示，不塞入当前模型上下文",
        "/features 查看各生命能力是否真实启用",
        "/dream-web on 开启网页梦境学习",
        "/dream-web off 关闭网页梦境学习",
        "/dream-web status 查看网页梦境学习开关与最近状态",
        "任意状态命令可加 --json 输出完整机器可读证据树，例如 /memory --json",
        "",
        "日常合成检查（人话摘要，推荐优先）：",
    ]
    for _, description, aliases in SLASH_COMPOSITE_COMMANDS:
        primary = aliases[0]
        alias_text = " ".join(aliases[1:3])
        if alias_text:
            lines.append(f"{primary} ({alias_text}) {description}")
        else:
            lines.append(f"{primary} {description}")
    lines.append("")
    lines.append("分域检查（默认人话；部分域仍偏技术字段）：")
    for _, description, aliases in SLASH_STATE_COMMANDS:
        primary = aliases[0]
        alias_text = " ".join(aliases[1:4])
        if alias_text:
            lines.append(f"{primary} ({alias_text}) {description}")
        else:
            lines.append(f"{primary} {description}")
    lines.extend(
        [
            "/clear 清屏但不影响常驻过程",
            "/exit 离开当前终端，常驻过程继续睡眠、回忆、思考、成长、学习",
            "/stop 请求常驻过程通过正常 closeout 收口",
        ]
    )
    return "\n".join(lines)


def _render_state_inspection_bundle_for_terminal(bundle: dict[str, object]) -> str:
    inspections = bundle.get("inspections")
    if not isinstance(inspections, dict):
        return _render_generic_mapping_for_terminal(bundle)
    lines = ["状态总览："]
    for category, inspection in inspections.items():
        if not isinstance(inspection, dict):
            continue
        summary = _render_state_inspection_for_terminal(inspection, compact=True)
        if summary:
            lines.append(f"- {category}: {summary.splitlines()[0]}")
    lines.append("")
    lines.append("详情：")
    lines.extend(
        _render_state_inspection_for_terminal(bundle, compact=False).splitlines()
    )
    return "\n".join(lines).strip()


def _render_state_inspection_for_terminal(
    inspection: dict[str, object],
    *,
    compact: bool = False,
) -> str:
    if not isinstance(inspection, dict):
        return str(inspection)
    category = str(inspection.get("category") or "state")
    payload = inspection.get(category)
    if not isinstance(payload, dict):
        return _render_generic_mapping_for_terminal(inspection)
    if category == "memory":
        return _render_memory_inspection_for_terminal(payload, compact=compact)
    if category == "emotion":
        return _render_emotion_inspection_for_terminal(payload, compact=compact)
    if category == "dream":
        return _render_dream_inspection_for_terminal(payload, compact=compact)
    if category == "relationship":
        return _render_relationship_inspection_for_terminal(payload, compact=compact)
    if category == "state":
        return _render_state_overview_for_terminal(payload, compact=compact)
    if category in COMPOSITE_CATEGORIES:
        return _render_composite_inspection_for_terminal(
            category,
            payload,
            compact=compact,
        )
    summary = _render_generic_mapping_for_terminal(payload)
    if compact:
        return summary.splitlines()[0] if summary else ""
    return _append_evidence_preview(summary, payload)


def _render_memory_inspection_for_terminal(
    memory: dict[str, object],
    *,
    compact: bool,
) -> str:
    relationship_memory = memory.get("relationship_memory")
    relationship_memory = _inspection_value(relationship_memory)
    if not isinstance(relationship_memory, dict):
        relationship_memory = {}
    relation_profile = relationship_memory.get("relation_person_profile")
    if not isinstance(relation_profile, dict):
        relation_profile = {}
    observed_names = relation_profile.get("observed_names")
    if not isinstance(observed_names, list):
        observed_names = []
    lines = [
        "记忆：",
        f"  关系对象名字: {', '.join(str(item) for item in observed_names[:5]) or '暂无'}",
        f"  记忆写门: {str(_nested_value(memory, ['memory_write_gate', 'status']) or 'unknown')}",
        f"  写门策略: {str(_nested_value(memory, ['memory_write_gate', 'stage_policy']) or 'unknown')}",
        f"  写入偏置: {str(_nested_value(memory, ['memory_write_gate', 'body_signal_write_modulation', 'write_bias']) or 'unknown')}",
        f"  记忆召回: {str(_nested_value(memory, ['memory_retrieval', 'retrieval_mode']) or 'unknown')}",
        f"  关系主题: {', '.join(str(item) for item in _list_value(relationship_memory.get('relationship_theme_tags'))[:5]) or '暂无'}",
        f"  下次唤回线索: {', '.join(str(item) for item in _list_value(relationship_memory.get('next_wake_cues'))[:5]) or '暂无'}",
        f"  salient_core_memory_refs: {', '.join(str(item) for item in _list_value(relationship_memory.get('salient_core_memory_refs'))[:3]) or '暂无'}",
        f"  retrievable_context_memory_refs: {', '.join(str(item) for item in _list_value(relationship_memory.get('retrievable_context_memory_refs'))[:3]) or '暂无'}",
        f"  deep_sediment_memory_refs: {', '.join(str(item) for item in _list_value(relationship_memory.get('deep_sediment_memory_refs'))[:3]) or '暂无'}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return _append_evidence_preview("\n".join(lines), memory)


def _render_emotion_inspection_for_terminal(
    emotion: dict[str, object],
    *,
    compact: bool,
) -> str:
    core = emotion.get("core_affect_vector")
    core = _inspection_value(core)
    if not isinstance(core, dict):
        core = {}
    affective_episode = emotion.get("affective_episode")
    affective_episode = _inspection_value(affective_episode)
    if not isinstance(affective_episode, dict):
        affective_episode = {}
    emotion_regulation = emotion.get("emotion_regulation_loop")
    emotion_regulation = _inspection_value(emotion_regulation)
    if not isinstance(emotion_regulation, dict):
        emotion_regulation = {}
    lines = [
        "情绪：",
        f"  核心效价: {str(core.get('valence') or 'unknown')}",
        f"  核心唤醒: {str(core.get('arousal') or 'unknown')}",
        f"  修复驱动: {str(core.get('repair_drive') or 'unknown')}",
        f"  情绪片段: {str(affective_episode.get('episode_label') or 'unknown')}",
        f"  调节方式: {str(emotion_regulation.get('regulation_mode') or 'unknown')}",
        f"  痛苦/后悔报告: {str(_nested_value(emotion, ['pain_regret_repair_report', 'repair_followup_required']) or 'unknown')}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return _append_evidence_preview("\n".join(lines), emotion)


def _render_dream_inspection_for_terminal(
    dream: dict[str, object],
    *,
    compact: bool,
) -> str:
    web = dream.get("web_dream_learning_state")
    web = _inspection_value(web)
    if not isinstance(web, dict):
        web = {}
    dream_window = dream.get("dream_experience_window")
    dream_window = _inspection_value(dream_window)
    if not isinstance(dream_window, dict):
        dream_window = {}
    fact_gate = dream.get("dream_fact_gate_decision")
    fact_gate = _inspection_value(fact_gate)
    if not isinstance(fact_gate, dict):
        fact_gate = {}
    lines = [
        "梦境：",
        f"  网页梦境状态: {str(web.get('status') or 'unknown')}",
        f"  最近页面: {str(web.get('page_title') or '暂无')}",
        f"  梦境窗口: {str(dream_window.get('window_kind') or 'unknown')}",
        f"  允许写入: {', '.join(str(item) for item in _list_value(fact_gate.get('allowed_writes'))[:5]) or '暂无'}",
        f"  阻断写入: {', '.join(str(item) for item in _list_value(fact_gate.get('blocked_writes'))[:5]) or '暂无'}",
        f"  唤回线索: {str(_nested_value(dream, ['exit_dream_consolidation_summary', 'next_wake_memory_cue_refs']) or '暂无')}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return _append_evidence_preview("\n".join(lines), dream)


def _render_relationship_inspection_for_terminal(
    relationship: dict[str, object],
    *,
    compact: bool,
) -> str:
    subject_graph = relationship.get("relationship_subject_graph")
    subject_graph = _inspection_value(subject_graph)
    if not isinstance(subject_graph, dict):
        subject_graph = {}
    continuity_reports = _list_value(
        _nested_value(relationship, ["relationship_timeline", "relationship_continuity_reports"])
    )
    continuity_state = "unknown"
    if continuity_reports and isinstance(continuity_reports[0], dict):
        continuity_state = str(continuity_reports[0].get("continuity_state") or "unknown")
    lines = [
        "关系：",
        f"  当前阶段: {str(_nested_value(relationship, ['relationship_timeline', 'relationship_stage']) or _nested_value(relationship, ['relationship_timeline', 'status']) or 'unknown')}",
        f"  连续状态: {str(_nested_value(relationship, ['relationship_timeline', 'continuity_state']) or continuity_state)}",
        f"  关系对象名字: {', '.join(str(item) for item in _list_value(_nested_value(relationship, ['relationship_memory', 'relation_person_profile', 'observed_names']))[:5]) or '暂无'}",
        f"  共同主题: {', '.join(str(item) for item in _list_value(_nested_value(relationship, ['relationship_memory', 'relationship_theme_tags']))[:5]) or '暂无'}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return _append_evidence_preview("\n".join(lines), relationship)


def _render_state_overview_for_terminal(
    state: dict[str, object],
    *,
    compact: bool,
) -> str:
    lines = [
        "状态：",
        f"  生命周期: {str(_nested_value(state, ['resident_lifecycle_state', 'status']) or 'unknown')}",
        f"  常驻过程: {str(_nested_value(state, ['digital_life_process_report', 'status']) or 'unknown')}",
        f"  治理阶段: {str(_nested_value(state, ['resident_governance_state', 'governance_phase']) or _nested_value(state, ['resident_continuity_summary', 'governance_phase']) or 'unknown')}",
        f"  下次动作: {str(_nested_value(state, ['terminal_life_loop_state', 'next_required_action']) or 'unknown')}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return _append_evidence_preview("\n".join(lines), state)


def _render_composite_inspection_for_terminal(
    category: str,
    payload: dict[str, object],
    *,
    compact: bool,
) -> str:
    renderers = {
        "me": _render_me_inspection_for_terminal,
        "turn": _render_turn_inspection_for_terminal,
        "recall": _render_recall_inspection_for_terminal,
        "express": _render_express_inspection_for_terminal,
        "carry": _render_carry_inspection_for_terminal,
        "background": _render_background_inspection_for_terminal,
        "converge": _render_converge_inspection_for_terminal,
    }
    renderer = renderers.get(category)
    if renderer is None:
        return _render_generic_mapping_for_terminal(payload)
    return renderer(payload, compact=compact)


def _render_me_inspection_for_terminal(
    me: dict[str, object],
    *,
    compact: bool,
) -> str:
    lines = [
        "我是谁：",
        f"  生命名: {str(me.get('life_name') or 'unknown')}",
        f"  生命周期: {str(me.get('lifecycle_status') or 'unknown')}",
        f"  等待姿态: {str(me.get('waiting_mode') or 'unknown')}",
        f"  关系阶段: {str(me.get('relationship_stage') or 'unknown')}",
        f"  语义焦点: {str(me.get('semantic_focus') or '暂无')}",
        f"  表达姿态: {str(me.get('expression_posture') or 'unknown')}",
        f"  模型表达: {str(me.get('model_expression_status') or 'unknown')}",
        f"  记忆召回模式: {str(me.get('memory_recall_mode') or 'unknown')}",
        f"  梦境残留: {'有' if me.get('dream_residue_present') else '无'}",
        f"  主动发话: {str(me.get('proactive_status') or 'unknown')}",
        f"  下次动作: {str(me.get('next_required_action') or 'unknown')}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip() + " " + lines[3].strip()
    notes = me.get("honest_notes")
    if isinstance(notes, list) and notes:
        lines.append("  诚实说明:")
        lines.extend(f"    - {note}" for note in notes[:3])
    return "\n".join(lines)


def _render_turn_inspection_for_terminal(
    turn: dict[str, object],
    *,
    compact: bool,
) -> str:
    recall_refs = turn.get("memory_recall_refs")
    recall_preview = ", ".join(str(item) for item in _list_value(recall_refs)[:3]) or "暂无"
    lines = [
        "上一回合：",
        f"  语义焦点: {str(turn.get('semantic_focus') or '暂无')}",
        f"  你刚说的话: {_preview_text(turn.get('last_external_utterance'), 80)}",
        f"  生命刚回的话: {_preview_text(turn.get('last_life_utterance'), 80)}",
        f"  记忆召回引用: {recall_preview}",
        f"  表达目标: {str(turn.get('expression_goal') or 'unknown')}",
        f"  表达监视: {str(turn.get('expression_monitor_status') or 'unknown')}",
        f"  模型表达: {str(turn.get('model_expression_status') or 'unknown')}",
        f"  表达门: {str(turn.get('post_expression_gate_status') or 'unknown')}",
        f"  释放路径: {str(turn.get('expression_release_path') or 'unknown')}",
        f"  释放层级: {str(turn.get('expression_release_tier') or 'unknown')}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    flags = turn.get("missing_evidence_flags")
    if isinstance(flags, list) and flags:
        lines.append(f"  缺证据标记: {', '.join(str(item) for item in flags[:5])}")
    return "\n".join(lines)


def _render_recall_inspection_for_terminal(
    recall: dict[str, object],
    *,
    compact: bool,
) -> str:
    activated = recall.get("activated_engram_refs")
    activated_preview = ", ".join(str(item) for item in _list_value(activated)[:3]) or "暂无"
    cues = recall.get("cue_terms")
    cue_preview = ", ".join(str(item) for item in _list_value(cues)[:5]) or "暂无"
    lines = [
        "记忆召回：",
        f"  检索模式: {str(recall.get('retrieval_mode') or 'unknown')}",
        f"  线索词: {cue_preview}",
        f"  激活印迹: {activated_preview}",
        f"  重建焦点: {str(recall.get('reconstruction_focus') or '暂无')}",
        f"  已进入语义地图: {'是' if recall.get('recall_reached_semantic_map') else '否'}",
        f"  已进入表达计划: {'是' if recall.get('recall_reached_expression_plan') else '否'}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return "\n".join(lines)


def _render_express_inspection_for_terminal(
    express: dict[str, object],
    *,
    compact: bool,
) -> str:
    can_speak = express.get("can_speak_naturally")
    lines = [
        "表达释放：",
        f"  语义目标: {str(express.get('semantic_goal') or '暂无')}",
        f"  节奏模式: {str(express.get('expression_tempo_mode') or 'unknown')}",
        f"  释放谨慎度: {str(express.get('release_caution_level') or 'unknown')}",
        f"  监视决策: {str(express.get('delay_or_release_decision') or 'unknown')}",
        f"  模型表达: {str(express.get('model_expression_status') or 'unknown')}",
        f"  表达门: {str(express.get('post_expression_gate_status') or 'unknown')}",
        f"  此刻能自然说话: {'能' if can_speak else '不能'}",
    ]
    if compact:
        return lines[0] + " " + lines[-1].strip()
    flags = express.get("missing_evidence_flags")
    if isinstance(flags, list) and flags:
        lines.append(f"  缺证据: {', '.join(str(item) for item in flags[:5])}")
    return "\n".join(lines)


def _render_carry_inspection_for_terminal(
    carry: dict[str, object],
    *,
    compact: bool,
) -> str:
    shared = carry.get("shared_term_surfaces")
    shared_preview = ", ".join(str(item) for item in _list_value(shared)[:5]) or "暂无"
    lines = [
        "跨唤醒携带：",
        f"  关系角色: {str(carry.get('relation_role') or 'unknown')}",
        f"  关系阶段: {str(carry.get('relationship_stage') or 'unknown')}",
        f"  语义焦点: {str(carry.get('semantic_focus') or '暂无')}",
        f"  共享词面: {shared_preview}",
        f"  时间线恢复引用: {len(_list_value(carry.get('relationship_timeline_restore_refs')))} 条",
        f"  承诺表达恢复: {len(_list_value(carry.get('commitment_expression_restore_refs')))} 条",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    return "\n".join(lines)


def _render_background_inspection_for_terminal(
    background: dict[str, object],
    *,
    compact: bool,
) -> str:
    kinds = background.get("covered_activity_kinds")
    kind_preview = ", ".join(str(item) for item in _list_value(kinds)[:6]) or "暂无"
    lines = [
        "后台活动：",
        f"  活动计数: {str(background.get('activity_count') or 'unknown')}",
        f"  已覆盖种类: {kind_preview}",
        f"  周期覆盖完整: {'是' if background.get('cycle_coverage_complete') else '否'}",
        f"  思考模式: {str(background.get('thinking_mode') or 'unknown')}",
        f"  思考状态: {str(background.get('thinking_status') or 'unknown')}",
        f"  主动发话: {str(background.get('proactive_status') or 'unknown')}",
        f"  网页梦境: {str(background.get('web_dream_status') or 'unknown')}",
    ]
    if compact:
        return lines[0] + " " + lines[1].strip()
    note = background.get("thinking_honest_note")
    if note:
        lines.append(f"  说明: {note}")
    return "\n".join(lines)


def _render_converge_inspection_for_terminal(
    converge: dict[str, object],
    *,
    compact: bool,
) -> str:
    traits = converge.get("trait_slow_variables")
    trait_preview = ", ".join(str(item) for item in _list_value(traits)[:4]) or "暂无"
    lines = [
        "慢收敛：",
        f"  性格慢变量: {trait_preview}",
        f"  共享词晋升数: {str(converge.get('promoted_shared_term_count') or converge.get('shared_term_promotion_count') or '0')}",
        f"  表达节奏: {str(converge.get('expression_tempo_mode') or 'unknown')}",
        f"  节奏历史条数: {str(converge.get('tempo_history_count') or '0')}",
    ]
    if compact:
        return lines[0] + " " + lines[2].strip()
    return "\n".join(lines)


def _append_evidence_preview(summary: str, payload: dict[str, object]) -> str:
    evidence_lines = _evidence_preview_lines(payload)
    if not evidence_lines:
        return summary
    return "\n".join([summary, "  关键证据:", *evidence_lines])


def _evidence_preview_lines(
    value: object,
    *,
    prefix: str = "",
    depth: int = 0,
    limit: int = 32,
) -> list[str]:
    if depth > 3 or limit <= 0:
        return []
    value = _inspection_value(value)
    lines: list[str] = []
    if isinstance(value, dict):
        items = sorted(
            value.items(),
            key=lambda pair: _evidence_preview_key_priority(
                str(pair[0]),
                top_level=depth == 0,
            ),
        )
        for key, item in items:
            if len(lines) >= limit:
                break
            key_text = f"{prefix}.{key}" if prefix else str(key)
            item_value = _inspection_value(item)
            if isinstance(item_value, dict) and (
                str(key).endswith("_summary") or str(key).endswith("_profile")
            ):
                lines.extend(
                    _evidence_preview_lines(
                        item_value,
                        prefix=key_text,
                        depth=depth + 1,
                        limit=limit - len(lines),
                    )
                )
                continue
            if _is_evidence_preview_key(str(key)):
                lines.append(
                    f"    {key_text}: {_preview_evidence_value(item_value)}"
                )
                continue
            if isinstance(item_value, dict):
                lines.extend(
                    _evidence_preview_lines(
                        item_value,
                        prefix=key_text,
                        depth=depth + 1,
                        limit=limit - len(lines),
                    )
                )
    return lines[:limit]


def _evidence_preview_key_priority(key: str, *, top_level: bool = False) -> int:
    if top_level and (
        key.endswith("_summary")
        or key.endswith("_summary_view")
        or key.endswith("_profile")
    ):
        return -1
    if key in {"schema_version", "summary_kind"}:
        return 0
    if key.endswith("_summary") or key.endswith("_profile"):
        return 1
    if key.endswith("_boundary"):
        return 2
    if key.endswith("_status") or key.endswith("_focus"):
        return 3
    if key.endswith("_mode") or key.endswith("_policy") or key.endswith("_bias"):
        return 4
    if key.endswith("_adjustments"):
        return 4
    if key.endswith("_refs") or key.endswith("_ref"):
        return 5
    return 6


def _is_evidence_preview_key(key: str) -> bool:
    return (
        key == "schema_version"
        or key == "summary_kind"
        or key.endswith("_summary")
        or key.endswith("_summary_kind")
        or key.endswith("_status")
        or key.endswith("_focus")
        or key.endswith("_mode")
        or key.endswith("_policy")
        or key.endswith("_boundary")
        or key.endswith("_bias")
        or key.endswith("_route")
        or key.endswith("_risk")
        or key.endswith("_refs")
        or key.endswith("_ref")
        or key.endswith("_candidates")
        or key.endswith("_targets")
        or key.endswith("_adjustments")
    )


def _preview_evidence_value(value: object) -> str:
    value = _inspection_value(value)
    if isinstance(value, list):
        preview = ", ".join(_preview_text(item, 80) for item in value[:5])
        if len(value) > 5:
            preview += f", ...({len(value)})"
        return preview or "[]"
    if isinstance(value, dict):
        items = list(value.items())
        preview = ", ".join(
            f"{key}={_preview_text(item, 60)}" for key, item in items[:5]
        )
        if len(items) > 5:
            preview += f", ...({len(items)})"
        return preview or "{}"
    return _preview_text(value, 180)


def _preview_text(value: object, limit: int) -> str:
    text = str(value or "").strip()
    if not text:
        return EMPTY_PREVIEW_TEXT
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _render_lifecycle_summary_for_terminal(summary: dict[str, object]) -> str:
    lines = [
        "停止结果：",
        f"  状态: {str(summary.get('status') or 'unknown')}",
        f"  生命名: {str(summary.get('life_name') or 'Adam')}",
        f"  常驻: {str(summary.get('persistent_process_status') or 'unknown')}",
        f"  下一动作: {str(summary.get('next_required_action') or 'unknown')}",
    ]
    return "\n".join(lines)


def _render_web_dream_toggle_for_terminal(result: dict[str, object]) -> str:
    lines = [
        "网页梦境学习：",
        f"  状态: {str(result.get('status') or 'unknown')}",
        f"  启用: {str(result.get('enabled'))}",
        f"  最近页面: {str(result.get('page_title') or '暂无')}",
    ]
    return "\n".join(lines)


def _render_generic_mapping_for_terminal(value: dict[str, object]) -> str:
    lines: list[str] = []
    for key, item in value.items():
        if isinstance(item, dict):
            preview = ", ".join(f"{k}={v}" for k, v in list(item.items())[:4])
            lines.append(f"{key}: {preview}" if preview else f"{key}:")
        elif isinstance(item, list):
            preview = ", ".join(str(v) for v in item[:5])
            lines.append(f"{key}: {preview}")
        else:
            lines.append(f"{key}: {item}")
    return "\n".join(lines) if lines else "{}"


def _nested_value(payload: dict[str, object], path: list[str]) -> object:
    current: object = payload
    for key in path:
        current = _inspection_value(current)
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _list_value(value: object) -> list[object]:
    value = _inspection_value(value)
    return value if isinstance(value, list) else []


def _inspection_value(value: object) -> object:
    if isinstance(value, dict) and "value" in value and "available" in value:
        return value.get("value")
    return value


def _ensure_pipe_terminal_session(
    *,
    terminal_dir: Path,
    life_name: str | None,
    existing_session_id: str | None = None,
) -> str:
    if existing_session_id:
        return existing_session_id
    event = start_terminal_session_transcript(
        terminal_dir=terminal_dir,
        life_name=life_name,
    )
    return str(event.get("session_id") or "")


def _print_command_result(
    *,
    terminal_dir: Path,
    session_id: str,
    life_name: str | None,
    title: str,
    text: str,
    record_terminal_transcript: bool,
) -> None:
    print(render_dialogue_box(title, text))
    if not record_terminal_transcript:
        return
    if session_id:
        append_terminal_session_event(
            terminal_dir=terminal_dir,
            session_id=session_id,
            event_kind="command_result",
            speaker="command_result",
            text=text,
            life_name=life_name,
            metadata={"title": title},
        )


def _resume_session_count(command: str) -> int:
    parts = str(command or "").split()
    if len(parts) < 2:
        return 3
    try:
        value = int(parts[1])
    except ValueError:
        return 3
    return max(1, min(value, 20))


def _build_terminal_slash_completion_items() -> tuple[tuple[str, str], ...]:
    items: list[tuple[str, str]] = [
        ("/me", "我是谁：生命名、等待姿态、关系与表达摘要"),
        ("/turn", "上一关系回合链路"),
        ("/recall", "记忆召回链路"),
        ("/express", "表达释放链路"),
        ("/carry", "跨唤醒携带"),
        ("/background", "后台自主活动"),
        ("/converge", "性格与语言慢收敛"),
        ("/state", "常驻状态、生命周期、等待心跳、终端输入"),
        ("/context", "关系上下文、语义焦点、回合累积"),
        ("/memory", "短期/长期记忆、召回、写门、沉淀层"),
        ("/dream", "梦境、离线整合、醒后整合、网页梦境学习"),
        ("/emotion", "情绪、痛苦压力、调节循环"),
        ("/relationship", "关系时间线、承诺、共同语言、关系阶段"),
        ("/body", "身体节律、资源预算、需要状态"),
        ("/personality", "人格慢变量、性格收敛、自传栈"),
        ("/consciousness", "意识工作区、广播、元认知、可报告性"),
        ("/language", "语言感知、语义地图、内言语、表达计划"),
    ]
    for _, description, aliases in SLASH_STATE_COMMANDS:
        for alias in aliases:
            items.append((alias, description))
    items.extend(
        [
            ("/thinking", "自我思考、内言语、等待反思"),
            ("/inner", "内环境、稳态、资源和调制压力"),
            ("/cognition", "工作区、预测、采样、写门"),
            ("/vision", "视觉/感知、外周观察、世界接触"),
            ("/growth", "成长、学习、自我修改候选、反遗忘回放"),
            ("/responsibility", "责任、痛苦、后悔、修复链"),
            ("/signal", "信号介质、调质、预测误差与释放偏置"),
            ("/membrane", "生命膜、事实门、边界与验证膜"),
            ("/ability", "能力面、出生准备、验收证据"),
            ("/prediction", "预测、主动采样、世界接触和确认绑定"),
            ("/proactive", "主动发话画像、释放状态、候选来源覆盖"),
            ("/dream-web", "网页梦境学习开关：/dream-web on|off|status"),
            ("/features", "查看生命能力启用审计"),
            ("/web-dream", "网页梦境学习开关：/web-dream on|off|status"),
            ("/dream-web on", "开启网页梦境学习"),
            ("/dream-web off", "关闭网页梦境学习"),
            ("/dream-web status", "查看网页梦境学习状态"),
            ("/resume", "查看过往终端会话记录，不注入当前上下文"),
            ("/resume 5", "查看最近 5 个终端会话记录"),
            ("/help", "查看终端命令"),
            ("/all", "状态总览"),
            ("/clear", "清空当前终端显示"),
            ("/exit", "离开当前终端，常驻过程继续存在"),
            ("/stop", "请求常驻过程正常停止"),
        ]
    )
    deduped: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, detail in items:
        key = label.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((label, detail))
    return tuple(deduped)


def _is_web_dream_toggle_command(command: str) -> bool:
    normalized = str(command or "").strip().lower()
    return normalized in {
        "/dream-web",
        "/dream-web on",
        "/dream-web off",
        "/dream-web status",
        "/dream-web 状态",
        "/web-dream",
        "/web-dream on",
        "/web-dream off",
        "/web-dream status",
        "/web-dream 状态",
        "/网页梦境",
        "/网页梦境 开",
        "/网页梦境 关",
        "/网页梦境 状态",
    }


def _handle_web_dream_toggle_command(
    *,
    terminal_dir: Path,
    command: str,
) -> dict[str, object]:
    normalized = str(command or "").strip().lower()
    state_dir = terminal_dir.parent
    if normalized in {
        "/dream-web",
        "/dream-web status",
        "/dream-web 状态",
        "/web-dream",
        "/web-dream status",
        "/web-dream 状态",
        "/网页梦境",
        "/网页梦境 状态",
    }:
        return _read_web_dream_toggle_status(state_dir=state_dir)
    enabled = normalized in {
        "/dream-web on",
        "/web-dream on",
        "/网页梦境 开",
    }
    return write_web_dream_learning_toggle(
        state_dir=state_dir,
        enabled=enabled,
        generated_at=_now_iso(),
    )


def _read_web_dream_toggle_status(*, state_dir: Path) -> dict[str, object]:
    seed_preview = build_web_dream_learning_effective_seed_preview(
        state_dir=state_dir,
    )
    state_payload = _read_runtime_json(
        state_dir / "dream" / "web_dream_learning_state.json"
    )
    return {
        "schema_version": "web_dream_learning_toggle_status_v1",
        "enabled": bool(seed_preview.get("enabled")),
        "configured_enabled": bool(seed_preview.get("configured_enabled")),
        "config_source": seed_preview.get("source"),
        "manual_toggle_state": (
            _read_runtime_json(
                state_dir / "dream" / "web_dream_learning_seeds.json"
            ).get("manual_toggle_state")
        ),
        "status": (
            "enabled_waiting_for_dream_cycle"
            if seed_preview.get("enabled")
            else "disabled"
        ),
        "last_learning_status": state_payload.get("status") or "not_recorded",
        "seed_count": seed_preview.get("seed_count"),
        "selected_url": state_payload.get("selected_url"),
        "page_title": state_payload.get("page_title"),
        "web_dream_learning_state_ref": (
            "runtime/state/dream/web_dream_learning_state.json"
        ),
        "web_dream_learning_seeds_ref": (
            "runtime/state/dream/web_dream_learning_seeds.json"
        ),
    }


def _parse_slash_command(command: str) -> tuple[str, bool]:
    parts = str(command or "").strip().lower().split()
    want_json = "--json" in parts
    cmd_parts = [part for part in parts if part != "--json"]
    return (cmd_parts[0] if cmd_parts else str(command or "").strip().lower(), want_json)


def _is_state_inspection_command(command: str) -> bool:
    slash_command, _ = _parse_slash_command(command)
    normalized = slash_command.lstrip("/")
    return (
        normalized in STATE_INSPECTION_CATEGORIES
        or normalized in SLASH_INSPECTION_ALIASES
        or normalized in COMPOSITE_CATEGORIES
    )


def _resolve_state_inspection_category(command: str) -> str:
    slash_command, _ = _parse_slash_command(command)
    normalized = slash_command.lstrip("/")
    return SLASH_INSPECTION_ALIASES.get(normalized, normalized)


def _build_state_inspection_for_command(
    *,
    terminal_dir: Path,
    command: str,
) -> dict[str, object]:
    category = _resolve_state_inspection_category(command)
    if category in COMPOSITE_CATEGORIES:
        return build_composite_state_inspection(
            terminal_dir=terminal_dir,
            category=category,
        )
    return build_resident_state_inspection(
        terminal_dir=terminal_dir,
        category=category,
    )


def _build_resident_state_inspection_bundle(
    *,
    terminal_dir: Path,
) -> dict[str, object]:
    composite_categories = [category for category, _, _ in SLASH_COMPOSITE_COMMANDS]
    ordered_categories = [category for category, _, _ in SLASH_STATE_COMMANDS]
    all_categories = composite_categories + ordered_categories
    return {
        "schema_version": "resident_state_inspection_bundle_v0",
        "inspection_scope": "terminal_view_only_not_relation_turn",
        "categories": all_categories,
        "inspections": {
            category: _build_state_inspection_for_command(
                terminal_dir=terminal_dir,
                command=f"/{category}",
            )
            for category in all_categories
        },
    }


def _append_terminal_history(history: list[str], utterance: str) -> None:
    text = str(utterance or "").strip()
    if not text:
        return
    if history and history[-1] == utterance:
        return
    history.append(utterance)
    del history[:-100]


def _plain_text_from_terminal_output(rendered: str) -> str:
    text = str(rendered or "").strip()
    if not text:
        return ""
    lines = text.splitlines()
    if len(lines) >= 2 and all((not line) or line.startswith("  ") for line in lines[1:]):
        return "\n".join(line[2:] if line.startswith("  ") else "" for line in lines[1:]).strip()
    return text


def _read_runtime_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_runtime_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _format_relation_send_unreleased_output(state: dict) -> dict:
    response_event = state.get("response_event")
    response_status = None
    if isinstance(response_event, dict):
        response_status = response_event.get("status")
    return {
        "schema_version": "resident_relation_send_result_v0",
        "send_status": state.get("send_status"),
        "response_status": response_status,
        "natural_language_released": False,
        "resident_lifecycle_state_ref": state.get("resident_lifecycle_state_ref"),
        "resident_relation_inbox_ref": state.get("resident_relation_inbox_ref"),
        "resident_relation_outbox_ref": state.get("resident_relation_outbox_ref"),
        "resident_relation_queue_state_ref": state.get(
            "resident_relation_queue_state_ref"
        ),
        "pid": state.get("pid"),
        "pid_alive": state.get("pid_alive"),
    }


def _should_attach_resident(args: argparse.Namespace) -> bool:
    if args.attach:
        return True
    if args.foreground or args.resident:
        return False
    return bool(sys.stdin.isatty())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _format_lifecycle_output(
    state: dict,
    *,
    action: str,
    full: bool,
) -> str:
    if full:
        return json.dumps(state, ensure_ascii=False, indent=2)
    return json.dumps(
        _lifecycle_terminal_summary(state, action=action),
        ensure_ascii=False,
        indent=2,
    )


def _lifecycle_terminal_summary(state: dict, *, action: str) -> dict:
    long_term = state.get("resident_long_term_residency_status") or {}
    summary = {
        "schema_version": "resident_lifecycle_terminal_summary_v0",
        "action": action,
        "status": state.get("status"),
        "run_id": state.get("run_id"),
        "pid": state.get("pid"),
        "pid_alive": state.get("pid_alive"),
        "life_name": state.get("life_name"),
        "life_name_id": state.get("life_name_id"),
        "life_name_lock_state": state.get("life_name_lock_state"),
        "residency_mode": state.get("residency_mode"),
        "residency_posture": state.get("residency_posture"),
        "relation_queue_status": state.get("resident_relation_queue_status"),
        "relation_last_completed_sequence": state.get(
            "resident_relation_last_completed_sequence"
        ),
        "autonomous_activity_count": state.get("resident_autonomous_activity_count"),
        "autonomous_activity_last_kind": state.get(
            "resident_autonomous_activity_last_kind"
        ),
        "autonomous_activity_cycle_completion_count": state.get(
            "resident_autonomous_activity_cycle_completion_count"
        ),
        "autonomous_activity_cycle_coverage_complete": state.get(
            "resident_autonomous_activity_cycle_coverage_complete"
        ),
        "autonomous_activity_next_kind": state.get(
            "resident_autonomous_activity_next_kind"
        ),
        "waiting_heartbeat_counter": state.get("resident_waiting_heartbeat_counter"),
        "waiting_mode": state.get("resident_waiting_mode"),
        "next_required_action": state.get("resident_next_required_action"),
        "governance_phase": state.get("resident_governance_phase"),
        "governance_attention_target": state.get(
            "resident_governance_attention_target"
        ),
        "idle_probe_mode": state.get("resident_idle_probe_mode"),
        "next_idle_action": state.get("resident_next_idle_action"),
        "heartbeat_interval_ms": state.get("resident_heartbeat_interval_ms"),
        "terminal_current_mode": state.get("resident_terminal_current_mode"),
        "resident_process_lease_state": state.get("resident_process_lease_state"),
        "resident_process_identity_continuity_state": state.get(
            "resident_process_identity_continuity_state"
        ),
        "resident_process_lease_history_event_count": state.get(
            "resident_process_lease_history_event_count"
        ),
        "persistent_process_status": state.get("resident_persistent_process_status")
        or long_term.get("persistent_process_status"),
        "background_convergence_state": state.get(
            "resident_background_convergence_state"
        )
        or long_term.get("background_convergence_state"),
        "background_convergence_pressure_level": state.get(
            "resident_background_convergence_pressure_level"
        )
        or long_term.get("background_convergence_pressure_level"),
        "evidence_refs": long_term.get("evidence_refs", []),
        "full_json_hint": "pass --json to print the complete lifecycle evidence tree",
    }
    return {key: value for key, value in summary.items() if value is not None}


def ensure_minimal_digital_life_runtime(
    *,
    docs_dir: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None,
    strict: bool,
) -> int:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    docs_dir = docs_dir.resolve()
    runtime_root = state_dir.parent
    doc_out = runtime_root / "docs"

    stage_explanation_report = reports_dir / "stage_explanation_report.json"
    if stage_explanation_report.exists():
        return 0

    doc_index_path = doc_out / "doc_carrier_index.json"
    direction_state = state_dir / "direction"
    authority_state = state_dir / "authority"
    neural_state = state_dir / "neural_life_core"
    membrane_state = state_dir / "membrane"
    life_targets_state = state_dir / "life_targets"
    validation_state = state_dir / "validation"
    observation_state = state_dir / "observation"
    schema_runner_state = state_dir / "schema_runner"

    steps = [
        lambda: run_doc_ingestion(
            docs_dir=docs_dir,
            out_dir=doc_out,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "ingest"),
            strict=strict,
        ),
        lambda: run_direction_lock(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            out_dir=direction_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "direction"),
            strict=strict,
        ),
        lambda: run_source_authority(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            direction_state_dir=direction_state,
            out_dir=authority_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "authority"),
            strict=strict,
        ),
        lambda: run_neural_life_core(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            authority_state_dir=authority_state,
            out_dir=neural_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "neural"),
            strict=strict,
        ),
        lambda: run_check_neural_life_core(
            state_dir=neural_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_state_store(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            neural_core_state_dir=neural_state,
            out_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "state"),
            strict=strict,
        ),
        lambda: run_check_state_store(
            state_dir=state_dir,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_life_membrane(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            direction_state_dir=direction_state,
            neural_core_state_dir=neural_state,
            state_dir=state_dir,
            out_dir=membrane_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "membrane"),
            strict=strict,
        ),
        lambda: run_check_life_membrane(
            membrane_dir=membrane_state,
            state_dir=state_dir,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_build_language_relationship(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            neural_core_state_dir=neural_state,
            state_dir=state_dir,
            membrane_dir=membrane_state,
            out_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "language"),
            strict=strict,
        ),
        lambda: run_check_language_relationship(
            state_dir=state_dir,
            membrane_dir=membrane_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_birth_readiness(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            direction_state_dir=direction_state,
            neural_core_state_dir=neural_state,
            state_dir=state_dir,
            membrane_dir=membrane_state,
            out_dir=life_targets_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "birth"),
            strict=strict,
        ),
        lambda: run_validation_membrane(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            membrane_dir=membrane_state,
            life_targets_dir=life_targets_state,
            validation_dir=validation_state,
            observation_dir=observation_state,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "validation"),
            strict=strict,
        ),
        lambda: run_check_validation_membrane(
            state_dir=state_dir,
            validation_dir=validation_state,
            observation_dir=observation_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_schema_runner(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "schema"),
            strict=strict,
        ),
        lambda: run_check_schema_runner(
            state_dir=schema_runner_state,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_schema_smoke(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "smoke"),
            strict=strict,
        ),
        lambda: run_life_support(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            validation_report_path=reports_dir / "validation_membrane_report.json",
            out_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "support"),
            strict=strict,
        ),
        lambda: run_check_life_support(
            state_dir=state_dir,
            reports_dir=reports_dir,
            strict=strict,
        ),
        lambda: run_cycle(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "cycle"),
            shadow_only=True,
            strict=strict,
        ),
        lambda: run_check_v0_contracts(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "contracts"),
            strict=strict,
        ),
        lambda: run_first_activation_preflight(
            docs_dir=docs_dir,
            doc_index_path=doc_index_path,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "preflight"),
            strict=strict,
        ),
        lambda: run_replay_shadow(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "replay"),
            strict=strict,
        ),
        lambda: run_write_growth_archive(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "archive"),
            strict=strict,
        ),
        lambda: run_emit_report(
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "emit"),
            strict=strict,
        ),
        lambda: run_explain_stage(
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            run_id=_bootstrap_run_id(run_id, "stage"),
            strict=strict,
        ),
    ]

    for step in steps:
        result = step()
        if result.exit_code != 0:
            return result.exit_code

    return 0


def _bootstrap_run_id(run_id: str | None, suffix: str) -> str:
    prefix = run_id or "digital-life-bootstrap"
    return f"{prefix}-{suffix}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
