from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "bookmarks"),
    path("<int:bookmark_id>", views.listing, name = "bookmark")
]
