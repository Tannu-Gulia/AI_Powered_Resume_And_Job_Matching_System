"""
NLP Processing Module for AI-Powered Resume & Job Matching System
Provides text cleaning, tokenization, stopword removal, keyword extraction,
and skill categorization.
"""

import re
import string

# Fallback English stopwords in case NLTK corpus is unavailable
FALLBACK_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
    'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    STOPWORDS = set(stopwords.words('english'))
except Exception:
    STOPWORDS = FALLBACK_STOPWORDS


def clean_text(text: str) -> str:
    """
    Clean raw input text by removing URLs, special characters, and extra spaces.
    Preserves alphanumeric terms, hyphens, and plus signs (e.g. C++, CI/CD).
    """
    if not text:
        return ""
    # Remove URL links
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    # Remove email addresses from raw text processing
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' ', text)
    # Normalize slashes & special technical markers
    text = text.replace('/', ' ')
    # Remove non-word characters except +, #, -
    text = re.sub(r'[^\w\s\+#\-]', ' ', text)
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()


def tokenize_and_remove_stopwords(text: str) -> list:
    """
    Tokenize text and remove English stopwords.
    Returns a list of significant lowercase tokens.
    """
    cleaned = clean_text(text)
    # Tokenize by whitespace and punctuation boundary
    raw_tokens = re.findall(r'\b[\w\+#\-]{2,}\b', cleaned)
    tokens = [t for t in raw_tokens if t not in STOPWORDS and not t.isdigit()]
    return tokens


def extract_keywords(text: str, top_n: int = 15) -> list:
    """
    Extract the most frequent significant keywords from text.
    """
    tokens = tokenize_and_remove_stopwords(text)
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]


# Comprehensive Skills Knowledge Base for NLP Extraction
KNOWN_SKILLS_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "r", "sql", "go",
        "rust", "php", "ruby", "kotlin", "swift", "scala", "perl", "bash", "shell",
        "html", "html5", "css", "css3"
    ],
    "Frameworks & Libraries": [
        "react", "angular", "vue", "vue.js", "node", "node.js", "express", "express.js",
        "django", "flask", "fastapi", "spring", "spring boot", "asp.net", "laravel",
        "pandas", "numpy", "scipy", "scikit-learn", "tensorflow", "pytorch", "keras",
        "opencv", "matplotlib", "seaborn", "plotly", "nltk", "spacy", "huggingface",
        "transformers", "tailwind", "bootstrap"
    ],
    "Data & AI": [
        "machine learning", "deep learning", "natural language processing", "nlp",
        "computer vision", "artificial intelligence", "data science", "data analysis",
        "data analytics", "data engineering", "big data", "spark", "hadoop", "kafka",
        "tableau", "power bi", "excel", "statistics", "data mining", "predictive modeling",
        "time series", "neural networks", "llm", "generative ai", "rag"
    ],
    "Databases & Cloud": [
        "postgresql", "mysql", "mongodb", "redis", "oracle", "sqlite", "snowflake",
        "cassandra", "dynamodb", "aws", "azure", "gcp", "google cloud", "docker",
        "kubernetes", "terraform", "ci/cd", "jenkins", "git", "github", "gitlab",
        "linux", "devops", "cloud computing"
    ],
    "Soft Skills": [
        "communication", "problem solving", "team leadership", "critical thinking",
        "agile", "agile methodology", "scrum", "time management", "adaptability",
        "collaboration", "presentation skills", "analytical thinking", "negotiation",
        "creativity", "work ethic", "leadership"
    ]
}


def categorize_skills(skills_list: list) -> dict:
    """
    Categorize a list of extracted skills into taxonomy domains.
    """
    categorized = {
        "Programming Languages": [],
        "Frameworks & Libraries": [],
        "Data & AI": [],
        "Databases & Cloud": [],
        "Soft Skills": [],
        "Other Skills": []
    }
    
    for s in skills_list:
        s_lower = s.strip().lower()
        matched = False
        for category, members in KNOWN_SKILLS_TAXONOMY.items():
            if s_lower in members or any(m in s_lower for m in members):
                categorized[category].append(s.strip())
                matched = True
                break
        if not matched:
            categorized["Other Skills"].append(s.strip())
            
    # Remove empty categories
    return {k: list(set(v)) for k, v in categorized.items() if v}


class NLPProcessor:
    """
    Object-Oriented NLP Processor Class.
    Encapsulates text normalization, tokenization, stopword removal,
    keyword salience calculation, and domain skill categorization.
    """
    def __init__(self, stopwords_set=None, taxonomy=None):
        self.stopwords = stopwords_set or STOPWORDS
        self.taxonomy = taxonomy or KNOWN_SKILLS_TAXONOMY

    def clean(self, text: str) -> str:
        """Clean and normalize raw text."""
        return clean_text(text)

    def tokenize(self, text: str) -> list:
        """Tokenize text and remove stopwords."""
        return tokenize_and_remove_stopwords(text)

    def extract_keywords(self, text: str, top_n: int = 15) -> list:
        """Extract top frequent significant keywords."""
        return extract_keywords(text, top_n)

    def categorize_skills(self, skills_list: list) -> dict:
        """Classify skills into standard taxonomy categories."""
        return categorize_skills(skills_list)

