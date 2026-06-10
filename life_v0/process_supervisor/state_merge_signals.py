from __future__ import annotations

from typing import Any


def state_merge_long_term_change_profile(
    state_merge_guard: dict[str, Any] | None,
) -> dict[str, Any]:
    change_sources = (state_merge_guard or {}).get("long_term_change_sources", {})
    if not isinstance(change_sources, dict):
        change_sources = {}
    families: list[str] = []
    refs: list[str] = []
    for family, values in change_sources.items():
        if not isinstance(values, list):
            continue
        family_refs = [str(item) for item in values if item]
        if not family_refs:
            continue
        families.append(str(family))
        refs.extend(family_refs)
    refs = _dedupe_string_list(refs)
    return {
        "state_merge_long_term_change_count": len(refs),
        "state_merge_long_term_change_families": families,
        "state_merge_long_term_change_refs": refs,
    }


def _dedupe_string_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
