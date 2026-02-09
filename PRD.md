# 🍷 와인 시음 플랫폼 PRD (Product Requirements Document)

> **WineNowNote** — 기존 프로젝트(mywine, mywine2, winenote)를 참고하여 체계적으로 재설계한 통합 PRD

## 📑 목차
1. [제품 개요](#1-제품-개요)
2. [문제 정의 및 목표](#2-문제-정의-및-목표)
3. [사용자 페르소나](#3-사용자-페르소나)
4. [기능 요구사항](#4-기능-요구사항)
5. [비기능 요구사항](#5-비기능-요구사항)
6. [기술 아키텍처](#6-기술-아키텍처)
7. [UI/UX 디자인 원칙](#7-uiux-디자인-원칙)
8. [데이터 모델](#8-데이터-모델)
9. [API 명세](#9-api-명세)
10. [개발 로드맵](#10-개발-로드맵)
11. [성공 지표 (KPI)](#11-성공-지표-kpi)
12. [리스크 및 완화 전략](#12-리스크-및-완화-전략)
13. [출시 전략](#13-출시-전략)
14. [부록 및 참조](#14-부록-및-참조)

---

## 1. 제품 개요

### 1.1 프로젝트 비전
**"한국 와인 애호가를 위한 가장 직관적이고 개인화된 와인 경험 플랫폼"**

### 1.2 제품 설명
비비노(Vivino)와 같은 글로벌 와인 앱이 한국 사용자의 문화적 특성을 반영하지 못하는 점을 개선하여, 한국어 중심의 UI/UX, 개인화된 시음 노트, 데이터 분석, 커뮤니티 기능을 제공하는 모바일 우선 플랫폼입니다.

### 1.3 핵심 가치 제안 (Value Proposition)
| 기존 솔루션 (비비노) | 우리 제품 |
|---|---|
| 영어 중심 인터페이스 | 한국어 네이티브 경험 |
| 고정된 리뷰 템플릿 | 커스터마이징 가능한 시음 노트 |
| 단순 평점/리뷰 | 데이터 분석 & 시각화 대시보드 |
| 글로벌 커뮤니티 | 한국 와인 문화 중심 커뮤니티 |

### 1.4 기존 프로젝트 참조
| 프로젝트 | 참조 포인트 |
|----------|-------------|
| **mywine** | 커뮤니티, 대시보드, 갤러리, 달력, 시음 노트 CRUD, 사용자 프로필 |
| **mywine2** | 사용자(CustomUser), 시음 노트 모델(와인 종류/국가/슬라이더), 공개 여부 |
| **winenote** | 시음 노트(외관/향/맛/종합), 이미지 업로드, PRD 초안, 시리얼라이저 |

---

## 2. 문제 정의 및 목표

### 2.1 해결하려는 문제
1. **문화적 장벽**: 기존 앱들이 한국어 지원이 부족하거나 한국 사용자 특성을 고려하지 않음
2. **개인화 부족**: 획일화된 리뷰 양식으로 개인의 취향과 경험을 상세히 기록하기 어려움
3. **데이터 활용 미흡**: 시음 기록이 쌓여도 자신의 선호도를 분석하기 어려움
4. **지역 커뮤니티 부재**: 한국 와인 애호가들이 교류할 수 있는 전용 공간 부족

### 2.2 제품 목표
- **단기 (6개월)**: 1,000명의 활성 사용자 확보, MVP 출시
- **중기 (1년)**: 10,000명 사용자, 월 평균 시음 기록 5회/인
- **장기 (2년)**: 한국 와인 앱 시장 점유율 1위, 와인 수입업체 파트너십 체결

---

## 3. 사용자 페르소나

### 페르소나 1: "와인 애호가 지민"
- **연령**: 32세 | **직업**: IT 기업 마케터
- **특징**: 주 1-2회 와인 시음, 취향 기록 중시, 데이터 기반 의사결정 선호
- **니즈**: 체계적인 시음 노트 관리, 선호도 패턴 분석, 비슷한 취향 추천 교환

### 페르소나 2: "와린이 수진"
- **연령**: 27세 | **직업**: 디자이너
- **특징**: 와인 입문 단계, 예쁜 디자인 선호, SNS 활동 활발
- **니즈**: 쉬운 와인 검색/정보 확인, 사진으로 간편 기록, 커뮤니티 추천

### 페르소나 3: "소믈리에 준호"
- **연령**: 38세 | **직업**: 레스토랑 소믈리에
- **특징**: 전문가 수준 지식, 상세한 테이스팅 노트 작성
- **니즈**: 전문 테이스팅 템플릿, 와인 DB 접근, 전문가 커뮤니티

---

## 4. 기능 요구사항

### 4.1 MVP 기능 (Phase 1 - 3개월)

#### 4.1.1 사용자 인증 및 프로필 (P0)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| AUTH-001 | 회원가입 | 이메일/소셜 로그인 지원 | 이메일 인증 완료, 카카오/네이버/구글 OAuth 연동 |
| AUTH-002 | 로그인/로그아웃 | JWT 토큰 기반 인증 | 자동 로그인 유지, 토큰 만료 시 재발급 |
| AUTH-003 | 프로필 관리 | 닉네임, 프로필 사진, 선호 와인 설정 | 프로필 이미지 업로드, 선호 와인 타입 선택 |

#### 4.1.2 와인 검색 및 정보 (P0)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| SEARCH-001 | 와인 검색 | 이름/종류/산지로 검색 | 자동완성 지원, 검색 결과 0.5초 이내 반환 |
| SEARCH-002 | 와인 상세 정보 | 기본 정보 표시 | 이름, 종류, 산지, 품종, 도수, 가격, Wine-Searcher API 연동 |
| SEARCH-003 | 와인 필터링 | 종류/가격대/산지 필터 | 다중 필터 조합 가능, 필터 결과 즉시 반영 |

#### 4.1.3 사진 업로드 (P0)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| PHOTO-001 | 와인 사진 촬영/업로드 | 카메라/갤러리 연동 | 이미지 최대 5MB, JPEG/PNG 지원 |
| PHOTO-002 | 이미지 저장 | 클라우드 스토리지 저장 | S3/Firebase 연동, 썸네일 자동 생성 |
| PHOTO-003 | OCR (선택) | 라벨에서 텍스트 추출 | 와인명 인식률 70% 이상, 빈티지 연도 추출 |

#### 4.1.4 시음 노트 (P0)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| NOTE-001 | 노트 작성 | 기본 템플릿 제공 | 날짜, 장소, 평점, 메모 필수, 리치 텍스트 지원 |
| NOTE-002 | 템플릿 커스터마이징 | 사용자 정의 필드 추가 | 최대 20개 커스텀 필드, 필드 타입: 텍스트/숫자/선택지 |
| NOTE-003 | 노트 수정/삭제 | CRUD 기능 | 수정 이력 저장, 삭제 시 확인 다이얼로그 |
| NOTE-004 | 노트 검색 | 키워드 검색 | 와인명/메모 내용 검색, 검색 하이라이팅 |

#### 4.1.5 달력 뷰 (P1)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| CAL-001 | 월간 달력 | 시음 기록 날짜 표시 | 기록 있는 날짜 강조, 월 단위 네비게이션 |
| CAL-002 | 일별 상세 뷰 | 날짜 클릭 시 기록 목록 | 해당 날짜 모든 기록 표시, 썸네일 미리보기 |

---

### 4.2 Phase 2 기능 (4-5개월차)

#### 4.2.1 데이터 분석 대시보드 (P1)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| DASH-001 | 시음 통계 | 총 시음 횟수, 월별 트렌드 | 차트 라이브러리 연동, 기간 필터 (1/3/12개월) |
| DASH-002 | 선호도 분석 | 가장 많이 마신 와인 종류/산지 | 파이/바 차트, Top 5 표시 |
| DASH-003 | 평점 분석 | 평균 평점, 평점 분포 | 히스토그램, 평점별 와인 목록 링크 |
| DASH-004 | 가격 분석 | 평균 소비 금액, 가격대별 분포 | 월별 지출 추이, 예산 대비 분석 (선택) |

#### 4.2.2 커뮤니티 기능 (P1)
| 기능 ID | 기능명 | 설명 | 수용 기준 |
|---------|--------|------|-----------|
| COMM-001 | 공개 리뷰 | 시음 노트 공개/비공개 설정 | 토글 버튼, 기본값: 비공개 |
| COMM-002 | 좋아요/댓글 | 다른 사용자 리뷰에 반응 | 실시간 알림, 댓글 중첩 1단계 |
| COMM-003 | 토론 게시판 | 주제별 게시판 | 와인 추천/질문/정보 카테고리, 검색 |
| COMM-004 | 팔로우 시스템 | 사용자 팔로우 | 팔로잉 피드, 알림 설정 |

---

### 4.3 Phase 3 기능 (6개월차 이후)
| 기능 ID | 기능명 | 우선순위 |
|---------|--------|----------|
| ADV-001 | AI 추천 시스템 | P2 |
| ADV-002 | 와인 컬렉션 관리 (셀러) | P2 |
| ADV-003 | 와인 페어링 추천 | P2 |
| ADV-004 | 오프라인 이벤트 연동 | P3 |
| ADV-005 | 와인샵 제휴 연동 | P2 |

---

## 5. 비기능 요구사항

### 5.1 성능
| 항목 | 요구사항 |
|------|----------|
| 앱 초기 로딩 시간 | 2초 이내 |
| API 응답 시간 | 평균 500ms 이내 |
| 이미지 업로드 시간 | 5MB 기준 3초 이내 |
| 동시 사용자 처리 | 초기 1,000명 지원 |

### 5.2 보안
- HTTPS 통신 필수
- JWT 토큰 만료: Access 1시간, Refresh 30일
- 개인정보 암호화 저장 (AES-256)
- GDPR/개인정보보호법 준수

### 5.3 접근성
- 웹 접근성 WCAG 2.1 AA 수준
- 다크모드 지원
- 폰트 크기 조절 (최대 150%)

### 5.4 호환성
- **iOS**: 14.0 이상 | **Android**: 8.0 (API 26) 이상
- **화면 크기**: 320px ~ 428px 너비 최적화

---

## 6. 기술 아키텍처

### 6.1 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                   Client Layer                       │
├─────────────────────────────────────────────────────┤
│  React Native (iOS/Android)                           │
│  - Redux Toolkit (상태 관리)                         │
│  - React Navigation (라우팅)                          │
│  - React Native Paper (UI 컴포넌트)                 │
└──────────────────┬──────────────────────────────────┘
                   │ REST API (JSON)
                   ▼
┌─────────────────────────────────────────────────────┐
│                  API Gateway                         │
│              (AWS API Gateway / Nginx)               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Application Layer                       │
├─────────────────────────────────────────────────────┤
│  Django 4.2 + Django REST Framework                 │
│  - JWT (djangorestframework-simplejwt)             │
│  - Celery (비동기) | Redis (캐싱 & 메시지 브로커)   │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
┌─────────────┐ ┌──────────┐ ┌──────────────┐
│ PostgreSQL  │ │ AWS S3   │ │ 3rd Party API│
│ (주 DB)     │ │ (이미지) │ │ (Wine Search)│
└─────────────┘ └──────────┘ └──────────────┘
```

### 6.2 기술 스택 상세

**프론트엔드:** React Native 0.72+, TypeScript 5.0+, Redux Toolkit + RTK Query, React Native Paper 5.x, React Navigation 6.x, react-native-chart-kit, react-native-calendars, react-native-image-picker, react-native-pell-rich-editor

**백엔드:** Django 4.2 + DRF 3.14, Python 3.11+, djangorestframework-simplejwt, drf-spectacular (OpenAPI 3.0), Celery 5.x, Redis 7.x, Pillow 10.x, pytesseract (선택)

**데이터베이스:** PostgreSQL 15, Redis 7.x, Elasticsearch 8.x (Phase 2)

**인프라:** AWS (EC2/ECS, S3, RDS, ElastiCache, CloudFront), Docker + Docker Compose, GitHub Actions, CloudWatch + Sentry

---

## 7. UI/UX 디자인 원칙

### 7.1 디자인 시스템

**색상 팔레트**
```css
--wine-burgundy: #722F37;   /* 주 버튼, 강조 */
--wine-deep-red: #8B1E3F;   /* 헤더, 중요 요소 */
--wine-rose: #C9A6A6;       /* 보조 요소 */
--cream: #FFF8F0;           /* 배경 */
--warm-gray: #E5D9D0;       /* 카드 배경 */
--dark-gray: #3A3A3A;       /* 본문 텍스트 */
--gold: #D4AF37;            /* 별점, 뱃지 */
--success: #2D6E3F;         /* 성공 메시지 */
--error: #C1292E;           /* 에러 메시지 */
```

**타이포그래피:** Pretendard (한글), Inter (영문/숫자)  
**간격:** 4px(xs), 8px(sm), 16px(md), 24px(lg), 32px(xl)

### 7.2 주요 화면 구성
- **홈**: 이번 달 시음 횟수, 월별 활동 차트, 최근 시음 기록, [새 시음 기록하기]
- **시음 노트 작성**: 사진 추가, 와인 검색, 평점/날짜/장소, 템플릿 선택, 색상/바디/산미/타닌, 메모(리치 텍스트)

---

## 8. 데이터 모델

### 8.1 ERD 요약

```
User ──┬── TastingNote ◀── Wine
       ├── Template
       └── (Comment, Like → TastingNote)
```

### 8.2 주요 모델 상세

#### User (AbstractUser)
- email (unique), username (unique), profile_image, preferred_wine_types (JSON), bio, created_at, updated_at

#### Wine
- name, type (RED|WHITE|ROSE|SPARKLING|DESSERT), region, country, vintage, grape_varieties (JSON), alcohol_content, average_price, winery, external_id, created_at  
- Index: name, region

#### TastingNote
- user (FK), wine (FK), template (FK, nullable)
- rating (1-5), tasted_date, location (HOME|RESTAURANT|BAR|EVENT|OTHER), location_detail
- color, body, acidity, tannin, sweetness (1-5 each, nullable)
- notes, custom_fields (JSON), photos (JSON, S3 URL 배열), is_public
- created_at, updated_at  
- Ordering: -tasted_date, -created_at  
- Index: (user, -tasted_date), wine

#### Template
- user (FK), name, fields (JSON), is_default, created_at  
- fields 예: pairing(text), occasion(select), price_paid(number)

#### Comment / Like
- TastingNote에 대한 댓글 및 좋아요 (Phase 2)

---

## 9. API 명세

### 9.1 인증
- **POST /api/auth/register** — 회원가입 (email, username, password, password_confirm) → user + tokens
- **POST /api/auth/login** — 로그인 (email, password) → tokens + user

### 9.2 와인
- **GET /api/wines/search** — q, type, region, page, page_size → paginated results
- **GET /api/wines/{id}** — 와인 상세 (tasting_notes_count, average_rating 포함)

### 9.3 시음 노트
- **POST /api/tasting-notes** — multipart (wine_id, rating, tasted_date, location, ... photos)
- **GET /api/tasting-notes** — wine_id, start_date, end_date, rating, ordering, page, page_size
- **GET /api/tasting-notes/{id}**, **PATCH**, **DELETE**

### 9.4 대시보드
- **GET /api/dashboard/stats** — start_date, end_date → total_tastings, monthly_trend, type_distribution, rating_distribution 등
- **GET /api/dashboard/calendar** — year, month → days[] (date, count, notes[])

### 9.5 커뮤니티 (Phase 2)
- **GET /api/community/feed** — 공개 시음 노트 피드
- **POST /api/tasting-notes/{id}/like** — 좋아요
- **POST /api/tasting-notes/{id}/comments** — 댓글 작성 (content)

---

## 10. 개발 로드맵

### Phase 1: MVP (3개월)
- **Month 1:** 프로젝트 셋업(React Native, Django, PostgreSQL, AWS, CI/CD), JWT 인증, 회원가입/로그인/프로필
- **Month 2:** 와인 검색(Wine-Searcher API), 와인 상세, 이미지 업로드(S3, 썸네일), OCR(선택)
- **Month 3:** 시음 노트 CRUD, 기본/커스텀 템플릿, 리치 텍스트, 달력 뷰, 통합 테스트, 베타 준비

### Phase 2: 분석 & 커뮤니티 (2개월)
- **Month 4:** 대시보드 차트, 통계 API, 선호도/평점/가격 분석, CSV 내보내기
- **Month 5:** 공개 피드, 좋아요/댓글, 실시간 알림, 팔로우, 토론 게시판, Elasticsearch 검색

### Phase 3: 출시 (1개월)
- **Month 6:** 성능/이미지/쿼리 최적화, QA, 앱스토어 등록, 소프트 론칭, 피드백 수집

### Post-Launch
- AI 추천, 와인 컬렉션, 페어링 추천, 오프라인 이벤트, 와인샵 제휴, 웹 버전

---

## 11. 성공 지표 (KPI)

| 구분 | 3개월 | 6개월 | 1년 |
|------|-------|-------|-----|
| 가입자 | 500 | 2,000 | 10,000 |
| MAU | 300 | 1,200 | 6,000 |
| DAU | 50 | 200 | 1,000 |
| 평균 시음 기록/사용자 | 3회 | 8회 | 25회 |
| 공개 노트 비율 | 20% | 30% | 40% |

---

## 12. 리스크 및 완화 전략

- **Wine API 불안정:** 자체 DB 구축, 다중 API 백업, 캐싱 강화
- **OCR 저조:** 수동 입력 옵션, 피드백 기반 학습
- **확장성:** 오토스케일링, 인덱싱, Redis 캐싱
- **초기 사용자 부족:** 와인 커뮤니티 마케팅, 인플루언서, 와인바 제휴
- **개인정보:** GDPR/개인정보보호법 준수, 암호화, 정기 감사

---

## 13. 출시 전략

- **베타 (Month 3):** 소믈리에 10명, 애호가 30명, 일반 60명, TestFlight/Play 베타, 주 1회 피드백
- **소프트 론칭 (Month 4):** 강남/이태원 와인바 제휴, 인스타 인플루언서, 네이버 와인 카페
- **공식 출시 (Month 6):** ASO, SNS 광고, 초대/챌린지/리뷰 이벤트
- **Post-Launch:** 친구 초대, 와인 교육 콘텐츠, 오프라인 시음회, B2B 제휴

---

## 14. 부록 및 참조

### 14.1 참고 자료
- Vivino 앱 분석, 한국 와인 시장 보고서, Wine-Searcher API 문서, React Native 성능 가이드

### 14.2 용어 사전
- **바디(Body)**: 와인의 질감/무게감 | **타닌(Tannin)**: 떫은맛 성분 | **산미(Acidity)**: 신맛 정도 | **빈티지(Vintage)**: 포도 수확 연도 | **테루아(Terroir)**: 생산 환경

### 14.3 FAQ
- **비비노와 차별점:** 한국어 네이티브, 커스텀 템플릿, 데이터 대시보드, 한국 커뮤니티
- **무료 여부:** MVP 무료, 프리미엄 기능 유료화 검토
- **오프라인:** Phase 2 예정 | **웹 버전:** Post-Launch 예정

### 14.4 다음 단계
1. GitHub 이슈 생성 (Epic/Feature/Task)
2. 기술 스펙 문서 (API 상세, DB 스키마)
3. Figma 프로토타입
4. 저장소 및 초기 코드 구조

---

## 📝 문서 이력

| 버전 | 날짜 | 작성자 | 변경 내역 |
|------|------|--------|----------|
| 1.0 | 2024-01-15 | grace287 | 초안 작성 (winenote) |
| 1.1 | 2024-02-09 | Copilot | 전체 구조 재설계 및 상세화 |
| 2.0 | 2025-02-09 | WineNowNote | mywine/mywine2/winenote 참조 통합 PRD, WineNowNote 폴더 신규 설계 |
