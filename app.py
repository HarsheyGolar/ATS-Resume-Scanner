from flask import Flask, render_template, request, jsonify
import pandas as pd
import io
import logging
from pathlib import Path

# Configure Flask Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import backend modules
from src.reader import read_resume
from src.ats import ats_score
from src.skills import category_score
from src.improve import improve_resume

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load skills database once at startup
try:
    skills_db = pd.read_csv("datasets/skills_master.csv")
    logger.info("Skills database loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load skills database: {e}")
    # Create a dummy DF to prevent crash, but log error
    skills_db = pd.DataFrame(columns=['skill', 'category'])

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle resume analysis"""
    try:
        # Get uploaded file
        resume_file = request.files.get('resume_file')
        jd_text = request.form.get('jd_text', '')
        
        if not resume_file or not jd_text:
            return jsonify({'error': 'Missing resume file or job description'}), 400
        
        # Validate minimum length for job description (non-blocking warning)
        warnings = []
        if len(jd_text.strip()) < 200:
            warnings.append(f'Job description is short ({len(jd_text.strip())} chars). For best results, provide at least 200 characters.')
        
        logger.info(f"Analyzing resume: {resume_file.filename}")
        
        resume_text = ""

        # 1. Read resume (Robust parsing - NEVER blocks)
        try:
            resume_text, warning_msg = read_resume(resume_file)
            if warning_msg:
                warnings.append(warning_msg)
                
            # NEVER block analysis - even if text is empty or OCR unavailable
            # The scoring functions will handle empty/short text gracefully
            if not resume_text:
                logger.warning("Resume text extraction returned empty - continuing with analysis")
                resume_text = ""  # Empty string is fine, scoring will handle it
                if not any('text' in w.lower() for w in warnings):
                    warnings.append("Could not extract text from resume. Results may be limited.")
                
        except Exception as e:
            logger.error(f"Resume parsing error: {e}", exc_info=True)
            warnings.append(f"Resume parsing encountered issues: {str(e)}. Results may be incomplete.")
            resume_text = ""  # Continue with empty text - don't block
        
        # 2. Calculate ATS score (always returns valid score, never 0% incorrectly)
        try:
            score = ats_score(resume_text, jd_text.lower())
        except Exception as e:
            logger.error(f"ATS scoring error: {e}", exc_info=True)
            score = 15.0  # Baseline score instead of failing
            warnings.append("ATS scoring encountered issues. Score may be approximate.")
        
        # 3. Calculate category scores & skills (always returns valid results)
        try:
            cat_scores, matched_skills, missing_skills = category_score(resume_text, jd_text.lower(), skills_db)
        except Exception as e:
            logger.error(f"Category scoring error: {e}", exc_info=True)
            # Return default values instead of failing
            cat_scores = {'AI': 0, 'Data': 0, 'Cloud': 0, 'Programming': 0, 'Tools': 0, 'Web': 0}
            matched_skills = []
            missing_skills = []
            warnings.append("Category scoring encountered issues. Results may be incomplete.")
        
        # 4. Generate suggestions (always returns valid list)
        try:
            suggestions = improve_resume(missing_skills)
        except Exception as e:
            logger.error(f"Suggestion generation error: {e}", exc_info=True)
            suggestions = []
            warnings.append("Could not generate suggestions. Please try again.")
        
        # Log success
        logger.info(f"Analysis complete. Score: {score}%, Warnings: {len(warnings)}")
        
        # ALWAYS return valid JSON response - never fail
        return jsonify({
            'success': True,
            'ats_score': score,
            'category_scores': cat_scores,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
            'warnings': warnings
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in /analyze: {e}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
