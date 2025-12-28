"""
Global error handling middleware for consistent error responses.
"""
import logging
from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from core.utils.exceptions import BusinessLogicError


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    
    Args:
        exc: Exception instance
        context: Context dictionary
        
    Returns:
        Response object with error details
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response data
        custom_response_data = {
            'error': {
                'code': getattr(exc, 'default_code', 'error'),
                'message': str(exc),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data}
            }
        }
        response.data = custom_response_data
        
        # Log the error
        logger.error(
            f"API Error: {exc.__class__.__name__} - {str(exc)}",
            extra={
                'status_code': response.status_code,
                'path': context.get('request').path if context.get('request') else None,
                'method': context.get('request').method if context.get('request') else None,
            }
        )
    
    return response


class ErrorHandlingMiddleware:
    """
    Middleware for handling uncaught exceptions.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Process uncaught exceptions and return JSON response.
        
        Args:
            request: HTTP request
            exception: Exception instance
            
        Returns:
            JsonResponse with error details
        """
        logger.exception(
            f"Unhandled exception: {exception.__class__.__name__}",
            extra={
                'path': request.path,
                'method': request.method,
            }
        )
        
        # Return a generic error response
        return JsonResponse(
            {
                'error': {
                    'code': 'internal_server_error',
                    'message': 'An unexpected error occurred. Please try again later.',
                }
            },
            status=500
        )
