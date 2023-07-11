from rest_framework import generics
from .models import Template
from .serializers import TemplateSerializer

class TemplateList(generics.ListAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
