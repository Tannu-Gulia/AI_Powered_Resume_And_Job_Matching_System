"""
Resume Parser Module for AI-Powered Resume & Job Matching System
Extracts structured candidate details (Name, Contact, Education, Experience, Skills)
from uploaded PDF resumes using PyMuPDF, regular expressions, and NLP.
"""

try:
    import pymupdf as fitz
except ImportError:
    import fitz
import re
import os
import json
import database
from nlp_processing import clean_text, KNOWN_SKILLS_TAXONOMY, categorize_skills


def extract_text_from_pdf(pdf_stream_or_path) -> str:
    """
    Extract text cleanly from a PDF file buffer or filepath using PyMuPDF.
    """
    try:
        if isinstance(pdf_stream_or_path, (str, bytes, bytearray)):
            if isinstance(pdf_stream_or_path, str) and os.path.isfile(pdf_stream_or_path):
                doc = fitz.open(pdf_stream_or_path)
            else:
                doc = fitz.open(stream=pdf_stream_or_path, filetype="pdf")
        else:
            # Streamlit UploadedFile object
            bytes_data = pdf_stream_or_path.read()
            doc = fitz.open(stream=bytes_data, filetype="pdf")
            
        full_text = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            full_text.append(page.get_text("text"))
        doc.close()
        
        extracted = "\n".join(full_text).strip()
        return extracted if extracted else ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def extract_email(text: str) -> str:
    """Extract email address using regex."""
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """Extract phone number using international and Indian regex patterns."""
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3,5}[-.\s]?\d{4})'
    # Try finding explicit phone labels first
    labeled = re.search(r'(?:phone|tel|mobile|contact|cell)[\s:]*([+\d\s().-]{10,20})', text, re.I)
    if labeled:
        clean_num = labeled.group(1).strip()
        if len(re.sub(r'\D', '', clean_num)) >= 10:
            return clean_num

    matches = re.findall(phone_pattern, text)
    for m in matches:
        full = "".join(m).strip()
        digits = re.sub(r'\D', '', full)
        if 10 <= len(digits) <= 13:
            return full
    return ""


def extract_name(text: str) -> str:
    """
    Extract candidate name from header lines of the resume.
    Avoids common document headings.
    """
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    skip_keywords = {
        'resume', 'curriculum vitae', 'cv', 'profile', 'contact',
        'education', 'experience', 'summary', 'skills', 'objective',
        'page', 'email', 'phone', 'address'
    }
    
    for line in lines[:8]:
        cleaned_line = line.lower()
        if any(skip in cleaned_line for skip in skip_keywords):
            continue
        # Names are typically 2 to 4 capitalized words without digits
        if 2 <= len(line.split()) <= 4 and not re.search(r'[\d@#:\/]', line):
            # Check length is reasonable
            if 3 <= len(line) <= 40:
                return line.title()
                
    return "Candidate Name"


def extract_education(text: str) -> str:
    """
    Extract degrees, educational institutions, or certifications.
    """
    degrees = [
        r'\b(?:Master of Computer Applications|MCA)\b',
        r'\b(?:Bachelor of Computer Applications|BCA)\b',
        r'\b(?:B\.?Tech|Bachelor of Technology)\b',
        r'\b(?:M\.?Tech|Master of Technology)\b',
        r'\b(?:B\.?Sc|Bachelor of Science)\b',
        r'\b(?:M\.?Sc|Master of Science)\b',
        r'\b(?:B\.?E|Bachelor of Engineering)\b',
        r'\b(?:M\.?E|Master of Engineering)\b',
        r'\b(?:MBA|Master of Business Administration)\b',
        r'\b(?:Ph\.?D|Doctor of Philosophy)\b',
        r'\b(?:Bachelor|Master|Diploma|Associate Degree)\b'
    ]
    
    found_degrees = []
    for deg in degrees:
        matches = re.findall(deg, text, re.IGNORECASE)
        for m in matches:
            if m.upper() not in [d.upper() for d in found_degrees]:
                found_degrees.append(m)
                
    # Look for major specialization lines (e.g. Computer Science, Data Science)
    spec_match = re.search(r'(?:in|of)\s+([A-Za-z\s]{3,30})(?:from|university|institute|college|\n)', text, re.I)
    spec = f" ({spec_match.group(1).strip()})" if spec_match and len(spec_match.group(1).strip()) < 30 else ""
    
    if found_degrees:
        return ", ".join(found_degrees) + spec
    return "Degree in Computer Science / Related Field"


