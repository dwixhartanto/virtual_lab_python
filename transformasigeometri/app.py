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


# --- Fungsi Inti Transformasi ---
# Fungsi ini dipanggil untuk menghitung hasil transformasi berdasarkan state saat ini
def perform_transformasi(titik_awal_matrix, active_transform):
    
    # Ambil parameter dari session state
    if active_transform == "Translasi":
        a = st.session_state.get('a_t', 2)
        b = st.session_state.get('b_t', 1)
        matriks_translasi = np.array([[a], [b]])
        return titik_awal_matrix + matriks_translasi

    elif active_transform == "Refleksi":
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
        k = st.session_state.get('dil_k', 1.5)
        matriks_transformasi = np.array([[k, 0], [0, k]])
        return matriks_transformasi @ titik_awal_matrix
    
    return titik_awal_matrix

# --- Inisialisasi Session State (Dilakukan HANYA sekali) ---
if 'transformasi_aktif' not in st.session_state:
    st.session_state.transformasi_aktif = "Translasi"
if 'titik_hasil_matrix' not in st.session_state:
    # Inisialisasi dengan hasil translasi default
    st.session_state.titik_hasil_matrix = perform_transformasi(SHAPES[list(SHAPES.keys())[0]], "Translasi")

# --- Fungsi Callback untuk Mengubah Sesi State Transformasi Aktif ---
def set_active_transform(name):
    # Hanya ubah state jika memang tab berbeda yang diklik
    if st.session_state.transformasi_aktif != name:
        st.session_state.transformasi_aktif = name
        # Force re-calculation on tab switch
        st.session_state.titik_hasil_matrix = perform_transformasi(
            SHAPES[st.session_state.get('shape_select', list(SHAPES.keys())[0])], name
        )

# --- 1. Konfigurasi Awal ---
st.subheader("1. Pilih Bangun Datar Awal")
# Tambahkan on_change callback untuk memastikan titik hasil diperbarui ketika shape berubah
def on_shape_change():
    # Ketika shape berubah, hitung ulang titik hasil berdasarkan active_transform saat ini
    new_shape = SHAPES[st.session_state.shape_select]
    st.session_state.titik_hasil_matrix = perform_transformasi(
        new_shape, st.session_state.transformasi_aktif
    )

