from __future__ import annotations

import re
from typing import Any

_BLOCKED_NAME_FRAGMENTS = (
    "是否",
    "不是",
    "真的",
    "记得",
    "把",
    "在",
    "能",
    "否",
    "为了",
    "关系",
    "回答",
    "解释",
    "什么",
    "哪一种",
    "哪种",
    "为什么",
    "怎么",
    "如果",
    "可以",
    "需要",
    "应该",
    "模型",
    "助手",
    "编程",
    "语言模型",
    "人工智能",
    "ChatGPT",
    "OpenAI",
    "Codex",
    "GPT",
    "吗",
    "呢",
)

_BLOCKED_EXACT_NAMES = {
    "我",
    "你",
    "他",
    "她",
    "它",
    "我们",
    "朋友",
    "用户",
    "客户",
}


def is_valid_observed_name(value: Any) -> bool:
    text = _normalize_name(value)
    if not text:
        return False
    if text in _BLOCKED_EXACT_NAMES:
        return False
    if len(text) < 2 or len(text) > 16:
        return False
    if any(fragment in text for fragment in _BLOCKED_NAME_FRAGMENTS):
        return False
    if re.search(r"[？?！!。.,，；;：:]", text):
        return False
    if re.fullmatch(r"[A-Za-z]{1,5}", text) and text.upper() in {
        "GPT",
        "CODEX",
    }:
        return False
    return True


def sanitize_observed_names(values: list[Any]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = _normalize_name(value)
        if is_valid_observed_name(text):
            cleaned.append(text)
    return _dedupe(cleaned)


def extract_observed_names_from_utterances(
    utterances: list[str],
) -> list[str]:
    names: list[str] = []
    patterns = (
        r"(?:^|[，。,.\s！？!?；;：:、])(?:我叫|我的名字是|你可以叫我|以后叫我)\s*([\u4e00-\u9fffA-Za-z0-9_\-]{2,16})",
        r"(?:^|[，。,.\s！？!?；;：:、])之后你可以叫我\s*([\u4e00-\u9fffA-Za-z0-9_\-]{2,16})",
        r"(?:^|[，。,.\s！？!?；;：:、])以后你可以叫我\s*([\u4e00-\u9fffA-Za-z0-9_\-]{2,16})",
        r"(?:^|[，。,.\s！？!?；;：:、])叫我\s*([\u4e00-\u9fffA-Za-z0-9_\-]{2,16})",
    )
    for utterance in utterances:
        text = str(utterance or "")
        for pattern in patterns:
            for match in re.findall(pattern, text):
                cleaned = _normalize_name(match)
                if is_valid_observed_name(cleaned):
                    names.append(cleaned)
    return sanitize_observed_names(names)


def _normalize_name(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return re.split(r"[，。,.\s！？!?；;：:、]", text)[0].strip()


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
