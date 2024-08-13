"""URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.apps import apps
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

root_url = []

urlpatterns = [
    path("api/", include(root_url)),
]

if apps.is_installed("django.contrib.admin"):
    urlpatterns += i18n_patterns(
        path("admin/", admin.site.urls),
    )

if apps.is_installed("debug_toolbar"):
    urlpatterns += i18n_patterns(
        path("__debug__/", include("debug_toolbar.urls")),
    )

if apps.is_installed("drf_spectacular"):
    urlpatterns += i18n_patterns(
        path("api_doc/", include("apps.api_doc.urls")),
    )

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
