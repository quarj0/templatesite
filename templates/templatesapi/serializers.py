from rest_framework import serializers
from .models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'title', 'description', 'image', 'category', 'created_at', 'download_link', 'author', 'price', 'rating']
