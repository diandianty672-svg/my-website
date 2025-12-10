import streamlit as st
import numpy as np

st.title("Solusi SPNL dengan Metode Bisection")
st.write("Aplikasi ini menyelesaikan persamaan non-linear f(x)=0 menggunakan metode Bisection.")

# Input fungsi
func_input = st.text_input("Masukkan fungsi f(x):", "x**3 - x - 2")

# Input interval
a_input = st.number_input("Nilai a (batas kiri):", value=1.0)
b_input = st.number_input("Nilai b (batas kanan):", value=2.0)

# Maks iterasi
max_iter = st.number_input("Maksimal Iterasi:", value=20, step=1)

# Toleransi
 tol_input = st.text_input("Toleransi (contoh: 1e-6)", value="1e-6")

# Definisi fungsi
def f(x):
    return eval(func_input)

# Tombol eksekusi
if st.button("Hitung Akar"):
    a = a_input
    b = b_input

    if f(a) * f(b) >= 0:
        st.error("f(a) dan f(b) harus berbeda tanda! Pilih interval lain.")
    else:
        iterasi_data = []
        for i in range(1, int(max_iter) + 1):
            c = (a + b) / 2
            fc = f(c)

            iterasi_data.append([i, a, b, c, fc])

            if abs(fc) < tol:
                break

            if f(a) * fc < 0:
                b = c
            else:
                a = c

        st.success(f"Perkiraan akar = {c}")

        # Tampilkan tabel iterasi
        st.subheader("Tabel Iterasi Bisection")
        st.table(
            {
                "Iterasi": [row[0] for row in iterasi_data],
                "a": [row[1] for row in iterasi_data],
                "b": [row[2] for row in iterasi_data],
                "c": [row[3] for row in iterasi_data],
                "f(c)": [row[4] for row in iterasi_data],
            }
        )
