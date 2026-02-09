"""
WineNowNote URL Configuration (PRD Section 9)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),
    path("calendar/", TemplateView.as_view(template_name="calendar.html"), name="calendar"),
    path("notes/add/", TemplateView.as_view(template_name="tasting_note_form.html"), name="tasting_note_add"),
    path("admin/", admin.site.urls),
    # API
    path("api/auth/", include("apps.users.urls")),
    path("api/wines/", include("apps.wines.urls")),
    path("api/tasting-notes/", include("apps.notes.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    # OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
