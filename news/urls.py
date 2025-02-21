from django.urls import path

from . import views


app_name = "news"
urlpatterns = [
    path("",                     views.NewsMainView.as_view(),   name = "main"),
    path('export/',              views.NewsExportView.as_view(), name = "export"),
    path("<int:news_id>/",       views.NewsDetailView.as_view(), name = "detail"),
    path("<int:news_id>/update", views.NewsUpdateView.as_view(), name = "update"),
    path("<int:news_id>/delete", views.NewsDeleteView.as_view(), name = "delete"),
    path("create/",              views.NewsCreateView.as_view(), name = "create"),
]
