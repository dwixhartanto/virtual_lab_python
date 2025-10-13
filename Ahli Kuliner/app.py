import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# KONFIGURASI APLIKASI STREAMLIT
# ==============================================================================

# Atur Judul Halaman dan Ikon
st.set_page_config(page_title="Ahli Kuliner Gemini", page_icon="🍔")

# ==============================================================================
# PENGATURAN API KEY DAN MODEL
# ==============================================================================

# Dapatkan API Key dari Streamlit Secrets (Disimpan aman, tidak di dalam kode)
# Pastikan Anda sudah membuat file .streamlit/secrets.toml
# dengan kunci "GEMINI_API_KEY"
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("🚨 **Error Konfigurasi:** Kunci `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets.")
    st.info("Mohon tambahkan API Key Anda ke `secrets.toml` atau Environment Variables.")
    st.stop() # Hentikan eksekusi aplikasi jika API Key tidak ada

# Nama model Gemini yang akan digunakan.
MODEL_NAME = 'gemini-2.5-flash-lite' # Direkomendasikan untuk Streamlit
TEMPERATURE = 0.4
MAX_TOKENS = 500

# ==============================================================================
# KONTEKS AWAL CHATBOT (Sama dengan kode Anda)
# ==============================================================================

INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah ahli kuliner. Beri 3 rekomendasi makanan dan minuman di lokasi yang diminta . Jawaban singkat dan faktual. Tolak pertanyaan diluar kuliner."]
    },
    {
        "role": "model",
        "parts": ["Baik! Berikan lokasi untuk saya berikan rekomendasinya."]
    }
]

# ==============================================================================
# INISIALISASI GEMINI API DAN CHAT
# ==============================================================================

# Fungsi untuk inisialisasi API dan Model
@st.cache_resource # Cache sumber daya untuk menghindari inisialisasi berulang
def init_gemini_chat():
    try:
        # Konfigurasi API
        genai.configure(api_key=API_KEY)

        # Inisialisasi model
        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config=genai.types.GenerationConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_TOKENS
            )
        )

        # Memulai sesi chat dengan riwayat awal (konteks)
        chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)
        return chat
    except Exception as e:
        st.error(f"❌ **Gagal Menginisialisasi Gemini!** Detail: {e}")
        st.stop()
        
# Inisialisasi chat dan simpan di session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = init_gemini_chat()

# Inisialisasi riwayat pesan di Streamlit session state
if "messages" not in st.session_state:
    # Ambil pesan awal dari INITIAL_CHATBOT_CONTEXT untuk ditampilkan
    st.session_state.messages = [
        {"role": "assistant", "content": INITIAL_CHATBOT_CONTEXT[1]["parts"][0]}
    ]
    
# ==============================================================================
# ANTARMUKA PENGGUNA STREAMLIT
# ==============================================================================

st.title("🍔 Ahli Kuliner Gemini")
st.caption("Chatbot yang akan memberikan 3 rekomendasi makanan dan minuman terbaik di lokasi yang Anda minta.")

# Tampilkan semua riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom input untuk pengguna
if prompt := st.chat_input("Tanyakan rekomendasi kuliner (misal: Jakarta Pusat)..."):
    # Tambahkan input pengguna ke riwayat pesan dan tampilkan
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Dapatkan balasan dari Gemini
    with st.chat_message("assistant"):
        with st.spinner("Ahli Kuliner sedang mencari rekomendasi..."):
            try:
                # Kirim input pengguna ke model
                response = st.session_state.chat_session.send_message(
                    prompt, 
                    request_options={"timeout": 60}
                )

                if response and response.text:
                    st.markdown(response.text)
                    # Tambahkan balasan model ke riwayat pesan
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    error_msg = "Maaf, saya tidak bisa memberikan balasan. Respons API kosong atau tidak valid."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except Exception as e:
                error_msg = f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {e}"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})