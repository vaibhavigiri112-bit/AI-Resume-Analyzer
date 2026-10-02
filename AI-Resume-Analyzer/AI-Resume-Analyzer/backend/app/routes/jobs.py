import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Resume, Job
from ..schemas import JobRequest
from ..auth import get_current_user
from ..services.skill_extractor import extract_skills
from ..services.matcher import match_skills

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.post("/analyze")
def analyze_job(data: JobRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.id.desc()).first()
    if not resume:
        return {"message": "Upload a resume first"}
    job_skills = extract_skills(data.description)
    resume_skills = json.loads(resume.skills or "[]")
    score, matched, missing = match_skills(resume_skills, job_skills)
    resume.score = score
    job = Job(user_id=user.id, title=data.title, description=data.description, skills=json.dumps(job_skills), match_score=score)
    db.add(job); db.commit()
    return {"title": data.title, "score": score, "resume_skills": resume_skills, "job_skills": job_skills, "matched": matched, "missing": missing}

@router.get("")
def list_jobs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Job).filter(Job.user_id == user.id).order_by(Job.id.desc()).all()
    return [{"id": j.id, "title": j.title, "score": j.match_score, "skills": json.loads(j.skills or "[]")} for j in rows]