def extract_experience_years(text: str) -> float:
    """
    Extract total estimated experience in years using keyword patterns.
    """
    # Pattern 1: Explicit years of experience (e.g., "3+ years of experience", "2.5 years experience")
    match = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)', text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass

    # Pattern 2: Search for year ranges like 2020 - 2024
    year_ranges = re.findall(r'\b(20\d{2}|19\d{2})\s*(?:-|to|–)\s*(20\d{2}|present|current)\b', text, re.IGNORECASE)
    if year_ranges:
        total_yrs = 0
        from datetime import datetime
        current_year = datetime.now().year
        for start, end in year_ranges:
            try:
                s_yr = int(start)
                e_yr = current_year if end.lower() in ['present', 'current'] else int(end)
                if 0 <= (e_yr - s_yr) <= 30:
                    total_yrs += (e_yr - s_yr)
            except Exception:
                pass
        if total_yrs > 0:
            return float(min(total_yrs, 25))

    return 1.0


def extract_skills(text: str) -> tuple:
    """
    Extract skills by scanning against database skills catalog and NLP taxonomy.
    Returns (all_skills, technical_skills, soft_skills).
    """
    text_lower = text.lower()
    found_skills = set()
    
    # 1. Check against DB catalog
    try:
        db_skills = database.get_all_skills_catalog()
        catalog_names = [s['skill_name'] for s in db_skills]
    except Exception:
        catalog_names = []
        
    all_targets = set(catalog_names)
    for cat_list in KNOWN_SKILLS_TAXONOMY.values():
        all_targets.update([s.title() for s in cat_list])
        
    for skill in all_targets:
        s_clean = skill.strip().lower()
        if not s_clean:
            continue
        # Use regex boundary matching
        # Handle special characters like C++, C#, .NET
        escaped = re.escape(s_clean)
        if re.search(r'(?:\b|(?<=[^a-zA-Z0-9]))' + escaped + r'(?:\b|(?=[^a-zA-Z0-9]))', text_lower):
            found_skills.add(skill.strip())
            
    # Classify into Technical and Soft Skills
    soft_pool = [s.lower() for s in KNOWN_SKILLS_TAXONOMY["Soft Skills"]]
    technical_skills = []
    soft_skills = []
    
    for s in sorted(found_skills):
        if s.lower() in soft_pool:
            soft_skills.append(s)
        else:
            technical_skills.append(s)
            
    return sorted(list(found_skills)), technical_skills, soft_skills


def parse_resume(file_or_bytes, filename: str) -> dict:
    """
    Main parser entrypoint. Extracts all attributes into a structured dictionary.
    """
    raw_text = extract_text_from_pdf(file_or_bytes)
    if not raw_text:
        return {
            "success": False,
            "error": "Failed to extract text from the PDF file. Please ensure the file is not password-protected or an image-only scan."
        }

    email = extract_email(raw_text)
    phone = extract_phone(raw_text)
    name = extract_name(raw_text)
    education = extract_education(raw_text)
    experience_years = extract_experience_years(raw_text)
    all_skills, tech_skills, soft_skills = extract_skills(raw_text)
    categorized = categorize_skills(all_skills)

    parsed_data = {
        "success": True,
        "filename": filename,
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "experience_years": experience_years,
        "skills": all_skills,
        "technical_skills": tech_skills,
        "soft_skills": soft_skills,
        "categorized_skills": categorized,
        "raw_text": raw_text
    }
    return parsed_data


class ResumeParser:
    """
    Object-Oriented Resume Parser Class.
    Encapsulates PyMuPDF document extraction, regex-based candidate metadata mining,
    and skill taxonomy matching into an unified object.
    """
    def __init__(self):
        self.supported_format = "pdf"

    def extract_text(self, pdf_stream_or_path) -> str:
        """Extract plain text from PDF stream or file."""
        return extract_text_from_pdf(pdf_stream_or_path)

    def extract_contact_info(self, text: str) -> tuple:
        """Extract candidate email and phone number."""
        return extract_email(text), extract_phone(text)

    def extract_candidate_name(self, text: str) -> str:
        """Extract candidate name from header segments."""
        return extract_name(text)

    def extract_education(self, text: str) -> str:
        """Extract academic qualifications and degrees."""
        return extract_education(text)

    def extract_experience(self, text: str) -> float:
        """Extract estimated years of professional experience."""
        return extract_experience_years(text)

    def extract_skills(self, text: str) -> tuple:
        """Extract all, technical, and soft skills from resume text."""
        return extract_skills(text)

    def parse(self, file_or_bytes, filename: str) -> dict:
        """Parse resume document into a structured profile dictionary."""
        return parse_resume(file_or_bytes, filename)

