"""
═══════════════════════════════════════════════════════════════════════════════
SKILLLENS AI — Streamlit Integration Guide
Premium UI Components & Animations

This file demonstrates how to integrate the SkillLens AI premium UI
into your Streamlit application. Copy the relevant sections into your app.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION - Must be first Streamlit command
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SkillLens AI | ATS Resume Scanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS INJECTION - Load from file or embed directly
# ═══════════════════════════════════════════════════════════════════════════════

def load_css():
    """Load premium CSS styles."""
    # Option 1: Load from file
    # with open("E:\AI_Lab\Frontend\assets\css\styles.css", "r") as f:
    #     css = f.read()
    # st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Option 2: Inline CSS (subset for quick start)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --sl-bg-primary: #0a0a0f;
            --sl-bg-secondary: #12121a;
            --sl-bg-tertiary: #1a1a26;
            --sl-bg-elevated: #1e1e2e;
            --sl-bg-card: rgba(26, 26, 38, 0.7);
            --sl-bg-glass: rgba(26, 26, 38, 0.4);
            --sl-accent-primary: #8b5cf6;
            --sl-accent-secondary: #a78bfa;
            --sl-accent-glow: rgba(139, 92, 246, 0.4);
            --sl-accent-subtle: rgba(139, 92, 246, 0.1);
            --sl-cyan-primary: #06b6d4;
            --sl-gradient-primary: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
            --sl-text-primary: #f8fafc;
            --sl-text-secondary: #94a3b8;
            --sl-text-tertiary: #64748b;
            --sl-success: #22c55e;
            --sl-warning: #f59e0b;
            --sl-error: #ef4444;
            --sl-font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --sl-radius-xl: 1rem;
            --sl-radius-2xl: 1.5rem;
            --sl-radius-full: 9999px;
            --sl-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        /* Animations */
        @keyframes sl-fade-in-up {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes sl-scale-in {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes sl-float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        @keyframes sl-pulse-glow {
            0%, 100% { box-shadow: 0 0 20px var(--sl-accent-glow); }
            50% { box-shadow: 0 0 40px var(--sl-accent-glow); }
        }
        @keyframes sl-progress-fill {
            from { transform: scaleX(0); }
            to { transform: scaleX(1); }
        }
        @keyframes sl-slide-in-left {
            from { opacity: 0; transform: translateX(-40px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        /* Global Overrides */
        body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
            background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%) !important;
            color: var(--sl-text-primary) !important;
            font-family: var(--sl-font-primary) !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stToolbar"], footer, #MainMenu { display: none !important; }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--sl-bg-secondary); }
        ::-webkit-scrollbar-thumb { background: var(--sl-bg-elevated); border-radius: 9999px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--sl-accent-primary); }
        
        /* Buttons */
        .stButton button {
            background: var(--sl-gradient-primary) !important;
            color: var(--sl-text-primary) !important;
            border: none !important;
            border-radius: var(--sl-radius-xl) !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            transition: all 0.25s var(--sl-ease-out) !important;
            box-shadow: 0 10px 15px rgba(0,0,0,0.5), 0 0 20px var(--sl-accent-glow) !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 20px 25px rgba(0,0,0,0.5), 0 0 40px var(--sl-accent-glow) !important;
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: var(--sl-bg-glass) !important;
            border: 2px dashed var(--sl-accent-primary) !important;
            border-radius: var(--sl-radius-2xl) !important;
            padding: 2rem !important;
            backdrop-filter: blur(24px) !important;
            transition: all 0.25s var(--sl-ease-out) !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: var(--sl-accent-secondary) !important;
            box-shadow: 0 0 30px var(--sl-accent-glow) !important;
        }
        
        /* Inputs */
        .stTextInput input, .stTextArea textarea {
            background: var(--sl-bg-tertiary) !important;
            border: 1px solid transparent !important;
            border-radius: 0.75rem !important;
            color: var(--sl-text-primary) !important;
            padding: 1rem !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--sl-accent-primary) !important;
            box-shadow: 0 0 0 3px var(--sl-accent-subtle) !important;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] { 
            font-size: 3rem !important; 
            font-weight: 700 !important;
            background: var(--sl-gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        [data-testid="stMetricLabel"] { 
            color: var(--sl-text-tertiary) !important; 
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }
        
        /* Progress */
        .stProgress > div > div { background: var(--sl-bg-tertiary) !important; border-radius: 9999px !important; }
        .stProgress > div > div > div { background: var(--sl-gradient-primary) !important; border-radius: 9999px !important; }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { background: var(--sl-bg-tertiary) !important; border-radius: var(--sl-radius-xl) !important; padding: 4px !important; }
        .stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--sl-text-secondary) !important; border-radius: 0.75rem !important; }
        .stTabs [aria-selected="true"] { background: var(--sl-accent-primary) !important; color: var(--sl-text-primary) !important; }
        .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }
        
        /* Markdown */
        .stMarkdown { color: var(--sl-text-secondary) !important; }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: var(--sl-text-primary) !important; }
        
        /* Alerts */
        .stAlert { background: var(--sl-bg-tertiary) !important; border-radius: var(--sl-radius-xl) !important; }
        
        /* Reduced Motion */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
        }
    </style>
    """, unsafe_allow_html=True)


