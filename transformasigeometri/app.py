import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
# Atur layout ke 'wide' untuk memanfaatkan ruang layar
st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri",
    layout="wide" 
)

st.title("📐 Virtual Lab: Transformasi Geometri Bangun Datar")
st.markdown("Eksplorasi **Rotasi, Dilatasi, Refleksi, dan Translasi** secara visual pada poligon.")

# --- Definisi Bangun Datar Awal (Matriks 2xN) ---
# Format: np.array([[x1, x2, x3, ...], [y1, y2, y3, ...]])
SHAPES = {
    "Segitiga Siku-Siku": np.array([[2., 5., 2., 2.], [1., 1., 4., 1.]]),
    "Persegi": np.array([[1., 4., 4., 1., 1.], [1., 1., 4., 4., 1.]]),
    "Garis (Dua Titik)": np.array([[-5., 5.], [2., -3.]]),
    "Segi Lima": np.array([[3., 5., 4., 2., 1., 3.], [1., 3., 5., 5., 3., 1.]]),
}

# --- Fungsi Plotting (Tetap) ---
def plot_transformasi(titik_awal_matrix, titik_hasil_matrix, judul):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Fungsi untuk menutup poligon (menghubungkan titik terakhir ke titik pertama)
    def close_polygon(matrix):
        # np.hstack: menggabungkan kolom-kolom secara horizontal
        # matrix[:, 0:1]: mengambil kolom pertama (titik awal)
        return np.hstack([matrix, matrix[:, 0:1]])

    # 1. Menentukan Batas Plot secara dinamis
    all_points = np.hstack([titik_awal_matrix, titik_hasil_matrix])
    max_abs = np.max(np.abs(all_points))
    buffer = max(5, max_abs + 2) 
    X_batas = [-buffer, buffer]
    Y_batas = [-buffer, buffer]

    # Plot Bentuk Awal (Biru - garis putus-putus)
    awal_closed = close_polygon(titik_awal_matrix)
    ax.plot(awal_closed[0, :], awal_closed[1, :], 'b--', linewidth=2, alpha=0.6, label='Bentuk Awal')
    ax.plot(titik_awal_matrix[0, :], titik_awal_matrix[1, :], 'bo', markersize=6) # Plot vertices

    # Plot Bentuk Hasil (Merah - garis solid)
    hasil_closed = close_polygon(titik_hasil_matrix)
    ax.plot(hasil_closed[0, :], hasil_closed[1, :], 'r-', linewidth=2, label='Bentuk Hasil')
    ax.plot(titik_hasil_matrix[0, :], titik_hasil_matrix[1, :], 'ro', markersize=6) # Plot vertices

    # Grid dan Axes
    ax.grid(True, linestyle='--')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    # Batas Sumbu
    ax.set_xlim(X_batas[0], X_batas[1])
    ax.set_ylim(Y_batas[0], Y_batas[1])
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")
    ax.set_title(judul)
    ax.legend(loc='upper right')
    ax.set_aspect('equal', adjustable='box') 
    st.pyplot(fig)
    plt.close(fig)

# --- 1. Konfigurasi Awal (Dilakukan di luar kolom) ---
st.subheader("1. Pilih Bangun Datar Awal")
pilihan_bentuk = st.selectbox(
    "Bangun Datar:",
    list(SHAPES.keys())
)
titik_awal_matrix = SHAPES[pilihan_bentuk]

# Tampilkan Koordinat Awal
st.caption("Koordinat Awal:")
coords_text = " | ".join([f"$P_{i+1}({titik_awal_matrix[0, i]:.1f}, {titik_awal_matrix[1, i]:.1f})$" for i in range(titik_awal_matrix.shape[1] - 1 if "Garis" not in pilihan_bentuk else titik_awal_matrix.shape[1])])
st.markdown(coords_text)
st.markdown("---")

# --- 2. Implementasi Layout Dua Kolom ---
col_input, col_output = st.columns([1, 1.3], gap="large") # Input (Kiri) dan Output Grafik (Kanan)

# Inisialisasi variabel hasil
titik_hasil_matrix = titik_awal_matrix.copy()
transformasi_aktif = "Awal"

