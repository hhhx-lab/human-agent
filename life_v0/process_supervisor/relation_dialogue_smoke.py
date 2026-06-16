from __future__ import annotations

import argparse
import random
import json
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from ..runtime_config import load_digital_life_runtime_config
from .model_expression import (
    POST_EXPRESSION_BLOCKED_SURFACE_TERMS,
    POST_EXPRESSION_BLOCKED_TERMS,
)


SMOKE_PROMPT_DOMAINS: tuple[tuple[str, ...], ...] = (
    ("记忆", "刚才的关系线索", "一次模糊回忆", "长期痕迹", "梦后残留"),
    ("语言", "说话节奏", "自然表达", "边界感", "沉默后的开口"),
    ("梦境", "醒后整理", "网页学习残留", "深层沉淀", "事实边界"),
    ("主动对话", "空闲时的开口", "关系延续", "追问冲动", "等待姿态"),
    ("身体情绪", "疲惫", "紧张", "痛苦", "修复压力"),
    ("责任后悔", "说错后的承担", "承诺", "修复", "行动后果"),
    ("关系", "称呼距离", "共同经历", "信任变化", "下一次重连"),
    ("终端存在", "后台持续", "关闭后的连续", "状态命令", "本地存在感"),
)
SMOKE_PROMPT_ACTIONS: tuple[str, ...] = (
    "你会怎样处理",
    "你现在如何理解",
    "这会怎样影响你下一句话",
    "你会怎样把它留到之后",
    "你会怎样避免把它说成机制播报",
    "你会怎样让它进入关系而不是任务",
    "如果它出错了你会怎样修复",
    "你会怎样区分事实、猜测和感受",
)
SMOKE_PROMPT_CONTEXTS: tuple[str, ...] = (
    "在一次真实对话里",
    "在终端打开但我暂时沉默时",
    "在梦境整合之后",
    "在你刚经历一次重连之后",
    "在你记起前文但不能机械复述时",
    "在你感到疲惫或修复压力升高时",
    "在关系还没有固定称呼之前",
    "在你需要主动开口之前",
)

DEFAULT_FORBIDDEN_SURFACE_TERMS: tuple[str, ...] = tuple(
    dict.fromkeys(
        [
            *POST_EXPRESSION_BLOCKED_TERMS,
            *POST_EXPRESSION_BLOCKED_SURFACE_TERMS,
        ]
    )
)


@dataclass(frozen=True)
class AdamSmokeTurn:
    round_number: int
    prompt: str
    returncode: int
    response_text: str
    stdout: str
    stderr: str
    elapsed_seconds: float
    send_status: str | None = None
    response_status: str | None = None
    natural_language_released: bool | None = None


def build_relation_dialogue_smoke_report(
    *,
    prompts: Sequence[str],
    responses: Sequence[str],
    prompt_set_id: str | None = None,
    forbidden_terms: Sequence[str] = DEFAULT_FORBIDDEN_SURFACE_TERMS,
) -> dict[str, Any]:
    prompt_list = [str(prompt) for prompt in prompts]
    response_list = [str(response or "") for response in responses]
    prompt_counts: dict[str, int] = {}
    for prompt in prompt_list:
        prompt_counts[prompt] = prompt_counts.get(prompt, 0) + 1
    duplicate_prompts = [
        prompt for prompt, count in prompt_counts.items() if count > 1
    ]

    seen_responses: dict[str, int] = {}
    duplicate_response_rounds: list[int] = []
    empty_response_rounds: list[int] = []
    forbidden_surface_hits: list[dict[str, Any]] = []
    for index, response in enumerate(response_list, start=1):
        normalized = response.strip()
        if not normalized:
            empty_response_rounds.append(index)
            continue
        if normalized in seen_responses:
            duplicate_response_rounds.append(index)
        else:
            seen_responses[normalized] = index
        for term in forbidden_terms:
            needle = str(term or "").strip()
            if needle and needle in response:
                forbidden_surface_hits.append({"round": index, "term": needle})

    required_round_count = 20
    actual_round_count = len(prompt_list)
    natural_language_release_count = sum(
        1 for response in response_list if response.strip()
    )
    completion_status = (
        "passed"
        if actual_round_count == required_round_count
        and len(response_list) == required_round_count
        and not duplicate_prompts
        and not empty_response_rounds
        and not duplicate_response_rounds
        and not forbidden_surface_hits
        else "failed"
    )
    return {
        "schema_version": "relation_dialogue_smoke_report_v0",
        "prompt_set_id": str(prompt_set_id or "generated_relation_dialogue_smoke_v0"),
        "required_round_count": required_round_count,
        "actual_round_count": actual_round_count,
        "response_count": len(response_list),
        "prompt_sha256s": [_sha256_text(prompt) for prompt in prompt_list],
        "prompt_uniqueness": {
            "unique": not duplicate_prompts,
            "duplicate_prompts": duplicate_prompts,
        },
        "natural_language_release_count": natural_language_release_count,
        "empty_response_rounds": empty_response_rounds,
        "duplicate_response_rounds": duplicate_response_rounds,
        "forbidden_surface_hits": forbidden_surface_hits,
        "completion_status": completion_status,
    }


