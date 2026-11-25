"""
Database Module for AI-Powered Resume & Job Matching System
Handles SQLite database connection, schema setup, CRUD operations, and initial data seeding.
"""

import sqlite3
import os
import hashlib
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def get_connection():
    """Return an active connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = "ai_recruitment_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def init_db():
    """
    Initialize SQLite database tables and seed sample data if tables are empty.
    Creates tables:
    - users
    - candidates
    - recruiters
    - resumes
    - jobs
    - skills
    - job_applications
    - candidate_matches
    - shortlisted_candidates
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Job Seeker', 'Recruiter')),
        full_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Candidates Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        location TEXT,
        education TEXT,
        experience_years REAL DEFAULT 0,
        current_role TEXT,
        bio TEXT,
        skills TEXT,
        resume_id INTEGER,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 3. Recruiters Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recruiters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        company_name TEXT NOT NULL,
        department TEXT,
        company_website TEXT,
        contact_phone TEXT,
        location TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 4. Resumes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        raw_text TEXT NOT NULL,
        parsed_json TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )
    """)

    # 5. Skills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT,
        importance_weight INTEGER DEFAULT 5,
        recommended_course TEXT,
        course_platform TEXT,
        course_url TEXT
    )
    """)

    # 6. Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recruiter_id INTEGER,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        category TEXT NOT NULL,
        location TEXT,
        job_type TEXT DEFAULT 'Hybrid',
        experience_level TEXT DEFAULT 'Mid',
        min_experience_years REAL DEFAULT 0,
        salary_range TEXT,
        required_skills TEXT NOT NULL,
        qualifications TEXT,
        description TEXT,
        responsibilities TEXT,
        status TEXT DEFAULT 'Active',
        posted_date TEXT,
        FOREIGN KEY (recruiter_id) REFERENCES recruiters(id) ON DELETE SET NULL
    )
    """)

    # 7. Job Applications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        candidate_id INTEGER NOT NULL,
        match_score REAL DEFAULT 0.0,
        status TEXT DEFAULT 'Applied' CHECK(status IN ('Applied', 'Under Review', 'Shortlisted', 'Rejected')),
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        UNIQUE(job_id, candidate_id),
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )
    """)

    # 8. Candidate Matches (Cached calculations)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        candidate_id INTEGER NOT NULL,
        match_score REAL NOT NULL,
        matched_skills TEXT,
        missing_skills TEXT,
        explanation TEXT,
        calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(job_id, candidate_id),
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )
    """)

    # 9. Shortlisted Candidates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shortlisted_candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recruiter_id INTEGER,
        job_id INTEGER NOT NULL,
        candidate_id INTEGER NOT NULL,
        match_score REAL,
        shortlist_reason TEXT,
        shortlisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(job_id, candidate_id),
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )
    """)

    # 10. Resume Profiles (For AI Resume Builder)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        location TEXT,
        linkedin TEXT,
        github TEXT,
        portfolio TEXT,
        career_objective TEXT,
        summary TEXT,
        technical_skills TEXT,
        soft_skills TEXT,
        template_id TEXT DEFAULT 'modern_professional',
        quality_score REAL DEFAULT 0.0,
        achievements TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 11. Resume Education (Multiple entries per profile)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        degree TEXT NOT NULL,
        institution TEXT NOT NULL,
        passing_year TEXT,
        score TEXT,
        coursework TEXT,
        FOREIGN KEY (profile_id) REFERENCES resume_profiles(id) ON DELETE CASCADE
    )
    """)

    # 12. Resume Projects (Multiple entries per profile)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        technologies TEXT,
        outcome TEXT,
        github_link TEXT,
        FOREIGN KEY (profile_id) REFERENCES resume_profiles(id) ON DELETE CASCADE
    )
    """)

    # 13. Resume Experience / Internships (Multiple entries per profile)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_experience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        duration TEXT,
        responsibilities TEXT,
        achievements TEXT,
        FOREIGN KEY (profile_id) REFERENCES resume_profiles(id) ON DELETE CASCADE
    )
    """)

    # 14. Resume Certifications (Multiple entries per profile)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        issuer TEXT,
        completion_date TEXT,
        FOREIGN KEY (profile_id) REFERENCES resume_profiles(id) ON DELETE CASCADE
    )
    """)

    # 15. Resume Templates (Catalog of ATS and visual templates)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_templates (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT DEFAULT 'Modern',
        is_active INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    seed_initial_data(conn)
    conn.close()


