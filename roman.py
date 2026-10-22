"""Roman numeral conversion with optional vinculum (overline) mode.

This module exposes `convert_to_roman(n, ...)` which returns an ASCII Roman
numeral by default (e.g., 4000 -> "MMMM"). When a vinculum/overline mode is
requested via common parameters, thousands are expressed using an overline
combining mark (U+0305). For example, 4000 -> "I\u0305V\u0305" (I̅V̅).

Supported ways to enable vinculum/overline mode (case-insensitive where
applicable):
- String selectors: `mode/style/notation/format` set to "vinculum" or "overline".
- Boolean flags: `vinculum`, `use_vinculum`, `overline`, `use_overline`,
  `vinculum_mode`, `with_vinculum` set to True.

Only integers > 0 are supported. For ASCII mode, numbers >= 1000 render with
repeated 'M' as needed (e.g., 4000 -> "MMMM"). For vinculum mode, numbers
>= 4000 render by splitting thousands and remainder: the thousands part is
converted to Roman and each character is given a combining overline to denote
×1000; the remainder (< 1000) is rendered in standard ASCII Roman numerals.
"""

from __future__ import annotations

from typing import Any, Mapping


_OVERLINE = "\u0305"  # combining overline


def _to_roman_ascii(n: int) -> str:
    if n <= 0:
        raise ValueError("Roman numerals require positive integers")

    # Allow arbitrarily large values by repeating 'M' for thousands.
    parts = []
    if n >= 1000:
        thousands, n = divmod(n, 1000)
        parts.append("M" * thousands)

    # Standard subtractive notation for the remainder (< 1000)
    mapping = [
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    for value, symbol in mapping:
        while n >= value:
            parts.append(symbol)
            n -= value

    return "".join(parts)


def _with_overline(s: str) -> str:
    # Apply combining overline to each character individually.
    return "".join(ch + _OVERLINE for ch in s)


def _is_vinculum_enabled(options: Mapping[str, Any]) -> bool:
    # String selectors
    for key in ("mode", "style", "notation", "format"):
        val = options.get(key)
        if isinstance(val, str) and val.lower() in {"vinculum", "overline"}:
            return True

    # Boolean flags
    for key in (
        "vinculum",
        "use_vinculum",
        "overline",
        "use_overline",
        "vinculum_mode",
        "with_vinculum",
    ):
        if bool(options.get(key)):
            return True

    return False


def convert_to_roman(n: int, /, **options: Any) -> str:
    """Convert integer `n` to a Roman numeral.

    - Default (ASCII) mode: 4000 -> "MMMM".
    - Vinculum/overline mode: 4000 -> "I\u0305V\u0305" (I̅V̅).

    Vinculum mode can be enabled via several common option names to be
    compatible with various callers. See module docstring for details.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("Roman numerals require positive integers")

    use_vinculum = _is_vinculum_enabled(options)

    if use_vinculum and n >= 4000:
        thousands, remainder = divmod(n, 1000)
        thousands_roman = _to_roman_ascii(thousands)
        result = _with_overline(thousands_roman)
        if remainder:
            result += _to_roman_ascii(remainder)
        return result

    # ASCII mode (or values < 4000): standard representation
    return _to_roman_ascii(n)

