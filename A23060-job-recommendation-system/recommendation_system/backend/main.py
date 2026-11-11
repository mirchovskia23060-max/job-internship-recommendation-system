from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.database import engine, get_db, Base
from backend.models import Candidate, Job
from backend.schemas import (
    JobCreate, JobResponse,
    CandidateCreate, CandidateResponse,
    RecommendationResponse, RecommendationItem
)
from backend.recommender import evaluate_job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs", response_model=List[JobResponse])
def get_jobs(
    category: Optional[str] = None,
    employment_type: Optional[str] = None,
    remote_only: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    query = db.query(Job).filter(Job.deleted_at.is_(None))
    if category:
        query = query.filter(Job.category.ilike(f"%{category}%"))
    if employment_type:
        query = query.filter(Job.employment_type.ilike(f"%{employment_type}%"))
    if remote_only:
        query = query.filter(Job.work_mode.ilike("Remote"))
    return query.all()

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id, Job.deleted_at.is_(None)).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.post("/jobs", response_model=JobResponse)
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(**job_in.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/candidates", response_model=List[CandidateResponse])
def get_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).filter(Candidate.deleted_at.is_(None)).all()

@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    cand = db.query(Candidate).filter(Candidate.id == candidate_id, Candidate.deleted_at.is_(None)).first()
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return cand

@app.post("/candidates", response_model=CandidateResponse)
def create_candidate(cand_in: CandidateCreate, db: Session = Depends(get_db)):
    cand = Candidate(**cand_in.model_dump())
    db.add(cand)
    db.commit()
    db.refresh(cand)
    return cand

@app.get("/recommendations/{candidate_id}", response_model=RecommendationResponse)
def get_recommendations_for_candidate(candidate_id: int, db: Session = Depends(get_db)):
    cand = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")

    jobs = db.query(Job).filter(Job.deleted_at.is_(None)).all()
    c_dict = {
        "skills": cand.skills,
        "study_area": cand.study_area,
        "preferred_employment_type": cand.preferred_employment_type,
        "preferred_work_mode": cand.preferred_work_mode,
        "latitude": cand.latitude,
        "longitude": cand.longitude,
        "min_salary": cand.min_salary
    }

    recs = []
    for job in jobs:
        res = evaluate_job(c_dict, job)
        if res:
            recs.append(RecommendationItem(**res))

    recs.sort(key=lambda x: x.score, reverse=True)
    return RecommendationResponse(
        candidate_id=cand.id,
        candidate_name=cand.name,
        recommendations=recs
    )

@app.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations_custom(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    skills: Optional[str] = Query(""),
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).filter(Job.deleted_at.is_(None)).all()
    c_dict = {
        "skills": skills,
        "latitude": lat,
        "longitude": lon,
        "min_salary": 0
    }
    recs = []
    for job in jobs:
        res = evaluate_job(c_dict, job)
        if res:
            recs.append(RecommendationItem(**res))
    recs.sort(key=lambda x: x.score, reverse=True)
    return RecommendationResponse(recommendations=recs)
