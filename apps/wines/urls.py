from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WineViewSet

router = DefaultRouter()
router.register(r"", WineViewSet, basename="wine")
urlpatterns = [path("", include(router.urls))]
