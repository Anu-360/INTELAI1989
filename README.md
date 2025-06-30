# 🚀 Document Ingestion & Classification System

A powerful, modular document ingestion platform built with **Streamlit**, integrated with **AWS S3**, and enhanced by **LLM-powered classification (Gemini/AI)**. Automate your document workflows — from upload to classification and cloud-based storage routing — in one seamless interface.

---

## 🔧 Key Features

✅ **Multi-Format Upload**  
Supports drag-and-drop uploads for:  
`.pdf`, `.docx`, `.xls`, `.xlsx`, `.jpg`, `.jpeg`, `.png`, `.gif`

🧠 **Smart Text Extraction**  
- Built-in OCR via **Tesseract** for image-based documents  
- Fast and reliable text parsing for Word, PDF, and Excel files

📚 **AI-Driven Classification**  
- Uses **Gemini/LLM** to automatically tag documents  
- Categorizes into appropriate **departments and sub-departments**

📂 **Auto-Routing to AWS S3**  
- Documents are sent to their designated **department folders**  
- Uncategorized files are routed to **Admin Review** for manual handling

📈 **Real-Time Activity Log**  
- View recent upload statuses:  
  _Extracted → Classified → Routed_

📊 **Interactive Dashboard**  
- Explore by department/sub-department  
- Instantly **preview** and **download** files from **S3**  
- Responsive UI with **icons**, **color codes**, and user-friendly navigation

---

## 🗂️ Supported File Types

| Type         | Description            |
|--------------|------------------------|
| `.pdf`       | PDF Documents          |
| `.docx`      | Word Documents         |
| `.xls/.xlsx` | Excel Spreadsheets     |
| `.jpg/.jpeg` | Image Files (JPG)      |
| `.png`       | Image Files (PNG)      |
| `.gif`       | Animated Images (GIF)  |

---

## 📌 Ideal Use Cases

- Enterprise document intake and routing
- Departmental document management
- Automated filing for HR, Legal, Finance, etc.
- Admin review pipelines

---

## 📎 Technologies Used

- **Frontend**: Streamlit (Python)
- **Storage**: AWS S3
- **OCR**: Tesseract
- **LLM**: Gemini / Google Vertex AI / OpenAI (pluggable)

---

## 🧪 Coming Soon

- 🔐 Authentication & User Roles  
- 📦 Batch Upload Support  
- 📜 Audit Trail Export (CSV/Excel)  
- 🧠 Custom Classifier Fine-Tuning  
- 📨 Email-to-Ingest Automation  
