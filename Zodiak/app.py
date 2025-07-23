import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# KONFIGURASI API KEY & MODEL
# ==============================================================================

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key Gemini tidak ditemukan. Harap atur 'GOOGLE_API_KEY' di Streamlit Secrets atau Environment Variable Anda.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Kesalahan saat mengkonfigurasi API Key: {e}. Pastikan API Key valid.")
    st.stop()

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

NAMA_BOT = 'Peramal Zodiak Harian' # Ganti nama bot di sini!

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
st.write("Dapatkan ramalan zodiak harianmu di sini!") # Pesan deskriptif di bawah judul

# Inisialisasi riwayat chat di Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # HANYA tambahkan balasan pertama dari MODEL sebagai pesan pembuka di chat UI
    # Bagian instruksi "user" (role: user) dari INITIAL_CHATBOT_CONTEXT tidak ditampilkan
    st.session_state.messages.append({"role": "assistant", "content": INITIAL_CHATBOT_CONTEXT[1]["parts"][0]})

# Tampilkan riwayat chat ke antarmuka Streamlit
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"]) # Menggunakan "content" untuk input user
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"]) # Menggunakan "content" untuk output assistant

# Input pengguna
user_input_placeholder = INITIAL_CHATBOT_CONTEXT[1]["parts"][0]
user_input = st.chat_input(user_input_placeholder)

if user_input:
    # Tambahkan pesan pengguna ke riwayat dan tampilkan
    # Ubah format menjadi "content" untuk konsistensi di st.session_state.messages
    st.session_state.messages.append({"role": "user", "content": user_input.lower()})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Kirim pesan ke Gemini dan dapatkan respons
    try:
        # Bangun riwayat chat LENGKAP untuk dikirim ke Gemini:
        # 1. Mulai dengan instruksi sistem (INITIAL_CHATBOT_CONTEXT[0])
        # 2. Tambahkan balasan awal model (INITIAL_CHATBOT_CONTEXT[1])
        # 3. Tambahkan semua interaksi selanjutnya dari st.session_state.messages
        
        # Perhatikan: Kita perlu mengubah format "content" menjadi "parts" saat mengirim ke Gemini
        full_chat_history_for_gemini = [
            INITIAL_CHATBOT_CONTEXT[0], # Instruksi sistem untuk model
            INITIAL_CHATBOT_CONTEXT[1]  # Balasan awal dari model
        ]
        
        # Tambahkan semua pesan dari st.session_state.messages (mulai dari pesan kedua, yaitu user input pertama)
        # Kita perlu memformat ulang dari {"role": "user", "content": "..."} menjadi {"role": "user", "parts": ["..."]}
        for msg in st.session_state.messages[1:]: # Mulai dari indeks 1 karena indeks 0 adalah balasan awal bot
            if msg["role"] == "user":
                full_chat_history_for_gemini.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                full_chat_history_for_gemini.append({"role": "model", "parts": [msg["content"]]}) # Role model di API

        chat_session = model.start_chat(history=full_chat_history_for_gemini)
        response = chat_session.send_message(user_input.lower(), request_options={"timeout": 60})

        if response and response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            # Simpan respons ke session_state dengan format "content"
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            with st.chat_message("assistant"):
                st.markdown("Maaf, saya tidak bisa memberikan balasan. Respons API kosong atau tidak valid.")

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {e}")
            st.markdown("Kemungkinan penyebab: Masalah koneksi, API Key tidak valid/kuota habis, atau masalah internal server.")
