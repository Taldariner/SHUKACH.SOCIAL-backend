from django.urls import path

from . import views


app_name = "api"
urlpatterns = [
    path("",               views.IndexView.as_view(), name = "main"),
    path("resonant_news/", views.ResonantNewsAPI.as_view(), name = "resonant_news"),
]
