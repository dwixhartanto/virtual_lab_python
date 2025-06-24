import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Laboratorium Bayangan Arsitek Mini",
    page_icon="☀️",
    layout="centered"
)

# --- Judul dan Deskripsi Aplikasi ---
st.header("☀️ Laboratorium Bayangan Arsitek Mini")
st.markdown("""
Selamat datang di Lab Bayangan Arsitek Mini! Di sini kamu akan berperan sebagai arsitek yang harus memahami bagaimana bayangan terbentuk.
""")

st.divider()

# --- Inisialisasi Session State untuk menyimpan data eksperimen ---
if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = pd.DataFrame(
        columns=['Tinggi Gedung (m)', 'Sudut Elevasi (°)', 'Panjang Bayangan (m)']
    )

# --- Sidebar untuk Navigasi Menu ---
st.sidebar.header("Navigasi")
menu_selection = st.sidebar.radio(
    "Pilih Menu:",
    ("Simulasi", "Panduan Penemuan")
)

# --- Konten berdasarkan Menu yang Dipilih ---

if menu_selection == "Simulasi":
    st.subheader("Simulasi Bayangan Gedung")
    st.markdown("""
    Ubahlah **Tinggi Gedung** dan **Sudut Elevasi Matahari**, lalu amati **Panjang Bayangan** yang dihasilkan.
    Coba catat datamu dan temukan polanya!
    """)

    # --- Kontrol Interaktif ---
    st.sidebar.header("Pengaturan Simulasi")
    tinggi_gedung = st.sidebar.slider(
        "1. Tinggi Gedung (meter)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=0.5,
        help="Geser untuk mengubah tinggi gedung yang ingin kamu simulasikan."
    )

    sudut_elevasi_derajat = st.sidebar.slider(
        "2. Sudut Elevasi Matahari (derajat)",
        min_value=1.0, # Tidak bisa 0 karena tan(0) tidak terdefinisi (bayangan tak hingga)
        max_value=89.0, # Tidak bisa 90 karena tan(90) tidak terdefinisi (bayangan nol)
        value=45.0,
        step=1.0,
        help="Geser untuk mengubah sudut matahari dari cakrawala. Semakin tinggi sudut, semakin tinggi matahari di langit."
    )

    st.sidebar.markdown("""
    **Petunjuk Tambahan:**
    * **Sudut Elevasi:** Adalah sudut antara sinar matahari dan permukaan tanah.
    """)

    # --- Perhitungan Panjang Bayangan ---
    # Konversi sudut dari derajat ke radian karena fungsi trigonometri di Python menggunakan radian
    sudut_elevasi_radian = math.radians(sudut_elevasi_derajat)

    # Pastikan tan tidak nol atau tak hingga untuk menghindari error
    if math.tan(sudut_elevasi_radian) != 0 and not math.isinf(math.tan(sudut_elevasi_radian)):
        panjang_bayangan = tinggi_gedung / math.tan(sudut_elevasi_radian)
    else:
        panjang_bayangan = float('inf') # Bayangan sangat panjang jika sudut mendekati 0

    st.subheader("Hasil Simulasi")
    st.write(f"**Tinggi Gedung:** {tinggi_gedung:.1f} meter")
    st.write(f"**Sudut Elevasi Matahari:** {sudut_elevasi_derajat:.1f}°")

    if panjang_bayangan == float('inf'):
        st.write("**Panjang Bayangan:** Sangat panjang (Matahari sangat rendah di langit atau mendekati cakrawala)")
    else:
        st.write(f"**Panjang Bayangan:** {panjang_bayangan:.2f} meter") # Format 2 angka di belakang koma

    # --- Visualisasi Segitiga Siku-siku ---
    st.subheader("Visualisasi")
    fig, ax = plt.subplots(figsize=(8, 4))

    # Sisi bawah (bayangan)
    ax.plot([0, panjang_bayangan], [0, 0], color='blue', linewidth=3, label='Panjang Bayangan')
    # Sisi vertikal (gedung)
    ax.plot([0, 0], [0, tinggi_gedung], color='red', linewidth=3, label='Tinggi Gedung')
    # Sisi miring (sinar matahari)
    ax.plot([0, panjang_bayangan], [tinggi_gedung, 0], color='green', linestyle='--', label='Sinar Matahari')

    # Teks label untuk sisi
    ax.text(panjang_bayangan / 2, -1, f'{panjang_bayangan:.2f} m', ha='center', va='top', color='blue')
    ax.text(-1, tinggi_gedung / 2, f'{tinggi_gedung:.1f} m', ha='right', va='center', color='red')

    # Sudut elevasi (arc)
    # Menggunakan lingkaran kecil untuk menandai sudut
    circle_radius = min(panjang_bayangan, tinggi_gedung) * 0.1
    if panjang_bayangan > 0: # Hanya gambar jika ada bayangan
        ax.add_patch(plt.Circle((0, 0), circle_radius, color='gray', alpha=0.3))
        # Teks sudut
        ax.text(circle_radius * math.cos(math.radians(sudut_elevasi_derajat/2)),
                circle_radius * math.sin(math.radians(sudut_elevasi_derajat/2)),
                f'{sudut_elevasi_derajat:.1f}°',
                color='black', ha='left', va='bottom')

    # Pengaturan plot
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-5, max(panjang_bayangan + 5, 20)) # Batasi sumbu x agar tidak terlalu lebar
    ax.set_ylim(-5, max(tinggi_gedung + 5, 20)) # Batasi sumbu y
    ax.set_xlabel("Jarak (meter)")
    ax.set_ylabel("Tinggi (meter)")
    ax.set_title("Simulasi Segitiga Siku-Siku")
    ax.grid(True)
    ax.legend()
    plt.tight_layout() # Untuk penyesuaian layout otomatis
    st.pyplot(fig)

    st.divider()

    # --- Bagian Data Eksperimen ---
    st.subheader("Data Eksperimen Anda")
    if st.button("Tambahkan ke Data Eksperimen"):
        new_data = pd.DataFrame([{
            'Tinggi Gedung (m)': tinggi_gedung,
            'Sudut Elevasi (°)': sudut_elevasi_derajat,
            'Panjang Bayangan (m)': panjang_bayangan if panjang_bayangan != float('inf') else 'Sangat Panjang'
        }])
        st.session_state.experiment_data = pd.concat([st.session_state.experiment_data, new_data], ignore_index=True)
        st.success("Data telah ditambahkan!")

    if not st.session_state.experiment_data.empty:
        st.dataframe(st.session_state.experiment_data)
        if st.button("Hapus Semua Data Eksperimen"):
            st.session_state.experiment_data = pd.DataFrame(columns=['Tinggi Gedung (m)', 'Sudut Elevasi (°)', 'Panjang Bayangan (m)'])
            st.warning("Semua data eksperimen telah dihapus.")
    else:
        st.info("Belum ada data eksperimen. Lakukan simulasi dan klik 'Tambahkan ke Data Eksperimen'.")


