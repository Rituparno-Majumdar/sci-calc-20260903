"""
ui.py — Lightweight UI layer for calculator.py (apy UI proposal)
Path: /tmp/sci-calc-20260903/ui.py
Does NOT modify calculator.py. Import calculator and add presentation.
< 400 lines; click+rich enhanced + rich history table.
"""
from __future__ import annotations

import math
from pathlib import Path

# rich is required for history table; click optional for CLI enhancements
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None  # type: ignore

import calculator as calc

# ── 1) Rich history table (reusable) ─────────────────────────────────────
def history_table(entries=None, title="Calculation History") -> Table | str:
    """Return rich Table for history entries; fallback to plain text."""
    if entries is None:
        entries = calc.history()
    if not HAS_RICH:
        if not entries:
            return "No history yet."
        lines = [f"{i}. {e['op']}{e['args']} = {e['result']}" for i, e in enumerate(entries, 1)]
        return "\n".join(lines)
    table = Table(title=title, show_lines=False, header_style="bold magenta")
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Op", style="cyan", no_wrap=True)
    table.add_column("Args", style="white")
    table.add_column("Result", style="bold green", justify="right")
    if not entries:
        table.add_row("-", "-", "-", "[yellow]empty[/yellow]")
        return table
    for i, e in enumerate(entries, 1):
        args_s = ", ".join(str(a) for a in e["args"])
        # highlight errors if any (stored result could be exception string)
        res_s = f"{e['result']:.6g}" if isinstance(e["result"], float) else str(e["result"])
        table.add_row(str(i), e["op"], f"({args_s})", res_s)
    return table


def render_history(entries=None) -> None:
    """Print history table to console (or stdout fallback)."""
    t = history_table(entries)
    if HAS_RICH:
        console.print(t)
        console.print(f"[dim]Total: {len(entries or calc.history())} entries[/dim]")
    else:
        print(t)


def banner() -> None:
    if HAS_RICH:
        console.print(Panel(Text("sci-calc-20260903 — Scientific Calculator", justify="center", style="bold white on blue"), subtitle="add sub mul div pow sqrt sin cos tan log exp | history"))
    else:
        print("sci-calc-20260903 — Scientific Calculator")


