import unittest
from unittest.mock import patch, MagicMock

from app import wsgi


class TestWSGI(unittest.TestCase):
    @patch("app.wsgi.argparse.ArgumentParser")
    def test_settings_from_command_line(self, mock_argparse):
        """Test when --env argument is provided."""
        mock_args = MagicMock()
        mock_args.env = "app.settings.production"
        mock_argparse.return_value.parse_known_args.return_value = (mock_args, None)

        result = wsgi._get_django_setting_module()
        self.assertEqual(result, "app.settings.production")

    @patch("app.wsgi.load_dotenv")
    @patch("app.wsgi.os.getenv")
    @patch("app.wsgi.argparse.ArgumentParser")
    def test_settings_from_env_file(self, mock_argparse, mock_getenv, mock_load_dotenv):
        """Test when --env argument is not provided and .env file exists."""
        mock_args = MagicMock()
        mock_args.env = None
        mock_argparse.return_value.parse_known_args.return_value = (mock_args, None)
        mock_load_dotenv.return_value = True
        mock_getenv.return_value = "app.settings.staging"
        result = wsgi._get_django_setting_module()
        self.assertEqual(result, "app.settings.staging")

    @patch("app.wsgi.load_dotenv")
    @patch("app.wsgi.argparse.ArgumentParser")
    def test_default_settings(self, mock_argparse, mock_load_dotenv):
        """Test when --env argument is not provided and .env file doesn't
        exists."""
        mock_args = MagicMock()
        mock_args.env = None
        mock_argparse.return_value.parse_known_args.return_value = (mock_args, None)
        mock_load_dotenv.return_value = False

        result = wsgi._get_django_setting_module()
        self.assertEqual(result, "app.settings.local")
