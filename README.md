# Mob-Programming-with-Codex

Small demonstration project for Roman numeral conversion including optional
vinculum (overline) notation for values ≥ 4000.

## Quick Start (macOS / Linux / WSL)

```bash
# 1. Clone (if you have not already)
git clone <this-repo-url>
cd Mob-Programming-with-Codex

# 2. (Recommended) Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install test dependency
python -m pip install --upgrade pip
python -m pip install pytest

# 4. Run the tests
python -m pytest -q

# 5. Use the module in an interactive session
python
>>> from roman import convert_to_roman
>>> convert_to_roman(4000)
'MMMM'
>>> convert_to_roman(4000, mode="vinculum")  # overline notation
'I\u0305V\u0305'
```

## One-Liner to Run Tests (if venv already created)

```bash
. .venv/bin/activate && python -m pytest -q
```

## Function Usage

`convert_to_roman(n: int, **options) -> str`

Supported ways to enable vinculum / overline mode (case-insensitive where
strings are used):

Flags / keywords: `mode`, `style`, `notation`, `format` (values: `vinculum` or `overline`)

Boolean switches: `vinculum`, `use_vinculum`, `overline`, `use_overline`,
`vinculum_mode`, `with_vinculum`.

Examples:

```python
convert_to_roman(944)          # 'CMXLIV'
convert_to_roman(4000)         # 'MMMM'
convert_to_roman(4000, mode="vinculum")  # 'I\u0305V\u0305'
convert_to_roman(12345, style="overline")  # 'X\u0305I\u0305I\u0305I\u0305CCXLV'
```

## Extended Tests

- The test suite includes broad coverage across 1..10,000,000 using sampling
  at every thousand boundary with representative remainders.
- To run optional exhaustive checks over the full range (slow), set:

```bash
FULL_ROMAN_RANGE=1 python -m pytest -q -m slow
```

This enables two extra tests that iterate through every integer from 1 to
10,000,000, verifying ASCII and vinculum consistency properties.

## Development Notes

- The implementation allows arbitrarily large integers by repeating `M` in ASCII mode.
- In vinculum mode, thousands are factored out, converted to Roman, and each glyph is given a combining overline (U+0305) to indicate ×1000, followed by the remainder < 1000 rendered normally.
- Tests live in `tests/` and currently cover 4000 in both ASCII and vinculum forms.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `zsh: command not found: python` | Use `python3` or ensure a Python 3.11+ install is on PATH. |
| `No module named pytest` | Install with `python -m pip install pytest`. |
| Accented/overline characters look odd | Ensure your terminal/font supports combining characters. Try a different monospace font. |

## License

Add a license here (e.g., MIT) if you intend to distribute this project.
