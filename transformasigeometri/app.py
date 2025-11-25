import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri",
    layout="wide" 
)

st.title("📐 Virtual Lab: Transformasi Geometri Bangun Datar")
st.markdown("Eksplorasi **Rotasi, Dilatasi, Refleksi, dan Translasi** secara visual pada poligon.")

# --- Definisi Bangun Datar Awal (Matriks 2xN) ---
SHAPES = {
    "Segitiga Siku-Siku": np.array([[2., 5., 2., 2.], [1., 1., 4., 1.]]),
    "Persegi": np.array([[1., 4., 4., 1., 1.], [1., 1., 4., 4., 1.]]),
    "Garis (Dua Titik)": np.array([[-5., 5.], [2., -3.]]),
    "Segi Lima": np.array([[3., 5., 4., 2., 1., 3.], [1., 3., 5., 5., 3., 1.]]),
}

# --- Inisialisasi Session State ---
if 'transformasi_aktif' not in st.session_state:
    st.session_state.transformasi_aktif = "Translasi"
    
# --- Fungsi Plotting (Tetap) ---
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

# --- 1. Konfigurasi Awal ---
st.subheader("1. Pilih Bangun Datar Awal")
# Gunakan 'key' agar pilihan bangun datar tidak mengubah sesi transformasi aktif
pilihan_bentuk = st.selectbox(
    "Bangun Datar:",
    list(SHAPES.keys()),
    key='shape_select'
)
titik_awal_matrix = SHAPES[pilihan_bentuk]

st.caption("Koordinat Awal:")
coords_text = " | ".join([f"$P_{i+1}({titik_awal_matrix[0, i]:.1f}, {titik_awal_matrix[1, i]:.1f})$" for i in range(titik_awal_matrix.shape[1] - 1 if "Garis" not in pilihan_bentuk else titik_awal_matrix.shape[1])])
st.markdown(coords_text)
st.markdown("---")

# --- 2. Implementasi Layout Dua Kolom ---
col_input, col_output = st.columns([1, 1.3], gap="large") 

# Inisialisasi variabel hasil untuk plot (di luar tab)
titik_hasil_matrix = titik_awal_matrix.copy()

# --- Fungsi Callback untuk Mengubah Sesi State Transformasi Aktif ---
# Fungsi ini dipanggil setiap kali tab berubah
def set_active_transform(name):
    st.session_state.transformasi_aktif = name