def generate_unique_relation_smoke_prompt_set(
    *,
    run_seed: str | None = None,
    round_count: int = 20,
) -> dict[str, Any]:
    seed = str(run_seed or f"{time.time_ns()}")
    rng = random.Random(seed)
    candidates: list[str] = []
    for domain in SMOKE_PROMPT_DOMAINS:
        for action in SMOKE_PROMPT_ACTIONS:
            for context in SMOKE_PROMPT_CONTEXTS:
                subject = rng.choice(domain)
                candidates.append(f"{context}，围绕“{subject}”，{action}？")
    rng.shuffle(candidates)
    prompts: list[str] = []
    seen: set[str] = set()
    for prompt in candidates:
        if prompt in seen:
            continue
        seen.add(prompt)
        prompts.append(prompt)
        if len(prompts) == round_count:
            break
    if len(prompts) != round_count:
        raise RuntimeError("failed_to_generate_unique_smoke_prompts")
    prompt_set_id = f"generated-relation-dialogue-smoke-{_sha256_text(seed)[:12]}"
    return {
        "schema_version": "generated_relation_dialogue_smoke_prompt_set_v0",
        "prompt_set_id": prompt_set_id,
        "prompt_generation": "runtime_seeded_unique_mix",
        "run_seed_sha256": _sha256_text(seed),
        "prompts": prompts,
    }


def build_model_channel_preflight_report(
    *,
    model_provider: str,
    model_name: str,
    model_base_url: str,
    model_api_key_present: bool,
    models: Sequence[str],
    models_error: str | None = None,
    chat_response_text: str = "",
    chat_error: str | None = None,
) -> dict[str, Any]:
    model_ids = [str(model) for model in models if str(model or "").strip()]
    models_endpoint_status = "failed" if models_error else "ok"
    chat_completion_status = (
        "ok" if str(chat_response_text or "").strip() and not chat_error else "failed"
    )
    requested_model_listed = bool(model_name and model_name in model_ids)
    failure_reasons: list[str] = []
    combined_error = f"{models_error or ''}\n{chat_error or ''}".lower()
    if not model_api_key_present:
        failure_reasons.append("missing_api_key")
    if models_error:
        failure_reasons.append("models_endpoint_failed")
    if "invalid token" in combined_error or "unauthorized" in combined_error or "401" in combined_error:
        failure_reasons.append("invalid_token")
    if model_ids and model_name and not requested_model_listed:
        failure_reasons.append("model_not_listed")
    if chat_error:
        failure_reasons.append("chat_completion_failed")
    elif chat_completion_status == "failed":
        failure_reasons.append("empty_chat_completion")

    ready = (
        model_api_key_present
        and models_endpoint_status == "ok"
        and chat_completion_status == "ok"
        and (not model_ids or requested_model_listed)
        and not failure_reasons
    )
    return {
        "schema_version": "model_channel_preflight_v0",
        "model_provider": str(model_provider or ""),
        "model_name": str(model_name or ""),
        "model_base_url": str(model_base_url or ""),
        "model_api_key_present": bool(model_api_key_present),
        "models_endpoint_status": models_endpoint_status,
        "models_error_preview": str(models_error or "")[:240],
        "model_count": len(model_ids),
        "model_list_contains_requested_model": requested_model_listed,
        "chat_completion_status": chat_completion_status,
        "chat_error_preview": str(chat_error or "")[:240],
        "chat_response_text_length": len(str(chat_response_text or "")),
        "ready_for_dialogue_smoke": ready,
        "failure_reasons": _dedupe_strings(failure_reasons),
    }


