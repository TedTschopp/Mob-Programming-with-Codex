"""Extended tests for Roman numeral conversion across a large range.

Goals:
- Validate ASCII mode correctness via a decomposition property.
- Validate vinculum/overline mode consistency with the documented behavior.
- Cover values up to 10,000,000 with efficient sampling and optional full sweep.

Notes:
- Full exhaustive testing of 1..10,000,000 is expensive; enable it by setting
  the env var `FULL_ROMAN_RANGE=1`. Sampled tests always run and include all
  thousand boundaries with representative remainders below 1000.
"""

from __future__ import annotations

import os
import unicodedata as _ud

import pytest


def _import_convert_to_roman():
    """Try common module paths to locate convert_to_roman()."""
    try:
        from roman import convert_to_roman  # type: ignore
        return convert_to_roman
    except Exception:
        pass
    try:
        from app import convert_to_roman  # type: ignore
        return convert_to_roman
    except Exception:
        pass
    try:
        from roman_numerals import convert_to_roman  # type: ignore
        return convert_to_roman
    except Exception:
        pass
    pytest.skip(
        "convert_to_roman function not found. Import it from your module to enable this test."
    )


def _overline(s: str) -> str:
    return "".join(ch + "\u0305" for ch in s)


ASCII_CHARS = set("IVXLCDM")


def test_ascii_decomposition_sampled():
    convert_to_roman = _import_convert_to_roman()

    # Representative remainder values below 1000 covering subtractive and round cases
    residuals = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        14,
        19,
        40,
        44,
        49,
        50,
        90,
        94,
        99,
        100,
        400,
        444,
        490,
        500,
        900,
        944,
        999,
    ]

    # Cover every thousand boundary from 0..10,000 (i.e., up to 10,000,000)
    for k in range(0, 10000 + 1):
        prefix = "M" * k
        for r in residuals:
            n = k * 1000 + r
            if n == 0 or n > 10_000_000:
                continue
            s = convert_to_roman(n)

            # Decomposition property for ASCII mode
            expected_remainder = "" if r == 0 else convert_to_roman(r)
            expected = prefix + expected_remainder
            assert s == expected

            # Only ASCII Roman symbols are used
            assert set(s) <= ASCII_CHARS


def test_vinculum_consistency_sampled():
    convert_to_roman = _import_convert_to_roman()

    residuals = [
        0,
        1,
        4,
        5,
        9,
        10,
        40,
        49,
        50,
        90,
        99,
        100,
        400,
        490,
        500,
        900,
        944,
        999,
    ]

    for k in range(0, 10000 + 1):
        t = "" if k == 0 else convert_to_roman(k)  # thousands segment in ASCII
        ov = _overline(t)
        for r in residuals:
            n = k * 1000 + r
            if n == 0 or n > 10_000_000:
                continue
            v = convert_to_roman(n, vinculum=True)
            a = convert_to_roman(n)

            if n < 4000:
                # For small numbers, vinculum should match ASCII form
                assert _ud.normalize("NFC", v) == _ud.normalize("NFC", a)
            else:
                # Vinculum form is overlined thousands-part + ASCII remainder
                expected_remainder = "" if r == 0 else convert_to_roman(r)
                expected = ov + expected_remainder
                assert _ud.normalize("NFC", v) == _ud.normalize("NFC", expected)


@pytest.mark.slow
def test_full_range_ascii_when_opt_in():
    """Optional exhaustive ASCII check over 1..10_000_000.

    Enabled only when `FULL_ROMAN_RANGE=1` is set in the environment to
    keep default test runs fast.
    """
    if os.getenv("FULL_ROMAN_RANGE") != "1":
        pytest.skip("Set FULL_ROMAN_RANGE=1 to run this exhaustive test.")

    convert_to_roman = _import_convert_to_roman()
    for n in range(1, 10_000_000 + 1):
        k, r = divmod(n, 1000)
        expected_remainder = "" if r == 0 else convert_to_roman(r)
        expected = ("M" * k) + expected_remainder
        s = convert_to_roman(n)
        assert s == expected
        assert set(s) <= ASCII_CHARS


@pytest.mark.slow
def test_full_range_vinculum_when_opt_in():
    if os.getenv("FULL_ROMAN_RANGE") != "1":
        pytest.skip("Set FULL_ROMAN_RANGE=1 to run this exhaustive test.")

    convert_to_roman = _import_convert_to_roman()
    for n in range(1, 10_000_000 + 1):
        if n < 4000:
            assert convert_to_roman(n, vinculum=True) == convert_to_roman(n)
        else:
            k, r = divmod(n, 1000)
            thousands_ascii = convert_to_roman(k)
            expected_remainder = "" if r == 0 else convert_to_roman(r)
            expected = _overline(thousands_ascii) + expected_remainder
            v = convert_to_roman(n, vinculum=True)
            assert _ud.normalize("NFC", v) == _ud.normalize("NFC", expected)
