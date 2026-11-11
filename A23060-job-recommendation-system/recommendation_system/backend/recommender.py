import math
from datetime import date
from typing import Tuple, Optional

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Радиус на Земјата во км
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def evaluate_job(candidate_dict: dict, job) -> Optional[dict]:
    today = date.today()
    available_pos = job.vacancies - job.filled_positions

    # Елиминација на пополнети или истечени огласи
    if available_pos <= 0 or job.application_deadline < today:
        return None

    score = 0
    reasons = []

    # 1. Вештини (макс 35 поени)
    c_skills = {s.strip().lower() for s in candidate_dict.get("skills", "").split(",") if s.strip()}
    j_skills = {s.strip().lower() for s in (job.required_skills or "").split(",") if s.strip()}

    if j_skills:
        matched_skills = c_skills.intersection(j_skills)
        match_ratio = len(matched_skills) / len(j_skills)
        skill_score = int(match_ratio * 35)
        score += skill_score
        if matched_skills:
            reasons.append(f"Се совпаѓа со вашите вештини: {', '.join([s.title() for s in matched_skills])}")

    # 2. Образование (макс 15 поени)
    c_study = candidate_dict.get("study_area", "").lower()
    j_target = (job.target_audience or "").lower()
    if j_target == "all graduates" or j_target == c_study or c_study in j_target:
        score += 15
        reasons.append("Соодветно за вашата насока на студии")

    # 3. Работен однос (макс 15 поени)
    c_type = candidate_dict.get("preferred_employment_type", "").lower()
    if c_type == (job.employment_type or "").lower():
        score += 15
        reasons.append(f"Одговара на посакуваниот тип ({job.employment_type})")

    # 4. Локација и оддалеченост (макс 15 поени)
    dist = None
    c_lat = candidate_dict.get("latitude")
    c_lon = candidate_dict.get("longitude")

    if job.work_mode.lower() == "remote":
        score += 15
        reasons.append("Целосно далечинска позиција (Remote)")
    elif c_lat is not None and c_lon is not None and job.latitude and job.longitude:
        dist = haversine_distance(c_lat, c_lon, job.latitude, job.longitude)
        if dist <= 3.0:
            score += 15
            reasons.append(f"Одлична локација ({dist} km од вас)")
        elif dist <= 10.0:
            score += 10
            reasons.append(f"Прифатлива оддалеченост ({dist} km)")
        else:
            score += 5
    else:
        score += 8

    # 5. Плата (макс 10 поени)
    c_salary = candidate_dict.get("min_salary", 0)
    if job.salary_max and job.salary_max >= c_salary:
        score += 10
        reasons.append("Ја исполнува вашата минимална очекувана плата")
    elif job.salary_min and job.salary_min >= c_salary * 0.8:
        score += 5

    # 6. Достапност и рок (макс 10 поени)
    days_left = (job.application_deadline - today).days
    if days_left > 7 and available_pos >= 2:
        score += 10
    else:
        score += 5

    return {
        "job_id": job.id,
        "title": job.title,
        "category": job.category,
        "employer": job.employer,
        "employment_type": job.employment_type,
        "work_mode": job.work_mode,
        "location_name": job.location_name,
        "distance_km": dist,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "application_deadline": job.application_deadline.strftime("%Y-%m-%d"),
        "available_positions": available_pos,
        "score": min(score, 100),
        "reason": ". ".join(reasons) + "."
    }
