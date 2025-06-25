import streamlit as st
import json
import os
from datetime import datetime
import boto3
from dotenv import load_dotenv


load_dotenv()

# Initialize S3 client with credentials from .env
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

BUCKET_NAME = "designathon1"

def list_folders(prefix=""):
    """List folders under a given S3 prefix."""
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter='/')
    folders = [cp['Prefix'].replace(prefix, "").strip("/") for cp in response.get('CommonPrefixes', [])]
    return folders

def upload_to_s3(local_path, filename, department, subcategory):
    """Upload file to appropriate S3 folder."""
    s3_key = f"{department}/{subcategory}/{filename}"
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

def run_manual_route_page():
   
      # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 0px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Manual Routing</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    

    selected_filenames = st.session_state.get("selected_docs", [])
    if not selected_filenames:
        st.warning("No documents selected for routing.")
        return

    if "current_doc_index" not in st.session_state:
        st.session_state.current_doc_index = 0

    log_path = "document_log.json"
    if not os.path.exists(log_path):
        st.error("document_log.json not found.")
        return

    with open(log_path, "r") as f:
        log_data = json.load(f)

    for i in range(st.session_state.current_doc_index + 1):
        if i >= len(selected_filenames):
            continue

        filename = selected_filenames[i]
        doc = next((d for d in log_data if d["filename"] == filename), None)
        if not doc:
            st.warning(f"'{filename}' not found in log.")
            continue

        st.subheader(f"{filename}")

        if i < st.session_state.current_doc_index:
            st.success("Routed")
        elif i == st.session_state.current_doc_index:
            departments = list_folders()  # Get main folders
            department = st.selectbox("Select Department", departments, key=f"dept_{filename}")

            subcategories = list_folders(prefix=f"{department}/") if department else []
            subcategory = st.selectbox("Select Sub-Category", subcategories, key=f"sub_{filename}")

            if st.button(f"Route '{filename}' to S3", key=f"route_{filename}"):
                local_path = os.path.join("uploads", filename)

                if upload_to_s3(local_path, filename, department, subcategory):
                    doc["type"] = f"{department} > {subcategory}"
                    doc["status"] += " Classified → Manually Routed"
                    doc["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    with open(log_path, "w") as f:
                        json.dump(log_data, f, indent=4)

                    st.success(f"Routed '{filename}' to {department}/{subcategory}")
                    st.session_state.current_doc_index += 1
                    st.rerun()
                else:
                    st.error("Upload failed. Check AWS credentials or bucket permissions.")

    if st.session_state.current_doc_index >= len(selected_filenames):
        st.success("All selected documents have been routed.")
    
    st.markdown("---")
    if st.button("Back to Review Page"):
        st.session_state.page = "review"
        if "current_doc_index" in st.session_state:
            del st.session_state.current_doc_index
        st.rerun()