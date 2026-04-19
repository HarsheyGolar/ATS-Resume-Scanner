import re

def category_score(resume_text, jd_text, skills_db):
    """
    Calculates match score per category and identifies matched/missing skills.
    Uses robust regex-based matching (partial & semantic-ish).
    """
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    # PROFESSIONAL CATEGORY STRUCTURE
    fixed_categories = ['Core Skills', 'Tools & Frameworks', 'Data & Analytics', 'Bonus Skills']
    cat_scores = {}
    all_missing_skills = []
    all_matched_skills = []
    
    # Track categories that SHOULD have a score (JD has skills in them)
    relevant_categories = []

    def has_skill_semantic(text, skill, semantic_map=None):
        """
        Enhanced skill detection with semantic matching support.
        Checks for exact matches and semantic equivalents.
        """
        skill = str(skill).lower().strip()
        if not skill: return False
        
        # Exact match check
        if re.search(r'[^a-z0-9]', skill):
            return skill in text
        
        if len(skill) <= 2:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                return True
        else:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                return True
        
        # Semantic equivalent check
        if semantic_map and skill in semantic_map:
            for equivalent in semantic_map[skill]:
                equiv_pattern = r'\b' + re.escape(str(equivalent).lower()) + r'\b'
                if re.search(equiv_pattern, text):
                    return True
        
        return False
    
    def has_skill(text, skill):
        """Legacy wrapper for backward compatibility"""
        return has_skill_semantic(text, skill, semantic_equivalents)

    # PROFESSIONAL SKILL CATEGORIES WITH SEMANTIC MAPPING
    category_skills = {
        'Core Skills': [
            'python', 'machine learning', 'ml', 'artificial intelligence', 'ai',
            'deep learning', 'neural networks', 'nlp', 'natural language processing',
            'computer vision', 'cv', 'tensorflow', 'pytorch', 'scikit-learn', 'sklearn',
            'pandas', 'numpy', 'data science', 'algorithms', 'programming', 'coding',
            'software development', 'development', 'engineer', 'engineering'
        ],
        'Tools & Frameworks': [
            'flask', 'fastapi', 'django', 'streamlit', 'react', 'angular', 'vue',
            'node.js', 'nodejs', 'express', 'spring', 'docker', 'kubernetes',
            'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'api', 'rest', 'graphql',
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'
        ],
        'Data & Analytics': [
            'data analysis', 'data preprocessing', 'feature engineering', 'etl',
            'data visualization', 'matplotlib', 'seaborn', 'plotly', 'bokeh',
            'statistics', 'statistical analysis', 'model evaluation', 'model validation',
            'metrics', 'performance metrics', 'optimization', 'data cleaning',
            'pandas', 'numpy', 'sql', 'big data', 'spark', 'hadoop'
        ],
        'Bonus Skills': [
            'aws', 'amazon web services', 'azure', 'google cloud platform', 'gcp',
            'cloud computing', 'serverless', 'lambda', 'ec2', 's3', 'gke', 'aks',
            'terraform', 'ansible', 'iac', 'infrastructure as code', 'devops',
            'tableau', 'power bi', 'excel', 'powerpoint', 'jira', 'confluence'
        ]
    }
    
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
    
    for cat in fixed_categories:
        # Use predefined skills for each category or fallback to skills_db
        if cat in category_skills:
            cat_skills = category_skills[cat]
        else:
            # Fallback to skills_db if category not in predefined list
            cat_skills = skills_db[skills_db['category'] == cat]['skill'].tolist()
        
        # 1. Identify skills relevant to the JD
        jd_skills_found = [s for s in cat_skills if has_skill(jd_text, str(s))]
        
        # 2. Identify which of those are in the Resume
        resume_skills_found = [s for s in jd_skills_found if has_skill(resume_text, str(s))]
        
        # 3. Calculate Score with Partial Credit for Semantic Matches
        if jd_skills_found:
            score = int((len(resume_skills_found) / len(jd_skills_found)) * 100)
            relevant_categories.append(cat)
            
            # Conservative boost for semantic matches to prevent over-scoring
            if cat in ['Core Skills', 'Tools & Frameworks', 'Data & Analytics'] and score > 0:
                # Check for semantic matches that weren't caught by exact matching
                semantic_matches = 0
                for skill in jd_skills_found:
                    skill_str = str(skill).lower()
                    if skill_str in semantic_equivalents:
                        for equivalent in semantic_equivalents[skill_str]:
                            if equivalent in resume_text:
                                semantic_matches += 1
                                break
                
                if semantic_matches > 0:
                    semantic_boost = min(15, int((semantic_matches / len(jd_skills_found)) * 75))
                    score = min(90, score + semantic_boost)  # Cap at 90% to maintain realism
        else:
            # If JD doesn't mention this category, default to neutral score
            score = 50  # Neutral baseline instead of 0

        cat_scores[cat] = score
        
        # Collect matched and missing
        all_matched_skills.extend(resume_skills_found)
        all_missing_skills.extend(list(set(jd_skills_found) - set(resume_skills_found)))

    # PROFESSIONAL SCORE SAFEGUARD
    # Ensure realistic scoring that reflects candidate strengths
    if len(resume_text.strip()) > 0 and len(jd_text.strip()) > 0:
        total_score = sum(cat_scores.values())
        
        # Check if there are relevant categories in JD
        if relevant_categories:
            # Prevent unrealistic 0% scores for qualified candidates
            if total_score < 60:  # Threshold for intervention
                for cat in relevant_categories:
                    if cat_scores[cat] == 0:
                        # Look for contextual evidence of skills
                        if cat in category_skills:
                            cat_skills = category_skills[cat]
                            contextual_matches = 0
                            
                            # Check for related terms and context
                            for skill in cat_skills:
                                skill_lower = str(skill).lower()
                                # Look for skill or related terms
                                if (skill_lower in resume_text or 
                                    any(equiv in resume_text for equiv in semantic_equivalents.get(skill_lower, []))):
                                    contextual_matches += 1
                            
                            if contextual_matches > 0:
                                # Calculate reasonable partial score
                                jd_skills_count = len([s for s in cat_skills if has_skill(jd_text, str(s))])
                                if jd_skills_count > 0:
                                    cat_scores[cat] = min(70, max(20, int((contextual_matches / jd_skills_count) * 100)))
                                else:
                                    cat_scores[cat] = min(30, contextual_matches * 10)
            
            # Boost scores for well-matched candidates
            avg_score = total_score / len(relevant_categories) if relevant_categories else 0
            if avg_score > 60:
                # Strong candidates deserve recognition
                boost_amount = min(15, int(avg_score * 0.1))
                for cat in relevant_categories:
                    if cat_scores[cat] > 50:
                        cat_scores[cat] = min(100, cat_scores[cat] + boost_amount)

    # BALANCED BONUS SKILLS HANDLING
    # Ensure bonus skills enhance but don't dominate scoring
    if 'Bonus Skills' in cat_scores:
        bonus_score = cat_scores['Bonus Skills']
        # Cap bonus skills contribution to prevent over-inflation
        if bonus_score > 80:
            cat_scores['Bonus Skills'] = 80  # Reasonable maximum
        elif bonus_score == 0:
            # If bonus skills aren't relevant in JD, use neutral score
            bonus_relevant = len([s for s in category_skills.get('Bonus Skills', []) if has_skill(jd_text, s)]) > 0
            if not bonus_relevant:
                cat_scores['Bonus Skills'] = 50  # Neutral baseline
    
    return cat_scores, list(set(all_matched_skills)), list(set(all_missing_skills))
