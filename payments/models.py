from django.db import models
from django.conf import settings
from listings.models import Listing
from bookings.models import Booking

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField(help_text="Amount in paise")
    currency = models.CharField(max_length=10, default="inr")
    status = models.CharField(max_length=20, default="pending")  # pending, paid, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user} - {self.status}"
