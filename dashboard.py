import streamlit as st
import plotly.express as px
from database.db import get_by_department, update_status
from utils.helpers import create_dataframe

def dashboard_page():
    st.header("🏢 Dashboard")

    if st.session_state.role == "Department":
        dept = st.session_state.department
        st.subheader(f"{dept}")
    else:
        dept = st.selectbox("Department", [
            "Loan Department", "Credit Card Department", "Customer Service",
            "Fraud & Security", "Technical Issues", "Account Management"
        ])

    data = get_by_department(dept)
    df = create_dataframe(data)

    if df.empty:
        st.warning("No complaints")
        return

    # -------------------------
    # Charts
    # -------------------------

    # 🔥 FIX: Ensure all statuses appear (even 0 count)
    all_status = ["Pending", "In Progress", "Resolved"]

    status_counts = (
        df["Status"]
        .value_counts()
        .reindex(all_status, fill_value=0)
        .reset_index()
    )

    status_counts.columns = ["Status", "Count"]

    # Optional message
    if df["Status"].nunique() == 1:
        st.info("All complaints currently fall under one status")

    fig = px.bar(status_counts, x="Status", y="Count", color="Status", text="Count")
    st.plotly_chart(fig)

    # -------------------------
    # Priority Pie (UNCHANGED)
    # -------------------------
    priority_counts = df["Priority"].value_counts().reset_index()
    priority_counts.columns = ["Priority", "Count"]

    fig2 = px.pie(priority_counts, names="Priority", values="Count")
    st.plotly_chart(fig2)

    # -------------------------
    # List (UNCHANGED)
    # -------------------------
    for _, row in df.iterrows():
        st.subheader(f"ID: {row['ID']}")
        st.write(row["Complaint"])

        new_status = st.selectbox(
            f"Update {row['ID']}",
            ["Pending","In Progress","Resolved"],
            key=f"s_{row['ID']}"
        )

        if st.button(f"Update {row['ID']}", key=f"b_{row['ID']}"):
            update_status(row["ID"], new_status)
            st.success("Updated")