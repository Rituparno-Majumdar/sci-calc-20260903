"""
app.py — Optional Streamlit web UI sketch for calculator.py
Path: /tmp/sci-calc-20260903/app.py
Run: streamlit run app.py
Fallback: python app.py --tk  (launches Tkinter if streamlit missing)
Under 120 lines; imports calculator.py only.
"""
from __future__ import annotations

import math
import sys

import calculator as calc

# ── Streamlit UI (if installed) ──────────────────────────────────────────
def run_streamlit():
    import streamlit as st

    st.set_page_config(page_title="sci-calc-20260903", layout="centered")
    st.title("🔬 sci-calc-20260903 — Scientific Calculator")
    st.caption("add · sub · mul · div · pow · sqrt · sin · cos · tan · log · exp · history")

    deg = st.toggle("Degree mode (trig in °)", value=False)
    calc.set_degree_mode(bool(deg))

    col1, col2 = st.columns(2)
    with col1:
        op = st.selectbox("Operation", ["add", "sub", "mul", "div", "pow", "sqrt", "sin", "cos", "tan", "log", "exp"])
    with col2:
        prec = st.slider("Precision", 2, 12, 6)

    a = st.number_input("a", value=0.0, format="%.6f")
    b = None
    base = math.e
    if op in ("add", "sub", "mul", "div", "pow"):
        b = st.number_input("b", value=0.0, format="%.6f")
    if op == "log":
        base = st.number_input("base", value=math.e, format="%.6f", help="default e")

    if st.button("Calculate", type="primary"):
        try:
            fn = {"add": calc.add, "sub": calc.sub, "mul": calc.mul, "div": calc.div, "pow": calc.pow, "sqrt": calc.sqrt, "sin": calc.sin, "cos": calc.cos, "tan": calc.tan, "log": calc.log, "exp": calc.exp}[op]
            args = (a, b) if b is not None else (a, base) if op == "log" else (a,)
            # log needs (a, base)
            if op == "log":
                res = calc.log(a, base)
            else:
                res = fn(*args)  # type: ignore
            st.success(f"{op}{tuple(args)} = {res:.{prec}g}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()
    st.subheader("History")
    hist = calc.history()
    if not hist:
        st.info("No history yet.")
    else:
        # Use rich-like table via st.table
        import pandas as pd
        df = pd.DataFrame([{"#": i + 1, "op": e["op"], "args": str(e["args"]), "result": e["result"]} for i, e in enumerate(hist)])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(hist)}")
    if st.button("Clear history"):
        calc.clear_history()
        st.rerun()

# ── Tkinter fallback (desktop, no extra deps) ────────────────────────────
def run_tkinter():
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("sci-calc-20260903")
    root.geometry("420x520")

    ttk.Label(root, text="sci-calc-20260903 — Scientific Calculator", font=("TkDefaultFont", 11, "bold")).pack(pady=8)

    deg_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(root, text="Degree mode", variable=deg_var, command=lambda: calc.set_degree_mode(deg_var.get())).pack()

    op_var = tk.StringVar(value="add")
    ttk.OptionMenu(root, op_var, "add", "add", "sub", "mul", "div", "pow", "sqrt", "sin", "cos", "tan", "log", "exp").pack(pady=6)

    frm = ttk.Frame(root)
    frm.pack(pady=4)
    ttk.Label(frm, text="a").grid(row=0, column=0)
    a_entry = ttk.Entry(frm, width=14)
    a_entry.grid(row=0, column=1, padx=4)
    ttk.Label(frm, text="b / base").grid(row=0, column=2)
    b_entry = ttk.Entry(frm, width=14)
    b_entry.grid(row=0, column=3, padx=4)
    a_entry.insert(0, "0")
    b_entry.insert(0, "0")

    res_var = tk.StringVar(value="Result: —")
    ttk.Label(root, textvariable=res_var, font=("TkDefaultFont", 10, "bold")).pack(pady=8)

    def do_calc():
        try:
            a = float(a_entry.get())
            b_s = b_entry.get()
            op = op_var.get()
            m = {"add": calc.add, "sub": calc.sub, "mul": calc.mul, "div": calc.div, "pow": calc.pow, "sqrt": calc.sqrt, "sin": calc.sin, "cos": calc.cos, "tan": calc.tan, "exp": calc.exp}
            if op == "log":
                base = float(b_s) if b_s else math.e
                r = calc.log(a, base)
            elif op in m:
                if op in ("add", "sub", "mul", "div", "pow"):
                    r = m[op](a, float(b_s))
                else:
                    r = m[op](a)
            else:
                r = "?"
            res_var.set(f"Result: {r:.6g}" if isinstance(r, float) else f"Result: {r}")
            refresh_hist()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(root, text="Calculate", command=do_calc).pack(pady=6)

    hist_box = tk.Listbox(root, height=12)
    hist_box.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh_hist():
        hist_box.delete(0, tk.END)
        for i, e in enumerate(calc.history(), 1):
            hist_box.insert(tk.END, f"{i}. {e['op']}{e['args']} = {e['result']:.6g}" if isinstance(e["result"], float) else f"{i}. {e['op']}{e['args']} = {e['result']}")

    def clear_hist():
        calc.clear_history()
        refresh_hist()

    ttk.Button(root, text="Clear history", command=clear_hist).pack(pady=4)
    refresh_hist()
    root.mainloop()


if __name__ == "__main__":
    if "--tk" in sys.argv:
        run_tkinter()
    else:
        try:
            import streamlit  # noqa: F401
            run_streamlit()
        except ImportError:
            print("streamlit not installed — falling back to Tkinter (or run: pip install streamlit). Use --tk to force Tkinter.")
            try:
                run_tkinter()
            except Exception as e:
                print(f"Tkinter failed: {e}")
                print("CLI fallback: python ui.py add 2 3  or  python calculator.py --help")
