from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("create-payment-order/<int:booking_id>/", views.create_payment_order, name="create_payment_order"),
    path("webhook/", views.razorpay_webhook, name="razorpay_webhook"),
    path("success/<int:booking_id>/", views.payment_success, name="payment_success"),
    path("cancel/<int:booking_id>/", views.payment_cancel, name="payment_cancel"),
]
