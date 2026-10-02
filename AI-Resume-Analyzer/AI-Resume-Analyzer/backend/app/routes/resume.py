import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Resume
from ..auth import get_current_user
from ..services.pdf_parser import extract_text
from ..services.skill_extractor import extract_skills

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Please upload a PDF resume")
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(400, "PDF must be smaller than 5 MB")
    text = extract_text(data)
    if not text:
        raise HTTPException(400, "Could not extract text. Use a text-based PDF.")
    skills = extract_skills(text)
    resume = Resume(user_id=user.id, filename=file.filename or "resume.pdf", extracted_text=text, skills=json.dumps(skills))
    db.add(resume); db.commit(); db.refresh(resume)
    return {"id": resume.id, "filename": resume.filename, "skills": skills, "text_preview": text[:500]}

@router.get("")
def list_resumes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.id.desc()).all()
    return [{"id": r.id, "filename": r.filename, "skills": json.loads(r.skills or "[]"), "score": r.score} for r in rows]
