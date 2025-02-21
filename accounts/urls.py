from django.urls import path

from accounts import views


app_name = "accounts"
urlpatterns = [
    path("register/", views.RegisterView.as_view(), name = "register"),
    path("profile/",  views.ProfileView.as_view(),  name = "profile"),
    
    path("mailings/create",                  views.MailingCreateView.as_view(), name = "mailing_create"),
    path("mailings/<int:mailing_id>",        views.MailingDetailView.as_view(), name = "mailing_detail"),
    path("mailings/<int:mailing_id>/update", views.MailingUpdateView.as_view(), name = "mailing_update"),

    path("projects/create",                  views.ProjectCreateView.as_view(), name = "project_create"),
    path("projects/<int:project_id>",        views.ProjectDetailView.as_view(), name = "project_detail"),
    path("projects/<int:project_id>/delete", views.ProjectDeleteView.as_view(), name = "project_delete"),
    path("projects/<int:project_id>/update", views.ProjectUpdateView.as_view(), name = "project_update"),
    path("projects/<int:project_id>/search", views.ProjectSearchView.as_view(), name = "project_search"),

    
]
