import streamlit as st

# -------------------------
# SESSION STATE INIT
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = "User"

if "department" not in st.session_state:
    st.session_state.department = ""

# -------------------------
# USERS DATA (FULL DEPARTMENTS)
# -------------------------
users = {
    "User": {
        "user": "user123"
    },
    "Admin": {
        "admin": "admin123"
    },
    "Department": {
        "Loan Department": "loan123",
        "Credit Card Department": "credit123",
        "Customer Service": "customer123",
        "Fraud & Security": "fraud123",
        "Technical Issues": "tech123",
        "Account Management": "account123"
    }
}

# -------------------------
# UI STYLE
# -------------------------
st.markdown("""
<style>
body {
    background-color: #1f2428;
}
.title {
    text-align: center;
    font-size: 42px;
    color: white;
    margin-top: 40px;
    margin-bottom: 30px;
}
.stButton>button {
    background-color: #4a4f55;
    color: white;
    border-radius: 10px;
    height: 100px;
    font-size: 18px;
}
.stButton>button:hover {
    background-color: #5c6269;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOGIN PAGE
# -------------------------
if not st.session_state.logged_in:

    st.markdown('<div class="title">Get Started with Us</div>', unsafe_allow_html=True)

    st.markdown("### Select Role")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("User", use_container_width=True):
            st.session_state.role = "User"

    with col2:
        if st.button("Admin", use_container_width=True):
            st.session_state.role = "Admin"

    with col3:
        if st.button("Department", use_container_width=True):
            st.session_state.role = "Department"

    st.markdown("---")

    role = st.session_state.role

    st.markdown(f"### Selected Role: {role}")

    # -------------------------
    # DYNAMIC LOGIN FIELDS
    # -------------------------
    usernames = list(users[role].keys())

    username = st.selectbox("Username", usernames)

    password = st.selectbox(
        "Password",
        [users[role][username]]
    )

    # -------------------------
    # LOGIN BUTTON
    # -------------------------
    if st.button("Login"):
        if username in users[role] and password == users[role][username]:
            st.session_state.logged_in = True
            st.session_state.role = role

            # 🔥 IMPORTANT FIX
            if role == "Department":
                st.session_state.department = username

            st.success(f"Logged in as {role}")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# -------------------------
# AFTER LOGIN
# -------------------------
st.sidebar.write(f"👤 {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.department = ""
    st.rerun()

# -------------------------
# IMPORT PAGES
# -------------------------
from pages.submit import submit_page
from pages.dashboard import dashboard_page
from pages.history import history_page

# -------------------------
# ROLE-BASED ROUTING
# -------------------------
if st.session_state.role == "User":
    submit_page()

elif st.session_state.role == "Admin":
    menu = st.sidebar.selectbox("Menu", ["Dashboard", "History"])

    if menu == "Dashboard":
        dashboard_page()
    else:
        history_page()

elif st.session_state.role == "Department":
    dashboard_page()
