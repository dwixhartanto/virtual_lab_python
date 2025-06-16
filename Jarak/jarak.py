import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

st.title("Simulasi Gerak Kendaraan: Menyusul dan Bertemu")
st.markdown("""
    Selamat datang di media pembelajaran interaktif ini!
    Ayo kita eksplorasi bagaimana dua kendaraan bergerak dan kapan mereka bisa saling menyusul atau bertemu.
    Coba ubah-ubah nilai kecepatan, jarak, dan waktu berangkat, lalu amati apa yang terjadi pada grafik!
""")

st.sidebar.header("Pengaturan Simulasi")

# --- Input Pengguna ---
scenario = st.sidebar.selectbox(
    "Pilih Skenario:",
    ("Kendaraan Menyusul", "Kendaraan Bertemu")
)

st.sidebar.subheader("Detail Kendaraan 1")
v1 = st.sidebar.number_input("Kecepatan Kendaraan 1 (km/jam)", value=60.0, min_value=1.0, step=5.0)
start_time1 = st.sidebar.number_input("Waktu Keberangkatan Kendaraan 1 (jam)", value=0.0, min_value=0.0, step=0.5)

st.sidebar.subheader("Detail Kendaraan 2")
v2 = st.sidebar.number_input("Kecepatan Kendaraan 2 (km/jam)", value=40.0, min_value=1.0, step=5.0)
start_time2 = st.sidebar.number_input("Waktu Keberangkatan Kendaraan 2 (jam)", value=0.0, min_value=0.0, step=0.5)

initial_distance = st.sidebar.number_input("Jarak Awal Antara Kendaraan (km)", value=100.0, min_value=0.0, step=10.0)

duration = st.sidebar.slider("Durasi Simulasi Maksimal (jam)", value=5, min_value=1, max_value=24)

st.sidebar.write("---")
simulate_button = st.sidebar.button("Mulai Simulasi")

