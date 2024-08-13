import logging
from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.core.cache import cache
from app.constants import CacheKey
from app.message.middlewares import START_REQUEST, END_REQUEST

logger = logging.getLogger(__name__)


class RequestDumperMiddleware:
    """Middleware for logging Django Request objects."""

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_count = cache.get(CacheKey.REQUEST_COUNT, 1)
        cache.set(CacheKey.REQUEST_COUNT, request_count + 1)

        self.log_request(request, request_count, START_REQUEST)
        response = self.get_response(request)
        self.log_request(request, request_count, END_REQUEST)

        return response

    @staticmethod
    def log_request(request: HttpRequest, count: int, stage: str) -> None:
        query = request.META.get("QUERY_STRING", "")
        body = RequestDumperMiddleware.get_request_body(request)
        if body:
            body = f", body={body}"
        log_message = (
            f"REQUEST {count} "
            f"[method={request.method}, content_type={request.content_type}, "
            f"path={request.path}, query={query}{body}], {stage}"
        )
        logger.info(log_message)

    @staticmethod
    def get_request_body(request: HttpRequest) -> str:
        try:
            return request.body.decode("utf-8")
        except Exception as error:
            logger.warning(f"Failed to decode request body: {error}")
            return ""
