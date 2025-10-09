# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# # import razorpay
# from .models import Listing, Review
# from .forms import ListingForm
# from datetime import datetime
# from bookings.models import Booking
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# # Replace with your Stripe secret ke

# User = get_user_model()

# # ---------------------- HELPERS ----------------------

# def is_host(user):
#     """Check if user is a Host (role=host)."""
#     return getattr(user, "role", None) == User.Role.HOST


# def is_admin(user):
#     """Check if user is an Admin (role=admin OR is_staff)."""
#     return user.is_staff or getattr(user, "role", None) == User.Role.ADMIN


# def is_listing_host(user, listing):
#     """Allow admin or listing owner (host) to edit/delete."""
#     return is_admin(user) or listing.owner == user


# # ---------------------- PUBLIC VIEWS ----------------------

# def home(request):
#     listings = Listing.objects.all()
#     return render(request, "home.html", {"listings": listings})

# from .models import Listing, Review, AppSettings  # add AppSettings

# def listing_list(request):
#     query = request.GET.get("q", "")
#     category = request.GET.get("category", "All")

#     listings = Listing.objects.all()

#     if query:
#         listings = listings.filter(title__icontains=query)

#     if category and category != "All":
#         listings = listings.filter(category__iexact=category)

#     # ✅ Fetch GST settings
#     app_settings = AppSettings.objects.first()

#     context = {
#         "listings": listings,
#         "active_category": category,
#         "app_settings": app_settings,  # pass to template
#     }
#     return render(request, "listings/listing_list.html", context)




# def listing_detail(request, pk):
#     listing = get_object_or_404(Listing, pk=pk)

#     # ----------------- Handle Booking -----------------
#     if request.method == "POST":
#         if not request.user.is_authenticated:
#             messages.error(request, "You must be logged in to book.")
#             return redirect("users:login")  # adjust your login URL name

#         if request.user.is_staff:
#             messages.error(request, "Staff cannot make bookings.")
#             return redirect("listings:listing_detail", pk=listing.id)

#         check_in = request.POST.get("check_in")
#         check_out = request.POST.get("check_out")

#         if check_in and check_out:
#             try:
#                 check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
#                 check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

#                 if check_out_date <= check_in_date:
#                     messages.error(request, "Check-out must be after check-in.")
#                     return redirect("listings:listing_detail", pk=listing.id)

#                 Booking.objects.create(
#                     user=request.user,
#                     listing=listing,
#                     check_in=check_in_date,
#                     check_out=check_out_date,
#                 )
#                 messages.success(request, "Booking successful!")
#                 return redirect("listings:listing_detail", pk=listing.id)

#             except Exception as e:
#                 messages.error(request, f"Invalid booking dates: {e}")

#     # ----------------- Bookings Visibility -----------------
#     bookings = None
#     if request.user.is_authenticated:
#         if request.user.is_staff or request.user == listing.owner:
#             bookings = listing.bookings.select_related("user").all()

#     # ----------------- Reviews -----------------
#     reviews = listing.reviews.all()

#     return render(request, "listings/listing_detail.html", {
#         "listing": listing,
#         "reviews": reviews,
#         "bookings": bookings,
#         "today": datetime.today().date(),
#     })

# # ---------------------- CRUD ----------------------

# @login_required
# def listing_create(request):
#     if not (is_admin(request.user) or is_host(request.user)):
#         messages.error(request, "You are not allowed to create listings.")
#         return redirect("listings:listing_list")

#     if request.method == "POST":
#         form = ListingForm(request.POST, request.FILES)
#         if form.is_valid():
#             listing = form.save(commit=False)
#             listing.owner = request.user
#             listing.save()
#             messages.success(request, "Listing created successfully.")
#             return redirect("listings:listing_detail", pk=listing.pk)
#     else:
#         form = ListingForm()

#     return render(request, "listings/listing_form.html", {"form": form})


# @login_required
# def listing_edit(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)

#     if not is_listing_host(request.user, listing):
#         messages.error(request, "You cannot edit this listing.")
#         return redirect("listings:listing_detail", pk=listing.pk)

#     if request.method == "POST":
#         form = ListingForm(request.POST, request.FILES, instance=listing)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Listing updated successfully.")
#             return redirect("listings:listing_detail", pk=listing.pk)
#     else:
#         form = ListingForm(instance=listing)

#     return render(request, "listings/listing_form.html", {"form": form, "listing": listing})


# @login_required
# def listing_delete(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)

#     if not is_listing_host(request.user, listing):
#         messages.error(request, "You cannot delete this listing.")
#         return redirect("listings:listing_detail", pk=listing.pk)

#     if request.method == "POST":
#         listing.delete()
#         messages.success(request, "Listing deleted successfully.")
#         return redirect("listings:listing_list")

