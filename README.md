# Document Ingestion and Classification System

This is a robust, modular document ingestion platform built with **Streamlit** and powered by **AWS S3** and **LLM-based document classification**. It automates document upload, extraction, classification, and routing to appropriate cloud storage folders.

---

## 🔹 Features

- **Upload and Ingest**: Supports documents in PDF, Word, Excel, and image formats.
- **Text Extraction**: Uses **OCR (Tesseract)** for images and text parsing for documents.
- **AI Classification**: Uses **Gemini / LLM** to classify documents into departments.
- **Automated Routing**:
  - Classified documents are routed to corresponding **S3 department folders**.
  - Unclassified (Others) are **sent for Admin Review**.
- **Recent Activity Log**: Tracks status updates (e.g., Extracted, Classified, Routed).
- **Interactive Dashboard**:
  - Browse departments and sub-departments.
  - Preview and download documents directly from **S3**.
- **User Interface**: Clean, responsive design with icon support and color-coded departments.

  ---

  ##  🔹 Supported File Types

.pdf — PDF Documents

.docx — Word Documents

.xls, .xlsx — Excel Files

.jpg, .jpeg, .png, .gif — Image Files