# ── 2) Click+rich CLI enhancements (importable group) ─────────────────────
# Suggested file: /tmp/sci-calc-20260903/cli_enhanced.py or extend ui.py
# Usage: python ui.py calc add 2 3
#        python ui.py history --limit 5
try:
    import click

    @click.group(help="Enhanced CLI — wraps calculator.py with rich output, --deg, --precision, --dry-run")
    @click.option("--deg", is_flag=True, help="Trig inputs in degrees (global)")
    @click.option("--precision", default=6, type=int, help="Float display precision")
    @click.option("--dry-run", is_flag=True, help="Show what would run without executing")
    @click.pass_context
    def cli(ctx, deg, precision, dry_run):
        ctx.ensure_object(dict)
        ctx.obj["deg"] = deg
        ctx.obj["precision"] = precision
        ctx.obj["dry_run"] = dry_run
        if deg:
            calc.set_degree_mode(True)

    def _fmt(v, prec):
        return f"{v:.{prec}g}" if isinstance(v, float) else str(v)

    def _run(fn, args, ctx):
        if ctx.obj["dry_run"]:
            if HAS_RICH:
                console.print(f"[yellow][dry-run][/yellow] {fn.__name__}{args}")
            else:
                print(f"[dry-run] {fn.__name__}{args}")
            return
        try:
            res = fn(*args)
            if HAS_RICH:
                console.print(f"[green]{fn.__name__}{args} = {_fmt(res, ctx.obj['precision'])}[/green]")
            else:
                print(f"{fn.__name__}{args} = {res}")
        except Exception as e:
            if HAS_RICH:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")
            raise click.ClickException(str(e))

    @cli.command("add")
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    @click.pass_context
    def add_cmd(ctx, a, b):
        _run(calc.add, (a, b), ctx)

    @cli.command("sub")
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    @click.pass_context
    def sub_cmd(ctx, a, b):
        _run(calc.sub, (a, b), ctx)

    @cli.command("mul")
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    @click.pass_context
    def mul_cmd(ctx, a, b):
        _run(calc.mul, (a, b), ctx)

    @cli.command("div")
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    @click.pass_context
    def div_cmd(ctx, a, b):
        _run(calc.div, (a, b), ctx)

    @cli.command("pow")
    @click.argument("a", type=float)
    @click.argument("b", type=float)
    @click.pass_context
    def pow_cmd(ctx, a, b):
        _run(calc.pow, (a, b), ctx)

    @cli.command("sqrt")
    @click.argument("a", type=float)
    @click.pass_context
    def sqrt_cmd(ctx, a):
        _run(calc.sqrt, (a,), ctx)

    @cli.command("sin")
    @click.argument("a", type=float)
    @click.pass_context
    def sin_cmd(ctx, a):
        _run(calc.sin, (a,), ctx)

    @cli.command("cos")
    @click.argument("a", type=float)
    @click.pass_context
    def cos_cmd(ctx, a):
        _run(calc.cos, (a,), ctx)

    @cli.command("tan")
    @click.argument("a", type=float)
    @click.pass_context
    def tan_cmd(ctx, a):
        _run(calc.tan, (a,), ctx)

    @cli.command("log")
    @click.argument("a", type=float)
    @click.option("--base", default=math.e, type=float)
    @click.pass_context
    def log_cmd(ctx, a, base):
        _run(calc.log, (a, base), ctx)

    @cli.command("exp")
    @click.argument("a", type=float)
    @click.pass_context
    def exp_cmd(ctx, a):
        _run(calc.exp, (a,), ctx)

    @cli.command("history")
    @click.option("--limit", default=0, type=int, help="Last N entries (0=all)")
    @click.option("--clear", is_flag=True, help="Clear after showing")
    def history_cmd(limit, clear):
        entries = calc.history()
        if limit > 0:
            entries = entries[-limit:]
        render_history(entries)
        if clear:
            calc.clear_history()
            if HAS_RICH:
                console.print("[yellow]History cleared.[/yellow]")

    @cli.command("repl")
    @click.option("--deg", is_flag=True)
    def repl_cmd(deg):
        if deg:
            calc.set_degree_mode(True)
        banner()
        c = calc.ScientificCalculator(degree_mode=bool(deg))
        while True:
            try:
                s = input("calc> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nbye")
                break
            if s in ("q", "quit", "exit"):
                break
            if s == "history":
                render_history()
                continue
            if s == "clear":
                calc.clear_history()
                c.clear_history()
                print("cleared")
                continue
            if s in ("help", "?"):
                print("add sub mul div pow sqrt sin cos tan log exp | history clear | q")
                continue
            try:
                allowed = {"add": calc.add, "sub": calc.sub, "mul": calc.mul, "div": calc.div, "pow": calc.pow, "sqrt": calc.sqrt, "sin": calc.sin, "cos": calc.cos, "tan": calc.tan, "log": calc.log, "exp": calc.exp, "math": math, "history": calc.history}
                r = eval(s, {"__builtins__": {}}, allowed)
                if HAS_RICH:
                    console.print(f"[green]= {r}[/green]")
                else:
                    print(r)
            except Exception as e:
                print(f"Error: {e}")

    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False
    cli = None  # type: ignore

# ── 3) File-path suggestions (docstring for parent) ───────────────────────
# /tmp/sci-calc-20260903/ui.py          -> this file (rich table + enhanced CLI)
# /tmp/sci-calc-20260903/app.py         -> Streamlit web UI (sketch below, <120 lines)
# /tmp/sci-calc-20260903/tk_app.py      -> Tkinter desktop fallback (sketch below)
# Keep calculator.py untouched; UI layers import it.

if __name__ == "__main__":
    if HAS_CLICK and cli:
        cli()
    else:
        banner()
        render_history()
