# Initial Code Review — Advanced Scientific Calculator

## Executive Summary

The initial constants module imports and compiles successfully. The duplicate proton-mass declaration has been corrected and regression coverage added. The calculator engine and user interface have not yet been added, so functional and security review of expression evaluation remains pending until implementation exists.

## Findings

| Severity | Location | Finding | Recommendation |
|---|---|---|---|
| Resolved | `calculator/constants.py` | `mp` was initially declared as `1.67262192369e-31`, then mutated below the dictionary. | Declared `mp` once as `1.67262192369e-27` and removed the mutation. |
| Pending | Project-wide | No parser/evaluator or test cases exist yet. | Review the evaluator for AST allow-listing (never unrestricted `eval`), domain errors, overflow, units, and regression tests when added. |

## Verification Performed

| Check | Result |
|---|---|
| Python bytecode compilation | Pass (`python3 -m compileall`) |
| Constants import | Pass |
| Proton-mass runtime invariant | Pass (`mp == 1.67262192369e-27`) |
| Automated test suite | Added (`tests/test_constants.py`) |
| **Totals** | **1 resolved finding; 3 checks passed; 1 review area pending implementation** |

## Review Checklist

- [x] Consolidate the proton mass into one accurate declaration.
- [ ] Add a restricted expression parser before accepting arbitrary input.
- [ ] Add tests for arithmetic, trigonometry modes, invalid domains, overflow, and malformed expressions.
- [ ] Re-run the review when the engine and interface are available.
