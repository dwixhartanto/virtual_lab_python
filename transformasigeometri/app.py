import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📐 Virtual Lab: Transformasi Geometri Interaktif")
st.markdown("Eksplorasi **Rotasi, Dilatasi, Refleksi, dan Translasi** secara visual.")

# Inisialisasi Titik Awal
X = 2
Y = 3
titik_awal = np.array([X, Y])

# --- Fungsi Plotting ---
def plot_transformasi(titik_awal, titik_hasil, judul, X_batas, Y_batas):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot Titik Awal (Biru)
    ax.plot(titik_awal[0], titik_awal[1], 'bo', label=f'Awal: ({titik_awal[0]}, {titik_awal[1]})')

    # Plot Titik Hasil (Merah)
    ax.plot(titik_hasil[0], titik_hasil[1], 'ro', label=f'Hasil: ({titik_hasil[0]}, {titik_hasil[1]})')

    # Garis dari titik awal ke hasil (untuk visualisasi pergerakan)
    ax.plot([titik_awal[0], titik_hasil[0]], [titik_awal[1], titik_hasil[1]], 'r--')

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
    ax.set_aspect('equal', adjustable='box') # Penting agar grid terlihat persegi
    st.pyplot(fig)
    plt.close(fig)

# --- Sidebar Input Titik Awal ---
st.sidebar.header("Titik Awal $P(x, y)$")
X_input = st.sidebar.slider("Koordinat X:", -10, 10, X)
Y_input = st.sidebar.slider("Koordinat Y:", -10, 10, Y)
titik_awal = np.array([X_input, Y_input])
st.sidebar.info(f"Titik saat ini: $P({X_input}, {Y_input})$")

# --- Pilih Transformasi ---
transformasi_pilih = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ["Translasi", "Refleksi", "Rotasi", "Dilatasi"]
)

# --- Main Content Area ---
X_batas = [-10, 10]
Y_batas = [-10, 10]

st.header(f"✨ Mode: {transformasi_pilih}")

if transformasi_pilih == "Translasi":
    st.markdown("**Translasi** (Pergeseran): $P(x, y) \\to P'(x+a, y+b)$")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("Vektor Translasi 'a' (Horizontal)", -5, 5, 2)
    with col2:
        b = st.slider("Vektor Translasi 'b' (Vertikal)", -5, 5, 1)

    matriks_translasi = np.array([a, b])
    titik_hasil = titik_awal + matriks_translasi
    
    st.subheader("Rumus dan Hasil")
    st.latex(f"P' = P + T = ({X_input}, {Y_input}) + ({a}, {b}) = ({titik_hasil[0]}, {titik_hasil[1]})")

    plot_transformasi(titik_awal, titik_hasil, "Translasi Titik", X_batas, Y_batas)

elif transformasi_pilih == "Refleksi":
    st.markdown("**Refleksi** (Pencerminan): Mencerminkan titik terhadap sumbu atau garis.")
    
    pilihan_refleksi = st.selectbox(
        "Pilih Garis Refleksi",
        ["Sumbu X ($y=0$)", "Sumbu Y ($x=0$)", "Garis $y=x$", "Garis $y=-x$"]
    )

    if pilihan_refleksi == "Sumbu X ($y=0$)":
        matriks_refleksi = np.array([[1, 0], [0, -1]])
        titik_hasil = matriks_refleksi @ titik_awal
    elif pilihan_refleksi == "Sumbu Y ($x=0$)":
        matriks_refleksi = np.array([[-1, 0], [0, 1]])
        titik_hasil = matriks_refleksi @ titik_awal
    elif pilihan_refleksi == "Garis $y=x$":
        matriks_refleksi = np.array([[0, 1], [1, 0]])
        titik_hasil = matriks_refleksi @ titik_awal
    elif pilihan_refleksi == "Garis $y=-x$":
        matriks_refleksi = np.array([[0, -1], [-1, 0]])
        titik_hasil = matriks_refleksi @ titik_awal
    
    st.subheader("Rumus dan Hasil")
    st.markdown(f"**Matriks Transformasi:**")
    st.latex(f"\\begin{{pmatrix}} x' \\\\ y' \\end{{pmatrix}} = \\begin{{pmatrix}} {matriks_refleksi[0, 0]} & {matriks_refleksi[0, 1]} \\\\ {matriks_refleksi[1, 0]} & {matriks_refleksi[1, 1]} \\end{{pmatrix}} \\begin{{pmatrix}} {X_input} \\\\ {Y_input} \\end{{pmatrix}} = \\begin{{pmatrix}} {titik_hasil[0]} \\\\ {titik_hasil[1]} \\end{{pmatrix}}")

    plot_transformasi(titik_awal, titik_hasil, f"Refleksi Terhadap {pilihan_refleksi}", X_batas, Y_batas)

