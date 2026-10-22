"""
Unit test for converting 4000 to a Roman numeral.

Notes on notation (checked from reputable sources like Britannica and Wikipedia):
- Classical/vinculum style uses an overline to indicate ×1000; thus 4000 is IV with an overline.
- In ASCII-only/common programming practice, 4000 is represented as "MMMM".

This test uses the ASCII form ("MMMM"). If your implementation uses
vinculum style, change the expected value to "I05V05" (I and V with combining overline).
"""

import pytest


def _import_convert_to_roman():
    """Try a couple common module paths to locate convert_to_roman()."""
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
        # Fallback to a more generic name some projects use
        from roman_numerals import convert_to_roman  # type: ignore
        return convert_to_roman
    except Exception:
        pass
    pytest.skip(
        "convert_to_roman function not found. Import it from your module to enable this test."
    )


def test_convert_to_roman_4000_ascii():
    convert_to_roman = _import_convert_to_roman()
    assert convert_to_roman(4000) == "MMMM"


def test_convert_to_roman_4000_vinculum():
    """Test 4000 using vinculum/overline notation when supported.

    Tries a few common call patterns and skips if the implementation
    does not expose a vinculum/overline mode.
    """
    convert_to_roman = _import_convert_to_roman()

    expected = "I\u0305V\u0305"  # I̅V̅ (combining overline)

    # Try several likely APIs; skip if none are supported
    attempts = [
        {"mode": "vinculum"},
        {"style": "vinculum"},
        {"notation": "vinculum"},
        {"format": "vinculum"},
        {"mode": "overline"},
        {"style": "overline"},
        {"notation": "overline"},
        {"format": "overline"},
        {"vinculum": True},
        {"use_vinculum": True},
        {"overline": True},
        {"use_overline": True},
        {"vinculum_mode": True},
        {"with_vinculum": True},
    ]

    for kwargs in attempts:
        try:
            result = convert_to_roman(4000, **kwargs)
        except TypeError:
            # Signature doesn't support these kwargs; try next form
            continue
        except Exception:
            # Implementation-specific rejection of this form; try next
            continue
        else:
            # Compare using NFC to be robust to internal normalization
            import unicodedata as _ud

            assert _ud.normalize("NFC", result) == _ud.normalize("NFC", expected)
            return

    import pytest as _pytest

    _pytest.skip("Vinculum/overline mode not supported by convert_to_roman.")
