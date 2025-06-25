import streamlit as st
import boto3
import os
from dotenv import load_dotenv
import urllib.parse
import mimetypes

# Load environment variables
load_dotenv()


# AWS S3 client setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

BUCKET_NAME = "designathon1"
# Department images and descriptions (customize as needed)
department_meta = {
    "Human Resources": {
        "image": "https://i.pinimg.com/736x/99/78/81/997881c27d9ee41ba0a73878222b8d5f.jpg",
        "description": "Handles employee management and organizational staffing"
    },
    "Finance and Accounting": {
        "image": "https://wallpaperaccess.com/full/1104816.jpg",
        "description": "Manages financial planning, transactions, and reporting"
    },
    "Administration": {
        "image": "https://wallpapercave.com/wp/wp10701801.jpg",
        "description": "Manages office operations and internal coordination"
    },
    "Customer Service": {
        "image":"https://wallpapercave.com/wp/wp6680305.jpg",
        "description": "Supports customers through feedback and service handling",
    },
    "IT Department": {
        "image": "https://learn.g2.com/hubfs/What_is_Information_Technology.jpg",
        "description":"Maintains technology systems and digital infrastructure"
    },
    "Legal": {
        "image": "https://static.vecteezy.com/system/resources/previews/027/105/968/large_2x/legal-law-and-justice-concept-open-law-book-with-a-wooden-judges-gavel-in-a-courtroom-or-law-enforcement-office-free-photo.jpg",
        "description":"Oversees compliance, contracts, and legal affairs"
    },
    "Marketing":{
        "image":"http://getwallpapers.com/wallpaper/full/b/1/f/916900-vertical-marketing-wallpapers-1920x1080.jpg",
        "description":"Promotes products and manages brand strategy"
    },
    "Operations":{
        "image":"https://img.freepik.com/premium-photo/hands-businessman-virtual-innovation-business-process-problem-solving-workflow-monitoring-evaluation-as-well-as-quality-control-are-all-part-operations-management_27634-829.jpg",
        "description":"Ensures smooth day-to-day business processes"
    },
    "Research and Development":{
        "image":"https://img.freepik.com/premium-photo/hand-businessman-working-r-d-icon-research-development-laptop-screen_112554-964.jpg",
        "description":"Focuses on innovation and product improvement"
    },
    "Sales":{
        "image":"https://wallpaperaccess.com/full/1804129.jpg",
        "description":"Drives revenue through client acquisition and deals"
    },
    "Others":{
        "image":"https://png.pngtree.com/thumb_back/fh260/background/20230926/pngtree-stack-of-black-binders-from-bsu-college-of-business-administration-image_13299656.jpg",
        "description":"Covers uncategorized or miscellaneous documents"
    }

}


def list_departments_from_s3():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter='/')
        return [cp['Prefix'].strip('/') for cp in response.get('CommonPrefixes', [])]
    except Exception as e:
        st.error(f"Error fetching departments: {e}")
        return []

def list_subdepartments_from_s3(department):
    try:
        prefix = f"{department}/"
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter="/")
        return [cp["Prefix"].replace(prefix, "").strip("/") for cp in response.get("CommonPrefixes", [])]
    except Exception as e:
        st.error(f"Error fetching sub-departments for {department}: {e}")
        return []

def list_files_in_subdepartment(department, subdepartment):
    prefix = f"{department}/{subdepartment}/"
   
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
      
        return [obj["Key"].replace(prefix, "") for obj in response.get("Contents", []) if obj["Key"] != prefix]
    except Exception as e:
        st.error(f"Error fetching files: {e}")
        return []

