import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

import streamlit as st
from nltk.corpus import wordnet
from googletrans import Translator
from gtts import gTTS
import os
import uuid

translator = Translator()

def get_meaning(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    return None   # <-- return None if not found

def translate_text(text, lang):
    return translator.translate(text, dest=lang).text

def speak_text(text, lang='en'):
    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    if os.name == "nt":   # Windows
        os.system(f"start {filename}")
    else:                 # Mac / Linux
        os.system(f"open {filename}")

st.set_page_config(page_title="Speaking  Dictionary")

st.title("Speaking  Dictionary")
st.write("Type a word to Hear pronunciation and Get meanings in multiple languages")

word = st.text_input("Enter a word")

# ---- ONLY RUN IF WORD IS ENTERED ----
if word: 

    meaning_en = get_meaning(word)

    # ---- ONLY RUN IF MEANING EXISTS ----
    if meaning_en:

        st.subheader("📘 English Meaning")
        st.write(meaning_en)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔊 Speak Word"):
                speak_text(word, 'en')

        with col2:
            if st.button("🔊 Speak Meaning"):
                speak_text(meaning_en, 'en')

        st.subheader("Meanings in Other Languages")

        # translate ONLY after meaning exists
        meaning_hi = translate_text(meaning_en, "hi")
        meaning_ta = translate_text(meaning_en, "ta")
        meaning_ml = translate_text(meaning_en, "ml")

        st.write("🟢 **Hindi:**", meaning_hi)
        st.write("🟠 **Tamil:**", meaning_ta)
        st.write("🔵 **Malayalam:**", meaning_ml)

    else:
        st.error("❌ Meaning not found. Try another English word.")

else:
    st.info("➡️ Please enter a word above.")
