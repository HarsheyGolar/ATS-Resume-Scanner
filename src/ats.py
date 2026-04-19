from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import re

def normalize_text_for_matching(text):
    """
    Normalize text for better matching:
    - Lowercase
    - Remove special characters (keep alphanumeric and spaces)
    - Normalize whitespace
    - Handle common variations (NumPy vs numpy, etc.)
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Normalize common skill variations
    text = re.sub(r'\bnumpy\b', 'numpy', text)
    text = re.sub(r'\bnum\s*py\b', 'numpy', text)
    text = re.sub(r'\bpy\s*torch\b', 'pytorch', text)
    text = re.sub(r'\bnode\s*\.?\s*js\b', 'nodejs', text)
    text = re.sub(r'\bc\s*\+\s*\+\b', 'c++', text)
    text = re.sub(r'\bc\s*#\b', 'c#', text)
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text

def ats_score(resume, jd):
    """
    Professional ATS scoring engine aligned with real HR practices.
    
    Industry-standard weighted model:
    - Core Skills (AI/ML/Programming): 45%
    - Tools & Frameworks: 25%
    - Data & Analytics: 20%
    - Bonus Skills (Cloud/Extras): 10%
    
    Key enhancements:
    - Semantic matching with skill equivalencies
    - Cloud skills treated as bonuses, not blockers
    - Context-aware partial matching
    - Realistic score ranges (70-80% for strong candidates)
    - NEVER returns 0% incorrectly
    
    Score bands:
    0–29%   → Needs Improvement
    30–49%  → Below Average  
    50–69%  → Good Match
    70%+    → Strong Match
    """
    try:
        # Normalize both texts for better matching
        resume_norm = normalize_text_for_matching(resume)
        jd_norm = normalize_text_for_matching(jd)
        
        # Early return if either is empty
        if not resume_norm or not jd_norm:
            logging.warning("Empty resume or JD text")
            return 15.0  # Baseline score instead of 0
        
        # PROFESSIONAL CATEGORY DEFINITIONS WITH SEMANTIC MAPPING
        
        # Core Skills (45% weight) - AI/ML/Programming fundamentals
        core_skills_keywords = [
            'python', 'machine learning', 'ml', 'artificial intelligence', 'ai',
            'deep learning', 'neural networks', 'nlp', 'natural language processing',
            'computer vision', 'cv', 'tensorflow', 'pytorch', 'scikit-learn', 'sklearn',
            'pandas', 'numpy', 'data science', 'algorithms', 'programming', 'coding',
            'software development', 'development', 'engineer', 'engineering'
        ]
        
        # Tools & Frameworks (25% weight) - Libraries, frameworks, deployment tools
        tools_frameworks_keywords = [
            'flask', 'fastapi', 'django', 'streamlit', 'react', 'angular', 'vue',
            'node.js', 'nodejs', 'express', 'spring', 'docker', 'kubernetes',
            'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'api', 'rest', 'graphql',
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'
        ]
        
        # Data & Analytics (20% weight) - Data processing and analysis skills
        data_analytics_keywords = [
            'data analysis', 'data preprocessing', 'feature engineering', 'etl',
            'data visualization', 'matplotlib', 'seaborn', 'plotly', 'bokeh',
            'statistics', 'statistical analysis', 'model evaluation', 'model validation',
            'metrics', 'performance metrics', 'optimization', 'data cleaning',
            'pandas', 'numpy', 'sql', 'big data', 'spark', 'hadoop'
        ]
        
        # Bonus Skills (10% weight) - Cloud platforms and nice-to-haves
        bonus_skills_keywords = [
            'aws', 'amazon web services', 'azure', 'google cloud platform', 'gcp',
            'cloud computing', 'serverless', 'lambda', 'ec2', 's3', 'gke', 'aks',
            'terraform', 'ansible', 'iac', 'infrastructure as code', 'devops',
            'tableau', 'power bi', 'excel', 'powerpoint', 'jira', 'confluence'
        ]
        
        # Semantic Equivalence Mapping for Intelligent Matching
        semantic_equivalents = {
            'feature engineering': ['data preprocessing', 'data cleaning', 'data transformation'],
            'model evaluation': ['model validation', 'model testing', 'performance evaluation', 'optimization'],
            'pandas': ['data analysis', 'data manipulation', 'data processing'],
            'numpy': ['numerical computing', 'mathematical computing', 'scientific computing'],
            'machine learning': ['ml', 'ai', 'artificial intelligence', 'predictive modeling'],
            'data science': ['data analysis', 'analytics', 'business intelligence'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud computing'],
            'api': ['rest api', 'graphql', 'web services'],
            'docker': ['containerization', 'containers', 'kubernetes'],
            'sql': ['database', 'postgresql', 'mysql', 'querying']
        }
        
        # 1. TF-IDF Cosine Similarity (Semantic matching)
        cosine_sim = 0.0
        try:
            vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
            vectors = vectorizer.fit_transform([resume_norm, jd_norm])
            cosine_sim = cosine_similarity(vectors[0], vectors[1])[0][0]
        except (ValueError, Exception) as e:
            logging.warning(f"TF-IDF calculation failed: {e}")
            cosine_sim = 0.0
        
        # 2. Enhanced Matching Logic with Semantic Awareness
        def count_matches_with_semantics(text, keywords, semantic_map=None):
            """Count matches with semantic equivalence support"""
            matches = 0
            text_lower = text.lower()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Exact match check
                pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                if re.search(pattern, text_lower):
                    matches += 1
                    continue
                
                # Semantic equivalent check
                if semantic_map and keyword_lower in semantic_map:
                    for equivalent in semantic_map[keyword_lower]:
                        equiv_pattern = r'\b' + re.escape(equivalent.lower()) + r'\b'
                        if re.search(equiv_pattern, text_lower):
                            matches += 0.7  # Partial credit for semantic match
                            break
            
            return matches
        
        def count_matches(text, keywords):
            """Legacy wrapper for backward compatibility"""
            return count_matches_with_semantics(text, keywords)
        
        # PROFESSIONAL WEIGHTED SCORING MODEL WITH CONDITIONAL BONUS HANDLING
        
        # Core Skills (45% weight) - AI/ML/Programming fundamentals
        core_matches = count_matches_with_semantics(resume_norm, core_skills_keywords, semantic_equivalents)
        core_in_jd = count_matches_with_semantics(jd_norm, core_skills_keywords, semantic_equivalents)
        core_score = (core_matches / core_in_jd * 100) if core_in_jd > 0 else 0
        
        # Tools & Frameworks (25% weight) - Libraries and deployment tools
        tools_matches = count_matches_with_semantics(resume_norm, tools_frameworks_keywords, semantic_equivalents)
        tools_in_jd = count_matches_with_semantics(jd_norm, tools_frameworks_keywords, semantic_equivalents)
        tools_score = (tools_matches / tools_in_jd * 100) if tools_in_jd > 0 else 0
        
        # Data & Analytics (20% weight) - Data processing and analysis
        data_matches = count_matches_with_semantics(resume_norm, data_analytics_keywords, semantic_equivalents)
        data_in_jd = count_matches_with_semantics(jd_norm, data_analytics_keywords, semantic_equivalents)
        data_score = (data_matches / data_in_jd * 100) if data_in_jd > 0 else 0
        
        # Bonus Skills (10% weight) - Cloud and extras (OPTIONAL, NO PENALTY if missing)
        bonus_matches = count_matches_with_semantics(resume_norm, bonus_skills_keywords, semantic_equivalents)
        bonus_in_jd = count_matches_with_semantics(jd_norm, bonus_skills_keywords, semantic_equivalents)
        bonus_score = (bonus_matches / bonus_in_jd * 100) if bonus_in_jd > 0 else 0
        
        # CONDITIONAL WEIGHTED CALCULATION
        # Only include bonus skills in calculation if they are mentioned in JD
        if bonus_in_jd > 0:
            # JD includes bonus skills, so include them in weighted average
            total_weight = 0.45 + 0.25 + 0.20 + 0.10  # 1.0
            weighted_score = (core_score * 0.45) + (tools_score * 0.25) + (data_score * 0.20) + (bonus_score * 0.10)
        else:
            # JD does not include bonus skills, redistribute weight proportionally
            # Original weights: Core:45%, Tools:25%, Data:20%, Bonus:10%
            # Without bonus, total weight becomes 90%, so normalize accordingly
            # New weights: Core:50% (45/90), Tools:27.8% (25/90), Data:22.2% (20/90)
            norm_core_weight = 0.45 / 0.90  # ~0.50
            norm_tools_weight = 0.25 / 0.90  # ~0.278
            norm_data_weight = 0.20 / 0.90   # ~0.222
            
            weighted_score = (core_score * norm_core_weight) + (tools_score * norm_tools_weight) + (data_score * norm_data_weight)
            
        # Ensure weighted score doesn't exceed 100%
        weighted_score = min(100.0, weighted_score)
        
        # 3. Keyword Overlap (Jaccard-like) - improved
        stop_words = {'and', 'the', 'is', 'in', 'at', 'of', 'for', 'to', 'a', 'an', 'with', 'by', 'on', 'or', 'but'}
        resume_words = {w for w in resume_norm.split() if w not in stop_words and len(w) > 2}
        jd_words = {w for w in jd_norm.split() if w not in stop_words and len(w) > 2}
        
        overlap_score = 0.0
        if jd_words:
            overlap = len(resume_words.intersection(jd_words))
            overlap_score = (overlap / len(jd_words)) * 100
        
        # 4. ENHANCED SCORE COMBINATION WITH PROPER BONUS HANDLING
        # Apply bonus adjustment only if bonus skills are in JD
        bonus_addition = 0.0
        if bonus_in_jd > 0 and bonus_matches > 0:
            # Positive bonus for having bonus skills when they're mentioned in JD
            bonus_ratio = bonus_matches / bonus_in_jd
            bonus_addition = min(8.0, bonus_ratio * 15.0)  # Max 8% addition
        
        # Combine scores with adjusted weighting
        final_score = (weighted_score * 0.6) + (overlap_score * 0.25) + (cosine_sim * 100 * 0.15)
        final_score += bonus_addition
        
        # Ensure final score doesn't exceed 100%
        final_score = min(100.0, final_score)
        
        # 5. CRITICAL: Ensure score is NEVER 0% incorrectly
        resume_len = len(resume_norm.strip())
        jd_len = len(jd_norm.strip())
        
        # If we have both resume and JD text, apply baseline logic
        if resume_len > 0 and jd_len > 0:
            # Check if there's ANY meaningful overlap
            has_overlap = (
                overlap_score > 0 or
                cosine_sim > 0.01 or
                skills_matches > 0 or
                exp_matches > 0 or
                tools_matches > 0 or
                edu_matches > 0
            )
            
            if has_overlap:
                # SAFETY CHECK: If Core Skills ≥ 80% and Data ≥ 70%, final score should NOT fall below 70%
                if core_in_jd > 0 and data_in_jd > 0:  # Only check if both categories are in JD
                    core_pct = (core_matches / core_in_jd * 100) if core_in_jd > 0 else 0
                    data_pct = (data_matches / data_in_jd * 100) if data_in_jd > 0 else 0
                    
                    if core_pct >= 80 and data_pct >= 70:
                        # Strong candidates in core areas should score well
                        final_score = max(final_score, 70.0)
                
                # Boost realistic scores for strong candidates
                if final_score < 30:
                    # Strong candidates shouldn't score below 30%
                    final_score = max(final_score, 30.0)
                elif final_score > 65:
                    # Top performers deserve 70%+ scores
                    final_score = min(100.0, final_score + 5.0)  # Gentle boost
            else:
                # Even with no direct overlap, recognize structured resumes
                resume_sections = ['experience', 'education', 'skills', 'projects', 'summary', 'objective', 'work', 'technical']
                section_count = sum(1 for section in resume_sections if section in resume_norm)
                if section_count > 0:
                    final_score = 25.0 + min(15.0, section_count * 3.0)  # 25-40% baseline
                else:
                    final_score = 20.0  # Minimum reasonable baseline
            
            # For short resumes, cap maximum but ensure minimum
            if resume_len < 200:
                final_score = min(final_score, 50.0)  # Cap at 50% for very short resumes
                final_score = max(final_score, 15.0)  # But never below 15%
            elif resume_len < 600:
                # Short but valid resume
                if final_score < 25:
                    final_score = max(final_score, 25.0)
        
        # Round and cap at 100%
        final_score_100 = min(round(final_score, 1), 100.0)
        
        # Final safeguard: Never return 0% if we have both texts
        if resume_len > 0 and jd_len > 0 and final_score_100 < 15.0:
            final_score_100 = 15.0
        
        logging.info(f"ATS Score calculated: {final_score_100}% (resume: {resume_len} chars, JD: {jd_len} chars)")
        return final_score_100
        
    except Exception as e:
        logging.error(f"Error calculating ATS score: {e}", exc_info=True)
        # Return baseline instead of 0
        return 15.0
