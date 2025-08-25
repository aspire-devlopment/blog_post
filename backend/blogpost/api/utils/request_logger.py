# api/utils/request_logger.py
import time
import logging

logger = logging.getLogger(__name__)

class RequestLogger:
    """Helper to track request duration and log messages"""

    def __init__(self):
        self.start_time = time.time()

    def duration_ms(self) -> float:
        return (time.time() - self.start_time) * 1000

  
