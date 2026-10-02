def match_skills(resume_skills: list[str], job_skills: list[str]):
    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}
    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    score = round((len(matched) / len(job_set)) * 100, 2) if job_set else 0
    return score, matched, missing
