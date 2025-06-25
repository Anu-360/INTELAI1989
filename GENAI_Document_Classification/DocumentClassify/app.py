import os
import pytesseract
import streamlit as st
import urllib
# ✅ App imports
from mail_box import run_mailbox_page
from utils import process_and_display_file
from document_status import run_status_page
from progress_page import run_progress_page
from review_page import run_review_page
from manual_route import run_manual_route_page
from re_classify import run_re_classify_page
from re_extract import run_re_extract_page
from departments import run_departments_page,run_subdepartment_page

# ✅ Set page config FIRST
st.set_page_config(page_title="Document Ingestion System", layout="wide")

st.markdown(
    """
    <style>
        /* Global text color */
        html, body, [class*="st-"] {
            color: #000022 !important; /* Oxford Blue */
        }

        /* Bold text */
        strong, b {
            color: #00CED1 !important;
        }

        /* Button styles */
        button, .stButton > button {
            color: #92DCE5 !important;
            background-color: white !important;
            border: 1px solid #000022 !important;
            border-radius: 5px;
            padding: 0.5em 1em;
        }

        /* Button hover effect */
        button:hover, .stButton > button:hover {
            background-color: #40E0D0 !important;
            color: #000022 !important;
            border-color: #40E0D0 !important;
        }

        /* Expander and dropdown arrow override */
        details summary {
            color: #000022 !important;
        }

        details summary::marker {
            color: #000022 !important;
        }

        /* Dropdown and selectbox text */
        .css-1wa3eu0-placeholder,
        .css-1uccc91-singleValue {
            color: #000022 !important;
        }

        svg {
            fill: #000022 !important;
        }
        
        /* Checkbox (unchecked) border color */
        input[type="checkbox"] {
        accent-color: #000022 !important; /* Oxford Blue */
    }

    /* For webkit-based browsers (Chrome, Edge) */
        input[type="checkbox"]:checked {
        accent-color: #000022 !important;  /* Oxford Blue background */
        background-color: #000022 !important;
    }

    /* Customize checkmark color using a pseudo element where possible */
        .stCheckbox > div > label > div:first-child {
        background-color: #000022 !important; /* Checkbox box */
        border: 1px solid #000022 !important;
    }

        .stCheckbox > div > label > div:first-child svg {
        stroke: #40E0D0 !important; /* Tick color: Turquoise */
    }
      

        /* File uploader border and background hover fix */
        section[data-testid="stFileUploader"] > div:hover {
            border: 1px solid #40E0D0 !important;
            background-color: #e0f7f7 !important;
        }

        /* Optional: drop zone */
        div[data-testid="stFileDropzone"] {
            border: 2px dashed #40E0D0 !important;
        }

        div[data-testid="stFileDropzone"]:hover {
            background-color: #40E0D0 !important;
            color: #40E0D0;


        }

        /* Override st.success background to Oxford Blue */
        .stAlert[data-testid="stAlert-success"] {
            background-color: #000022 !important;
            color: #40E0D0 !important;
            border-radius: 10px;
            padding: 1rem;
        }

        /* Optional: style st.info (if you use it for incomplete steps) */
        .stAlert[data-testid="stAlert-info"] {
            background-color: #40E0D0 !important;  /* Turquoise */
            color: #000022 !important;
            border-radius: 10px;
            padding: 1rem;
        }

        /* Ensure markdown bold inside these blocks uses the same color */
        .stAlert strong {
            color: #00CED1 !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)





# ✅ Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'xls', 'xlsx'}

# ✅ Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ✅ Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Main Streamlit app logic
def main():
    
    params = st.query_params
    if "dept" in params and "sub" in params:
        
        run_subdepartment_page(params["dept"], params["sub"])
        return
    
    if "page" not in st.session_state:
        st.session_state.page = "status"

    # ✅ Route to pages
    if st.session_state.page == "status":
        
        run_status_page()
    
    elif st.session_state.page == "upload":
       
        # Centered Page Title
        st.markdown(
    """
    <div style='text-align: center; margin-top: 0px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Document Classification</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    
    

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("Connect Mailbox"):
                st.session_state.page = "mailbox"
                st.rerun()

        st.header("Upload Documents")
        uploaded_files = st.file_uploader("Choose files", type=list(ALLOWED_EXTENSIONS), accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                if allowed_file(uploaded_file.name):
                    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"Uploaded: {uploaded_file.name}")
                    process_and_display_file(file_path, uploaded_file.name)
                else:
                    st.warning(f"Unsupported file type: {uploaded_file.name}")

        # ✅ Back to landing
        if st.button("Back to Landing Page"):
            st.session_state.page = "status"
            st.rerun()

    elif st.session_state.page == "mailbox":
        run_mailbox_page()

    elif st.session_state.page == "progress":
        run_progress_page()

    elif st.session_state.page == "review":
        run_review_page()  

    elif st.session_state.page == "manual_route":
        run_manual_route_page()    

    elif st.session_state.page == "re_classify":
        run_re_classify_page()    

    elif st.session_state.page == "re_extract":
        run_re_extract_page()     

    elif st.session_state.page == "departments":
        run_departments_page()



   

# ✅ Entry point
if __name__ == "__main__":
    main()
