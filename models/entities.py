"""
Data Entity Models for AI-Powered Resume & Job Matching System
Defines OOP classes representing domain entities across the recruitment lifecycle.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class User:
    """Represents an authenticated platform user."""
    id: Optional[int]
    email: str
    role: str  # 'Job Seeker' or 'Recruiter'
    full_name: str
    created_at: Optional[str] = None


@dataclass
class Candidate:
    """Represents a job seeker profile with educational and skill attributes."""
    id: Optional[int]
    user_id: int
    full_name: str
    email: str
    phone: str = ""
    location: str = ""
    education: str = ""
    experience_years: float = 0.0
    current_role: str = ""
    bio: str = ""
    skills: List[str] = field(default_factory=list)
    resume_id: Optional[int] = None
    updated_at: Optional[str] = None


@dataclass
class Recruiter:
    """Represents an employer or talent acquisition specialist."""
    id: Optional[int]
    user_id: int
    company_name: str
    department: str = ""
    company_website: str = ""
    contact_phone: str = ""
    location: str = ""


@dataclass
class JobPosting:
    """Represents an employment opportunity posted by a recruiter."""
    id: Optional[int]
    title: str
    company: str
    category: str
    location: str = "India"
    job_type: str = "Hybrid"
    experience_level: str = "Mid"
    min_experience_years: float = 0.0
    salary_range: str = "Competitive"
    required_skills: List[str] = field(default_factory=list)
    qualifications: str = ""
    description: str = ""
    responsibilities: str = ""
    status: str = "Active"
    posted_date: Optional[str] = None
    recruiter_id: Optional[int] = 1


@dataclass
class ResumeDocument:
    """Represents an uploaded resume file and its parsed text representations."""
    id: Optional[int]
    candidate_id: int
    file_name: str
    file_path: str
    raw_text: str
    parsed_json: Optional[str] = None
    uploaded_at: Optional[str] = None


@dataclass
class JobApplication:
    """Represents a job application submitted by a candidate."""
    id: Optional[int]
    job_id: int
    candidate_id: int
    match_score: float = 0.0
    status: str = "Applied"  # Applied, Under Review, Shortlisted, Rejected
    applied_at: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class MatchResult:
    """Represents the dynamic calculation output of the AI matching algorithm."""
    job_id: int
    match_percentage: float
    skill_match_ratio: float
    tfidf_similarity: float
    experience_fit: float
    matched_skills: List[str]
    missing_skills: List[str]
    explanation: str


@dataclass
class SkillGapReport:
    """Represents the gap analysis findings between a candidate and a target role."""
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float
    gap_count: int
    status: str


@dataclass
class ResumeProfile:
    """Represents a structured resume profile created with AI Resume Builder."""
    id: Optional[int]
    user_id: int
    full_name: str
    email: str
    phone: str
    location: str
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    career_objective: str = ""
    summary: str = ""
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    template_id: str = "modern_professional"
    quality_score: float = 0.0
    education: List[dict] = field(default_factory=list)
    projects: List[dict] = field(default_factory=list)
    experience: List[dict] = field(default_factory=list)
    certifications: List[dict] = field(default_factory=list)
    achievements: str = ""


@dataclass
class ResumeTemplate:
    """Represents an ATS or visual resume layout template."""
    id: str
    name: str
    description: str
    category: str = "Modern"
    is_active: bool = True

