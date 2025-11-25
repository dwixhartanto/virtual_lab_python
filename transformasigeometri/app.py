import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri (Bangun Datar)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📐 Virtual Lab: Transformasi Geometri Bangun Datar")
st.markdown("Eksplorasi **Rotasi, Dilatasi, Refleksi, dan Translasi** pada bentuk geometris.")

# --- Definisi Bangun Datar Awal (Matriks 2xN) ---
# Format: np.array([[x1, x2, x3, ...], [y1, y2, y3, ...]])
SHAPES = {
    "Segitiga Siku-Siku": np.array([[2., 5., 2.], [1., 1., 4.]]),
    "Persegi": np.array([[1., 4., 4., 1.], [1., 1., 4., 4.]]),
    "Garis (Dua Titik)": np.array([[-5., 5.], [2., -3.]])
}

# --- Fungsi Plotting (diperbarui untuk Poligon) ---
def plot_transformasi(titik_awal_matrix, titik_hasil_matrix, judul):
    fig, ax = plt.subplots(figsize=(7, 7))

    # Fungsi untuk menutup poligon (menghubungkan titik terakhir ke titik pertama)
    def close_polygon(matrix):
        # np.hstack: menggabungkan kolom-kolom secara horizontal
        # matrix[:, 0:1]: mengambil kolom pertama (titik awal)
        return np.hstack([matrix, matrix[:, 0:1]])

    # 1. Menentukan Batas Plot secara dinamis
    all_points = np.hstack([titik_awal_matrix, titik_hasil_matrix])
    max_abs = np.max(np.abs(all_points))
    buffer = max(5, max_abs + 2) # Buffer minimum 5 atau 2 lebih dari nilai maks
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
    ax.set_aspect('equal', adjustable='box') # Pastikan skala X dan Y sama
    st.pyplot(fig)
    plt.close(fig)

# --- Sidebar Input ---
st.sidebar.header("Konfigurasi Bangun Datar")
pilihan_bentuk = st.sidebar.selectbox(
    "Pilih Bangun Datar Awal",
    list(SHAPES.keys())
)
titik_awal_matrix = SHAPES[pilihan_bentuk]

st.sidebar.markdown("---")

transformasi_pilih = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ["Translasi", "Refleksi", "Rotasi", "Dilatasi"]
)

# Tampilkan Koordinat Awal
st.sidebar.subheader("Koordinat Awal")
for i in range(titik_awal_matrix.shape[1]):
    st.sidebar.caption(f"P{i+1}: ({titik_awal_matrix[0, i]:.1f}, {titik_awal_matrix[1, i]:.1f})")

# --- Main Content Area ---
st.header(f"✨ Mode: {transformasi_pilih}")

if transformasi_pilih == "Translasi":
    st.markdown("**Translasi** (Pergeseran): Menggeser setiap titik dengan vektor yang sama.")

    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("Vektor Translasi 'a' (Horizontal)", -5, 5, 2)
    with col2:
        b = st.slider("Vektor Translasi 'b' (Vertikal)", -5, 5, 1)

    # Lakukan Translasi (penambahan vektor kolom [a, b] ke setiap kolom matriks)
    matriks_translasi = np.array([[a], [b]])
    titik_hasil_matrix = titik_awal_matrix + matriks_translasi # NumPy broadcasting
    
    st.subheader("Konsep")
    st.latex(f"\\text{{Matriks Hasil}} = \\text{{Matriks Awal}} + \\begin{{pmatrix}} {a} \\\\ {b} \\end{{pmatrix}}")
    st.info(f"Setiap titik $P(x, y)$ bergeser menjadi $P'(x+{a}, y+{b})$")

    plot_transformasi(titik_awal_matrix, titik_hasil_matrix, "Translasi Bangun Datar")

