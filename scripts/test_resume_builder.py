"""
Automated Comprehensive Test Script for AI-Powered Resume Builder
Tests:
1. Content Enhancements (STAR structure, Action Verbs, Objective, Skills)
2. Quality Scoring & Diagnostics
3. HTML Preview Generation for 4 Templates
4. ReportLab PDF Generation for 4 Templates
5. SQLite Database Persistence & Synchronization
"""

import os
import sys
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database
from resume_builder import (
    ResumeContentEnhancer,
    ResumeQualityChecker,
    ResumeTemplateManager,
    ResumePDFGenerator
)


def run_tests():
    print("=" * 60)
    print("TEST 1: AI Content Enhancement Engine")
    print("=" * 60)
    
    # Test project description improvement (from user prompt)
    raw_proj = "I made a project using Python and SQL for analysing data."
    improved_proj = ResumeContentEnhancer.improve_project_description(
        raw_proj,
        title="Data Analytics System",
        technologies="Python, SQL, Pandas",
        outcome="automated reporting and 40% time savings"
    )
    print("Original Input:", raw_proj)
    print("AI Improved Output:\n", improved_proj)
    assert "Developed" in improved_proj or "Architected" in improved_proj or "Engineered" in improved_proj
    assert "Python" in improved_proj and "SQL" in improved_proj
    print("✓ Project enhancement test passed!")

    # Test career objective improvement
    raw_obj = "I want a job in python and machine learning."
    improved_obj = ResumeContentEnhancer.improve_objective(
        raw_obj,
        degree="Master of Computer Applications (MCA)",
        target_role="Data Scientist",
        skills="Python, SQL, Machine Learning"
    )
    print("\nOriginal Objective:", raw_obj)
    print("AI Improved Objective:\n", improved_obj)
    assert "Python" in improved_obj
    print("✓ Objective enhancement test passed!")

    # Test skills presentation
    raw_tech = "python, sql, machine learning, react, git, aws"
    raw_soft = "communication, problem solving"
    clean_t, clean_s = ResumeContentEnhancer.improve_skills_presentation(raw_tech, raw_soft)
    print("\nCleaned Tech Skills:", clean_t)
    print("Cleaned Soft Skills:", clean_s)
    assert "Python" in clean_t and "SQL" in clean_t
    print("✓ Skills presentation test passed!")

    print("\n" + "=" * 60)
    print("TEST 2: Resume Quality Checker")
    print("=" * 60)
    sample_resume = {
        "full_name": "Aarav Sharma",
        "email": "candidate@test.com",
        "phone": "+91 98765 43210",
        "location": "Bangalore, India",
        "linkedin": "https://linkedin.com/in/aarav",
        "github": "https://github.com/aarav",
        "career_objective": improved_obj,
        "summary": "Data Scientist with MCA degree and hands-on ML expertise.",
        "technical_skills": clean_t,
        "soft_skills": clean_s,
        "education": [
            {
                "degree": "MCA in Data Science",
                "institution": "Tech University",
                "passing_year": "2024",
                "score": "8.8 CGPA",
                "coursework": "ML, NLP, SQL"
            }
        ],
        "projects": [
            {
                "title": "Customer Churn Prediction",
                "description": improved_proj,
                "technologies": "Python, SQL, Scikit-learn",
                "outcome": "91% accuracy",
                "github_link": "https://github.com/aarav/churn"
            },
            {
                "title": "NLP Resume Matcher",
                "description": "Developed TF-IDF similarity matcher using Python and Scikit-learn.",
                "technologies": "Python, NLTK, Scikit-learn",
                "outcome": "Ranked candidates",
                "github_link": "https://github.com/aarav/matcher"
            }
        ],
        "experience": [
            {
                "company": "TechSphere",
                "role": "Data Science Intern",
                "duration": "6 Months",
                "responsibilities": "Built automated data ingestion pipelines and dashboards.",
                "achievements": "Reduced latency by 20%."
            }
        ],
        "certifications": [
            {
                "name": "Machine Learning Specialization",
                "issuer": "Coursera",
                "completion_date": "2023"
            }
        ],
        "achievements": "• 1st place in University Hackathon"
    }

    report = ResumeQualityChecker.evaluate(sample_resume)
    print(f"Resume Quality Score: {report['score']}/100 ({report['grade']})")
    print("Strengths:", len(report['strengths']), report['strengths'][:2])
    print("Issues:", len(report['issues']))
    print("Suggestions:", len(report['suggestions']))
    assert report['score'] >= 80, f"Expected high quality score, got {report['score']}"
    print("✓ Quality checker test passed!")

    print("\n" + "=" * 60)
    print("TEST 3: HTML Preview for All 4 Templates")
    print("=" * 60)
    for template_id in ["modern_professional", "ats_friendly", "fresher_student", "experienced_professional"]:
        html = ResumeTemplateManager.render_html_preview(sample_resume, template_id=template_id)
        assert len(html) > 500, f"HTML preview for {template_id} too short"
        assert sample_resume['full_name'] in html
        print(f"✓ HTML preview generated for template: {template_id} ({len(html)} chars)")

    print("\n" + "=" * 60)
    print("TEST 4: ReportLab PDF Generation for All 4 Templates")
    print("=" * 60)
    os.makedirs("uploads", exist_ok=True)
    for template_id in ["modern_professional", "ats_friendly", "fresher_student", "experienced_professional"]:
        pdf_bytes = ResumePDFGenerator.generate_pdf(sample_resume, template_id=template_id)
        assert len(pdf_bytes) > 1000, f"PDF bytes for {template_id} too small"
        test_path = os.path.join("uploads", f"test_{template_id}.pdf")
        with open(test_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"✓ PDF successfully generated for template: {template_id} ({len(pdf_bytes)} bytes) -> {test_path}")

    print("\n" + "=" * 60)
    print("TEST 5: SQLite Database Persistence & Synchronization")
    print("=" * 60)
    database.init_db()
    # Use candidate user (user_id = 1)
    user_id = 1
    sample_resume['template_id'] = "modern_professional"
    sample_resume['quality_score'] = report['score']

    profile_id = database.save_resume_builder_profile(user_id, sample_resume)
    print(f"✓ Saved profile #{profile_id} to database")

    loaded_profile = database.get_resume_builder_profile(user_id)
    assert loaded_profile is not None
    assert loaded_profile['full_name'] == sample_resume['full_name']
    assert len(loaded_profile['education']) >= 1
    assert len(loaded_profile['projects']) >= 1
    print(f"✓ Loaded profile from DB: Name='{loaded_profile['full_name']}', Education count={len(loaded_profile['education'])}, Projects count={len(loaded_profile['projects'])}")

    # Verify candidate table synchronization
    cand = database.get_candidate_profile(user_id)
    assert cand is not None
    print(f"✓ Candidate table synchronized: Skills='{cand['skills'][:40]}...', Education='{cand['education']}'")

    print("\n" + "=" * 60)
    print("🎉 ALL 5 TEST SUITES PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