# --- Logika Perhitungan ---
if simulate_button:
    st.subheader("Hasil Simulasi")

    time_points = np.linspace(0, duration, 500) # Titik-titik waktu untuk grafik

    # Posisi awal kendaraan
    # Asumsi kendaraan 1 mulai dari 0
    pos_veh1_at_t0 = 0.0

    # Kendaraan 2 dimulai dari initial_distance (baik menyusul maupun bertemu)
    pos_veh2_at_t0 = initial_distance

    positions_veh1 = []
    positions_veh2 = []

    time_of_event = None # Waktu terjadi penyusulan/pertemuan
    distance_at_event = None # Jarak saat penyusulan/pertemuan

    # Untuk menyimpan data event secara akurat
    min_diff = float('inf')
    best_time_idx = -1

    for i, t in enumerate(time_points):
        # Penyesuaian waktu efektif berangkat untuk masing-masing kendaraan
        effective_t1 = max(0, t - start_time1)
        effective_t2 = max(0, t - start_time2)

        pos1 = pos_veh1_at_t0 + (v1 * effective_t1)

        # Bagian ini yang krusial diperbaiki
        if scenario == "Kendaraan Bertemu":
            # Kendaraan 2 bergerak dari initial_distance menuju 0 (mundur)
            pos2 = pos_veh2_at_t0 - (v2 * effective_t2)
        else: # Skenario "Kendaraan Menyusul"
            # Kendaraan 2 bergerak dari initial_distance ke arah yang sama dengan Kendaraan 1 (maju)
            pos2 = pos_veh2_at_t0 + (v2 * effective_t2)

        positions_veh1.append(pos1)
        positions_veh2.append(pos2)

        # Deteksi event
        if scenario == "Kendaraan Menyusul":
            # Kendaraan 1 menyusul kendaraan 2 jika pos1 >= pos2 dan belum pernah menyusul
            # Juga pastikan Kendaraan 1 lebih cepat dari Kendaraan 2 untuk skenario ini,
            # atau setidaknya berangkat duluan sehingga bisa menyusul.
            if v1 > v2 or start_time1 < start_time2: # Cek kondisi potensial menyusul
                 if pos1 >= pos2 and time_of_event is None and t > 0:
                    # Pastikan Kendaraan 1 awalnya di belakang atau sama posisi
                    # agar ini bukan deteksi yang salah di awal simulasi.
                    if (pos_veh1_at_t0 + (v1 * max(0, time_points[0] - start_time1))) < \
                       (pos_veh2_at_t0 + (v2 * max(0, time_points[0] - start_time2))):
                        time_of_event = t
                        distance_at_event = pos1
        elif scenario == "Kendaraan Bertemu":
            # Kendaraan bertemu jika posisi mereka berpotongan (atau jarak sangat dekat)
            # Karena mereka bergerak berlawanan, titik perpotongan adalah pertemuan
            if time_of_event is None: # Hanya deteksi sekali
                current_diff = abs(pos1 - pos2)
                # Jika ada persilangan atau jarak sangat kecil
                if i > 0 and ((positions_veh1[i-1] < positions_veh2[i-1] and pos1 >= pos2) or \
                              (positions_veh1[i-1] > positions_veh2[i-1] and pos1 <= pos2)):
                    time_of_event = t
                    distance_at_event = (pos1 + pos2) / 2 # Ambil rata-rata posisi saat bertemu
                    
                # Alternatif: Cari titik terdekat jika tidak ada persilangan sempurna
                if current_diff < min_diff:
                    min_diff = current_diff
                    best_time_idx = i
                # Jika sudah melewati titik terdekat dan belum terdeteksi pertemuan (misal karena langkah waktu besar)
                if i > best_time_idx + 10 and time_of_event is None and min_diff < 1.0: # Jika jaraknya sudah sangat dekat
                    time_of_event = time_points[best_time_idx]
                    distance_at_event = (positions_veh1[best_time_idx] + positions_veh2[best_time_idx]) / 2


    # --- Visualisasi ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time_points, positions_veh1, label=f'Kendaraan 1 (v={v1} km/jam, start={start_time1} jam)', color='blue')
    ax.plot(time_points, positions_veh2, label=f'Kendaraan 2 (v={v2} km/jam, start={start_time2} jam)', color='red', linestyle='--')

    if time_of_event is not None:
        ax.axvline(x=time_of_event, color='green', linestyle=':', label=f'Waktu Event: {time_of_event:.2f} jam')
        ax.plot(time_of_event, distance_at_event, 'go', markersize=8, label=f'Posisi Event: {distance_at_event:.2f} km')
        st.success(f"**{scenario} terjadi pada waktu:** {time_of_event:.2f} jam")
        st.success(f"**Pada jarak dari titik awal Kendaraan 1:** {distance_at_event:.2f} km")
    else:
        st.warning(f"**{scenario} tidak terjadi dalam durasi simulasi ({duration} jam).** Coba tingkatkan durasi atau ubah parameter.")


    ax.set_xlabel("Waktu (jam)")
    ax.set_ylabel("Posisi (km)")
    ax.set_title(f"Grafik Posisi vs Waktu ({scenario})")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Ayo Berpikir!")
    st.markdown("""
    Setelah mencoba beberapa kali dengan mengubah-ubah nilai di samping, coba jawab pertanyaan berikut:
    1.  **Kendaraan Menyusul:** Apa hubungan antara kecepatan kedua kendaraan, jarak awal, dan waktu penyusulan? Bisakah kamu menemukan sebuah rumus yang menghubungkan ketiganya?
    2.  **Kendaraan Bertemu:** Bagaimana hubungan antara kecepatan, jarak awal, dan waktu pertemuan? Apakah ada rumus yang bisa kamu rumuskan?
    3.  Apa yang terjadi jika kecepatan kendaraan yang di depan lebih cepat dalam skenario 'menyusul'?
    4.  Apa yang terjadi jika salah satu kendaraan berangkat lebih dulu?
    """)

    st.markdown("---")
    st.subheader("Rumus yang Mungkin Kamu Temukan (Jangan langsung dibuka ya! Coba cari tahu sendiri dulu!)")
    with st.expander("Klik untuk melihat petunjuk rumus"):
        st.markdown(r"""
        * **Konsep Dasar:** Jarak = Kecepatan $\times$ Waktu.
        * **Kasus Menyusul:**
            * Misalkan $t$ adalah waktu saat menyusul (dihitung dari $t=0$).
            * Posisi Kendaraan 1: $P_1(t) = v_1 \times \max(0, t - \text{start\_time}_1)$
            * Posisi Kendaraan 2: $P_2(t) = \text{initial\_distance} + (v_2 \times \max(0, t - \text{start\_time}_2))$
            * Saat menyusul, $P_1(t) = P_2(t)$.
            * $v_1 \times (t - \text{start\_time}_1) = \text{initial\_distance} + v_2 \times (t - \text{start\_time}_2)$
            * Coba substitusikan dan selesaikan untuk $t$!
        * **Kasus Bertemu:**
            * Misalkan $t$ adalah waktu saat bertemu (dihitung dari $t=0$).
            * Posisi Kendaraan 1: $P_1(t) = v_1 \times \max(0, t - \text{start\_time}_1)$
            * Posisi Kendaraan 2: $P_2(t) = \text{initial\_distance} - (v_2 \times \max(0, t - \text{start\_time}_2))$
            * Saat bertemu, posisi mereka sama: $P_1(t) = P_2(t)$.
            * $v_1 \times (t - \text{start\_time}_1) = \text{initial\_distance} - v_2 \times (t - \text{start\_time}_2)$
            * Coba substitusikan dan selesaikan untuk $t$!
        """)

    st.markdown("---")
    st.subheader("Contoh Soal Kontekstual")
    st.markdown("""
    1.  **Soal Menyusul:** "Andi naik motor dengan kecepatan 60 km/jam. Satu jam kemudian, Budi menyusul dengan mobil berkecepatan 80 km/jam dari tempat yang sama. Kapan dan di mana Budi akan menyusul Andi?"
    2.  **Soal Bertemu:** "Kota A dan Kota B berjarak 300 km. Sebuah bus berangkat dari Kota A menuju Kota B dengan kecepatan 70 km/jam. Pada saat yang bersamaan, sebuah truk berangkat dari Kota B menuju Kota A dengan kecepatan 50 km/jam. Kapan dan di mana mereka akan bertemu?"
    """)
