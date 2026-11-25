"""
Recruiter Module for AI-Powered Resume & Job Matching System
Handles job vacancy posting, applicant tracking, AI candidate ranking, shortlisting,
and explainable screening.
"""

import streamlit as st
import pandas as pd
import database
import job_matching
from skill_gap import create_gauge_chart


def render_post_job_page(recruiter_id: int):
    """Page for recruiters to post a new job vacancy."""
    st.title("📢 Post a New Job Vacancy")
    st.markdown("Publish a job opening and let our AI matching engine match and rank qualified candidates.")

    with st.form("post_job_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Job Title*", placeholder="e.g. Senior Data Scientist")
            company = st.text_input("Company Name*", placeholder="e.g. TechSphere Solutions")
            category = st.selectbox("Job Category*", [
                "Data Science & Analytics",
                "Machine Learning & AI",
                "Python & Backend Development",
                "Full-Stack Web Development",
                "Java & Enterprise Development",
                "Business Intelligence & Analysis",
                "Database Administration & Engineering",
                "Cloud Computing & DevOps",
                "Software Quality & Testing",
                "Cybersecurity & Networks"
            ])
            location = st.text_input("Job Location", value="Bengaluru, India")
            job_type = st.selectbox("Workplace Type", ["Hybrid", "Remote", "On-site"])

        with col2:
            experience_level = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead"])
            min_exp = st.number_input("Minimum Experience Required (Years)", min_value=0.0, max_value=20.0, value=2.0, step=0.5)
            salary_range = st.text_input("Salary Range", placeholder="e.g. 12 - 18 LPA")
            required_skills = st.text_area("Required Skills* (comma-separated)", placeholder="e.g. Python, Machine Learning, SQL, Scikit-learn, Git")
            qualifications = st.text_input("Qualifications", value="B.Tech / MCA / M.Sc in Computer Science or Data Science")

        description = st.text_area("Job Summary & Description*", height=120, placeholder="Describe the role, key objectives, and day-to-day impact...")
        responsibilities = st.text_area("Responsibilities (Bullet points)", height=120, placeholder="- Build and deploy machine learning models\n- Collaborate with product teams\n- Write unit tests...")

        submitted = st.form_submit_button("🚀 Publish Job Vacancy", use_container_width=True, type="primary")

        if submitted:
            if not title or not company or not required_skills or not description:
                st.error("Please fill in all required fields (marked with *).")
            else:
                job_id = database.create_job(
                    recruiter_id=recruiter_id,
                    title=title,
                    company=company,
                    category=category,
                    location=location,
                    job_type=job_type,
                    experience_level=experience_level,
                    min_exp=min_exp,
                    salary_range=salary_range,
                    required_skills=required_skills,
                    qualifications=qualifications,
                    description=description,
                    responsibilities=responsibilities
                )
                st.success(f"🎉 Job vacancy '{title}' published successfully! Job ID: #{job_id}")


