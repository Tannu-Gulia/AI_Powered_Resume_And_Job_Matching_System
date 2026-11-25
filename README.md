# 🚀 AI-Powered Resume & Job Matching System
### MCA Data Science Academic Project | UN SDG 8: Decent Work and Economic Growth

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-2.0%2B-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-blueviolet.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 📌 Executive Summary & SDG 8 Alignment

The **AI-Powered Resume & Job Matching System** is an intelligent web-based recruitment and labor market intelligence platform developed for an **MCA Data Science** academic curriculum. 

The project directly aligns with **United Nations Sustainable Development Goal 8 (Target 8.5)**:
> *"By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities, and equal pay for work of equal value."*

By substituting traditional, subjective resume screening with transparent, explainable Natural Language Processing (NLP) and Machine Learning (TF-IDF Vectorization & Cosine Similarity), this system eliminates cognitive human bias, identifies personalized skill gaps, recommends targeted courses, and empowers recruiters to shortlist talent purely based on verified skills and qualifications.

---

## 🏗️ Architecture & Technology Stack

```
                          ┌─────────────────────────────┐
                          │   Streamlit Web Interface   │
                          │   (Job Seeker & Recruiter)  │
                          └──────────────┬──────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     ┌────────────────────────┐                     ┌────────────────────────┐
     │  Resume Parsing & NLP  │                     │   Recruiter Workflows  │
     │  - PyMuPDF Text Extr.  │                     │  - Job Posting         │
     │  - Regular Expressions │                     │  - Candidate Ranking   │
     │  - Tokenization & NLTK │                     │  - Shortlist / Reject  │
     └───────────┬────────────┘                     └───────────┬────────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                     ┌──────────────────────────────────────┐
                     │       AI Matching & Analysis         │
                     │  - TF-IDF Vectorizer (scikit-learn)  │
                     │  - Cosine Similarity Matrix          │
                     │  - Skill Overlap Ratio               │
                     │  - Experience Level Fitting          │
                     │  - Skill Gap & Course Recommender    │
                     └──────────────────┬───────────────────┘
                                        ▼
                     ┌──────────────────────────────────────┐
                     │        SQLite Database Layer         │
                     │  (Users, Jobs, Candidates, Resumes)  │
                     └──────────────────────────────────────┘
```

### Technology Highlights
- **Programming Language:** Python 3.10+
- **Frontend / UI:** Streamlit (Custom Responsive Theme in Blue, White & Light Purple)
- **Database:** SQLite3 (Relational Schema with Cascading Integrity)
- **Natural Language Processing (NLP):** NLTK & Regular Expressions (Tokenization, Stopword Removal, Taxonomic Extraction)
- **Machine Learning:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- **Document Parsing:** PyMuPDF (`pymupdf`)
- **Data Manipulation:** Pandas & NumPy
- **Interactive Visualizations:** Plotly Express & Plotly Graph Objects

---

## ⚙️ Mathematical & Algorithmic Formulation

The matching score is **never hardcoded**; it is dynamically calculated using a weighted composite model:

$$\text{Composite Match Score} = \left( 0.50 \times S_{\text{skills}} + 0.35 \times S_{\text{TF-IDF}} + 0.15 \times S_{\text{exp}} \right) \times 100\%$$

Where:
1. **Skill Overlap Ratio ($S_{\text{skills}}$):**
   $$S_{\text{skills}} = \frac{|\text{Candidate Skills} \cap \text{Job Required Skills}|}{|\text{Job Required Skills}|}$$

2. **TF-IDF Cosine Similarity ($S_{\text{TF-IDF}}$):**
   Calculated across the $n$-gram representations of the candidate's professional summary, skills, education and the job description:
   $$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \|\vec{v}\|_2}$$

3. **Experience Fit ($S_{\text{exp}}$):**
   $$S_{\text{exp}} = \min\left(1.0, \frac{\text{Candidate Experience (Yrs)}}{\max(1.0, \text{Job Min Experience})}\right)$$

---

## 📂 Project Directory Structure