pilihan_bentuk = st.selectbox(
    "Bangun Datar:",
    list(SHAPES.keys()),
    key='shape_select', # Wajib
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
    # Gunakan 'key' di tabs untuk memicu callback
    tab_objects = st.tabs(tab_titles, key='main_tabs')

    # --- TAB TRANSLASI ---
    with tab_objects[0]: 
        set_active_transform("Translasi")
        st.markdown("**Translasi** (Pergeseran): $P(x, y) \\to P'(x+a, y+b)$")
        
        # Tambahkan on_change callback untuk setiap slider/widget
        def update_translasi():
            new_a = st.session_state.a_t
            new_b = st.session_state.b_t
            matriks_translasi = np.array([[new_a], [new_b]])
            st.session_state.titik_hasil_matrix = titik_awal_matrix + matriks_translasi

        a = st.slider("Vektor Translasi 'a' (Horizontal)", -5, 5, 2, key='a_t', on_change=update_translasi)
        b = st.slider("Vektor Translasi 'b' (Vertikal)", -5, 5, 1, key='b_t', on_change=update_translasi)
        
        st.subheader("Rumus")
        st.latex(f"\\text{{Matriks Hasil}} = \\text{{Matriks Awal}} + \\begin{{pmatrix}} {a} \\\\ {b} \\end{{pmatrix}}")

    # --- TAB REFLEKSI ---
    with tab_objects[1]:
        set_active_transform("Refleksi")
        st.markdown("**Refleksi** (Pencerminan): Mencerminkan bentuk terhadap sumbu atau garis.")
        
        def update_refleksi():
            st.session_state.titik_hasil_matrix = perform_transformasi(titik_awal_matrix, "Refleksi")

        pilihan_refleksi = st.selectbox(
            "Pilih Garis Refleksi",
            ["Sumbu X ($y=0$)", "Sumbu Y ($x=0$)", "Garis $y=x$", "Garis $y=-x$"],
            key='ref_pilih',
            on_change=update_refleksi
        )
        
        st.subheader("Rumus")
        # Panggil perform_transformasi lagi hanya untuk mendapatkan matriksnya
        matriks_transformasi = np.array([[1, 0], [0, 1]])
        if pilihan_refleksi == "Sumbu Y ($x=0$)": matriks_transformasi = np.array([[-1, 0], [0, 1]])
        elif pilihan_refleksi == "Garis $y=x$": matriks_transformasi = np.array([[0, 1], [1, 0]])
        elif pilihan_refleksi == "Garis $y=-x$": matriks_transformasi = np.array([[0, -1], [-1, 0]])

        st.markdown(f"**Matriks Refleksi:**")
        st.latex(f"\\begin{{pmatrix}} x' \\\\ y' \\end{{pmatrix}} = \\begin{{pmatrix}} {matriks_transformasi[0, 0]} & {matriks_transformasi[0, 1]} \\\\ {matriks_transformasi[1, 0]} & {matriks_transformasi[1, 1]} \\end{{pmatrix}} \\begin{{pmatrix}} x \\\\ y \\end{{pmatrix}}")

    # --- TAB ROTASI ---
    with tab_objects[2]:
        set_active_transform("Rotasi")
        st.markdown("**Rotasi** (Perputaran): Memutar bentuk terhadap titik pusat $(0,0)$.")
        
        def update_rotasi():
            st.session_state.titik_hasil_matrix = perform_transformasi(titik_awal_matrix, "Rotasi")

        sudut_derajat = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90, key='rot_sudut', on_change=update_rotasi)
        
        st.subheader("Rumus")
        sudut_rad = np.deg2rad(sudut_derajat)
        cos_theta = np.cos(sudut_rad)
        sin_theta = np.sin(sudut_rad)
        st.markdown(f"**Sudut:** ${sudut_derajat}^\circ$.")
        st.markdown(f"**Matriks Rotasi:**")
        st.latex(f"\\begin{{pmatrix}} \\cos{{\\theta}} & -\\sin{{\\theta}} \\\\ \\sin{{\\theta}} & \\cos{{\\theta}} \\end{{pmatrix}} \\approx \\begin{{pmatrix}} {round(cos_theta, 2)} & {round(-sin_theta, 2)} \\\\ {round(sin_theta, 2)} & {round(cos_theta, 2)} \\end{{pmatrix}}")

    # --- TAB DILATASI ---
    with tab_objects[3]:
        set_active_transform("Dilatasi")
        st.markdown("**Dilatasi** (Penskalaan): Memperbesar atau memperkecil bentuk terhadap titik pusat $(0,0)$.")
        
        def update_dilatasi():
            st.session_state.titik_hasil_matrix = perform_transformasi(titik_awal_matrix, "Dilatasi")

        k = st.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1, key='dil_k', on_change=update_dilatasi)

        st.subheader("Rumus")
        st.markdown(f"**Faktor Skala:** $k={k}$.")
        st.markdown(f"**Matriks Dilatasi:**")
        st.latex(f"\\text{{Matriks Dilatasi}} = \\begin{{pmatrix}} {k} & 0 \\\\ 0 & {k} \\end{{pmatrix}}")

# --- Kolom Kanan: Output Grafik ---
with col_output:
    # Karena kita menggunakan on_change dan callback, Session State selalu sinkron.
    # Kita hanya perlu mengambil nilainya di sini.
    st.header(f"3. Visualisasi Hasil: {st.session_state.transformasi_aktif}")
    
    # Panggil plot menggunakan data dari Session State
    plot_transformasi(titik_awal_matrix, st.session_state.titik_hasil_matrix, f"Transformasi: {st.session_state.transformasi_aktif}") 

    st.subheader("Koordinat Hasil")
    final_result = st.session_state.titik_hasil_matrix
    
    hasil_coords_text = " | ".join([f"$P'_{i+1}({final_result[0, i]:.2f}, {final_result[1, i]:.2f})$" for i in range(final_result.shape[1] - 1 if "Garis" not in pilihan_bentuk else final_result.shape[1])])
    st.markdown(hasil_coords_text)
