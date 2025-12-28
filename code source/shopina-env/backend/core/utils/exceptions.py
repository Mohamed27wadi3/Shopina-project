"""
Custom exception classes for the application.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class BusinessLogicError(APIException):
    """
    Exception raised when business logic validation fails.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic validation failed.'
    default_code = 'business_logic_error'


class InsufficientStockError(BusinessLogicError):
    """
    Exception raised when product stock is insufficient.
    """
    default_detail = 'Insufficient stock available.'
    default_code = 'insufficient_stock'


class InvalidOrderStateError(BusinessLogicError):
    """
    Exception raised when order is in invalid state for operation.
    """
    default_detail = 'Order is in invalid state for this operation.'
    default_code = 'invalid_order_state'


class PaymentError(APIException):
    """
    Exception raised when payment processing fails.
    """
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment processing failed.'
    default_code = 'payment_error'


class UnauthorizedAccessError(APIException):
    """
    Exception raised when user attempts unauthorized access.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'unauthorized_access'


class ResourceNotFoundError(APIException):
    """
    Exception raised when requested resource is not found.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Requested resource not found.'
    default_code = 'resource_not_found'


class DuplicateResourceError(BusinessLogicError):
    """
    Exception raised when attempting to create duplicate resource.
    """
    default_detail = 'Resource already exists.'
    default_code = 'duplicate_resource'


class ValidationError(BusinessLogicError):
    """
    Exception raised when data validation fails.
    """
    default_detail = 'Data validation failed.'
    default_code = 'validation_error'