def render_manage_jobs_page():
    """Manage existing job openings, view details, and toggle active/closed status."""
    st.title("💼 Manage Job Openings")
    st.markdown("Monitor your posted vacancies and review applicants.")

    jobs = database.get_all_jobs(status=None)
    if not jobs:
        st.info("No job openings found. Click 'Post a Job' to create one.")
        return

    # Filter controls
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search = st.text_input("🔍 Search jobs by title, company, or skills", "")
    with col_f2:
        status_filter = st.selectbox("Status Filter", ["All", "Active", "Closed"])

    filtered_jobs = jobs
    if search:
        search_lower = search.lower()
        filtered_jobs = [j for j in filtered_jobs if search_lower in j['title'].lower() or search_lower in j['company'].lower() or search_lower in j['required_skills'].lower()]
    if status_filter != "All":
        filtered_jobs = [j for j in filtered_jobs if j['status'] == status_filter]

    st.markdown(f"**Showing {len(filtered_jobs)} job openings**")

    for job in filtered_jobs:
        with st.expander(f"📌 {job['title']} — {job['company']} ({job['status']}) | ID #{job['id']}"):
            col1, col2, col3 = st.columns([3, 2, 1.5])
            with col1:
                st.markdown(f"**Category:** {job['category']}")
                st.markdown(f"**Location:** {job['location']} ({job['job_type']})")
                st.markdown(f"**Salary:** {job['salary_range']}")
                st.markdown(f"**Min Experience:** {job['min_experience_years']} years ({job['experience_level']})")
            with col2:
                st.markdown(f"**Required Skills:**  \n`{job['required_skills']}`")
                st.markdown(f"**Qualifications:** {job['qualifications']}")
                st.markdown(f"**Posted Date:** {job['posted_date']}")
            with col3:
                curr_status = job['status']
                new_status = "Closed" if curr_status == "Active" else "Active"
                if st.button(f"Mark as {new_status}", key=f"toggle_stat_{job['id']}"):
                    database.update_job_status(job['id'], new_status)
                    st.success(f"Updated status to {new_status}!")
                    st.rerun()

            st.markdown("---")
            st.markdown(f"**Job Description:**  \n{job['description']}")
            if job['responsibilities']:
                st.markdown(f"**Responsibilities:**  \n{job['responsibilities']}")


