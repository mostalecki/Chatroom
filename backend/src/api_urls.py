from django.urls import path, include


urlpatterns = [
    path("", include("src.apps.authentication.urls")),
    path("", include("src.apps.profile.urls")),
]
