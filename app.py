import streamlit as st
from auth.login import login
from pages.submit import submit_page
from pages.dashboard import dashboard_page
from pages.history import history_page

st.set_page_config(page_title="Bank Grievance System", layout="wide")

# Login
login()

# Header
st.title("🏦 AI Bank Grievance System")
st.write(f"👤 {st.session_state.user} ({st.session_state.role})")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# Role-based routing
if st.session_state.role == "User":
    submit_page()
elif st.session_state.role == "Department":
    dashboard_page()
else:
    history_page()