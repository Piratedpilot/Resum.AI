# 🚀 Resum.AI - Smart AI Resume Analyzer

<div align="center">

![Resum.AI Logo](https://img.shields.io/badge/Resum.AI-Smart%20Resume%20Intelligence-6366f1?style=for-the-badge&logo=rocket)

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Transform Your Career with AI-Powered Resume Analysis**

[🌟 Live Demo](https://your-app-url.streamlit.app) •

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 What Makes Resum.AI Special](#-what-makes-resumai-special)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🎮 Usage](#-usage)
- [🏗️ Project Structure](#️-project-structure)
- [🤖 AI Models](#-ai-models)
- [📊 Analytics & Dashboard](#-analytics--dashboard)
- [🔧 API Reference](#-api-reference)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)
- [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ Features

### 🔍 **AI-Powered Analysis**
- **Google Gemini Integration** - Advanced AI analysis with personalized feedback
- **ATS Compatibility Check** - Ensure your resume passes Applicant Tracking Systems
- **Role-Specific Analysis** - Tailored feedback for 50+ job roles across multiple industries
- **Custom Job Description Matching** - Upload specific job descriptions for targeted analysis

### 📝 **Smart Resume Builder**
- **Comprehensive Form Builder** - Personal info, experience, education, skills, projects, activities
- **Multiple Templates** - Modern, Professional, Minimal, and Creative designs
- **Real-time Validation** - Instant feedback and suggestions while building
- **Export Options** - Download as DOCX with professional formatting

### 📊 **Advanced Analytics**
- **Performance Dashboard** - Track resume improvements over time
- **Score Breakdown** - Detailed metrics for different resume sections
- **Industry Benchmarking** - Compare against industry standards
- **Success Rate Tracking** - Monitor application success rates

### 🎯 **Job Search Integration**
- **Role Recommendations** - AI-suggested positions based on your profile
- **Skill Gap Analysis** - Identify missing skills for target roles
- **Course Recommendations** - Personalized learning paths for career growth
- **Market Insights** - Industry trends and salary information

### 🔒 **Enterprise Features**
- **Admin Dashboard** - Comprehensive analytics and user management
- **Bulk Analysis** - Process multiple resumes simultaneously
- **Custom Branding** - White-label solution for organizations
- **API Access** - Integrate with existing HR systems

---

## 🎯 What Makes Resum.AI Special

| Feature | Traditional Tools | Resum.AI |
|---------|------------------|----------|
| **AI Analysis** | ❌ Basic keyword matching | ✅ Advanced Google Gemini AI |
| **ATS Optimization** | ❌ Limited checking | ✅ Comprehensive ATS analysis |
| **Role Specificity** | ❌ Generic feedback | ✅ 50+ role-specific analyses |
| **Real-time Feedback** | ❌ Static reports | ✅ Interactive, dynamic insights |
| **Resume Building** | ❌ Basic templates | ✅ AI-powered smart builder |
| **Career Guidance** | ❌ No recommendations | ✅ Personalized career paths |
| **Analytics** | ❌ No tracking | ✅ Comprehensive dashboard |
| **Cost** | 💰 Expensive subscriptions | 🆓 **Completely Free** |

---

## 🚀 Quick Start

### Option 1: Run Locally (Recommended)

\`\`\`bash
# Clone the repository
git clone https://github.com/yourusername/Smart-AI-Resume-Analyzer.git
cd Smart-AI-Resume-Analyzer

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app.py
\`\`\`

### Option 2: Docker Deployment

\`\`\`bash
# Build and run with Docker
docker build -t resumai .
docker run -p 8501:8501 resumai
\`\`\`

### Option 3: One-Click Deploy

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/yourusername/smart-ai-resume-analyzer/main/app.py)

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **Google Gemini API Key** - [Get API Key](https://ai.google.dev)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Step-by-Step Installation

1. **Clone the Repository**
   \`\`\`bash
   git clone https://github.com/yourusername/Smart-AI-Resume-Analyzer.git
   cd Smart-AI-Resume-Analyzer
   \`\`\`

2. **Create Virtual Environment**
   \`\`\`bash
   # Windows
   python -m venv venv
   venv\\Scripts\\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   \`\`\`

3. **Install Dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Set Up Environment Variables**
   \`\`\`bash
   cp .env.example .env
   \`\`\`
   
   Edit \`.env\` file:
   \`\`\`env
   GOOGLE_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///resumai.db
   SECRET_KEY=your_secret_key_here
   \`\`\`

5. **Initialize Database**
   \`\`\`bash
   python -c "from config.database import init_database; init_database()"
   \`\`\`

6. **Run the Application**
   \`\`\`bash
   streamlit run app.py
   \`\`\`

7. **Access the Application**
   Open your browser and navigate to \`http://localhost:8501\`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| \`GOOGLE_API_KEY\` | Google Gemini API key | ✅ Yes | - |
| \`DATABASE_URL\` | Database connection string | ❌ No | \`sqlite:///resumai.db\` |
| \`SECRET_KEY\` | Application secret key | ❌ No | Auto-generated |
| \`DEBUG\` | Enable debug mode | ❌ No | \`False\` |
| \`MAX_FILE_SIZE\` | Maximum upload file size (MB) | ❌ No | \`10\` |

### API Keys Setup

#### Google Gemini API
1. Visit [Google AI Studio](https://ai.google.dev)
2. Create a new project or select existing
3. Enable the Gemini API
4. Generate an API key
5. Add to your \`.env\` file

### Database Configuration

Resum.AI supports multiple database backends:

\`\`\`python
# SQLite (Default)
DATABASE_URL=sqlite:///resumai.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/resumai

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/resumai
\`\`\`

---

## 🎮 Usage

### 1. 🔍 Resume Analysis

#### Standard Analysis
1. Navigate to the **Analyzer** page
2. Select your target job category and role
3. Upload your resume (PDF or DOCX)
4. Click **"Analyze Resume"**
5. Review detailed feedback and recommendations

#### AI-Powered Analysis
1. Go to **AI Analysis** tab
2. Choose **Google Gemini** as your AI model
3. Optionally provide a custom job description
4. Upload your resume
5. Click **"Analyze with AI"**
6. Get comprehensive AI-generated insights

### 2. 📝 Resume Building

#### Step-by-Step Builder
1. Visit the **Builder** page
2. Choose your preferred template
3. Fill out each section:
   - **Personal Information** - Contact details and links
   - **Professional Summary** - Career objective and highlights
   - **Skills** - Technical, soft skills, languages, tools
   - **Work Experience** - Job history with achievements
   - **Education** - Academic background and certifications
   - **Projects** - Portfolio of work and personal projects
   - **Activities** - Leadership, volunteer work, competitions
4. Click **"Generate Resume"**
5. Download your professionally formatted resume

### 3. 📊 Dashboard Analytics

#### Personal Dashboard
- **Resume Score Trends** - Track improvements over time
- **Analysis History** - Review past analyses
- **Skill Development** - Monitor skill gap progress
- **Application Success** - Track job application outcomes

#### Admin Dashboard (For Organizations)
- **User Analytics** - Platform usage statistics
- **Performance Metrics** - Success rates and trends
- **Content Management** - Manage job roles and templates
- **System Health** - Monitor application performance

### 4. 🎯 Job Search Features

#### Smart Recommendations
- **Role Matching** - AI-suggested positions based on your profile
- **Skill Analysis** - Identify gaps for target roles
- **Market Insights** - Salary ranges and industry trends
- **Course Suggestions** - Personalized learning recommendations

---

## 🏗️ Project Structure

\`\`\`
Smart-AI-Resume-Analyzer/
├── 📁 app.py                 # Main Streamlit application
├── 📁 requirements.txt       # Python dependencies
├── 📁 .env.example          # Environment variables template
├── 📁 Dockerfile           # Docker configuration
├── 📁 README.md            # Project documentation
├── 📁 LICENSE              # MIT License
│
├── 📂 config/              # Configuration files
│   ├── database.py         # Database setup and connections
│   ├── job_roles.py        # Job role definitions
│   └── courses.py          # Course recommendations
│
├── 📂 utils/               # Utility modules
│   ├── ai_resume_analyzer.py    # Google Gemini integration
│   ├── resume_analyzer.py       # Standard analysis engine
│   ├── resume_builder.py        # Resume generation
│   └── text_extraction.py      # PDF/DOCX text extraction
│
├── 📂 dashboard/           # Dashboard components
│   ├── dashboard.py        # Main dashboard logic
│   ├── analytics.py        # Analytics calculations
│   └── visualizations.py  # Chart and graph generation
│
├── 📂 feedback/            # Feedback system
│   ├── feedback.py         # Feedback collection
│   └── sentiment.py       # Feedback analysis
│
├── 📂 jobs/                # Job search features
│   ├── job_search.py       # Job matching logic
│   ├── recommendations.py  # AI recommendations
│   └── market_data.py      # Industry insights
│
├── 📂 ui_components/       # UI components
│   ├── __init__.py
│   ├── cards.py           # Reusable card components
│   ├── charts.py          # Chart components
│   └── forms.py           # Form components
│
├── 📂 templates/           # Resume templates
│   ├── modern.py          # Modern template
│   ├── professional.py    # Professional template
│   ├── minimal.py         # Minimal template
│   └── creative.py        # Creative template
│
├── 📂 static/              # Static assets
│   ├── css/               # Custom stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images and icons
│
├── 📂 tests/               # Test suite
│   ├── test_analyzer.py   # Analyzer tests
│   ├── test_builder.py    # Builder tests
│   └── test_api.py        # API tests
│
└── 📂 docs/                # Documentation
    ├── api.md             # API documentation
    ├── deployment.md      # Deployment guide
    └── contributing.md    # Contribution guidelines
\`\`\`

---

## 🤖 AI Models

### Google Gemini Integration

Resum.AI leverages Google's advanced Gemini AI model for intelligent resume analysis:

#### Capabilities
- **Natural Language Understanding** - Comprehends resume content contextually
- **Role-Specific Analysis** - Tailors feedback based on target job roles
- **ATS Optimization** - Ensures compatibility with tracking systems
- **Personalized Recommendations** - Provides actionable improvement suggestions

#### Analysis Features
- **Content Quality Assessment** - Evaluates writing quality and clarity
- **Keyword Optimization** - Identifies missing industry keywords
- **Structure Analysis** - Reviews resume organization and flow
- **Achievement Quantification** - Suggests metrics and numbers
- **Skills Gap Identification** - Compares skills against job requirements

#### Custom Prompts
The AI uses carefully crafted prompts for different analysis types:

\`\`\`python
# Example: Software Engineer Analysis
prompt = f"""
Analyze this resume for a {job_role} position:

Resume Content: {resume_text}

Provide detailed feedback on:
1. Technical skills alignment
2. Project descriptions and impact
3. ATS optimization
4. Missing keywords
5. Overall score (1-100)

Format as structured analysis with actionable recommendations.
"""
\`\`\`

---

## 📊 Analytics & Dashboard

### Key Metrics Tracked

#### User Analytics
- **Resume Scores** - Track improvement over time
- **Analysis Frequency** - Usage patterns and engagement
- **Success Rates** - Job application outcomes
- **Skill Development** - Progress in skill acquisition

#### System Analytics
- **Performance Metrics** - Response times and system health
- **Usage Statistics** - Active users and feature adoption
- **Error Tracking** - System reliability and bug reports
- **API Usage** - Google Gemini API consumption

### Dashboard Features

#### Personal Dashboard
\`\`\`python
# Example metrics displayed
metrics = {
    "resume_score": 85,
    "improvement": "+12 points",
    "analyses_count": 15,
    "success_rate": "78%"
}
\`\`\`

#### Admin Dashboard
- **User Management** - View and manage user accounts
- **Content Management** - Update job roles and templates
- **System Monitoring** - Track performance and usage
- **Analytics Reports** - Generate detailed reports

---

## 🔧 API Reference

### Core Functions

#### Resume Analysis
\`\`\`python
from utils.ai_resume_analyzer import AIResumeAnalyzer

analyzer = AIResumeAnalyzer()
result = analyzer.analyze_resume_with_gemini(
    resume_text="...",
    job_role="Software Engineer",
    job_description="..." # Optional
)
\`\`\`

#### Resume Building
\`\`\`python
from utils.resume_builder import ResumeBuilder

builder = ResumeBuilder()
resume_buffer = builder.generate_resume({
    "personal_info": {...},
    "experience": [...],
    "education": [...],
    "skills": {...}
})
\`\`\`

### Database Operations

#### Save Analysis Data
\`\`\`python
from config.database import save_ai_analysis_data

save_ai_analysis_data(user_id, {
    "model_used": "Google Gemini",
    "resume_score": 85,
    "job_role": "Software Engineer"
})
\`\`\`

### Configuration

#### Environment Setup
\`\`\`python
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
\`\`\`

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Reporting Bugs

1. **Check existing issues** - Search for similar problems
2. **Create detailed report** - Include steps to reproduce
3. **Provide context** - OS, Python version, browser
4. **Add screenshots** - Visual evidence helps

### 💡 Suggesting Features

1. **Check roadmap** - See if feature is already planned
2. **Create feature request** - Use the issue template
3. **Explain use case** - Why is this feature needed?
4. **Provide examples** - Mock-ups or descriptions

### 🔧 Code Contributions

#### Getting Started
1. **Fork the repository**
2. **Create feature branch** - \`git checkout -b feature/amazing-feature\`
3. **Make changes** - Follow coding standards
4. **Add tests** - Ensure code coverage
5. **Update documentation** - Keep docs current
6. **Submit pull request** - Use PR template

#### Development Setup
\`\`\`bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
black .

# Run type checking
mypy .
\`\`\`

#### Coding Standards
- **PEP 8** - Follow Python style guide
- **Type Hints** - Use type annotations
- **Docstrings** - Document all functions
- **Tests** - Write unit tests for new features

### 📝 Documentation

Help improve our documentation:
- **Fix typos** - Even small corrections help
- **Add examples** - Show how to use features
- **Improve clarity** - Make instructions clearer
- **Translate** - Help with internationalization

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ **Commercial use** - Use in commercial projects
- ✅ **Modification** - Modify and adapt the code
- ✅ **Distribution** - Share and distribute
- ✅ **Private use** - Use for personal projects
- ❌ **Liability** - No warranty or liability
- ❌ **Trademark use** - Cannot use project trademarks

---

## 👨‍💻 Author

<div align="center">

### **Akul Yadav**
*Full Stack Developer & AI Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-Piratedpilot-181717?style=for-the-badge&logo=github)](https://github.com/Piratedpilot)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Akul%20Yadav-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/akul-yadav-1832b0258/)
[![Email](https://img.shields.io/badge/Email-akulyadav1959%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:akulyadav1959@gmail.com)

*"Passionate about creating intelligent solutions that help people advance their careers."*

</div>

### 🌟 About the Developer

Akul Yadav is a dedicated full-stack developer with expertise in:
- **AI/ML Integration** - Google Gemini, OpenAI, TensorFlow
- **Web Development** - Python, Streamlit, React, Node.js
- **Data Science** - Pandas, NumPy, Plotly, Scikit-learn
- **Cloud Platforms** - AWS, Google Cloud, Vercel
- **Database Systems** - PostgreSQL, MongoDB, SQLite

### 💼 Professional Experience
- **5+ years** in software development
- **50+ projects** delivered successfully
- **Open source contributor** with 100+ repositories
- **AI enthusiast** with focus on practical applications

---

## 🙏 Acknowledgments

### 🤖 AI & Technology Partners
- **[Google Gemini](https://ai.google.dev)** - Advanced AI analysis capabilities
- **[Streamlit](https://streamlit.io)** - Rapid web app development framework
- **[Plotly](https://plotly.com)** - Interactive data visualization
- **[Python-docx](https://python-docx.readthedocs.io)** - Document generation

### 📚 Libraries & Dependencies
- **[PyPDF2](https://pypdf2.readthedocs.io)** - PDF text extraction
- **[Pandas](https://pandas.pydata.org)** - Data manipulation and analysis
- **[SQLAlchemy](https://sqlalchemy.org)** - Database ORM
- **[Requests](https://requests.readthedocs.io)** - HTTP library

### 🎨 Design & UI
- **[Google Fonts](https://fonts.google.com)** - Typography (Inter, Poppins)
- **[Lucide Icons](https://lucide.dev)** - Beautiful icon set
- **[Tailwind CSS](https://tailwindcss.com)** - Utility-first CSS framework

### 🌟 Inspiration & Community
- **Resume analysis research** from leading HR professionals
- **ATS optimization techniques** from recruitment experts
- **Open source community** for continuous learning and improvement
- **Beta testers** who provided valuable feedback

### 🏆 Special Thanks
- **Career counselors** who validated the analysis algorithms
- **HR professionals** who provided industry insights
- **Job seekers** who tested and improved the platform
- **Contributors** who helped enhance the codebase

---

## 📈 Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/yourusername/Smart-AI-Resume-Analyzer?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/Smart-AI-Resume-Analyzer?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/Smart-AI-Resume-Analyzer?style=social)

![GitHub issues](https://img.shields.io/github/issues/yourusername/Smart-AI-Resume-Analyzer)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/Smart-AI-Resume-Analyzer)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/Smart-AI-Resume-Analyzer)

![Lines of code](https://img.shields.io/tokei/lines/github/yourusername/Smart-AI-Resume-Analyzer)
![Code size](https://img.shields.io/github/languages/code-size/yourusername/Smart-AI-Resume-Analyzer)
![Repository size](https://img.shields.io/github/repo-size/yourusername/Smart-AI-Resume-Analyzer)

</div>

---

## 🔮 Roadmap

### 🚀 Upcoming Features

#### Q1 2024
- [ ] **Multi-language Support** - Spanish, French, German translations
- [ ] **LinkedIn Integration** - Import profile data automatically
- [ ] **Resume Templates** - 10+ new professional templates
- [ ] **Mobile App** - React Native mobile application

#### Q2 2024
- [ ] **Video Resume Analysis** - AI-powered video resume feedback
- [ ] **Interview Preparation** - Mock interview with AI
- [ ] **Salary Negotiation** - AI-powered salary recommendations
- [ ] **Team Collaboration** - Share and collaborate on resumes

#### Q3 2024
- [ ] **Enterprise Features** - White-label solution for companies
- [ ] **API Marketplace** - Public API for third-party integrations
- [ ] **Advanced Analytics** - Predictive success modeling
- [ ] **Career Coaching** - AI-powered career guidance

#### Q4 2024
- [ ] **Blockchain Verification** - Secure credential verification
- [ ] **AR/VR Integration** - Immersive resume presentation
- [ ] **Global Job Board** - Integrated job search platform
- [ ] **AI Mentorship** - Personalized career mentoring

---

<div align="center">

### 🌟 **Star this repository if you found it helpful!** 🌟

**Made with ❤️ by [Akul Yadav](https://github.com/Piratedpilot)**

*"Smart resumes for a smarter future"*

---

**© 2024 Resum.AI. All rights reserved.**

</div>
