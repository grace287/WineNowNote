"""
환경에 따라 development / production 설정 로드.
사용: DJANGO_ENV=production 또는 미설정(개발)
"""
import os

_env = os.environ.get("DJANGO_ENV", "development").lower()
if _env == "production":
    from .production import *  # noqa: F401, F403
else:
    from .development import *  # noqa: F401, F403
