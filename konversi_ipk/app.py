import streamlit as st

def tentukan_nilai(nilai):
    """Fungsi untuk menentukan dan mengembalikan predikat nilai."""
    
    # Cek nilai tidak valid (di luar rentang 0-100)
    if nilai > 100 or nilai < 0:
        return "Nilai Anda **tidak valid** (di luar rentang 0-100)"
    # Cek Nilai A (85-100)
    elif nilai >= 85: 
        return "Nilai Anda **A**"
    # Cek Nilai B (70-84.99...)
    elif nilai >= 70:
        return "Nilai Anda **B**"
    # Cek Nilai C (55-69.99...)
    elif nilai >= 55:
        return "Nilai Anda **C**"
    # Cek Nilai D (40-54.99...)
    elif nilai >= 40:
        return "Nilai Anda **D**"
    # Sisanya adalah Nilai E (0-39.99...)
    else:
        return "Nilai Anda **E**"

# Judul Aplikasi
st.title("Aplikasi Penentuan Predikat Nilai")

# Input Pengguna menggunakan Textbox
nilai_str = st.text_input("Masukkan nilai Anda (contoh: 85.5):", value="50.0")

# Tombol untuk menjalankan fungsi
if st.button("Tentukan Predikat"):
    try:
        # Konversi input string (dari textbox) ke float
        nilai_input = float(nilai_str)
        
        # Panggil fungsi penentuan nilai
        hasil = tentukan_nilai(nilai_input)
        
        # Tampilkan hasil
        st.markdown(f"**Hasil:** {hasil}")
        
    except ValueError:
        # Tangani jika input bukan angka
        st.error("Input yang Anda masukkan **bukan angka**; Mohon masukkan nilai numerik yang valid;")
