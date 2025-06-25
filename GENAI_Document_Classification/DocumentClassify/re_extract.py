import streamlit as st
from review_utils import run_ocr, get_document_by_name
import os


def run_re_extract_page():
    
      # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 0px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Re-Extraction</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    

    selected_docs = st.session_state.get("selected_docs", [])

    if not selected_docs:
        st.warning("No documents selected for OCR re-extraction.")
        return

    # Initialize session variables
    if "reextract_index" not in st.session_state:
        st.session_state.reextract_index = 0
    if "reextract_results" not in st.session_state:
        st.session_state.reextract_results = {}

    # Only show one document at a time
    if st.session_state.reextract_index < len(selected_docs):
        filename = selected_docs[st.session_state.reextract_index]
        doc = get_document_by_name(filename)

        if not doc:
            st.warning(f"Document not found: {filename}")
            return

        st.markdown(f"#### {filename}")
        path = doc["path"] if os.path.exists(doc["path"]) else os.path.join("uploads", doc["name"])

        if filename not in st.session_state.reextract_results:
            if st.button(" Run OCR Again"):
                result = run_ocr(path)
                st.session_state.reextract_results[filename] = result
                st.rerun()  # Force rerun to show download/next
        else:
            result = st.session_state.reextract_results[filename]
            extracted_text = result["text"]
            ocr_time = result["ocr_time"]

            st.success(" OCR Completed")
            st.download_button(
                label="Download Extracted Text",
                data=extracted_text,
                file_name=f"{doc['name'].split('.')[0]}_ocr.txt",
                mime="text/plain"
            )
            st.markdown(f"**Time Taken:** {ocr_time}s")
            st.markdown("###  Extracted Text")
            st.code(extracted_text[:5000], language="text")

            if st.button(" Next Document"):
                st.session_state.reextract_index += 1
                st.rerun()
    else:
        st.success(" All selected documents have been re-extracted.")
    
    st.markdown("---")
    if st.button("Back to Review Page"):
        st.session_state.page = "review"
        st.rerun()