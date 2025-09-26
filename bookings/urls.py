from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("<int:pk>/", views.booking_detail, name="booking_detail"),
    path("new/", views.booking_create, name="booking_create"),
    path("notifications/", views.notifications_list, name="notifications"),
]