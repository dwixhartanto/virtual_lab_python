import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# KONFIGURASI API KEY & MODEL
# ==============================================================================

# Ambil API Key dari Streamlit Secrets atau Environment Variable
# Ini adalah cara aman untuk menyimpan API Key di Streamlit Cloud
try:
    # Coba ambil dari Streamlit Secrets (direkomendasikan untuk deployment)
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    # Fallback ke Environment Variable jika tidak ditemukan di secrets (untuk testing lokal)
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key Gemini tidak ditemukan. Harap atur 'GOOGLE_API_KEY' di Streamlit Secrets atau Environment Variable Anda.")
    st.stop() # Hentikan eksekusi aplikasi jika API Key tidak ada

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Kesalahan saat mengkonfigurasi API Key: {e}. Pastikan API Key valid.")
    st.stop()

# Nama model Gemini yang akan digunakan
MODEL_NAME = 'gemini-1.5-flash' # Rekomendasi: 'gemini-1.5-flash' atau 'gemini-2.5-flash-lite'

try:
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4, # Kontrol kreativitas (0.0=faktual, 1.0=kreatif)
            max_output_tokens=500 # Batas maksimal panjang jawaban dalam token
        )
    )
except Exception as e:
    st.error(f"Kesalahan saat inisialisasi model '{MODEL_NAME}': {e}. Pastikan nama model benar.")
    st.stop()

# ==============================================================================
# KONTEKS AWAL CHATBOT (INI BISA KAMU MODIFIKASI!)
# ==============================================================================

# Definisikan nama bot Anda di sini.
NAMA_BOT = 'Peramal Zodiak Harian'

# Definisikan peran chatbot Anda di sini.
# Buatlah singkat, jelas, dan langsung pada intinya untuk menghemat token.
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": [
            "Kamu adalah peramal zodiak harian. Berikan ramalan untuk hari ini berdasarkan tanggal lahir atau zodiak. "
            "Fokus pada ramalan singkat dan positif. Jika tanggal/zodiak tidak valid, minta input ulang."
        ]
    },
    {
        "role": "model",
        "parts": [
            "Halo! Saya siap membacakan ramalan zodiak Anda untuk hari ini. "
            "Silakan berikan tanggal lahir Anda (DD/MM) atau sebutkan zodiak Anda!"
        ]
    }
]

# ==============================================================================
# ANTEMUKA STREAMLIT
# ==============================================================================

st.title(f"🔮 {NAMA_BOT} 🔮")
st.write("Dapatkan ramalan zodiak harianmu di sini!")

# Inisialisasi riwayat chat di Streamlit's session state
# Ini penting agar chatbot "mengingat" percakapan sebelumnya
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Tambahkan konteks awal ke riwayat chat saat pertama kali dimulai
    st.session_state.messages.extend(INITIAL_CHATBOT_CONTEXT)

# Tampilkan riwayat chat ke antarmuka Streamlit
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["parts"][0])
    elif message["role"] == "model":
        with st.chat_message("assistant"):
            st.markdown(message["parts"][0])

# Input pengguna
user_input = st.chat_input(INITIAL_CHATBOT_CONTEXT[1]["parts"][0]) # Gunakan pesan awal model sebagai placeholder input

if user_input:
    # Tambahkan pesan pengguna ke riwayat dan tampilkan
    st.session_state.messages.append({"role": "user", "parts": [user_input.lower()]})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Kirim pesan ke Gemini dan dapatkan respons
    try:
        # Kirim seluruh riwayat chat (termasuk konteks awal) ke model untuk menjaga konteks
        chat_session = model.start_chat(history=st.session_state.messages)
        response = chat_session.send_message(user_input.lower(), request_options={"timeout": 60})

        # Tampilkan respons dari Gemini
        if response and response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
        else:
            with st.chat_message("assistant"):
                st.markdown("Maaf, saya tidak bisa memberikan balasan. Respons API kosong atau tidak valid.")

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {e}")
            st.markdown("Kemungkinan penyebab: Masalah koneksi, API Key tidak valid/kuota habis, atau masalah internal server.")
