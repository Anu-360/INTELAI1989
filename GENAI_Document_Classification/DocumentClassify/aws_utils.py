import boto3
import os
import mimetypes
from folder_mapping import folder_map
from dotenv import load_dotenv

load_dotenv()  # Loads credentials from .env

BUCKET_NAME = "designathon1"

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)



def upload_to_s3(local_path, filename, classification):
    # Map classification to folder path
    folder = folder_map.get(classification, "Others")
    s3_key = f"{folder}/{filename}"

    # Check if the file exists
    if not os.path.exists(local_path):
        print(f"File not found: {local_path}")
        return False

    # Guess the MIME type (optional, but useful for previewing files in S3)
    content_type, _ = mimetypes.guess_type(local_path)
    extra_args = {"ContentType": content_type} if content_type else {}

    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key, ExtraArgs=extra_args)
        print(f"Uploaded {filename} → s3://{BUCKET_NAME}/{s3_key}")
        return True
    except Exception as e:
        print(f"Failed to upload {filename}: {e}")
        return False