#     return render(request, "listings/listing_confirm_delete.html", {"listing": listing})


# # ---------------------- BOOKINGS ----------------------

# @login_required
# def book_listing(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)

#     if request.method == "POST":
#         check_in = request.POST.get("check_in")
#         check_out = request.POST.get("check_out")

#         try:
#             check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
#             check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

#             if check_out_date <= check_in_date:
#                 messages.error(request, "Check-out must be after check-in.")
#                 return redirect("listings:listing_detail", pk=listing.id)

#             Booking.objects.create(
#                 user=request.user,
#                 listing=listing,
#                 check_in=check_in_date,
#                 check_out=check_out_date,
#             )
#             messages.success(request, "Booking successful!")
#             return redirect("listings:listing_detail", pk=listing.id)

#         except Exception:
#             messages.error(request, "Invalid booking dates.")

#     return redirect("listings:listing_detail", pk=listing.id)


# # ---------------------- REVIEWS ----------------------

# @login_required
# def add_review(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)

#     if is_admin(request.user):
#         messages.error(request, "Admins cannot leave reviews.")
#         return redirect("listings:listing_detail", pk=listing.id)

#     if listing.reviews.filter(user=request.user).exists():
#         messages.warning(request, "You have already reviewed this listing.")
#         return redirect("listings:listing_detail", pk=listing.id)

#     if request.method == "POST":
#         rating = request.POST.get("rating")
#         comment = request.POST.get("comment")

#         if rating and comment:
#             Review.objects.create(
#                 listing=listing,
#                 user=request.user,
#                 rating=rating,
#                 comment=comment
#             )
#             messages.success(request, "Your review has been added!")
#         else:
#             messages.error(request, "Please provide both rating and comment.")

#     return redirect("listings:listing_detail", pk=listing.id)


# @login_required
# def delete_review(request, listing_id, review_id):
#     listing = get_object_or_404(Listing, id=listing_id)
#     review = get_object_or_404(Review, id=review_id, listing=listing)

#     if request.user == review.user or is_admin(request.user):
#         review.delete()
#         messages.success(request, "Review deleted.")
#     else:
#         messages.error(request, "You cannot delete this review.")

#     return redirect("listings:listing_detail", pk=listing.id)


# # ---------------------- STATIC PAGES ----------------------

# def privacy(request):
#     return render(request, "listings/privacy.html")


# def terms(request):
#     return render(request, "listings/terms.html")


# # ---------------------- PAYMENTS ----------------------



# def autocomplete_search(request):
#     query = request.GET.get('term', '')  # jQuery UI sends 'term' by default
#     if query:
#         listings = Listing.objects.filter(title__icontains=query)[:10]
#         results = [listing.title for listing in listings]
#         return JsonResponse(results, safe=False)
#     return JsonResponse([], safe=False)


# def payment_success(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)
#     return render(request, 'listings/payment_success.html', {'listing': listing})


# def payment_cancel(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)
#     return render(request, 'listings/payment_cancel.html', {'listing': listing})

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Listing, Review, AppSettings
from .forms import ListingForm
from bookings.models import Booking

User = get_user_model()

# ---------------------- HELPERS ----------------------

def is_host(user):
    """Check if user is a Host."""
    return getattr(user, "role", None) == User.Role.HOST


def is_admin(user):
    """Check if user is an Admin (role=admin or is_staff)."""
    return user.is_staff or getattr(user, "role", None) == User.Role.ADMIN


def is_listing_host(user, listing):
    """Allow admin or listing owner (host) to modify listing."""
    return is_admin(user) or listing.owner == user


# ---------------------- PUBLIC VIEWS ----------------------

def home(request):
    """Render home page with all listings."""
    listings = Listing.objects.all()
    return render(request, "home.html", {"listings": listings})


def listing_list(request):
    """Display all listings with search and filter."""
    query = request.GET.get("q", "")
    category = request.GET.get("category", "All")

    listings = Listing.objects.all()

    if query:
        listings = listings.filter(title__icontains=query)

    if category and category != "All":
        listings = listings.filter(category__iexact=category)

    # Fetch GST or app-level settings (optional)
    app_settings = AppSettings.objects.first()

    context = {
        "listings": listings,
        "active_category": category,
        "app_settings": app_settings,
    }
    return render(request, "listings/listing_list.html", context)


