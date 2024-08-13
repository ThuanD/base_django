import json
import unittest
from unittest.mock import Mock, patch

from app.contrib.dumper.middleware import RequestDumperMiddleware
from django.http import HttpResponse
from django.test import RequestFactory
from django.core.cache import cache

from app.constants import CacheKey
from app.message.middlewares import START_REQUEST, END_REQUEST


class TestRequestDumperMiddleware(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestDumperMiddleware(
            get_response=Mock(return_value=HttpResponse())
        )

    def tearDown(self):
        cache.clear()

    @patch("app.contrib.dumper.middleware.logger")
    def test_middleware_call(self, mock_logger):
        request = self.factory.get("/test/", {"param": "value"})
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cache.get(CacheKey.REQUEST_COUNT), 2)

        # Check if log_request was called twice
        self.assertEqual(mock_logger.info.call_count, 2)

    @patch("app.contrib.dumper.middleware.logger")
    def test_log_request(self, mock_logger):
        request = self.factory.get("/test/", {"param": "value"})
        RequestDumperMiddleware.log_request(request, 1, START_REQUEST)

        expected_log = (
            "REQUEST 1 [method=GET, content_type=, path=/test/, query=param=value], "
            "Start of request."
        )
        mock_logger.info.assert_called_once_with(expected_log)

    @patch("app.contrib.dumper.middleware.logger")
    def test_log_request_with_body(self, mock_logger):
        data = {"param": "value"}
        request = self.factory.post(
            "/test/",
            data=data,
            content_type="application/json",
        )
        RequestDumperMiddleware.log_request(request, 1, END_REQUEST)

        expected_log = (
            "REQUEST 1 [method=POST, content_type=application/json, "
            f"path=/test/, query=, body={json.dumps(data)}], End of request."
        )
        mock_logger.info.assert_called_once_with(expected_log)

    def test_get_request_body_success(self):
        request = Mock()
        request.body.decode.return_value = "test_body"
        body = RequestDumperMiddleware.get_request_body(request)
        self.assertEqual(body, "test_body")

    @patch("app.contrib.dumper.middleware.logger")
    def test_get_request_body_failure(self, mock_logger):
        request = Mock()
        request.body.decode.side_effect = UnicodeDecodeError(
            "utf-8", b"", 0, 1, "invalid start byte"
        )
        body = RequestDumperMiddleware.get_request_body(request)
        self.assertEqual(body, "")
        mock_logger.warning.assert_called_once()
