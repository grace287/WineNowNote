from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_staff", "created_at")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("-created_at",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("추가 정보", {"fields": ("profile_image", "preferred_wine_types", "bio")}),
    )
