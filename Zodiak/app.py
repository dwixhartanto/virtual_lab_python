import streamlit as st
import google.generativeai as genai
import os

# ... (bagian kode konfigurasi API KEY, MODEL, dan KONTEKS AWAL CHATBOT tetap sama) ...

# ==============================================================================
# ANTEMUKA STREAMLIT
# ==============================================================================

st.title(f"🔮 {NAMA_BOT} 🔮")
st.write("Dapatkan ramalan zodiak harianmu di sini!") # Pesan deskriptif di bawah judul

# Inisialisasi riwayat chat di Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # HANYA tambahkan balasan pertama dari MODEL sebagai pesan pembuka di chat UI
    st.session_state.messages.append({"role": "assistant", "content": INITIAL_CHATBOT_CONTEXT[1]["parts"][0]})

# Tampilkan riwayat chat ke antarmuka Streamlit
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Input pengguna
# --- PERUBAHAN DI SINI ---
user_input_placeholder = "Silakan masukkan tgl lahir (DD/MM) atau zodiak Anda" # <--- Pesan placeholder yang lebih ringkas
user_input = st.chat_input(user_input_placeholder)
# --- AKHIR PERUBAHAN ---

if user_input:
    # ... (lanjutan kode lainnya tetap sama) ...
