import csv
import os
import random
from datetime import datetime, timedelta

os.makedirs("data/raw", exist_ok=True)

SKOPJE_LAT = 41.9981
SKOPJE_LON = 21.4254

CATEGORIES = [
    "Software Development", "Data Analytics", "Marketing", "Business",
    "Design", "Finance", "Human Resources", "Customer Support"
]

SKILLS_BY_CAT = {
    "Software Development": ["Python", "SQL", "Git", "FastAPI", "JavaScript", "Docker"],
    "Data Analytics": ["Python", "SQL", "Excel", "PowerBI", "Pandas", "R"],
    "Marketing": ["Social Media", "Communication", "SEO", "Content Writing", "Excel"],
    "Business": ["Excel", "Communication", "Project Management", "Agile", "Reporting"],
    "Design": ["Figma", "Adobe XD", "Photoshop", "Illustrator", "UI/UX"],
    "Finance": ["Excel", "Financial Modeling", "Accounting", "Analysis", "Reporting"],
    "Human Resources": ["Communication", "Recruitment", "Interviewing", "Administration"],
    "Customer Support": ["Communication", "Problem Solving", "CRM", "English", "Ticketing"]
}

EMPLOYMENT_TYPES = ["Internship", "Full-time", "Part-time"]
WORK_MODES = ["On-site", "Hybrid", "Remote"]
STUDY_AREAS = ["Computer Science", "Economics", "Marketing", "Design", "Business Administration"]

# 1. Генерирање на огласи за работа (120 огласи)
jobs = []
for i in range(1, 121):
    cat = random.choice(CATEGORIES)
    skills = random.sample(SKILLS_BY_CAT[cat], k=random.randint(2, 4))
    emp_type = random.choice(EMPLOYMENT_TYPES)
    work_mode = random.choice(WORK_MODES)
    vacancies = random.randint(1, 5)
    filled = random.randint(0, vacancies - 1)

    # 90% од огласите со валиден рок во иднината
    days_ahead = random.randint(10, 90) if random.random() > 0.1 else -5
    deadline = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    lat = round(SKOPJE_LAT + random.uniform(-0.05, 0.05), 4)
    lon = round(SKOPJE_LON + random.uniform(-0.05, 0.05), 4)

    if emp_type == "Internship":
        s_min, s_max = random.choice([(15000, 22000), (18000, 25000), (20000, 30000)])
    else:
        s_min, s_max = random.choice([(35000, 50000), (45000, 65000), (60000, 90000)])

    jobs.append({
        "job_id": i,
        "title": f"Junior {cat} Specialist" if emp_type != "Internship" else f"{cat} Intern",
        "description": f"Great career opportunity in the field of {cat}.",
        "category": cat,
        "employer": f"Company {chr(65 + (i % 26))}",
        "location_name": "Skopje",
        "latitude": lat,
        "longitude": lon,
        "employment_type": emp_type,
        "work_mode": work_mode,
        "required_skills": ",".join(skills),
        "target_audience": random.choice(STUDY_AREAS + ["All Graduates"]),
        "salary_min": s_min,
        "salary_max": s_max,
        "application_deadline": deadline,
        "vacancies": vacancies,
        "filled_positions": filled
    })

with open("data/raw/jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
    writer.writeheader()
    writer.writerows(jobs)

# 2. Генерирање на кандидати (80 кандидати)
candidates = []
first_names = ["Ana", "Marko", "Elena", "Stefan", "Ivana", "Bojan", "Marija", "Darko"]
last_names = ["Petrova", "Ivanov", "Stojanova", "Trajkovski", "Nikolovska", "Dimitrov", "Popova", "Jovanov"]

for i in range(1, 81):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    study = random.choice(STUDY_AREAS)
    cat_match = "Software Development" if study == "Computer Science" else random.choice(CATEGORIES)
    cand_skills = random.sample(SKILLS_BY_CAT[cat_match], k=random.randint(2, 4))
    interests = random.sample(CATEGORIES, k=random.randint(1, 3))

    candidates.append({
        "candidate_id": i,
        "name": name,
        "email": f"candidate{i}@example.com",
        "study_area": study,
        "year_of_study": random.randint(1, 4),
        "latitude": round(SKOPJE_LAT + random.uniform(-0.04, 0.04), 4),
        "longitude": round(SKOPJE_LON + random.uniform(-0.04, 0.04), 4),
        "skills": ",".join(cand_skills),
        "interests": ",".join(interests),
        "preferred_employment_type": random.choice(EMPLOYMENT_TYPES),
        "preferred_work_mode": random.choice(WORK_MODES),
        "available_from": "09:00",
        "available_to": "17:00",
        "min_salary": random.choice([15000, 20000, 25000, 35000, 45000])
    })

with open("data/candidates.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=candidates[0].keys())
    writer.writeheader()
    writer.writerows(candidates)

print("Генерирани се data/raw/jobs.csv и data/candidates.csv!")
