from rest_framework import permissions


class Is2FAVerified(permissions.BasePermission):
    """Permission that requires email 2FA verification for non-safe methods.

    - If the user has `two_factor_enabled` False -> allow
    - If request.method is safe (GET, HEAD, OPTIONS) -> allow
    - Otherwise require a session flag '2fa_verified_{user.id}' == True
    """

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False

        if not getattr(user, 'two_factor_enabled', False):
            return True

        # Allow read-only access even when 2FA is required
        if request.method in permissions.SAFE_METHODS:
            return True

        session_key = f'2fa_verified_{user.id}'
        return bool(request.session.get(session_key, False))
