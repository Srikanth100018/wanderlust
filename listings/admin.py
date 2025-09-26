from django.contrib import admin
from .models import AppSettings, Listing, Review


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ("gst_rate", "service_charge", "updated_at")
    readonly_fields = ("updated_at",)
    ordering = ("-updated_at",)

    # optional: allow only 1 settings row (singleton style)
    def has_add_permission(self, request):
        if AppSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "price", "price_with_tax", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "location", "owner__username")
    readonly_fields = ("created_at", "price_with_tax")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("listing__title", "user__username", "comment")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
