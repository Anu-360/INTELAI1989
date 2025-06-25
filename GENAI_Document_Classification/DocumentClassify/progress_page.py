def run_progress_page():
    import os
    import json
    import fitz  # PyMuPDF
    import streamlit as st
    from datetime import datetime
  

   

     # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 0px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Live Progress Bar</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    
    

    if "selected_file" not in st.session_state:
        st.warning("No document selected. Go back to the dashboard and select one.")
        return

    filename = st.session_state.selected_file
    file_path = os.path.join("uploads", filename)

    if not os.path.exists(file_path):
        st.error(f"Selected file not found: {file_path}")
        return

    # --- Extract text from file ---
    document_text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                document_text += page.get_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return

    # --- Load metadata from document_log.json ---
    metadata = {}
    try:
        with open("document_log.json", "r") as f:
            logs = json.load(f)
            for doc in logs:
                if doc["filename"] == filename:
                    metadata = doc
                    break
    except Exception:
        st.warning("Unable to read metadata from document_log.json")

    doc_type = metadata.get("type", "Unknown")
    status = metadata.get("status", "Unknown")
    uploaded_time = metadata.get("last_updated", "Not recorded")

    # Determine file type from extension
    file_ext = filename.split(".")[-1].lower()
    file_type = {
        "pdf": "PDF",
        "docx": "Word Document",
        "xlsx": "Excel Spreadsheet",
        "xls": "Excel Spreadsheet",
        "png": "Image",
        "jpg": "Image",
        "jpeg": "Image",
        "gif": "Image"
    }.get(file_ext, "Unknown File Type")

    # Format routed info if manually routed
    if ">" in doc_type:
        parts = [p.strip() for p in doc_type.split(">")]
        routed_info = f"{parts[1]} [{parts[0]}]"
    else:
        routed_info = "appropriate team based on classification"

     # Special handling for admin review case
    routed_details = (
        "Routed for Admin Review"
        if "admin review" in status.lower()
        else f"Sent to **{routed_info}**"
    )

    # --- Layout split ---
    col_meta, col_main = st.columns([1, 2])

    # --- Metadata Panel ---
    with col_meta:
        st.subheader("Document Metadata")
        st.write(f"**File Name:** {filename}")
        st.write(f"**Type:** {doc_type}")
        st.write(f"**Status:** {status}")
        st.write(f"**Uploaded:** {uploaded_time}")
        st.markdown("---")
        if st.button("Back to Dashboard"):
            del st.session_state["selected_file"]
            st.session_state.page = "status"
            st.rerun()

    # --- Workflow Progress Panel ---
    with col_main:
        

        steps = {
            "Ingested": {
                "done": True,
                "details": f"Document uploaded by user on {uploaded_time}"
            },
            "Extracted": {
                "done": True,
                "details": f"Extracted {len(document_text)} characters from {file_type}"
            },
            "Classified": {
                "done": True,
                "details": f"Classified as **{doc_type}** using Gemini"
            },
            "Routed": {
                "done": True,
                "details": routed_details
            }
        }

        st.markdown("### Workflow Steps")
        cols = st.columns(4)
        for i, step in enumerate(steps.keys()):
            with cols[i]:
                if steps[step]["done"]:
                    st.success(f"**{step}** ")
                else:
                    st.info(f"**{step}** ")

        st.markdown("---")

        for step, info in steps.items():
            with st.expander(f"{step} Details"):
                st.write(info["details"])
