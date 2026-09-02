"""Tests for Scientific Calculator — sci-calc-20260903"""
import math
import pytest
import calculator as calc
from calculator import ScientificCalculator


@pytest.fixture(autouse=True)
def clear():
    calc.clear_history()
    yield
    calc.clear_history()


def test_add():
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0


def test_sub():
    assert calc.sub(5, 2) == 3
    assert calc.sub(0, 5) == -5


def test_mul():
    assert calc.mul(3, 4) == 12
    assert calc.mul(-2, 3) == -6


def test_div():
    assert calc.div(10, 2) == 5
    with pytest.raises(ZeroDivisionError):
        calc.div(1, 0)


def test_pow():
    assert calc.pow(2, 8) == 256
    assert calc.pow(9, 0.5) == 3


def test_sqrt():
    assert calc.sqrt(16) == 4
    assert calc.sqrt(0) == 0
    with pytest.raises(ValueError):
        calc.sqrt(-1)


def test_sin_cos_tan_radian():
    assert calc.sin(0) == pytest.approx(0, abs=1e-9)
    assert calc.cos(0) == pytest.approx(1, abs=1e-9)
    assert calc.tan(0) == pytest.approx(0, abs=1e-9)
    assert calc.sin(math.pi / 2) == pytest.approx(1, abs=1e-9)


def test_sin_degree_mode():
    calc.set_degree_mode(True)
    assert calc.sin(30) == pytest.approx(0.5, abs=1e-9)
    assert calc.cos(60) == pytest.approx(0.5, abs=1e-9)
    calc.set_degree_mode(False)


def test_log():
    assert calc.log(10, 10) == pytest.approx(1)
    assert calc.log(math.e) == pytest.approx(1)
    assert calc.log(8, 2) == pytest.approx(3)
    with pytest.raises(ValueError):
        calc.log(-1)
    with pytest.raises(ValueError):
        calc.log(10, 1)
    with pytest.raises(ValueError):
        calc.log(10, -2)


def test_exp():
    assert calc.exp(0) == pytest.approx(1)
    assert calc.exp(1) == pytest.approx(math.e)


def test_history():
    calc.add(1, 1)
    calc.mul(2, 3)
    h = calc.history()
    assert len(h) == 2
    assert h[0]["op"] == "add"
    assert h[1]["result"] == 6
    calc.clear_history()
    assert calc.history() == []


def test_class_calculator():
    c = ScientificCalculator()
    assert c.add(2, 2) == 4
    assert c.div(10, 2) == 5
    with pytest.raises(ZeroDivisionError):
        c.div(1, 0)
    assert len(c.get_history()) == 2
    c.clear_history()
    assert c.get_history() == []


def test_class_degree_mode():
    c = ScientificCalculator(degree_mode=True)
    assert c.sin(90) == pytest.approx(1, abs=1e-9)
    c.set_degree_mode(False)
    assert c.sin(math.pi / 2) == pytest.approx(1, abs=1e-9)


def test_chained_history_global_and_instance():
    c = ScientificCalculator()
    c.add(1, 2)
    assert len(c.get_history()) == 1
    assert len(calc.history()) == 1
    calc.add(5, 5)
    assert len(calc.history()) == 2
