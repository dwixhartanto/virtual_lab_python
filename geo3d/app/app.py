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
