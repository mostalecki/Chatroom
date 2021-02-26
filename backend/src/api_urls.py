from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("", include("src.apps.authentication.urls")),
    path("", include("src.apps.profile.urls")),
]

if settings.DEBUG:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="Chatroom API",
            default_version="v1",
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += (
        path(
            "swagger",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    )
