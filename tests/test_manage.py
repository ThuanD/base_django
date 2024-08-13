import os
import unittest
from unittest.mock import patch, MagicMock

from manage import _get_django_setting_module


class TestGetDjangoSettingModule(unittest.TestCase):
    @patch("manage._get_django_setting_module")
    @patch.dict("os.environ", {}, clear=True)
    def test_django_import_error(self, mock_get_settings):
        mock_get_settings.return_value = "app.settings.local"

        with patch.dict("sys.modules", {"django.core.management": None}):
            with self.assertRaises(ImportError) as context:
                from manage import main

                main()

        self.assertIn(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?",
            str(context.exception),
        )

    @patch("argparse.ArgumentParser.parse_known_args")
    def test_settings_from_command_line(self, mock_parse_known_args):
        # Simulate --settings argument provided via command line
        mock_args = MagicMock()
        mock_args.settings = "app.settings.production"
        mock_parse_known_args.return_value = (mock_args, None)

        result = _get_django_setting_module()
        self.assertEqual(result, "app.settings.production")

    @patch("argparse.ArgumentParser.parse_known_args")
    def test_settings_from_env_file(
        self,
        mock_parse_known_args,
    ):
        os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings.staging"
        mock_args = MagicMock()
        mock_args.settings = None
        mock_parse_known_args.return_value = (mock_args, None)
        result = _get_django_setting_module()
        self.assertEqual(result, "app.settings.staging")

    @patch("argparse.ArgumentParser.parse_known_args")
    def test_default_settings(self, mock_parse_known_args):
        mock_args = MagicMock()
        mock_args.settings = None
        mock_parse_known_args.return_value = (mock_args, [])
        result = _get_django_setting_module(".env.mock")
        self.assertEqual(result, "app.settings.local")
