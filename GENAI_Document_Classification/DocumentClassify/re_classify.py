import streamlit as st
from review_utils import get_document_by_name, run_ocr_and_classify
import os


def run_re_classify_page():
    
      # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 0px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Re-Classification</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    

    # Get selected docs
    selected_docs = st.session_state.get("selected_docs", [])

    if not selected_docs:
        st.warning("No documents selected for re-classification.")
        return

    # Initialize state for reclassification results
    if "reclass_results" not in st.session_state:
        st.session_state.reclass_results = {}

    for filename in selected_docs:
        doc = get_document_by_name(filename)
        if not doc:
            st.warning(f"Document not found: {filename}")
            continue

        st.markdown(f"#### {filename}")
        path = doc["path"] if os.path.exists(doc["path"]) else os.path.join("uploads", doc["name"])

        # Display previous result if exists
        if filename in st.session_state.reclass_results:
            result = st.session_state.reclass_results[filename]
            st.success(f" Previously Re-classified as: {result['classification']['type']}")
            st.info(f"Reason: {result['classification']['reason']}")

        # Re-classify button
        if st.button(f" Re-Classify '{filename}'", key=f"reclassify_{filename}"):
            result = run_ocr_and_classify(path)
            st.session_state.reclass_results[filename] = result
            st.success(f" Re-classified as: {result['classification']['type']}")
            st.info(f"Reason: {result['classification']['reason']}")

        st.divider()
    
    # Back to review
    if st.button("Back to Review Page"):
        st.session_state.page = "review"
        st.rerun()