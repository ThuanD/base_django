import json
from unittest import TestCase

from app.config import config
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.test import override_settings

from rest_framework import exceptions
from rest_framework.response import Response

from app.django.exception import exception_handler


class TestExceptionHandler(TestCase):
    def tearDown(self):
        config.reset()

    def test_http404_exception(self):
        response = exception_handler(Http404(), {})
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content)
        self.assertEqual(content["code"], "not_found")
        self.assertEqual(content["message"], "Not found.")

    def test_permission_denied_exception(self):
        response = exception_handler(PermissionDenied(), {})
        self.assertEqual(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEqual(content["code"], "permission_denied")
        self.assertEqual(
            content["message"], "You do not have permission to perform this action."
        )

    def test_api_exception_with_auth_header(self):
        exc = exceptions.AuthenticationFailed()
        exc.auth_header = "Bearer realm='api'"
        response = exception_handler(exc, {})
        self.assertEqual(response.status_code, 401)
        content = json.loads(response.content)
        self.assertEqual(content["code"], "authentication_failed")
        self.assertEqual(content["message"], "Incorrect authentication credentials.")
        self.assertEqual(response["WWW-Authenticate"], "Bearer realm='api'")

    def test_api_exception_with_wait(self):
        exc = exceptions.Throttled(wait=60)
        response = exception_handler(exc, {})
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response["Retry-After"], "60")

    def test_validation_error(self):
        exc = exceptions.ValidationError({"field": ["This field is required."]})
        response = exception_handler(exc, {})
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(content["code"], "invalid")
        self.assertEqual(
            content["message"],
            {"field": [{"message": "This field is required.", "code": "invalid"}]},
        )

    @override_settings(DEBUG=False)
    def test_json_response_in_production(self):
        response = exception_handler(exceptions.NotFound(), {})
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=True)
    def test_response_in_development(self):
        response = exception_handler(exceptions.NotFound(), {})
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 404)

    def test_non_api_exception(self):
        exc = ValueError("Some error")
        response = exception_handler(exc, {})
        self.assertIsNone(response)
