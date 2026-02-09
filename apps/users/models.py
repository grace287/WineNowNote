"""
사용자 모델 (PRD 8.2.1)
- email unique, username unique, profile_image, preferred_wine_types(JSON), bio
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """사용자 모델 — PRD User"""
    email = models.EmailField("이메일", unique=True)
    username = models.CharField("닉네임", max_length=50, unique=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True,
        verbose_name="프로필 이미지",
    )
    preferred_wine_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name="선호 와인 종류",
        help_text="예: ['RED', 'WHITE']",
    )
    bio = models.TextField("소개", max_length=500, blank=True)
    created_at = models.DateTimeField("가입일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def __str__(self):
        return self.username
