#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import argparse
import os
import sys

from dotenv import load_dotenv


def _get_django_setting_module(env_file=".env") -> str:
    """Return django settings module."""
    # Get django settings module from manage.py command
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", help="Django settings module")
    args, _ = parser.parse_known_args()
    if args.settings:
        return args.settings
    # Get django settings module from .env file
    if load_dotenv(env_file):
        return os.getenv("DJANGO_SETTINGS_MODULE")
    # Return django settings module default
    return "app.settings.local"


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", _get_django_setting_module())
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
