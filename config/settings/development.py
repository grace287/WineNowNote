"""
개발 환경 설정 — base 상속 후 개발용만 오버라이드
"""
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# 개발 시 프론트 연동용 CORS
CORS_ALLOW_ALL_ORIGINS = True
