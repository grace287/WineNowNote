# 🍷 WineNowNote

**한국 와인 애호가를 위한 와인 시음 플랫폼** — PRD 기반 통합 설계 + Django 백엔드 프로젝트.

## 📂 구성

| 항목 | 설명 |
|------|------|
| **PRD.md** | 전체 제품 요구사항 (비전, 기능, 데이터 모델, API, 로드맵, KPI 등) |
| **config/** | Django 설정 (settings 분리, urls, asgi, wsgi) |
| **apps/** | 앱 모듈 (users, wines, notes, dashboard) |
| **requirements/** | 의존성 분리 (base, development, production) |
| **.env.example** | 환경 변수 예시 |

## 📁 프로젝트 구조

```
WineNowNote/
├── config/                    # Django 설정
│   ├── settings/
│   │   ├── __init__.py        # DJANGO_ENV에 따라 development/production 로드
│   │   ├── base.py            # 공통 설정
│   │   ├── development.py    # 개발 환경 (DEBUG, CORS)
│   │   └── production.py     # 운영 환경 (PostgreSQL, ALLOWED_HOSTS)
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── users/                 # 사용자 (User 모델, 회원가입/로그인/프로필)
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── wines/                 # 와인 마스터 (Wine 모델, 검색/상세)
│   │   ├── models.py          # Wine, WINE_TYPES, WINE_COUNTRY_CHOICES
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── notes/                 # 시음 노트 (TastingNote, Template)
│   │   ├── models.py          # Template, TastingNote (와인 FK, 외관/아로마/맛)
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── dashboard/             # 대시보드 (stats, calendar)
│       ├── urls.py
│       └── views.py
├── requirements/
│   ├── base.txt               # 공통 의존성 (Django, DRF, JWT, CORS 등)
│   ├── development.txt        # base + 개발용
│   └── production.txt         # base + gunicorn, psycopg2-binary
├── requirements.txt           # 기본: requirements/development.txt 참조
├── manage.py
├── .env.example
├── .gitignore
├── PRD.md
└── README.md
```

## 🚀 실행 방법

```bash
cd WineNowNote
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
# 또는 환경별: pip install -r requirements/development.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # 선택
python manage.py runserver
```

- **API 문서**: http://127.0.0.1:8000/api/docs/
- **Admin**: http://127.0.0.1:8000/admin/

**환경 변수 (선택)**  
- `DJANGO_ENV`: `development`(기본) / `production`  
- `DJANGO_SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ORIGINS` 등 → `.env.example` 참고

## 📡 API 엔드포인트 요약

| 구분 | 메서드 | 경로 |
|------|--------|------|
| 인증 | POST | `/api/auth/register/`, `/api/auth/login/` |
| 인증 | GET/PATCH | `/api/auth/me/` (JWT 필요) |
| 와인 | GET | `/api/wines/?q=&type=&region=` (검색), `/api/wines/{id}/` |
| 시음 노트 | GET/POST | `/api/tasting-notes/?wine_id=&start_date=&end_date=` |
| 시음 노트 | GET/PATCH/DELETE | `/api/tasting-notes/{id}/` |
| 템플릿 | CRUD | `/api/tasting-notes/templates/` |
| 대시보드 | GET | `/api/dashboard/stats/`, `/api/dashboard/calendar/?year=&month=` |

## 🔗 기존 프로젝트 참조

| 프로젝트 | 참조 포인트 |
|----------|-------------|
| **mywine** | 커뮤니티, 대시보드, 갤러리, 달력, 시음 노트 CRUD, Wine/WineCountry |
| **mywine2** | CustomUser, 시음 노트 필드(슬라이더, 공개 여부, 국가/종류 choices) |
| **winenote** | 시음 노트(외관/향/맛/종합), 이미지 업로드 |

## ✅ 다음 단계

- 프론트(웹/React Native) 연동, 이미지 업로드(S3), Wine-Searcher API 연동, 커뮤니티(Phase 2)
