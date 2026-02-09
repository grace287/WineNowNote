"""
시음 노트 API (PRD 9.3)
- GET/POST /api/tasting-notes/
- GET/PATCH/DELETE /api/tasting-notes/{id}
- 필터: wine, rating, tasted_date, location, is_public / 검색: notes, aroma_notes, pairing, wine__name
- 커스텀 액션: my_notes, calendar, statistics, upload_photo, delete_photo
"""
from datetime import timedelta
import uuid

from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.core.files.storage import default_storage
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Template, TastingNote
from .serializers import (
    TemplateSerializer,
    TastingNoteListSerializer,
    TastingNoteDetailSerializer,
    TastingNoteCreateUpdateSerializer,
    TastingNotePhotoUploadSerializer,
    TastingNoteStatisticsSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """본인 소유만 수정/삭제 허용. 조회는 본인 + 공개 노트."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "user", None) == request.user


class TemplateViewSet(viewsets.ModelViewSet):
    """
    템플릿 CRUD API (본인 것만).
    list / retrieve / create / update / destroy
    액션: set_default (POST) — 기본 템플릿 지정
    """

    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def set_default(self, request, pk=None):
        """이 템플릿을 기본 템플릿으로 설정"""
        template = self.get_object()
        Template.objects.filter(user=request.user, is_default=True).update(
            is_default=False
        )
        template.is_default = True
        template.save(update_fields=["is_default"])
        return Response(
            {"message": f'"{template.name}"을(를) 기본 템플릿으로 설정했습니다.'}
        )


class TastingNoteViewSet(viewsets.ModelViewSet):
    """
    시음 노트 CRUD API.
    list: 내 노트 + 공개 노트 / retrieve / create / update / destroy
    액션: my_notes, calendar, statistics, upload_photo, delete_photo
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "wine": ["exact"],
        "rating": ["exact", "gte", "lte"],
        "tasted_date": ["exact", "gte", "lte"],
        "location": ["exact"],
        "is_public": ["exact"],
    }
    search_fields = ["notes", "aroma_notes", "pairing", "wine__name"]
    ordering_fields = ["tasted_date", "rating", "created_at"]
    ordering = ["-tasted_date", "-created_at"]
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        user = self.request.user
        return (
            TastingNote.objects.filter(Q(user=user) | Q(is_public=True))
            .select_related("user", "wine", "template")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == "list":
            return TastingNoteListSerializer
        if self.action in ("create", "update", "partial_update"):
            return TastingNoteCreateUpdateSerializer
        return TastingNoteDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=["get"])
    def my_notes(self, request):
        """내 시음 노트만 (공개 노트 제외)"""
        qs = TastingNote.objects.filter(user=request.user).select_related("wine")
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                TastingNoteListSerializer(page, many=True).data
            )
        return Response(TastingNoteListSerializer(qs, many=True).data)

    @action(detail=False, methods=["get"])
    def calendar(self, request):
        """
        달력용 데이터. query: year, month (기본값: 현재 연·월)
        응답: year, month, days = [{ date, count, notes }] (날짜 오름차순)
        """
        year = int(request.query_params.get("year", timezone.now().year))
        month = int(request.query_params.get("month", timezone.now().month))
        qs = TastingNote.objects.filter(
            user=request.user,
            tasted_date__year=year,
            tasted_date__month=month,
        ).select_related("wine")

        by_date = {}
        for note in qs:
            date_str = note.tasted_date.strftime("%Y-%m-%d")
            if date_str not in by_date:
                by_date[date_str] = []
            by_date[date_str].append(
                {
                    "id": note.id,
                    "wine_name": note.wine.name,
                    "rating": note.rating,
                    "photo": (note.photos[0] if note.photos else None),
                }
            )

        days = [
            {"date": d, "count": len(items), "notes": items}
            for d, items in sorted(by_date.items())
        ]
        return Response({"year": year, "month": month, "days": days})

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """
        내 시음 통계. query: start_date, end_date (선택)
        """
        qs = TastingNote.objects.filter(user=request.user)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date:
            qs = qs.filter(tasted_date__gte=start_date)
        if end_date:
            qs = qs.filter(tasted_date__lte=end_date)

        total_notes = qs.count()
        avg_result = qs.aggregate(Avg("rating"))
        average_rating = avg_result["rating__avg"]
        if average_rating is not None:
            average_rating = round(float(average_rating), 2)

        type_row = (
            qs.values("wine__type")
            .annotate(count=Count("id"))
            .order_by("-count")
            .first()
        )
        favorite_wine_type = type_row["wine__type"] if type_row else ""
        region_row = (
            qs.values("wine__region")
            .annotate(count=Count("id"))
            .order_by("-count")
            .first()
        )
        favorite_region = (region_row["wine__region"] or "") if region_row else ""

        six_months_ago = timezone.now().date() - timedelta(days=180)
        monthly_qs = (
            qs.filter(tasted_date__gte=six_months_ago)
            .annotate(month=TruncMonth("tasted_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        monthly_count = {
            str(row["month"])[:7]: row["count"] for row in monthly_qs
        }

        rating_distribution = {
            str(i): qs.filter(rating=i).count() for i in range(1, 6)
        }

        data = {
            "total_notes": total_notes,
            "average_rating": average_rating,
            "favorite_wine_type": favorite_wine_type,
            "favorite_region": favorite_region,
            "monthly_count": monthly_count,
            "rating_distribution": rating_distribution,
        }
        serializer = TastingNoteStatisticsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def upload_photo(self, request, pk=None):
        """시음 노트에 사진 1장 추가. Body: multipart/form-data, photo=파일"""
        note = self.get_object()
        ser = TastingNotePhotoUploadSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        photo_file = ser.validated_data["photo"]

        ext = (photo_file.name or "").split(".")[-1] or "jpg"
        filename = f"tasting_notes/{request.user.pk}/{uuid.uuid4().hex}.{ext}"
        path = default_storage.save(filename, photo_file)
        url = default_storage.url(path)

        if not note.photos:
            note.photos = []
        note.photos.append(url)
        note.save(update_fields=["photos"])

        return Response(
            {"message": "사진이 업로드되었습니다.", "url": url, "photos": note.photos},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["delete"])
    def delete_photo(self, request, pk=None):
        """시음 노트에서 사진 제거. query: url=삭제할 URL"""
        note = self.get_object()
        photo_url = request.query_params.get("url")
        if not photo_url:
            return Response(
                {"error": "url 파라미터가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if photo_url in note.photos:
            note.photos = [u for u in note.photos if u != photo_url]
            note.save(update_fields=["photos"])
            return Response({"message": "사진이 삭제되었습니다."})
        return Response(
            {"error": "해당 사진을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )
