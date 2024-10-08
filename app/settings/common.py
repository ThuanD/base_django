"""Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from app.constants import TRUE_VALUES

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# get env
django_settings_module = os.getenv("DJANGO_SETTINGS_MODULE")
env = django_settings_module.split(".")[-1]
# load .env file
if not load_dotenv(os.path.join(BASE_DIR, ".env." + env)):
    if not load_dotenv(os.path.join(BASE_DIR, ".env")):
        print("\033[91mERROR: Unable to find .env file.")
        sys.exit(1)
    django_settings_module = os.getenv("DJANGO_SETTINGS_MODULE")

IS_LOCAL = django_settings_module == "app.settings.local"
IS_LOCAL_TEST = django_settings_module == "app.settings.local_test"
IS_STAGING = django_settings_module == "app.settings.staging"
IS_PRODUCTION = django_settings_module == "app.settings.production"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") in TRUE_VALUES

ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()
]

# SECURITY WARNING: don't allow all origins in production!
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
cors_allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS")
if cors_allowed_origins:
    CORS_ALLOWED_ORIGINS = [
        origin.strip() for origin in cors_allowed_origins.split(",") if origin.strip()
    ]
else:
    CORS_ALLOWED_ORIGINS = []

csrf_trusted_origins = os.getenv("CSRF_TRUSTED_ORIGINS")
if csrf_trusted_origins:
    CSRF_TRUSTED_ORIGINS = [
        origin.strip() for origin in csrf_trusted_origins.split(",") if origin.strip()
    ]
else:
    CSRF_TRUSTED_ORIGINS = []

# Application definition
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
]
THIRD_PARTY_APPS = [
    "constance",
    "corsheaders",
    "django_filters",
    "rest_framework",
]
CUSTOM_APPS = [
    "apps.api_doc",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "app.contrib.health_check.middleware.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "app.contrib.health_check.middleware.MaintenanceMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.contrib.dumper.middleware.RequestDumperMiddleware",
]

ROOT_URLCONF = "app.urls"
APPEND_SLASH = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # NOQA NOSONAR
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# locale
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
LANGUAGE_DEFAULT = "en"
LANGUAGES = [
    ("en", _("English")),
    ("vi", _("Vietnamese")),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = []

# Media file
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "auth.User"

# django-extensions
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = False
SHELL_PLUS_IMPORTS = [
    "from app.config import config",
]
# logging
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
if IS_PRODUCTION:
    LOG_LEVEL = "INFO"
    BACKUP_COUNT = 100
elif IS_STAGING:
    LOG_LEVEL = "DEBUG"
    BACKUP_COUNT = 30
else:
    LOG_LEVEL = "DEBUG"
    BACKUP_COUNT = 10
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s: %(name)s:%(lineno)d %(process)d %(thread)d "
            "[%(levelname)s] - %(message)s"
        },
    },
    "handlers": {
        "backend_log_file": {
            "level": "ERROR",
            "filters": [],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/backend.log"),
            "when": "M",
            "interval": 1,
            "backupCount": BACKUP_COUNT,
            "formatter": "verbose",
        },
        "sql_log_file": {
            "level": "DEBUG",
            "filters": [],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/sql.log"),
            "when": "M",
            "interval": 1,
            "backupCount": BACKUP_COUNT,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["backend_log_file"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["sql_log_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "app": {
            "handlers": ["backend_log_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "apps": {
            "handlers": ["backend_log_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

REST_FRAMEWORK = {
    # Base API policies
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_VERSIONING_CLASS": None,
    # Generic view behavior
    "DEFAULT_PAGINATION_CLASS": "app.django.pagination.CustomPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    # Throttling
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/day",
        "user": "10000/day",
    },
    # Pagination
    "PAGE_SIZE": 20,
    # Versioning
    "DEFAULT_VERSION": "1",
    "ALLOWED_VERSIONS": None,
    "VERSION_PARAM": "version",
    # Exception handling
    "EXCEPTION_HANDLER": "app.django.exception.exception_handler",
}


# SMTP Gmail
EMAIL_USE_LOCALTIME = True
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 5  # seconds
EMAIL_PORT = 587
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_SUBJECT_PREFIX = "[APP]"

MAINTENANCE_ENABLE = False

# django-constance
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    # Maintenance configuration
    "MAINTENANCE_ENABLE": (MAINTENANCE_ENABLE, _("Maintenance mode"), bool),
}
CONSTANCE_CONFIG_FIELDSETS = (
    (
        _("Maintenance configuration"),
        {
            "fields": ("MAINTENANCE_ENABLE",),
        },
    ),
)
