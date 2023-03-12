from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "listings"),
    path("<uuid:listing_id>", views.listing, name = "listing"),
    path("search", views.search, name = "search")
]
