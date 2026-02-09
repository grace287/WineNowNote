from django.contrib import admin
from .models import Template, TastingNote


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_default", "created_at")
    list_filter = ("is_default",)


@admin.register(TastingNote)
class TastingNoteAdmin(admin.ModelAdmin):
    list_display = ("wine", "user", "rating", "tasted_date", "location", "is_public", "created_at")
    list_filter = ("location", "is_public", "rating")
    search_fields = ("wine__name", "notes")
    raw_id_fields = ("user", "wine", "template")
