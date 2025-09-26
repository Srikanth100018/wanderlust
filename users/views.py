from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from decimal import Decimal
from .forms import UserForm, LoginForm
from .models import User
from bookings.models import Booking

User = get_user_model()  # ✅ custom User model


def signup_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Ensure they are normal customers (not staff/admin)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Auto login
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("listings:listing_list")
    else:
        form = UserForm()

    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("listings:listing_list")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("users:login")




@login_required
def profile_view(request):
    user = request.user

    # ✅ Handle profile image upload
    if request.method == "POST" and request.FILES.get("profile_image"):
        user.profile_image = request.FILES["profile_image"]
        user.save()
        return redirect("users:profile")

    # ✅ Get bookings (latest first)
    bookings = Booking.objects.filter(user=user).order_by("booked_at")

    has_discount = False
    if bookings.exists():
        first_booking = bookings.first()
        if not first_booking.is_paid:  # only if unpaid
            # use Decimal instead of float
            first_booking.discounted_price = (first_booking.total_bill * Decimal("0.7")).quantize(Decimal("0.01"))
            has_discount = True

    context = {
        "user": user,
        "bookings": bookings,
        "has_discount": has_discount,
    }
    return render(request, "users/profile.html", context)

