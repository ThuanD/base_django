from django.urls import path
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularJSONAPIView,
)

app_name = "api_doc"
urlpatterns = [
    path(
        "redoc/", SpectacularRedocView.as_view(url_name="api_doc:schema"), name="redoc"
    ),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="api_doc:schema"),
        name="swagger-ui",
    ),
    path(
        "schema/",
        SpectacularJSONAPIView.as_view(),
        name="schema",
    ),
]
