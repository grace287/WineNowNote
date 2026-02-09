"""
와인 정보 모델 (PRD 8.2.2)
- mywine2 / winenote / mywine notes·와인 모델 참조하여 정리
- name, type, region, country, vintage, grape_varieties(JSON), alcohol_content, average_price, winery, external_id
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# 와인 종류 (mywine2, winenote, mywine 통합)
WINE_TYPES = [
    ("red", "레드"),
    ("white", "화이트"),
    ("rose", "로제"),
    ("sparkling", "스파클링"),
    ("champagne", "샴페인"),
    ("dessert", "디저트 와인"),
    ("fortified", "주정강화"),
    ("orange", "오렌지 와인"),
    ("natural", "내추럴 와인"),
    ("other", "기타"),
]

# 주요 생산국 (mywine2, mywine 참조 — UI/폼 choices용)
WINE_COUNTRY_CHOICES = [
    ("France", "프랑스"),
    ("Italy", "이탈리아"),
    ("USA", "미국"),
    ("Spain", "스페인"),
    ("Argentina", "아르헨티나"),
    ("Australia", "호주"),
    ("Chile", "칠레"),
    ("South Africa", "남아프리카"),
    ("Germany", "독일"),
    ("Portugal", "포르투갈"),
    ("New Zealand", "뉴질랜드"),
    ("Austria", "오스트리아"),
    ("Hungary", "헝가리"),
    ("Greece", "그리스"),
    ("Canada", "캐나다"),
    ("Japan", "일본"),
    ("South Korea", "대한민국"),
    ("Brazil", "브라질"),
    ("China", "중국"),
    ("Switzerland", "스위스"),
    ("Other", "기타"),
]


class Wine(models.Model):
    """와인 마스터 — 시음 노트에서 FK로 참조"""

    name = models.CharField("와인명", max_length=200)
    type = models.CharField(
        "종류",
        max_length=20,
        choices=WINE_TYPES,
        default="other",
    )
    region = models.CharField("산지(지역)", max_length=100, blank=True)
    country = models.CharField(
        "국가",
        max_length=100,
        blank=True,
        help_text="WINE_COUNTRY_CHOICES 또는 자유 입력",
    )
    vintage = models.IntegerField(
        "빈티지",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 1),
        ],
    )
    grape_varieties = models.JSONField(
        "품종",
        default=list,
        blank=True,
        help_text="예: ['Cabernet Sauvignon', 'Merlot']",
    )
    alcohol_content = models.DecimalField(
        "도수",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )
    average_price = models.DecimalField(
        "평균 가격",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    winery = models.CharField("와이너리", max_length=200, blank=True)
    external_id = models.CharField(
        "외부 API ID (Wine-Searcher 등)",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("등록일", auto_now_add=True)

    class Meta:
        db_table = "wines"
        verbose_name = "와인"
        verbose_name_plural = "와인"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["winery"]),
            models.Index(fields=["type"]),
            models.Index(fields=["region"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        if self.vintage:
            return f"{self.name} ({self.vintage})"
        return self.name

    def get_grape_varieties_display(self):
        """품종 리스트를 문자열로 반환 (mywine 참조)"""
        if not self.grape_varieties:
            return ""
        return ", ".join(str(g) for g in self.grape_varieties)
