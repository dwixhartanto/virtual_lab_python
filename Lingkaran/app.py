import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Laboratorium Virtual Keliling Lingkaran")

st.title("🔬 Laboratorium Virtual Keliling Lingkaran")
st.write("Jelajahi hubungan antara keliling dan diameter lingkaran untuk menemukan rumusnya!")

st.sidebar.header("Pengaturan Lingkaran")
radius = st.sidebar.slider("Pilih Radius Lingkaran (cm)", 1.0, 10.0, 3.0, 0.1)

diameter = 2 * radius
keliling_teoritis = 2 * np.pi * radius

st.sidebar.markdown("---")
st.sidebar.header("Alat Pengukuran")
measure_button = st.sidebar.button("Ukur Lingkaran Ini")

# Inisialisasi atau muat data dari session state
if 'measurements' not in st.session_state:
    st.session_state.measurements = pd.DataFrame(columns=["Radius (cm)", "Diameter (cm)", "Keliling (cm)", "Keliling/Diameter"])

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualisasi Lingkaran")

    fig, ax = plt.subplots(figsize=(6, 6))
    circle = plt.Circle((0, 0), radius, color='blue', fill=False, linewidth=2)
    ax.add_patch(circle)

    # Garis diameter
    ax.plot([-radius, radius], [0, 0], 'r--', linewidth=1, label=f'Diameter = {diameter:.2f} cm')
    # Teks radius
    ax.plot([0, radius], [0, 0], 'g-', linewidth=1)
    ax.text(radius/2, 0.5, f'Radius = {radius:.1f} cm', color='green', fontsize=10, ha='center')

    ax.set_xlim(-(radius + 2), (radius + 2))
    ax.set_ylim(-(radius + 2), (radius + 2))
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(f"Lingkaran dengan Radius {radius:.1f} cm")
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")
    st.pyplot(fig)

    st.markdown(f"""
    ---
    ### Informasi Lingkaran Saat Ini:
    * **Radius (r):** `{radius:.1f}` cm
    * **Diameter (d):** `{diameter:.1f}` cm
    * **Keliling (K) (perkiraan):** `{keliling_teoritis:.2f}` cm (Ini adalah nilai yang akan Anda coba temukan!)
    """)

with col2:
    st.subheader("Tabel Pengukuran Anda")
    st.write("Catat hasil pengukuran Anda di sini:")

    if measure_button:
        new_measurement = pd.DataFrame([{
            "Radius (cm)": radius,
            "Diameter (cm)": diameter,
            "Keliling (cm)": keliling_teoritis, # Untuk tujuan simulasi, kita gunakan keliling teoritis
            "Keliling/Diameter": keliling_teoritis / diameter
        }])
        st.session_state.measurements = pd.concat([st.session_state.measurements, new_measurement], ignore_index=True)
        st.session_state.measurements = st.session_state.measurements.drop_duplicates(subset=["Radius (cm)"]).sort_values(by="Radius (cm)").reset_index(drop=True)

    st.dataframe(st.session_state.measurements)

    if not st.session_state.measurements.empty:
        st.subheader("Grafik Keliling vs. Diameter")
        fig_scatter, ax_scatter = plt.subplots()
        ax_scatter.scatter(st.session_state.measurements["Diameter (cm)"], st.session_state.measurements["Keliling (cm)"])
        ax_scatter.set_xlabel("Diameter (cm)")
        ax_scatter.set_ylabel("Keliling (cm)")
        ax_scatter.set_title("Hubungan Keliling dan Diameter")
        ax_scatter.grid(True)
        st.pyplot(fig_scatter)

        st.subheader("Analisis Hasil")
        st.write("Perhatikan kolom 'Keliling/Diameter'.")
        if len(st.session_state.measurements) > 1:
            avg_ratio = st.session_state.measurements["Keliling/Diameter"].mean()
            st.write(f"Rata-rata nilai Keliling/Diameter dari pengukuran Anda adalah: **{avg_ratio:.4f}**")
            st.write("Apakah nilai ini mendekati suatu konstanta matematika yang Anda kenal?")

st.markdown("---")
st.subheader("Instruksi Eksperimen:")
st.markdown("""
1.  **Atur Radius:** Gunakan slider di sidebar untuk mengatur ukuran lingkaran.
2.  **Ukur:** Klik tombol "Ukur Lingkaran Ini" untuk mencatat radius, diameter, dan keliling ke dalam tabel.
3.  **Ulangi:** Coba dengan beberapa radius yang berbeda dan catat hasilnya.
4.  **Analisis:** Amati kolom "Keliling/Diameter" di tabel. Apa yang Anda lihat?
5.  **Rumus:** Dari pengamatan Anda, bisakah Anda menyimpulkan rumus untuk keliling lingkaran?
""")

st.markdown("---")
st.info("💡 **Petunjuk Discovery:** Siswa diharapkan memperhatikan bahwa rasio Keliling/Diameter selalu mendekati nilai Pi (π) terlepas dari ukuran lingkaran.")