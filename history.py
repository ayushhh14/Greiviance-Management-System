import streamlit as st
import plotly.express as px
from database.db import get_all_complaints
from utils.helpers import create_dataframe

def history_page():
    st.header("📜 Complaint History (Admin)")

    data = get_all_complaints()
    df = create_dataframe(data)

    if df.empty:
        st.warning("No data")
        return

    # -------------------------
    # 📊 STATUS PIE CHART
    # -------------------------
    st.subheader("📊 Complaint Status Distribution")

    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig1 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.4,
        color="Status",
        color_discrete_map={
            "Pending": "#636EFA",
            "In Progress": "#FFA15A",
            "Resolved": "#00CC96"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -------------------------
    # 📊 DEPARTMENT BAR CHART
    # -------------------------
    st.subheader("🏢 Complaints per Department")

    dept_counts = df["Department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Count"]

    fig2 = px.bar(
        dept_counts,
        x="Department",
        y="Count",
        color="Department",
        text="Count",
        title="Department-wise Complaints"
    )

    fig2.update_layout(template="plotly_white")

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # -------------------------
    # 🔍 SEARCH
    # -------------------------
    search = st.text_input("Search Complaint")

    if search:
        df = df[df["Complaint"].str.contains(search, case=False)]

    st.dataframe(df)

    # -------------------------
    # ⬇ DOWNLOAD
    # -------------------------
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "complaints.csv"
    )