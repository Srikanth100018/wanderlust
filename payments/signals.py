from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def update_booking_payment_status(sender, instance, created, **kwargs):
    """
    Whenever a Payment is updated to 'paid', mark the related booking as paid.
    """
    if instance.status == "paid" and instance.booking:
        booking = instance.booking
        if not booking.is_paid:  # prevent redundant saves
            booking.is_paid = True
            booking.save()
