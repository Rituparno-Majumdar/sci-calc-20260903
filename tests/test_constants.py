"""Regression tests for constants.py — proton-mass invariant"""
import pathlib
import pytest
import constants

def test_proton_mass_value():
    """mp must be CODATA 2018 1.67262192369e-27 exactly."""
    assert constants.PHYSICAL_CONSTANTS["mp"] == 1.67262192369e-27
    assert constants.ALLOWED_CONSTS["mp"] == 1.67262192369e-27

def test_proton_mass_single_declaration_no_mutation():
    """File must declare mp once in PHYSICAL_CONSTANTS and not mutate it below."""
    p = pathlib.Path(__file__).parent.parent / "constants.py"
    text = p.read_text(encoding="utf-8")
    # exactly one dictionary entry for mp value (description entry is separate)
    assert text.count('"mp": 1.67262192369e-27') == 1, f'expected single mp value declaration' 
    # no post-dict mutation like ALLOWED_CONSTS["mp"] = or PHYSICAL_CONSTANTS["mp"] =
    # allow only the two legitimate dict definitions and the Unicode aliases block
    lines = text.splitlines()
    # find lines that assign mp outside the PHYSICAL_CONSTANTS dict literal
    # PHYSICAL_CONSTANTS dict ends at "}"
    # Any line containing ALLOWED_CONSTS["mp"] would be a mutation
    assert 'ALLOWED_CONSTS["mp"]' not in text
    assert "ALLOWED_CONSTS['mp']" not in text
    # ensure the wrong exponent -31 is absent
    assert "1.67262192369e-31" not in text

def test_proton_mass_not_wrong_exponent():
    """Ensure the historic wrong value 1.67262192369e-31 is absent at runtime."""
    assert constants.PHYSICAL_CONSTANTS["mp"] != 1.67262192369e-31
    assert constants.PHYSICAL_CONSTANTS["mp"] == pytest.approx(1.67262192369e-27)

def test_allowed_consts_completeness():
    """ALLOWED_CONSTS merges mathematical + physical, unicode aliases present."""
    assert "pi" in constants.ALLOWED_CONSTS
    assert "c" in constants.ALLOWED_CONSTS
    assert "π" in constants.ALLOWED_CONSTS
    assert constants.ALLOWED_CONSTS["π"] == constants.ALLOWED_CONSTS["pi"]

def test_list_and_describe_constants():
    allc = constants.list_constants()
    assert isinstance(allc, dict)
    assert "mp" in allc
    desc = constants.describe_constants()
    assert any(name == "mp" for name, _, _ in desc)

def test_other_physical_constants_sanity():
    """Sanity checks for neighbouring constants to catch accidental edits."""
    assert constants.PHYSICAL_CONSTANTS["me"] == 9.1093837015e-31
    assert constants.PHYSICAL_CONSTANTS["mn"] == 1.67492749804e-27
    assert constants.PHYSICAL_CONSTANTS["c"] == 299792458.0


def test_is_mp_correct_helper():
    """is_mp_correct() returns True for correct CODATA value."""
    assert constants.is_mp_correct() is True
    assert constants.is_mp_correct() == (constants.PHYSICAL_CONSTANTS["mp"] == 1.67262192369e-27)
