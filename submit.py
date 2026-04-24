import speech_recognition as sr
import streamlit as st
from model.predictor import predict
from database.db import insert_complaint

def submit_page():
    st.header("📩 Submit Complaint")

    name = st.text_input("Name")
    email = st.text_input("Email")
    account = st.text_input("Account Number")

    # -------------------------
    # VOICE STATE (EXISTING)
    # -------------------------
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""

    complaint = st.text_area("Complaint", value=st.session_state.voice_text)

    # -------------------------
    # 🎤 ORIGINAL SPEAK BUTTON (UNCHANGED)
    # -------------------------
    if st.button("🎤 Speak Complaint"):
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                st.info("Listening... Speak now")
                audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)
            st.success("Voice captured")

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