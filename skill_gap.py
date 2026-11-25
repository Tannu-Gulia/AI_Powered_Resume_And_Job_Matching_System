"""
Skill Gap Analysis Module for AI-Powered Resume & Job Matching System
Compares candidate competencies against target job requirements, calculates gaps,
and generates Plotly visual comparisons.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import database


def analyze_skill_gap(candidate_skills_list: list, required_skills_list: list) -> dict:
    """
    Perform granular skill gap analysis between candidate skills and required skills.
    Returns matched skills, missing skills, match percentage, and gap severity.
    """
    if not required_skills_list:
        return {
            "matched_skills": candidate_skills_list,
            "missing_skills": [],
            "match_percentage": 100.0,
            "gap_count": 0,
            "status": "Ready for Role"
        }

    cand_set = {s.strip().lower() for s in candidate_skills_list if s.strip()}
    matched = []
    missing = []

    for req in required_skills_list:
        r_clean = req.strip().lower()
        if r_clean in cand_set or any(r_clean in c or c in r_clean for c in cand_set):
            matched.append(req.strip())
        else:
            missing.append(req.strip())

    total_req = len(required_skills_list)
    match_pct = round((len(matched) / total_req) * 100, 1) if total_req > 0 else 0

    if match_pct >= 80:
        status = "🟢 Strong Fit - High Readiness"
    elif match_pct >= 50:
        status = "🟡 Moderate Fit - Minor Skill Gaps"
    else:
        status = "🔴 Substantial Gap - Upskilling Recommended"

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_pct,
        "gap_count": len(missing),
        "status": status
    }


def create_skill_gap_chart(matched_skills: list, missing_skills: list):
    """
    Generate an interactive Plotly horizontal bar chart showing matched vs missing skills.
    """
    skills = matched_skills + missing_skills
    statuses = ["Acquired Skill"] * len(matched_skills) + ["Skill Gap (To Learn)"] * len(missing_skills)
    colors = ["#10b981"] * len(matched_skills) + ["#ef4444"] * len(missing_skills)
    values = [1] * len(skills)

    if not skills:
        fig = go.Figure()
        fig.update_layout(title="No skills found for comparison")
        return fig

    fig = go.Figure(go.Bar(
        x=values,
        y=skills,
        orientation='h',
        marker=dict(color=colors),
        text=statuses,
        textposition='inside',
        insidetextanchor='middle',
        hoverinfo='y+text'
    ))

    fig.update_layout(
        title="<b>Skill Competency Matrix: Acquired vs Missing Skills</b>",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=50, b=20),
        height=max(320, len(skills) * 32),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def create_gauge_chart(percentage: float, title: str = "Skill Compatibility Score"):
    """
    Create a sleek Plotly gauge indicator chart for skill match percentage.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        number={'suffix': "%", 'font': {'size': 32, 'color': '#1e293b'}},
        title={'text': f"<b>{title}</b>", 'font': {'size': 18, 'color': '#334155'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
            'bar': {'color': "#6366f1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 50], 'color': '#fee2e2'},
                {'range': [50, 75], 'color': '#fef3c7'},
                {'range': [75, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "#10b981", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    fig.update_layout(
        height=260,
        margin=dict(l=30, r=30, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


class SkillGapAnalyzer:
    """
    Object-Oriented Skill Gap Analyzer Class.
    Encapsulates gap quantification, readiness benchmarking, and interactive
    Plotly visual matrix generation.
    """
    def __init__(self):
        pass

    def analyze(self, candidate_skills: list, required_skills: list) -> dict:
        """Analyze matched skills, missing skills, and readiness rating."""
        return analyze_skill_gap(candidate_skills, required_skills)

    def generate_matrix(self, matched_skills: list, missing_skills: list):
        """Generate Plotly horizontal bar chart competency matrix."""
        return create_skill_gap_chart(matched_skills, missing_skills)

    def generate_gauge(self, percentage: float, title: str = "Skill Compatibility Score"):
        """Generate Plotly gauge chart for skill compatibility."""
        return create_gauge_chart(percentage, title)

