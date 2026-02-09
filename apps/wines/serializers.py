from rest_framework import serializers
from .models import Wine


class WineListSerializer(serializers.ModelSerializer):
    """검색/목록용 (PRD 9.2)"""

    class Meta:
        model = Wine
        fields = (
            "id",
            "name",
            "type",
            "region",
            "country",
            "vintage",
            "grape_varieties",
            "alcohol_content",
            "average_price",
            "winery",
        )


class WineDetailSerializer(serializers.ModelSerializer):
    """상세용 — tasting_notes_count, average_rating는 ViewSet에서 주입"""

    tasting_notes_count = serializers.IntegerField(read_only=True, default=0)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True, default=None
    )

    class Meta:
        model = Wine
        fields = (
            "id",
            "name",
            "type",
            "region",
            "country",
            "vintage",
            "grape_varieties",
            "alcohol_content",
            "average_price",
            "winery",
            "external_id",
            "tasting_notes_count",
            "average_rating",
            "created_at",
        )
