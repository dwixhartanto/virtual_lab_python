import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri",
    layout="wide" 
)

st.title("📐 Virtual Lab: Transformasi Geometri Bangun Datar")
# ... (SHAPES dan plot_transformasi tetap sama) ...
# --- Definisi Bangun Datar Awal (Matriks 2xN) ---
SHAPES = {
    "Segitiga Siku-Siku": np.array([[2., 5., 2., 2.], [1., 1., 4., 1.]]),
    "Persegi": np.array([[1., 4., 4., 1., 1.], [1., 1., 4., 4., 1.]]),
    "Garis (Dua Titik)": np.array([[-5., 5.], [2., -3.]]),
    "Segi Lima": np.array([[3., 5., 4., 2., 1., 3.], [1., 3., 5., 5., 3., 1.]]),
}

# Fungsi Plotting (Tetap sama)
def plot_transformasi(titik_awal_matrix, titik_hasil_matrix, judul):
    fig, ax = plt.subplots(figsize=(6, 6))
    def close_polygon(matrix):
        return np.hstack([matrix, matrix[:, 0:1]])
    all_points = np.hstack([titik_awal_matrix, titik_hasil_matrix])
    max_abs = np.max(np.abs(all_points))
    buffer = max(5, max_abs + 2) 
    X_batas = [-buffer, buffer]
    Y_batas = [-buffer, buffer]
    awal_closed = close_polygon(titik_awal_matrix)
    ax.plot(awal_closed[0, :], awal_closed[1, :], 'b--', linewidth=2, alpha=0.6, label='Bentuk Awal')
    ax.plot(titik_awal_matrix[0, :], titik_awal_matrix[1, :], 'bo', markersize=6)
    hasil_closed = close_polygon(titik_hasil_matrix)
    ax.plot(hasil_closed[0, :], hasil_closed[1, :], 'r-', linewidth=2, label='Bentuk Hasil')
    ax.plot(titik_hasil_matrix[0, :], titik_hasil_matrix[1, :], 'ro', markersize=6)
    ax.grid(True, linestyle='--')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlim(X_batas[0], X_batas[1])
    ax.set_ylim(Y_batas[0], Y_batas[1])
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")
    ax.set_title(judul)
    ax.legend(loc='upper right')
    ax.set_aspect('equal', adjustable='box') 
    st.pyplot(fig)
    plt.close(fig)


# --- Fungsi Inti Transformasi ---
# Fungsi ini sekarang membaca semua state dari widget yang terpisah (dengan keys)
def perform_transformasi(titik_awal_matrix, active_transform):
    # Ambil parameter dari session state
    if active_transform == "Translasi":
        a = st.session_state.get('a_t', 2)
        b = st.session_state.get('b_t', 1)
        matriks_translasi = np.array([[a], [b]])
        return titik_awal_matrix + matriks_translasi

    elif active_transform == "Refleksi":
        # Ambil state dari widget (selectbox)
        pilihan_refleksi = st.session_state.get('ref_pilih', "Sumbu X ($y=0$)")
        if pilihan_refleksi == "Sumbu X ($y=0$)":
            matriks_transformasi = np.array([[1, 0], [0, -1]])
        elif pilihan_refleksi == "Sumbu Y ($x=0$)":
            matriks_transformasi = np.array([[-1, 0], [0, 1]])
        elif pilihan_refleksi == "Garis $y=x$":
            matriks_transformasi = np.array([[0, 1], [1, 0]])
        elif pilihan_refleksi == "Garis $y=-x$":
            matriks_transformasi = np.array([[0, -1], [-1, 0]])
        return matriks_transformasi @ titik_awal_matrix

    elif active_transform == "Rotasi":
        # Ambil state dari widget (slider)
        sudut_derajat = st.session_state.get('rot_sudut', 90)
        sudut_rad = np.deg2rad(sudut_derajat)
        cos_theta = np.cos(sudut_rad)
        sin_theta = np.sin(sudut_rad)
        matriks_transformasi = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        titik_hasil_matrix_mentah = matriks_transformasi @ titik_awal_matrix
        return np.round(titik_hasil_matrix_mentah, 2)

    elif active_transform == "Dilatasi":
        # Ambil state dari widget (slider)
        k = st.session_state.get('dil_k', 1.5)
        matriks_transformasi = np.array([[k, 0], [0, k]])
        return matriks_transformasi @ titik_awal_matrix
    
    return titik_awal_matrix


# --- Inisialisasi Session State & Callback Sederhana ---
# Kita tidak perlu lagi session state untuk titik_hasil_matrix, cukup hitung di akhir

# Callback untuk pembaruan ketika shape berubah
def on_shape_change():
    # Ketika shape berubah, kita akan memicu run ulang, dan hitungan akan dilakukan di akhir skrip
    pass

# --- 1. Konfigurasi Awal ---
st.subheader("1. Pilih Bangun Datar Awal")
pilihan_bentuk = st.selectbox(
    "Bangun Datar:",
    list(SHAPES.keys()),
    key='shape_select', 
    on_change=on_shape_change
)
titik_awal_matrix = SHAPES[pilihan_bentuk]

st.caption("Koordinat Awal:")
coords_text = " | ".join([f"$P_{i+1}({titik_awal_matrix[0, i]:.1f}, {titik_awal_matrix[1, i]:.1f})$" for i in range(titik_awal_matrix.shape[1] - 1 if "Garis" not in pilihan_bentuk else titik_awal_matrix.shape[1])])
st.markdown(coords_text)
st.markdown("---")


