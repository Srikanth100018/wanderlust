import json
import razorpay
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from .models import Payment

# Razorpay client setup
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def create_payment_order(request, booking_id):
    """Create a Razorpay payment order for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Apply 30% discount if this is the user's first paid booking
    has_discount = not Booking.objects.filter(user=request.user, is_paid=True).exists()
    amount = booking.total_bill

    if has_discount:
        amount = (amount * Decimal('0.7')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    try:
        # Convert amount to paise (Razorpay expects smallest currency unit)
        razorpay_amount = int(amount * 100)

        # Create Razorpay order
        order = client.order.create({
            "amount": razorpay_amount,
            "currency": "INR",
            "payment_capture": 1,  # auto capture
            "notes": {
                "booking_id": str(booking.id),
                "user_id": str(request.user.id),
            }
        })

        # Save payment entry (create or update)
        Payment.objects.update_or_create(
            booking=booking,
            defaults={
                "user": request.user,
                "listing": booking.listing,
                "razorpay_order_id": order['id'],
                "amount": razorpay_amount,
                "status": "pending",
            }
        )

        return JsonResponse({
            "order_id": order['id'],
            "amount": razorpay_amount,
            "currency": "INR",
            "name": booking.listing.title,
            "discount_applied": has_discount,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def razorpay_webhook(request):
    """Handle Razorpay webhook events"""
    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
    payload = request.body
    signature = request.META.get("HTTP_X_RAZORPAY_SIGNATURE")

    # Verify webhook signature
    try:
        client.utility.verify_webhook_signature(payload, signature, webhook_secret)
        data = json.loads(payload)
    except Exception:
        return JsonResponse({"status": "invalid signature"}, status=400)

    # Handle payment captured event
    if data.get("event") == "payment.captured":
        razorpay_order_id = data['payload']['payment']['entity']['order_id']
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.status = "paid"
            payment.save()

            booking = payment.booking
            booking.is_paid = True
            booking.save()

        except Payment.DoesNotExist:
            # Optionally log this case
            pass

    return JsonResponse({"status": "ok"}, status=200)


@login_required
def payment_success(request, booking_id):
    """Render success page with payment details"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Mark booking as paid if payment is verified
    payment = Payment.objects.filter(booking=booking).first()
    if payment and payment.status == "paid":
        booking.is_paid = True
        booking.save()

    return render(request, "payments/success.html", {
        "booking": booking,
        "payment": payment
    })


@login_required
def payment_cancel(request, booking_id):
    """Render cancel page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "payments/paymentcancel.html", {"booking": booking})
