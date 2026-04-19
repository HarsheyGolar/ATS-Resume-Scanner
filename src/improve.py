def improve_resume(missing_skills):
    """
    Generate 6-10 actionable AI recommendations.
    Each must:
    • mention a concrete project/action
    • include measurable impact
    """
    suggestions = []
    
    # Limit to max 12 skills (prioritized)
    limited_skills = missing_skills[:12]
    
    # Define specific project suggestions for common skills
    project_suggestions = {
        'python': f"Create a Python project like a data analysis tool or web scraper that demonstrates your {', '.join([s for s in limited_skills if 'python' in s.lower()][:3])} skills with measurable impact.",
        'javascript': f"Build a JavaScript application (e.g., React dashboard) showcasing {', '.join([s for s in limited_skills if 'javascript' in s.lower()][:3])} with performance metrics.",
        'sql': f"Develop a SQL project analyzing a real dataset (e.g., sales, user behavior) with measurable insights and performance improvements.",
        'aws': f"Deploy a cloud application on AWS demonstrating {', '.join([s for s in limited_skills if 'aws' in s.lower()][:3])} with cost optimization metrics.",
        'docker': f"Containerize an application using Docker and document the deployment process, showing performance or efficiency improvements.",
        'react': f"Create a React application with {', '.join([s for s in limited_skills if 'react' in s.lower()][:3])} features, measuring user engagement or performance.",
        'machine learning': f"Implement a machine learning model that solves a real-world problem, demonstrating {', '.join([s for s in limited_skills if 'ml' in s.lower() or 'machine learning' in s.lower()][:3])} with accuracy metrics.",
        'data analysis': f"Perform comprehensive data analysis on a public dataset, showcasing {', '.join([s for s in limited_skills if 'analysis' in s.lower()][:3])} with concrete business insights.",
        'git': f"Maintain a GitHub portfolio with 3-5 projects demonstrating proper version control, collaboration, and {', '.join([s for s in limited_skills if 'git' in s.lower()][:3])} practices.",
        'api': f"Build or integrate with RESTful APIs, showcasing {', '.join([s for s in limited_skills if 'api' in s.lower()][:3])} skills with performance benchmarks."
    }
    
    # Generate specific, actionable recommendations
    for i, skill in enumerate(limited_skills):
        skill_lower = skill.lower()
        
        if skill_lower in project_suggestions:
            suggestions.append(project_suggestions[skill_lower])
        else:
            # Generic but specific suggestions
            suggestions.append(
                f"Add a specific project or work experience demonstrating {skill.title()}. "
                f"Include quantifiable results like 'increased efficiency by 25%' or 'reduced processing time by 40%'."
            )
        
        # Limit to 10 suggestions maximum
        if len(suggestions) >= 10:
            break
    
    return suggestions
