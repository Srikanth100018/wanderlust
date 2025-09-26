from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),       # add namespace
    path("listings/", include("listings.urls", namespace="listings")),
    path("", RedirectView.as_view(url=reverse_lazy("listings:listing_list"))),
    path("payments/", include("payments.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
