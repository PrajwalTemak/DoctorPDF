# 👨‍⚕️ DoctorPDF API

DoctorPDF is a modular, lightweight FastAPI-based web service designed for high-quality document-to-PDF conversion. It handles images, plain text, and Microsoft Office formats with precision and efficiency.

---

## 🚀 Features

- **Universal Image Conversion**: Converts JPG, PNG, JFIF, and WebP. Automatically normalizes color spaces to RGB for PDF compatibility.
- **Smart Text Wrapping**: Converts `.txt` files into professional PDFs with automatic line wrapping, margins, and special character escaping (HTML/XML safety).
- **Office Document Rendering**: Leverages a headless LibreOffice engine to convert `.docx` and `.pptx` files while maintaining original layouts.
- **Clean Architecture**: Modular logic split into dedicated handlers for easy maintenance and scaling.
- **Docker Ready**: Fully containerized for instant deployment.

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Image Processing**: [Pillow](https://python-pillow.org/) & [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)
- **PDF Layout**: [ReportLab](https://www.reportlab.com/) (Platypus Engine)
- **Office Engine**: [LibreOffice](https://www.libreoffice.org/) (Headless Mode)
- **Server**: Uvicorn

---

## 📂 Project Structure

```text
DoctorPDF/
├── main.py              # API Routing & Middleware
├── convert_image.py     # Image-to-PDF Logic
├── convert_text.py      # Text-to-PDF Logic (with Wrapping)
├── convert_office.py    # Word/PPT-to-PDF Logic (LibreOffice)
├── requirements.txt     # Python Dependencies
└── Dockerfile           # System-level Dependencies