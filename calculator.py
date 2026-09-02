"""
Scientific Calculator — sci-calc-20260903
Author: Rituparno Majumdar
Date: 2026-09-03
Version: v1

Functions: add, sub, mul, div, pow, sqrt, sin, cos, tan, log, exp, history
- Pure module-level functions + ScientificCalculator class
- History tracking with rich metadata
- Degree/radian toggle for trig
- Robust error handling
"""

from __future__ import annotations

import math
from typing import List, Dict, Any, Union

Number = Union[int, float]

# ── History store ──────────────────────────────────────────────────────────
_history: List[Dict[str, Any]] = []
_trig_in_degrees: bool = False  # global toggle; class instance can override


def _record(op: str, args: tuple, result: Any) -> None:
    """Append entry to global history."""
    _history.append({"op": op, "args": args, "result": result})


def set_degree_mode(enabled: bool = True) -> None:
    """Toggle trig functions between degrees (True) and radians (False)."""
    global _trig_in_degrees
    _trig_in_degrees = enabled


def is_degree_mode() -> bool:
    return _trig_in_degrees


def _to_radians(x: Number) -> float:
    return math.radians(float(x)) if _trig_in_degrees else float(x)


# ── Core arithmetic ────────────────────────────────────────────────────────
def add(a: Number, b: Number) -> float:
    """Add two numbers."""
    result = float(a) + float(b)
    _record("add", (a, b), result)
    return result


def sub(a: Number, b: Number) -> float:
    """Subtract b from a."""
    result = float(a) - float(b)
    _record("sub", (a, b), result)
    return result


def mul(a: Number, b: Number) -> float:
    """Multiply two numbers."""
    result = float(a) * float(b)
    _record("mul", (a, b), result)
    return result


def div(a: Number, b: Number) -> float:
    """Divide a by b. Raises ZeroDivisionError on b==0."""
    if float(b) == 0:
        raise ZeroDivisionError("division by zero")
    result = float(a) / float(b)
    _record("div", (a, b), result)
    return result


def pow(a: Number, b: Number) -> float:  # noqa: A001  shadow built-in
    """Raise a to the power b (a**b)."""
    result = math.pow(float(a), float(b))
    _record("pow", (a, b), result)
    return result


def sqrt(a: Number) -> float:
    """Square root of a. Raises ValueError for negative input."""
    if float(a) < 0:
        raise ValueError("sqrt domain error: negative input")
    result = math.sqrt(float(a))
    _record("sqrt", (a,), result)
    return result


# ── Transcendental ─────────────────────────────────────────────────────────
def sin(a: Number) -> float:
    """Sine of a (radians by default; toggle via set_degree_mode)."""
    result = math.sin(_to_radians(a))
    _record("sin", (a,), result)
    return result


def cos(a: Number) -> float:
    """Cosine of a (radians by default)."""
    result = math.cos(_to_radians(a))
    _record("cos", (a,), result)
    return result


def tan(a: Number) -> float:
    """Tangent of a (radians by default)."""
    result = math.tan(_to_radians(a))
    _record("tan", (a,), result)
    return result


def log(a: Number, base: Number = math.e) -> float:
    """
    Logarithm of a with given base (default e → natural log).
    Raises ValueError for non-positive a or invalid base.
    """
    a_f, b_f = float(a), float(base)
    if a_f <= 0:
        raise ValueError("log domain error: a must be > 0")
    if b_f <= 0 or b_f == 1:
        raise ValueError("log domain error: base must be >0 and !=1")
    if b_f == math.e:
        result = math.log(a_f)
    elif b_f == 10:
        result = math.log10(a_f)
    else:
        result = math.log(a_f, b_f)
    _record("log", (a, base), result)
    return result


def exp(a: Number) -> float:
    """e raised to a (exp(a))."""
    result = math.exp(float(a))
    _record("exp", (a,), result)
    return result


# ── History API ────────────────────────────────────────────────────────────
def history() -> List[Dict[str, Any]]:
    """Return shallow copy of operation history."""
    return list(_history)


def clear_history() -> None:
    """Clear global history."""
    _history.clear()


def get_history() -> List[Dict[str, Any]]:
    """Alias for history() — compatibility."""
    return history()


