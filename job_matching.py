"""
Job Matching Module for AI-Powered Resume & Job Matching System
Implements TF-IDF vectorization, Cosine Similarity, and weighted skill overlap
to provide dynamic, explainable matching scores between resumes and job postings.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_processing import clean_text
import database


def calculate_skill_overlap(candidate_skills: list, required_skills_str: str) -> tuple:
    """
    Compare candidate skills against the comma-separated required job skills.
    Returns:
    - overlap_ratio: float between 0.0 and 1.0
    - matched_skills: list of matched skill names
    - missing_skills: list of missing skill names
    """
    if not required_skills_str:
        return 1.0, candidate_skills, []
    
    # Parse required skills
    req_skills = [s.strip() for s in required_skills_str.split(',') if s.strip()]
    if not req_skills:
        return 1.0, candidate_skills, []

    cand_set = {s.strip().lower() for s in candidate_skills}
    matched = []
    missing = []

    for req in req_skills:
        r_clean = req.strip().lower()
        # Direct match or substring match for variants (e.g. "React" matches "React.js")
        if r_clean in cand_set or any(r_clean in c or c in r_clean for c in cand_set):
            matched.append(req.strip())
        else:
            missing.append(req.strip())

    ratio = len(matched) / len(req_skills) if req_skills else 0.0
    return ratio, matched, missing


def calculate_experience_fit(cand_exp: float, job_min_exp: float) -> float:
    """
    Calculate how well the candidate's experience matches the job requirement.
    Score: 1.0 if meeting or exceeding requirement, proportional if lower.
    """
    if job_min_exp <= 0:
        return 1.0
    if cand_exp >= job_min_exp:
        return 1.0
    # Proportional credit
    return max(0.2, cand_exp / job_min_exp)


def calculate_dynamic_match(candidate_profile: dict, job: dict) -> dict:
    """
    Dynamically calculate matching percentage between a candidate and a job.
    Formula:
      Composite Match Score = (0.50 * Skill Overlap) + (0.35 * TF-IDF Cosine Similarity) + (0.15 * Experience Fit)
    All components are calculated dynamically from actual content.
    """
    # 1. Parse Skills
    skills_raw = candidate_profile.get('skills', '')
    if isinstance(skills_raw, str):
        candidate_skills = [s.strip() for s in skills_raw.split(',') if s.strip()]
    elif isinstance(skills_raw, list):
        candidate_skills = skills_raw
    else:
        candidate_skills = []

    required_skills_str = job.get('required_skills', '')
    skill_ratio, matched_skills, missing_skills = calculate_skill_overlap(candidate_skills, required_skills_str)

    # 2. Textual TF-IDF Cosine Similarity
    # Build candidate representation text
    cand_bio = candidate_profile.get('bio', '')
    cand_edu = candidate_profile.get('education', '')
    cand_role = candidate_profile.get('current_role', '')
    cand_text = f"{cand_role} {' '.join(candidate_skills)} {cand_edu} {cand_bio}"
    cand_cleaned = clean_text(cand_text)

    # Build job representation text
    job_title = job.get('title', '')
    job_desc = job.get('description', '')
    job_resp = job.get('responsibilities', '')
    job_qual = job.get('qualifications', '')
    job_text = f"{job_title} {job_desc} {job_resp} {required_skills_str} {job_qual}"
    job_cleaned = clean_text(job_text)

    tfidf_sim = 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([cand_cleaned, job_cleaned])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        tfidf_sim = float(sim_matrix[0][0])
    except Exception:
        # Fallback if vocabulary is too sparse
        tfidf_sim = skill_ratio

    # 3. Experience Fit
    cand_exp = float(candidate_profile.get('experience_years', 1.0))
    job_min_exp = float(job.get('min_experience_years', 0.0))
    exp_fit = calculate_experience_fit(cand_exp, job_min_exp)

    # 4. Weighted Composite Score
    # 50% Skill Match, 35% TF-IDF Cosine, 15% Experience Fit
    final_score = (0.50 * skill_ratio) + (0.35 * tfidf_sim) + (0.15 * exp_fit)
    final_percentage = round(min(final_score * 100, 100.0), 1)

    # Explainability breakdown
    explanation = (
        f"Matching Score Breakdown: "
        f"Skill Overlap: {int(skill_ratio * 100)}% ({len(matched_skills)}/{len(matched_skills) + len(missing_skills)} required skills matched), "
        f"NLP Content Similarity: {int(tfidf_sim * 100)}%, "
        f"Experience Level Fit: {int(exp_fit * 100)}% ({cand_exp} yrs vs {job_min_exp} yrs required)."
    )

    return {
        "job_id": job.get('id'),
        "match_percentage": final_percentage,
        "skill_match_ratio": round(skill_ratio * 100, 1),
        "tfidf_similarity": round(tfidf_sim * 100, 1),
        "experience_fit": round(exp_fit * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "explanation": explanation
    }


def find_matching_jobs_for_candidate(candidate_profile: dict, top_n: int = 10, category_filter: str = "All") -> list:
    """
    Scan all active jobs and return ranked job recommendations with matching breakdown.
    """
    jobs = database.get_all_jobs(category=category_filter, status="Active")
    results = []

    for job in jobs:
        job_dict = dict(job)
        match_info = calculate_dynamic_match(candidate_profile, job_dict)
        combined = {**job_dict, **match_info}
        results.append(combined)

    # Sort descending by match percentage
    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results[:top_n]


def rank_candidates_for_job(job_id: int) -> list:
    """
    Rank all available candidates for a specific job posting.
    Used by recruiters in candidate ranking and shortlisting.
    """
    job = database.get_job_by_id(job_id)
    if not job:
        return []
    job_dict = dict(job)

    conn = database.get_connection()
    candidates = conn.execute("SELECT * FROM candidates").fetchall()
    conn.close()

    ranked = []
    for cand in candidates:
        c_dict = dict(cand)
        match_info = calculate_dynamic_match(c_dict, job_dict)
        ranked.append({
            "candidate_id": c_dict['id'],
            "name": c_dict['full_name'],
            "email": c_dict['email'],
            "phone": c_dict['phone'],
            "education": c_dict['education'],
            "experience_years": c_dict['experience_years'],
            "current_role": c_dict['current_role'],
            "skills": c_dict['skills'],
            "match_score": match_info['match_percentage'],
            "skill_match_ratio": match_info['skill_match_ratio'],
            "matched_skills": match_info['matched_skills'],
            "missing_skills": match_info['missing_skills'],
            "explanation": match_info['explanation']
        })

    ranked.sort(key=lambda x: x['match_score'], reverse=True)
    return ranked


class JobMatcher:
    """
    Object-Oriented Job Matching & Candidate Screening Engine.
    Implements TF-IDF vectorization, Cosine Similarity, skill overlap ratio,
    and experience fitting to produce explainable match scores and rankings.
    """
    def __init__(self, skill_weight: float = 0.50, tfidf_weight: float = 0.35, exp_weight: float = 0.15):
        self.skill_weight = skill_weight
        self.tfidf_weight = tfidf_weight
        self.exp_weight = exp_weight

    def calculate_skill_overlap(self, candidate_skills: list, required_skills_str: str) -> tuple:
        """Calculate skill overlap ratio, matched and missing skills."""
        return calculate_skill_overlap(candidate_skills, required_skills_str)

    def calculate_experience_fit(self, cand_exp: float, job_min_exp: float) -> float:
        """Calculate experience level fitting score."""
        return calculate_experience_fit(cand_exp, job_min_exp)

    def match(self, candidate_profile: dict, job: dict) -> dict:
        """Calculate dynamic composite match score between a candidate and a job."""
        return calculate_dynamic_match(candidate_profile, job)

    def recommend_jobs(self, candidate_profile: dict, top_n: int = 10, category_filter: str = "All") -> list:
        """Rank and recommend jobs for a candidate profile."""
        return find_matching_jobs_for_candidate(candidate_profile, top_n, category_filter)

    def rank_candidates(self, job_id: int) -> list:
        """Rank all candidates for a specific job vacancy."""
        return rank_candidates_for_job(job_id)

