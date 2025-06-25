import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

   
LOG_FILE = "document_log.json"

def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def run_status_page():
   
    # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 1px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Document Processing Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    col_right1 , col_right2, col_right3 = st.columns([1, 1,1])

    with col_right1:
        if st.button("Go to Upload Page"):
            st.session_state.page = "upload"
            st.rerun()

    with col_right2:
        if st.button("Review Documents"):
            st.session_state.page = "review"  
            st.rerun()

    with col_right3:
        if st.button("Departments"):
            st.session_state.page = "departments"     
            st.rerun()


    log_data = load_log()

    if not log_data:
        st.info("No documents have been processed yet.")
        return

    # --- Layout: Bar and Pie Chart side by side ---
    col1, col2 = st.columns(2)

    with col1:
        
        status_counts = {}
        for doc in log_data:
          status = doc.get("status", "Unknown").split("→")[-1].strip()
          status_counts[status] = status_counts.get(status, 0) + 1

        status_df = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
        fig_bar = px.bar(status_df, x="Status", y="Count", color="Status", text="Count", title="Document Status Overview")
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        
        type_counts = {}
        for doc in log_data:
            doc_type = doc.get("type", "Unknown")
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1

        type_df = pd.DataFrame(list(type_counts.items()), columns=["Type", "Count"])
        fig_pie = px.pie(type_df, names="Type", values="Count", title="Document Type Distribution", hole=0.4)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Recently Processed Documents ---
    st.subheader("Recently Processed Documents")
    recent_docs = sorted(log_data, key=lambda x: x["last_updated"], reverse=True)[:4]

    for doc in recent_docs:
        with st.expander(f"{doc['filename']}"):
            st.markdown(f"**Type**: {doc.get('type', 'Pending')}")
            st.markdown(f"**Status**: {doc['status']}")
            st.markdown(f"**Last Updated**: {doc['last_updated']}")

            if st.button(f"View Progress", key=f"view_{doc['filename']}"):
                st.session_state.selected_file = doc['filename']
                st.session_state.page = "progress"
                st.rerun()

