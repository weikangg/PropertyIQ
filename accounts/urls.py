from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name = "login"),
    path("logout", views.logout, name = "logout"),
    path("register", views.register, name = "register"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path("update", views.update, name = "update"),
    path("bookmarks/<uuid:listing_id>", views.bookmarks, name = "bookmarks"),
    path("history", views.searchHistory, name = "searchHistory"),
    path('clearHistory', views.clearSearchHistory,name = "clearHistory")
]
