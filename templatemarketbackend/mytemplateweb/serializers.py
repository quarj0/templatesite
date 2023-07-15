from rest_framework import serializers
from .models import Template, UserProfile, Order, Category


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            "id",
            "title",
            "description",
            "image",
            "category",
            "created_at",
            "download_link",
            "author",
            "is_free",
            "price",
            "rating",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "email", "password"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "template", "order_date", "status"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "city",
            "phone",
            "address",
        ]


class TemplateCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            "title",
            "description",
            "image",
            "category",
            "download_link",
            "author",
            "is_free",
            "price",
        ]