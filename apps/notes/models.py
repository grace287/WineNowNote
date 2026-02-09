"""
시음 노트·템플릿 모델 (PRD 8.2.3, 8.2.4)
- wines.Wine 참조: 시음 노트는 와인 FK로 연결, 외관/아로마/맛 스케일 정리
- TastingNote: user, wine, template, rating, tasted_date, location, 시각/아로마/맛, notes, custom_fields, photos, is_public
- Template: user, name, fields(JSON), is_default
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# 1~5 스케일 공통 (와인 시음 — 바디/산도/탄닌/당도, mywine 참조)
TASTING_SCALE_1_5 = [
    (1, "매우 낮음"),
    (2, "낮음"),
    (3, "중간"),
    (4, "높음"),
    (5, "매우 높음"),
]

# 투명도 (mywine2, winenote 참조)
APPEARANCE_CLARITY_CHOICES = [
    ("clear", "맑음"),
    ("hazy", "흐림"),
    ("cloudy", "탁함"),
]


class Template(models.Model):
    """시음 노트 템플릿 — 커스텀 필드 정의 (PRD NOTE-002). wines.Wine 필드와 조합해 사용."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="templates",
    )
    name = models.CharField("템플릿명", max_length=100)
    fields = models.JSONField(
        "필드 정의",
        default=dict,
        help_text=(
            "커스텀 필드 목록. 예: "
            '{"fields": ['
            '{"name": "pairing", "type": "text", "label": "페어링 음식"}, '
            '{"name": "appearance_notes", "type": "text", "label": "외관 메모"}, '
            '{"name": "aroma_tags", "type": "tags", "label": "아로마 태그"}]}'
        ),
    )
    is_default = models.BooleanField("기본 사용", default=False)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        db_table = "templates"
        verbose_name = "시음 노트 템플릿"
        verbose_name_plural = "시음 노트 템플릿"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name


class TastingNote(models.Model):
    """시음 노트 (PRD 8.2.3). wines.Wine FK로 와인 정보 참조, 시음 당시 평가만 저장."""

    LOCATION_CHOICES = [
        ("home", "집"),
        ("restaurant", "레스토랑"),
        ("bar", "바"),
        ("event", "이벤트"),
        ("other", "기타"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasting_notes",
    )
    wine = models.ForeignKey(
        "wines.Wine",
        on_delete=models.CASCADE,
        related_name="tasting_notes",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasting_notes",
    )

    rating = models.IntegerField(
        "평점",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    tasted_date = models.DateField("시음일")
    location = models.CharField(
        "장소 유형",
        max_length=20,
        choices=LOCATION_CHOICES,
        default="other",
    )
    location_detail = models.CharField("장소 상세", max_length=200, blank=True)

    # 외관 (wines 타입·색 개념과 구분 — 시음 당시 관찰)
    appearance_clarity = models.CharField(
        "투명도",
        max_length=20,
        choices=APPEARANCE_CLARITY_CHOICES,
        blank=True,
    )
    appearance_intensity = models.IntegerField(
        "색 강도",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    color = models.CharField("색상 설명", max_length=50, blank=True)

    # 아로마 (mywine2, winenote, mywine 참조)
    aroma_intensity = models.IntegerField(
        "향 강도",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    aroma_notes = models.TextField("아로마 노트", blank=True)

    # 맛 (1~5 스케일, wines와 동일한 축)
    body = models.IntegerField(
        "바디",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    acidity = models.IntegerField(
        "산도",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    tannin = models.IntegerField(
        "타닌",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    sweetness = models.IntegerField(
        "당도",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    pairing = models.CharField("페어링 음식", max_length=200, blank=True)
    notes = models.TextField("메모", blank=True)
    custom_fields = models.JSONField("커스텀 필드 값", default=dict, blank=True)
    photos = models.JSONField(
        "사진 URL 목록",
        default=list,
        blank=True,
        help_text="S3 등 URL 리스트. 로컬 개발 시 미디어 경로",
    )
    is_public = models.BooleanField("공개 여부", default=False)

    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        db_table = "tasting_notes"
        ordering = ["-tasted_date", "-created_at"]
        verbose_name = "시음 노트"
        verbose_name_plural = "시음 노트"
        indexes = [
            models.Index(fields=["user", "-tasted_date"]),
            models.Index(fields=["wine"]),
            models.Index(fields=["is_public"]),
        ]

    def __str__(self):
        return f"{self.wine.name} — {self.tasted_date}"

    @property
    def wine_display(self):
        """와인 표기 문자열 (wines.Wine.__str__와 동일)"""
        return str(self.wine)
