from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "check_in", "check_out", "total_price", "is_paid", "booked_at")
    list_filter = ("is_paid", "booked_at")
    search_fields = ("listing__title", "user__username")
    readonly_fields = ("booked_at",)
    ordering = ("-booked_at",)
    

