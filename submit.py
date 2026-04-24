import streamlit as st
from model.predictor import predict
from database.db import insert_complaint

def submit_page():
    st.header("📩 Submit Complaint")

    name = st.text_input("Name")
    email = st.text_input("Email")
    account = st.text_input("Account Number")

    complaint = st.text_area("Complaint")

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