def seed_initial_data(conn):
    """Seed initial skills, jobs, default users, and sample applications if empty."""
    cursor = conn.cursor()

    # 1. Seed Skills if empty
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        skills_csv = os.path.join(os.path.dirname(__file__), "dataset", "skills.csv")
        if os.path.exists(skills_csv):
            df_skills = pd.read_csv(skills_csv)
            for _, row in df_skills.iterrows():
                cursor.execute("""
                INSERT OR IGNORE INTO skills 
                (skill_name, category, sub_category, importance_weight, recommended_course, course_platform, course_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row['skill_name']).strip(),
                    str(row.get('category', 'Technical')).strip(),
                    str(row.get('sub_category', '')).strip(),
                    int(row.get('importance_weight', 5)),
                    str(row.get('recommended_course', '')).strip(),
                    str(row.get('course_platform', 'Coursera')).strip(),
                    str(row.get('course_url', '')).strip()
                ))
            conn.commit()

    # 2. Seed Default Recruiter & Candidate Accounts
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Default Candidate
        cand_pass = hash_password("Password123")
        cursor.execute("""
        INSERT INTO users (email, password_hash, role, full_name)
        VALUES (?, ?, 'Job Seeker', ?)
        """, ("candidate@test.com", cand_pass, "Aarav Sharma"))
        cand_user_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO candidates (user_id, full_name, email, phone, location, education, experience_years, current_role, bio, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cand_user_id,
            "Aarav Sharma",
            "candidate@test.com",
            "+91 98765 43210",
            "Bangalore, India",
            "Master of Computer Applications (MCA) in Data Science, 2024",
            1.5,
            "Junior Data Scientist",
            "Passionate MCA Data Science postgraduate with practical skills in NLP, Machine Learning, Python, and SQL.",
            "Python, Machine Learning, Scikit-learn, Pandas, NumPy, SQL, Tableau, Statistics, Git, NLP, Problem Solving, Communication"
        ))

        # Default Recruiter
        rec_pass = hash_password("Password123")
        cursor.execute("""
        INSERT INTO users (email, password_hash, role, full_name)
        VALUES (?, ?, 'Recruiter', ?)
        """, ("recruiter@test.com", rec_pass, "Pooja Verma"))
        rec_user_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO recruiters (user_id, company_name, department, company_website, contact_phone, location)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            rec_user_id,
            "TechSphere Solutions",
            "Talent Acquisition",
            "https://techspheresolutions.example.com",
            "+91 80 4123 4567",
            "Bengaluru, Karnataka, India"
        ))
        conn.commit()

    # 3. Seed Candidates from CSV if needed
    cursor.execute("SELECT COUNT(*) FROM candidates")
    cand_count = cursor.fetchone()[0]
    if cand_count <= 1:
        candidates_csv = os.path.join(os.path.dirname(__file__), "dataset", "candidates.csv")
        if os.path.exists(candidates_csv):
            df_cands = pd.read_csv(candidates_csv)
            for _, row in df_cands.iterrows():
                email = str(row['email']).strip()
                # Check if user already exists
                cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                existing_user = cursor.fetchone()
                if not existing_user:
                    p_hash = hash_password("Password123")
                    cursor.execute("""
                    INSERT INTO users (email, password_hash, role, full_name)
                    VALUES (?, ?, 'Job Seeker', ?)
                    """, (email, p_hash, str(row['name'])))
                    uid = cursor.lastrowid
                    cursor.execute("""
                    INSERT INTO candidates (user_id, full_name, email, phone, location, education, experience_years, current_role, bio, skills)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        uid,
                        str(row['name']),
                        email,
                        str(row.get('phone', '')),
                        str(row.get('location', '')),
                        str(row.get('education', '')),
                        float(row.get('experience_years', 1)),
                        str(row.get('current_role', '')),
                        str(row.get('bio', '')),
                        str(row.get('skills', ''))
                    ))
            conn.commit()

    # 4. Seed Jobs from CSV if empty
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        jobs_csv = os.path.join(os.path.dirname(__file__), "dataset", "jobs.csv")
        if os.path.exists(jobs_csv):
            df_jobs = pd.read_csv(jobs_csv)
            for _, row in df_jobs.iterrows():
                cursor.execute("""
                INSERT INTO jobs 
                (recruiter_id, title, company, category, location, job_type, experience_level, min_experience_years, salary_range, required_skills, qualifications, description, responsibilities, status, posted_date)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active', ?)
                """, (
                    str(row['title']).strip(),
                    str(row['company']).strip(),
                    str(row['category']).strip(),
                    str(row.get('location', 'India')).strip(),
                    str(row.get('job_type', 'Hybrid')).strip(),
                    str(row.get('experience_level', 'Mid')).strip(),
                    float(row.get('min_experience_years', 0)),
                    str(row.get('salary_range', 'Negotiable')).strip(),
                    str(row['required_skills']).strip(),
                    str(row.get('qualifications', '')).strip(),
                    str(row.get('description', '')).strip(),
                    str(row.get('responsibilities', '')).strip(),
                    str(row.get('posted_date', '2026-10-15')).strip()
                ))
            conn.commit()

    # 5. Seed some sample job applications for realistic recruiter dashboard experience
    cursor.execute("SELECT COUNT(*) FROM job_applications")
    if cursor.fetchone()[0] == 0:
        # Connect first 5 candidates to jobs 1, 2, 3, 4, 5
        cursor.execute("SELECT id FROM candidates LIMIT 6")
        cand_ids = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT id FROM jobs LIMIT 10")
        job_ids = [r[0] for r in cursor.fetchall()]

        statuses = ['Applied', 'Under Review', 'Shortlisted', 'Shortlisted', 'Applied', 'Applied']
        scores = [85.5, 78.0, 92.0, 68.5, 88.0, 74.5]

        for i, c_id in enumerate(cand_ids):
            for j_offset in range(2):
                j_id = job_ids[(i + j_offset) % len(job_ids)]
                st = statuses[i % len(statuses)]
                sc = scores[i % len(scores)]
                cursor.execute("""
                INSERT OR IGNORE INTO job_applications (job_id, candidate_id, match_score, status, notes)
                VALUES (?, ?, ?, ?, ?)
                """, (j_id, c_id, sc, st, "Evaluated with AI dynamic matching model."))
                
                if st == 'Shortlisted':
                    cursor.execute("""
                    INSERT OR IGNORE INTO shortlisted_candidates (recruiter_id, job_id, candidate_id, match_score, shortlist_reason)
                    VALUES (1, ?, ?, ?, ?)
                    """, (j_id, c_id, sc, "Strong match on core technical skills and educational background."))
        conn.commit()

    # 6. Seed Resume Templates if empty
    cursor.execute("SELECT COUNT(*) FROM resume_templates")
    if cursor.fetchone()[0] == 0:
        templates = [
            ("modern_professional", "Modern Professional", "Clean two-tone layout with subtle navy accents and visual section dividers. Ideal for tech and corporate roles.", "Modern"),
            ("ats_friendly", "Simple ATS-Friendly", "Single-column linear structure with standardized headings. Maximizes parse rate across all Applicant Tracking Systems.", "ATS-Friendly"),
            ("fresher_student", "Fresher / Student Resume", "Emphasizes education, academic projects, coursework, and campus achievements first. Tailored for graduates.", "Fresher"),
            ("experienced_professional", "Experienced Professional", "Prioritizes work experience, quantifiable impact metrics, leadership roles, and technical stack depth.", "Experienced")
        ]
        for t_id, name, desc, cat in templates:
            cursor.execute("INSERT OR IGNORE INTO resume_templates (id, name, description, category) VALUES (?, ?, ?, ?)", (t_id, name, desc, cat))
        conn.commit()


