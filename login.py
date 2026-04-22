import streamlit as st

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.user = ""
        st.session_state.department = None

    credentials = {
        "User": [("user", "user123")],
        "Admin": [("admin", "admin123")],
        "Department": [
            ("loan", "loan123"),
            ("credit", "credit123"),
            ("customer_service", "cs123"),
            ("fraud", "fraud123"),
            ("technical", "tech123"),
            ("account", "acc123")
        ]
    }

    department_map = {
        "loan": "Loan Department",
        "credit": "Credit Card Department",
        "customer_service": "Customer Service",
        "fraud": "Fraud & Security",
        "technical": "Technical Issues",
        "account": "Account Management"
    }

    if not st.session_state.logged_in:
        st.title("🔐 Login")

        role = st.selectbox("Select Role", list(credentials.keys()))
        usernames = [u for u, p in credentials[role]]
        selected_user = st.selectbox("Username", usernames)
        passwords = [p for u, p in credentials[role] if u == selected_user]
        selected_pass = st.selectbox("Password", passwords)

        if st.button("Login"):
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.user = selected_user

            if role == "Department":
                st.session_state.department = department_map[selected_user]
            else:
                st.session_state.department = None

            st.rerun()

        st.stop()