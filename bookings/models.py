from django.db import models
from decimal import Decimal
from django.conf import settings
from listings.models import Listing
from django.core.validators import MinValueValidator# your listings app

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.TextField()
    booked_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}: {self.message[:30]}..."

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        blank=True,
        null=True
    )
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} → {self.listing.title}"

    def save(self, *args, **kwargs):
        if self.total_price is None and self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            if nights > 0:
                self.total_price = self.listing.price_with_tax * Decimal(nights)
        super().save(*args, **kwargs)

    @property
    def nights(self):
        """Number of nights for the booking."""
        return (self.check_out - self.check_in).days


    @property
    def total_bill(self):
        """Compute total price dynamically in case total_price is None."""
        if self.total_price is not None:
            return self.total_price
        nights = (self.check_out - self.check_in).days
        return self.listing.price_with_tax * Decimal(nights) if nights > 0 else Decimal("0.00")