def run_departments_page():
    
      # Centered Page Title
    st.markdown(
    """
    <div style='text-align: center; margin-top: 1px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>Departments</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    
    all_departments = list_departments_from_s3()
    departments = [d for d in all_departments if d in department_meta]

    if "dept_page" not in st.session_state:
        st.session_state.dept_page = 1

    page_size = 6
    total_pages = (len(departments) + page_size - 1) // page_size
    current_page = st.session_state.dept_page
    start = (current_page - 1) * page_size
    end = start + page_size

    cols = st.columns(3)
    for idx, dept in enumerate(departments[start:end]):
        with cols[idx % 3]:
            meta = department_meta.get(dept, {})
            sub_depts = list_subdepartments_from_s3(dept)

            if sub_depts:
                sub_html = "".join(
                    f"<div style='margin-bottom: 5px;'><a href='?dept={urllib.parse.quote(dept)}&sub={urllib.parse.quote(sub)}' "
    f"target='_self' style='color:#000022;  text-decoration: none;'>{sub}</a></div>"
                    for sub in sub_depts
                )
            else:
                sub_html = "<li>No sub-departments found.</li>"

            st.markdown(
    f"""
    <div style="width: 350px; border-radius: 15px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.1); margin-bottom: 20px; background-color: white;">
        <div style="background-image: url('{meta.get('image')}'); background-size: cover; background-position: center; height: 100px;"></div>
        <div style="padding: 15px; color: #000022;">
            <h4 style="margin-bottom: 8px; color: #000022;">{dept}</h4>
            <p style="font-size: 13px; color: #333;">{meta.get('description', '')}</p>
            <details style="margin-top: 10px;">
                <summary style="color: #40E0D0;">Sub-Departments</summary>
                <div style="padding-left: 20px; color: #40E0D0;">{sub_html}</div>
            </details>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if current_page > 1 and st.button("Previous"):
            st.session_state.dept_page -= 1
            st.rerun()
    with col3:
        if current_page < total_pages and st.button("Next"):
            st.session_state.dept_page += 1
            st.rerun()
    with col2:
        st.markdown(f"<center>Page {current_page} of {total_pages}</center>", unsafe_allow_html=True)

    # Back button
    if st.button("Back"):
        st.session_state.page = "status"
        
        st.rerun()    

def run_subdepartment_page(dept, sub):
    
    st.markdown(
    f"""
    <div style='text-align: center; margin-top: 1px; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em;'>{sub}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    
    

    files = list_files_in_subdepartment(dept, sub)
    if not files:
        st.info("No files found.")
        return

    
    # Generate rows HTML
    rows_html = ""
    for file in files:
        key = f"{dept}/{sub}/{file}"
        file_ext = file.split(".")[-1].upper()

        # Get last modified time from S3
        try:
            obj_head = s3.head_object(Bucket=BUCKET_NAME, Key=key)
            uploaded_time = obj_head["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            uploaded_time = "Unknown"
            
        mime_type, _=mimetypes.guess_type(file)
        # For images, force inline preview
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            view_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": key,
            "ResponseContentDisposition": "inline",
            "ResponseContentType": mime_type or "image/jpehg"
        },
        ExpiresIn=3600
    )
        else:
    # Default view behavior (PDF, etc.)
            view_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=3600
    )


# Download link (forces download)
        download_url = s3.generate_presigned_url(
    ClientMethod="get_object",
    Params={
        "Bucket": BUCKET_NAME,
        "Key": key,
        "ResponseContentDisposition": f"attachment; filename={file}"
    },
    ExpiresIn=3600
)



        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png",".docx",".xslx",".xls",".gif")):
           preview_icon = f"<a href='{view_url}' target='_blank' class='icon-btn'><i class='fas fa-eye'></i></a>"
        else:
           preview_icon = f"<a href='{view_url}' target='_blank' class='icon-btn'><i class='fas fa-eye'></i></a>"

        download_icon = f"<a href='{download_url}'  target='_blank' download class='icon-btn'><i class='fas fa-download'></i></a>"

        rows_html += f"""
            <tr>
                <td>{file}</td>
                <td>{file_ext}</td>
                <td>{uploaded_time}</td>
                <td>{preview_icon}{download_icon}</td>
            </tr>
        """

  

    import streamlit.components.v1 as components

    components.html(f"""
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    .file-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }}
    .file-table th, .file-table td {{
        border: 1px solid #444;
        padding: 10px 15px;
        text-align: center;
        min-width: 120px;
    }}
    .file-table th {{
        background-color: #40E0D0;
        color: #000022;
        font-weight: 600;
    }}
    .file-table td {{
        background-color:white;
        color: #333333;
    }}
    .icon-btn {{
            margin: 0 8px;
            font-size: 1.2em;
            text-decoration: none;
            color: #002147;  /* Oxford Blue for icons */
        }}
</style>
</head>
<body>
<div style="overflow-x:auto;">
    <table class="file-table">
        <thead>
            <tr>
                <th>File Name</th>
                <th>Type</th>
                <th>Uploaded</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</div>
</body>
</html>
""", height=500, scrolling=True)
    
    st.markdown("---")
    if st.button("Back to Departments", key="back_top"):
        st.query_params.clear()
        st.rerun()
    
   

    
