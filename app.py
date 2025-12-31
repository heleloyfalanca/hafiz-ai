import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import io

# API Ayarı
GOOGLE_API_KEY = "AIzaSyBjbNXNUx7p_x0ZStNEXM-QVkni0P3FbVQ"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Hafız AI", page_icon="📖", layout="centered")

# PROFESYONEL TASARIM (CSS) - Düzeni Korumak İçin Sabitlendi
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0a2e12 0%, #000000 100%); color: white; }
    .main-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 20px; padding: 25px; backdrop-filter: blur(10px); margin-top: 10px; }
    h1 { color: #FFD700 !important; text-align: center; font-family: 'Georgia', serif; margin-bottom: 0px; }
    .arabic-text { font-size: 30px !important; direction: rtl; text-align: right; background: rgba(0, 0, 0, 0.4); padding: 20px; border-radius: 10px; border-right: 5px solid #FFD700; line-height: 1.8; margin: 15px 0; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(255,215,0,0.1); border-radius: 10px 10px 0 0; color: white; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #FFD700 !important; color: #0a2e12 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>📖 HAFIZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFD700; opacity: 0.8;'>Tilavet Analiz ve Tanıma Sistemi</p>", unsafe_allow_html=True)

# SEKMELİ YAPI (Anlık ve Arşiv Seçimi)
tab1, tab2 = st.tabs(["🎤 Anlık Ses Kaydı", "📁 Arşivden Dosya Seç"])

audio_to_process = None

with tab1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    audio_data = mic_recorder(start_prompt="🎤 Kayda Başla", stop_prompt="🛑 Bitir", key='recorder')
    if audio_data:
        audio_to_process = {"data": audio_data['bytes'], "type": "audio/wav"}
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Cihazınızdaki ses dosyasını seçin (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])
    if uploaded_file:
        audio_to_process = {"data": uploaded_file.read(), "type": uploaded_file.type}
    st.markdown("</div>", unsafe_allow_html=True)

# ANALİZ MOTORU (Aynı Düzenle Çalışır)
if audio_to_process:
    with st.spinner("🌙 Tilavet Analiz Ediliyor..."):
        try:
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            prompt = """
            Bu bir Kuran tilavetidir. Lütfen:
            1. Sayfa Sayısı Sure ve Ayet No'yu <h3> içine yaz.
            2. Arapça metni <div class='arabic-text'> içine yaz.
            3. Meali <div style='color: #e0e0e0; border-left: 3px solid #FFD700; padding-left: 15px;'><b>Meal:</b> ...</div> içine yaz.
            4. Varsa benzer ayetleri (Müteşabih) belirt (yani lafız bakımından benzer olan) ve onun da Sayfa Sayısı Sure ve Ayet No'yu büyük punto ile (ilk ayeti belirttiğin gibi) belirt.
            """
            
            response = model.generate_content([
                prompt,
                {'mime_type': audio_to_process['type'], 'data': audio_to_process['data']}
            ])
            
            st.markdown("---")
            st.markdown(response.text, unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Analiz sırasında bir hata oluştu: {e}")

st.markdown("<br><p style='text-align: center; font-size: 0.7em; opacity: 0.5;'>Hafız AI v1.0 | Tilavet Analiz ve Tanıma Sistemi</p>", unsafe_allow_html=True)