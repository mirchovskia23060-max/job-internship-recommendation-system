import csv
from datetime import datetime
from backend.database import SessionLocal, engine, Base
from backend.models import Job, Candidate

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    with open("data/raw/jobs.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job = Job(
                title=row["title"],
                description=row["description"],
                category=row["category"],
                employer=row["employer"],
                location_name=row["location_name"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                employment_type=row["employment_type"],
                work_mode=row["work_mode"],
                required_skills=row["required_skills"],
                target_audience=row["target_audience"],
                salary_min=float(row["salary_min"]),
                salary_max=float(row["salary_max"]),
                application_deadline=datetime.strptime(row["application_deadline"], "%Y-%m-%d").date(),
                vacancies=int(row["vacancies"]),
                filled_positions=int(row["filled_positions"])
            )
            db.add(job)

    with open("data/candidates.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            candidate = Candidate(
                name=row["name"],
                email=row["email"],
                study_area=row["study_area"],
                year_of_study=int(row["year_of_study"]),
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                skills=row["skills"],
                interests=row["interests"],
                preferred_employment_type=row["preferred_employment_type"],
                preferred_work_mode=row["preferred_work_mode"],
                available_from=row["available_from"],
                available_to=row["available_to"],
                min_salary=float(row["min_salary"])
            )
            db.add(candidate)

    db.commit()
    print("Успешно внесени податоци во PostgreSQL!")
finally:
    db.close()
