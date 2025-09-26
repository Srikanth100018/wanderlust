from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .models import Booking, Notification, Listing
from .forms import BookingForm
from datetime import date

# -----------------------------
# Notifications
# -----------------------------
@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "bookings/notifications.html", {"notifications": notifications})

# -----------------------------
# Booking list view (all bookings visible depending on role)
# -----------------------------
@login_required
def booking_list(request):
    if request.user.is_staff:
        # Admin → see all bookings
        bookings = Booking.objects.select_related("listing", "user").all()
    elif request.user.groups.filter(name="Hosts").exists():
        # Host → see bookings for their own listings
        bookings = Booking.objects.filter(listing__owner=request.user).select_related("listing", "user")
    else:
        # Guest → see only their own bookings
        bookings = Booking.objects.filter(user=request.user).select_related("listing", "user")

    return render(request, "bookings/booking_list.html", {"bookings": bookings, "today": date.today()})

# -----------------------------
# Listing Detail + Booking Form
# -----------------------------
@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Handle booking submission from listing detail page
    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        if check_in and check_out:
            Booking.objects.create(
                user=request.user,
                listing=listing,
                check_in=check_in,
                check_out=check_out,
            )
            return redirect("listings:listing_detail", pk=listing.id)

    # Determine which bookings to display
    if request.user.is_staff:
        bookings = listing.bookings.select_related("user").all()
    elif request.user == listing.owner:
        bookings = listing.bookings.select_related("user").all()
    else:
        bookings = listing.bookings.filter(user=request.user).select_related("user")

    return render(request, "listings/listing_detail.html", {
        "listing": listing,
        "bookings": bookings,
        "today": date.today(),
    })

# -----------------------------
# Direct Booking Create View (optional)
# -----------------------------
@login_required
def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.clean()  # Run model validation if you added overlaps/capacity checks
                booking.save()
                return redirect("bookings:booking_list")
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()

    return render(request, "bookings/booking_form.html", {"form": form})
