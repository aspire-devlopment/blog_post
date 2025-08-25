# api/views.py
import json
import logging
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..services.user_service import UserService
from ..utils.request_logger import RequestLogger

logger = logging.getLogger(__name__)
# Dependency injection: assign the service
user_service = UserService() 

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")  # accepts numbers with optional +, 7-15 digits
@csrf_exempt

async def user_list(request):
    req_logger = RequestLogger()

    try:
        if request.method == "GET":
            users = await user_service.list_users()
            logger.info(f"GET /api/users completed in {req_logger.duration_ms():.2f}ms")
            return JsonResponse(users, safe=False)

        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            
            first_name = data.get("first_name", "").strip()
            last_name = data.get("last_name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone_number", "").strip()
            password = data.get("password", "").strip()

            # Validate fields
            if not first_name or len(first_name) < 2:
                return JsonResponse({"error": "First name must be at least 2 characters"}, status=400)
            if not last_name or len(last_name) < 2:
                return JsonResponse({"error": "Last name must be at least 2 characters"}, status=400)
            if not email or not EMAIL_REGEX.match(email):
                return JsonResponse({"error": "Invalid email address"}, status=400)
            if not phone or not PHONE_REGEX.match(phone):
                return JsonResponse({"error": "Invalid phone number"}, status=400)
            if not password or len(password) < 6:
                return JsonResponse({"error": "Password must be at least 6 characters"}, status=400)

            try:
                
                user = await user_service.create_user(data)
               
            except ValueError as e:
                logger.error(f"POST /api/users failed in {req_logger.duration_ms():.2f}ms: {str(e)}")
                return JsonResponse({"error": str(e)}, status=400)
            
            logger.info(f"POST /api/users completed in {req_logger.duration_ms():.2f}ms")
            return JsonResponse({"id": user.id, "message": "User created"})

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:

        logger.error(f"ERROR {request.method} {request.path} after {req_logger.duration_ms():.2f}ms: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
async def user_detail(request, pk):
    req_logger = RequestLogger()
    try:
        user = await user_service.get_user(pk)
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)
        
        logger.info(f"GET /api/users/id completed in {req_logger.duration_ms():.2f}ms")

        if request.method == "GET":
            return JsonResponse({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "email": user.email
            })

        if request.method == "PUT":
            data = json.loads(request.body)
            await user_service.update_user(user, data)
            return JsonResponse({"message": "User updated"})

        if request.method == "DELETE":
            await user_service.delete_user(user)
            return JsonResponse({"message": "User deleted"})

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        logger.error(f"ERROR {request.method} {request.path} after {req_logger.duration_ms():.2f}ms: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)
