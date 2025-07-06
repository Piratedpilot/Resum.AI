# 🤖 Resum.AI — Smart AI Resume Analyzer

[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://resumaibyakul.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Resum.AI** is a smart, AI-powered resume analysis web app that leverages **Google Gemini AI** to provide deep insights into your resume. Whether you're applying for your dream job or refining your CV, Resum.AI helps you stand out with personalized, structured feedback and scoring.

---

## 🚀 Live Demo

👉 [Click to open Resum.AI](https://resumaibyakul.streamlit.app/)

---

## 👨‍💻 Developed By

**Akul Yadav**  
📧 Contact: akulyadac1959@gmail.com  
🌐 GitHub: [Akul-Yadav](https://github.com/Piratedpilot)

---

## 📸 Screenshots

### 🔍 Resume Upload & Role Selection
![Upload Screenshot]()

### 📊 AI Analysis Report
![Analysis Screenshot](screenshots/analysis.png)

### 📥 PDF Report Download
![PDF Screenshot](screenshots/pdf_download.png)

> _📝 Add your screenshots inside a folder named `/screenshots` in your repo._

---

## ⚙️ Features

✅ Upload resume in `.pdf` format  
✅ Enter desired job role for targeted analysis  
✅ AI-powered evaluation using Google Gemini  
✅ Section-wise breakdown:
- Overall Assessment
- Profile & Skills Analysis
- Experience & Education
- ATS Optimization
- Job Role Match
✅ Resume Score  
✅ Personalized course recommendations  
✅ Downloadable PDF report  
✅ Clean and responsive UI built with **Streamlit**

---

## 🧠 Tech Stack

- **Frontend/UI:** Streamlit  
- **Backend/AI:** Google Gemini Pro API  
- **PDF Generation:** ReportLab  
- **File Handling & Parsing:** Python, PyPDF2  
- **Deployment:** Streamlit Cloud

---

## 📦 Installation & Local Setup

```bash
git clone https://github.com/Piratedpilot/Resum.AI.git
cd Resum.AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env.local file
touch .env.local
