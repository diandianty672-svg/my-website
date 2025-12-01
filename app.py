# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import sympify, symbols, lambdify
from math import isfinite

st.set_page_config(page_title="Bisection Solver", layout="centered")

st.title("Solusi Persamaan Non-Linear (Metode Bisection)")
st.write("Masukkan fungsi f(x), interval [a,b], toleransi, dan maksimal iterasi.")

# Input pengguna
expr_input = st.text_input("Masukkan f(x) (contoh: x**3 - 2*x - 5)", value="x**3 - 2*x - 5")
col1, col2 = st.columns(2)
with col1:
    a_input = st.text_input("a (kiri)", value="-5")
    b_input = st.text_input("b (kanan)", value="5")
with col2:
    tol_input = st.text_input("Toleransi (contoh: 1e-6)", value="1e-6")
    maxiter_input = st.text_input("Max iterasi", value="50")

solve_btn = st.button("Solve (Bisection)")

# Helper: parse numeric safely
def to_float(s):
    try:
        return float(s)
    except:
        return None

if solve_btn:
    # parse numeric inputs
    a = to_float(a_input)
    b = to_float(b_input)
    try:
        tol = float(tol_input)
    except:
        tol = None
    try:
        maxiter = int(maxiter_input)
    except:
        maxiter = None

    # Validasi input dasar
    if a is None or b is None:
        st.error("Nilai a atau b tidak valid. Pastikan angka valid (mis. -1.5 atau 2).")
    elif tol is None or tol <= 0:
        st.error("Toleransi tidak valid. Gunakan angka positif kecil, mis. 1e-6.")
    elif maxiter is None or maxiter <= 0:
        st.error("Max iterasi tidak valid. Gunakan integer positif.")
    else:
        # Parse fungsi menggunakan sympy -> lambdify
        x = symbols('x')
        try:
            expr = sympify(expr_input)
            f = lambdify(x, expr, 'numpy')  # menggunakan numpy
            # quick check evaluate
            fa = f(a)
            fb = f(b)
            # ensure finite
            if not (isfinite(fa) and isfinite(fb)):
                st.error("Evaluasi f(a) atau f(b) menghasilkan nilai tak terhingga atau NaN.")
            else:
                if fa * fb > 0:
                    st.error(f"f(a)*f(b) = {fa*fb:.4g} > 0. Metode Bisection memerlukan tanda berbeda pada kedua ujung.")
                    st.info("Coba interval lain atau cek apakah ada akar ganda (even multiplicity).")
                else:
                    # jalankan bisection
                    rows = []
                    left, right = a, b
                    root = None
                    for k in range(1, maxiter+1):
                        m = 0.5*(left+right)
                        fm = f(m)
                        # record iterasi
                        rows.append({"iter": k, "a": left, "b": right, "m": m, "f(m)": float(fm)})
                        # cek konvergensi
                        if not isfinite(fm):
                            st.warning(f"f(m) bukan finite di iterasi {k}. Hentikan.")
                            break
                        # berhenti jika nilai fungsi cukup dekat 0
                        if abs(fm) < 1e-12:
                            root = m
                            stop_reason = f"|f(m)| < 1e-12"
                            break
                        # update interval
                        if fa * fm < 0:
                            right = m
                            fb = fm
                        else:
                            left = m
                            fa = fm
                        # cek ukuran interval
                        if (right - left)/2.0 < tol:
                            root = 0.5*(left+right)
                            stop_reason = f"interval width {(right-left)/2:.2e} < tol"
                            break
                    else:
                        # maxiter reached
                        root = 0.5*(left+right)
                        stop_reason = "max iterasi tercapai"

                    df = pd.DataFrame(rows)
                    st.subheader("Tabel Iterasi")
                    st.dataframe(df.style.format({"a":"{:.6g}", "b":"{:.6g}", "m":"{:.6g}", "f(m)":"{:.6g}"}))

                    st.subheader("Hasil")
                    st.write(f"Akar aproksimasi: **{root:.12g}**")
                    st.write(f"Sebab berhenti: {stop_reason}")
                    st.write(f"Perkiraan error interval: {(right-left)/2.0:.3e}")

                    # Plot fungsi pada rentang sedikit lebih luas dari [a,b]
                    pad = (b - a) * 0.1 if (b-a)!=0 else 1.0
                    xs = np.linspace(min(a,b)-pad, max(a,b)+pad, 500)
                    try:
                        ys = f(xs)
                        # jika ys bukan array numpy (mis. konstanta), cast
                        ys = np.array(ys, dtype=float)
                        fig, ax = plt.subplots(figsize=(7,4))
                        ax.plot(xs, ys)
                        ax.axhline(0, linestyle='--')
                        ax.axvline(root, color='orange', linewidth=1.5, label=f"root ≈ {root:.6g}")
                        ax.set_xlabel("x")
                        ax.set_ylabel("f(x)")
                        ax.legend()
                        st.pyplot(fig)
                    except Exception as e:
                        st.warning("Gagal membuat plot: " + str(e))

        except Exception as e:
            st.error("Gagal mem-parsing fungsi. Pastikan ekspresi valid, mis. x**3 - 2*x - 5.")
            st.exception(e)