# --- Kolom Kiri: Input dan Kontrol (Menggunakan Tabs) ---
with col_input:
    st.header("2. Kontrol Transformasi")
    
    tab_titles = ["Translasi", "Refleksi", "Rotasi", "Dilatasi"]
    tab_objects = st.tabs(tab_titles)

    # --- TAB TRANSLASI ---
    with tab_objects[0]: 
        # Set status aktif ketika tab ini ditampilkan
        set_active_transform("Translasi")
        st.markdown("**Translasi** (Pergeseran): $P(x, y) \\to P'(x+a, y+b)$")
        
        a = st.slider("Vektor Translasi 'a' (Horizontal)", -5, 5, 2, key='a_t')
        b = st.slider("Vektor Translasi 'b' (Vertikal)", -5, 5, 1, key='b_t')

        matriks_translasi = np.array([[a], [b]])
        titik_hasil_matrix = titik_awal_matrix + matriks_translasi 
        
        # Simpan hasil ke session state jika tab ini aktif
        if st.session_state.transformasi_aktif == "Translasi":
            st.session_state.titik_hasil_matrix = titik_hasil_matrix

        st.subheader("Rumus")
        st.latex(f"\\text{{Matriks Hasil}} = \\text{{Matriks Awal}} + \\begin{{pmatrix}} {a} \\\\ {b} \\end{{pmatrix}}")

    # --- TAB REFLEKSI ---
    with tab_objects[1]:
        set_active_transform("Refleksi")
        st.markdown("**Refleksi** (Pencerminan): Mencerminkan bentuk terhadap sumbu atau garis.")
        
        pilihan_refleksi = st.selectbox(
            "Pilih Garis Refleksi",
            ["Sumbu X ($y=0$)", "Sumbu Y ($x=0$)", "Garis $y=x$", "Garis $y=-x$"],
            key='ref_pilih'
        )

        matriks_transformasi = np.array([[1, 0], [0, 1]])
        if pilihan_refleksi == "Sumbu X ($y=0$)":
            matriks_transformasi = np.array([[1, 0], [0, -1]])
        elif pilihan_refleksi == "Sumbu Y ($x=0$)":
            matriks_transformasi = np.array([[-1, 0], [0, 1]])
        elif pilihan_refleksi == "Garis $y=x$":
            matriks_transformasi = np.array([[0, 1], [1, 0]])
        elif pilihan_refleksi == "Garis $y=-x$":
            matriks_transformasi = np.array([[0, -1], [-1, 0]])
        
        titik_hasil_matrix = matriks_transformasi @ titik_awal_matrix
        
        if st.session_state.transformasi_aktif == "Refleksi":
            st.session_state.titik_hasil_matrix = titik_hasil_matrix

        st.subheader("Rumus")
        st.markdown(f"**Matriks Refleksi:**")
        st.latex(f"\\begin{{pmatrix}} x' \\\\ y' \\end{{pmatrix}} = \\begin{{pmatrix}} {matriks_transformasi[0, 0]} & {matriks_transformasi[0, 1]} \\\\ {matriks_transformasi[1, 0]} & {matriks_transformasi[1, 1]} \\end{{pmatrix}} \\begin{{pmatrix}} x \\\\ y \\end{{pmatrix}}")

    # --- TAB ROTASI ---
    with tab_objects[2]:
        set_active_transform("Rotasi")
        st.markdown("**Rotasi** (Perputaran): Memutar bentuk terhadap titik pusat $(0,0)$.")
        
        sudut_derajat = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90, key='rot_sudut')
        sudut_rad = np.deg2rad(sudut_derajat)

        cos_theta = np.cos(sudut_rad)
        sin_theta = np.sin(sudut_rad)
        matriks_transformasi = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])

        titik_hasil_matrix_mentah = matriks_transformasi @ titik_awal_matrix
        titik_hasil_matrix = np.round(titik_hasil_matrix_mentah, 2)
        
        if st.session_state.transformasi_aktif == "Rotasi":
            st.session_state.titik_hasil_matrix = titik_hasil_matrix
        
        st.subheader("Rumus")
        st.markdown(f"**Sudut:** ${sudut_derajat}^\circ$.")
        st.markdown(f"**Matriks Rotasi:**")
        st.latex(f"\\begin{{pmatrix}} \\cos{{\\theta}} & -\\sin{{\\theta}} \\\\ \\sin{{\\theta}} & \\cos{{\\theta}} \\end{{pmatrix}} \\approx \\begin{{pmatrix}} {round(cos_theta, 2)} & {round(-sin_theta, 2)} \\\\ {round(sin_theta, 2)} & {round(cos_theta, 2)} \\end{{pmatrix}}")

    # --- TAB DILATASI ---
    with tab_objects[3]:
        set_active_transform("Dilatasi")
        st.markdown("**Dilatasi** (Penskalaan): Memperbesar atau memperkecil bentuk terhadap titik pusat $(0,0)$.")
        
        k = st.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1, key='dil_k')

        matriks_transformasi = np.array([
            [k, 0],
            [0, k]
        ])

        titik_hasil_matrix = matriks_transformasi @ titik_awal_matrix
        
        if st.session_state.transformasi_aktif == "Dilatasi":
            st.session_state.titik_hasil_matrix = titik_hasil_matrix
        
        st.subheader("Rumus")
        st.markdown(f"**Faktor Skala:** $k={k}$.")
        st.markdown(f"**Matriks Dilatasi:**")
        st.latex(f"\\text{{Matriks Dilatasi}} = \\begin{{pmatrix}} {k} & 0 \\\\ 0 & {k} \\end{{pmatrix}}")

# --- Kolom Kanan: Output Grafik ---
with col_output:
    st.header(f"3. Visualisasi Hasil: {st.session_state.transformasi_aktif}")
    
    # Panggil plot menggunakan data dari Session State
    if 'titik_hasil_matrix' in st.session_state:
        plot_transformasi(titik_awal_matrix, st.session_state.titik_hasil_matrix, f"Transformasi: {st.session_state.transformasi_aktif}")

        st.subheader("Koordinat Hasil")
        # Ambil hasil dari session state untuk ditampilkan
        final_result = st.session_state.titik_hasil_matrix
        
        hasil_coords_text = " | ".join([f"$P'_{i+1}({final_result[0, i]:.2f}, {final_result[1, i]:.2f})$" for i in range(final_result.shape[1] - 1 if "Garis" not in pilihan_bentuk else final_result.shape[1])])
        st.markdown(hasil_coords_text)
    else:
        st.info("Silakan pilih transformasi untuk memulai visualisasi.")
