"""
대시보드 API (PRD 9.4)
- GET /api/dashboard/stats/ — 전체 통계 (start_date, end_date)
- GET /api/dashboard/calendar/ — 달력 (year, month)
- GET /api/dashboard/top-wines/ — Top 10 와인 (sort=count|rating)
"""
from collections import defaultdict
from datetime import timedelta

from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notes.models import TastingNote
from apps.wines.models import Wine


class StatsView(APIView):
    """
    대시보드 전체 통계.
    GET /api/dashboard/stats/
    Query: start_date, end_date (선택)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        qs = TastingNote.objects.filter(user=user)
        if start_date:
            qs = qs.filter(tasted_date__gte=start_date)
        if end_date:
            qs = qs.filter(tasted_date__lte=end_date)

        total_tastings = qs.count()
        total_wines = qs.values("wine").distinct().count()
        avg_result = qs.aggregate(Avg("rating"))["rating__avg"]
        average_rating = round(float(avg_result), 2) if avg_result is not None else None

        type_stats = (
            qs.values("wine__type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        type_distribution = {row["wine__type"]: row["count"] for row in type_stats}
        most_tasted_type = (
            type_stats.first()["wine__type"] if type_stats else None
        )

        region_stats = (
            qs.values("wine__region")
            .annotate(count=Count("id"))
            .exclude(wine__region="")
            .order_by("-count")
        )
        most_tasted_region = (
            region_stats.first()["wine__region"] if region_stats else None
        )

        twelve_months_ago = timezone.now().date() - timedelta(days=365)
        monthly_qs = (
            qs.filter(tasted_date__gte=twelve_months_ago)
            .annotate(month=TruncMonth("tasted_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        monthly_trend = [
            {"month": str(row["month"])[:7], "count": row["count"]}
            for row in monthly_qs
        ]

        rating_distribution = {
            str(i): qs.filter(rating=i).count() for i in range(1, 6)
        }

        return Response(
            {
                "total_tastings": total_tastings,
                "total_wines": total_wines,
                "average_rating": average_rating,
                "most_tasted_type": most_tasted_type,
                "most_tasted_region": most_tasted_region,
                "monthly_trend": monthly_trend,
                "type_distribution": type_distribution,
                "rating_distribution": rating_distribution,
            }
        )


class CalendarView(APIView):
    """
    달력용 데이터.
    GET /api/dashboard/calendar/?year=&month=
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        year = int(request.query_params.get("year", timezone.now().year))
        month = int(request.query_params.get("month", timezone.now().month))

        qs = (
            TastingNote.objects.filter(
                user=user,
                tasted_date__year=year,
                tasted_date__month=month,
            )
            .select_related("wine")
            .order_by("tasted_date")
        )

        by_date = defaultdict(list)
        for note in qs:
            date_str = note.tasted_date.strftime("%Y-%m-%d")
            by_date[date_str].append(
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


class TopWinesView(APIView):
    """
    내가 가장 많이/높게 평가한 와인 Top 10.
    GET /api/dashboard/top-wines/?sort=count (기본) | sort=rating
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        sort_by = request.query_params.get("sort", "count")

        notes_qs = TastingNote.objects.filter(user=user)

        if sort_by == "rating":
            top_rows = (
                notes_qs.values("wine")
                .annotate(
                    avg_rating=Avg("rating"),
                    count=Count("id"),
                )
                .filter(count__gte=1)
                .order_by("-avg_rating", "-count")[:10]
            )
        else:
            top_rows = (
                notes_qs.values("wine")
                .annotate(
                    count=Count("id"),
                    avg_rating=Avg("rating"),
                )
                .order_by("-count", "-avg_rating")[:10]
            )

        wine_ids = [row["wine"] for row in top_rows]
        wines = {w.id: w for w in Wine.objects.filter(pk__in=wine_ids)}

        results = []
        for row in top_rows:
            wine = wines.get(row["wine"])
            if not wine:
                continue
            results.append(
                {
                    "wine": {
                        "id": wine.id,
                        "name": wine.name,
                        "type": wine.type,
                        "region": wine.region or "",
                        "country": wine.country or "",
                        "vintage": wine.vintage,
                        "winery": wine.winery or "",
                    },
                    "count": row.get("count", 0),
                    "avg_rating": round(float(row.get("avg_rating") or 0), 2),
                }
            )
        return Response(results)
