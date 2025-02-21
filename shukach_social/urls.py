from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('admin/',    admin.site.urls,           name = "admin"),
    path('',          views.IndexView.as_view(), name = "index"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/", include("accounts.urls")),
    path("news/",     include("news.urls")),
    path("api/",      include("api.urls")),
]
