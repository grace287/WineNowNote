"""
운영 환경 설정 — base 상속 후 운영용만 오버라이드
"""
import os
from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").strip().split(",")
if not ALLOWED_HOSTS or (len(ALLOWED_HOSTS) == 1 and not ALLOWED_HOSTS[0]):
    raise ValueError("운영 환경에서는 ALLOWED_HOSTS 환경 변수를 설정해야 합니다.")

# CORS: 허용 오리진만 명시
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "").strip().split(",")

# PostgreSQL (환경 변수로 설정)
DATABASES["default"] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ.get("DB_NAME", ""),
    "USER": os.environ.get("DB_USER", ""),
    "PASSWORD": os.environ.get("DB_PASSWORD", ""),
    "HOST": os.environ.get("DB_HOST", "localhost"),
    "PORT": os.environ.get("DB_PORT", "5432"),
    "OPTIONS": {"sslmode": os.environ.get("DB_SSLMODE", "prefer")},
}
