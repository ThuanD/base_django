from typing import Callable, List
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings

from app.config import config
from app.constants import HEALTH_CHECK_API
from app.django.exception import ServerIsUnderMaintenance


class HealthCheckMiddleware:
    """Health check middleware for operators."""

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path == HEALTH_CHECK_API:
            return HttpResponse(status=200)
        return self.get_response(request)


class MaintenanceMiddleware:
    """Maintenance middleware for users."""

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.allowed_paths: List[str] = self._get_allowed_paths()

    @staticmethod
    def _get_allowed_paths() -> List[str]:
        allowed_paths = ["/admin"]
        allowed_paths += [f"/{lang[0]}/admin" for lang in settings.LANGUAGES]
        return allowed_paths

    def is_allowed_path(self, request: HttpRequest) -> bool:
        return any(request.path.startswith(path) for path in self.allowed_paths)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.is_allowed_path(request) or not config.MAINTENANCE_ENABLE:
            return self.get_response(request)
        return JsonResponse(
            ServerIsUnderMaintenance().get_full_details(),
            status=ServerIsUnderMaintenance.status_code,
        )
