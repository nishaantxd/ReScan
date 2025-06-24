from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# Load BERT model
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text_list(text_list):
    return " ".join([t.strip() for t in text_list if t.strip()])

def get_bert_score(text1, text2):
    if not text1 or not text2:
        return 0
    embeddings = bert_model.encode([text1, text2], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return round(score * 100, 2)

def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def compare_resume_with_jd(resume_info, jd_text):
    section_scores = {}

    resume_sections = {
        "skills": clean_text_list(resume_info.get("skills", [])),
        "experience": clean_text_list(resume_info.get("experience", [])),
        "education": clean_text_list(resume_info.get("education", [])),
    }

    for section, text in resume_sections.items():
        section_scores[section] = get_bert_score(text, jd_text)

    overall_score = round(sum(section_scores.values()) / len(section_scores), 2)

    # Keyword comparison (case-insensitive, token-based)
    resume_text = " ".join(resume_sections.values())
    jd_keywords = tokenize(jd_text)
    resume_keywords = tokenize(resume_text)

    missing_keywords = list(jd_keywords - resume_keywords)
    matched_keywords = list(jd_keywords & resume_keywords)

    return {
        "section_scores": section_scores,
        "overall_score": overall_score,
        "missing_keywords": missing_keywords,
        "matched_count": len(matched_keywords),
        "missing_count": len(missing_keywords)
    }
