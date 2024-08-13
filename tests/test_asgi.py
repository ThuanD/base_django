import unittest
from unittest.mock import patch, MagicMock


class TestASGI(unittest.TestCase):
    @patch("django.core.asgi.get_asgi_application")
    def test_asgi_application(self, mock_get_asgi_application):
        # Create a mock ASGI application
        mock_application = MagicMock()
        mock_get_asgi_application.return_value = mock_application

        # Import the asgi module
        from app import asgi

        # Check if the application is correctly set
        self.assertEqual(asgi.application, mock_application)

        # Verify that get_asgi_application was called
        mock_get_asgi_application.assert_called_once()