elif menu_selection == "Panduan Penemuan":
    st.subheader("Panduan Penemuan ")
    st.markdown("""
    Selamat datang di bagian Panduan Penemuan! Di sini kamu bisa belajar lebih dalam tentang konsep matematika di balik pembentukan bayangan.

    ### 1. Eksplorasi Awal:
    * Coba ubah **Tinggi Gedung** sambil menjaga **Sudut Elevasi** tetap. Apa yang terjadi pada panjang bayangan?
    * Coba ubah **Sudut Elevasi** sambil menjaga **Tinggi Gedung** tetap. Bagaimana perubahan sudut memengaruhi panjang bayangan?

    ### 2. Identifikasi Pola:
    * Lihat data yang kamu kumpulkan di tabel (di menu 'Simulasi'). Apakah kamu melihat hubungan antara Tinggi, Sudut, dan Bayangan?
    * Misalnya, jika sudutnya 45°, apa hubungan antara tinggi dan bayangan?

    ### 3. Rumus Tersembunyi:
    * Apakah kamu ingat konsep segitiga siku-siku dari pelajaran matematika?
    * Bagaimana rasio antara sisi 'depan' (Tinggi Gedung) dan sisi 'samping' (Panjang Bayangan) berhubungan dengan sudut? (Petunjuk: Ada fungsi trigonometri yang bisa membantumu!)

    ### 4. Uji Hipotesismu:
    * Setelah kamu menemukan rumusnya, coba gunakan untuk memprediksi panjang bayangan pada kombinasi Tinggi dan Sudut yang berbeda. Kemudian, gunakan simulasi ini untuk memverifikasi prediksimu!

    ---

  
    Ini adalah dasar dari banyak perhitungan dalam arsitektur, teknik sipil, dan astronomi!
    """)
    st.info("Selamat bereksperimen dan temukan rahasia di balik bayangan!")

