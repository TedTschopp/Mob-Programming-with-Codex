"""Simple CLI to convert integers to Roman numerals using roman.py.

Usage examples:

  - Interactive (prompts):
      python app.py

  - One-shot with args:
      python app.py 4000 --vinculum
      python app.py 1999
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from roman import convert_to_roman


def _prompt_int(prompt: str) -> int:
    try:
        raw = input(prompt).strip()
    except EOFError:
        raise SystemExit(1)
    try:
        value = int(raw)
    except ValueError:
        print("Please enter a valid integer.", file=sys.stderr)
        raise SystemExit(2)
    if value <= 0:
        print("Please enter a positive integer (>= 1).", file=sys.stderr)
        raise SystemExit(2)
    return value


def _prompt_yes_no(prompt: str, default: bool = False) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    try:
        raw = input(prompt + suffix).strip().lower()
    except EOFError:
        return default
    if not raw:
        return default
    if raw in {"y", "yes"}:
        return True
    if raw in {"n", "no"}:
        return False
    # Unrecognized; assume default
    return default


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Convert integers to Roman numerals")
    p.add_argument("number", nargs="?", type=int, help="Positive integer to convert")
    p.add_argument(
        "-v",
        "--vinculum",
        action="store_true",
        help="Use vinculum/overline mode for thousands (e.g., 4000 -> I\u0305V\u0305)",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.number is None:
        # Interactive prompts
        n = _prompt_int("Enter a positive integer to convert: ")
        use_vinculum = _prompt_yes_no("Use vinculum/overline mode?", default=False)
    else:
        n = args.number
        if n <= 0:
            print("Please provide a positive integer (>= 1).", file=sys.stderr)
            return 2
        use_vinculum = bool(args.vinculum)

    try:
        result = convert_to_roman(n, vinculum=use_vinculum)
    except Exception as exc:  # surface friendly error
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

