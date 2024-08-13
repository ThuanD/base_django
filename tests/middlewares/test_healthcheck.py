import json
from unittest import TestCase
from unittest.mock import Mock

from constance import config as constance_config
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.test import override_settings

from app.config import config
from app.contrib.health_check.middleware import (
    HealthCheckMiddleware,
    MaintenanceMiddleware,
)


class TestHealthCheckMiddleware(TestCase):
    """Test suite for the HealthCheckMiddleware."""

    def setUp(self):
        """Set up the test environment before each test method."""
        self.get_response = Mock(return_value=HttpResponse())
        self.middleware = HealthCheckMiddleware(self.get_response)

    def test_health_check_path(self):
        """Test that the middleware returns a 200 status code for the health
        check path."""
        request = HttpRequest()
        request.path = "/api/health_check/"
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
        self.get_response.assert_not_called()

    def test_non_health_check_path(self):
        """Test that the middleware calls get_response for non-health check
        paths."""
        request = HttpRequest()
        request.path = "/some-other-path"
        response = self.middleware(request)
        self.get_response.assert_called_once_with(request)
        self.assertEqual(response, self.get_response.return_value)


class TestMaintenanceMiddleware(TestCase):
    """Test suite for the MaintenanceMiddleware."""

    def setUp(self):
        """Set up the test environment before each test method."""
        self.get_response = Mock(return_value=HttpResponse())
        self.middleware = MaintenanceMiddleware(self.get_response)

    def tearDown(self):
        config.reset()

    def test_maintenance_disabled(self):
        """Test that the middleware allows all requests when maintenance mode
        is disabled."""
        setattr(constance_config, "MAINTENANCE_ENABLE", False)
        request = HttpRequest()
        request.path = "/some-path"
        response = self.middleware(request)
        self.get_response.assert_called_once_with(request)
        self.assertEqual(response, self.get_response.return_value)

    def test_maintenance_enabled_allowed_path(self):
        """Test that the middleware allows requests to allowed paths when
        maintenance mode is enabled."""
        setattr(constance_config, "MAINTENANCE_ENABLE", True)
        request = HttpRequest()
        request.path = "/admin/"  # Assuming "/admin" is in allowed_paths
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
        self.get_response.assert_called_once_with(request)
        self.assertEqual(response, self.get_response.return_value)

    def test_maintenance_enabled_disallowed_path(self):
        """Test that the middleware blocks requests to disallowed paths when
        maintenance mode is enabled."""
        setattr(constance_config, "MAINTENANCE_ENABLE", True)
        request = HttpRequest()
        request.path = "/some-path/"
        response = self.middleware(request)
        self.get_response.assert_not_called()
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 503)
        content = json.loads(response.content)
        self.assertEqual(content["code"], "E0001")
        self.assertEqual(content["message"], "Server is under maintenance.")

    @override_settings(LANGUAGES=[("en", "English"), ("vi", "Vietnamese")])
    def test_get_allowed_paths(self):
        """Test that _get_allowed_paths returns the correct list of allowed
        paths."""
        paths = self.middleware._get_allowed_paths()
        expected_paths = ["/admin", "/en/admin", "/vi/admin"]
        self.assertEqual(set(paths), set(expected_paths))

    def test_is_allowed_path(self):
        """Test that is_allowed_path correctly identifies allowed and
        disallowed paths."""
        self.middleware.allowed_paths = ["/admin", "/en/admin"]
        request = HttpRequest()

        request.path = "/admin/some/path"
        self.assertTrue(self.middleware.is_allowed_path(request))

        request.path = "/en/admin/some/path"
        self.assertTrue(self.middleware.is_allowed_path(request))

        request.path = "/some/other/path"
        self.assertFalse(self.middleware.is_allowed_path(request))
