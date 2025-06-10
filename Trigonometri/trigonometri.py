import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# --- Fungsi Pembantu ---
def calculate_triangle(sisi_a=None, sisi_b=None, sisi_c=None, sudut_alpha_deg=None, sudut_beta_deg=None):
    results = {}
    
    if sisi_a is not None and sisi_b is not None:
        results['sisi_c'] = math.sqrt(sisi_a**2 + sisi_b**2)
        results['sudut_alpha_deg'] = math.degrees(math.atan(sisi_a / sisi_b))
        results['sudut_beta_deg'] = 90 - results['sudut_alpha_deg']
        results['sisi_a'] = sisi_a
        results['sisi_b'] = sisi_b
    elif sisi_a is not None and sisi_c is not None:
        if sisi_a >= sisi_c:
            return "Sisi a harus lebih kecil dari hipotenusa c."
        results['sisi_b'] = math.sqrt(sisi_c**2 - sisi_a**2)
        results['sudut_alpha_deg'] = math.degrees(math.asin(sisi_a / sisi_c))
        results['sudut_beta_deg'] = 90 - results['sudut_alpha_deg']
        results['sisi_a'] = sisi_a
        results['sisi_c'] = sisi_c
    elif sisi_b is not None and sisi_c is not None:
        if sisi_b >= sisi_c:
            return "Sisi b harus lebih kecil dari hipotenusa c."
        results['sisi_a'] = math.sqrt(sisi_c**2 - sisi_b**2)
        results['sudut_beta_deg'] = math.degrees(math.asin(sisi_b / sisi_c))
        results['sudut_alpha_deg'] = 90 - results['sudut_beta_deg']
        results['sisi_b'] = sisi_b
        results['sisi_c'] = sisi_c
    elif sisi_a is not None and sudut_alpha_deg is not None:
        if sudut_alpha_deg >= 90 or sudut_alpha_deg <= 0:
            return "Sudut alpha harus antara 0 dan 90 derajat."
        sudut_alpha_rad = math.radians(sudut_alpha_deg)
        results['sisi_b'] = sisi_a / math.tan(sudut_alpha_rad)
        results['sisi_c'] = sisi_a / math.sin(sudut_alpha_rad)
        results['sudut_alpha_deg'] = sudut_alpha_deg
        results['sudut_beta_deg'] = 90 - sudut_alpha_deg
        results['sisi_a'] = sisi_a
    elif sisi_b is not None and sudut_alpha_deg is not None:
        if sudut_alpha_deg >= 90 or sudut_alpha_deg <= 0:
            return "Sudut alpha harus antara 0 dan 90 derajat."
        sudut_alpha_rad = math.radians(sudut_alpha_deg)
        results['sisi_a'] = sisi_b * math.tan(sudut_alpha_rad)
        results['sisi_c'] = sisi_b / math.cos(sudut_alpha_rad)
        results['sudut_alpha_deg'] = sudut_alpha_deg
        results['sudut_beta_deg'] = 90 - sudut_alpha_deg
        results['sisi_b'] = sisi_b
    elif sisi_c is not None and sudut_alpha_deg is not None:
        if sudut_alpha_deg >= 90 or sudut_alpha_deg <= 0:
            return "Sudut alpha harus antara 0 dan 90 derajat."
        sudut_alpha_rad = math.radians(sudut_alpha_deg)
        results['sisi_a'] = sisi_c * math.sin(sudut_alpha_rad)
        results['sisi_b'] = sisi_c * math.cos(sudut_alpha_rad)
        results['sudut_alpha_deg'] = sudut_alpha_deg
        results['sudut_beta_deg'] = 90 - sudut_alpha_deg
        results['sisi_c'] = sisi_c
    elif sudut_alpha_deg is not None and sudut_beta_deg is not None:
        return "Tidak bisa menghitung sisi hanya dengan dua sudut."
    else:
        return "Mohon masukkan setidaknya dua informasi (sisi/sudut) untuk perhitungan."

    return results

