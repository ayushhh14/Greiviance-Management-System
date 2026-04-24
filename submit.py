import streamlit as st
import speech_recognition as sr
import tempfile
from model.predictor import predict
from database.db import insert_complaint

def submit_page():
    st.header("📩 Submit Complaint")

    name = st.text_input("Name")
    email = st.text_input("Email")
    account = st.text_input("Account Number")

    # -------------------------
    # STATE FOR AUDIO TEXT
    # -------------------------
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""

    complaint = st.text_area("Complaint", value=st.session_state.voice_text)

    # -------------------------
    # 🎤 AUDIO INPUT (NEW)
    # -------------------------
    st.subheader("🎤 Record Complaint")

    audio_data = st.audio_input("Click to record and stop when finished")

    if audio_data is not None and st.button("Convert Audio to Text"):
        recognizer = sr.Recognizer()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_data.getbuffer())
            audio_path = tmp.name

        try:
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)

            st.success("Converted to text")
            st.session_state.voice_text = text
            st.rerun()

        except sr.UnknownValueError:
            st.error("Could not understand audio")

        except sr.RequestError:
            st.error("Speech service unavailable")

    # -------------------------
    # ORIGINAL SUBMIT (UNCHANGED)
    # -------------------------
    if st.button("Submit"):
        if complaint.strip() == "":
            st.error("Enter complaint")
        else:
            result = predict(complaint)

            if len(result) == 3:
                dept, priority, confidence = result
            else:
                dept, priority = result
                confidence = 1.0

            insert_complaint(name, email, account, complaint, dept, priority)

            st.success("Submitted")
            st.write("Department:", dept)