# ── Class wrapper (stateful, instance history + degree toggle) ────────────
class ScientificCalculator:
    """Stateful calculator with instance history and degree/radian mode."""

    def __init__(self, degree_mode: bool = False):
        self.history: List[Dict[str, Any]] = []
        self.degree_mode = degree_mode

    def _radians(self, x: Number) -> float:
        return math.radians(float(x)) if self.degree_mode else float(x)

    def _rec(self, op: str, args: tuple, result: Any) -> None:
        entry = {"op": op, "args": args, "result": result}
        self.history.append(entry)
        _record(op, args, result)

    # arithmetic
    def add(self, a: Number, b: Number) -> float:
        r = float(a) + float(b)
        self._rec("add", (a, b), r)
        return r

    def sub(self, a: Number, b: Number) -> float:
        r = float(a) - float(b)
        self._rec("sub", (a, b), r)
        return r

    def mul(self, a: Number, b: Number) -> float:
        r = float(a) * float(b)
        self._rec("mul", (a, b), r)
        return r

    def div(self, a: Number, b: Number) -> float:
        if float(b) == 0:
            raise ZeroDivisionError("division by zero")
        r = float(a) / float(b)
        self._rec("div", (a, b), r)
        return r

    def pow(self, a: Number, b: Number) -> float:
        r = math.pow(float(a), float(b))
        self._rec("pow", (a, b), r)
        return r

    def sqrt(self, a: Number) -> float:
        if float(a) < 0:
            raise ValueError("sqrt domain error: negative input")
        r = math.sqrt(float(a))
        self._rec("sqrt", (a,), r)
        return r

    def sin(self, a: Number) -> float:
        r = math.sin(self._radians(a))
        self._rec("sin", (a,), r)
        return r

    def cos(self, a: Number) -> float:
        r = math.cos(self._radians(a))
        self._rec("cos", (a,), r)
        return r

    def tan(self, a: Number) -> float:
        r = math.tan(self._radians(a))
        self._rec("tan", (a,), r)
        return r

    def log(self, a: Number, base: Number = math.e) -> float:
        a_f, b_f = float(a), float(base)
        if a_f <= 0:
            raise ValueError("log domain error: a must be > 0")
        if b_f <= 0 or b_f == 1:
            raise ValueError("log domain error: base must be >0 and !=1")
        r = math.log(a_f, b_f) if b_f != math.e else math.log(a_f)
        if b_f == 10:
            r = math.log10(a_f)
        self._rec("log", (a, base), r)
        return r

    def exp(self, a: Number) -> float:
        r = math.exp(float(a))
        self._rec("exp", (a,), r)
        return r

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self.history)

    def clear_history(self) -> None:
        self.history.clear()

    def set_degree_mode(self, enabled: bool = True) -> None:
        self.degree_mode = enabled

    # alias so module-level history() also accessible via instance
    def history_alias(self) -> List[Dict[str, Any]]:
        return self.get_history()


# ── CLI (click + rich) ─────────────────────────────────────────────────────
try:
    import click
    from rich.console import Console
    from rich.table import Table

    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None  # type: ignore

if HAS_RICH:

    @click.group()
    def cli():
        """Scientific Calculator CLI — sci-calc-20260903"""
        pass

    @cli.command()
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    def add_cmd(a, b):
        console.print(f"[green]add({a}, {b}) = {add(a,b)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    def sub_cmd(a, b):
        console.print(f"[green]sub({a}, {b}) = {sub(a,b)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    def mul_cmd(a, b):
        console.print(f"[green]mul({a}, {b}) = {mul(a,b)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    def div_cmd(a, b):
        console.print(f"[green]div({a}, {b}) = {div(a,b)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    def pow_cmd(a, b):
        console.print(f"[green]pow({a}, {b}) = {pow(a,b)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    def sqrt_cmd(a):
        console.print(f"[green]sqrt({a}) = {sqrt(a)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    @click.option("--deg", is_flag=True, help="Input in degrees")
    def sin_cmd(a, deg):
        if deg:
            set_degree_mode(True)
        console.print(f"[green]sin({a}) = {sin(a)}[/green]")
        if deg:
            set_degree_mode(False)

    @cli.command()
    @click.argument("a", type=float)
    @click.option("--deg", is_flag=True)
    def cos_cmd(a, deg):
        if deg:
            set_degree_mode(True)
        console.print(f"[green]cos({a}) = {cos(a)}[/green]")
        if deg:
            set_degree_mode(False)

    @cli.command()
    @click.argument("a", type=float)
    @click.option("--deg", is_flag=True)
    def tan_cmd(a, deg):
        if deg:
            set_degree_mode(True)
        console.print(f"[green]tan({a}) = {tan(a)}[/green]")
        if deg:
            set_degree_mode(False)

    @cli.command()
    @click.argument("a", type=float)
    @click.option("--base", default=math.e, type=float, help="Log base (default e)")
    def log_cmd(a, base):
        console.print(f"[green]log({a}, base={base}) = {log(a, base)}[/green]")

    @cli.command()
    @click.argument("a", type=float)
    def exp_cmd(a):
        console.print(f"[green]exp({a}) = {exp(a)}[/green]")

    @cli.command()
    def history_cmd():
        h = history()
        if not h:
            console.print("[yellow]No history yet.[/yellow]")
            return
        table = Table(title="Calculation History")
        table.add_column("#", style="dim")
        table.add_column("Operation")
        table.add_column("Args")
        table.add_column("Result", style="green")
        for i, e in enumerate(h, 1):
            table.add_row(str(i), e["op"], str(e["args"]), str(e["result"]))
        console.print(table)

    @cli.command()
    def clear_cmd():
        clear_history()
        console.print("[yellow]History cleared.[/yellow]")


if __name__ == "__main__":
    if HAS_RICH:
        cli()
    else:
        # Fallback REPL when click/rich not installed
        print("Scientific Calculator REPL — type 'help' or 'exit'")
        calc = ScientificCalculator()
        while True:
            try:
                expr = input("calc> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nbye")
                break
            if expr in ("exit", "quit", "q"):
                break
            if expr == "help":
                print("Functions: add(a,b) sub(a,b) mul(a,b) div(a,b) pow(a,b) sqrt(a) sin(a) cos(a) tan(a) log(a,base=e) exp(a) history() clear_history()")
                continue
            if expr == "history":
                print(calc.get_history() or history())
                continue
            if expr == "clear":
                clear_history()
                calc.clear_history()
                print("cleared")
                continue
            try:
                # safe eval with limited globals
                allowed = {"add": add, "sub": sub, "mul": mul, "div": div, "pow": pow, "sqrt": sqrt, "sin": sin, "cos": cos, "tan": tan, "log": log, "exp": exp, "math": math}
                print(eval(expr, {"__builtins__": {}}, allowed))
            except Exception as e:
                print(f"Error: {e}")