def render_candidate_ranking_page():
    """Rank candidates for any specific job posting using dynamic NLP & TF-IDF match scores."""
    st.title("🎯 AI Candidate Ranking & Screening")
    st.markdown("Select a job vacancy to rank candidate profiles dynamically based on job-related qualifications, skills, and experience.")

    jobs = database.get_all_jobs(status="Active")
    if not jobs:
        st.warning("No active jobs available. Please post an active job first.")
        return

    job_options = {f"#{j['id']}: {j['title']} @ {j['company']}": j['id'] for j in jobs}
    selected_label = st.selectbox("Select Target Job Posting:", list(job_options.keys()))
    target_job_id = job_options[selected_label]

    job_details = database.get_job_by_id(target_job_id)

    # Job Summary Card
    st.markdown(f"""
    <div style="background-color: #f1f5f9; border-left: 5px solid #6366f1; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #1e293b;">{job_details['title']} — {job_details['company']}</h4>
        <p style="margin: 5px 0 0 0; color: #475569; font-size: 0.95rem;">
            <b>Required Skills:</b> {job_details['required_skills']} &nbsp;|&nbsp; 
            <b>Min Experience:</b> {job_details['min_experience_years']} yrs &nbsp;|&nbsp; 
            <b>Type:</b> {job_details['job_type']} ({job_details['location']})
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Calculate Candidate Ranking
    with st.spinner("Analyzing candidate resumes with TF-IDF vectorization & skill overlap..."):
        ranked_candidates = job_matching.rank_candidates_for_job(target_job_id)

    if not ranked_candidates:
        st.info("No candidates found in database.")
        return

    st.subheader(f"Ranked Candidates ({len(ranked_candidates)} evaluated)")

    for rank, cand in enumerate(ranked_candidates, start=1):
        score = cand['match_score']
        score_color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 60 else "#ef4444")

        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-bottom: 15px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background-color: #6366f1; color: white; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">Rank #{rank}</span>
                        <h3 style="display: inline; margin-left: 10px; color: #1e293b; font-size: 1.25rem;">{cand['name']}</h3>
                        <span style="color: #64748b; font-size: 0.9rem; margin-left: 10px;">• {cand['current_role']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.5rem; font-weight: 800; color: {score_color};">{score}%</span>
                        <div style="font-size: 0.8rem; color: #64748b;">Matching Score</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**Education:** {cand['education']}")
                st.markdown(f"**Experience:** {cand['experience_years']} years")
                st.markdown(f"**Candidate Skills:** `{cand['skills']}`")
                st.markdown(f"**Matched Required Skills:** `{', '.join(cand['matched_skills']) if cand['matched_skills'] else 'None'}`")
                if cand['missing_skills']:
                    st.markdown(f"**Missing Skills:** <span style='color: #ef4444;'>{', '.join(cand['missing_skills'])}</span>", unsafe_allow_html=True)

            with col2:
                st.markdown("##### 🔍 Explainable AI Ranking Rationale")
                st.caption(cand['explanation'])
                
                # Action Buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("⭐ Shortlist Candidate", key=f"shortlist_cand_{cand['candidate_id']}_{target_job_id}", use_container_width=True, type="primary"):
                        conn = database.get_connection()
                        conn.execute("""
                        INSERT OR REPLACE INTO shortlisted_candidates (recruiter_id, job_id, candidate_id, match_score, shortlist_reason)
                        VALUES (1, ?, ?, ?, ?)
                        """, (target_job_id, cand['candidate_id'], score, "Ranked highly by AI algorithm for core competencies."))
                        conn.commit()
                        conn.close()
                        st.success(f"{cand['name']} added to Shortlist!")

                with col_btn2:
                    if st.button("📧 Contact", key=f"contact_{cand['candidate_id']}_{target_job_id}", use_container_width=True):
                        st.info(f"Email: {cand['email']} | Phone: {cand['phone']}")

            st.markdown("<hr style='margin: 15px 0 25px 0; border: none; border-top: 1px dashed #cbd5e1;'/>", unsafe_allow_html=True)


def render_shortlisted_page():
    """View and manage all shortlisted candidates across job postings."""
    st.title("📋 Shortlisted Candidates")
    st.markdown("Review top shortlisted talent and manage hiring decisions.")

    conn = database.get_connection()
    query = """
    SELECT s.*, c.full_name as candidate_name, c.email, c.phone, c.education, c.skills, c.experience_years,
           j.title as job_title, j.company as job_company
    FROM shortlisted_candidates s
    JOIN candidates c ON s.candidate_id = c.id
    JOIN jobs j ON s.job_id = j.id
    ORDER BY s.shortlisted_at DESC
    """
    shortlisted = conn.execute(query).fetchall()
    conn.close()

    if not shortlisted:
        st.info("No candidates shortlisted yet. Use 'Candidate Ranking' to screen and shortlist candidates.")
        return

    st.markdown(f"**Total Shortlisted:** {len(shortlisted)}")

    for row in shortlisted:
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #c7d2fe; background-color: #f8fafc; border-radius: 8px; padding: 15px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #1e1b4b;">👤 {row['candidate_name']} — For: {row['job_title']}</h4>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #4338ca;">{row['match_score']}% Match</span>
                </div>
                <p style="margin: 8px 0 4px 0; color: #334155; font-size: 0.9rem;">
                    <b>Email:</b> {row['email']} | <b>Phone:</b> {row['phone']} | <b>Experience:</b> {row['experience_years']} yrs | <b>Education:</b> {row['education']}
                </p>
                <p style="margin: 0; color: #475569; font-size: 0.85rem;">
                    <b>Shortlist Rationale:</b> {row['shortlist_reason']} | <b>Date:</b> {row['shortlisted_at']}
                </p>
            </div>
            """, unsafe_allow_html=True)


class RecruiterManager:
    """
    Object-Oriented Recruiter Workflow Manager Class.
    Coordinates job vacancy postings, applicant evaluations,
    AI candidate ranking, and shortlisting workflows.
    """
    def __init__(self, recruiter_id: int = 1):
        self.recruiter_id = recruiter_id

    def post_job(self):
        """Render post job vacancy interface."""
        render_post_job_page(self.recruiter_id)

    def manage_jobs(self):
        """Render job management and status toggling interface."""
        render_manage_jobs_page()

    def rank_candidates(self):
        """Render candidate ranking and screening interface."""
        render_candidate_ranking_page()

    def view_shortlisted(self):
        """Render shortlisted applicants overview."""
        render_shortlisted_page()

