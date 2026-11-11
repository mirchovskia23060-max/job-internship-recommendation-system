# Систем за препорака на пракси и вработувања

Систем кој препорачува работни позиции (пракси и вработувања) на студенти врз основа
на детерминистички алгоритам за бодирање (вештини, образование, работен однос,
локација, плата и рок).

## Структура

```text
recommendation_system/
├── data/
│   ├── raw/
│   │   └── jobs.csv          # генерирани огласи (120)
│   └── candidates.csv        # генерирани кандидати (80)
├── backend/
│   ├── __init__.py
│   ├── database.py           # SQLAlchemy engine / сесии
│   ├── models.py             # ORM модели (Candidate, Job)
│   ├── schemas.py            # Pydantic шеми
│   ├── recommender.py        # логика за бодирање + Haversine
│   └── main.py               # FastAPI endpoints
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── generate_data.py          # генерира синтетички CSV податоци
├── seed_db.py                # внесува CSV во PostgreSQL
├── requirements.txt
└── README.md
```

## Алгоритам за бодирање (вкупно 100 поени)

| Критериум             | Макс. поени |
|-----------------------|-------------|
| Вештини               | 35          |
| Образование           | 15          |
| Работен однос         | 15          |
| Дистанца / Режим      | 15          |
| Плата                 | 10          |
| Рок / Слободни места  | 10          |

Огласите кои се пополнети или со истечен рок автоматски се исклучуваат.

## Стартување

1. Инсталација на зависности:
   ```bash
   pip install -r requirements.txt
   ```

2. Креирање на базата во PostgreSQL:
   ```bash
   createdb -U postgres rec_db
   ```
   (по потреба постави `DATABASE_URL`, стандардно
   `postgresql://postgres:postgres@localhost:5432/rec_db`)

3. Генерирање на податоци и полнење на базата:
   ```bash
   python generate_data.py
   python seed_db.py
   ```

4. Стартување на бекендот:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

5. Преглед на апликацијата:
   ```bash
   python -m http.server 3000 --directory frontend
   # потоа отвори http://localhost:3000/?candidate_id=1
   ```

## Главни endpoints

- `GET /jobs` — листа на огласи (филтри: `category`, `employment_type`, `remote_only`)
- `GET /jobs/{job_id}` — еден оглас
- `POST /jobs` — нов оглас
- `GET /candidates` — листа на кандидати
- `GET /candidates/{candidate_id}` — еден кандидат
- `POST /candidates` — нов кандидат
- `GET /recommendations/{candidate_id}` — препораки за кандидат
- `GET /recommendations?lat=&lon=&skills=` — препораки по сопствени параметри
