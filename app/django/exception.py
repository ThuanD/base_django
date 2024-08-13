import logging
from typing import Optional, Dict, Any

from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_503_SERVICE_UNAVAILABLE,
)
from rest_framework.views import set_rollback

from app.config import config
from app.message.errors import (
    MAINTENANCE_ERROR_DETAIL,
    MAINTENANCE_ERROR_CODE,
)

logger = logging.getLogger(__name__)


def exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    """Override default exception handler
    rest_framework.views.exception_handler."""
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))  # NOQA
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))  # NOQA

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header  # NOQA
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait  # NOQA

        if isinstance(exc, exceptions.ValidationError):
            exc = RequestBodyValidationError(exc.get_full_details())
        data = exc.get_full_details()
        set_rollback()

        response_class = Response if config.DEBUG else JsonResponse
        return response_class(data, status=exc.status_code, headers=headers)

    return None


class RequestBodyValidationError(exceptions.ValidationError):
    """Request body validation error."""

    def __init__(self, detail: Dict[str, Any]) -> None:
        self.detail = detail

    def get_full_details(self):
        return dict(code=self.default_code, message=self.detail)


class ServerIsUnderMaintenance(exceptions.APIException):
    """Server is under maintenance."""

    status_code = HTTP_503_SERVICE_UNAVAILABLE
    default_detail = MAINTENANCE_ERROR_DETAIL
    default_code = MAINTENANCE_ERROR_CODE
