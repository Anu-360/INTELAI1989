import streamlit as st
import json
import os
from manual_route import run_manual_route_page


def run_review_page():
    # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 0px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Review Documents</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    # Hide default Streamlit UI and setup custom styles
    st.markdown(
        """
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        .top-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .button-group {
            display: flex;
            gap: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Top row: Back button on left, action buttons on right
    st.markdown('<div class="top-row">', unsafe_allow_html=True)
    c1,c2,c3 = st.columns([2,2,2])

    with c1:
        if st.button("Re-Extract OCR"):
                st.session_state.page = "re_extract"
                st.rerun()

   

    with c2:
        if st.button("Re-Classify"):
            if st.session_state.get("selected_docs"):
                st.session_state.reclassify_index = 0
                try:
                    with open("document_log.json", "r") as f:
                        all_docs = json.load(f)

                    selected_doc = next(
                            (doc for doc in all_docs if doc["filename"] == st.session_state["selected_docs"][0]),
                            None
                    )

                    if selected_doc:
                        st.session_state["doc_filename"] = selected_doc["filename"]
                        st.session_state.page = "re_classify"
                        st.rerun()
                    else:
                        st.warning("Unable to find the selected document for re-classification.")
                except Exception as e:
                    st.error(f"Re-classification failed: {e}")
            else:
                st.warning("Please select at least one document to re-classify.")

    with c3:
        if st.button("Route Manually"):
            if st.session_state.get("selected_docs"):
                try:
                    with open("document_log.json", "r") as f:
                        all_docs = json.load(f)

                    selected_doc = next(
                            (doc for doc in all_docs if doc["filename"] == st.session_state["selected_docs"][0]),
                            None
                    )

                    if selected_doc:
                        st.session_state["doc_filename"] = selected_doc["filename"]
                        st.session_state.page = "manual_route"
                        st.rerun()
                    else:
                        st.warning("Unable to find the selected document.")
                except Exception as e:
                    st.error(f"Routing failed: {e}")
            else:
                st.warning("Please select at least one document to route.")

        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

  

    # Load documents classified as 'Others'
    LOG_FILE = "document_log.json"
    if not os.path.exists(LOG_FILE):
        st.error(f"File {LOG_FILE} not found!")
        return

    def load_others_docs():
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
        return [doc for doc in data if doc.get("type", "").strip().lower() == "others"
                and "Manually Routed" not in doc.get("status","")]

    others_docs = load_others_docs()

    # Initialize selected docs session state
    if "selected_docs" not in st.session_state:
        st.session_state.selected_docs = []

    if not others_docs:
        st.info("No documents classified as 'Others' found.")
    else:
        selected = []
        for doc in others_docs:
            col_checkbox, col_expander = st.columns([0.05, 0.95])
            with col_checkbox:
                checked = st.checkbox("", key=f"select_{doc['filename']}")
            with col_expander:
                with st.expander(f"{doc['filename']}"):
                    st.markdown(f"**Type:** {doc.get('type', 'Unknown')}")
                    st.markdown(f"**Status:** {doc.get('status', 'Unknown')}")
                    st.markdown(f"**Last Updated:** {doc.get('last_updated', 'Unknown')}")

            if checked:
                selected.append(doc["filename"])

        st.session_state.selected_docs = selected
        st.markdown("---")
        if st.button("Back to Dashboard"):
          st.session_state.page = "status"
          st.rerun()



