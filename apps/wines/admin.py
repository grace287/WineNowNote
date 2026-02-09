from django.contrib import admin
from .models import Wine


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "country", "region", "vintage", "winery")
    list_filter = ("type", "country")
    search_fields = ("name", "winery", "region")
    ordering = ("name",)