# --- 2. Implementasi Layout Dua Kolom ---
col_input, col_output = st.columns([1, 1.3], gap="large") 

# --- Kolom Kiri: Input dan Kontrol (Menggunakan Tabs) ---
with col_input:
    st.header("2. Kontrol Transformasi")
    
    tab_titles = ["Translasi", "Refleksi", "Rotasi", "Dilatasi"]
    # PENTING: Key 'main_tabs' menyimpan string tab yang sedang aktif
    tab_objects = st.tabs(tab_titles, key='main_tabs')

    # --- TAB TRANSLASI ---
    with tab_objects[0]: 
        st.markdown("**Translasi** (Pergeseran): $P(x, y) \\to P'(x+a, y+b)$")
        a = st.slider("Vektor Translasi 'a' (Horizontal)", -5, 5, 2, key='a_t')
        b = st.slider("Vektor Translasi 'b' (Vertikal)", -5, 5, 1, key='b_t')
        st.subheader("Rumus")
        st.latex(f"\\text{{Matriks Hasil}} = \\text{{Matriks Awal}} + \\begin{{pmatrix}} {a} \\\\ {b} \\end{{pmatrix}}")

    # --- TAB REFLEKSI ---
    with tab_objects[1]:
        st.markdown("**Refleksi** (Pencerminan): Mencerminkan bentuk terhadap sumbu atau garis.")
        pilihan_refleksi = st.selectbox(
            "Pilih Garis Refleksi",
            ["Sumbu X ($y=0$)", "Sumbu Y ($x=0$)", "Garis $y=x$", "Garis $y=-x$"],
            key='ref_pilih'
        )
        st.subheader("Rumus")
        # Logika matriks di sini hanya untuk display
        matriks_transformasi = np.array([[1, 0], [0, 1]])
        if pilihan_refleksi == "Sumbu Y ($x=0$)": matriks_transformasi = np.array([[-1, 0], [0, 1]])
        elif pilihan_refleksi == "Garis $y=x$": matriks_transformasi = np.array([[0, 1], [1, 0]])
        elif pilihan_refleksi == "Garis $y=-x$": matriks_transformasi = np.array([[0, -1], [-1, 0]])
        st.markdown(f"**Matriks Refleksi:**")
        st.latex(f"\\begin{{pmatrix}} x' \\\\ y' \\end{{pmatrix}} = \\begin{{pmatrix}} {matriks_transformasi[0, 0]} & {matriks_transformasi[0, 1]} \\\\ {matriks_transformasi[1, 0]} & {matriks_transformasi[1, 1]} \\end{{pmatrix}} \\begin{{pmatrix}} x \\\\ y \\end{{pmatrix}}")

    # --- TAB ROTASI ---
    with tab_objects[2]:
        st.markdown("**Rotasi** (Perputaran): Memutar bentuk terhadap titik pusat $(0,0)$.")
        sudut_derajat = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90, key='rot_sudut')
        st.subheader("Rumus")
        sudut_rad = np.deg2rad(sudut_derajat)
        cos_theta = np.cos(sudut_rad)
        sin_theta = np.sin(sudut_rad)
        st.markdown(f"**Sudut:** ${sudut_derajat}^\circ$.")
        st.markdown(f"**Matriks Rotasi:**")
        st.latex(f"\\begin{{pmatrix}} \\cos{{\\theta}} & -\\sin{{\\theta}} \\\\ \\sin{{\\theta}} & \\cos{{\\theta}} \\end{{pmatrix}} \\approx \\begin{{pmatrix}} {round(cos_theta, 2)} & {round(-sin_theta, 2)} \\\\ {round(sin_theta, 2)} & {round(cos_theta, 2)} \\end{{pmatrix}}")

    # --- TAB DILATASI ---
    with tab_objects[3]:
        st.markdown("**Dilatasi** (Penskalaan): Memperbesar atau memperkecil bentuk terhadap titik pusat $(0,0)$.")
        k = st.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1, key='dil_k')
        st.subheader("Rumus")
        st.markdown(f"**Faktor Skala:** $k={k}$.")
        st.markdown(f"**Matriks Dilatasi:**")
        st.latex(f"\\text{{Matriks Dilatasi}} = \\begin{{pmatrix}} {k} & 0 \\\\ 0 & {k} \\end{{pmatrix}}")


# --- Perhitungan Hasil Akhir (Di Luar Kolom Input/Tab) ---
# Dapatkan nama tab yang sedang aktif
transformasi_aktif = st.session_state.main_tabs 
# Lakukan perhitungan menggunakan fungsi yang membaca semua state widget
titik_hasil_matrix = perform_transformasi(titik_awal_matrix, transformasi_aktif)


# --- Kolom Kanan: Output Grafik ---
with col_output:
    st.header(f"3. Visualisasi Hasil: {transformasi_aktif}")
    
    # Panggil plot dengan hasil perhitungan terbaru
    plot_transformasi(titik_awal_matrix, titik_hasil_matrix, f"Transformasi: {transformasi_aktif}")

    st.subheader("Koordinat Hasil")
    
    hasil_coords_text = " | ".join([f"$P'_{i+1}({titik_hasil_matrix[0, i]:.2f}, {titik_hasil_matrix[1, i]:.2f})$" for i in range(titik_hasil_matrix.shape[1] - 1 if "Garis" not in pilihan_bentuk else titik_hasil_matrix.shape[1])])
    st.markdown(hasil_coords_text)
