"""
시음 노트 API (PRD 9.3)
- GET/POST /api/tasting-notes/
- GET/PATCH/DELETE /api/tasting-notes/{id}
- Query: wine_id, start_date, end_date, rating, ordering
"""
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.utils import timezone
from .models import TastingNote, Template
from .serializers import (
    TastingNoteListSerializer,
    TastingNoteDetailSerializer,
    TastingNoteCreateUpdateSerializer,
    TemplateSerializer,
)


class TastingNoteViewSet(viewsets.ModelViewSet):
    serializer_class = TastingNoteListSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        qs = TastingNote.objects.filter(user=self.request.user).select_related(
            "wine", "template"
        )
        wine_id = self.request.query_params.get("wine_id")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        rating = self.request.query_params.get("rating")
        ordering = self.request.query_params.get("ordering", "-tasted_date")
        if wine_id:
            qs = qs.filter(wine_id=int(wine_id))
        if start_date:
            qs = qs.filter(tasted_date__gte=start_date)
        if end_date:
            qs = qs.filter(tasted_date__lte=end_date)
        if rating:
            qs = qs.filter(rating=int(rating))
        if ordering.lstrip("-") in ("tasted_date", "rating", "created_at"):
            qs = qs.order_by(ordering)
        return qs

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TastingNoteCreateUpdateSerializer
        if self.action == "retrieve":
            return TastingNoteDetailSerializer
        return TastingNoteListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TemplateViewSet(viewsets.ModelViewSet):
    """시음 노트 템플릿 CRUD (본인 것만)"""
    serializer_class = TemplateSerializer

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
