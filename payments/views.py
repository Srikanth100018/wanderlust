import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_HALF_UP
from bookings.models import Booking
from .models import Payment

# Razorpay client setup
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def create_payment_order(request, booking_id):
    """Create a Razorpay payment order for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Apply 30% discount if first booking
    has_discount = not Booking.objects.filter(user=request.user, is_paid=True).exists()
    amount = booking.total_bill
    if has_discount:
        amount = (amount * Decimal('0.7')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    try:
        # Convert amount to paise (Razorpay expects smallest currency unit)
        razorpay_amount = int(amount * 100)

        # Create Razorpay order
        order = client.order.create(dict(
            amount=razorpay_amount,
            currency="INR",
            payment_capture='1',  # auto capture
            notes={"booking_id": str(booking.id), "user_id": str(request.user.id)}
        ))

        # Save payment entry
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
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def razorpay_webhook(request):
    """Handle Razorpay webhook events"""
    import json
    from django.views.decorators.http import require_POST

    @require_POST
    def _handler(request):
        payload = request.body
        signature = request.META.get("HTTP_X_RAZORPAY_SIGNATURE")
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET

        # Verify webhook signature
        try:
            client.utility.verify_webhook_signature(payload, signature, webhook_secret)
            data = json.loads(payload)
        except Exception:
            return JsonResponse({"status": "invalid signature"}, status=400)

        # Payment captured successfully
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
                pass

        return JsonResponse({"status": "ok"}, status=200)

    return _handler(request)


@login_required
def payment_success(request, booking_id):
    """Render success page with payment details"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.is_paid = True
    booking.save()

    # Get the related payment object (if exists)
    try:
        payment = Payment.objects.get(booking=booking)
    except Payment.DoesNotExist:
        payment = None

    return render(request, "payments/success.html", {
        "booking": booking,
        "payment": payment
    })


@login_required
def payment_cancel(request, booking_id):
    """Render cancel page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "payments/paymentcancel.html", {"booking": booking})
