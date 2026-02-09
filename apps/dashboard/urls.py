from django.urls import path
from .views import StatsView, CalendarView

urlpatterns = [
    path("stats/", StatsView.as_view(), name="dashboard-stats"),
    path("calendar/", CalendarView.as_view(), name="dashboard-calendar"),
]