def load_js():
    """Load premium animations JS."""
    st.markdown("""
    <script>
    (function() {
        // Score counter animation
        function animateValue(element, start, end, duration) {
            const range = end - start;
            let current = start;
            const increment = end > start ? 1 : -1;
            const stepTime = Math.abs(Math.floor(duration / range));
            const timer = setInterval(function() {
                current += increment;
                element.textContent = current;
                if (current === end) clearInterval(timer);
            }, stepTime);
        }
        
        // Initialize on Streamlit load
        document.addEventListener('DOMContentLoaded', function() {
            const scoreElements = document.querySelectorAll('[data-score]');
            scoreElements.forEach(el => {
                const score = parseInt(el.dataset.score);
                animateValue(el, 0, score, 1500);
            });
        });
    })();
    </script>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PREMIUM UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def render_hero():
    """Render the premium hero header."""
    st.markdown("""
    <div class="sl-hero" style="text-align: center; padding: 4rem 1.5rem; position: relative;">
        <div style="
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #1a1a26;
            border: 1px solid rgba(139, 92, 246, 0.4);
            border-radius: 9999px;
            font-size: 0.75rem;
            color: #a78bfa;
            margin-bottom: 1.5rem;
            animation: sl-fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
        ">
            <span style="
                display: inline-block;
                width: 6px;
                height: 6px;
                background: #8b5cf6;
                border-radius: 50%;
                margin-right: 0.5rem;
            "></span>
            AI-Powered Resume Analysis
        </div>
        
        <div style="
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
            border-radius: 1.5rem;
            font-size: 2.5rem;
            box-shadow: 0 0 60px rgba(139, 92, 246, 0.4);
            animation: sl-scale-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards, sl-float 6s ease-in-out infinite 0.8s;
        ">🔍</div>
        
        <h1 style="
            font-size: clamp(2.25rem, 1.6rem + 3.25vw, 3.5rem);
            font-weight: 700;
            background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            line-height: 1.1;
            animation: sl-fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s backwards;
        ">SkillLens AI</h1>
        
        <p style="
            font-size: clamp(1.125rem, 1rem + 0.6vw, 1.25rem);
            color: #94a3b8;
            max-width: 500px;
            margin: 0 auto;
            animation: sl-fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s backwards;
        ">See Your Resume Through an ATS Lens</p>
    </div>
    """, unsafe_allow_html=True)


def render_score_circle(score: int, label: str = "ATS Score"):
    """Render animated circular score display."""
    # Calculate stroke-dashoffset for the progress
    circumference = 2 * 3.14159 * 90  # radius = 90
    offset = circumference - (score / 100) * circumference
    
    # Determine score status
    if score >= 80:
        status_class = "excellent"
        status_text = "Excellent Match"
        status_color = "#22c55e"
    elif score >= 60:
        status_class = "good"
        status_text = "Good Match"
        status_color = "#84cc16"
    elif score >= 40:
        status_class = "average"
        status_text = "Needs Improvement"
        status_color = "#f59e0b"
    else:
        status_class = "poor"
        status_text = "Poor Match"
        status_color = "#ef4444"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2.5rem; animation: sl-scale-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards;">
        <div style="position: relative; width: 200px; height: 200px; margin: 0 auto 1.5rem;">
            <svg style="transform: rotate(-90deg); width: 100%; height: 100%;">
                <defs>
                    <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#8b5cf6"/>
                        <stop offset="100%" style="stop-color:#06b6d4"/>
                    </linearGradient>
                </defs>
                <circle cx="100" cy="100" r="90" fill="none" stroke="#1a1a26" stroke-width="8"/>
                <circle cx="100" cy="100" r="90" fill="none" stroke="url(#scoreGradient)" stroke-width="8"
                    stroke-linecap="round" stroke-dasharray="{circumference}" 
                    stroke-dashoffset="{offset}" 
                    style="transition: stroke-dashoffset 1.5s cubic-bezier(0.16, 1, 0.3, 1);"/>
            </svg>
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
            ">
                <span style="
                    font-size: clamp(3rem, 2rem + 5vw, 4rem);
                    font-weight: 700;
                    background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    line-height: 1;
                ">{score}</span>
                <span style="font-size: 1.5rem; color: #64748b; font-weight: 400;">%</span>
            </div>
        </div>
        <div style="font-size: 1.125rem; color: #94a3b8; font-weight: 500; margin-bottom: 0.75rem;">{label}</div>
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba({','.join(str(int(status_color[i:i+2], 16)) for i in (1, 3, 5))}, 0.15);
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            color: {status_color};
        ">
            <span>●</span> {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_category_scores(categories: dict):
    """Render category score cards with animated progress bars."""
    cols = st.columns(len(categories))
    
    for i, (category, score) in enumerate(categories.items()):
        with cols[i]:
            # Determine color class
            if score >= 80:
                bar_style = "background: linear-gradient(90deg, #22c55e, #4ade80);"
            elif score >= 60:
                bar_style = "background: linear-gradient(90deg, #84cc16, #a3e635);"
            elif score >= 40:
                bar_style = "background: linear-gradient(90deg, #f59e0b, #fbbf24);"
            else:
                bar_style = "background: linear-gradient(90deg, #ef4444, #f87171);"
            
            st.markdown(f"""
            <div style="
                background: rgba(26, 26, 38, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.03);
                border-radius: 1rem;
                padding: 1.25rem;
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
                animation: sl-fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) {0.1 * i}s backwards;
            ">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                    <span style="font-size: 0.875rem; font-weight: 500; color: #94a3b8;">{category}</span>
                    <span style="font-size: 1.25rem; font-weight: 700; color: #f8fafc;">{score}%</span>
                </div>
                <div style="height: 6px; background: #1a1a26; border-radius: 9999px; overflow: hidden;">
                    <div style="
                        height: 100%;
                        width: {score}%;
                        border-radius: 9999px;
                        {bar_style}
                        transform-origin: left;
                        animation: sl-progress-fill 1s cubic-bezier(0.16, 1, 0.3, 1) {0.2 + 0.1 * i}s backwards;
                    "></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_skill_pills(skills: list, skill_type: str = "missing"):
    """Render skill pills with hover glow effect."""
    if skill_type == "missing":
        border_color = "rgba(239, 68, 68, 0.3)"
        hover_color = "#ef4444"
        icon = "✗"
        title = "Missing Skills"
        count_bg = "rgba(239, 68, 68, 0.15)"
        count_color = "#ef4444"
    else:
        border_color = "rgba(34, 197, 94, 0.3)"
        hover_color = "#22c55e"
        icon = "✓"
        title = "Matched Skills"
        count_bg = "rgba(34, 197, 94, 0.15)"
        count_color = "#22c55e"
    
    pills_html = ""
    for skill in skills:
        pills_html += f"""
        <span style="
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: #1a1a26;
            border: 1px solid {border_color};
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            color: #94a3b8;
            transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: default;
        " onmouseover="
            this.style.background='#1e1e2e';
            this.style.borderColor='{hover_color}';
            this.style.color='#f8fafc';
            this.style.transform='translateY(-2px)';
            this.style.boxShadow='0 0 20px rgba({','.join(str(int(hover_color[i:i+2], 16)) for i in (1, 3, 5))}, 0.3)';
        " onmouseout="
            this.style.background='#1a1a26';
            this.style.borderColor='{border_color}';
            this.style.color='#94a3b8';
            this.style.transform='translateY(0)';
            this.style.boxShadow='none';
        ">
            <span style="font-size: 0.75rem;">{icon}</span> {skill}
        </span>
        """
    
    st.markdown(f"""
    <div style="animation: sl-fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.3s backwards;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <h3 style="font-size: 1.125rem; font-weight: 600; color: #f8fafc; margin: 0;">{title}</h3>
            <span style="
                padding: 0.25rem 0.75rem;
                background: {count_bg};
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                color: {count_color};
            ">{len(skills)}</span>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            {pills_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_suggestions(suggestions: list):
    """Render improvement suggestions with slide-in animation."""
    suggestions_html = ""
    for i, suggestion in enumerate(suggestions):
        suggestions_html += f"""
        <div style="
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            padding: 1rem;
            background: #1a1a26;
            border-radius: 0.75rem;
            border-left: 3px solid #8b5cf6;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            animation: sl-slide-in-left 0.5s cubic-bezier(0.16, 1, 0.3, 1) {0.1 + 0.05 * i}s backwards;
        " onmouseover="
            this.style.background='#1e1e2e';
            this.style.transform='translateX(4px)';
            this.style.borderLeftColor='#06b6d4';
        " onmouseout="
            this.style.background='#1a1a26';
            this.style.transform='translateX(0)';
            this.style.borderLeftColor='#8b5cf6';
        ">
            <div style="
                flex-shrink: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(139, 92, 246, 0.1);
                border-radius: 0.5rem;
                font-size: 0.75rem;
                color: #8b5cf6;
            ">💡</div>
            <p style="font-size: 0.875rem; color: #94a3b8; line-height: 1.625; margin: 0;">{suggestion}</p>
        </div>
        """
    
    st.markdown(f"""
    <div style="animation: sl-fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.4s backwards;">
        <h3 style="
            font-size: 1.125rem;
            font-weight: 600;
            color: #f8fafc;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        ">
            <span>📝</span> Resume Improvement Suggestions
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            {suggestions_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_loading():
    """Render premium loading state."""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 4rem;
        animation: sl-fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    ">
        <div style="
            width: 48px;
            height: 48px;
            border: 3px solid #1e1e2e;
            border-top-color: #8b5cf6;
            border-radius: 50%;
            animation: sl-spin 1s linear infinite;
            margin: 0 auto 1.5rem;
        " class="sl-spinner"></div>
        <p style="
            font-size: 1.125rem;
            color: #94a3b8;
            animation: sl-subtle-pulse 1.5s ease-in-out infinite;
        ">Analyzing your resume...</p>
    </div>
    <style>
        @keyframes sl-spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @keyframes sl-subtle-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
    </style>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main application entry point."""
    # Load styles
    load_css()
    
    # Render hero
    render_hero()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="
            background: rgba(26, 26, 38, 0.4);
            backdrop-filter: blur(24px);
            border: 2px dashed #1e1e2e;
            border-radius: 1.5rem;
            padding: 3rem;
            text-align: center;
            animation: sl-fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards;
        ">
            <div style="
                width: 64px;
                height: 64px;
                margin: 0 auto 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(139, 92, 246, 0.1);
                border-radius: 1rem;
                font-size: 1.75rem;
            ">📄</div>
            <h3 style="color: #f8fafc; margin-bottom: 0.5rem;">Upload Resume</h3>
            <p style="color: #64748b; font-size: 0.875rem;">Drag & drop or click to browse</p>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=['pdf', 'docx'], label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <label style="
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            color: #94a3b8;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        ">Job Description</label>
        """, unsafe_allow_html=True)
        job_description = st.text_area("", height=200, placeholder="Paste the job description here...", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button("🔍 Analyze Resume", use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Demo results (replace with your actual analysis)
    if analyze_clicked or uploaded_file:
        st.markdown("""<hr style="
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #1e1e2e, rgba(139, 92, 246, 0.3), #1e1e2e, transparent);
            margin: 2rem 0;
        ">""", unsafe_allow_html=True)
        
        # Score display
        render_score_circle(78, "ATS Compatibility Score")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Category scores
        render_category_scores({
            "Skills Match": 85,
            "Experience": 72,
            "Keywords": 68,
            "Format": 90
        })
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Skills
        col1, col2 = st.columns(2)
        with col1:
            render_skill_pills(["React", "TypeScript", "GraphQL", "AWS Lambda"], skill_type="matched")
        with col2:
            render_skill_pills(["Kubernetes", "Terraform", "Go", "Redis"], skill_type="missing")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Suggestions
        render_suggestions([
            "Add quantifiable achievements to your work experience (e.g., 'Increased performance by 40%')",
            "Include keywords from the job description: Kubernetes, Terraform, Infrastructure as Code",
            "Add a technical skills section with proficiency levels",
            "Include relevant certifications (AWS, GCP, or Azure)",
            "Expand on your experience with microservices architecture"
        ])


if __name__ == "__main__":
    main()
