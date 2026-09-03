"""Tests for factorial(n) — module + class + history + CLI"""
import math
import pytest
import calculator as calc
from calculator import ScientificCalculator


@pytest.fixture(autouse=True)
def clear():
    calc.clear_history()
    yield
    calc.clear_history()


def test_factorial_zero():
    assert calc.factorial(0) == 1.0
    assert isinstance(calc.factorial(0), float)
    # also float int-like
    assert calc.factorial(0.0) == 1.0
    # class parity
    c = ScientificCalculator()
    assert c.factorial(0) == 1.0
    # history recorded
    h = calc.history()
    # last entry should be factorial
    assert any(e["op"] == "factorial" and e["args"] == (0,) and e["result"] == 1.0 for e in h)


def test_factorial_one():
    assert calc.factorial(1) == 1.0
    assert calc.factorial(1.0) == 1.0
    c = ScientificCalculator()
    assert c.factorial(1) == 1.0
    assert isinstance(c.factorial(5.0), float)


def test_factorial_five():
    assert calc.factorial(5) == 120.0
    assert calc.factorial(5.0) == 120.0
    c = ScientificCalculator()
    assert c.factorial(5) == 120.0
    # history args preservation
    calc.clear_history()
    calc.factorial(5)
    h = calc.history()
    assert h[-1]["op"] == "factorial"
    assert h[-1]["args"] == (5,)
    assert h[-1]["result"] == 120.0
    # class history parity
    c2 = ScientificCalculator()
    c2.factorial(5)
    assert c2.get_history()[-1]["op"] == "factorial"
    assert c2.get_history()[-1]["result"] == 120.0


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        calc.factorial(-1)
    with pytest.raises(ValueError):
        calc.factorial(-5)
    with pytest.raises(ValueError):
        calc.factorial(-1.0)
    c = ScientificCalculator()
    with pytest.raises(ValueError):
        c.factorial(-1)
    with pytest.raises(ValueError):
        c.factorial(-3.0)


def test_factorial_non_int_raises():
    with pytest.raises(ValueError):
        calc.factorial(3.5)
    with pytest.raises(ValueError):
        calc.factorial(2.1)
    with pytest.raises(TypeError):
        calc.factorial("5")
    with pytest.raises(TypeError):
        calc.factorial(None)
    with pytest.raises(TypeError):
        calc.factorial([5])
    c = ScientificCalculator()
    with pytest.raises(ValueError):
        c.factorial(4.2)
    with pytest.raises(TypeError):
        c.factorial("foo")
