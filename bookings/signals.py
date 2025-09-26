from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking, Notification


@receiver(post_save, sender=Booking)
def notify_host_on_booking(sender, instance, created, **kwargs):
    if created:
        listing = instance.listing
        host = listing.owner  # assuming `owner` is the host field in Listing
        guest = instance.user

        # 1. Save a notification in DB
        Notification.objects.create(
            user=host,
            message=f"New booking for '{listing.title}' from {guest.get_full_name()} ({guest.email})"
        )

        # 2. Send email to host (if email backend is configured)
        if host.email:
            send_mail(
                subject=f"New Booking for {listing.title}",
                message=f"""
Hello {host.get_full_name() or host.username},

You have a new booking for your property "{listing.title}".

Guest: {guest.get_full_name()} ({guest.email})
Check-in: {instance.check_in}
Check-out: {instance.check_out}

Please check the dashboard for more details.
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[host.email],
                fail_silently=True,
            )
