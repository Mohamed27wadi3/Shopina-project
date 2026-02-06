from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .services import build_cache_key, build_response, rate_limited, sanitize_text


@method_decorator(csrf_protect, name='dispatch')
class ChatbotMessageView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [AllowAny]

    @csrf_protect
    def post(self, request):
        message = (request.data or {}).get('message', '')
        cleaned = sanitize_text(message)
        if not cleaned:
            return Response({'detail': 'Message requis.'}, status=400)

        user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
        role = 'GUEST'
        if user:
            role = getattr(user, 'role', 'CUSTOMER') or 'CUSTOMER'

        if not request.session.session_key:
            request.session.save()

        cache_key = build_cache_key(user.id if user else None, request.session.session_key)
        if rate_limited(cache_key):
            return Response({'detail': 'Trop de requêtes. Veuillez réessayer bientôt.'}, status=429)

        reply = build_response(message, role, cache_key)
        return Response({
            'reply': reply,
            'role': role,
            'timestamp': timezone.now().isoformat(),
        })
