from rest_framework import generics
from .models import Template
from .serializers import TemplateSerializer
from rest_framework.permissions import AllowAny

class TemplateListView(generics.ListAPIView):
    queryset = Template.objects.filter(is_active=True)
    serializer_class = TemplateSerializer
    permission_classes = [AllowAny]

class TemplateDetailView(generics.RetrieveAPIView):
    queryset = Template.objects.filter(is_active=True)
    serializer_class = TemplateSerializer
    permission_classes = [AllowAny]
