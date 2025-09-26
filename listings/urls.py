from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),             # Show all listings
    path('new/', views.listing_create, name='listing_create'),     # Create a new listing (host only)
    path('<int:pk>/', views.listing_detail, name='listing_detail'),# View listing details
    path('<int:listing_id>/edit/', views.listing_edit, name='listing_edit'),# Edit listing (host only)
    path("<int:listing_id>/book/", views.book_listing, name="book_listing"),
    path('<int:listing_id>/delete/', views.listing_delete, name='listing_delete'),# Delete listing
    path("<int:listing_id>/add_review/", views.add_review, name="add_review"),
    path("<int:listing_id>/delete_review/<int:review_id>/", views.delete_review, name="delete_review"),
    path('create-checkout-session/<int:listing_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('search/', views.autocomplete_search, name='autocomplete_search'),
    path('payment-success/<int:listing_id>/', views.payment_success, name='payment_success'),
    path('payment-cancel/<int:listing_id>/', views.payment_cancel, name='payment_cancel'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]
