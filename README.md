# sci-calc-20260903 — Scientific Calculator

> Python scientific calculator with 12 functions + history — built via auto-orchestrated multi-agent workflow.

## Executive Summary

Modular scientific calculator covering arithmetic, power, roots, trigonometry, logarithms, and exponentials. Dual API: module-level functions and `ScientificCalculator` class. History tracking, degree/radian toggle, robust error handling, click+rich CLI, pytest suite.

| Metric | Value |
|--------|-------|
| Functions | 12 (add, sub, mul, div, pow, sqrt, sin, cos, tan, log, exp, history) |
| Class methods | 12 + helpers |
| Tests | 14 |
| Dependencies | click, rich, pytest |
| Python | >=3.8 |
| **Total** | **Single module + tests + CLI** |

## Features

- **Arithmetic:** `add(a,b)` `sub(a,b)` `mul(a,b)` `div(a,b)` — zero-division guard
- **Power/Root:** `pow(a,b)` `sqrt(a)` — negative sqrt raises `ValueError`
- **Trig:** `sin(a)` `cos(a)` `tan(a)` — radian default, `set_degree_mode(True)` for degrees
- **Log/Exp:** `log(a, base=e)` `exp(a)` — domain validation
- **History:** `history()` / `get_history()` / `clear_history()` + instance `get_history()`
- **CLI:** `python calculator.py` — click group + rich tables, fallback REPL
- **Class:** `ScientificCalculator(degree_mode=False)` — isolated history per instance

## Quick Start

```bash
pip install -r requirements.txt
python calculator.py --help
pytest -v
```

```python
import calculator as calc

calc.add(2, 3)          # 5.0
calc.div(10, 2)         # 5.0
calc.pow(2, 8)          # 256.0
calc.sqrt(16)           # 4.0
calc.sin(1.5708)        # ~1.0
calc.set_degree_mode(True)
calc.sin(30)            # 0.5
calc.log(8, 2)          # 3.0
calc.exp(1)             # 2.718...
calc.history()          # [{op, args, result}, ...]
calc.clear_history()

# Class API
c = calc.ScientificCalculator(degree_mode=True)
c.sin(90)  # 1.0
c.get_history()
```

## CLI Examples

```bash
python calculator.py add-cmd 2 3        # via click group (if renamed)
python calculator.py history-cmd
python calculator.py sin-cmd 30 --deg
# REPL fallback when click/rich missing:
python calculator.py
```

> Note: CLI entry is `calculator.py` with click commands `add-cmd`, `sub-cmd`, `mul-cmd`, `div-cmd`, `pow-cmd`, `sqrt-cmd`, `sin-cmd`, `cos-cmd`, `tan-cmd`, `log-cmd`, `exp-cmd`, `history-cmd`, `clear-cmd`.

## Project Structure

```
sci-calc-20260903/
├── calculator.py      # core module (functions + class + CLI)
├── test_calculator.py # pytest suite
├── requirements.txt
├── .gitignore
└── README.md
```

## Auto-Orchestration

Built with parallel multi-agent workflow:

| Agent | Role | Model |
|-------|------|-------|
| opencode plan | Planning & spec | muse-spark |
| opencode build | Core build & tests | big-pickle |
| codex review | Correctness review | codex |
| agy UI | CLI/UI design | Gemini 3.7 Flash High |
| researcher + scout | Parallel research | researcher / scout |

## Testing

```bash
pytest -v                          # all tests
pytest test_calculator.py -k history
python -m calculator               # REPL
```

## Error Handling

| Condition | Exception |
|-----------|-----------|
| div by 0 | `ZeroDivisionError` |
| sqrt(-x) | `ValueError` |
| log(≤0) / invalid base | `ValueError` |

## Review Checklist

- [ ] All 12 functions verified with pytest
- [ ] Degree/radian toggle tested
- [ ] History isolated per instance + global
- [ ] CLI renders with rich tables
- [ ] Error paths raise correct exceptions

## License

MIT — Rituparno Majumdar, 2026-09-03
