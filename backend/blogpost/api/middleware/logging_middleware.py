# api/middleware/request_logging.py
import time
import logging
import traceback
import os
from django.http import HttpRequest, HttpResponse, JsonResponse

# Ensure the logs folder exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure logging
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()  # also print to console
        ]
    )

class RequestLoggingMiddleware:
    """
    Middleware to log every request's method, path, duration in ms,
    and capture errors if they occur.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()

        try:
            response = self.get_response(request)
            duration_ms = (time.time() - start_time) * 1000
            logger.info(f"{request.method} {request.path} completed in {duration_ms:.2f}ms, status={response.status_code}")
            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            tb = traceback.format_exc()
            logger.error(f"ERROR {request.method} {request.path} after {duration_ms:.2f}ms: {str(e)}\n{tb}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