def listing_detail(request, pk):
    """Show listing details, handle booking and display reviews."""
    listing = get_object_or_404(Listing, pk=pk)

    # ----------------- Handle Booking -----------------
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to book.")
            return redirect("users:login")

        if request.user.is_staff:
            messages.error(request, "Staff cannot make bookings.")
            return redirect("listings:listing_detail", pk=listing.id)

        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

                if check_out_date <= check_in_date:
                    messages.error(request, "Check-out must be after check-in.")
                    return redirect("listings:listing_detail", pk=listing.id)

                Booking.objects.create(
                    user=request.user,
                    listing=listing,
                    check_in=check_in_date,
                    check_out=check_out_date,
                )
                messages.success(request, "Booking created successfully!")
                return redirect("listings:listing_detail", pk=listing.id)

            except ValueError:
                messages.error(request, "Invalid date format. Please try again.")

    # ----------------- Show Bookings -----------------
    bookings = None
    if request.user.is_authenticated and (request.user.is_staff or request.user == listing.owner):
        bookings = listing.bookings.select_related("user").all()

    # ----------------- Reviews -----------------
    reviews = listing.reviews.all()

    return render(request, "listings/listing_detail.html", {
        "listing": listing,
        "reviews": reviews,
        "bookings": bookings,
        "today": datetime.today().date(),
    })


# ---------------------- CRUD ----------------------

@login_required
def listing_create(request):
    """Create a new listing (only for hosts/admins)."""
    if not (is_admin(request.user) or is_host(request.user)):
        messages.error(request, "You are not allowed to create listings.")
        return redirect("listings:listing_list")

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, "Listing created successfully.")
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ListingForm()

    return render(request, "listings/listing_form.html", {"form": form})


@login_required
def listing_edit(request, listing_id):
    """Edit an existing listing."""
    listing = get_object_or_404(Listing, id=listing_id)

    if not is_listing_host(request.user, listing):
        messages.error(request, "You cannot edit this listing.")
        return redirect("listings:listing_detail", pk=listing.pk)

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully.")
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ListingForm(instance=listing)

    return render(request, "listings/listing_form.html", {"form": form, "listing": listing})


@login_required
def listing_delete(request, listing_id):
    """Delete a listing (host/admin only)."""
    listing = get_object_or_404(Listing, id=listing_id)

    if not is_listing_host(request.user, listing):
        messages.error(request, "You cannot delete this listing.")
        return redirect("listings:listing_detail", pk=listing.pk)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect("listings:listing_list")

    return render(request, "listings/listing_confirm_delete.html", {"listing": listing})


# ---------------------- BOOKINGS ----------------------

@login_required
def book_listing(request, listing_id):
    """Book a listing."""
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

            if check_out_date <= check_in_date:
                messages.error(request, "Check-out must be after check-in.")
                return redirect("listings:listing_detail", pk=listing.id)

            Booking.objects.create(
                user=request.user,
                listing=listing,
                check_in=check_in_date,
                check_out=check_out_date,
            )
            messages.success(request, "Booking successful!")
            return redirect("listings:listing_detail", pk=listing.id)

        except ValueError:
            messages.error(request, "Invalid booking dates.")

    return redirect("listings:listing_detail", pk=listing.id)


# ---------------------- REVIEWS ----------------------

@login_required
def add_review(request, listing_id):
    """Add a review for a listing."""
    listing = get_object_or_404(Listing, id=listing_id)

    if is_admin(request.user):
        messages.error(request, "Admins cannot leave reviews.")
        return redirect("listings:listing_detail", pk=listing.id)

    if listing.reviews.filter(user=request.user).exists():
        messages.warning(request, "You have already reviewed this listing.")
        return redirect("listings:listing_detail", pk=listing.id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating and comment:
            Review.objects.create(
                listing=listing,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Your review has been added!")
        else:
            messages.error(request, "Please provide both rating and comment.")

    return redirect("listings:listing_detail", pk=listing.id)


@login_required
def delete_review(request, listing_id, review_id):
    """Delete a review (by author or admin)."""
    listing = get_object_or_404(Listing, id=listing_id)
    review = get_object_or_404(Review, id=review_id, listing=listing)

    if request.user == review.user or is_admin(request.user):
        review.delete()
        messages.success(request, "Review deleted.")
    else:
        messages.error(request, "You cannot delete this review.")

    return redirect("listings:listing_detail", pk=listing.id)


# ---------------------- STATIC PAGES ----------------------

def privacy(request):
    """Privacy policy page."""
    return render(request, "listings/privacy.html")


def terms(request):
    """Terms and conditions page."""
    return render(request, "listings/terms.html")


# ---------------------- AUTOCOMPLETE SEARCH ----------------------

def autocomplete_search(request):
    """Autocomplete search for listing titles."""
    query = request.GET.get('term', '')  # jQuery UI sends 'term' by default
    if query:
        listings = Listing.objects.filter(title__icontains=query)[:10]
        results = [listing.title for listing in listings]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


# ---------------------- PAYMENT PAGES (Redirect) ----------------------

def payment_success(request, listing_id):
    """Render payment success page."""
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/payment_success.html', {'listing': listing})


def payment_cancel(request, listing_id):
    """Render payment cancellation page."""
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/payment_cancel.html', {'listing': listing})