# --- Bagian 1: Eksplorasi Segitiga Siku-siku Interaktif ---
def segitiga_siku_section():
    st.header("🔬 Eksplorasi Segitiga Siku-siku")
    st.write("Atur panjang sisi atau besar sudut dan lihat bagaimana segitiga berubah.")

    st.sidebar.subheader("Input Segitiga")
    input_type = st.sidebar.radio(
        "Pilih tipe input:",
        ("Dua Sisi", "Satu Sisi & Satu Sudut")
    )

    sisi_a, sisi_b, sisi_c, sudut_alpha_deg, sudut_beta_deg = None, None, None, None, None
    calculation_results = {}

    if input_type == "Dua Sisi":
        sisi_options = st.sidebar.multiselect(
            "Pilih dua sisi yang diketahui:",
            ["Sisi A", "Sisi B", "Sisi C (Hipotenusa)"],
            max_selections=2
        )
        
        if len(sisi_options) == 2:
            try:
                if "Sisi A" in sisi_options:
                    sisi_a = st.sidebar.number_input("Panjang Sisi A:", min_value=0.1, value=3.0, step=0.1)
                if "Sisi B" in sisi_options:
                    sisi_b = st.sidebar.number_input("Panjang Sisi B:", min_value=0.1, value=4.0, step=0.1)
                if "Sisi C (Hipotenusa)" in sisi_options:
                    sisi_c = st.sidebar.number_input("Panjang Sisi C (Hipotenusa):", min_value=0.1, value=5.0, step=0.1)

                calculation_results = calculate_triangle(sisi_a=sisi_a, sisi_b=sisi_b, sisi_c=sisi_c)
            except ValueError:
                st.sidebar.error("Input tidak valid. Harap masukkan angka.")
        else:
            st.info("Pilih tepat dua sisi untuk melakukan perhitungan.")

    elif input_type == "Satu Sisi & Satu Sudut":
        sisi_known = st.sidebar.selectbox(
            "Sisi yang diketahui:",
            ["Sisi A", "Sisi B", "Sisi C (Hipotenusa)"]
        )
        sudut_known = st.sidebar.selectbox(
            "Sudut yang diketahui (bukan 90°):",
            ["Sudut Alpha (depan A)", "Sudut Beta (depan B)"]
        )

        try:
            if sisi_known == "Sisi A":
                sisi_a = st.sidebar.number_input("Panjang Sisi A:", min_value=0.1, value=3.0, step=0.1)
            elif sisi_known == "Sisi B":
                sisi_b = st.sidebar.number_input("Panjang Sisi B:", min_value=0.1, value=4.0, step=0.1)
            elif sisi_known == "Sisi C (Hipotenusa)":
                sisi_c = st.sidebar.number_input("Panjang Sisi C (Hipotenusa):", min_value=0.1, value=5.0, step=0.1)
            
            if sudut_known == "Sudut Alpha (depan A)":
                sudut_alpha_deg = st.sidebar.slider("Besar Sudut Alpha (derajat):", min_value=1.0, max_value=89.0, value=36.87, step=0.1)
            elif sudut_known == "Sudut Beta (depan B)":
                sudut_beta_deg = st.sidebar.slider("Besar Sudut Beta (derajat):", min_value=1.0, max_value=89.0, value=53.13, step=0.1)

            calculation_results = calculate_triangle(
                sisi_a=sisi_a, sisi_b=sisi_b, sisi_c=sisi_c,
                sudut_alpha_deg=sudut_alpha_deg, sudut_beta_deg=sudut_beta_deg
            )
        except ValueError:
            st.sidebar.error("Input tidak valid. Harap masukkan angka.")


    if isinstance(calculation_results, str):
        st.error(calculation_results)
    elif calculation_results:
        st.subheader("Hasil Perhitungan:")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Sisi a:** `{calculation_results.get('sisi_a', 0.0):.2f}`")
            st.write(f"**Sisi b:** `{calculation_results.get('sisi_b', 0.0):.2f}`")
            st.write(f"**Sisi c (Hipotenusa):** `{calculation_results.get('sisi_c', 0.0):.2f}`")
        with col2:
            st.write(f"**Sudut Alpha (depan a):** `{calculation_results.get('sudut_alpha_deg', 0.0):.2f}°`")
            st.write(f"**Sudut Beta (depan b):** `{calculation_results.get('sudut_beta_deg', 0.0):.2f}°`")

        st.subheader("Visualisasi Segitiga:")
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if all(key in calculation_results for key in ['sisi_a', 'sisi_b', 'sisi_c']):
            a = calculation_results['sisi_a']
            b = calculation_results['sisi_b']
            c = calculation_results['sisi_c']
            alpha = calculation_results['sudut_alpha_deg']
            beta = calculation_results['sudut_beta_deg']

            # Scaling factor for better visualization
            max_dim = max(a, b)
            scale = 150 / max_dim # Max 150 units for longer side

            ax.plot([0, b * scale], [0, 0], 'k-', linewidth=2) # Sisi b
            ax.plot([b * scale, b * scale], [0, a * scale], 'k-', linewidth=2) # Sisi a
            ax.plot([0, b * scale], [0, a * scale], 'k-', linewidth=2) # Sisi c (Hipotenusa)

            # Labels for sides
            ax.text(b * scale / 2, -0.1 * scale, f'b={b:.2f}', ha='center', va='top')
            ax.text(b * scale + 0.1 * scale, a * scale / 2, f'a={a:.2f}', ha='left', va='center')
            ax.text(b * scale / 2 - 0.1 * scale, a * scale / 2 + 0.1 * scale, f'c={c:.2f}', ha='center', va='bottom', rotation=math.degrees(math.atan2(a, b)))

            # Right angle mark
            ax.plot([0, 0.1 * scale, 0.1 * scale, 0], [0.1 * scale, 0.1 * scale, 0, 0], 'k-')

            # Angle labels
            ax.text(0.15 * scale, 0.15 * scale, f'{alpha:.1f}°', ha='center', va='center') # Alpha (at origin)
            ax.text(b * scale - 0.15 * scale, a * scale - 0.15 * scale, f'{beta:.1f}°', ha='center', va='center') # Beta (at top-right)

            ax.set_aspect('equal', adjustable='box')
            ax.set_xlim(-0.2 * scale, (b + 0.2) * scale)
            ax.set_ylim(-0.2 * scale, (a + 0.2) * scale)
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.warning("Tidak cukup data untuk menggambar segitiga atau data tidak valid.")

    else:
        st.info("Silakan masukkan nilai pada sidebar untuk memulai perhitungan dan visualisasi.")

