from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TastingNoteViewSet, TemplateViewSet

router = DefaultRouter()
# 'templates'를 먼저 등록해 /api/tasting-notes/templates/ 가 <pk>에 걸리지 않도록
router.register(r"templates", TemplateViewSet, basename="template")
router.register(r"", TastingNoteViewSet, basename="tasting-note")

urlpatterns = [path("", include(router.urls))]
