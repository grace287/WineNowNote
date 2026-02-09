"""
대시보드 API (PRD 9.4)
- GET /api/dashboard/stats?start_date=&end_date=
- GET /api/dashboard/calendar?year=&month=
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from notes.models import TastingNote


class StatsView(APIView):
    """GET /api/dashboard/stats — 전체 통계"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        start = request.query_params.get("start_date")
        end = request.query_params.get("end_date")
        qs = TastingNote.objects.filter(user=user)
        if start:
            qs = qs.filter(tasted_date__gte=start)
        if end:
            qs = qs.filter(tasted_date__lte=end)

        total_tastings = qs.count()
        total_wines = qs.values("wine").distinct().count()
        avg_rating = qs.aggregate(Avg("rating"))["rating__avg"]
        avg_rating = round(float(avg_rating), 2) if avg_rating else None

        type_dist = dict(
            qs.values("wine__type").annotate(c=Count("id")).values_list("wine__type", "c")
        )
        rating_dist = dict(
            qs.values("rating").annotate(c=Count("id")).values_list("rating", "c")
        )

        # 월별 트렌드 (최근 12개월)
        if not end:
            end = timezone.now().date()
        if not start:
            start = end - timedelta(days=365)
        monthly = (
            TastingNote.objects.filter(user=user, tasted_date__gte=start, tasted_date__lte=end)
            .annotate(month=TruncMonth("tasted_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        monthly_trend = [{"month": str(m["month"])[:7], "count": m["count"]} for m in monthly]

        most_type = (
            qs.values("wine__type")
            .annotate(c=Count("id"))
            .order_by("-c")
            .first()
        )
        most_region = (
            qs.values("wine__region")
            .annotate(c=Count("id"))
            .order_by("-c")
            .exclude(wine__region="")
            .first()
        )

        return Response(
            {
                "total_tastings": total_tastings,
                "total_wines": total_wines,
                "average_rating": avg_rating,
                "most_tasted_type": most_type["wine__type"] if most_type else None,
                "most_tasted_region": most_region["wine__region"] if most_region else None,
                "monthly_trend": monthly_trend,
                "type_distribution": type_dist,
                "rating_distribution": rating_dist,
            }
        )


class CalendarView(APIView):
    """GET /api/dashboard/calendar?year=&month= — 달력 데이터"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        year = int(request.query_params.get("year", timezone.now().year))
        month = int(request.query_params.get("month", timezone.now().month))
        qs = (
            TastingNote.objects.filter(
                user=request.user,
                tasted_date__year=year,
                tasted_date__month=month,
            )
            .select_related("wine")
            .order_by("tasted_date")
        )
        from collections import defaultdict

        by_date = defaultdict(list)
        for note in qs:
            by_date[str(note.tasted_date)].append(
                {
                    "id": note.id,
                    "wine_name": note.wine.name,
                    "rating": note.rating,
                    "photo": note.photos[0] if note.photos else None,
                }
            )
        days = [
            {"date": date, "count": len(notes), "notes": notes}
            for date, notes in sorted(by_date.items())
        ]
        return Response({"year": year, "month": month, "days": days})
