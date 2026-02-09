from django.urls import path

from .views import CalendarView, StatsView, TopWinesView

urlpatterns = [
    path("stats/", StatsView.as_view(), name="dashboard-stats"),
    path("calendar/", CalendarView.as_view(), name="dashboard-calendar"),
    path("top-wines/", TopWinesView.as_view(), name="dashboard-top-wines"),
]