```
AI_Resume_Job_Matching/
│
├── app.py                      # Main Streamlit web application & routing
├── database.py                 # SQLite schema, CRUD operations & data seeders
├── auth.py                     # Authentication, password hashing, session state
├── resume_parser.py            # PyMuPDF PDF parsing & attribute extraction
├── resume_builder.py           # AI-Powered Resume Builder, Templates, Quality Checker, PDF Generator
├── nlp_processing.py           # Text cleaning, stopwords, tokenization, skill taxonomy
├── job_matching.py             # TF-IDF vectorization & Cosine Similarity matching engine
├── skill_gap.py                # Skill gap analysis & Plotly competency matrices
├── recruiter.py                # Recruiter management, vacancy posting, candidate ranking
├── analytics.py                # Interactive recruitment analytics & market KPIs
├── recommendations.py          # Course & certification recommendation engine
│
├── dataset/
│   ├── jobs.csv                # 140+ realistic job listings across 10 industry domains
│   ├── candidates.csv          # Sample candidate profiles
│   └── skills.csv              # Curated skill catalog with online learning links
│
├── uploads/                    # Stores uploaded candidate resumes & sample PDF
├── models/                     # Saved NLP artifacts & models
│
├── scripts/
│   └── generate_datasets.py    # Dataset generator script
│
├── requirements.txt            # Python dependencies
└── README.md                   # Comprehensive documentation
```

---

## 🚀 Installation & Execution Guide (VS Code)

### Step 1: Open Project in VS Code
Open VS Code, press `Ctrl + ~` to launch the integrated terminal, and ensure your terminal is in the project directory:
```bash
cd "c:\Users\hp\OneDrive\Desktop\IMF"
```

### Step 2: (Optional) Create a Python Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows Command Prompt (CMD):
.\venv\Scripts\activate.bat
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py
```
Streamlit will automatically launch your default browser at `http://localhost:8501`.

---

## 🔑 Pre-Configured Test Credentials

For quick evaluation and grading, pre-configured accounts are provided on the login page:

| Role | Email | Password | Included Pre-Loaded Data |
| :--- | :--- | :--- | :--- |
| **Job Seeker** | `candidate@test.com` | `Password123` | Aarav Sharma (MCA Data Science, 1.5 yrs exp, Python, ML, NLP, SQL) |
| **Recruiter** | `recruiter@test.com` | `Password123` | Pooja Verma (TechSphere Solutions, Talent Acquisition) |

> 💡 **Quick Demo:** You can also click the **"⚡ Quick Demo Login"** tab on the login screen to sign in with 1 click without typing.

---

## 🌟 Key Functional Features

### 👨‍💻 Job Seeker Experience
1. **Interactive Dashboard:** Live counts of verified skills, tracked experience, active applications, and top recommendations.
2. **Resume Upload & Parsing:** Upload any text-based PDF resume. PyMuPDF and NLP extract candidate name, email, phone, education, experience, and categorized skills with review & edit support.
3. **AI Resume Analysis:** Word frequency analysis, NLTK stopword filtering, and domain skill distribution pie charts.
4. **Find Matching Jobs:** Search 140+ active jobs filtered by domain and minimum match score. Each card provides an explainable AI rationale.
5. **Skill Gap Analysis:** Side-by-side competency matrix comparing candidate skills with job requirements, accompanied by a Plotly gauge indicator.
6. **Course Recommendations:** Directly links missing skills to relevant courses on Coursera, Udemy, and edX.
7. **Candidate Profile & History:** Edit profile details and view the real-time status of applied jobs.

### 🏢 Recruiter Experience
1. **Command Center:** Real-time metrics on talent pool size, job postings, and received applications.
2. **Post Job Vacancies:** Add new positions across 10 specialized tech domains with custom requirements.
3. **Manage Jobs:** Track status (Active/Closed) and review job descriptions.
4. **Candidate Directory:** Search all registered job seekers by name, role, or technical skillset.
5. **AI Candidate Ranking:** Select any vacancy to dynamically rank candidates using TF-IDF and skill overlap, with instant shortlisting.
6. **Shortlisted Talent Review:** Centralized view of shortlisted applicants with candidate contact details.
7. **Recruitment Analytics:** Plotly dashboards displaying labor market skill demand, candidate score histograms, and job category distribution.

---

## ⚖️ Fair and Transparent Hiring Protocol

In accordance with responsible AI standards:
- **Zero Demographic Bias:** The matching engine does **not** consume or score age, gender, race, religion, caste, nationality, or marital status.
- **Explainable AI (XAI):** Every matching score provides a transparent mathematical breakdown (Skill Overlap %, TF-IDF text similarity %, Experience fit %).
- **Human-in-the-Loop:** AI serves strictly as an assist tool for sorting and screening; all shortlisting and final hiring decisions remain strictly in human recruiter hands.

---

## 🎓 Academic Project Information
- **Course:** Master of Computer Applications (MCA) — Data Science
- **Project Domain:** Artificial Intelligence, Natural Language Processing, Machine Learning, Web Technologies
- **UN SDG Focus:** Goal 8: Decent Work & Economic Growth
