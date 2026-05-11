import pdfplumber
import re
from collections import defaultdict

EMAIL_RE = re.compile(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d{1,4}[\s-])?(?:\d{10}|\d{5}[\s-]\d{5}|\d{3}[\s-]\d{3}[\s-]\d{4})")

COMMON_SKILLS = ["python","java","c++","machine learning","data analysis","sql","excel","r","matlab","deep learning"]

def extract_text(pdf_path):
    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                text_pages.append(txt)
    return "\n".join(text_pages)

def extract_email(text):
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None

def extract_phone(text):
    m = PHONE_RE.search(text)
    return m.group(0) if m else None

def extract_skills(text):
    t = text.lower()
    found = [s for s in COMMON_SKILLS if s in t]
    return found

def parse_pdf(path):
    text = extract_text(path)
    parsed = {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }
    return parsed, text
