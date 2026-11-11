from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from backend.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    study_area = Column(String)
    year_of_study = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    skills = Column(String)
    interests = Column(String)
    preferred_employment_type = Column(String)
    preferred_work_mode = Column(String)
    available_from = Column(String)
    available_to = Column(String)
    min_salary = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, index=True)
    employer = Column(String)
    location_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    employment_type = Column(String, index=True)
    work_mode = Column(String)
    required_skills = Column(String)
    target_audience = Column(String)
    salary_min = Column(Float)
    salary_max = Column(Float)
    application_deadline = Column(Date)
    vacancies = Column(Integer, default=1)
    filled_positions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
