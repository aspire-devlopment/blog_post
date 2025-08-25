# api/middleware.py
import logging
from django.conf import settings
from django.http import JsonResponse
from ..models.user_models import UserInfo
from ..utils.jwt_utils import decode_jwt

logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Load protected paths from settings
        self.protected_paths = getattr(settings, "PROTECTED_PATHS", [])

    def __call__(self, request):
        # Skip admin paths
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # Normalize path (remove trailing slash for consistency)
        request_path = request.path.rstrip("/")

        # Check if path is protected
        if any(request_path.startswith(p.rstrip("/")) for p in self.protected_paths):
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            if not auth_header.startswith("Bearer "):
                return JsonResponse({"error": "Authorization header missing"}, status=401)

            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)

            if not payload:
                return JsonResponse({"error": "Invalid or expired token"}, status=401)

            user_id = payload.get("user_id")
            if not user_id:
                return JsonResponse({"error": "Invalid token payload"}, status=401)

            try:
                user = UserInfo.objects.get(id=user_id)
                request.user = user
            except UserInfo.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=401)
        else:
            request.user = None

        return self.get_response(request)
