"""
시음 노트·템플릿 API 시리얼라이저 (PRD 8.2.3, 8.2.4)
- Template: CRUD, fields JSON 검증
- TastingNote: 목록/상세/생성·수정, wines.Wine 중첩, choices display 필드
"""
from rest_framework import serializers
from apps.wines.serializers import WineListSerializer
from .models import Template, TastingNote


class TemplateSerializer(serializers.ModelSerializer):
    """템플릿 CRUD. fields는 {'fields': [{name, type, label}, ...]} 구조."""

    class Meta:
        model = Template
        fields = [
            "id",
            "name",
            "fields",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_fields(self, value):
        """필드 JSON 구조 검증: 'fields' 키와 리스트, 각 항목에 name/type/label 필요."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("fields는 딕셔너리 형식이어야 합니다.")
        if "fields" not in value:
            raise serializers.ValidationError("'fields' 키가 필요합니다.")
        if not isinstance(value["fields"], list):
            raise serializers.ValidationError("'fields'는 리스트여야 합니다.")
        required_keys = ["name", "type", "label"]
        for field in value["fields"]:
            if not isinstance(field, dict):
                raise serializers.ValidationError("각 필드는 딕셔너리여야 합니다.")
            if not all(k in field for k in required_keys):
                raise serializers.ValidationError(
                    f"각 필드에는 {required_keys}가 필요합니다."
                )
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TastingNoteListSerializer(serializers.ModelSerializer):
    """시음 노트 목록용 — 와인 중첩, 사용자명·장소 한글 표기."""

    wine = WineListSerializer(read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    location_display = serializers.CharField(
        source="get_location_display", read_only=True
    )

    class Meta:
        model = TastingNote
        fields = [
            "id",
            "user_username",
            "wine",
            "rating",
            "tasted_date",
            "location",
            "location_display",
            "pairing",
            "photos",
            "is_public",
            "created_at",
        ]


class TastingNoteDetailSerializer(serializers.ModelSerializer):
    """시음 노트 상세 — 와인·템플릿 중첩, 외관/아로마/맛·choices 한글 표기."""

    wine = WineListSerializer(read_only=True)
    template_name = serializers.CharField(source="template.name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    location_display = serializers.CharField(
        source="get_location_display", read_only=True
    )
    appearance_clarity_display = serializers.CharField(
        source="get_appearance_clarity_display", read_only=True
    )

    class Meta:
        model = TastingNote
        fields = [
            "id",
            "user_username",
            "wine",
            "template",
            "template_name",
            "rating",
            "tasted_date",
            "location",
            "location_display",
            "location_detail",
            "appearance_clarity",
            "appearance_clarity_display",
            "appearance_intensity",
            "color",
            "aroma_intensity",
            "aroma_notes",
            "body",
            "acidity",
            "tannin",
            "sweetness",
            "pairing",
            "notes",
            "custom_fields",
            "photos",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class TastingNoteCreateUpdateSerializer(serializers.ModelSerializer):
    """시음 노트 생성·수정. wine/template 검증, 생성 시 user는 request에서 설정."""

    class Meta:
        model = TastingNote
        fields = [
            "wine",
            "template",
            "rating",
            "tasted_date",
            "location",
            "location_detail",
            "appearance_clarity",
            "appearance_intensity",
            "color",
            "aroma_intensity",
            "aroma_notes",
            "body",
            "acidity",
            "tannin",
            "sweetness",
            "pairing",
            "notes",
            "custom_fields",
            "photos",
            "is_public",
        ]

    def validate_wine(self, value):
        from apps.wines.models import Wine

        if not Wine.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("존재하지 않는 와인입니다.")
        return value

    def validate_template(self, value):
        if value is None:
            return value
        if value.user_id != self.context["request"].user.pk:
            raise serializers.ValidationError("본인의 템플릿만 사용할 수 있습니다.")
        return value

    def validate_photos(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("photos는 리스트여야 합니다.")
        if len(value) > 5:
            raise serializers.ValidationError("최대 5장까지 등록 가능합니다.")
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TastingNotePhotoUploadSerializer(serializers.Serializer):
    """사진 업로드 요청용 — 단일 이미지, 크기·형식 검증."""

    photo = serializers.ImageField(required=True)

    def validate_photo(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("파일 크기는 5MB를 초과할 수 없습니다.")
        allowed = ("image/jpeg", "image/png", "image/jpg")
        if value.content_type not in allowed:
            raise serializers.ValidationError("JPEG 또는 PNG 형식만 업로드 가능합니다.")
        return value


class TastingNoteStatisticsSerializer(serializers.Serializer):
    """시음 노트 통계 API 응답용 (읽기 전용)."""

    total_notes = serializers.IntegerField()
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, allow_null=True
    )
    favorite_wine_type = serializers.CharField(allow_blank=True)
    favorite_region = serializers.CharField(allow_blank=True)
    monthly_count = serializers.DictField()
    rating_distribution = serializers.DictField()
