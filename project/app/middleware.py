import time

from django.core.management.color import color_style


class RequestLoggingMiddleware:
    """
    Middleware to log request information and the time taken to process the request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for each request before it reaches the view.
        It processes the request and returns a response.
        """
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        duration = end_time - start_time

        print(color_style().NOTICE(f"Request to {request.path} took {duration:.4f} seconds."))

        return response
