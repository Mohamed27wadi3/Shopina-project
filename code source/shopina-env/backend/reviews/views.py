"""Review views."""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from reviews.models import Review
from reviews.serializers import ReviewSerializer, ReviewCreateSerializer
from core.permissions.custom_permissions import IsOwnerOrAdmin


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for product reviews."""
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product')
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
