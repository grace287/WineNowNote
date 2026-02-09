"""
와인 API (PRD 9.2)
- GET /api/wines/search?q=&type=&region=&page=&page_size=
- GET /api/wines/{id}
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Q, Count, Avg
from .models import Wine
from .serializers import WineListSerializer, WineDetailSerializer


class WineViewSet(viewsets.ReadOnlyModelViewSet):
    """와인 검색·상세 (쓰기는 admin 또는 시음노트 작성 시 생성)"""
    queryset = Wine.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WineDetailSerializer
        return WineListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q", "").strip()
        wine_type = self.request.query_params.get("type", "").strip().upper()
        region = self.request.query_params.get("region", "").strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(winery__icontains=q)
                | Q(region__icontains=q)
                | Q(country__icontains=q)
            )
        if wine_type and wine_type in dict(Wine.WINE_TYPES):
            qs = qs.filter(type=wine_type)
        if region:
            qs = qs.filter(region__icontains=region)
        return qs

    def retrieve(self, request, *args, **kwargs):
        """상세 시 tasting_notes_count, average_rating 포함"""
        instance = self.get_object()
        from apps.notes.models import TastingNote

        agg = TastingNote.objects.filter(wine=instance).aggregate(
            count=Count("id"),
            avg_rating=Avg("rating"),
        )
        serializer = WineDetailSerializer(instance)
        data = serializer.data
        data["tasting_notes_count"] = agg["count"] or 0
        data["average_rating"] = (
            round(float(agg["avg_rating"]), 2) if agg["avg_rating"] is not None else None
        )
        from rest_framework.response import Response

        return Response(data)
