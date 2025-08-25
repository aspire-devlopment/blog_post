# api/views.py
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..services.login_service import LoginService
from ..utils.request_logger import RequestLogger

logger = logging.getLogger(__name__)
# Dependency injection: assign the service
login_service = LoginService() 

@csrf_exempt
async def user_login(request):
    req_logger = RequestLogger()

    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not email or not password:
            return JsonResponse({"error": "Email and Password are required"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:

        result = await login_service.login_user(data.get("email"), data.get("password"))
        logger.info(f"Login successful in {req_logger.duration_ms():.2f}ms")
        return JsonResponse(result)
    except ValueError as e:
        logger.warning(f"Login failed in {req_logger.duration_ms():.2f}ms: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Login error in {req_logger.duration_ms():.2f}ms: {str(e)}", exc_info=True)
        return JsonResponse({"error": "Internal Server Error"}, status=500)

def protected_view(request):
    return JsonResponse({"message": " you are authorized!"})