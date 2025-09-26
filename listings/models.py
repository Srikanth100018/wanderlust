from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class AppSettings(models.Model):
    gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("18.00"),
        validators=[MinValueValidator(0)]
    )
    service_charge = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)]
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GST: {self.gst_rate}% | Service: {self.service_charge}%"


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("Trending", "Trending"),
        ("Rooms", "Rooms"),
        ("Iconic Cities", "Iconic Cities"),
        ("Hot Beaches", "Hot Beaches"),
        ("Mountains", "Mountains"),
        ("Castles", "Castles"),
        ("Pools", "Pools"),
        ("Islands", "Islands"),
        ("Camping", "Camping"),
        ("Farms", "Farms"),
        ("Arctic", "Arctic"),
        ("Ships", "Ships"),
        ("Domes", "Domes"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image_filename = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Extracted filename (auto-filled from upload or URL)"
    )

    image_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Enter full URL (https://...) or relative static path (e.g. images/Maldives.jpg)"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Trending"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    geometry_type = models.CharField(
        max_length=20,
        choices=[("Point", "Point")],
        default="Point"
    )
    geometry_coordinates = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image_url:
            if self.image_url.startswith("http"):
                return self.image_url
            return f"/static/{self.image_url}"
        return None

    @property
    def price_with_tax(self):
        from .models import AppSettings  # local import to avoid circular issues
        settings = AppSettings.objects.first()
        gst = settings.gst_rate if settings else Decimal("18.00")
        tax_multiplier = (gst / 100) + 1
        return self.price * tax_multiplier

class Review(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.listing.title}"