---

## Bagian 2: Visualisasi Fungsi Trigonometri

def fungsi_trigonometri_section():
    st.header("📈 Visualisasi Fungsi Trigonometri")
    st.write("Eksplorasi grafik fungsi sinus, kosinus, dan tangen.")

    func_choice = st.selectbox(
        "Pilih fungsi yang ingin divisualisasikan:",
        ("Sin(x)", "Cos(x)", "Tan(x)")
    )

    x_range_min = st.slider("Rentang X Minimum (radian):", min_value=-4 * np.pi, max_value=0.0, value=-2 * np.pi, step=0.1 * np.pi)
    x_range_max = st.slider("Rentang X Maksimum (radian):", min_value=0.0, max_value=4 * np.pi, value=2 * np.pi, step=0.1 * np.pi)

    if x_range_min >= x_range_max:
        st.error("Rentang X minimum harus lebih kecil dari maksimum.")
        return

    x = np.linspace(x_range_min, x_range_max, 500)
    y = []
    title = ""

    if func_choice == "Sin(x)":
        y = np.sin(x)
        title = "Grafik Fungsi Sin(x)"
    elif func_choice == "Cos(x)":
        y = np.cos(x)
        title = "Grafik Fungsi Cos(x)"
    elif func_choice == "Tan(x)":
        y = np.tan(x)
        title = "Grafik Fungsi Tan(x)"
        # Handle asymptotes for tan(x) to avoid drawing vertical lines where they shouldn't be
        y = np.where(np.abs(y) > 10, np.nan, y) # Set large values to NaN for plotting discontinuity

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, label=func_choice, color='blue')
    
    ax.set_title(title)
    ax.set_xlabel("X (radian)")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.8) # Sumbu X
    ax.axvline(0, color='black', linewidth=0.8) # Sumbu Y
    ax.legend()

    # Set x-ticks to multiples of pi
    pi_ticks = np.arange(int(x_range_min / np.pi) * np.pi, int(x_range_max / np.pi) * np.pi + np.pi, np.pi / 2)
    ax.set_xticks(pi_ticks)
    ax.set_xticklabels([f'{tick/np.pi:.0f}<span class="math-inline">\\pi</span>' if tick != 0 else '0' for tick in pi_ticks])
    
    st.pyplot(fig)

