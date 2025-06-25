import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import docx
import pandas as pd
import streamlit as st
import json
import re
from datetime import datetime
from embedding_utils import classify_document
from aws_utils import upload_to_s3  # ✅ Added for S3 upload




# File to track document processing status
LOG_FILE = "document_log.json"

# Extract text based on file type
def extract_text(file_path, filename):
    if filename.endswith(('jpg', 'jpeg', 'png', 'gif')):
        return pytesseract.image_to_string(Image.open(file_path))

    elif filename.endswith('.pdf'):
        try:
            with fitz.open(file_path) as doc:
                return "".join([page.get_text() for page in doc])
        except Exception as e:
            st.error(f"Error reading PDF file: {str(e)}")
            return ""

    elif filename.endswith('.docx'):
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading Word file: {str(e)}")
            return ""

    elif filename.endswith(('.xls', '.xlsx')):
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            return df.to_string(index=False)
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
            return ""

    else:
        return "Unsupported file type."

# Update document status in the log
def update_document_log(filename, doc_type, status):
    log_entry = {
        "filename": filename,
        "type": doc_type,
        "status": status,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data = [d for d in data if d["filename"] != filename]
    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Main processing function
def process_and_display_file(file_path, filename):
    
    st.subheader(f" {filename}")

    # Step 1: Extract
    extracted_text = extract_text(file_path, filename)
    update_document_log(filename, "Pending", "Ingested → Extracted")

    st.markdown("** Extracted Text:**")

    # 💾 Download button
    st.download_button(
        label="Download Extracted Text",
        data=extracted_text,
        file_name=f"{filename.split('.')[0]}_extracted.txt",
        mime="text/plain"
    )

    # Step 2: Classify using Gemini
    st.markdown("**Document Classification Summary:**")
    try:
        result_text = classify_document(extracted_text)

        if result_text.startswith("ERROR::"):
            raise Exception(result_text.replace("ERROR::", ""))

        # ✅ Clean up markdown/code block formatting
        if result_text.strip().startswith("```"):
            result_text = re.sub(r"```(?:json)?", "", result_text).strip("` \n")

        classification = json.loads(result_text)

        doc_type = classification.get("type", "Unknown")
        confidence = float(classification.get("confidence", 0.0))
        reason = classification.get("reason", "No reason provided.")

        st.success(f"This document is classified as **{doc_type.upper()}** with confidence **{confidence:.2f}**.")
        st.info(f"Reason: {reason}")

        status = "Classified"

        if doc_type.strip().lower() == "others":
            # Do NOT upload to S3 — send for admin review
            status += " → Sent for Admin Review"
            update_document_log(filename, doc_type, status)
            st.warning("Document classified as 'Others'. Routed to Admin Review.")
        else:

            # ✅ Create doc structure for S3 upload
            doc = {
            "path": file_path,
            "name": filename,
            "type": doc_type,
            "status": status
            }

            success = upload_to_s3(doc["path"], doc["name"], doc["type"])

            if success:
               doc["status"] += " → Routed to S3"
               update_document_log(filename, doc_type, doc["status"])
               st.success("Document successfully routed to S3.")
            else:
               doc["status"] += " → S3 Upload Failed"
               update_document_log(filename, doc_type, doc["status"])
               st.error("Failed to route document to S3.")

    except json.JSONDecodeError:
        st.error("Gemini response is not valid JSON. Raw response:")
        st.code(result_text)
    except Exception as e:
        st.warning(f"Gemini classification failed: {str(e)}")
