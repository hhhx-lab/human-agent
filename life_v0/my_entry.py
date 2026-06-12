from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .digital_entry import main as digital_main
from .digital_life_identity import bind_or_validate_life_name, read_life_name_registry


def main(argv: list[str] | None = None) -> int:
    raw_args = list(sys.argv[1:] if argv is None else argv)
    if _help_requested(raw_args):
        print(_help_text())
        return 0
    if len(raw_args) < 2 or raw_args[:2] != ["digital", "life"]:
        print(_help_text(), file=sys.stderr)
        return 2

    life_args = raw_args[2:]
    if _life_help_requested(life_args):
        return digital_main(["life", *life_args])

    identity_parser = argparse.ArgumentParser(add_help=False)
    identity_parser.add_argument("--state", default="runtime/state")
    identity_parser.add_argument("--name", default=None)
    identity_parser.add_argument("--life-name", dest="name", default=None)
    identity_args, remaining_life_args = identity_parser.parse_known_args(life_args)
    requested_name = identity_args.name
    state_dir = Path(identity_args.state)
    if (
        not requested_name
        and sys.stdin.isatty()
        and not read_life_name_registry(state_dir)
    ):
        requested_name = input("第一次启动请为这个数字生命取一个名字：").strip()

    identity = bind_or_validate_life_name(
        state_dir=state_dir,
        requested_name=requested_name,
        source_command="my digital life",
    )
    if identity.get("exit_code") != 0:
        print(json.dumps(identity, ensure_ascii=False, indent=2), file=sys.stderr)
        return int(identity.get("exit_code", 2) or 2)

    delegated_args = [
        "life",
        "--state",
        str(identity_args.state),
        *remaining_life_args,
    ]
    return digital_main(delegated_args)


def _help_requested(args: list[str]) -> bool:
    return not args or args in (["-h"], ["--help"])


def _life_help_requested(args: list[str]) -> bool:
    return any(arg in {"-h", "--help"} for arg in args)


def _help_text() -> str:
    return "\n".join(
        [
            "usage: my digital life [--name <name>] [digital life options]",
            "",
            "First launch binds a permanent digital life name for this runtime.",
            "After the name is bound, my digital life restores the same resident process.",
            "",
            "examples:",
            "  my digital life --name 星火",
            "  my digital life --status",
            "  my digital life --say \"你还在吗？\"",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
