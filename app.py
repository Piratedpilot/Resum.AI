"""
Resum.AI - Fixed HTML Rendering Issues (Using Streamlit Native Components)
"""
import time
from PIL import Image
from jobs.job_search import render_job_search
from datetime import datetime
from ui_components import (
    apply_modern_styles, hero_section, feature_card, about_section,
    page_header, render_analytics_section, render_activity_section,
    render_suggestions_section
)
from feedback.feedback import FeedbackManager
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx import Document
import io
import base64
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from dashboard.dashboard import DashboardManager
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS, get_courses_for_role, get_category_for_role
from config.job_roles import JOB_ROLES
from config.database import (
    get_database_connection, save_resume_data, save_analysis_data,
    init_database, verify_admin, log_admin_action, save_ai_analysis_data,
    get_ai_analysis_stats, reset_ai_analysis_stats, get_detailed_ai_analysis_stats
)
from utils.ai_resume_analyzer import AIResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.resume_analyzer import ResumeAnalyzer
import traceback
import plotly.express as px
import pandas as pd
import json
import streamlit as st
import datetime

# Set page config with modern theme
st.set_page_config(
    page_title="Resum.AI - Smart Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ModernResumeApp:
    def __init__(self):
        """Initialize the modern application"""
        # Initialize session state
        self.init_session_state()
        
        # Initialize components
        self.dashboard_manager = DashboardManager()
        self.analyzer = ResumeAnalyzer()
        self.ai_analyzer = AIResumeAnalyzer()
        self.builder = ResumeBuilder()
        self.job_roles = JOB_ROLES
        
        # Initialize database
        init_database()
        
        # Apply modern styling
        self.apply_modern_theme()

    def init_session_state(self):
        """Initialize all session state variables"""
        # Form data
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'personal_info': {
                    'full_name': '',
                    'email': '',
                    'phone': '',
                    'location': '',
                    'linkedin': '',
                    'portfolio': ''
                },
                'summary': '',
                'experiences': [],
                'education': [],
                'projects': [],
                'skills_categories': {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                }
            }

        # Navigation and user state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'default_user'
        if 'selected_role' not in st.session_state:
            st.session_state.selected_role = None
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = []
        if 'ai_analysis_stats' not in st.session_state:
            st.session_state.ai_analysis_stats = {
                'score_distribution': {},
                'total_analyses': 0,
                'average_score': 0
            }

    def apply_modern_theme(self):
        """Apply modern CSS theme"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
        
        /* Root Variables */
        :root {
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #10b981;
            --accent-color: #f59e0b;
            --background-dark: #0f172a;
            --surface-dark: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
        }
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Modern Card Component */
        .modern-card {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .modern-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
            border-color: var(--primary-color);
        }
        
        /* Hero Section */
        .hero-container {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
            border-radius: 24px;
            padding: 48px 32px;
            text-align: center;
            margin: 24px 0;
            border: 1px solid rgba(99, 102, 241, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .hero-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%236366f1' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.5;
        }
        
        .hero-title {
            font-family: 'Poppins', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 16px;
            position: relative;
            z-index: 1;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: 32px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            position: relative;
            z-index: 1;
        }
        
        /* Feature Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }
        
        .feature-item {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 16px;
            padding: 32px 24px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .feature-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .feature-item:hover::before {
            transform: scaleX(1);
        }
        
        .feature-item:hover {
            transform: translateY(-8px);
            border-color: var(--primary-color);
            box-shadow: 0 16px 64px rgba(99, 102, 241, 0.2);
        }
        
        .feature-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px;
            font-size: 24px;
            color: white;
        }
        
        .feature-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 16px;
        }
        
        .feature-description {
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        /* Modern Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 500;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
        }
        
        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 24px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(16, 185, 129, 0.1));
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            border: 1px solid rgba(99, 102, 241, 0.2);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(99, 102, 241, 0.2);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Upload Area */
        .upload-area {
            border: 2px dashed rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 48px 24px;
            text-align: center;
            background: rgba(30, 41, 59, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .upload-area:hover {
            border-color: var(--primary-color);
            background: rgba(99, 102, 241, 0.05);
        }
        
        .upload-icon {
            font-size: 48px;
            color: var(--primary-color);
            margin-bottom: 16px;
        }
        
        /* Analysis Results */
        .analysis-section {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 16px;
            padding: 24px;
            margin: 16px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .section-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 16px;
            color: white;
        }
        
        .section-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        /* Score Badges */
        .score-badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }
        
        .score-excellent {
            background: linear-gradient(135deg, #10b981, #34d399);
            color: white;
        }
        
        .score-good {
            background: linear-gradient(135deg, #f59e0b, #fbbf24);
            color: white;
        }
        
        .score-needs-improvement {
            background: linear-gradient(135deg, #ef4444, #f87171);
            color: white;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Animation Classes */
        .fade-in {
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .slide-up {
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
        """, unsafe_allow_html=True)

    def render_modern_sidebar(self):
        """Render modern sidebar navigation"""
        with st.sidebar:
            # Logo and branding
            st.markdown("""
            <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
                <div style="font-size: 2rem; margin-bottom: 8px;">🚀</div>
                <h2 style="color: white; margin: 0; font-family: 'Poppins', sans-serif;">Resum.AI</h2>
                <p style="color: #94a3b8; font-size: 0.9rem; margin: 4px 0 0 0;">Smart Resume Intelligence</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation menu
            pages = {
                "🏠 Home": "home",
                "🔍 Analyzer": "analyzer", 
                "📝 Builder": "builder",
                "📊 Dashboard": "dashboard",
                "🎯 Job Search": "job_search",
                "💬 Feedback": "feedback",
                "ℹ️ About": "about"
            }
            
            for page_name, page_key in pages.items():
                is_active = st.session_state.current_page == page_key
                button_style = "primary" if is_active else "secondary"
                
                if st.button(page_name, key=f"nav_{page_key}", use_container_width=True, type=button_style):
                    st.session_state.current_page = page_key
                    st.rerun()
            
            st.markdown("---")
            
            # Quick stats
            st.markdown("""
            <div class="modern-card" style="margin-top: 20px;">
                <h4 style="color: white; margin-bottom: 16px;">Quick Stats</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #94a3b8;">Analyses:</span>
                    <span style="color: #10b981; font-weight: 600;">1,234</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #94a3b8;">Avg Score:</span>
                    <span style="color: #6366f1; font-weight: 600;">78/100</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">Success Rate:</span>
                    <span style="color: #f59e0b; font-weight: 600;">92%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Admin section
            self.render_admin_section()

    def render_admin_section(self):
        """Render admin login/logout section"""
        st.markdown("---")
        
        if st.session_state.get('is_admin', False):
            st.success(f"👤 Admin: {st.session_state.get('current_admin_email', 'Unknown')}")
            if st.button("🚪 Logout", use_container_width=True):
                try:
                    log_admin_action(st.session_state.get('current_admin_email'), "logout")
                    st.session_state.is_admin = False
                    st.session_state.current_admin_email = None
                    st.success("Logged out successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error during logout: {str(e)}")
        else:
            with st.expander("👤 Admin Access"):
                admin_email = st.text_input("Email", key="admin_email")
                admin_password = st.text_input("Password", type="password", key="admin_password")
                if st.button("🔐 Login", use_container_width=True):
                    try:
                        if verify_admin(admin_email, admin_password):
                            st.session_state.is_admin = True
                            st.session_state.current_admin_email = admin_email
                            log_admin_action(admin_email, "login")
                            st.success("Welcome, Admin!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Login error: {str(e)}")

    def render_home_page(self):
        """Render modern home page"""
        # Hero section
        st.markdown("""
        <div class="hero-container fade-in">
            <h1 class="hero-title">Transform Your Career with AI</h1>
            <p class="hero-subtitle">
                Unlock your potential with intelligent resume analysis, professional building tools, 
                and personalized career insights powered by advanced AI technology.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # CTA buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
                    st.session_state.current_page = "analyzer"
                    st.rerun()
            with subcol2:
                if st.button("📝 Build Resume", use_container_width=True):
                    st.session_state.current_page = "builder"
                    st.rerun()
        
        # Features grid
        st.markdown('<div class="feature-grid slide-up">', unsafe_allow_html=True)
        
        features = [
            {
                "icon": "🤖",
                "title": "AI-Powered Analysis",
                "description": "Advanced machine learning algorithms analyze your resume for optimal performance and ATS compatibility."
            },
            {
                "icon": "📊",
                "title": "Detailed Insights",
                "description": "Get comprehensive feedback with actionable recommendations to improve your resume's effectiveness."
            },
            {
                "icon": "🎯",
                "title": "Job Matching",
                "description": "Tailored analysis based on specific job roles and industry requirements for better targeting."
            },
            {
                "icon": "📈",
                "title": "Performance Tracking",
                "description": "Monitor your progress with detailed analytics and track improvements over time."
            },
            {
                "icon": "🔧",
                "title": "Smart Builder",
                "description": "Create professional resumes with intelligent suggestions and modern templates."
            },
            {
                "icon": "🌟",
                "title": "Career Guidance",
                "description": "Receive personalized career advice and course recommendations for skill development."
            }
        ]
        
        for i in range(0, len(features), 3):
            cols = st.columns(3)
            for j, feature in enumerate(features[i:i+3]):
                with cols[j]:
                    st.markdown(f"""
                    <div class="feature-item">
                        <div class="feature-icon">{feature['icon']}</div>
                        <h3 class="feature-title">{feature['title']}</h3>
                        <p class="feature-description">{feature['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats section
        st.markdown("""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">50K+</div>
                <div class="stat-label">Resumes Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">95%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">24/7</div>
                <div class="stat-label">AI Availability</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">4.9★</div>
                <div class="stat-label">User Rating</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_analyzer_page(self):
        """Render modern analyzer page"""
        st.markdown("""
        <div class="modern-card">
            <div class="section-header">
                <div class="section-icon">🔍</div>
                <h2 class="section-title">Resume Analyzer</h2>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: 24px;">
                Upload your resume and get instant AI-powered feedback with detailed insights and recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analyzer tabs
        tab1, tab2 = st.tabs(["🎯 Standard Analysis", "🤖 AI Analysis"])
        
        with tab1:
            self.render_standard_analyzer()
            
        with tab2:
            self.render_ai_analyzer()

    def render_standard_analyzer(self):
        """Render standard analyzer interface"""
        # Job role selection
        col1, col2 = st.columns(2)
        with col1:
            categories = list(self.job_roles.keys())
            selected_category = st.selectbox("📂 Job Category", categories, key="std_category")
        
        with col2:
            roles = list(self.job_roles[selected_category].keys())
            selected_role = st.selectbox("🎯 Specific Role", roles, key="std_role")
        
        # Role info card
        role_info = self.job_roles[selected_category][selected_role]
        st.markdown(f"""
        <div class="modern-card">
            <h4 style="color: var(--primary-color); margin-bottom: 12px;">{selected_role}</h4>
            <p style="color: var(--text-secondary); margin-bottom: 16px;">{role_info['description']}</p>
            <div style="margin-bottom: 8px;">
                <strong style="color: var(--text-primary);">Required Skills:</strong>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                {' '.join([f'<span class="score-badge" style="background: rgba(99, 102, 241, 0.2); color: var(--primary-color);">{skill}</span>' for skill in role_info['required_skills']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # File upload
        uploaded_file = st.file_uploader(
            "📄 Upload Your Resume",
            type=['pdf', 'docx'],
            key="std_file",
            help="Supported formats: PDF, DOCX (Max 10MB)"
        )
        
        if uploaded_file:
            # File info
            st.markdown(f"""
            <div class="modern-card" style="background: rgba(16, 185, 129, 0.1); border-color: var(--secondary-color);">
                <div style="display: flex; align-items: center;">
                    <div style="margin-right: 16px; font-size: 24px;">📄</div>
                    <div>
                        <div style="color: var(--text-primary); font-weight: 600;">{uploaded_file.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">
                            {round(uploaded_file.size / 1024, 1)} KB • Ready for analysis
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Analyze button
            if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
                self.perform_standard_analysis(uploaded_file, selected_role, role_info)
        else:
            # Upload prompt
            st.markdown("""
            <div class="upload-area">
                <div class="upload-icon">📤</div>
                <h3 style="color: var(--text-primary); margin-bottom: 8px;">Upload Your Resume</h3>
                <p style="color: var(--text-secondary);">Drag and drop your resume file here or click to browse</p>
                <p style="color: var(--text-muted); font-size: 0.9rem;">Supports PDF and DOCX formats</p>
            </div>
            """, unsafe_allow_html=True)

    def render_ai_analyzer(self):
        """Render AI analyzer interface"""
        st.markdown("""
        <div class="modern-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(16, 185, 129, 0.1));">
            <div style="text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px;">🤖</div>
                <h3 style="color: var(--text-primary); margin-bottom: 12px;">AI-Powered Analysis</h3>
                <p style="color: var(--text-secondary);">
                    Get advanced insights using Google Gemini AI with personalized recommendations 
                    and detailed feedback tailored to your career goals.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI model selection and job description option
        col1, col2 = st.columns(2)
        with col1:
            ai_model = st.selectbox("🧠 AI Model", ["Google Gemini"], help="Select AI model for analysis")
        
        with col2:
            use_custom_job = st.checkbox("📋 Use Custom Job Description", help="Provide specific job description for targeted analysis")
        
        # Custom job description
        custom_job_desc = ""
        if use_custom_job:
            custom_job_desc = st.text_area(
                "📝 Job Description",
                height=150,
                placeholder="Paste the complete job description here for more accurate analysis...",
                help="The more detailed the job description, the better the AI analysis"
            )
            
            if custom_job_desc:
                st.markdown("""
                <div class="modern-card" style="background: rgba(16, 185, 129, 0.1); border-color: var(--secondary-color);">
                    <div style="display: flex; align-items: center;">
                        <div style="margin-right: 12px;">✅</div>
                        <div style="color: var(--secondary-color); font-weight: 500;">
                            Custom job description provided - analysis will be highly targeted!
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Job role selection for AI
        col1, col2 = st.columns(2)
        with col1:
            categories = list(self.job_roles.keys())
            selected_category = st.selectbox("📂 Job Category", categories, key="ai_category")
        
        with col2:
            roles = list(self.job_roles[selected_category].keys())
            selected_role = st.selectbox("🎯 Target Role", roles, key="ai_role")
        
        # File upload for AI
        uploaded_file = st.file_uploader(
            "📄 Upload Resume for AI Analysis",
            type=['pdf', 'docx'],
            key="ai_file",
            help="Upload your resume for advanced AI analysis"
        )
        
        if uploaded_file:
            # File preview
            st.markdown(f"""
            <div class="modern-card" style="background: rgba(99, 102, 241, 0.1); border-color: var(--primary-color);">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <div style="margin-right: 16px; font-size: 24px;">🤖</div>
                        <div>
                            <div style="color: var(--text-primary); font-weight: 600;">{uploaded_file.name}</div>
                            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                                Ready for AI analysis with {ai_model}
                            </div>
                        </div>
                    </div>
                    <div class="score-badge" style="background: var(--primary-color);">AI Ready</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Analysis button
            if st.button("🤖 Analyze with AI", type="primary", use_container_width=True):
                self.perform_ai_analysis(uploaded_file, selected_role, custom_job_desc, use_custom_job)

    def perform_standard_analysis(self, uploaded_file, selected_role, role_info):
        """Perform standard resume analysis"""
        with st.spinner("🔍 Analyzing your resume..."):
            progress_bar = st.progress(0)
            
            try:
                # Extract text
                progress_bar.progress(25)
                if uploaded_file.type == "application/pdf":
                    text = self.analyzer.extract_text_from_pdf(uploaded_file)
                else:
                    text = self.analyzer.extract_text_from_docx(uploaded_file)
                
                progress_bar.progress(50)
                
                # Analyze
                analysis = self.analyzer.analyze_resume({'raw_text': text}, role_info)
                progress_bar.progress(100)
                
                if 'error' not in analysis:
                    st.success("✅ Analysis Complete!")
                    st.balloons()
                    self.display_standard_results(analysis, selected_role)
                else:
                    st.error(f"❌ Analysis failed: {analysis['error']}")
                    
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

    def perform_ai_analysis(self, uploaded_file, selected_role, custom_job_desc, use_custom_job):
        """Perform AI-powered resume analysis"""
        with st.spinner("🤖 AI is analyzing your resume..."):
            progress_bar = st.progress(0)
            
            try:
                # Extract text
                progress_bar.progress(20)
                if uploaded_file.type == "application/pdf":
                    text = self.ai_analyzer.extract_text_from_pdf(uploaded_file)
                else:
                    text = self.ai_analyzer.extract_text_from_docx(uploaded_file)
                
                progress_bar.progress(40)
                
                # AI Analysis
                if use_custom_job and custom_job_desc:
                    analysis = self.ai_analyzer.analyze_resume_with_gemini(
                        text, job_role=selected_role, job_description=custom_job_desc
                    )
                else:
                    analysis = self.ai_analyzer.analyze_resume_with_gemini(
                        text, job_role=selected_role
                    )
                
                progress_bar.progress(80)
                
                # Save results
                if analysis and "error" not in analysis:
                    save_ai_analysis_data(None, {
                        "model_used": "Google Gemini",
                        "resume_score": analysis.get("resume_score", 0),
                        "job_role": selected_role
                    })
                
                progress_bar.progress(100)
                
                if analysis and "error" not in analysis:
                    st.success("✅ AI Analysis Complete!")
                    st.snow()
                    self.display_ai_results(analysis, selected_role, use_custom_job)
                else:
                    st.error(f"❌ AI Analysis failed: {analysis.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Error during AI analysis: {str(e)}")

    def display_standard_results(self, analysis, role):
        """Display standard analysis results"""
        # Score overview
        col1, col2, col3, col4 = st.columns(4)
        
        scores = [
            ("ATS Score", analysis.get('ats_score', 0), "🎯"),
            ("Keywords", analysis.get('keyword_match', {}).get('score', 0), "🔑"),
            ("Format", analysis.get('format_score', 0), "📄"),
            ("Sections", analysis.get('section_score', 0), "📋")
        ]
        
        for i, (label, score, icon) in enumerate(scores):
            with [col1, col2, col3, col4][i]:
                self.render_score_card(label, score, icon)
        
        # Detailed feedback
        col1, col2 = st.columns(2)
        
        with col1:
            # Strengths
            st.markdown("""
            <div class="analysis-section">
                <div class="section-header">
                    <div class="section-icon">✅</div>
                    <h3 class="section-title">Strengths</h3>
                </div>
            """, unsafe_allow_html=True)
            
            strengths = analysis.get('strengths', ['Professional formatting', 'Clear structure', 'Relevant experience'])
            for strength in strengths:
                st.markdown(f"• {strength}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Improvements
            st.markdown("""
            <div class="analysis-section">
                <div class="section-header">
                    <div class="section-icon">🎯</div>
                    <h3 class="section-title">Improvements</h3>
                </div>
            """, unsafe_allow_html=True)
            
            improvements = analysis.get('suggestions', ['Add more keywords', 'Quantify achievements', 'Update skills section'])
            for improvement in improvements:
                st.markdown(f"• {improvement}")
            
            st.markdown("</div>", unsafe_allow_html=True)

    def display_ai_results(self, analysis, role, used_custom_job):
        """Display AI analysis results"""
        # Score gauges
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_gauge_chart("Resume Score", analysis.get('resume_score', 0))
        
        with col2:
            self.render_gauge_chart("ATS Score", analysis.get('ats_score', 0))
        
        # Custom job match score if applicable
        if used_custom_job and analysis.get('job_match_score'):
            st.markdown("### 🎯 Job Match Analysis")
            self.render_gauge_chart("Job Match Score", analysis.get('job_match_score', 0))
        
        # Full AI analysis
        st.markdown("""
        <div class="analysis-section">
            <div class="section-header">
                <div class="section-icon">🤖</div>
                <h3 class="section-title">AI Analysis Report</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Format and display the AI response
        full_analysis = analysis.get('analysis', '')
        if full_analysis:
            # Apply formatting to the analysis
            formatted_analysis = self.format_ai_analysis(full_analysis)
            st.markdown(formatted_analysis, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download PDF report
        if st.button("📊 Download PDF Report", use_container_width=True):
            pdf_buffer = self.ai_analyzer.generate_pdf_report(
                analysis_result=analysis,
                candidate_name="User",
                job_role=role
            )
            
            if pdf_buffer:
                st.download_button(
                    label="📥 Download Report",
                    data=pdf_buffer,
                    file_name=f"ai_resume_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )

    def render_score_card(self, title, score, icon):
        """Render a score card component"""
        # Determine color based on score
        if score >= 80:
            color = "var(--success-color)"
            status = "Excellent"
        elif score >= 60:
            color = "var(--warning-color)"
            status = "Good"
        else:
            color = "var(--error-color)"
            status = "Needs Work"
        
        st.markdown(f"""
        <div class="modern-card" style="text-align: center;">
            <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
            <div style="font-size: 2rem; font-weight: 700; color: {color}; margin-bottom: 4px;">{score}</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 8px;">{title}</div>
            <div class="score-badge" style="background: {color}; color: white; font-size: 0.8rem;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

    def render_gauge_chart(self, title, score):
        """Render a gauge chart for scores"""
        import plotly.graph_objects as go
        
        # Determine color
        color = "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 16, 'color': 'white'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "rgba(255,255,255,0.3)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.2)'},
                    {'range': [40, 60], 'color': 'rgba(245, 158, 11, 0.2)'},
                    {'range': [60, 80], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 60
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=250,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def format_ai_analysis(self, analysis_text):
        """Format AI analysis text with better styling"""
        # Replace section headers with styled versions
        sections = {
            "## Overall Assessment": "🎯 Overall Assessment",
            "## Professional Profile Analysis": "👤 Professional Profile Analysis", 
            "## Skills Analysis": "🛠️ Skills Analysis",
            "## Experience Analysis": "💼 Experience Analysis",
            "## Education Analysis": "🎓 Education Analysis",
            "## Key Strengths": "✅ Key Strengths",
            "## Areas for Improvement": "🎯 Areas for Improvement",
            "## ATS Optimization Assessment": "🤖 ATS Optimization Assessment",
            "## Recommended Courses": "📚 Recommended Courses",
            "## Resume Score": "⭐ Resume Score",
            "## Role Alignment Analysis": "🎯 Role Alignment Analysis",
            "## Job Match Analysis": "🤝 Job Match Analysis"
        }
        
        formatted_text = analysis_text
        for old_header, new_header in sections.items():
            if old_header in formatted_text:
                formatted_text = formatted_text.replace(
                    old_header,
                    f"""
                    <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                                color: white; padding: 12px 16px; border-radius: 8px; margin: 20px 0 10px 0; 
                                font-weight: 600;">
                        {new_header}
                    </div>
                    """
                )
        
        return formatted_text

    def render_builder_page(self):
        """Render resume builder page"""
        st.markdown("""
        <div class="modern-card">
            <div class="section-header">
                <div class="section-icon">📝</div>
                <h2 class="section-title">Resume Builder</h2>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: 24px;">
                Create a professional resume with our intelligent builder that provides real-time suggestions and modern templates.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Template selection
        st.markdown("### 🎨 Choose Template")
        templates = ["Modern", "Professional", "Minimal", "Creative"]
        selected_template = st.selectbox("Template Style", templates)
        
        # Template preview
        st.markdown(f"""
        <div class="modern-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(16, 185, 129, 0.1));">
            <div style="text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px;">📄</div>
                <h4 style="color: var(--text-primary);">Selected: {selected_template} Template</h4>
                <p style="color: var(--text-secondary);">Professional layout optimized for ATS systems</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Form sections
        self.render_builder_form()

    def render_builder_form(self):
        """Render the resume builder form"""
        # Personal Information
        st.markdown("### 👤 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", value=st.session_state.form_data['personal_info']['full_name'])
            email = st.text_input("Email *", value=st.session_state.form_data['personal_info']['email'])
            phone = st.text_input("Phone", value=st.session_state.form_data['personal_info']['phone'])
        
        with col2:
            location = st.text_input("Location", value=st.session_state.form_data['personal_info']['location'])
            linkedin = st.text_input("LinkedIn URL", value=st.session_state.form_data['personal_info']['linkedin'])
            portfolio = st.text_input("Portfolio Website", value=st.session_state.form_data['personal_info']['portfolio'])
        
        # Update session state
        st.session_state.form_data['personal_info'].update({
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'location': location,
            'linkedin': linkedin,
            'portfolio': portfolio
        })
        
        # Professional Summary
        st.markdown("### 📝 Professional Summary")
        summary = st.text_area(
            "Write a compelling summary",
            value=st.session_state.form_data.get('summary', ''),
            height=120,
            help="2-3 sentences highlighting your key qualifications and career objectives"
        )
        st.session_state.form_data['summary'] = summary
         # Skills Section
        st.markdown("### 🛠️ Skills")
        
        # Initialize skills if not exists
        if 'skills_categories' not in st.session_state.form_data:
            st.session_state.form_data['skills_categories'] = {
                'technical': [],
                'soft': [],
                'languages': [],
                'tools': []
            }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Technical Skills
            st.markdown("**Technical Skills**")
            technical_skills = st.text_area(
                "Enter technical skills (one per line)",
                value='\n'.join(st.session_state.form_data['skills_categories']['technical']),
                height=100,
                key="technical_skills",
                help="e.g., Python, JavaScript, React, SQL"
            )
            st.session_state.form_data['skills_categories']['technical'] = [skill.strip() for skill in technical_skills.split('\n') if skill.strip()]
        
        # Programming Languages
        st.markdown("**Programming Languages**")
        languages = st.text_area(
            "Enter programming languages (one per line)",
            value='\n'.join(st.session_state.form_data['skills_categories']['languages']),
            height=80,
            key="languages",
            help="e.g., Python, Java, C++, JavaScript"
        )
        st.session_state.form_data['skills_categories']['languages'] = [lang.strip() for lang in languages.split('\n') if lang.strip()]
    
        with col2:
            # Soft Skills
            st.markdown("**Soft Skills**")
            soft_skills = st.text_area(
                "Enter soft skills (one per line)",
                value='\n'.join(st.session_state.form_data['skills_categories']['soft']),
                height=100,
                key="soft_skills",
                help="e.g., Leadership, Communication, Problem Solving"
            )
            st.session_state.form_data['skills_categories']['soft'] = [skill.strip() for skill in soft_skills.split('\n') if skill.strip()]
        
            # Tools & Technologies
            st.markdown("**Tools & Technologies**")
            tools = st.text_area(
                "Enter tools and technologies (one per line)",
                value='\n'.join(st.session_state.form_data['skills_categories']['tools']),
                height=80,
                key="tools",
                help="e.g., Git, Docker, AWS, Figma"
            )
            st.session_state.form_data['skills_categories']['tools'] = [tool.strip() for tool in tools.split('\n') if tool.strip()]
    
        # Experience Section
        st.markdown("### 💼 Work Experience")
    
        # Initialize experiences if not exists
        if 'experiences' not in st.session_state.form_data:
            st.session_state.form_data['experiences'] = []
    
        # Add new experience button
        if st.button("➕ Add Experience", key="add_exp"):
            st.session_state.form_data['experiences'].append({
                'title': '',
                'company': '',
                'location': '',
                'start_date': '',
                'end_date': '',
                'current': False,
                'description': ''
            })
            st.rerun()
    
        # Display existing experiences
        for i, exp in enumerate(st.session_state.form_data['experiences']):
            with st.expander(f"Experience {i+1}: {exp.get('title', 'New Position')}", expanded=True):
                col1, col2 = st.columns(2)
            
                with col1:
                    exp['title'] = st.text_input(f"Job Title", value=exp.get('title', ''), key=f"exp_title_{i}")
                    exp['company'] = st.text_input(f"Company", value=exp.get('company', ''), key=f"exp_company_{i}")
                    exp['location'] = st.text_input(f"Location", value=exp.get('location', ''), key=f"exp_location_{i}")
            
                with col2:
                    exp['start_date'] = st.text_input(f"Start Date", value=exp.get('start_date', ''), key=f"exp_start_{i}", help="e.g., Jan 2023")
                    exp['current'] = st.checkbox(f"Currently working here", value=exp.get('current', False), key=f"exp_current_{i}")
                    if not exp['current']:
                        exp['end_date'] = st.text_input(f"End Date", value=exp.get('end_date', ''), key=f"exp_end_{i}", help="e.g., Dec 2023")
                    else:
                        exp['end_date'] = 'Present'
            
                exp['description'] = st.text_area(
                    f"Job Description & Achievements",
                    value=exp.get('description', ''),
                    height=120,
                    key=f"exp_desc_{i}",
                    help="Describe your responsibilities and achievements. Use bullet points for better readability."
                )
            
                if st.button(f"🗑️ Remove Experience {i+1}", key=f"remove_exp_{i}"):
                    st.session_state.form_data['experiences'].pop(i)
                    st.rerun()
    
        # Education Section
        st.markdown("### 🎓 Education")
    
        # Initialize education if not exists
        if 'education' not in st.session_state.form_data:
            st.session_state.form_data['education'] = []
    
        # Add new education button
        if st.button("➕ Add Education", key="add_edu"):
            st.session_state.form_data['education'].append({
                'degree': '',
                'institution': '',
                'location': '',
                'graduation_date': '',
                'gpa': '',
                'relevant_courses': ''
            })
            st.rerun()
    
        # Display existing education
        for i, edu in enumerate(st.session_state.form_data['education']):
            with st.expander(f"Education {i+1}: {edu.get('degree', 'New Degree')}", expanded=True):
                col1, col2 = st.columns(2)
            
                with col1:
                    edu['degree'] = st.text_input(f"Degree", value=edu.get('degree', ''), key=f"edu_degree_{i}", help="e.g., Bachelor of Science in Computer Science")
                    edu['institution'] = st.text_input(f"Institution", value=edu.get('institution', ''), key=f"edu_institution_{i}")
                    edu['location'] = st.text_input(f"Location", value=edu.get('location', ''), key=f"edu_location_{i}")
            
                with col2:
                    edu['graduation_date'] = st.text_input(f"Graduation Date", value=edu.get('graduation_date', ''), key=f"edu_grad_{i}", help="e.g., May 2024")
                    edu['gpa'] = st.text_input(f"GPA (Optional)", value=edu.get('gpa', ''), key=f"edu_gpa_{i}", help="e.g., 3.8/4.0")
                    edu['relevant_courses'] = st.text_input(f"Relevant Courses", value=edu.get('relevant_courses', ''), key=f"edu_courses_{i}", help="Comma-separated list")
            
                if st.button(f"🗑️ Remove Education {i+1}", key=f"remove_edu_{i}"):
                    st.session_state.form_data['education'].pop(i)
                    st.rerun()
    
        # Projects Section
        st.markdown("### 🚀 Projects")
    
        # Initialize projects if not exists
        if 'projects' not in st.session_state.form_data:
            st.session_state.form_data['projects'] = []
    
        # Add new project button
        if st.button("➕ Add Project", key="add_project"):
            st.session_state.form_data['projects'].append({
                'name': '',
                'technologies': '',
                'description': '',
                'github_url': '',
                'live_url': '',
                'duration': ''
            })
            st.rerun()
    
        # Display existing projects
        for i, project in enumerate(st.session_state.form_data['projects']):
            with st.expander(f"Project {i+1}: {project.get('name', 'New Project')}", expanded=True):
                col1, col2 = st.columns(2)
            
                with col1:
                    project['name'] = st.text_input(f"Project Name", value=project.get('name', ''), key=f"proj_name_{i}")
                    project['technologies'] = st.text_input(f"Technologies Used", value=project.get('technologies', ''), key=f"proj_tech_{i}", help="e.g., React, Node.js, MongoDB")
                    project['duration'] = st.text_input(f"Duration", value=project.get('duration', ''), key=f"proj_duration_{i}", help="e.g., Jan 2024 - Mar 2024")
            
                with col2:
                    project['github_url'] = st.text_input(f"GitHub URL", value=project.get('github_url', ''), key=f"proj_github_{i}")
                    project['live_url'] = st.text_input(f"Live Demo URL", value=project.get('live_url', ''), key=f"proj_live_{i}")
            
                project['description'] = st.text_area(
                    f"Project Description",
                    value=project.get('description', ''),
                    height=100,
                    key=f"proj_desc_{i}",
                    help="Describe the project, your role, and key achievements"
                )
            
                if st.button(f"🗑️ Remove Project {i+1}", key=f"remove_proj_{i}"):
                    st.session_state.form_data['projects'].pop(i)
                    st.rerun()
    
        # Co-curricular Activities Section
        st.markdown("### 🏆 Co-curricular Activities")
    
        # Initialize activities if not exists
        if 'activities' not in st.session_state.form_data:
            st.session_state.form_data['activities'] = []
    
        # Add new activity button
        if st.button("➕ Add Activity", key="add_activity"):
            st.session_state.form_data['activities'].append({
                'title': '',
                'organization': '',
                'role': '',
                'duration': '',
                'description': ''
            })
            st.rerun()
    
        # Display existing activities
        for i, activity in enumerate(st.session_state.form_data['activities']):
            with st.expander(f"Activity {i+1}: {activity.get('title', 'New Activity')}", expanded=True):
                col1, col2 = st.columns(2)
            
                with col1:
                    activity['title'] = st.text_input(f"Activity/Event Title", value=activity.get('title', ''), key=f"act_title_{i}")
                    activity['organization'] = st.text_input(f"Organization", value=activity.get('organization', ''), key=f"act_org_{i}")
            
                with col2:
                    activity['role'] = st.text_input(f"Your Role", value=activity.get('role', ''), key=f"act_role_{i}", help="e.g., Team Leader, Participant, Organizer")
                    activity['duration'] = st.text_input(f"Duration", value=activity.get('duration', ''), key=f"act_duration_{i}", help="e.g., Jan 2024 - Mar 2024")
            
                activity['description'] = st.text_area(
                    f"Description & Achievements",
                    value=activity.get('description', ''),
                    height=100,
                    key=f"act_desc_{i}",
                    help="Describe your involvement and any achievements or recognition"
                )
            
                if st.button(f"🗑️ Remove Activity {i+1}", key=f"remove_act_{i}"):
                    st.session_state.form_data['activities'].pop(i)
                    st.rerun()
    
        # Generate Resume Button
        if st.button("🚀 Generate Resume", type="primary", use_container_width=True):
            if full_name and email:
                with st.spinner("🔨 Building your resume..."):
                    try:
                        resume_data = {
                            "personal_info": st.session_state.form_data['personal_info'],
                            "summary": summary,
                            "experience": st.session_state.form_data.get('experiences', []),
                            "education": st.session_state.form_data.get('education', []),
                            "projects": st.session_state.form_data.get('projects', []),
                            "skills": st.session_state.form_data.get('skills_categories', {}),
                            "template": "Modern"
                        }
                        
                        resume_buffer = self.builder.generate_resume(resume_data)
                        if resume_buffer:
                            st.success("✅ Resume generated successfully!")
                            st.balloons()
                            
                            st.download_button(
                                label="📥 Download Resume",
                                data=resume_buffer,
                                file_name=f"{full_name.replace(' ', '_')}_resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                        else:
                            st.error("❌ Failed to generate resume")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.error("⚠️ Please fill in required fields (Name and Email)")

    def render_dashboard_page(self):
        """Render dashboard page"""
        self.dashboard_manager.render_dashboard()

    def render_job_search_page(self):
        """Render job search page"""
        render_job_search()

    def render_feedback_page(self):
        """Render feedback page"""
        feedback_manager = FeedbackManager()
        
        st.markdown("""
        <div class="modern-card">
            <div class="section-header">
                <div class="section-icon">💬</div>
                <h2 class="section-title">Feedback & Suggestions</h2>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: 24px;">
                Help us improve Resum.AI by sharing your thoughts and suggestions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📝 Submit Feedback", "📊 Feedback Stats"])
        
        with tab1:
            feedback_manager.render_feedback_form()
        
        with tab2:
            feedback_manager.render_feedback_stats()

    def render_about_page(self):
        """Render about page using Streamlit native components"""
        # Hero section
        st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">About Resum.AI</h1>
            <p class="hero-subtitle">
                Empowering careers through intelligent resume analysis and AI-driven insights
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Developer section using native Streamlit components
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Profile section
            st.markdown("""
            <div style="text-align: center; background: rgba(30, 41, 59, 0.8); padding: 40px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #10b981); 
                            margin: 0 auto 24px; display: flex; align-items: center; justify-content: center; font-size: 48px;">
                    👨‍💻
                </div>
                <h3 style="color: #f8fafc; margin-bottom: 8px;">Akul Yadav</h3>
                <p style="color: #6366f1; margin-bottom: 16px;">Full Stack Developer & AI Enthusiast</p>
                <p style="color: #cbd5e1; line-height: 1.6;">
                    Passionate about solving Data Structures & Algorithms problems and constantly improving my problem-solving skills. I occasionally explore Web Development, 📷 Hobbyist photographer who loves capturing moments when not debugging code.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Social links using Streamlit buttons
            st.markdown("### 🔗 Connect with me")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("🐙 GitHub", use_container_width=True):
                    st.markdown("[Visit GitHub](https://github.com/Piratedpilot)")
            
            with col_b:
                if st.button("💼 LinkedIn", use_container_width=True):
                    st.markdown("[Visit LinkedIn](https://linkedin.com/in/akul-yadav-1832b0258/)")
            
            with col_c:
                if st.button("📧 Email", use_container_width=True):
                    st.markdown("[Send Email](mailto:akulyadav1959@gmail.com)")
        
        # Mission and vision
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="modern-card">
                <div class="section-header">
                    <div class="section-icon">🎯</div>
                    <h3 class="section-title">Our Mission</h3>
                </div>
                <p style="color: var(--text-secondary); line-height: 1.6;">
                    To democratize career advancement by providing intelligent, accessible tools 
                    that help job seekers optimize their resumes and unlock their potential in 
                    today's competitive job market.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="modern-card">
                <div class="section-header">
                    <div class="section-icon">🚀</div>
                    <h3 class="section-title">Our Vision</h3>
                </div>
                <p style="color: var(--text-secondary); line-height: 1.6;">
                    To become the leading AI-powered career platform that transforms how people 
                    present themselves professionally, making career success achievable for everyone 
                    through intelligent technology.
                </p>
            </div>
            """, unsafe_allow_html=True)

    def render_footer(self):
        """Render footer using Streamlit native components"""
        st.markdown("---")
        
        # Use columns for layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # GitHub star button
            if st.button("⭐ Star this project on GitHub", use_container_width=True, type="primary"):
                st.markdown("[Visit GitHub Repository](https://github.com/Akul-Yadav/Smart-AI-Resume-Analyzer)")
            
            # Footer text using native Streamlit
            st.markdown("---")
            
            st.markdown("""
<div style="text-align: center; font-size: 0.85rem; margin-top: 10px;">
    <p style="color: #cbd5e1;">
        Powered by <strong>Streamlit</strong> and <strong>Google Gemini AI</strong>
    </p>
    <p style="color: #cbd5e1;">
        Developed with ❤️ by <strong>Akul Yadav</strong>
    </p>
    <p style="color: #94a3b8; font-style: italic;">
        "Smart resumes for a smarter future"
    </p>
</div>
""", unsafe_allow_html=True)



    def main(self):
        """Main application entry point"""
        # Render sidebar
        self.render_modern_sidebar()
        
        # Route to appropriate page
        current_page = st.session_state.get('current_page', 'home')
        
        if current_page == 'home':
            self.render_home_page()
        elif current_page == 'analyzer':
            self.render_analyzer_page()
        elif current_page == 'builder':
            self.render_builder_page()
        elif current_page == 'dashboard':
            self.render_dashboard_page()
        elif current_page == 'job_search':
            self.render_job_search_page()
        elif current_page == 'feedback':
            self.render_feedback_page()
        elif current_page == 'about':
            self.render_about_page()
        else:
            self.render_home_page()
        
        # Render footer
        self.render_footer()

if __name__ == "__main__":
    app = ModernResumeApp()
    app.main()
