import re

SKILLS = [
    "python", "java", "c", "c++", "javascript", "typescript", "react", "next.js",
    "node.js", "fastapi", "django", "flask", "html", "css", "sql", "mysql",
    "postgresql", "mongodb", "git", "github", "docker", "kubernetes", "aws",
    "azure", "machine learning", "deep learning", "artificial intelligence", "nlp",
    "natural language processing", "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "opencv", "data structures", "algorithms", "rest api", "rest apis",
    "linux", "cybersecurity", "networking", "tableau", "power bi"
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())

def extract_skills(text: str) -> list[str]:
    t = normalize(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, t):
            found.append(skill)
    return sorted(set(found))
