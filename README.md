# 🚀 ATS Resume Scanner & Optimization Engine

![ATS Scanner Logo](https://img.shields.io/badge/ATS-Professional-blue?style=for-the-badge&logo=rocket)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-white?style=for-the-badge&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)

🚀 Live Demo: [https://ats-resume-scanner-k64r.onrender.com/]

**Professional-grade Applicant Tracking System (ATS) simulator designed to bridge the gap between candidates and recruiters.** This engine uses NLP-based semantic matching to provide deep insights into how well a resume aligns with a job description.

## ✨ Key Features

-   **🎯 Advanced ATS Scoring:** Realistic scoring algorithm (0-100%) that mimics professional HR software.
-   **🔍 Semantic Matching:** Goes beyond keyword stuffing—understands context (e.g., "Feature Engineering" ↔ "Data Preprocessing").
-   **📋 Category Breakdown:** Visualizes performance across Core Skills, Tools, Data, and Bonus competencies.
-   **💡 Actionable Insights:** Generates 5-10 concrete recommendations for resume improvement based on matching gaps.
-   **📄 Multi-Format Support:** Robust parsing for PDF, DOCX, and TXT files.
-   **📷 OCR Integration:** Built-in Tesseract OCR support for scanned/image-based resumes.
-   **🐳 Production Ready:** Fully containerized with Docker for easy deployment on Render, Railway, or AWS.

## 🛠️ Tech Stack

-   **Backend:** Python 3.9+, Flask
-   **Analysis:** Pandas, Scikit-learn (Semantic Matching)
-   **Parsing:** PyMuPDF (fitz), pdfplumber, python-docx
-   **OCR:** Tesseract OCR, Pytesseract
-   **AI:** Google Gemini API (Extensible Architecture)
-   **Deployment:** Docker, Gunicorn

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Tesseract OCR (Optional for local image support)

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/HarsheyGolar/ATS-Resume-Scanner.git
   cd ATS-Resume-Scanner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at `https://ats-resume-scanner-k64r.onrender.com/`.

## 🐳 Docker Deployment

To run the application in a production-ready environment:

```bash
docker build -t ats-scanner .
docker run -p 5000:5000 ats-scanner
```

## 📁 Project Structure

```text
├── app.py              # Flask Entry Point
├── Dockerfile          # Production Build Config
├── src/
│   ├── ats.py          # Scoring Engine Logic
│   ├── reader.py       # Multi-format File Parser
│   ├── skills.py       # Skill Classification
│   └── improve.py      # Suggestion Generator
├── templates/          # HTML Templates
├── static/             # Assets (CSS/JS/Images)
└── datasets/           # Skills Database & Samples
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed with ❤️ by Harshey Golar*
