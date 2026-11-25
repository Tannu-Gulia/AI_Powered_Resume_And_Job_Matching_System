"""
Authentication Module for AI-Powered Resume & Job Matching System
Handles user authentication, registration, session management, and role-based access.
"""

import streamlit as st
import database


def login_user(email: str, password: str):
    """Verify credentials and set up session state upon successful login."""
    user = database.get_user_by_email(email)
    if not user:
        return False, "No account found with this email address."
    
    hashed = database.hash_password(password)
    if user['password_hash'] != hashed:
        return False, "Incorrect password. Please try again."
    
    # Store session details
    st.session_state['logged_in'] = True
    st.session_state['user'] = {
        'id': user['id'],
        'email': user['email'],
        'role': user['role'],
        'full_name': user['full_name']
    }
    
    # Cache candidate profile if Job Seeker
    if user['role'] == 'Job Seeker':
        cand = database.get_candidate_profile(user['id'])
        if cand:
            st.session_state['candidate_id'] = cand['id']
            st.session_state['candidate_profile'] = dict(cand)
    return True, f"Welcome back, {user['full_name']}!"


def register_user(email: str, password: str, confirm_password: str, role: str, full_name: str):
    """Validate and register a new user."""
    if not email or not password or not full_name:
        return False, "All fields are required."
    
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
        
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
        
    if password != confirm_password:
        return False, "Passwords do not match."
        
    user_id, err = database.create_user(email, password, role, full_name)
    if err:
        return False, err
        
    return True, "Registration successful! You can now log in."


def logout_user():
    """Clear session variables and log out."""
    for key in ['logged_in', 'user', 'candidate_id', 'candidate_profile', 'selected_job']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state['logged_in'] = False
    st.rerun()


def render_auth_page():
    """Render modern tabbed Login / Register / Demo login interface."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #2b3a67; margin-bottom: 5px;">🚀 AI-Powered Resume & Job Matching System</h1>
        <p style="color: #6366f1; font-size: 1.1rem; font-weight: 500;">
            Bridging Talent and Opportunity with Explainable AI & NLP
        </p>
        <span style="background-color: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
            UN SDG 8: Decent Work & Economic Growth
        </span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register, tab_demo = st.tabs(["🔐 Sign In", "📝 Create Account", "⚡ Quick Demo Login"])

        # Tab 1: Login
        with tab_login:
            st.subheader("Welcome Back")
            st.caption("Sign in to access your AI recruitment dashboard")
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="name@example.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)

                if submitted:
                    success, msg = login_user(email, password)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        # Tab 2: Register
        with tab_register:
            st.subheader("Join the Platform")
            st.caption("Create an account as a Job Seeker or Recruiter")
            with st.form("register_form"):
                full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
                reg_email = st.text_input("Email Address", placeholder="name@example.com")
                role = st.selectbox("I am registering as a:", ["Job Seeker", "Recruiter"])
                reg_password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                reg_submitted = st.form_submit_button("Create Account", use_container_width=True)

                if reg_submitted:
                    success, msg = register_user(reg_email, reg_password, confirm_password, role, full_name)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

        # Tab 3: Quick Demo Accounts for grading / presentation
        with tab_demo:
            st.subheader("Academic Demo Profiles")
            st.info("Click any button below to instantly test the platform with pre-configured datasets.")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown("##### 👨‍💻 Job Seeker Profile")
                st.markdown("**User:** Aarav Sharma  \n**Role:** MCA Data Science  \n**Skills:** Python, ML, NLP, SQL")
                if st.button("Log In as Job Seeker", use_container_width=True, type="primary"):
                    login_user("candidate@test.com", "Password123")
                    st.rerun()

            with col_d2:
                st.markdown("##### 🏢 Recruiter Profile")
                st.markdown("**User:** Pooja Verma  \n**Company:** TechSphere Solutions  \n**Role:** Talent Acquisition")
                if st.button("Log In as Recruiter", use_container_width=True, type="secondary"):
                    login_user("recruiter@test.com", "Password123")
                    st.rerun()


class AuthManager:
    """
    Object-Oriented Authentication & Session Manager Class.
    Encapsulates user credential validation, role-based session states,
    and access control gates.
    """
    def __init__(self):
        pass

    def login(self, email: str, password: str) -> tuple:
        """Authenticate user and initialize session state."""
        return login_user(email, password)

    def register(self, email: str, password: str, confirm_pass: str, role: str, full_name: str) -> tuple:
        """Register a new user account."""
        return register_user(email, password, confirm_pass, role, full_name)

    def logout(self):
        """Terminate active user session."""
        logout_user()

    def render(self):
        """Render Streamlit authentication interface."""
        render_auth_page()

