"""
Custom validation utilities.

DESIGN PATTERNS UTILISÉS:
=======================

1. STRATEGY PATTERN (Principal):
   - Chaque validateur est une stratégie différente
   - validate_price(), validate_quantity(), validate_rating() sont des stratégies
   - Permet de changer la stratégie de validation sans modifier le code métier
   - Utilisé dans ProductService et ReviewService

2. FUNCTION OBJECTS PATTERN:
   - Les validateurs sont des fonctions réutilisables
   - Peuvent être passées en paramètre (callback)
   - Composables (combiner plusieurs validateurs)

3. CHAIN OF RESPONSIBILITY PATTERN (optionnel):
   - Valider successivement: type → range → format
   - Si une validation échoue, arrêter et retourner l'erreur
   - Chaque validateur reçoit les données et décide si elles sont valides

4. SINGLE RESPONSIBILITY (SOLID S):
   - Chaque fonction valide UNE SEULE chose
   - validate_price() = valide UNIQUEMENT le prix
   - validate_quantity() = valide UNIQUEMENT la quantité
   - Pas de dépendances entre validateurs

5. INTERFACE SEGREGATION (SOLID I):
   - Chaque service importe SEULEMENT les validateurs dont il a besoin
   - ProductService importe validate_price(), pas validate_rating()
   - ReviewService importe validate_rating(), pas validate_price()
   - Pas de dépendances inutiles

UTILISATION:
is_valid, error_msg = validate_price(9.99)
if not is_valid:
    raise ValidationError(error_msg)

AVANTAGES:
✅ Validations modulaires et réutilisables
✅ Facile d'ajouter une nouvelle validation
✅ Facile de changer une stratégie de validation
✅ Code métier ne connaît pas les détails
✅ Testable (chaque fonction = un test)
"""
import re
from typing import Optional


# STRATEGY PATTERN: chaque fonction = une stratégie de validation différente
# S - Responsabilité Unique: valide UNIQUEMENT le numéro de téléphone
# I - Interface Segregation: fonction séparée, importable individuellement
def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    STRATEGY PATTERN: stratégie pour valider les téléphones
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Basic international phone number validation
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


# STRATEGY PATTERN: stratégie différente pour les codes postaux
def validate_postal_code(postal_code: str, country: str = 'US') -> bool:
    """
    Validate postal code based on country.
    STRATEGY PATTERN: stratégie selon le pays
    
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


# STRATEGY PATTERN: Stratégie pour valider les prix
# S - Responsabilité Unique: valide UNIQUEMENT le prix
# I - Interface Segregation: ProductService importe SEULEMENT cette fonction
def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """
    Validate price value.
    STRATEGY PATTERN: stratégie pour valider les prix
    
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


# STRATEGY PATTERN: Stratégie différente pour la quantité
def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """
    Validate quantity value.
    STRATEGY PATTERN: stratégie pour valider les quantités
    
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


# STRATEGY PATTERN: Stratégie pour valider les notes
# S - Responsabilité Unique: ReviewService importe SEULEMENT cette fonction
# I - Interface Segregation: ProductService n'a pas besoin d'importer
def validate_rating(rating: float) -> tuple[bool, Optional[str]]:
    """
    Validate rating value.
    STRATEGY PATTERN: stratégie pour valider les notes
    
    Args:
        rating: Rating to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if rating < 0 or rating > 5:
        return False, "Rating must be between 0 and 5"
    return True, None