elif transformasi_pilih == "Rotasi":
    st.markdown("**Rotasi** (Perputaran): Memutar titik terhadap titik pusat.")
    
    # Rotasi diasumsikan terhadap titik pusat (0,0)
    sudut_derajat = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90)
    sudut_rad = np.deg2rad(sudut_derajat)

    # Matriks Rotasi
    cos_theta = np.cos(sudut_rad)
    sin_theta = np.sin(sudut_rad)
    matriks_rotasi = np.array([
        [cos_theta, -sin_theta],
        [sin_theta, cos_theta]
    ])

    titik_hasil_mentah = matriks_rotasi @ titik_awal
    # Pembulatan untuk hasil yang lebih rapi (misalnya -0.00000001 jadi 0)
    titik_hasil = np.round(titik_hasil_mentah, 2)
    
    st.subheader("Rumus dan Hasil")
    st.markdown(f"**Sudut:** ${sudut_derajat}^\circ$.")
    st.markdown(f"**Matriks Rotasi:**")
    st.latex(f"\\begin{{pmatrix}} \\cos{{\\theta}} & -\\sin{{\\theta}} \\\\ \\sin{{\\theta}} & \\cos{{\\theta}} \\end{{pmatrix}} = \\begin{{pmatrix}} {round(cos_theta, 2)} & {round(-sin_theta, 2)} \\\\ {round(sin_theta, 2)} & {round(cos_theta, 2)} \\end{{pmatrix}}")
    st.latex(f"P' = ({titik_hasil[0]}, {titik_hasil[1]})")

    plot_transformasi(titik_awal, titik_hasil, f"Rotasi {sudut_derajat}° Terhadap (0,0)", X_batas, Y_batas)

elif transformasi_pilih == "Dilatasi":
    st.markdown("**Dilatasi** (Penskalaan): Memperbesar atau memperkecil titik terhadap titik pusat.")
    
    k = st.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1)

    # Matriks Dilatasi terhadap titik pusat (0,0)
    matriks_dilatasi = np.array([
        [k, 0],
        [0, k]
    ])

    titik_hasil = matriks_dilatasi @ titik_awal
    
    st.subheader("Rumus dan Hasil")
    st.markdown(f"**Faktor Skala:** $k={k}$.")
    st.markdown(f"**Matriks Dilatasi:**")
    st.latex(f"\\begin{{pmatrix}} k & 0 \\\\ 0 & k \\end{{pmatrix}} = \\begin{{pmatrix}} {k} & 0 \\\\ 0 & {k} \\end{{pmatrix}}")
    st.latex(f"P' = (k \\cdot x, k \\cdot y) = ({k} \\cdot {X_input}, {k} \\cdot {Y_input}) = ({titik_hasil[0]}, {titik_hasil[1]})")

    # Sesuaikan batas plot agar titik hasil tetap terlihat jika terjadi perbesaran besar
    max_val = max(abs(titik_hasil[0]), abs(titik_hasil[1]), abs(X_input), abs(Y_input))
    buffer = max(5, max_val + 2) # Buffer minimum 5 atau 2 lebih dari nilai maks
    X_batas = [-buffer, buffer]
    Y_batas = [-buffer, buffer]

    plot_transformasi(titik_awal, titik_hasil, f"Dilatasi dengan k={k} Terhadap (0,0)", X_batas, Y_batas)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dibuat dengan Streamlit**")
