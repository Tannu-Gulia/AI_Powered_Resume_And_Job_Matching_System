"""
AI-Powered Resume & Job Matching System
Main Application Entrypoint (Streamlit)
Aligned with UN Sustainable Development Goal 8: Decent Work and Economic Growth
"""

import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Module imports
import database
import auth
import resume_parser
import nlp_processing
import job_matching
import skill_gap
import recommendations
import recruiter
import analytics
import resume_builder

# Page configuration
st.set_page_config(
    page_title="AI-Powered Resume & Job Matching System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Theme: Professional Blue, White, Light Purple)
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Header Bar */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #8b5cf6 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* KPI Metric Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* Job Card */
    .job-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: border-color 0.2s ease;
    }
    .job-card:hover {
        border-color: #6366f1;
    }
    
    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px 4px 2px 0;
    }
    .skill-badge-matched {
        background-color: #d1fae5;
        color: #065f46;
    }
    .skill-badge-missing {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize SQLite database and seed initial dataset
database.init_db()


def main():
    # Session state check
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # If user is not authenticated, render Login / Register page
    if not st.session_state['logged_in']:
        auth.render_auth_page()
        return

    # User is authenticated
    current_user = st.session_state['user']
    user_role = current_user['role']

    # Modern Sidebar Navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 10px 0 15px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 15px;">
            <h3 style="margin: 0; color: #1e3a8a; font-size: 1.25rem;">🎯 AI Recruitment</h3>
            <span style="font-size: 0.85rem; color: #64748b;">UN SDG 8 Platform</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Logged in as:**  \n👤 **{current_user['full_name']}**  \n🏷️ `{user_role}`")
        st.markdown("---")

        # Role-based menu items
        if user_role == "Job Seeker":
            menu_options = [
                "📊 Dashboard",
                "📝 AI Resume Builder",
                "📤 Upload Resume",
                "🔍 Resume Analysis",
                "💼 Find Matching Jobs",
                "🎯 Skill Gap Analysis",
                "📚 Course Recommendations",
                "👤 My Profile"
            ]
        else:
            menu_options = [
                "📊 Recruiter Dashboard",
                "📢 Post a Job",
                "💼 Manage Jobs",
                "👥 View Candidates",
                "🎯 Candidate Ranking",
                "⭐ Shortlist Candidates",
                "📈 Analytics"
            ]

        # Use query parameter or session state for page selection
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = menu_options[0]

        # Find index safely
        try:
            default_index = menu_options.index(st.session_state['current_page'])
        except ValueError:
            default_index = 0

        selected_page = st.radio("Navigation", menu_options, index=default_index)
        st.session_state['current_page'] = selected_page

        st.markdown("---")
        # Fair hiring badge
        st.markdown("""
        <div style="background-color: #f1f5f9; padding: 10px; border-radius: 8px; font-size: 0.78rem; color: #475569; line-height: 1.4;">
            ⚖️ <b>Fair Hiring Guarantee:</b><br/>
            All AI matching algorithms evaluate job-relevant technical skills, qualifications, and experience without bias on protected personal attributes.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout_user()

    # Routing based on selected page
    if user_role == "Job Seeker":
        render_job_seeker_app(selected_page, current_user)
    else:
        render_recruiter_app(selected_page, current_user)


# =========================================================================
# JOB SEEKER PAGES
# =========================================================================

def render_job_seeker_app(page: str, user: dict):
    candidate_profile = database.get_candidate_profile(user['id'])
    cand_dict = dict(candidate_profile) if candidate_profile else {}

    if page == "📊 Dashboard":
        render_job_seeker_dashboard(user, cand_dict)
    elif page == "📝 AI Resume Builder":
        resume_builder.render_resume_builder_page(user, cand_dict)
    elif page == "📤 Upload Resume":
        render_upload_resume_page(user, cand_dict)
    elif page == "🔍 Resume Analysis":
        render_resume_analysis_page(user, cand_dict)
    elif page == "💼 Find Matching Jobs":
        render_find_matching_jobs_page(user, cand_dict)
    elif page == "🎯 Skill Gap Analysis":
        render_skill_gap_page(user, cand_dict)
    elif page == "📚 Course Recommendations":
        render_course_recommendations_page(user, cand_dict)
    elif page == "👤 My Profile":
        render_candidate_profile_page(user, cand_dict)


def render_job_seeker_dashboard(user: dict, cand_dict: dict):
    """Job Seeker Main Dashboard overview."""
    st.markdown(f"""
    <div class="main-header">
        <h2 style="margin: 0; color: white;">👋 Welcome back, {user['full_name']}!</h2>
        <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 1.05rem;">
            Your AI Career Assistant is ready. Explore high-compatibility job matches and personalized upskilling paths.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Metric Row
    skills_list = [s.strip() for s in cand_dict.get('skills', '').split(',') if s.strip()]
    apps = database.get_candidate_applications(cand_dict.get('id', 0))
    all_jobs = database.get_all_jobs(status="Active")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #3b82f6; font-size: 1.8rem;">{len(skills_list)}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Verified Skills</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #10b981; font-size: 1.8rem;">{cand_dict.get('experience_years', 0)} Yrs</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Tracked Experience</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #8b5cf6; font-size: 1.8rem;">{len(apps)}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Job Applications</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #f59e0b; font-size: 1.8rem;">{len(all_jobs)}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Available Openings</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.subheader("🌟 Top Recommended Jobs for You")
        st.caption("Dynamically scored using TF-IDF content similarity and skill overlap.")
        
        matches = job_matching.find_matching_jobs_for_candidate(cand_dict, top_n=3)
        if matches:
            for job in matches:
                score = job['match_percentage']
                badge_color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 60 else "#ef4444")
                with st.container():
                    st.markdown(f"""
                    <div class="job-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin: 0; color: #1e293b;">{job['title']}</h4>
                                <span style="color: #64748b; font-size: 0.9rem;">🏢 {job['company']} &nbsp;•&nbsp; 📍 {job['location']} ({job['job_type']})</span>
                            </div>
                            <div style="background-color: {badge_color}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 700;">
                                {score}% Match
                            </div>
                        </div>
                        <p style="margin: 10px 0 6px 0; font-size: 0.9rem; color: #475569;">
                            <b>Required:</b> {job['required_skills']}
                        </p>
                        <p style="margin: 0; font-size: 0.85rem; color: #6366f1;">
                            💡 {job['explanation']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No matching jobs found. Update your skills in 'Upload Resume' or 'My Profile'.")

    with col_right:
        st.subheader("⚡ Quick Navigation")
        st.markdown("""
        - 📝 **AI Resume Builder**: Build an ATS-friendly resume from scratch or polish your existing resume with AI.
        - 📄 **Upload or Update Resume**: Extract skills and education from PDF.
        - 💼 **Explore Jobs**: Search 140+ job vacancies with explainable AI scores.
        - 🎯 **Analyze Skill Gaps**: Uncover competencies missing for your dream job.
        - 🎓 **Personalized Courses**: Upgrade your skillset with curated courses.
        """)
        
        if st.button("📝 Open AI Resume Builder", use_container_width=True, type="primary"):
            st.session_state['current_page'] = "📝 AI Resume Builder"
            st.rerun()
        
        st.markdown("""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 18px; margin-top: 15px;">
            <h4 style="color: #1e40af; margin-top: 0;">🌍 UN SDG 8 Goal</h4>
            <p style="color: #1e3a8a; font-size: 0.88rem; margin: 0;">
                By empowering candidates with actionable skill insights and unbiased AI matching, this system directly advances <b>Decent Work & Economic Growth</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_upload_resume_page(user: dict, cand_dict: dict):
    """Resume Upload and NLP Parsing Page."""
    st.title("📤 Upload & Parse Resume")
    st.markdown("Upload your PDF resume. Our AI parser extracts your contact info, education, experience, and categorized skill taxonomy.")

    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Select PDF Resume", type=["pdf"], help="Upload an authentic text-based PDF resume.")
        
        # Pre-loaded sample resume button for quick grading
        st.markdown("---")
        st.caption("Don't have a PDF handy? Click below to instantly parse our pre-built MCA Data Science resume:")
        use_sample = st.button("⚡ Load Pre-configured Sample Resume (Aarav Sharma - MCA Data Science)")

    parsed_result = None

    if uploaded_file is not None:
        with st.spinner("Parsing resume with PyMuPDF and NLP extraction..."):
            parsed_result = resume_parser.parse_resume(uploaded_file, uploaded_file.name)
            # Save raw file to uploads directory
            os.makedirs("uploads", exist_ok=True)
            saved_path = os.path.join("uploads", uploaded_file.name)
            uploaded_file.seek(0)
            with open(saved_path, "wb") as f:
                f.write(uploaded_file.read())
            uploaded_file.seek(0)
    elif use_sample:
        sample_path = os.path.join("uploads", "sample_resume.pdf")
        if os.path.exists(sample_path):
            with st.spinner("Parsing pre-configured sample resume..."):
                parsed_result = resume_parser.parse_resume(sample_path, "sample_resume.pdf")
        else:
            st.error("Sample resume file not found.")

    if parsed_result:
        if not parsed_result.get("success", False):
            st.error(parsed_result.get("error", "Error parsing resume."))
            return

        st.success("✅ Resume parsed successfully! Review the extracted data below and click Save.")

        # Display Review & Edit Form
        with st.form("resume_review_form"):
            st.subheader("📝 Review & Edit Extracted Information")
            
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                name = st.text_input("Candidate Name", value=parsed_result['name'])
                email = st.text_input("Email Address", value=parsed_result['email'] or user['email'])
                phone = st.text_input("Phone Number", value=parsed_result['phone'])
                education = st.text_input("Education / Degrees", value=parsed_result['education'])
            with c_f2:
                experience_years = st.number_input("Total Experience (Years)", min_value=0.0, max_value=40.0, value=float(parsed_result['experience_years']), step=0.5)
                location = st.text_input("Current Location", value=cand_dict.get('location', 'Bangalore, India'))
                current_role = st.text_input("Current or Desired Role", value=cand_dict.get('current_role', 'Data Scientist / Analyst'))

            # Skills
            skills_str = ", ".join(parsed_result['skills'])
            skills_input = st.text_area("Extracted Skills (Comma separated)", value=skills_str, height=100)
            bio = st.text_area("Professional Summary / Bio", value=parsed_result['raw_text'][:350] + "...", height=80)

            save_submitted = st.form_submit_button("💾 Save to Candidate Profile", use_container_width=True, type="primary")

            if save_submitted:
                candidate_id = cand_dict.get('id')
                if candidate_id:
                    # Update candidate profile in SQLite
                    database.update_candidate_profile(
                        candidate_id=candidate_id,
                        full_name=name,
                        phone=phone,
                        location=location,
                        education=education,
                        experience_years=experience_years,
                        current_role=current_role,
                        bio=bio,
                        skills=skills_input
                    )
                    # Save resume record
                    database.save_candidate_resume(
                        candidate_id=candidate_id,
                        file_name=parsed_result['filename'],
                        file_path=os.path.join("uploads", parsed_result['filename']),
                        raw_text=parsed_result['raw_text'],
                        parsed_json=json.dumps(parsed_result)
                    )
                    st.success("🎉 Profile and Resume saved to database! You can now explore matching jobs.")
                    st.rerun()


def render_resume_analysis_page(user: dict, cand_dict: dict):
    """Module 3: AI-Based Resume Analysis."""
    st.title("🔍 AI-Based Resume Analysis & Skill Extraction")
    st.markdown("Detailed NLP linguistic analysis of your resume text, vocabulary distribution, and categorized competencies.")

    skills_raw = cand_dict.get('skills', '')
    skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]

    if not skills_list:
        st.warning("No skills found in your profile. Please upload your resume in 'Upload Resume'.")
        return

    # Categorize skills using NLP taxonomy
    categorized = nlp_processing.categorize_skills(skills_list)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("🗂️ Categorized Skill Profile")
        for cat_name, cat_skills in categorized.items():
            st.markdown(f"**{cat_name}:**")
            badges_html = " ".join([f'<span class="skill-badge">{s}</span>' for s in cat_skills])
            st.markdown(badges_html, unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Skill Taxonomy Distribution")
        cat_counts = {k: len(v) for k, v in categorized.items()}
        df_cats = pd.DataFrame(list(cat_counts.items()), columns=['Category', 'Skill Count'])
        fig_donut = px.pie(
            df_cats,
            names='Category',
            values='Skill Count',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_donut.update_layout(
            margin=dict(l=10, r=10, t=20, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # Resume Text Keywords
    bio_text = cand_dict.get('bio', '') + " " + " ".join(skills_list)
    keywords = nlp_processing.extract_keywords(bio_text, top_n=12)
    
    st.subheader("🔑 NLP Keyword Salience & Term Frequencies")
    if keywords:
        df_kw = pd.DataFrame(keywords, columns=['Term', 'Occurrences'])
        fig_kw = px.bar(
            df_kw,
            x='Occurrences',
            y='Term',
            orientation='h',
            color='Occurrences',
            color_continuous_scale='Purples'
        )
        fig_kw.update_layout(
            yaxis=dict(autorange="reversed"),
            height=320,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_kw, use_container_width=True)


def render_find_matching_jobs_page(user: dict, cand_dict: dict):
    """Module 4: AI-Powered Job Matching."""
    st.title("💼 AI-Powered Job Matching Engine")
    st.markdown("Browse open vacancies ranked dynamically by TF-IDF textual similarity, skill overlap, and experience fit.")

    # Filters
    col_f1, col_f2, col_f3 = st.columns([2, 1.5, 1])
    with col_f1:
        search_query = st.text_input("🔍 Search by title or company", "")
    with col_f2:
        categories = ["All"] + [
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
        ]
        selected_cat = st.selectbox("Filter Category", categories)
    with col_f3:
        min_score = st.slider("Min Match %", 0, 100, 40)

    # Compute dynamic matches
    with st.spinner("Executing TF-IDF vectorization and cosine similarity matching..."):
        all_matched_jobs = job_matching.find_matching_jobs_for_candidate(cand_dict, top_n=50, category_filter=selected_cat)

    # Apply search filter and score filter
    filtered = []
    for j in all_matched_jobs:
        if j['match_percentage'] < min_score:
            continue
        if search_query:
            sq = search_query.lower()
            if sq not in j['title'].lower() and sq not in j['company'].lower() and sq not in j['required_skills'].lower():
                continue
        filtered.append(j)

    st.markdown(f"**Found {len(filtered)} matching job vacancies** (Sorted by AI Match Percentage)")

    for job in filtered[:10]:
        score = job['match_percentage']
        score_color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 60 else "#ef4444")

        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h3 style="margin: 0; color: #1e293b; font-size: 1.3rem;">{job['title']}</h3>
                        <div style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">
                            🏢 <b>{job['company']}</b> &nbsp;•&nbsp; 📍 {job['location']} ({job['job_type']}) &nbsp;•&nbsp; 💰 {job['salary_range']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.6rem; font-weight: 800; color: {score_color};">{score}%</span>
                        <div style="font-size: 0.8rem; color: #64748b;">Match Score</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_info, c_action = st.columns([3, 1.5])
            with c_info:
                st.markdown(f"**Required Experience:** {job['min_experience_years']} yrs ({job['experience_level']}) &nbsp;|&nbsp; **Qualifications:** {job['qualifications']}")
                
                # Matched skills
                st.markdown("**Matched Skills:**")
                m_html = " ".join([f'<span class="skill-badge skill-badge-matched">✓ {s}</span>' for s in job['matched_skills']]) if job['matched_skills'] else "<em>None directly matched</em>"
                st.markdown(m_html, unsafe_allow_html=True)

                # Missing skills
                if job['missing_skills']:
                    st.markdown("**Missing Skills (To Learn):**")
                    miss_html = " ".join([f'<span class="skill-badge skill-badge-missing">✕ {s}</span>' for s in job['missing_skills']])
                    st.markdown(miss_html, unsafe_allow_html=True)

                st.markdown(f"<p style='font-size: 0.85rem; color: #475569; margin-top: 6px;'><b>AI Matching Rationale:</b> {job['explanation']}</p>", unsafe_allow_html=True)

            with c_action:
                st.markdown("<br/>", unsafe_allow_html=True)
                # Apply button
                if st.button("🚀 Apply for Job", key=f"apply_{job['id']}", use_container_width=True, type="primary"):
                    success, msg = database.apply_for_job(job['id'], cand_dict.get('id', 1), score)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

                # Analyze Gap button
                if st.button("🎯 Analyze Skill Gap", key=f"gap_btn_{job['id']}", use_container_width=True):
                    st.session_state['selected_job_for_gap'] = job
                    st.session_state['current_page'] = "🎯 Skill Gap Analysis"
                    st.rerun()

            st.markdown("<hr style='margin: 10px 0 20px 0; border: none; border-top: 1px dashed #e2e8f0;'/>", unsafe_allow_html=True)


def render_skill_gap_page(user: dict, cand_dict: dict):
    """Module 5: Skill Gap Analysis."""
    st.title("🎯 Skill Gap Analysis")
    st.markdown("Compare your current skill profile against specific job requirements to reveal targeted competencies you need to acquire.")

    all_jobs = database.get_all_jobs(status="Active")
    job_options = {f"#{j['id']}: {j['title']} @ {j['company']}": j['id'] for j in all_jobs}

    # Default to pre-selected job if coming from job match page
    default_index = 0
    if 'selected_job_for_gap' in st.session_state:
        target_id = st.session_state['selected_job_for_gap']['id']
        for idx, (label, jid) in enumerate(job_options.items()):
            if jid == target_id:
                default_index = idx
                break

    selected_label = st.selectbox("Select Target Job for Skill Gap Analysis:", list(job_options.keys()), index=default_index)
    selected_job_id = job_options[selected_label]
    job_details = database.get_job_by_id(selected_job_id)

    cand_skills = [s.strip() for s in cand_dict.get('skills', '').split(',') if s.strip()]
    req_skills = [s.strip() for s in job_details['required_skills'].split(',') if s.strip()]

    # Perform Skill Gap Analysis
    gap_result = skill_gap.analyze_skill_gap(cand_skills, req_skills)

    col1, col2 = st.columns([1, 2])
    with col1:
        gauge_fig = skill_gap.create_gauge_chart(gap_result['match_percentage'], title="Skill Readiness")
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown(f"**Readiness Level:**  \n{gap_result['status']}")
        st.markdown(f"**Matched Competencies:** {len(gap_result['matched_skills'])} of {len(req_skills)}")
        st.markdown(f"**Identified Gaps:** {gap_result['gap_count']} skills")

    with col2:
        chart_fig = skill_gap.create_skill_gap_chart(gap_result['matched_skills'], gap_result['missing_skills'])
        st.plotly_chart(chart_fig, use_container_width=True)

    st.markdown("---")

    # Missing Skills Actionable Recommendations
    if gap_result['missing_skills']:
        st.subheader("🚀 Actionable Upskilling Recommendations")
        st.caption("Closing these skill gaps will substantially increase your matching score for this role:")
        
        courses = recommendations.get_recommendations_for_skills(gap_result['missing_skills'])
        
        c_cols = st.columns(min(3, max(1, len(courses))))
        for idx, course in enumerate(courses):
            with c_cols[idx % len(c_cols)]:
                st.markdown(f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; margin-bottom: 12px; height: 100%;">
                    <span style="background-color: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">Skill Gap: {course['skill']}</span>
                    <h5 style="margin: 10px 0 6px 0; color: #1e293b;">{course['course_name']}</h5>
                    <p style="margin: 0 0 10px 0; color: #64748b; font-size: 0.85rem;">Platform: <b>{course['platform']}</b></p>
                    <a href="{course['url']}" target="_blank" style="display: inline-block; background-color: #6366f1; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 0.85rem; font-weight: 600;">🌐 View Course</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("🎉 Outstanding! You have acquired all core technical skills required for this job vacancy.")


def render_course_recommendations_page(user: dict, cand_dict: dict):
    """Module 5: Course Recommendations Catalog."""
    st.title("📚 AI Learning Pathways & Course Recommendations")
    st.markdown("Curated certifications and courses from Coursera, Udemy, and edX to bridge career skill gaps.")

    all_skills_catalog = database.get_all_skills_catalog()
    skill_names = [s['skill_name'] for s in all_skills_catalog]

    selected_skill = st.selectbox("Search Learning Resources by Skill:", ["All Skills"] + skill_names)

    if selected_skill == "All Skills":
        courses = recommendations.get_recommendations_for_skills(skill_names[:15])
    else:
        courses = recommendations.get_recommendations_for_skills([selected_skill])

    col1, col2, col3 = st.columns(3)
    for idx, c in enumerate(courses):
        with [col1, col2, col3][idx % 3]:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px; margin-bottom: 15px;">
                <span style="background-color: #e0e7ff; color: #3730a3; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">{c['category']}</span>
                <h4 style="margin: 10px 0 5px 0; color: #1e293b;">{c['course_name']}</h4>
                <p style="margin: 0 0 12px 0; color: #64748b; font-size: 0.9rem;">
                    <b>Target Skill:</b> {c['skill']}<br/>
                    <b>Platform:</b> {c['platform']}
                </p>
                <a href="{c['url']}" target="_blank" style="display: inline-block; background: #3b82f6; color: white; padding: 8px 14px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem;">🚀 Start Learning</a>
            </div>
            """, unsafe_allow_html=True)


def render_candidate_profile_page(user: dict, cand_dict: dict):
    """Candidate My Profile Page."""
    st.title("👤 My Profile & Application History")

    tab_profile, tab_apps = st.tabs(["📝 Candidate Information", "📑 Submitted Applications"])

    with tab_profile:
        with st.form("edit_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", value=cand_dict.get('full_name', ''))
                email = st.text_input("Email", value=cand_dict.get('email', ''), disabled=True)
                phone = st.text_input("Phone", value=cand_dict.get('phone', ''))
                location = st.text_input("Location", value=cand_dict.get('location', ''))
            with col2:
                role = st.text_input("Current Title / Role", value=cand_dict.get('current_role', ''))
                exp = st.number_input("Years of Experience", min_value=0.0, max_value=30.0, value=float(cand_dict.get('experience_years', 1.0)), step=0.5)
                edu = st.text_input("Education", value=cand_dict.get('education', ''))
            
            skills = st.text_area("Skills (comma-separated)", value=cand_dict.get('skills', ''))
            bio = st.text_area("Bio / Professional Summary", value=cand_dict.get('bio', ''))

            submitted = st.form_submit_button("Update Profile Details", use_container_width=True, type="primary")

            if submitted:
                database.update_candidate_profile(
                    cand_dict['id'], name, phone, location, edu, exp, role, bio, skills
                )
                st.success("Profile updated successfully!")
                st.rerun()

    with tab_apps:
        apps = database.get_candidate_applications(cand_dict.get('id', 0))
        if not apps:
            st.info("You haven't submitted any job applications yet. Go to 'Find Matching Jobs' to apply!")
        else:
            st.markdown(f"**Total Applications:** {len(apps)}")
            for app in apps:
                st_color = "#10b981" if app['status'] == 'Shortlisted' else ("#3b82f6" if app['status'] == 'Applied' else "#f59e0b")
                st.markdown(f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #1e293b;">{app['title']} — {app['company']}</h4>
                        <span style="background-color: {st_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 700;">{app['status']}</span>
                    </div>
                    <p style="margin: 6px 0 0 0; color: #64748b; font-size: 0.9rem;">
                        <b>Location:</b> {app['location']} | <b>Category:</b> {app['category']} | <b>Match Score:</b> {app['match_score']}% | <b>Applied Date:</b> {app['applied_at']}
                    </p>
                </div>
                """, unsafe_allow_html=True)


# =========================================================================
# RECRUITER PAGES
# =========================================================================

def render_recruiter_app(page: str, user: dict):
    recruiter_id = 1  # default recruiter organization

    if page == "📊 Recruiter Dashboard":
        render_recruiter_dashboard(user)
    elif page == "📢 Post a Job":
        recruiter.render_post_job_page(recruiter_id)
    elif page == "💼 Manage Jobs":
        recruiter.render_manage_jobs_page()
    elif page == "👥 View Candidates":
        render_recruiter_candidates_view()
    elif page == "🎯 Candidate Ranking":
        recruiter.render_candidate_ranking_page()
    elif page == "⭐ Shortlist Candidates":
        recruiter.render_shortlisted_page()
    elif page == "📈 Analytics":
        analytics.render_analytics_dashboard()


def render_recruiter_dashboard(user: dict):
    """Recruiter Dashboard with applicant review stream and status updater."""
    st.markdown(f"""
    <div class="main-header">
        <h2 style="margin: 0; color: white;">🏢 Recruiter Command Center — Welcome, {user['full_name']}</h2>
        <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 1.05rem;">
            Automate resume screening, eliminate human bias, and shortlist top-tier talent with explainable AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    metrics = analytics.get_analytics_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #3b82f6; font-size: 1.8rem;">{metrics['total_jobs']}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Active Job Openings</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #8b5cf6; font-size: 1.8rem;">{metrics['total_candidates']}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Talent Pool Size</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #f59e0b; font-size: 1.8rem;">{metrics['total_applications']}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Applications Received</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #10b981; font-size: 1.8rem;">{metrics['total_shortlisted']}</h3>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">Shortlisted Candidates</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Recent Applications Section
    st.subheader("📬 Candidate Applications Review Stream")
    st.caption("Review candidate resumes against job requirements with instant status updating.")

    apps = database.get_job_applications_for_recruiter()
    if not apps:
        st.info("No applications received yet.")
        return

    for app in apps:
        score = app['match_score']
        score_color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 60 else "#ef4444")
        
        with st.container():
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin: 0; color: #1e293b;">👤 {app['candidate_name']} — Applied for: {app['job_title']}</h4>
                        <div style="color: #64748b; font-size: 0.9rem; margin-top: 4px;">
                            📧 {app['candidate_email']} &nbsp;|&nbsp; 📞 {app['phone']} &nbsp;|&nbsp; 🎓 {app['education']} &nbsp;|&nbsp; ⏱️ {app['experience_years']} yrs exp
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.5rem; font-weight: 800; color: {score_color};">{score}% Match</span>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #475569;">Status: {app['status']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_skills, c_btns = st.columns([3, 1.5])
            with c_skills:
                st.markdown(f"**Candidate Skills:** `{app['candidate_skills']}`")
                st.markdown(f"**Job Required Skills:** `{app['required_skills']}`")
            with c_btns:
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("⭐ Shortlist", key=f"rec_short_{app['id']}", use_container_width=True, type="primary"):
                        database.update_application_status(app['id'], 'Shortlisted')
                        st.success("Shortlisted!")
                        st.rerun()
                with col_b2:
                    if st.button("✕ Reject", key=f"rec_rej_{app['id']}", use_container_width=True):
                        database.update_application_status(app['id'], 'Rejected')
                        st.warning("Rejected.")
                        st.rerun()

            st.markdown("<hr style='margin: 10px 0 20px 0; border: none; border-top: 1px dashed #e2e8f0;'/>", unsafe_allow_html=True)


def render_recruiter_candidates_view():
    """Browse candidate directory with filters."""
    st.title("👥 Candidate Talent Directory")
    st.markdown("Search and inspect candidate profiles registered across the platform.")

    conn = database.get_connection()
    cands = conn.execute("SELECT * FROM candidates ORDER BY id DESC").fetchall()
    conn.close()

    search = st.text_input("🔍 Search candidate by name, role, or skills:", "")
    filtered = cands
    if search:
        s_low = search.lower()
        filtered = [c for c in filtered if s_low in c['full_name'].lower() or s_low in c['skills'].lower() or s_low in str(c['current_role']).lower()]

    st.markdown(f"**Showing {len(filtered)} candidates**")

    for cand in filtered:
        with st.expander(f"👤 {cand['full_name']} — {cand['current_role']} ({cand['experience_years']} yrs exp)"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Email:** {cand['email']}")
                st.markdown(f"**Phone:** {cand['phone']}")
                st.markdown(f"**Location:** {cand['location']}")
                st.markdown(f"**Education:** {cand['education']}")
            with c2:
                st.markdown(f"**Skills:**  \n`{cand['skills']}`")
                if cand['bio']:
                    st.markdown(f"**Summary:**  \n{cand['bio']}")


if __name__ == "__main__":
    main()