---

## Bagian 3: Soal Latihan & Kuis Interaktif

def soal_latihan_section():
    st.header("🧠 Soal Latihan & Kuis Interaktif")
    st.write("Uji pemahaman Anda dengan menjawab pertanyaan-pertanyaan trigonometri.")

    questions = [
        {"type": "segitiga_siku",
         "prompt": "Sebuah segitiga siku-siku memiliki sisi tegak (depan sudut alpha) 3 dan sisi alas (samping sudut alpha) 4. Berapakah panjang hipotenusanya?",
         "answer": "5",
         "hint": "Gunakan teorema Pythagoras: <span class="math-inline">a^2 \+ b^2 \= c^2</span>"},
        {"type": "segitiga_siku",
         "prompt": "Sebuah tangga sepanjang 10 meter disandarkan pada dinding. Jika sudut yang dibentuk tangga dengan tanah adalah 60 derajat, berapakah tinggi dinding yang dicapai tangga? (Tulis dalam 2 angka desimal)",
         "answer": f"{10 * math.sin(math.radians(60)):.2f}", # 8.66
         "hint": "Gunakan fungsi sinus. Tinggi = hipotenusa * sin(sudut)."},
        {"type": "nilai_trigonometri",
         "prompt": "Berapakah nilai dari <span class="math-inline">sin\(30^\\circ\)</span>? (Tulis dalam desimal 2 angka di belakang koma)",
         "answer": "0.50",
         "hint": "Ingat nilai-nilai istimewa trigonometri. sin(30) = 1/2."},
        {"type": "nilai_trigonometri",
         "prompt": "Jika <span class="math-inline">cos\(x\) \= 0\.8</span> dan <span class="math-inline">x</span> adalah sudut lancip, berapakah nilai <span class="math-inline">sin\(x\)</span>? (Tulis dalam desimal 2 angka di belakang koma)",
         "answer": f"{math.sqrt(1 - 0.8**2):.2f}", # 0.60
         "hint": "Gunakan identitas <span class="math-inline">sin^2\(x\) \+ cos^2\(x\) \= 1</span>."},
    ]

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.show_hint = False
        st.session_state.answer_submitted = False

    if st.session_state.current_question < len(questions):
        q = questions[st.session_state.current_question]
        st.subheader(f"Soal {st.session_state.current_question + 1} dari {len(questions)}")
        st.markdown(q["prompt"])

        user_answer = st.text_input("Jawaban Anda:", key=f"q_{st.session_state.current_question}")

        col_quiz1, col_quiz2 = st.columns(2)
        with col_quiz1:
            if st.button("Submit Jawaban", key=f"submit_q_{st.session_state.current_question}"):
                st.session_state.answer_submitted = True
                correct = False
                try:
                    if q["type"] in ["segitiga_siku", "nilai_trigonometri"]:
                        user_ans_float = float(user_answer)
                        correct_ans_float = float(q["answer"])
                        if abs(user_ans_float - correct_ans_float) < 0.01:
                            correct = True
                    else: # For exact string answers if any
                        if user_answer.strip().lower() == q["answer"].lower():
                            correct = True
                except ValueError:
                    st.warning("Input tidak valid. Harap masukkan angka.")

                if correct:
                    st.success("🎉 Benar sekali!")
                    st.session_state.score += 1
                else:
                    st.error("❌ Jawaban salah.")
                
        with col_quiz2:
            if st.button("Tampilkan Petunjuk", key=f"hint_q_{st.session_state.current_question}"):
                st.session_state.show_hint = True

        if st.session_state.show_hint:
            st.info(f"Petunjuk: {q['hint']}")
            st.session_state.show_hint = False # Reset hint after showing

        if st.session_state.answer_submitted:
            if st.button("Soal Selanjutnya", key=f"next_q_{st.session_state.current_question}"):
                st.session_state.current_question += 1
                st.session_state.answer_submitted = False
                st.experimental_rerun()