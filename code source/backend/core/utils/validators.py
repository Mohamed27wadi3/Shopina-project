"""
Custom validation utilities.
"""
import re
from typing import Optional


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Basic international phone number validation
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


def validate_postal_code(postal_code: str, country: str = 'US') -> bool:
    """
    Validate postal code based on country.
    
    Args:
        postal_code: Postal code to validate
        country: Country code (default: US)
        
    Returns:
        True if valid, False otherwise
    """
    patterns = {
        'US': r'^\d{5}(-\d{4})?$',
        'FR': r'^\d{5}$',
        'UK': r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$',
        'CA': r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$',
    }
    
    pattern = patterns.get(country, r'^\d{4,10}$')  # Default pattern
    return bool(re.match(pattern, postal_code.upper()))


def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """
    Validate price value.
    
    Args:
        price: Price to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if price < 0:
        return False, "Price cannot be negative"
    if price > 999999.99:
        return False, "Price exceeds maximum allowed value"
    return True, None


def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """
    Validate quantity value.
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if quantity < 1:
        return False, "Quantity must be at least 1"
    if quantity > 10000:
        return False, "Quantity exceeds maximum allowed value"
    return True, None


def validate_rating(rating: float) -> tuple[bool, Optional[str]]:
    """
    Validate rating value.
    
    Args:
        rating: Rating to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if rating < 0 or rating > 5:
        return False, "Rating must be between 0 and 5"
    return True, None