elif transformasi_pilih == "Refleksi":
    st.markdown("**Refleksi** (Pencerminan): Mencerminkan bangun datar terhadap sumbu atau garis tertentu.")
    
    pilihan_refleksi = st.selectbox(
        "Pilih Garis Refleksi",
        ["Sumbu X ($y=0$)", "Sumbu Y ($x=0$)", "Garis $y=x$", "Garis $y=-x$"]
    )

    if pilihan_refleksi == "Sumbu X ($y=0$)":
        matriks_transformasi = np.array([[1, 0], [0, -1]])
    elif pilihan_refleksi == "Sumbu Y ($x=0$)":
        matriks_transformasi = np.array([[-1, 0], [0, 1]])
    elif pilihan_refleksi == "Garis $y=x$":
        matriks_transformasi = np.array([[0, 1], [1, 0]])
    elif pilihan_refleksi == "Garis $y=-x$":
        matriks_transformasi = np.array([[0, -1], [-1, 0]])
    
    # Refleksi menggunakan perkalian matriks
    titik_hasil_matrix = matriks_transformasi @ titik_awal_matrix
    
    st.subheader("Konsep")
    st.markdown(f"**Matriks Transformasi:**")
    st.latex(f"\\text{{Matriks Refleksi}} = \\begin{{pmatrix}} {matriks_transformasi[0, 0]} & {matriks_transformasi[0, 1]} \\\\ {matriks_transformasi[1, 0]} & {matriks_transformasi[1, 1]} \\end{{pmatrix}}")

    plot_transformasi(titik_awal_matrix, titik_hasil_matrix, f"Refleksi Terhadap {pilihan_refleksi}")

elif transformasi_pilih == "Rotasi":
    st.markdown("**Rotasi** (Perputaran): Memutar bangun datar terhadap titik pusat $(0,0)$.")
    
    sudut_derajat = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90)
    sudut_rad = np.deg2rad(sudut_derajat)

    # Matriks Rotasi
    cos_theta = np.cos(sudut_rad)
    sin_theta = np.sin(sudut_rad)
    matriks_transformasi = np.array([
        [cos_theta, -sin_theta],
        [sin_theta, cos_theta]
    ])

    # Rotasi menggunakan perkalian matriks
    titik_hasil_matrix_mentah = matriks_transformasi @ titik_awal_matrix
    # Pembulatan untuk hasil yang lebih rapi
    titik_hasil_matrix = np.round(titik_hasil_matrix_mentah, 2)
    
    st.subheader("Konsep")
    st.markdown(f"**Sudut:** ${sudut_derajat}^\circ$ (Berlawanan arah jarum jam positif).")
    st.markdown(f"**Matriks Rotasi:**")
    st.latex(f"\\text{{Matriks Rotasi}} = \\begin{{pmatrix}} \\cos{{\\theta}} & -\\sin{{\\theta}} \\\\ \\sin{{\\theta}} & \\cos{{\\theta}} \\end{{pmatrix}} \\approx \\begin{{pmatrix}} {round(cos_theta, 2)} & {round(-sin_theta, 2)} \\\\ {round(sin_theta, 2)} & {round(cos_theta, 2)} \\end{{pmatrix}}")

    plot_transformasi(titik_awal_matrix, titik_hasil_matrix, f"Rotasi {sudut_derajat}° Terhadap (0,0)")

elif transformasi_pilih == "Dilatasi":
    st.markdown("**Dilatasi** (Penskalaan): Memperbesar atau memperkecil bangun datar terhadap titik pusat $(0,0)$.")
    
    k = st.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1)

    # Matriks Dilatasi
    matriks_transformasi = np.array([
        [k, 0],
        [0, k]
    ])

    # Dilatasi menggunakan perkalian matriks
    titik_hasil_matrix = matriks_transformasi @ titik_awal_matrix
    
    st.subheader("Konsep")
    st.markdown(f"**Faktor Skala:** $k={k}$.")
    st.markdown(f"**Matriks Dilatasi:**")
    st.latex(f"\\text{{Matriks Dilatasi}} = \\begin{{pmatrix}} k & 0 \\\\ 0 & k \\end{{pmatrix}} = \\begin{{pmatrix}} {k} & 0 \\\\ 0 & {k} \\end{{pmatrix}}")
    st.info(f"Setiap titik $P(x, y)$ diskalakan menjadi $P'(k \\cdot x, k \\cdot y)$")

    plot_transformasi(titik_awal_matrix, titik_hasil_matrix, f"Dilatasi dengan k={k} Terhadap (0,0)")

st.sidebar.markdown("---");
st.sidebar.markdown("Kode ini tersedia di GitHub");
