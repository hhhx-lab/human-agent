from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


ENV_FILE_NAME = ".env"
RUNTIME_CONFIG_STATE_REF = "runtime/state/terminal/runtime_config_state.json"
RUNTIME_CONFIG_REPORT_REF = "runtime/reports/latest/digital_life_runtime_config_report.json"


@dataclass(frozen=True)
class DigitalLifeRuntimeConfig:
    env_file: Path | None
    runtime_profile: str
    model_provider: str
    model_name: str
    model_base_url: str | None
    model_api_key_present: bool
    model_temperature: float | None
    model_max_output_tokens: int | None
    model_timeout_seconds: float | None
    response_language: str
    dialogue_style: str
    strict_default: bool
    env_source: str

    def to_snapshot(
        self,
        *,
        run_id: str,
        generated_at: str,
        state_dir: Path,
        reports_dir: Path,
        receipts_dir: Path,
        strict: bool,
    ) -> dict[str, Any]:
        return {
            "schema_version": "digital_life_runtime_config_snapshot_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "status": "closed",
            "runtime_config_ref": RUNTIME_CONFIG_STATE_REF,
            "runtime_config_report_ref": RUNTIME_CONFIG_REPORT_REF,
            "env_file": str(self.env_file) if self.env_file else None,
            "env_source": self.env_source,
            "runtime_profile": self.runtime_profile,
            "model_provider": self.model_provider,
            "model_name": self.model_name,
            "model_base_url": self.model_base_url,
            "model_api_key_present": self.model_api_key_present,
            "model_api_key_redacted": "<redacted>" if self.model_api_key_present else None,
            "model_temperature": self.model_temperature,
            "model_max_output_tokens": self.model_max_output_tokens,
            "model_timeout_seconds": self.model_timeout_seconds,
            "response_language": self.response_language,
            "dialogue_style": self.dialogue_style,
            "strict_default": self.strict_default,
            "strict_requested": strict,
            "state_dir": str(state_dir),
            "reports_dir": str(reports_dir),
            "receipts_dir": str(receipts_dir),
        }


def load_digital_life_runtime_config(
    *,
    repo_root: Path | None = None,
    env_file: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> DigitalLifeRuntimeConfig:
    repo_root = (
        repo_root.resolve()
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    process_env = dict(os.environ if environ is None else environ)
    resolved_env_file = _resolve_env_file(
        repo_root=repo_root,
        explicit_env_file=env_file,
        process_env=process_env,
    )
    file_env = _read_env_file(resolved_env_file) if resolved_env_file else {}
    merged_env = {**file_env, **process_env}

    runtime_profile = _get_str(merged_env, "DIGITAL_LIFE_RUNTIME_PROFILE", "resident")
    model_provider = _get_str(merged_env, "DIGITAL_LIFE_MODEL_PROVIDER", "local")
    model_name = _get_str(merged_env, "DIGITAL_LIFE_MODEL_NAME", "digital-life-core")
    model_base_url = _optional_str(merged_env, "DIGITAL_LIFE_MODEL_BASE_URL")
    model_api_key_present = bool(_optional_str(merged_env, "DIGITAL_LIFE_MODEL_API_KEY"))
    model_temperature = _optional_float(merged_env, "DIGITAL_LIFE_MODEL_TEMPERATURE")
    model_max_output_tokens = _optional_int(
        merged_env,
        "DIGITAL_LIFE_MODEL_MAX_OUTPUT_TOKENS",
    )
    model_timeout_seconds = _optional_float(
        merged_env,
        "DIGITAL_LIFE_MODEL_TIMEOUT_SECONDS",
    )
    response_language = _get_str(merged_env, "DIGITAL_LIFE_RESPONSE_LANGUAGE", "zh-CN")
    dialogue_style = _get_str(merged_env, "DIGITAL_LIFE_DIALOGUE_STYLE", "relationship")
    strict_default = _parse_bool(merged_env.get("DIGITAL_LIFE_STRICT_DEFAULT"), False)
    env_source = "process_env"
    if resolved_env_file and resolved_env_file.exists():
        env_source = f"env_file:{resolved_env_file}"

    return DigitalLifeRuntimeConfig(
        env_file=resolved_env_file,
        runtime_profile=runtime_profile,
        model_provider=model_provider,
        model_name=model_name,
        model_base_url=model_base_url,
        model_api_key_present=model_api_key_present,
        model_temperature=model_temperature,
        model_max_output_tokens=model_max_output_tokens,
        model_timeout_seconds=model_timeout_seconds,
        response_language=response_language,
        dialogue_style=dialogue_style,
        strict_default=strict_default,
        env_source=env_source,
    )


def write_digital_life_runtime_config_snapshot(
    *,
    repo_root: Path | None = None,
    env_file: Path | None = None,
    environ: Mapping[str, str] | None = None,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str,
    generated_at: str,
    strict: bool,
    write_json: Any,
) -> dict[str, Any]:
    runtime_config = load_digital_life_runtime_config(
        repo_root=repo_root,
        env_file=env_file,
        environ=environ,
    )
    snapshot = runtime_config.to_snapshot(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        strict=strict,
    )
    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(terminal_dir / "runtime_config_state.json", snapshot)
    write_json(reports_dir / "digital_life_runtime_config_report.json", snapshot)
    return snapshot


def _resolve_env_file(
    *,
    repo_root: Path,
    explicit_env_file: Path | None,
    process_env: Mapping[str, str],
) -> Path | None:
    candidate = explicit_env_file
    if candidate is None:
        env_file_value = process_env.get("DIGITAL_LIFE_ENV_FILE", "").strip()
        if env_file_value:
            candidate = Path(env_file_value)
        else:
            candidate = repo_root / ENV_FILE_NAME
    if candidate is None:
        return None
    candidate = candidate.expanduser()
    if not candidate.is_absolute():
        candidate = (repo_root / candidate).resolve()
    return candidate if candidate.exists() else None


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        values[key] = _unquote(value.strip())
    return values


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _get_str(values: Mapping[str, str], key: str, default: str) -> str:
    value = values.get(key)
    if value is None:
        return default
    stripped = value.strip()
    return stripped or default


def _optional_str(values: Mapping[str, str], key: str) -> str | None:
    value = values.get(key)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _optional_float(values: Mapping[str, str], key: str) -> float | None:
    value = _optional_str(values, key)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid float for {key}: {value!r}") from exc


def _optional_int(values: Mapping[str, str], key: str) -> int | None:
    value = _optional_str(values, key)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Invalid int for {key}: {value!r}") from exc


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default
