import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri Interaktif",
    layout="wide"
)

## 📌 Fungsi Transformasi Geometri
# Titik awal yang akan diubah. Kita gunakan bentuk matriks 2xN
# untuk kemudahan operasi matriks. Misalnya, titik (1, 2) dan (3, 4)
TITIK_AWAL = np.array([[1.0, 3.0, 1.0], [2.0, 2.0, 4.0]]) # 3 Titik untuk segitiga

def translasi(titik, tx, ty):
    """Melakukan translasi pada titik."""
    # Matriks translasi untuk setiap titik
    T = np.array([[tx], [ty]])
    return titik + T

def dilatasi(titik, kx, ky):
    """Melakukan dilatasi pada titik (terhadap titik asal (0,0))."""
    # Matriks transformasi dilatasi
    D = np.array([[kx, 0], [0, ky]])
    return D @ titik

def rotasi(titik, sudut_derajat):
    """Melakukan rotasi (terhadap titik asal (0,0))."""
    sudut_rad = np.deg2rad(sudut_derajat)
    cos_t = np.cos(sudut_rad)
    sin_t = np.sin(sudut_rad)
    
    # Matriks transformasi rotasi berlawanan arah jarum jam
    R = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
    return R @ titik

## 📐 Fungsi Plotting
def plot_transformasi(titik_asli, titik_transformasi, title):
    """Membuat plot untuk visualisasi transformasi."""
    fig, ax = plt.subplots()
    
    # Menampilkan titik asli (misalnya, sebagai segitiga)
    # Menambahkan titik pertama di akhir agar polygon tertutup
    titik_asli_polygon = np.column_stack((titik_asli, titik_asli[:, 0]))
    ax.plot(titik_asli_polygon[0, :], titik_asli_polygon[1, :], 'b-o', label='Benda Asli')
    
    # Menampilkan titik hasil transformasi
    titik_transformasi_polygon = np.column_stack((titik_transformasi, titik_transformasi[:, 0]))
    ax.plot(titik_transformasi_polygon[0, :], titik_transformasi_polygon[1, :], 'r--s', label='Bayangan')
    
    # Konfigurasi plot
    limit = max(np.max(np.abs(titik_transformasi)), 5) * 1.5
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel("Sumbu X"); ax.set_ylabel("Sumbu Y")
    
    st.pyplot(fig)

## 🛠️ Antarmuka Streamlit (UI)

st.title("➗ Virtual Lab: Visualisasi Transformasi Geometri")
st.markdown("Gunakan sidebar untuk memilih dan mengatur parameter transformasi.")

# --- Sidebar untuk Kontrol ---
st.sidebar.header("Pengaturan Transformasi")
pilihan_transformasi = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ("Translasi (Pergeseran)", "Dilatasi (Perkalian/Penskalaan)", "Rotasi (Perputaran)")
)

# --- Tampilan Utama Berdasarkan Pilihan ---

titik_transformasi = TITIK_AWAL # Inisialisasi

if pilihan_transformasi == "Translasi (Pergeseran)":
    st.header("➡️ Translasi (Pergeseran)")
    
    col1, col2 = st.columns(2)
    tx = col1.slider("Pergeseran X ($t_x$)", -5.0, 5.0, 2.0, 0.1)
    ty = col2.slider("Pergeseran Y ($t_y$)", -5.0, 5.0, 1.0, 0.1)
    
    titik_transformasi = translasi(TITIK_AWAL, tx, ty)
    
    st.latex(f"T = \\begin{{pmatrix}} {tx} \\\\ {ty} \\end{{pmatrix}}")
    st.latex("P' = P + T")
    
    plot_transformasi(
        TITIK_AWAL, 
        titik_transformasi, 
        f"Translasi dengan $T=({tx}, {ty})$"
    )

elif pilihan_transformasi == "Dilatasi (Perkalian/Penskalaan)":
    st.header(" 확대 Dilatasi (Perkalian/Penskalaan)")
    
    col1, col2 = st.columns(2)
    kx = col1.slider("Faktor Skala X ($k_x$)", 0.1, 5.0, 2.0, 0.1)
    ky = col2.slider("Faktor Skala Y ($k_y$)", 0.1, 5.0, 2.0, 0.1)
    
    titik_transformasi = dilatasi(TITIK_AWAL, kx, ky)
    
    st.latex(f"D = \\begin{{pmatrix}} {kx} & 0 \\\\ 0 & {ky} \\end{{pmatrix}}")
    st.latex("P' = D \\cdot P")
    
    plot_transformasi(
        TITIK_AWAL, 
        titik_transformasi, 
        f"Dilatasi dengan Faktor Skala $k_x={kx}, k_y={ky}$ (Pusat $(0,0)$)"
    )

elif pilihan_transformasi == "Rotasi (Perputaran)":
    st.header("🔄 Rotasi (Perputaran)")
    
    sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 45, 5)
    
    titik_transformasi = rotasi(TITIK_AWAL, sudut)
    
    cos_t = np.cos(np.deg2rad(sudut)); sin_t = np.sin(np.deg2rad(sudut))
    st.latex(f"R({sudut}^\\circ) = \\begin{{pmatrix}} {cos_t:.3f} & {-sin_t:.3f} \\\\ {sin_t:.3f} & {cos_t:.3f} \\end{{pmatrix}}")
    st.latex("P' = R \\cdot P")
    
    plot_transformasi(
        TITIK_AWAL, 
        titik_transformasi, 
        f"Rotasi sebesar ${sudut}^\\circ$ (Pusat $(0,0)$, Berlawanan Jarum Jam)"
    )

st.caption("Catatan: Objek yang diuji adalah segitiga dengan titik sudut: (1, 2), (3, 2), dan (1, 4).")
