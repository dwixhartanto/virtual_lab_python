import google.generativeai as genai
import os
import streamlit as st

# ==============================================================================
# PENGATURAN API KEY DAN MODEL
# ==============================================================================

# Mengambil API Key dari Streamlit Secrets atau variabel lingkungan.
# Penting: Di Streamlit, tambahkan GEMINI_API_KEY ke bagian "Secrets" aplikasi Anda.
# Contoh:
# GEMINI_API_KEY="AIzaSyDFRFkPGyghxdRJ0Iv1utEBO4UY-7Il6Ow" (GANTI DENGAN API KEY ANDA!)
API_KEY = os.getenv("GEMINI_API_KEY")

# Nama model Gemini yang akan digunakan.
MODEL_NAME = 'gemini-1.5-flash'

# ==============================================================================
# KONTEKS AWAL CHATBOT
# ==============================================================================

# Definisikan peran chatbot Anda di sini.
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah asisten diagnosis penyakit yang fokus pada gejala umum dan menyarankan obat generik yang relevan. Berikan saran singkat, jelas, dan hanya seputar diagnosis serta obat generik. Tolak pertanyaan yang tidak berkaitan dengan kesehatan atau obat-obatan."]
    },
    {
        "role": "model",
        "parts": ["Halo! Beri tahu saya gejala yang Anda rasakan, dan saya akan coba bantu dengan informasi diagnosis awal serta pilihan obat generik yang mungkin cocok."]
    }
]

# ==============================================================================
# FUNGSI UTAMA CHATBOT UNTUK STREAMLIT
# ==============================================================================

def main():
    st.set_page_config(page_title="Chatbot Diagnosa Penyakit & Obat Generik", page_icon="💊")
    st.title("💊 Chatbot Diagnosa Penyakit & Obat Generik")
    st.markdown("---")

    # Inisialisasi API Key
    if not API_KEY:
        st.error("API Key Gemini belum diatur. Harap tambahkan `GEMINI_API_KEY` ke Streamlit Secrets Anda.")
        st.stop() # Hentikan eksekusi jika API Key tidak ada

    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        st.error(f"Kesalahan saat mengkonfigurasi API Key: {e}")
        st.error("Pastikan API Key Anda benar dan koneksi internet stabil.")
        st.stop()

    # Inisialisasi model
    try:
        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=500
            )
        )
    except Exception as e:
        st.error(f"Kesalahan saat inisialisasi model '{MODEL_NAME}': {e}")
        st.error("Pastikan nama model benar dan tersedia untuk API Key Anda.")
        st.stop()

    # Inisialisasi riwayat chat di session_state jika belum ada
    if "messages" not in st.session_state:
        st.session_state.messages = INITIAL_CHATBOT_CONTEXT[:] # Salin konteks awal

    # Inisialisasi sesi chat Gemini jika belum ada atau jika model berubah
    if "chat_session" not in st.session_state or st.session_state.get("model_name") != MODEL_NAME:
        st.session_state.chat_session = model.start_chat(history=st.session_state.messages)
        st.session_state.model_name = MODEL_NAME
        # Hapus pesan pembuka awal dari riwayat tampilan agar tidak duplikat
        if len(st.session_state.messages) == 2 and st.session_state.messages[1]["role"] == "model":
            st.session_state.messages = [st.session_state.messages[0]]
            st.session_state.messages.append({"role": "model", "parts": [INITIAL_CHATBOT_CONTEXT[1]["parts"][0]]})


    # Tampilkan riwayat chat
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["parts"][0])
        elif message["role"] == "model":
            with st.chat_message("assistant"):
                st.markdown(message["parts"][0])

    # Input pengguna
    user_input = st.chat_input("Ketik gejala atau pertanyaan Anda di sini...")

    if user_input:
        # Tambahkan input pengguna ke riwayat dan tampilkan
        st.session_state.messages.append({"role": "user", "parts": [user_input]})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Kirim pesan ke model dan dapatkan balasan
        with st.spinner("Chatbot sedang berpikir..."):
            try:
                # Menggunakan chat_session yang sudah ada
                response = st.session_state.chat_session.send_message(user_input, request_options={"timeout": 60})

                if response and response.text:
                    chatbot_response = response.text
                else:
                    chatbot_response = "Maaf, saya tidak bisa memberikan balasan."

                # Tambahkan balasan chatbot ke riwayat dan tampilkan
                st.session_state.messages.append({"role": "model", "parts": [chatbot_response]})
                with st.chat_message("assistant"):
                    st.markdown(chatbot_response)

            except Exception as e:
                error_message = f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {e}"
                error_message += "\n\nKemungkinan penyebab:"
                error_message += "\n - Masalah koneksi internet atau timeout."
                error_message += "\n - API Key mungkin dibatasi, tidak valid, atau melebihi kuota."
                error_message += "\n - Masalah internal di server Gemini."
                st.error(error_message)
                # Opsional: Hapus input pengguna terakhir dari riwayat jika gagal mendapatkan balasan
                if st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()

if __name__ == "__main__":
    main()