# -------------------------------------------------------------------------
# Helper Query Functions
# -------------------------------------------------------------------------

def get_user_by_email(email: str):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),)).fetchone()
    conn.close()
    return user


def create_user(email: str, password: str, role: str, full_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    p_hash = hash_password(password)
    try:
        cursor.execute("""
        INSERT INTO users (email, password_hash, role, full_name)
        VALUES (?, ?, ?, ?)
        """, (email.strip(), p_hash, role, full_name.strip()))
        user_id = cursor.lastrowid

        if role == 'Job Seeker':
            cursor.execute("""
            INSERT INTO candidates (user_id, full_name, email, skills)
            VALUES (?, ?, ?, '')
            """, (user_id, full_name.strip(), email.strip()))
        else:
            cursor.execute("""
            INSERT INTO recruiters (user_id, company_name)
            VALUES (?, 'My Organization')
            """, (user_id,))
            
        conn.commit()
        return user_id, None
    except sqlite3.IntegrityError:
        return None, "Email address already exists."
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()


def get_candidate_profile(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM candidates WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def update_candidate_profile(candidate_id: int, full_name: str, phone: str, location: str,
                             education: str, experience_years: float, current_role: str,
                             bio: str, skills: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE candidates
    SET full_name = ?, phone = ?, location = ?, education = ?, experience_years = ?,
        current_role = ?, bio = ?, skills = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (full_name, phone, location, education, experience_years, current_role, bio, skills, candidate_id))
    conn.commit()
    conn.close()


def get_all_jobs(category=None, search_term=None, status='Active'):
    conn = get_connection()
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    if search_term:
        query += " AND (title LIKE ? OR company LIKE ? OR required_skills LIKE ? OR description LIKE ?)"
        wildcard = f"%{search_term}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])
    
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def get_job_by_id(job_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    conn.close()
    return row


def create_job(recruiter_id: int, title: str, company: str, category: str, location: str,
               job_type: str, experience_level: str, min_exp: float, salary_range: str,
               required_skills: str, qualifications: str, description: str, responsibilities: str):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
    INSERT INTO jobs 
    (recruiter_id, title, company, category, location, job_type, experience_level, min_experience_years, salary_range, required_skills, qualifications, description, responsibilities, posted_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (recruiter_id, title, company, category, location, job_type, experience_level, min_exp, salary_range, required_skills, qualifications, description, responsibilities, today))
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id


def update_job_status(job_id: int, status: str):
    conn = get_connection()
    conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()


def save_candidate_resume(candidate_id: int, file_name: str, file_path: str, raw_text: str, parsed_json: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO resumes (candidate_id, file_name, file_path, raw_text, parsed_json)
    VALUES (?, ?, ?, ?, ?)
    """, (candidate_id, file_name, file_path, raw_text, parsed_json))
    resume_id = cursor.lastrowid
    
    cursor.execute("UPDATE candidates SET resume_id = ? WHERE id = ?", (resume_id, candidate_id))
    conn.commit()
    conn.close()
    return resume_id


def apply_for_job(job_id: int, candidate_id: int, match_score: float):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO job_applications (job_id, candidate_id, match_score, status)
        VALUES (?, ?, ?, 'Applied')
        ON CONFLICT(job_id, candidate_id) DO UPDATE SET
        match_score = excluded.match_score
        """, (job_id, candidate_id, match_score))
        conn.commit()
        return True, "Application submitted successfully!"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def get_candidate_applications(candidate_id: int):
    conn = get_connection()
    query = """
    SELECT a.*, j.title, j.company, j.location, j.category, j.salary_range
    FROM job_applications a
    JOIN jobs j ON a.job_id = j.id
    WHERE a.candidate_id = ?
    ORDER BY a.applied_at DESC
    """
    rows = conn.execute(query, (candidate_id,)).fetchall()
    conn.close()
    return rows


def get_job_applications_for_recruiter(job_id=None):
    conn = get_connection()
    query = """
    SELECT a.*, c.full_name as candidate_name, c.email as candidate_email,
           c.education, c.experience_years, c.skills as candidate_skills,
           c.phone, c.location as candidate_location,
           j.title as job_title, j.company as job_company, j.required_skills as required_skills
    FROM job_applications a
    JOIN candidates c ON a.candidate_id = c.id
    JOIN jobs j ON a.job_id = j.id
    WHERE 1=1
    """
    params = []
    if job_id:
        query += " AND a.job_id = ?"
        params.append(job_id)
    query += " ORDER BY a.match_score DESC, a.applied_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def update_application_status(app_id: int, new_status: str, notes: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    if notes:
        cursor.execute("UPDATE job_applications SET status = ?, notes = ? WHERE id = ?", (new_status, notes, app_id))
    else:
        cursor.execute("UPDATE job_applications SET status = ? WHERE id = ?", (new_status, app_id))
    
    # If shortlisted, update shortlisted_candidates table
    if new_status == 'Shortlisted':
        cursor.execute("SELECT job_id, candidate_id, match_score FROM job_applications WHERE id = ?", (app_id,))
        app = cursor.fetchone()
        if app:
            cursor.execute("""
            INSERT OR REPLACE INTO shortlisted_candidates (recruiter_id, job_id, candidate_id, match_score, shortlist_reason)
            VALUES (1, ?, ?, ?, 'Recruiter approved through applicant review')
            """, (app['job_id'], app['candidate_id'], app['match_score']))
    conn.commit()
    conn.close()


def get_all_skills_catalog():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM skills ORDER BY skill_name ASC").fetchall()
    conn.close()
    return rows


# -------------------------------------------------------------------------
# Resume Builder Persistence Helpers
# -------------------------------------------------------------------------

def save_resume_builder_profile(user_id: int, data: dict) -> int:
    """
    Persist or update the complete resume builder profile and its relational
    child records (education, projects, experience, certifications) in SQLite.
    Also synchronizes skills, education, and bio with the candidate record.
    """
    conn = get_connection()
    cursor = conn.cursor()

    full_name = data.get('full_name', '').strip() or 'Candidate'
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    location = data.get('location', '').strip()
    linkedin = data.get('linkedin', '').strip()
    github = data.get('github', '').strip()
    portfolio = data.get('portfolio', '').strip()
    career_objective = data.get('career_objective', '').strip()
    summary = data.get('summary', '').strip()
    tech_skills = data.get('technical_skills', '')
    if isinstance(tech_skills, list):
        tech_skills = ", ".join(tech_skills)
    soft_skills = data.get('soft_skills', '')
    if isinstance(soft_skills, list):
        soft_skills = ", ".join(soft_skills)
    template_id = data.get('template_id', 'modern_professional')
    quality_score = float(data.get('quality_score', 0.0))
    achievements = data.get('achievements', '')

    cursor.execute("""
    INSERT INTO resume_profiles 
    (user_id, full_name, email, phone, location, linkedin, github, portfolio,
     career_objective, summary, technical_skills, soft_skills, template_id, quality_score, achievements, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(user_id) DO UPDATE SET
        full_name = excluded.full_name,
        email = excluded.email,
        phone = excluded.phone,
        location = excluded.location,
        linkedin = excluded.linkedin,
        github = excluded.github,
        portfolio = excluded.portfolio,
        career_objective = excluded.career_objective,
        summary = excluded.summary,
        technical_skills = excluded.technical_skills,
        soft_skills = excluded.soft_skills,
        template_id = excluded.template_id,
        quality_score = excluded.quality_score,
        achievements = excluded.achievements,
        updated_at = CURRENT_TIMESTAMP
    """, (user_id, full_name, email, phone, location, linkedin, github, portfolio,
          career_objective, summary, tech_skills, soft_skills, template_id, quality_score, achievements))

    # Retrieve profile_id
    cursor.execute("SELECT id FROM resume_profiles WHERE user_id = ?", (user_id,))
    profile_id = cursor.fetchone()[0]

    # Recreate child tables for this profile
    cursor.execute("DELETE FROM resume_education WHERE profile_id = ?", (profile_id,))
    for edu in data.get('education', []):
        if edu.get('degree') or edu.get('institution'):
            cursor.execute("""
            INSERT INTO resume_education (profile_id, degree, institution, passing_year, score, coursework)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (profile_id, edu.get('degree', ''), edu.get('institution', ''),
                  str(edu.get('passing_year', '')), str(edu.get('score', '')), edu.get('coursework', '')))

    cursor.execute("DELETE FROM resume_projects WHERE profile_id = ?", (profile_id,))
    for proj in data.get('projects', []):
        if proj.get('title'):
            cursor.execute("""
            INSERT INTO resume_projects (profile_id, title, description, technologies, outcome, github_link)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (profile_id, proj.get('title', ''), proj.get('description', ''),
                  proj.get('technologies', ''), proj.get('outcome', ''), proj.get('github_link', '')))

    cursor.execute("DELETE FROM resume_experience WHERE profile_id = ?", (profile_id,))
    for exp in data.get('experience', []):
        if exp.get('company') or exp.get('role'):
            cursor.execute("""
            INSERT INTO resume_experience (profile_id, company, role, duration, responsibilities, achievements)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (profile_id, exp.get('company', ''), exp.get('role', ''),
                  exp.get('duration', ''), exp.get('responsibilities', ''), exp.get('achievements', '')))

    cursor.execute("DELETE FROM resume_certifications WHERE profile_id = ?", (profile_id,))
    for cert in data.get('certifications', []):
        if cert.get('name'):
            cursor.execute("""
            INSERT INTO resume_certifications (profile_id, name, issuer, completion_date)
            VALUES (?, ?, ?, ?)
            """, (profile_id, cert.get('name', ''), cert.get('issuer', ''), cert.get('completion_date', '')))

    conn.commit()
    conn.close()

    # Synchronize candidate profile with resume data
    sync_resume_to_candidate(user_id, data)
    return profile_id


def sync_resume_to_candidate(user_id: int, data: dict):
    """
    Sync newly built or improved resume details with the candidate profile table
    so the AI Job Matching engine instantly reflects the updated skillset,
    qualifications, and experience.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Combine technical and soft skills
    tech = [s.strip() for s in data.get('technical_skills', '').split(',') if s.strip()] if isinstance(data.get('technical_skills'), str) else data.get('technical_skills', [])
    soft = [s.strip() for s in data.get('soft_skills', '').split(',') if s.strip()] if isinstance(data.get('soft_skills'), str) else data.get('soft_skills', [])
    combined_skills = ", ".join(list(dict.fromkeys(tech + soft)))

    # Get primary education string
    edu_list = data.get('education', [])
    edu_str = ""
    if edu_list:
        edu_str = f"{edu_list[0].get('degree', '')} - {edu_list[0].get('institution', '')}"

    # Calculate experience years approximately
    exp_list = data.get('experience', [])
    total_exp_years = 0.5 * len(exp_list)  # default estimate based on internships/roles

    cursor.execute("""
    UPDATE candidates
    SET full_name = COALESCE(NULLIF(?, ''), full_name),
        phone = COALESCE(NULLIF(?, ''), phone),
        location = COALESCE(NULLIF(?, ''), location),
        education = CASE WHEN ? != '' THEN ? ELSE education END,
        experience_years = CASE WHEN ? > 0 THEN ? ELSE experience_years END,
        bio = COALESCE(NULLIF(?, ''), bio),
        skills = CASE WHEN ? != '' THEN ? ELSE skills END,
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = ?
    """, (
        data.get('full_name', ''),
        data.get('phone', ''),
        data.get('location', ''),
        edu_str, edu_str,
        total_exp_years, total_exp_years,
        data.get('summary', '') or data.get('career_objective', ''),
        combined_skills, combined_skills,
        user_id
    ))
    conn.commit()
    conn.close()


def get_resume_builder_profile(user_id: int) -> dict:
    """
    Retrieve complete structured resume profile for a user from SQLite.
    Returns None if no profile exists yet.
    """
    conn = get_connection()
    row = conn.execute("SELECT * FROM resume_profiles WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        conn.close()
        return None

    profile_id = row['id']
    profile_data = dict(row)

    # Fetch education
    edu_rows = conn.execute("SELECT * FROM resume_education WHERE profile_id = ? ORDER BY id ASC", (profile_id,)).fetchall()
    profile_data['education'] = [dict(r) for r in edu_rows]

    # Fetch projects
    proj_rows = conn.execute("SELECT * FROM resume_projects WHERE profile_id = ? ORDER BY id ASC", (profile_id,)).fetchall()
    profile_data['projects'] = [dict(r) for r in proj_rows]

    # Fetch experience
    exp_rows = conn.execute("SELECT * FROM resume_experience WHERE profile_id = ? ORDER BY id ASC", (profile_id,)).fetchall()
    profile_data['experience'] = [dict(r) for r in exp_rows]

    # Fetch certifications
    cert_rows = conn.execute("SELECT * FROM resume_certifications WHERE profile_id = ? ORDER BY id ASC", (profile_id,)).fetchall()
    profile_data['certifications'] = [dict(r) for r in cert_rows]

    conn.close()
    return profile_data


def get_all_resume_templates() -> list:
    """Fetch all active resume templates from SQLite."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM resume_templates WHERE is_active = 1 ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


class DatabaseManager:
    """
    Object-Oriented Database Manager Class.
    Encapsulates SQLite connection management, table lifecycle,
    and CRUD operations across users, jobs, candidates, and applications.
    """
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        """Obtain a SQLite database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self):
        """Initialize database schema and seed initial records."""
        init_db()

    def get_user_by_email(self, email: str):
        """Fetch user record by email address."""
        return get_user_by_email(email)

    def register_user(self, email: str, password: str, role: str, full_name: str):
        """Create new user account and associated role profile."""
        return create_user(email, password, role, full_name)

    def get_candidate(self, user_id: int):
        """Fetch candidate profile by user ID."""
        return get_candidate_profile(user_id)

    def update_candidate(self, candidate_id: int, full_name: str, phone: str, location: str,
                         education: str, experience_years: float, current_role: str,
                         bio: str, skills: str):
        """Update candidate details."""
        update_candidate_profile(candidate_id, full_name, phone, location, education, experience_years, current_role, bio, skills)

    def get_jobs(self, category=None, search_term=None, status='Active'):
        """Query jobs with optional filtering."""
        return get_all_jobs(category, search_term, status)

    def create_job(self, recruiter_id: int, title: str, company: str, category: str, location: str,
                   job_type: str, experience_level: str, min_exp: float, salary_range: str,
                   required_skills: str, qualifications: str, description: str, responsibilities: str):
        """Create and publish a new job opening."""
        return create_job(recruiter_id, title, company, category, location, job_type, experience_level, min_exp, salary_range, required_skills, qualifications, description, responsibilities)

    def apply(self, job_id: int, candidate_id: int, match_score: float):
        """Submit a candidate application for a job."""
        return apply_for_job(job_id, candidate_id, match_score)

    def save_resume_profile(self, user_id: int, data: dict) -> int:
        """Save structured resume builder profile."""
        return save_resume_builder_profile(user_id, data)

    def get_resume_profile(self, user_id: int) -> dict:
        """Fetch structured resume builder profile."""
        return get_resume_builder_profile(user_id)

    def get_templates(self) -> list:
        """Fetch all resume templates."""
        return get_all_resume_templates()


