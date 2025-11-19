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

# Input Pengguna menggunakan slider Streamlit untuk nilai float
# Batasi rentang input dari -10 hingga 110 (untuk menguji validasi)
nilai_input = st.slider(
    "Masukkan nilai Anda:", 
    min_value=-10.0, 
    max_value=110.0, 
    value=50.0, # Nilai default
    step=0.1, 
    format="%.1f"
)

# Tombol untuk menjalankan fungsi
if st.button("Tentukan Predikat"):
    hasil = tentukan_nilai(nilai_input)
    st.markdown(f"**Hasil:** {hasil}")

# Anda juga bisa menampilkan hasil secara dinamis tanpa tombol
# hasil = tentukan_nilai(nilai_input)
# st.markdown(f"**Hasil (Otomatis):** {hasil}")