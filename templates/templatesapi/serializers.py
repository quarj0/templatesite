from rest_framework import serializers
from .models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'title', 'description', 'image', 'category', 'created_at', 'download_link', 'author', 'price', 'rating']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'template', 'created_at', 'price', 'status']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
    model = Category
    field = ['id', 'name', 'description', 'created_at']
