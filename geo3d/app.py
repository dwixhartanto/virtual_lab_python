import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab Geometri Dimensi 3",
    layout="wide"
)

st.title("🧊 Virtual Lab: Geometri Dimensi 3 (Bangun Ruang)")
st.markdown("Eksplorasi visual dan hitung jarak/sudut pada objek 3D.")

# --- 1. Definisi Bangun Ruang (Kubus) ---
# Kita fokus pada Kubus ABCD.EFGH untuk kemudahan input dan perhitungan
def get_kubus_vertices(s):
    # s: panjang sisi
    return {
        'A': np.array([0, 0, 0]), 'B': np.array([s, 0, 0]), 
        'C': np.array([s, s, 0]), 'D': np.array([0, s, 0]),
        'E': np.array([0, 0, s]), 'F': np.array([s, 0, s]),
        'G': np.array([s, s, s]), 'H': np.array([0, s, s]),
    }

# Definisi Rusuk Kubus (untuk Plotly)
KUBUS_EDGES = [
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), # Alas
    ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'E'), # Atas
    ('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H')  # Rusuk Tegak
]

# --- 2. Fungsi Visualisasi 3D (Plotly) ---
def plot_kubus(vertices, s, highlight_points=None, line_coords=None):
    fig = go.Figure()
    
    # 1. Plot Titik (Vertices)
    x_coords = [v[0] for v in vertices.values()]
    y_coords = [v[1] for v in vertices.values()]
    z_coords = [v[2] for v in vertices.values()]
    labels = list(vertices.keys())

    fig.add_trace(go.Scatter3d(
        x=x_coords, y=y_coords, z=z_coords,
        mode='markers+text',
        marker=dict(size=5, color='blue'),
        text=labels,
        textfont=dict(size=12, color='black'),
        name='Titik Sudut',
        hoverinfo='text',
        hovertext=[f'{l}({v[0]}, {v[1]}, {v[2]})' for l, v in vertices.items()]
    ))

    # 2. Plot Rusuk (Edges)
    for p1, p2 in KUBUS_EDGES:
        v1 = vertices[p1]
        v2 = vertices[p2]
        fig.add_trace(go.Scatter3d(
            x=[v1[0], v2[0]], y=[v1[1], v2[1]], z=[v1[2], v2[2]],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))

    # 3. Highlight Garis Jarak (Jika ada)
    if line_coords:
        v_start = vertices[line_coords[0]]
        v_end = vertices[line_coords[1]]
        fig.add_trace(go.Scatter3d(
            x=[v_start[0], v_end[0]], y=[v_start[1], v_end[1]], z=[v_start[2], v_end[2]],
            mode='lines',
            line=dict(color='red', width=5),
            name=f'Jarak {line_coords[0]}{line_coords[1]}'
        ))
        
    # 4. Highlight Titik Terpilih
    if highlight_points:
        for p in highlight_points:
            v = vertices[p]
            fig.add_trace(go.Scatter3d(
                x=[v[0]], y=[v[1]], z=[v[2]],
                mode='markers',
                marker=dict(size=8, color='red', symbol='circle'),
                showlegend=False
            ))

    # Pengaturan Layout
    max_range = s * 1.5
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_range/3, max_range], backgroundcolor="rgba(0,0,0,0)", gridcolor="white"),
            yaxis=dict(range=[-max_range/3, max_range], backgroundcolor="rgba(0,0,0,0)", gridcolor="white"),
            zaxis=dict(range=[-max_range/3, max_range], backgroundcolor="rgba(0,0,0,0)", gridcolor="white"),
            aspectmode='cube',
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(r=0, l=0, b=0, t=0),
        height=550
    )
    return fig

# --- 3. Fungsi Perhitungan Jarak ---

def hitung_jarak_titik_titik(p1, p2, s):
    # Hitung Jarak Euclidean: sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
    vector = p2 - p1
    distance_sq = np.sum(vector**2)
    distance = np.sqrt(distance_sq)
    
    # Menentukan jenis jarak (rusuk, diagonal sisi, atau diagonal ruang)
    if distance == s:
        jenis = f"Panjang Rusuk ({s})"
    elif distance == s * np.sqrt(2):
        jenis = f"Diagonal Sisi ({s}\\sqrt{{2}})"
    elif distance == s * np.sqrt(3):
        jenis = f"Diagonal Ruang ({s}\\sqrt{{3}})"
    else:
        jenis = "Jarak Umum"
        
    return distance, jenis

# --- 4. Streamlit UI Layout ---

st.header("Kubus ABCD.EFGH")

# Input Sisi Kubus
sisi = st.slider("Panjang Sisi Kubus (s)", 2.0, 10.0, 4.0, 0.5)

vertices = get_kubus_vertices(sisi)
titik_labels = list(vertices.keys())

col_input, col_visual = st.columns([1, 1.5])

# --- Kolom Kiri: Input Perhitungan ---
with col_input:
    st.subheader("1. Pilih Perhitungan")
    mode_perhitungan = st.selectbox(
        "Mode:",
        ["Jarak Titik ke Titik", "Jarak Titik ke Garis", "Jarak Titik ke Bidang"]
    )
    
    st.markdown("---")
    
    # Jarak Titik ke Titik
    if mode_perhitungan == "Jarak Titik ke Titik":
        st.subheader("2. Jarak Titik ke Titik")
        
        c1, c2 = st.columns(2)
        titik_awal = c1.selectbox("Titik Awal", titik_labels, key='p1')
        titik_akhir = c2.selectbox("Titik Akhir", titik_labels, index=6, key='p2')
        
        if titik_awal and titik_akhir:
            v_awal = vertices[titik_awal]
            v_akhir = vertices[titik_akhir]
            
            jarak, jenis = hitung_jarak_titik_titik(v_awal, v_akhir, sisi)
            
            st.markdown("### Hasil")
            st.info(f"Jenis Jarak: **{jenis}**")
            st.latex(f"\\text{{Jarak }} {titik_awal}{titik_akhir} = \\sqrt{{({v_akhir[0]}-{v_awal[0]})^2 + ({v_akhir[1]}-{v_awal[1]})^2 + ({v_akhir[2]}-{v_awal[2]})^2}}")
            st.latex(f"\\text{{Jarak }} {titik_awal}{titik_akhir} = {jarak:.3f}")
            
            line_to_highlight = (titik_awal, titik_akhir)
            highlight_points = [titik_awal, titik_akhir]
        else:
            line_to_highlight = None
            highlight_points = None

    elif mode_perhitungan == "Jarak Titik ke Garis":
        st.info("Fitur akan segera ditambahkan.")
        line_to_highlight = None
        highlight_points = None
    
    elif mode_perhitungan == "Jarak Titik ke Bidang":
        st.info("Fitur akan segera ditambahkan.")
        line_to_highlight = None
        highlight_points = None

# --- Kolom Kanan: Visualisasi 3D ---
with col_visual:
    st.subheader("Visualisasi 3D Interaktif")
    
    # Plot Kubus menggunakan hasil perhitungan dari kolom kiri
    if 'line_to_highlight' not in locals():
        line_to_highlight = None
        highlight_points = None
        
    fig = plot_kubus(vertices, sisi, highlight_points=highlight_points, line_coords=line_to_highlight)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(f"Kubus ABCD.EFGH dengan sisi = {sisi}")

st.markdown("---")
st.success("Gunakan mouse Anda untuk memutar, memperbesar/memperkecil, dan menjelajahi objek 3D.")
