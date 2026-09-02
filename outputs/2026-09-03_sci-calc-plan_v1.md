# Execution Plan — sci-calc-20260903 (opencode plan / muse-spark)

Date: 2026-09-03 | Repo: Rituparno-Majumdar/sci-calc-20260903 | Source: research + scout of calculator.py (401 lines, 14 tests)

## Executive Summary
Single-module calculator covering 12 spec functions with dual API (module functions + ScientificCalculator class), click+rich CLI with fallback REPL, pytest parametrized tests, capped JSON-friendly history. Plan locks scope to spec, avoids over-engineering (no package split, no SQLite), and maps directly to verified existing implementation.

## 1. File Layout (keep flat, under 6 files)

```
sci-calc-20260903/
├── calculator.py        # core: math wrappers + history + class + CLI (400 lines budget)
├── test_calculator.py   # pytest 14 tests (parametrized edges)
├── requirements.txt     # click>=8.0, rich>=13.0, pytest>=7.0
├── README.md            # exec summary + totals + usage + review checklist
├── .gitignore           # __pycache__, .pytest_cache, venv, outputs
└── outputs/             # 2026-09-03_sci-calc-plan_v1.md (this plan)
```

Rationale: research recommends `core/ui/history` split for larger apps but scout confirms current flat layout satisfies spec and tests; splitting now would widen scope.

## 2. Function Specs (12 functions, validated signatures)

| Fn | Sig | Returns | Error | History |
|---|---|---|---|---|
| add | add(a:Number,b:Number)->float | float sum | float() coercion only | _record("add",(a,b),r) |
| sub | sub(a,b)->float | diff | — | _record |
| mul | mul(a,b)->float | prod | — | _record |
| div | div(a,b)->float | quot | ZeroDivisionError if b==0 | _record (no record on fail) |
| pow | pow(a,b)->float | math.pow | ValueError via math domain (e.g. -1,0.5) | _record |
| sqrt | sqrt(a)->float | sqrt | ValueError if a<0 | _record |
| sin | sin(a)->float | math.sin | ValueError if inf/nan | _record |
| cos | cos(a)->float | — | — | _record |
| tan | tan(a)->float | — | large float near pi/2 (document, no raise) | _record |
| log | log(a,base=e)->float | log | ValueError if a<=0 or base<=0 or ==1 | _record |
| exp | exp(a)->float | exp | OverflowError if >~709 | _record |
| history | history()->List[Dict] | shallow copy list(_history) | — | — |
| clear_history | clear_history()->None | clears _history | — | — |
| + | get_history alias, set_degree_mode(bool), is_degree_mode() | — | — | — |

Trig mode: global `_trig_in_degrees` + `ScientificCalculator.degree_mode`; converts via `_to_radians`/`_radians` using math.radians only at I/O boundary. Document radians default.

Class `ScientificCalculator`: own `history: List[Dict]` + `degree_mode`; `_rec` dual-writes instance + global; mirrors 10 ops with same validation; `get_history`/`clear_history`/`set_degree_mode`.

History entry: `{"op":str, "args":tuple, "result":float}` — append-only, shallow copy on read, no record on exception.

## 3. Testing Strategy (pytest, no widening)

- Run: `python3 -m pytest -v` (14 tests already passing).
- Coverage: add/sub/mul/div/pow/sqrt/sin/cos/tan/log/exp/history/class/degree.
- Parametrized edges: div(1,0)->ZeroDivisionError, sqrt(-1)->ValueError, log(-1/0/base=1)->ValueError, exp(1000)->OverflowError (propagated), sin(pi/2)~=1 via pytest.approx, degree sin(30)=0.5.
- History: length checks, shallow copy immutability, clear, global+instance dual-write (test_chained_history).
- Tolerance: pytest.approx / math.isclose rel_tol 1e-9.
- No extra suites (CLI, persistence round-trip) — out of scope for v1.

## 4. README Outline

1. Title + one-line summary
2. Executive Summary (table: functions/class/tests/deps/python)
3. Features (arithmetic/power/trig/log/history/CLI/class)
4. Quick Start (pip install, --help, pytest -v, Python snippet)
5. CLI Examples (history, deg flag)
6. Project Structure
7. Auto-Orchestration table (plan/build/review/UI agents)
8. Testing section
9. Error Handling table (ZeroDivision/ValueError/OverflowError)
10. Review Checklist (5 items), License MIT

Save to outputs/ with YYYY-MM-DD prefix, v1, no overwrite.

## 5. Git + GitHub Plan

```bash
mkdir -p /tmp/sci-calc-20260903
# write calculator.py, test_calculator.py, requirements.txt, .gitignore, README.md
cd /tmp/sci-calc-20260903
git init -b main
git config user.name "Rituparno Majumdar" ; git config user.email "rituparno.majumdar@github.com"
git add calculator.py test_calculator.py requirements.txt README.md .gitignore
git commit -m "feat: scientific calculator v1 — add,sub,mul,div,pow,sqrt,sin,cos,tan,log,exp,history + class + CLI"
gh repo create Rituparno-Majumdar/sci-calc-20260903 --public --description "Scientific calculator — Python (12 functions) — auto-orchestrated 2026-09-03"
git remote add origin https://github.com/Rituparno-Majumdar/sci-calc-20260903.git
git push -u origin main
gh repo view Rituparno-Majumdar/sci-calc-20260903 --jq '{name, html_url, private}'
gh api repos/Rituparno-Majumdar/sci-calc-20260903 --jq .
```

Verification: `python3 -m pytest -v` 14 passed, `python3 calculator.py --help` lists 13 commands, `gh repo view` returns public URL.

## 6. Efficiency & Non-Goals

- Efficiency: flat single file, use stdlib math only, float coercion via float(), click+rich optional import with fallback.
- Not in scope: package split, SQLite, timestamps, tan asymptote guard, complex cmath, encryption/sync, coverage gating.

## Review Checklist
- [ ] All 12 functions signatures match spec
- [ ] Tests 14 pass, history shallow-copy verified
- [ ] Degree/radian conversion only at I/O boundary
- [ ] No scope widening (no extra deps/files)
- [ ] GitHub repo public and push verified

## Totals Row
| Artifact | Count |
|---|---|
| Spec functions | 12 |
| Tests | 14 |
| Files (core) | 5 |
| Lines calculator.py | ~401 |
