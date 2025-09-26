from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add role and profile_image to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "profile_image")}),
    )

    # Show fields in the list view
    list_display = ("username", "email", "role", "is_staff", "is_active", "profile_image")
