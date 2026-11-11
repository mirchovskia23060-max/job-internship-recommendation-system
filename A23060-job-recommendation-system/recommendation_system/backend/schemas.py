from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    employer: str
    location_name: str
    latitude: float
    longitude: float
    employment_type: str
    work_mode: str
    required_skills: str
    target_audience: str
    salary_min: float
    salary_max: float
    application_deadline: date
    vacancies: int
    filled_positions: int = 0

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    name: str
    email: str
    study_area: str
    year_of_study: int
    latitude: float
    longitude: float
    skills: str
    interests: str
    preferred_employment_type: str
    preferred_work_mode: str
    available_from: str
    available_to: str
    min_salary: float

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class RecommendationItem(BaseModel):
    job_id: int
    title: str
    category: str
    employer: str
    employment_type: str
    work_mode: str
    location_name: str
    distance_km: Optional[float] = None
    salary_min: float
    salary_max: float
    application_deadline: str
    available_positions: int
    score: int
    reason: str

class RecommendationResponse(BaseModel):
    candidate_id: Optional[int] = None
    candidate_name: Optional[str] = None
    recommendations: List[RecommendationItem]
