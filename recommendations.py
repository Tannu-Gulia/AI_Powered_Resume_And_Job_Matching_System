"""
Course & Certification Recommendations Module for AI-Powered Resume & Job Matching System
Provides personalized course recommendations, certifications, and learning roadmaps
based on identified skill gaps.
"""

import database

# Curated fallback knowledge base of premium learning resources
DEFAULT_COURSES = {
    "python": ("Python for Everybody Specialization", "Coursera", "https://www.coursera.org/specializations/python"),
    "machine learning": ("Machine Learning Specialization by Andrew Ng", "Coursera", "https://www.coursera.org/specializations/machine-learning-introduction"),
    "deep learning": ("Deep Learning Specialization (DeepLearning.AI)", "Coursera", "https://www.coursera.org/specializations/deep-learning"),
    "natural language processing": ("NLP Specialization by DeepLearning.AI", "Coursera", "https://www.coursera.org/specializations/natural-language-processing-nlp"),
    "nlp": ("Natural Language Processing in Python", "Coursera", "https://www.coursera.org/specializations/natural-language-processing-nlp"),
    "sql": ("The Complete SQL Bootcamp: Go from Zero to Hero", "Udemy", "https://www.udemy.com/course/the-complete-sql-bootcamp/"),
    "tableau": ("Tableau Desktop Specialist Certification", "Coursera", "https://www.coursera.org/learn/data-visualization-tableau"),
    "power bi": ("Microsoft Power BI Data Analyst Professional Certificate", "Coursera", "https://www.coursera.org/professional-certificates/microsoft-power-bi-data-analyst"),
    "docker": ("Docker & Kubernetes: The Practical Guide", "Udemy", "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"),
    "kubernetes": ("Certified Kubernetes Administrator (CKA)", "Udemy", "https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/"),
    "aws": ("AWS Certified Solutions Architect - Associate", "Coursera", "https://www.coursera.org/learn/aws-cloud-solutions-architect"),
    "azure": ("Microsoft Certified: Azure Fundamentals AZ-900", "Coursera", "https://www.coursera.org/learn/microsoft-azure-fundamentals-az-900"),
    "react": ("React - The Complete Guide (incl. React Router & Redux)", "Udemy", "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"),
    "node.js": ("The Complete Node.js Developer Course", "Udemy", "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/"),
    "spring boot": ("Spring Boot 3, Spring 6 & Hibernate for Beginners", "Udemy", "https://www.udemy.com/course/spring-hibernate-tutorial/"),
    "git": ("Version Control with Git", "Coursera", "https://www.coursera.org/learn/version-control-with-git"),
    "ci/cd": ("Continuous Integration and Continuous Deployment", "Coursera", "https://www.coursera.org/learn/continuous-integration-continuous-deployment"),
    "cybersecurity": ("Google Cybersecurity Professional Certificate", "Coursera", "https://www.coursera.org/professional-certificates/google-cybersecurity"),
    "statistics": ("Statistics with Python Specialization", "Coursera", "https://www.coursera.org/specializations/statistics-with-python"),
    "spark": ("Apache Spark 3 for Data Engineering & Big Data", "Udemy", "https://www.udemy.com/course/taming-big-data-with-apache-spark-hands-on/"),
    "communication": ("Effective Communication: Writing, Design, and Presentation", "Coursera", "https://www.coursera.org/specializations/effective-communication"),
    "problem solving": ("Computational Thinking for Problem Solving", "Coursera", "https://www.coursera.org/learn/computational-thinking-problem-solving")
}


def get_recommendations_for_skills(missing_skills: list) -> list:
    """
    Query database and catalog for learning recommendations targeting missing skills.
    Returns structured list of recommended courses.
    """
    if not missing_skills:
        return []

    conn = database.get_connection()
    recommendations = []

    for skill in missing_skills:
        s_clean = skill.strip()
        row = conn.execute("""
        SELECT skill_name, category, recommended_course, course_platform, course_url
        FROM skills
        WHERE LOWER(skill_name) = LOWER(?)
        LIMIT 1
        """, (s_clean,)).fetchone()

        if row and row['recommended_course']:
            recommendations.append({
                "skill": row['skill_name'],
                "category": row['category'],
                "course_name": row['recommended_course'],
                "platform": row['course_platform'],
                "url": row['course_url']
            })
        else:
            # Check fallback dict
            key = s_clean.lower()
            if key in DEFAULT_COURSES:
                c_name, c_plat, c_url = DEFAULT_COURSES[key]
                recommendations.append({
                    "skill": s_clean,
                    "category": "Technical",
                    "course_name": c_name,
                    "platform": c_plat,
                    "url": c_url
                })
            else:
                # Generic fallback resource
                recommendations.append({
                    "skill": s_clean,
                    "category": "General Upskilling",
                    "course_name": f"Mastering {s_clean}: From Fundamentals to Advanced",
                    "platform": "Coursera / Udemy",
                    "url": f"https://www.coursera.org/search?query={s_clean.replace(' ', '%20')}"
                })

    conn.close()
    return recommendations


class CourseRecommender:
    """
    Object-Oriented Course & Certification Recommendation Engine.
    Maps skill deficits to accredited online courses from Coursera, Udemy, and edX.
    """
    def __init__(self, fallback_catalog=None):
        self.fallback = fallback_catalog or DEFAULT_COURSES

    def get_recommendations(self, missing_skills: list) -> list:
        """Fetch targeted course recommendations for missing skills."""
        return get_recommendations_for_skills(missing_skills)