# --- Kolom Kiri: Input dan Kontrol (Menggunakan Tabs) ---
with col_input:
    st.header("2. Kontrol Transformasi")
    
    # Buat Tabs untuk setiap transformasi
    tab1, tab2, tab3, tab4 = st.tabs(["Translasi", "Refleksi", "Rotasi", "Dilatasi"])

    with tab1: # Translasi
        transformasi_aktif = "Translasi"
        st.markdown("**Translasi** (Pergeseran): $P(x, y) \\to P'(x+a, y+b)$")
        
        a = st.slider("Vektor Translasi 'a' (Horizontal)", -5, 5, 2, key='a_t')
        b = st.slider("Vektor Translasi 'b' (Vertikal)", -5, 5, 1, key='b_t')

        # Perhitungan
        matriks_translasi = np.array([[a], [b]])
        titik_hasil_matrix = titik_awal_matrix + matriks_translasi 
        
        st.subheader("Rumus")
        st.latex(f"\\text{{Matriks Hasil}} = \\text{{Matriks Awal}} + \\begin{{pmatrix}} {a} \\\\ {b} \\end{{pmatrix}}")

    with tab2: # Refleksi
        transformasi_aktif = "Refleksi"
        st.markdown("**Refleksi** (Pencerminan): Mencerminkan bentuk terhadap sumbu atau garis.")
        
        pilihan_refleksi = st.selectbox(
            "Pilih Garis Refleksi",
            ["Sumbu X ($y=0$)", "Sumbu Y ($x=0$)", "Garis $y=x$", "Garis $y=-x$"],
            key='ref_pilih'
        )

        matriks_transformasi = np.array([[1, 0], [0, 1]]) # Default
        if pilihan_refleksi == "Sumbu X ($y=0$)":
            matriks_transformasi = np.array([[1, 0], [0, -1]])
        elif pilihan_refleksi == "Sumbu Y ($x=0$)":
            matriks_transformasi = np.array([[-1, 0], [0, 1]])
        elif pilihan_refleksi == "Garis $y=x$":
            matriks_transformasi = np.array([[0, 1], [1, 0]])
        elif pilihan_refleksi == "Garis $y=-x$":
            matriks_transformasi = np.array([[0, -1], [-1, 0]])
        
        # Perhitungan
        titik_hasil_matrix = matriks_transformasi @ titik_awal_matrix
        
        st.subheader("Rumus")
        st.markdown(f"**Matriks Refleksi:**")
        st.latex(f"\\begin{{pmatrix}} x' \\\\ y' \\end{{pmatrix}} = \\begin{{pmatrix}} {matriks_transformasi[0, 0]} & {matriks_transformasi[0, 1]} \\\\ {matriks_transformasi[1, 0]} & {matriks_transformasi[1, 1]} \\end{{pmatrix}} \\begin{{pmatrix}} x \\\\ y \\end{{pmatrix}}")

    with tab3: # Rotasi
        transformasi_aktif = "Rotasi"
        st.markdown("**Rotasi** (Perputaran): Memutar bentuk terhadap titik pusat $(0,0)$.")
        
        sudut_derajat = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90, key='rot_sudut')
        sudut_rad = np.deg2rad(sudut_derajat)

        # Matriks Rotasi
        cos_theta = np.cos(sudut_rad)
        sin_theta = np.sin(sudut_rad)
        matriks_transformasi = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])

        # Perhitungan
        titik_hasil_matrix_mentah = matriks_transformasi @ titik_awal_matrix
        titik_hasil_matrix = np.round(titik_hasil_matrix_mentah, 2)
        
        st.subheader("Rumus")
        st.markdown(f"**Sudut:** ${sudut_derajat}^\circ$.")
        st.markdown(f"**Matriks Rotasi:**")
        st.latex(f"\\begin{{pmatrix}} \\cos{{\\theta}} & -\\sin{{\\theta}} \\\\ \\sin{{\\theta}} & \\cos{{\\theta}} \\end{{pmatrix}} \\approx \\begin{{pmatrix}} {round(cos_theta, 2)} & {round(-sin_theta, 2)} \\\\ {round(sin_theta, 2)} & {round(cos_theta, 2)} \\end{{pmatrix}}")

    with tab4: # Dilatasi
        transformasi_aktif = "Dilatasi"
        st.markdown("**Dilatasi** (Penskalaan): Memperbesar atau memperkecil bentuk terhadap titik pusat $(0,0)$.")
        
        k = st.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1, key='dil_k')

        # Matriks Dilatasi
        matriks_transformasi = np.array([
            [k, 0],
            [0, k]
        ])

        # Perhitungan
        titik_hasil_matrix = matriks_transformasi @ titik_awal_matrix
        
        st.subheader("Rumus")
        st.markdown(f"**Faktor Skala:** $k={k}$.")
        st.markdown(f"**Matriks Dilatasi:**")
        st.latex(f"\\text{{Matriks Dilatasi}} = \\begin{{pmatrix}} {k} & 0 \\\\ 0 & {k} \\end{{pmatrix}}")

# --- Kolom Kanan: Output Grafik ---
with col_output:
    st.header(f"3. Visualisasi Hasil")
    
    # Panggil fungsi plot dengan hasil dari tab yang sedang aktif
    plot_transformasi(titik_awal_matrix, titik_hasil_matrix, f"Transformasi: {transformasi_aktif}")

    st.subheader("Koordinat Hasil")
    # Tampilkan koordinat setelah transformasi
    hasil_coords_text = " | ".join([f"$P'_{i+1}({titik_hasil_matrix[0, i]:.2f}, {titik_hasil_matrix[1, i]:.2f})$" for i in range(titik_hasil_matrix.shape[1] - 1 if "Garis" not in pilihan_bentuk else titik_hasil_matrix.shape[1])])
    st.markdown(hasil_coords_text)