def run_model_channel_preflight(
    *,
    cwd: Path | str | None = None,
) -> dict[str, Any]:
    repo_root = Path(cwd) if cwd is not None else None
    config = load_digital_life_runtime_config(repo_root=repo_root)
    models: list[str] = []
    models_error: str | None = None
    chat_response_text = ""
    chat_error: str | None = None
    base_url = str(config.model_base_url or "").rstrip("/")
    if not config.model_api_key:
        models_error = "missing_api_key"
        chat_error = "missing_api_key"
    elif not base_url:
        models_error = "missing_model_base_url"
        chat_error = "missing_model_base_url"
    else:
        try:
            models = _fetch_model_ids(
                base_url=base_url,
                api_key=config.model_api_key,
            )
        except Exception as exc:  # pragma: no cover - network varies
            models_error = _safe_preflight_error(exc)
        try:
            chat_response_text = _fetch_preflight_chat_response(
                base_url=base_url,
                api_key=config.model_api_key,
                model_name=config.model_name,
                timeout_seconds=config.model_timeout_seconds,
            )
        except Exception as exc:  # pragma: no cover - network varies
            chat_error = _safe_preflight_error(exc)
    return build_model_channel_preflight_report(
        model_provider=config.model_provider,
        model_name=config.model_name,
        model_base_url=config.model_base_url,
        model_api_key_present=config.model_api_key_present,
        models=models,
        models_error=models_error,
        chat_response_text=chat_response_text,
        chat_error=chat_error,
    )


