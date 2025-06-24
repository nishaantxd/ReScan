import re
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf_or_image(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            return " ".join([page.get_text() for page in doc])
    elif uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)
    return ""

def extract_section(text, section_keywords):
    pattern = '|'.join([re.escape(keyword) for keyword in section_keywords])
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    sections = {}
    for i in range(len(matches)):
        start = matches[i].end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        section_name = matches[i].group().lower()
        sections[section_name] = text[start:end].strip()

    return sections

def extract_resume_info(resume_text):
    keywords = {
        "skills": ["skills", "technical skills"],
        "education": ["education", "academic background", "qualifications"],
        "experience": ["experience", "work experience", "professional experience"]
    }

    resume_info = {}
    for section, keys in keywords.items():
        sections = extract_section(resume_text, keys)
        resume_info[section] = list(sections.values())

    return resume_info
