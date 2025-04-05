import streamlit as st
import fitz  # PyMuPDF
import spacy
from typing import List, Dict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a sample skill set (you can expand it)
SKILLS_DB = [
    "python", "java", "c++", "html", "css", "javascript", "react", "node.js", "sql",
    "machine learning", "data analysis", "pandas", "numpy", "django", "flask",
    "communication", "teamwork", "git", "github", "docker", "aws", "kubernetes"
]

def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file using PyMuPDF"""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text"""
    text = text.lower()
    doc = nlp(text)
    extracted_skills = set()
    for token in doc:
        if token.text in SKILLS_DB:
            extracted_skills.add(token.text)
    return list(extracted_skills)

def compare_resumes(resume_skills: Dict[str, List[str]]) -> List[tuple]:
    """Compare resumes and return matching pairs with common skills"""
    matched_pairs = []
    names = list(resume_skills.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            skills_i = set(resume_skills[names[i]])
            skills_j = set(resume_skills[names[j]])
            common = skills_i & skills_j
            if common:
                matched_pairs.append((names[i], names[j], list(common)))
    return matched_pairs

# Streamlit UI
st.title("🤝 Resume Matcher - Find Skill Matches")

uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    resume_skills = {}
    
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        skills = extract_skills(text)
        resume_skills[file.name] = skills
        st.write(f"**{file.name}** - Extracted Skills: {', '.join(skills) if skills else 'No skills found'}")

    if len(resume_skills) >= 2:
        matches = compare_resumes(resume_skills)
        st.subheader("🔍 Matched Resumes Based on Skills:")
        if matches:
            for name1, name2, common_skills in matches:
                st.write(f"**{name1}** ↔ **{name2}** | Common Skills: {', '.join(common_skills)}")
        else:
            st.write("No matching resumes found based on skills.")
