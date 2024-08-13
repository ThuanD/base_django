"""WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import argparse
import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv


def _get_django_setting_module() -> str:
    """Return django settings module."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", help="Django settings module")
    args, _ = parser.parse_known_args()
    if args.env:
        return args.env
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    # Get django settings module from .env file
    if load_dotenv(env_path):
        return os.getenv("DJANGO_SETTINGS_MODULE")
    # Return django settings module default
    return "app.settings.local"


os.environ.setdefault("DJANGO_SETTINGS_MODULE", _get_django_setting_module())

application = get_wsgi_application()
