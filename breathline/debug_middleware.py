import logging

logger = logging.getLogger(__name__)

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.warning(f"DEBUG REQ: {request.method} {request.path_info}")
        return self.get_response(request)