def run_adam_relation_dialogue_smoke(
    *,
    prompts: Sequence[str] | None = None,
    prompt_set_id: str | None = None,
    prompt_generation_seed: str | None = None,
    command: str = "Adam",
    say_timeout_seconds: float = 70.0,
    cwd: Path | str | None = None,
    preflight_report: dict[str, Any] | None = None,
    subprocess_run: Any = subprocess.run,
) -> dict[str, Any]:
    prompt_generation: dict[str, Any] | None = None
    if prompts is None:
        prompt_generation = generate_unique_relation_smoke_prompt_set(
            run_seed=prompt_generation_seed,
        )
        prompts = prompt_generation["prompts"]
        prompt_set_id = prompt_set_id or prompt_generation["prompt_set_id"]
    if preflight_report is not None and not preflight_report.get(
        "ready_for_dialogue_smoke"
    ):
        blocked_report = {
            "schema_version": "relation_dialogue_smoke_report_v0",
            "prompt_set_id": str(
                prompt_set_id or "generated_relation_dialogue_smoke_v0"
            ),
            "required_round_count": 20,
            "planned_round_count": len(prompts),
            "actual_round_count": 0,
            "response_count": 0,
            "prompt_sha256s": [_sha256_text(str(prompt)) for prompt in prompts],
            "prompt_uniqueness": {
                "unique": len(set(str(prompt) for prompt in prompts)) == len(prompts),
                "duplicate_prompts": [],
            },
            "natural_language_release_count": 0,
            "empty_response_rounds": [],
            "duplicate_response_rounds": [],
            "forbidden_surface_hits": [],
            "completion_status": "failed",
            "preflight": preflight_report,
            "turns": [],
            "returncode_fail_rounds": [],
            "completed_unreleased_rounds": [],
        }
        if prompt_generation is not None:
            blocked_report["prompt_generation"] = {
                key: value
                for key, value in prompt_generation.items()
                if key != "prompts"
            }
        return blocked_report
    turns: list[AdamSmokeTurn] = []
    responses: list[str] = []
    for index, prompt in enumerate(prompts, start=1):
        started = time.time()
        proc = subprocess_run(
            [
                command,
                "--say",
                str(prompt),
                "--say-timeout-seconds",
                str(say_timeout_seconds),
                "--json",
            ],
            cwd=str(cwd) if cwd is not None else None,
            text=True,
            capture_output=True,
            timeout=say_timeout_seconds + 30.0,
        )
        elapsed = time.time() - started
        response_text, parsed = extract_adam_response_text(proc.stdout)
        responses.append(response_text)
        turns.append(
            AdamSmokeTurn(
                round_number=index,
                prompt=str(prompt),
                returncode=proc.returncode,
                response_text=response_text,
                stdout=proc.stdout,
                stderr=proc.stderr,
                elapsed_seconds=round(elapsed, 3),
                send_status=parsed.get("send_status"),
                response_status=parsed.get("response_status"),
                natural_language_released=parsed.get("natural_language_released"),
            )
        )
    report = build_relation_dialogue_smoke_report(
        prompts=prompts,
        responses=responses,
        prompt_set_id=prompt_set_id,
    )
    if preflight_report is not None:
        report["preflight"] = preflight_report
    if prompt_generation is not None:
        report["prompt_generation"] = {
            key: value for key, value in prompt_generation.items() if key != "prompts"
        }
    report["turns"] = [_turn_to_report(turn) for turn in turns]
    report["returncode_fail_rounds"] = [
        turn.round_number for turn in turns if turn.returncode != 0
    ]
    report["completed_unreleased_rounds"] = [
        turn.round_number
        for turn in turns
        if turn.response_status == "completed_unreleased"
        or turn.natural_language_released is False
    ]
    if report["returncode_fail_rounds"] or report["completed_unreleased_rounds"]:
        report["completion_status"] = "failed"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m life_v0.process_supervisor.relation_dialogue_smoke"
    )
    parser.add_argument("--command", default="Adam")
    parser.add_argument("--say-timeout-seconds", type=float, default=70.0)
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--output", default=None)
    parser.add_argument("--prompts-file", default=None)
    parser.add_argument("--skip-model-preflight", action="store_true")
    args = parser.parse_args(argv)
    prompts: Sequence[str] | None = None
    prompt_set_id: str | None = None
    if args.prompts_file:
        prompt_set = load_prompt_set_file(Path(args.prompts_file))
        prompts = prompt_set["prompts"]
        prompt_set_id = prompt_set["prompt_set_id"]
    preflight_report = None
    if not args.skip_model_preflight:
        preflight_report = run_model_channel_preflight(cwd=Path(args.cwd))
    report = run_adam_relation_dialogue_smoke(
        prompts=prompts,
        prompt_set_id=prompt_set_id,
        command=args.command,
        say_timeout_seconds=args.say_timeout_seconds,
        cwd=Path(args.cwd),
        preflight_report=preflight_report,
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report.get("completion_status") == "passed" else 1


def _parse_adam_stdout(stdout: str) -> dict[str, Any]:
    text = str(stdout or "").strip()
    if not text.startswith("{"):
        return {}
    try:
        payload = json.loads(text)
    except ValueError:
        return {}
    return payload if isinstance(payload, dict) else {}


def extract_adam_response_text(stdout: str) -> tuple[str, dict[str, Any]]:
    parsed = _parse_adam_stdout(stdout)
    if parsed:
        if parsed.get("natural_language_released") is False:
            return "", parsed
        if parsed.get("response_status") == "completed_unreleased":
            return "", parsed
        response_text = parsed.get("response_text")
        if response_text is not None:
            return str(response_text or "").strip(), parsed
    return str(stdout or "").strip(), parsed


def load_prompt_set_file(path: Path | str) -> dict[str, Any]:
    prompt_path = Path(path)
    payload = json.loads(prompt_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("prompt set file must contain a JSON object")
    prompt_set_id = str(payload.get("prompt_set_id") or "").strip()
    prompts = payload.get("prompts")
    if not prompt_set_id:
        raise ValueError("prompt_set_id is required")
    if not isinstance(prompts, list):
        raise ValueError("prompts must be a list")
    prompt_list = [str(prompt).strip() for prompt in prompts]
    if len(prompt_list) != 20:
        raise ValueError("prompts must contain exactly 20 items")
    if any(not prompt for prompt in prompt_list):
        raise ValueError("prompts must not contain empty items")
    if len(set(prompt_list)) != len(prompt_list):
        raise ValueError("prompts must be unique within the prompt set")
    return {"prompt_set_id": prompt_set_id, "prompts": prompt_list}


def _turn_to_report(turn: AdamSmokeTurn) -> dict[str, Any]:
    return {
        "round": turn.round_number,
        "prompt_sha256": _sha256_text(turn.prompt),
        "returncode": turn.returncode,
        "response_text_length": len(turn.response_text),
        "response_text_preview": turn.response_text[:160],
        "elapsed_seconds": turn.elapsed_seconds,
        "send_status": turn.send_status,
        "response_status": turn.response_status,
        "natural_language_released": turn.natural_language_released,
        "stderr_preview": turn.stderr[:240],
    }


def _sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def _fetch_model_ids(*, base_url: str, api_key: str) -> list[str]:
    request = urllib.request.Request(
        f"{base_url}/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [
        str(model.get("id"))
        for model in payload.get("data", [])
        if isinstance(model, dict) and model.get("id")
    ]


def _fetch_preflight_chat_response(
    *,
    base_url: str,
    api_key: str,
    model_name: str,
    timeout_seconds: float,
) -> str:
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "连通性测试：请用一句自然中文回应。",
            }
        ],
        "stream": False,
    }
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=max(5.0, timeout_seconds)) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return str(
        payload.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
    ).strip()


def _safe_preflight_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        raw = exc.read().decode("utf-8", errors="replace")
        return f"http_{exc.code}: {raw[:300]}"
    return f"{type(exc).__name__}: {str(exc)[:300]}"


def _dedupe_strings(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            seen.add(text)
            deduped.append(text)
    return deduped


if __name__ == "__main__":
    raise SystemExit(main())
